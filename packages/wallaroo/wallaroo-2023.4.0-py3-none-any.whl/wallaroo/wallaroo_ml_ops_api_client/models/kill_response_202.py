import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.arbex_status import ArbexStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.kill_response_202_input_data import KillResponse202InputData
  from ..models.task_run import TaskRun





T = TypeVar("T", bound="KillResponse202")


@attr.s(auto_attribs=True)
class KillResponse202:
    """ 
        Attributes:
            created_at (datetime.datetime):
            id (str):
            input_data (KillResponse202InputData):
            killed (bool):
            last_runs (List['TaskRun']): A list of the (by default: 5) most recent runs associated with this Task.
                This will only ever be more than 1 in the case of the Scheduled/Cron run.
            status (ArbexStatus):
            updated_at (datetime.datetime):
            workspace_id (int):
            name (Union[Unset, None, str]):
     """

    created_at: datetime.datetime
    id: str
    input_data: 'KillResponse202InputData'
    killed: bool
    last_runs: List['TaskRun']
    status: ArbexStatus
    updated_at: datetime.datetime
    workspace_id: int
    name: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        created_at = self.created_at.isoformat()

        id = self.id
        input_data = self.input_data.to_dict()

        killed = self.killed
        last_runs = []
        for last_runs_item_data in self.last_runs:
            last_runs_item = last_runs_item_data.to_dict()

            last_runs.append(last_runs_item)




        status = self.status.value

        updated_at = self.updated_at.isoformat()

        workspace_id = self.workspace_id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "id": id,
            "input_data": input_data,
            "killed": killed,
            "last_runs": last_runs,
            "status": status,
            "updated_at": updated_at,
            "workspace_id": workspace_id,
        })
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.kill_response_202_input_data import \
            KillResponse202InputData
        from ..models.task_run import TaskRun
        d = src_dict.copy()
        created_at = isoparse(d.pop("created_at"))




        id = d.pop("id")

        input_data = KillResponse202InputData.from_dict(d.pop("input_data"))




        killed = d.pop("killed")

        last_runs = []
        _last_runs = d.pop("last_runs")
        for last_runs_item_data in (_last_runs):
            last_runs_item = TaskRun.from_dict(last_runs_item_data)



            last_runs.append(last_runs_item)


        status = ArbexStatus(d.pop("status"))




        updated_at = isoparse(d.pop("updated_at"))




        workspace_id = d.pop("workspace_id")

        name = d.pop("name", UNSET)

        kill_response_202 = cls(
            created_at=created_at,
            id=id,
            input_data=input_data,
            killed=killed,
            last_runs=last_runs,
            status=status,
            updated_at=updated_at,
            workspace_id=workspace_id,
            name=name,
        )

        kill_response_202.additional_properties = d
        return kill_response_202

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
