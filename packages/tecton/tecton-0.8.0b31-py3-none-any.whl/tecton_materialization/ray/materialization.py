import base64
import os
import time
import urllib
from functools import partial
from typing import Optional

import pendulum
import ray
from google.protobuf import timestamp_pb2
from snowflake.connector import SnowflakeConnection

import tecton_core.query.dialect
from tecton_core import specs
from tecton_core.duckdb_context import DuckDBContext
from tecton_core.fco_container import create_fco_container
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.id_helper import IdHelper
from tecton_core.query.builder import build_materialization_querytree
from tecton_core.query.dialect import Dialect
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_unified_tecton_data_source_dialect
from tecton_core.query.node_utils import pipeline_has_aggregations
from tecton_core.query.node_utils import pipeline_has_odfvs
from tecton_core.query.query_tree_compute import DuckDBCompute
from tecton_core.query.query_tree_compute import PandasCompute
from tecton_core.query.query_tree_compute import SnowflakeCompute
from tecton_core.query.query_tree_executor import QueryTreeExecutor
from tecton_materialization.ray import delta
from tecton_materialization.ray.job_status import create_stage_monitor
from tecton_materialization.ray.nodes import AddTimePartitionNode
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage
from tecton_proto.materialization.params_pb2 import MaterializationTaskParams
from tecton_proto.online_store_writer.copier_pb2 import DeletionRequest
from tecton_proto.online_store_writer.copier_pb2 import LocalFileStage
from tecton_proto.online_store_writer.copier_pb2 import ObjectCopyRequest
from tecton_proto.online_store_writer.copier_pb2 import OnlineStoreCopierRequest
from tecton_proto.online_store_writer.copier_pb2 import S3Stage
from tecton_proto.online_store_writer.copier_pb2 import StatusUpdateRequest
from tecton_proto.online_store_writer.copier_pb2 import TimestampUnit


def _get_batch_materialization_plan(
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinition,
) -> NodeRef:
    feature_start_time = materialization_task_params.batch_task_info.batch_parameters.feature_start_time.ToDatetime()
    feature_end_time = materialization_task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
    feature_data_time_limits = pendulum.instance(feature_end_time) - pendulum.instance(feature_start_time)

    tree = build_materialization_querytree(
        dialect=Dialect.DUCKDB,
        fdw=fd,
        for_stream=False,
        feature_data_time_limits=feature_data_time_limits,
    )
    return AddTimePartitionNode.for_feature_definition(fd, tree)


def _prepare_qt_executor(
    qt: NodeRef,
    snowflake_connection: Optional[SnowflakeConnection],
    materialization_task_params: MaterializationTaskParams,
) -> "QueryTreeExecutor":
    monitor_for_stage = partial(create_stage_monitor, materialization_task_params=materialization_task_params)
    duckdb_compute = DuckDBCompute(session=DuckDBContext.get_instance().get_connection())
    pandas_compute = PandasCompute(sql_compute=duckdb_compute)

    ds_dialect = get_unified_tecton_data_source_dialect(qt)
    data_source_compute = duckdb_compute
    if ds_dialect == tecton_core.query.dialect.Dialect.PANDAS:
        data_source_compute = pandas_compute.with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.PYTHON, "Loading dataset with Pandas")
        )
    elif ds_dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
        data_source_compute = (
            SnowflakeCompute.for_connection(snowflake_connection)
            if snowflake_connection is not None
            else SnowflakeCompute.for_query_tree(qt)
        ).with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.SNOWFLAKE, "Loading dataset from Snowflake")
        )

    pipeline_dialect = get_pipeline_dialect(qt)
    # No pipeline dialect happens in the case of e.g. stream ingest api
    if pipeline_dialect is None:
        pipeline_compute = duckdb_compute.with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.PYTHON, "Processing dataset in DuckDB")
        )
    elif pipeline_dialect == tecton_core.query.dialect.Dialect.PANDAS:
        pipeline_compute = pandas_compute.with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.PYTHON, "Processing dataset in Pandas")
        )
    elif pipeline_dialect == tecton_core.query.dialect.Dialect.SNOWFLAKE:
        pipeline_compute = (
            SnowflakeCompute.for_connection(snowflake_connection)
            if snowflake_connection is not None
            else SnowflakeCompute.for_query_tree(qt)
        ).with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.SNOWFLAKE, "Processing dataset in Snowflake")
        )
    else:
        msg = f"Unexpected pipeline dialect: {pipeline_dialect}"
        raise ValueError(msg)

    agg_compute = duckdb_compute
    if pipeline_has_aggregations(qt):
        agg_compute = agg_compute.with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.AGGREGATE, "Compute aggregations")
        )

    odfv_compute = pandas_compute
    if pipeline_has_odfvs(qt):
        odfv_compute = odfv_compute.with_monitoring_ctx(
            monitor_for_stage(TectonManagedStage.StageType.PYTHON, "Compute on-demand features")
        )
    executor = QueryTreeExecutor(
        data_source_compute=data_source_compute,
        pipeline_compute=pipeline_compute,
        agg_compute=agg_compute,
        odfv_compute=odfv_compute,
    )

    return executor


def _write_to_online_store(
    materialization_task_params: MaterializationTaskParams,
    fd: FeatureDefinition,
    stage_uri_str: str,
) -> None:
    stage_uri = urllib.parse.urlparse(stage_uri_str)
    if stage_uri.scheme in ("file", ""):
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            object_copy_request=ObjectCopyRequest(
                local_file_stage=LocalFileStage(location=stage_uri.path), timestamp_units=TimestampUnit.MICROS
            ),
        )
    elif stage_uri.scheme == "s3":
        key = stage_uri.path
        if key.startswith("/"):
            key = key[1:]
        request = OnlineStoreCopierRequest(
            online_store_writer_configuration=materialization_task_params.online_store_writer_config,
            feature_view=materialization_task_params.feature_view,
            object_copy_request=ObjectCopyRequest(
                s3_stage=S3Stage(
                    bucket=stage_uri.netloc,
                    key=key,
                ),
                timestamp_units=TimestampUnit.MICROS,
            ),
        )
    else:
        msg = f"Unexpected staging uri scheme: {stage_uri.scheme}"
        raise NotImplementedError(msg)
    _run_online_store_copier(request)

    # Issue status update
    if fd.is_temporal or fd.is_continuous:
        status_update = StatusUpdateRequest(
            materialized_raw_data_end_time=materialization_task_params.batch_task_info.batch_parameters.feature_end_time
        )
    else:
        anchor_time = (
            materialization_task_params.batch_task_info.batch_parameters.feature_end_time.ToDatetime()
            - fd.aggregate_slide_interval.ToTimedelta()
        )
        anchor_time_pb = timestamp_pb2.Timestamp()
        anchor_time_pb.FromDatetime(anchor_time)
        status_update = StatusUpdateRequest(anchor_time=anchor_time_pb)
    status_request = OnlineStoreCopierRequest(
        online_store_writer_configuration=materialization_task_params.online_store_writer_config,
        feature_view=materialization_task_params.feature_view,
        status_update_request=status_update,
    )
    _run_online_store_copier(status_request)


def _delete_from_online_store(materialization_task_params: MaterializationTaskParams) -> None:
    if materialization_task_params.deletion_task_info.deletion_parameters.HasField("online_join_keys_path"):
        deletion_request = DeletionRequest(
            online_join_keys_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_path,
        )
    else:
        deletion_request = DeletionRequest(
            online_join_keys_full_path=materialization_task_params.deletion_task_info.deletion_parameters.online_join_keys_full_path,
        )
    request = OnlineStoreCopierRequest(
        online_store_writer_configuration=materialization_task_params.online_store_writer_config,
        feature_view=materialization_task_params.feature_view,
        deletion_request=deletion_request,
    )
    _run_online_store_copier(request)


def _run_online_store_copier(request):
    request_bytes = request.SerializeToString()
    runner_function = ray.cross_language.java_function(
        "com.tecton.onlinestorewriter.OnlineStoreCopier", "runFromSerializedRequest"
    )
    job = runner_function.remote(request_bytes, None)
    ray.get(job)


def ray_main() -> None:
    encoded_params = os.environ.get("MATERIALIZATION_TASK_PARAMS")
    _ray_main_helper(encoded_params)


def _should_write_to_online_store(materialization_params: MaterializationTaskParams):
    return materialization_params.batch_task_info.batch_parameters.write_to_online_feature_store


def _ray_main_helper(
    encoded_params: Optional[str],
    snowflake_connection_override: Optional[SnowflakeConnection] = None,
) -> None:
    if encoded_params is None:
        msg = "Materialization job cannot proceed since MATERIALIZATION_TASK_PARAMS is not set."
        raise RuntimeError(msg)
    _init_ray()
    materialization_task_params = _deserialize_materialization_task_params(encoded_params)
    assert materialization_task_params.feature_view.schemas.HasField("materialization_schema"), "missing schema"

    fd = _get_feature_definition(materialization_task_params)

    if materialization_task_params.HasField("deletion_task_info"):
        _delete_from_online_store(materialization_task_params)
    else:
        assert fd.writes_to_offline_store, f"Offline materialization is required for FeatureView {fd.id} ({fd.name})"
        assert fd.has_delta_offline_store, f"Delta is required for FeatureView {fd.id} ({fd.name})"

        qt = _get_batch_materialization_plan(materialization_task_params, fd)
        executor = _prepare_qt_executor(qt, snowflake_connection_override, materialization_task_params)
        offline_stage_monitor = create_stage_monitor(
            TectonManagedStage.StageType.OFFLINE_STORE, "Unload features to offline store", materialization_task_params
        )
        online_stage_monitor = (
            create_stage_monitor(
                TectonManagedStage.StageType.ONLINE_STORE,
                "Unload features to online store",
                materialization_task_params,
            )
            if _should_write_to_online_store(materialization_task_params)
            else None
        )

        try:
            materialized_data = executor.exec_qt(qt).result_table
        finally:
            executor.cleanup()

        interval = delta.TimeInterval(
            start=materialization_task_params.batch_task_info.batch_parameters.feature_start_time,
            end=materialization_task_params.batch_task_info.batch_parameters.feature_end_time,
        )

        with offline_stage_monitor() as progress_callback:
            delta_writer = delta.DeltaWriter(
                fd,
                table_uri=materialization_task_params.offline_store_path,
                dynamodb_log_table_name=materialization_task_params.delta_log_table,
                dynamodb_log_table_region=materialization_task_params.dynamodb_table_region,
                progress_callback=progress_callback,
            )
            parts = delta_writer.write(materialized_data)
            delta_writer.commit(interval)

        if _should_write_to_online_store(materialization_task_params):
            with online_stage_monitor() as progress_callback:
                # TODO(meastham): Probably should send these all at once to the online store copier
                for uri in parts:
                    _write_to_online_store(materialization_task_params, fd, uri)

                progress_callback(1.0)


def _init_ray():
    print(f"Initializing Ray from classpath: {os.environ['CLASSPATH']}")
    ray.init(job_config=ray.job_config.JobConfig(code_search_path=os.environ["CLASSPATH"].split(":")))


def _get_feature_definition(materialization_task_params):
    fco_container = create_fco_container(
        list(materialization_task_params.virtual_data_sources) + list(materialization_task_params.transformations),
        deserialize_funcs_to_main=True,
    )
    fv_spec = specs.create_feature_view_spec_from_data_proto(materialization_task_params.feature_view)
    fd = FeatureDefinition(fv_spec, fco_container)
    return fd


def _init_job_metadata_table_for_tests(materialization_task_params):
    from tecton_materialization.common import job_metadata

    dynamodb = job_metadata._dynamodb_client(materialization_task_params)
    attempt_id = IdHelper.to_string(materialization_task_params.attempt_id)
    now_seconds = int(time.time())
    empty_metadata = job_metadata.JobMetadata()
    dynamodb.put_item(
        TableName=materialization_task_params.job_metadata_table,
        Item={
            job_metadata.JOB_EXEC_PKEY_ATTRIBUTE: {"S": attempt_id},
            job_metadata.JOB_EXEC_LAST_UPDATED_ATTRIBUTE: {"N": str(now_seconds)},
            job_metadata.JOB_EXEC_DATA_ATTRIBUTE: {"B": empty_metadata.SerializeToString()},
            job_metadata.JOB_EXEC_VERSION_ATTRIBUTE: {"N": "1"},
        },
    )


def local_test_main(mat_params_path, snowflake_connection):
    os.environ["DUCKDB_DEBUG"] = "True"
    with open(mat_params_path, "r") as f:
        serialized_params = f.read()
    # Init DuckDB with a home dir override, which is used for writing temp files that are cleaned up
    # automatically
    duckdb_context = DuckDBContext.get_instance(home_dir_override=os.environ["TEST_TMPDIR"])
    duckdb_context.get_connection().sql("SET threads TO 1;")

    _init_job_metadata_table_for_tests(_deserialize_materialization_task_params(serialized_params))

    _ray_main_helper(
        serialized_params,
        snowflake_connection,
    )


def _deserialize_materialization_task_params(
    encoded_params: str,
) -> MaterializationTaskParams:
    params = MaterializationTaskParams()
    params.ParseFromString(base64.standard_b64decode(encoded_params))
    return params


if __name__ == "__main__":
    ray_main()
