import json
import pathlib
import sys
import time
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    Mapping,
    Sequence,
    Tuple,
    cast,
)

import gql  # type: ignore
import pandas as pd
import pyarrow as pa  # type: ignore
import requests
from IPython.display import HTML, display  # type: ignore
from httpx import AsyncClient, TimeoutException, HTTPStatusError, NetworkError
from requests.adapters import HTTPAdapter, Retry
from tenacity import AsyncRetrying, stop_after_attempt, retry_if_exception_type

from .auth import _PlatformAuth
from .inference_result import InferenceResult
from .logs import LogEntries
from .model_config import ModelConfig
from .object import *
from .utils import is_arrow_enabled, flatten_np_array_columns
from .wallaroo_ml_ops_api_client.api.pipelines import pipelines_undeploy
from .wallaroo_ml_ops_api_client.models import pipelines_undeploy_json_body
from .wallaroo_ml_ops_api_client.types import UNSET

if TYPE_CHECKING:
    from .client import Client
    from .model_version import ModelVersion
    from .pipeline_version import PipelineVersion

ARROW_HEADER = "application/vnd.apache.arrow.file"
ARROW_FORMAT = "arrow"
PANDAS_RECORDS_HEADER = "application/json; format=pandas-records"
PANDAS_RECORDS_FORMAT = "pandas-records"
JSON_HEADER = "application/json"
CUSTOM_JSON_FORMAT = "custom-json"
DEFAULT_RETRIES = 1


class WaitForError(Exception):
    def __init__(self, message: str, status: Optional[Dict[str, Any]]):
        super().__init__(message)
        self.status = status


class WaitForDeployError(RuntimeError):
    def __init__(self, message: str):
        super().__init__(message)

    def _render_traceback_(self):
        display(
            HTML(
                "<strong>*** An error occurred while deploying your pipeline.</strong>"
            )
        )
        return [str(self)]


def hack_pandas_dataframe_order(df):
    order = {"time": 0, "in": 1, "out": 2}

    def key_col(name):
        parts = name.split(".")
        return [order.get(parts[0], len(order)), *parts[1:]]

    reorder = list(df.columns)
    reorder.sort(key=key_col)

    return df[reorder]


class Deployment(Object):
    def __init__(self, client: Optional["Client"], data: Dict[str, Any]) -> None:
        self.client = client
        assert client is not None
        # TODO: revisit session initialization during connection pooling work
        self.session = self._initialize_session()
        super().__init__(gql_client=client._gql_client, data=data)

    def _fill(self, data: Dict[str, Any]) -> None:
        """Fills an object given a response dictionary from the GraphQL API.

        Only the primary key member must be present; other members will be
        filled in via rehydration if their corresponding member function is
        called.
        """
        from .pipeline_version import PipelineVersion  # avoids circular imports

        for required_attribute in ["id"]:
            if required_attribute not in data:
                raise RequiredAttributeMissing(
                    self.__class__.__name__, required_attribute
                )
        self._id = data["id"]

        self._name = value_if_present(data, "deploy_id")
        self._deployed = value_if_present(data, "deployed")
        self._model_configs = (
            [
                ModelConfig(self.client, elem["model_config"])
                for elem in data["deployment_model_configs"]
            ]
            if "deployment_model_configs" in data
            else DehydratedValue()
        )
        self._pipeline_versions = (
            [
                PipelineVersion(self.client, elem["pipeline_version"])
                for elem in data["deployment_pipeline_versions"]
            ]
            if "deployment_pipeline_versions" in data
            else DehydratedValue()
        )

        self._pipeline_id = value_if_present(data, "pipeline_id")
        self._pipeline_name = value_if_present(data, "pipeline.pipeline_id")
        self._engine_config = value_if_present(data, "engine_config")

    def _fetch_attributes(self) -> Dict[str, Any]:
        """Fetches all member data from the GraphQL API."""
        return self._gql_client.execute(
            gql.gql(
                """
            query DeploymentById($deployment_id: bigint!) {
                deployment_by_pk(id: $deployment_id) {
                    id
                    deploy_id
                    deployed
                    deployment_model_configs {
                        model_config {
                            id
                        }
                    }
                    deployment_pipeline_versions(order_by: {pipeline_version: {id: desc}}) {
                        pipeline_version {
                            id
                        }
                    }
                    pipeline {
                        pipeline_id
                    }
                    engine_config
                }
            }
            """
            ),
            variable_values={
                "deployment_id": self._id,
            },
        )["deployment_by_pk"]

    def _initialize_session(self) -> requests.Session:
        # TODO: make session initialization configurable
        #  to be informed by connection polling reqs.
        #  includes sane defaults to match current retry time (~45s)
        session = requests.Session()
        retries = Retry(
            total=10,
            backoff_factor=0.1,
            status_forcelist=[503],
            allowed_methods=["GET", "POST"],
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        return session

    def id(self) -> int:
        return self._id

    @rehydrate("_name")
    def name(self) -> str:
        return cast(str, self._name)

    @rehydrate("_deployed")
    def deployed(self) -> bool:
        return cast(bool, self._deployed)

    @rehydrate("_model_configs")
    def model_configs(self) -> List[ModelConfig]:
        return cast(List[ModelConfig], self._model_configs)

    @rehydrate("_pipeline_versions")
    def pipeline_versions(self) -> List["PipelineVersion"]:
        from .pipeline_version import PipelineVersion  # avoids circular imports

        return cast(List[PipelineVersion], self._pipeline_versions)

    @rehydrate("_pipeline_name")
    def pipeline_name(self) -> str:
        return cast(str, self._pipeline_name)

    @rehydrate("engine_config")
    def engine_config(self) -> Dict[str, Any]:
        return cast(Dict[str, Any], self._engine_config)

    def deploy(self) -> "Deployment":
        """Deploys this deployment, if it is not already deployed.

        If the deployment is already deployed, this is a no-op.
        """
        q = gql.gql(
            """
        mutation Deploy($id: bigint!) {
            update_deployment_by_pk(pk_columns: {id: $id} _set: { deployed: true }) {
                id
                deploy_id
                deployed
            }
        }
        """
        )
        variables = {"id": self.id()}
        assert self.client is not None
        self.client._gql_client.execute(q, variable_values=variables)
        self._rehydrate()
        return self

    def undeploy(self) -> "Deployment":
        """Shuts down this deployment, if it is deployed.

        If the deployment is already undeployed, this is a no-op.
        """
        # TODO: Error handling.
        assert self.client is not None

        data = pipelines_undeploy.sync_detailed(
            client=self.client.mlops(),
            json_body=pipelines_undeploy_json_body.PipelinesUndeployJsonBody(
                UNSET, self.id()
            ),
        )

        if data.status_code != 200:
            err = data.content.decode("utf-8")
            raise Exception(f"Failed to undeploy. {err}")

        self._rehydrate()
        return self.wait_for_undeployed()

    def _get_auth(self):
        # TODO: Digging the auth object out of the gql_client is cheating
        return self.client._gql_client.transport.auth

    def status(self) -> Dict[str, Any]:
        """Returns a dict of deployment status useful for determining if a deployment has succeeded.

        :return: Dict of deployment internal state information.
        :rtype: Dict[str, Any]
        """

        assert self.client is not None

        status_url = f"{self.client.api_endpoint}/v1/api/status/get_deployment"
        params = {"name": f"{self.name()}-{self.id()}"}

        kind = ""
        resp = None
        try:
            resp = requests.post(
                status_url,
                timeout=5,
                auth=self._get_auth(),
                json=params,
            )
            kind = ""
        except requests.ReadTimeout as ex:
            raise CommunicationError(f"rest-api connection to {status_url}")
        except Exception:
            kind = "comm"

        if resp is not None and resp.status_code == 200:
            res = resp.json()
            if res is not None and res["status"] == "Running":
                # retry for a running status
                return res

        details = ""
        if resp is not None:
            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 404:
                raise EntityNotFoundError(
                    f"Deployment not found", {"name": self.name()}
                )

            details = f"\nStatus code: {resp.status_code}\nMessage: {resp.text}"

        if kind == "comm":
            raise CommunicationError(f"rest-api connection to {status_url}")

        raise RuntimeError(f"Unable to query deployment status {status_url}{details}")

    def check_limit_status(self):
        q = gql.gql(
            """
            query QueryLimitStatus($id: bigint!) {
                deployment(where: {id: {_eq: $id}}) {
                    id
                    deployed
                    limit_status
                }
            }
            """
        )

        variables = {"id": self.id()}
        assert self.client is not None
        res = self.client._gql_client.execute(q, variable_values=variables)[
            "deployment"
        ]
        if len(res) > 0:
            status = res[0]
            if "limit_status" in status:
                limit_status = status["limit_status"]
                if limit_status is not None:
                    raise LimitError(limit_status)

    def _wait_for(
        self,
        poll_fn: Callable[[], Tuple[bool, str, str]],
        task_name: str,
        on_iter: Callable[[int], None] = lambda ix: None,
        timeout: Optional[int] = None,
    ) -> "Deployment":
        """Wait for a generic task to finish before completing.

        Will wait up "timeout_request" seconds for the deployment to enter that state. This is set


        :return: The deployment, for chaining.
        :rtype: Deployment
        """
        assert self.client is not None
        warning = False
        duration = timeout if timeout is not None else self.client.timeout
        message = "(none)"
        kind = "unset"

        start = time.monotonic()
        ix = 0
        while ix == 0 or time.monotonic() - start < duration:
            on_iter(ix)
            ix += 1

            res, message, kind = poll_fn()
            if res:
                if self.client._interactive:
                    sys.stdout.write(" ok\n")
                return self

            if self.client._interactive:
                if not warning:
                    sys.stdout.write(
                        f"Waiting for {task_name} - this will take up to {duration}s "
                    )
                    warning = True
                time.sleep(1)
                sys.stdout.write(".")
            else:
                time.sleep(1)

        if kind == "comm":
            raise CommunicationError(message)
        else:
            try:
                status: Optional[Dict[str, Any]] = self.status()
                message = f"{task_name.capitalize()} failed. See status for details."
            except:
                message = f"{task_name.capitalize()} did not finish within {duration}s."
                status = None
            raise WaitForError(message, status)

    def wait_for_running(self, timeout: Optional[int] = None) -> "Deployment":
        """Waits for the deployment status to enter the "Running" state.

        Will wait up "timeout_request" seconds for the deployment to enter that state. This is set
        in the "Client" object constructor. Will raise various exceptions on failures.

        :return: The deployment, for chaining.
        :rtype: Deployment
        """

        def check_limit(ix: int) -> None:
            # If this checks immediately, it will happen too soon for the deployment manager to
            # have cleared the limit_status column on the deployment and this will fail erroneously
            if ix > 5:
                self.check_limit_status()

        def check_for_running() -> Tuple[bool, str, str]:
            try:
                res = self.status()
                if res is not None and res["status"] == "Running":
                    return True, "", ""
                return False, "not running", "runtime"
            except CommunicationError as ex:
                # Connection may be coming up, try again
                return False, str(ex), "comm"
            except (EntityNotFoundError, RuntimeError) as ex:
                # Not found may switch to found, after a while. Retry it.
                return False, f"not found {ex}", "runtime"

        try:
            return self._wait_for(check_for_running, "deployment", check_limit, timeout)
        except WaitForError as ex:
            status = ex.status
            message = f"{str(ex)}\nStatus: {str(status)}"
            if status is not None and status.get("status") == "Error":
                quantity, resource = None, None
                engines = status.get("engines", [])
                engine_lbs = status.get("engine_lbs", [])
                required_cpu = next(
                    filter(
                        lambda item: item.get("status") == "Pending"
                        and item.get("required_cpu"),
                        engines + engine_lbs,
                    ),
                    cast(Dict[str, Any], {}),
                ).get("required_cpu")
                if required_cpu:
                    resource = "CPU"
                    quantity = (
                        "one CPU"
                        if required_cpu == "1"
                        else f"{required_cpu} units of CPU"
                    )
                else:
                    required_memory = next(
                        filter(
                            lambda item: item.get("status") == "Pending"
                            and item.get("required_memory"),
                            engines + engine_lbs,
                        ),
                        cast(Dict[str, Any], {}),
                    ).get("required_memory")
                    if required_memory:
                        resource = "memory"
                        quantity = f"{required_memory} of memory"

                if quantity is not None and resource is not None:
                    message = (
                        "Cannot deploy pipeline due to insufficient resources. "
                        f"Your pipeline needs {quantity} to run but there is not enough {resource} currently available. "
                        "Please try again or un-deploy pipelines not in use to adjust the resources that are available for your Wallaroo instance. "
                        "Contact your Wallaroo platform administrator for additional support."
                    )

            raise WaitForDeployError(message)

    def wait_for_undeployed(self) -> "Deployment":
        """Waits for the deployment to end.

        Will wait up "timeout_request" seconds for the deployment to enter that state. This is set
        in the "Client" object constructor. Will raise various exceptions on failures.

        :return: The deployment, for chaining.
        :rtype: Deployment
        """

        def check_for_undeployed() -> Tuple[bool, str, str]:
            try:
                self.status()
                return False, "still running", "runtime"
            except CommunicationError as ex:
                # Connection may be coming up, try again
                return False, str(ex), "comm"
            except RuntimeError as ex:
                # Not found may switch to found, after a while. Retry it.
                return False, f"not found {ex}", "runtime"
            except EntityNotFoundError:
                return True, "", ""

        try:
            return self._wait_for(check_for_undeployed, "undeployment")
        except WaitForError as ex:
            message = f"{str(ex)}\nStatus: {str(ex.status)}"
            raise RuntimeError(message)

    @staticmethod
    def _write_table_to_arrow_file(table: pa.Table, schema: pa.Schema):
        sink = pa.BufferOutputStream()
        with pa.ipc.new_file(sink, schema) as arrow_ipc:
            arrow_ipc.write(table)
            arrow_ipc.close()
        return sink.getvalue()

    @staticmethod
    def _init_infer_params(
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = dict()
        default_dataset_exclude = ["metadata"]
        if dataset is not None:
            if "metadata" in dataset:
                default_dataset_exclude = []
        params["dataset[]"] = dataset or ["*"]  # type: ignore
        params["dataset.exclude[]"] = (
            [*dataset_exclude, *default_dataset_exclude]
            if dataset_exclude is not None
            else default_dataset_exclude
        )
        params["dataset.separator"] = dataset_separator or "."  # type: ignore
        return params

    @staticmethod
    def _init_timeout(timeout: Optional[Union[int, float]]) -> float:
        if timeout is None:
            timeout = 15
        if not isinstance(timeout, (int, float)):
            raise TypeError(
                f"timeout is {type(timeout)} but 'int' or 'float' is required"
            )
        return timeout

    def _infer_with_pandas(
        self,
        tensor: pd.DataFrame,
        params: Mapping[str, Union[str, Sequence[str]]],
        timeout: Optional[Union[int, float]],
    ) -> pd.DataFrame:
        for col in tensor.columns:
            tensor[col] = flatten_np_array_columns(tensor, col)
        input_records = tensor.to_json(orient="records")
        headers = {
            "Content-Type": PANDAS_RECORDS_HEADER,
        }
        res = self._make_infer_request(
            data=input_records,
            headers=headers,
            params=params,
            timeout=timeout,
        )
        try:
            data = res.json()
        except (json.JSONDecodeError, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err
        data_df = pd.DataFrame.from_records(data)
        data_df["time"] = pd.to_datetime(data_df["time"], unit="ms")
        data_df["check_failures"] = data_df["check_failures"].apply(len)
        return hack_pandas_dataframe_order(data_df)

    def _infer_with_arrow(
        self,
        tensor: pa.Table,
        params: Mapping[str, Union[str, Sequence[str]]],
        timeout: Optional[Union[int, float]],
    ) -> pa.Table:
        assert self.client is not None

        input_arrow = self._write_table_to_arrow_file(tensor, tensor.schema)
        headers = {
            "Content-Type": ARROW_HEADER,
            "format": ARROW_FORMAT,
            "Accept": ARROW_HEADER,
        }
        res = self._make_infer_request(
            data=input_arrow,
            headers=headers,
            params=params,
            timeout=timeout,
        )
        try:
            with pa.ipc.open_file(res.content) as reader:
                data_table = reader.read_all()
        except (pa.ArrowInvalid, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err
        cleanedup_data_table = self.client.cleanup_arrow_data_for_display(data_table)
        return cleanedup_data_table

    def _infer_with_json(
        self,
        tensor: Union[dict, list],
        timeout: Optional[Union[int, float]],
    ) -> List[InferenceResult]:
        headers = {
            "Content-Type": JSON_HEADER,
            "Accept": JSON_HEADER,
        }
        try:
            res = self.session.post(
                self._url(),
                json=tensor,
                timeout=timeout,
                # TODO: Digging the auth object out of the gql_client is cheating
                auth=self._get_auth(),
                headers=headers,
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise InferenceError(json.loads(http_error.response.text)[0])
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ReadTimeout,
            requests.exceptions.RequestException,
        ):
            raise RuntimeError(
                f"Inference did not return within {timeout}s, adjust if necessary"
            )

        try:
            data = res.json()
        except (json.JSONDecodeError, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err
        if is_arrow_enabled():
            return data
        return [InferenceResult(self._gql_client, d) for d in data]

    def _make_infer_request(
        self,
        data: Union[Dict[str, Any], pd.DataFrame],
        headers: Dict[str, str],
        params: Mapping[str, Union[str, Sequence[str]]],
        timeout: Optional[Union[int, float]] = None,
    ) -> requests.Response:
        try:
            res = self.session.post(
                self._url(),
                data=data,
                timeout=timeout,
                # TODO: Digging the auth object out of the gql_client is cheating
                auth=self._get_auth(),
                params=params,
                headers=headers,
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            raise InferenceError(json.loads(http_error.response.text)[0])
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ReadTimeout,
            requests.exceptions.RequestException,
        ):
            raise RuntimeError(
                f"Inference did not return within {timeout}s, adjust if necessary"
            )

        return res

    def infer(
        self,
        tensor: Union[Dict[str, Any], List[Any], pd.DataFrame, pa.Table],
        timeout: Optional[Union[int, float]] = None,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
    ):
        """
        Returns an inference result on this deployment, given a tensor.
        :param: tensor: Union[Dict[str, Any], List[Any], pd.DataFrame, pa.Table]. The tensor to be sent to run inference on.
        :param: timeout: Optional[Union[int, float]] infer requests will time out after
            the amount of seconds provided are exceeded. timeout defaults
            to 15 secs.
        :param: dataset: Optional[List[str]] By default this is set to ["*"] which returns,
            ["time", "in", "out", "check_failures"]. Other available options - ["metadata"]
        :param: dataset_exclude: Optional[List[str]] If set, allows user to exclude parts of dataset.
        :param: dataset_separator: Optional[str] If set to ".", returned dataset will be flattened.
        :return: InferenceResult in dictionary, dataframe or arrow format.
        """

        timeout = self._init_timeout(timeout)

        if is_arrow_enabled():
            params = self._init_infer_params(
                dataset, dataset_exclude, dataset_separator
            )
            if not isinstance(tensor, (pd.DataFrame, pa.Table, dict, list)):
                raise TypeError(
                    f"tensor is of type {type(tensor)} but 'pandas.DataFrame', 'pyarrow.Table', dict or list is required"
                )
            if isinstance(tensor, pd.DataFrame):
                return self._infer_with_pandas(tensor, params, timeout)
            elif isinstance(tensor, pa.Table):
                return self._infer_with_arrow(tensor, params, timeout)
            elif isinstance(tensor, (dict, list)):
                return self._infer_with_json(tensor, timeout)
        else:
            if not isinstance(tensor, dict):
                raise TypeError(f"tensor is {type(tensor)} but 'dict' is required")
            return self._infer_with_json(tensor, timeout)

    def infer_from_file(
        self,
        filename: Union[str, pathlib.Path],
        data_format: Optional[str] = None,
        timeout: Optional[Union[int, float]] = None,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
    ) -> Union[List[InferenceResult], pd.DataFrame, pa.Table]:
        """
        This method is used to run inference on a deployment using a file. The file can be in one of the following
        formats: pandas.DataFrame: .arrow, .json which contains data either in the pandas.records format
        or wallaroo custom json format.
        :param: filename: Union[str, pathlib.Path]. The file to be sent to run inference on.
        :param: data_format: Optional[str]. The format of the data in the file. If not provided, the format will be
            inferred from the file extension.
        :param: timeout: Optional[Union[int, float]] infer requests will time out after the amount of seconds provided are
            exceeded. timeout defaults to 15 secs.
        :param: dataset: Optional[List[str]] By default this is set to ["*"] which returns,
            ["time", "in", "out", "check_failures"]. Other available options - ["metadata"]
        :param: dataset_exclude: Optional[List[str]] If set, allows user to exclude parts of dataset.
        :param: dataset_separator: Optional[str] If set to ".", returned dataset will be flattened.
        :return: InferenceResult in dictionary, dataframe or arrow format.
        """
        if not isinstance(filename, pathlib.Path):
            filename = pathlib.Path(filename)
        if is_arrow_enabled():
            if data_format:
                if data_format == PANDAS_RECORDS_FORMAT:
                    tensor = pd.read_json(filename, orient="records")
                elif data_format == CUSTOM_JSON_FORMAT:
                    with filename.open("rb") as f:
                        tensor = json.load(f)
                elif data_format == ARROW_FORMAT:
                    with pa.ipc.open_file(filename) as source:
                        tensor = source.read_all()
                else:
                    raise TypeError(
                        f"Not an accepted data_format, it can only be 'pandas-record', 'custom-json' or 'arrow'."
                    )
            else:
                if filename.suffix.lower() == ".arrow":
                    with pa.ipc.open_file(filename) as source:
                        tensor = source.read_all()
                elif filename.suffix.lower() == ".json":
                    tensor = pd.read_json(filename, orient="records")
                else:
                    raise TypeError(
                        f" File is of type {filename.suffix.lower()}, but only '.arrow' or '.json' are accepted"
                    )
        else:
            with filename.open("rb") as f:
                tensor = json.load(f)
        return self.infer(tensor, timeout, dataset, dataset_exclude, dataset_separator)

    # ----- Async infer functions -----#
    async def _async_infer_with_json(
        self,
        async_client: AsyncClient,
        tensor: Union[Dict[str, Any], List[Any]],
        timeout: Optional[Union[int, float]] = None,
        params: Optional[Dict[str, Any]] = None,
        retries: Optional[int] = None,
    ):
        headers = {
            "Content-Type": JSON_HEADER,
            "Accept": JSON_HEADER,
        }
        response = await self._make_async_infer_request(
            async_client=async_client,
            headers=headers,
            json_data=tensor,
            params=params,
            timeout=timeout,
            retries=retries,
        )
        try:
            data = response.json() if response is not None else None
        except (json.JSONDecodeError, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err

        return data

    async def _async_infer_with_arrow(
        self,
        async_client: AsyncClient,
        tensor: pa.Table,
        timeout: Optional[Union[int, float]] = None,
        params: Optional[Dict[str, Any]] = None,
        retries: Optional[int] = None,
    ):
        input_arrow = self._write_table_to_arrow_file(tensor, tensor.schema)
        headers = {
            "Content-Type": ARROW_HEADER,
            "format": ARROW_FORMAT,
            "Accept": ARROW_HEADER,
        }
        response = await self._make_async_infer_request(
            async_client=async_client,
            headers=headers,
            content=input_arrow.to_pybytes(),
            params=params,
            timeout=timeout,
            retries=retries,
        )

        try:
            with pa.ipc.open_file(response.content) as reader:
                data_table = reader.read_all()
        except (pa.ArrowInvalid, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err
        assert self.client is not None
        clean_data_table = self.client.cleanup_arrow_data_for_display(data_table)
        return clean_data_table

    async def _async_infer_with_pandas(
        self,
        async_client: AsyncClient,
        tensor: pd.DataFrame,
        timeout: Optional[Union[int, float]] = None,
        params: Optional[Dict[str, Any]] = None,
        retries: Optional[int] = None,
    ):
        for col in tensor.columns:
            tensor[col] = flatten_np_array_columns(tensor, col)
        input_records = tensor.to_json(orient="records")
        headers = {
            "Content-Type": PANDAS_RECORDS_HEADER,
        }
        response = await self._make_async_infer_request(
            async_client=async_client,
            headers=headers,
            content=input_records,
            params=params,
            timeout=timeout,
            retries=retries,
        )
        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError) as err:
            raise ValueError("Infer response is not valid.") from err
        data_df = pd.DataFrame.from_records(data)
        data_df["time"] = pd.to_datetime(data_df["time"], unit="ms")
        data_df["check_failures"] = data_df["check_failures"].apply(len)
        return hack_pandas_dataframe_order(data_df)

    async def _make_async_infer_request(
        self,
        async_client: AsyncClient,
        headers: Dict[str, str],
        content: Optional[Union[bytes, str]] = None,
        json_data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout: Optional[Union[int, float]] = None,
        retries: Optional[int] = None,
    ):
        assert self.client is not None
        # TODO: Probably better to rewrite WallarooAuth to use httpx.Auth to support both sync and async
        #  instead of requests.auth.AuthBase?
        if isinstance(self.client.auth, _PlatformAuth):
            headers.update(self.client.auth.auth_header())

        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(retries or DEFAULT_RETRIES),
            reraise=True,
            retry=retry_if_exception_type((TimeoutException, NetworkError)),
        ):
            with attempt:
                try:
                    response = await async_client.post(
                        self._url(),
                        content=content,
                        json=json_data,
                        params=params,
                        timeout=timeout,
                        headers=headers,
                    )
                    response.raise_for_status()
                except HTTPStatusError as status_err:
                    raise status_err
        return response

    async def async_infer(
        self,
        tensor: Union[Dict[str, Any], List[Any], pd.DataFrame, pa.Table],
        async_client: AsyncClient,
        timeout: Optional[Union[int, float]] = None,
        retries: Optional[int] = None,
        dataset: Optional[List[str]] = None,
        dataset_exclude: Optional[List[str]] = None,
        dataset_separator: Optional[str] = None,
    ):
        timeout = self._init_timeout(timeout)
        params = self._init_infer_params(dataset, dataset_exclude, dataset_separator)
        if isinstance(tensor, pd.DataFrame):
            return await self._async_infer_with_pandas(
                async_client=async_client,
                tensor=tensor,
                timeout=timeout,
                params=params,
                retries=retries,
            )
        elif isinstance(tensor, pa.Table):
            return await self._async_infer_with_arrow(
                async_client=async_client,
                tensor=tensor,
                timeout=timeout,
                params=params,
                retries=retries,
            )
        elif isinstance(tensor, (dict, list)):
            return await self._async_infer_with_json(
                async_client=async_client,
                tensor=tensor,
                timeout=timeout,
                params=params,
                retries=retries,
            )
        else:
            raise TypeError(
                f"tensor is of type {type(tensor)} but 'pandas.DataFrame', 'pyarrow.Table', dict or list is required"
            )

    def replace_model(self, model_version: "ModelVersion") -> "Deployment":
        """Replaces the current model with a default-configured Model.

        :param ModelVersion model_version: Model variant to replace current model with
        """
        return self.replace_configured_model(model_version.config())

    def replace_configured_model(self, model_config: ModelConfig) -> "Deployment":
        """Replaces the current model with a configured variant.

        :param ModelConfig model_config: Configured model to replace current model with
        """
        data = self._gql_client.execute(
            gql.gql(
                """
            mutation ReplaceModel($deployment_id: bigint!, $model_config_id: bigint!) {
                insert_deployment_model_configs(objects: {deployment_id: $deployment_id, model_config_id: $model_config_id}) {
                    returning {
                        id
                        deployment_id
                        model_config_id
                    }
                }
            }
        """
            ),
            variable_values={
                "deployment_id": self.id(),
                "model_config_id": model_config.id(),
            },
        )
        self._rehydrate()
        return self

    def internal_url(self) -> str:
        """Returns the internal inference URL that is only reachable from inside of the Wallaroo cluster by SDK instances deployed in the cluster.

        If both pipelines and models are configured on the Deployment, this
        gives preference to pipelines. The returned URL is always for the first
        configured pipeline or model.
        """
        return self._internal_url()

    def _internal_url(self) -> str:
        return f"http://engine-lb.{self.name()}-{self.id()}:29502/pipelines/{self.pipeline_name()}"

    def url(self) -> str:
        """Returns the inference URL.

        If both pipelines and models are configured on the Deployment, this
        gives preference to pipelines. The returned URL is always for the first
        configured pipeline or model.
        """
        return self._url()

    def _url(self) -> str:
        if self.client is None:
            raise RuntimeError("api_endpoint must be provided to wallaroo.Client()")
        if "api-lb" in self.client.api_endpoint:
            return self._internal_url()

        return f"{self.client.api_endpoint}/v1/api/pipelines/infer/{self.name()}-{self.id()}/{self.pipeline_name()}"

    def logs(self, limit: int = 100, valid: Optional[bool] = None) -> LogEntries:
        """Deployment.logs() has been removed. Please use pipeline.logs() instead."""
        raise RuntimeError(
            "Deployment.logs() has been removed. Please use pipeline.logs() instead."
        )
