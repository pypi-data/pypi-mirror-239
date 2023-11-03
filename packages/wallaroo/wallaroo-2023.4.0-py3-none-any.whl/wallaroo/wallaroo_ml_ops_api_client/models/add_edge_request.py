from typing import Any, Dict, List, Type, TypeVar, cast

import attr

T = TypeVar("T", bound="AddEdgeRequest")


@attr.s(auto_attribs=True)
class AddEdgeRequest:
    """ Request to publish a pipeline.

        Attributes:
            name (str):
            pipeline_publish_id (int):
            tags (List[str]):
     """

    name: str
    pipeline_publish_id: int
    tags: List[str]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        pipeline_publish_id = self.pipeline_publish_id
        tags = self.tags





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "pipeline_publish_id": pipeline_publish_id,
            "tags": tags,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        pipeline_publish_id = d.pop("pipeline_publish_id")

        tags = cast(List[str], d.pop("tags"))


        add_edge_request = cls(
            name=name,
            pipeline_publish_id=pipeline_publish_id,
            tags=tags,
        )

        add_edge_request.additional_properties = d
        return add_edge_request

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
