from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="PipelinesCreateResponse200")


@attr.s(auto_attribs=True)
class PipelinesCreateResponse200:
    """  Successful response to pipeline creation request.

        Attributes:
            pipeline_pk_id (int):  Internal pipeline identifier.
            pipeline_variant_pk_id (int):  Internal pipeline variant identifier.
            pipeline_variant_version (str):  Pipeline Version UUID identifier
     """

    pipeline_pk_id: int
    pipeline_variant_pk_id: int
    pipeline_variant_version: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        pipeline_pk_id = self.pipeline_pk_id
        pipeline_variant_pk_id = self.pipeline_variant_pk_id
        pipeline_variant_version = self.pipeline_variant_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pipeline_pk_id": pipeline_pk_id,
            "pipeline_variant_pk_id": pipeline_variant_pk_id,
            "pipeline_variant_version": pipeline_variant_version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipeline_pk_id = d.pop("pipeline_pk_id")

        pipeline_variant_pk_id = d.pop("pipeline_variant_pk_id")

        pipeline_variant_version = d.pop("pipeline_variant_version")

        pipelines_create_response_200 = cls(
            pipeline_pk_id=pipeline_pk_id,
            pipeline_variant_pk_id=pipeline_variant_pk_id,
            pipeline_variant_version=pipeline_variant_version,
        )

        pipelines_create_response_200.additional_properties = d
        return pipelines_create_response_200

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
