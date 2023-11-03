from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AdminGetPipelineExternalUrlJsonBody")


@attr.s(auto_attribs=True)
class AdminGetPipelineExternalUrlJsonBody:
    """  Request for pipeline URL-related operations.

        Attributes:
            workspace_id (int):  Unique workspace identifier.
            pipeline_name (str):  Name of the pipeline.
     """

    workspace_id: int
    pipeline_name: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        workspace_id = self.workspace_id
        pipeline_name = self.pipeline_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workspace_id": workspace_id,
            "pipeline_name": pipeline_name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        workspace_id = d.pop("workspace_id")

        pipeline_name = d.pop("pipeline_name")

        admin_get_pipeline_external_url_json_body = cls(
            workspace_id=workspace_id,
            pipeline_name=pipeline_name,
        )

        admin_get_pipeline_external_url_json_body.additional_properties = d
        return admin_get_pipeline_external_url_json_body

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
