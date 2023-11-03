from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelinesUndeployJsonBody")


@attr.s(auto_attribs=True)
class PipelinesUndeployJsonBody:
    """  Request to undeploy a pipeline by either its own identifier,  or the deployment identifier.

        Attributes:
            pipeline_id (Union[Unset, None, int]):  Pipeline identifier (required unless deployment_id is supplied).
            deployment_id (Union[Unset, None, int]):  Deployment identifier (required unless pipeline_id is supplied).
     """

    pipeline_id: Union[Unset, None, int] = UNSET
    deployment_id: Union[Unset, None, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        pipeline_id = self.pipeline_id
        deployment_id = self.deployment_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if pipeline_id is not UNSET:
            field_dict["pipeline_id"] = pipeline_id
        if deployment_id is not UNSET:
            field_dict["deployment_id"] = deployment_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipeline_id = d.pop("pipeline_id", UNSET)

        deployment_id = d.pop("deployment_id", UNSET)

        pipelines_undeploy_json_body = cls(
            pipeline_id=pipeline_id,
            deployment_id=deployment_id,
        )

        pipelines_undeploy_json_body.additional_properties = d
        return pipelines_undeploy_json_body

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
