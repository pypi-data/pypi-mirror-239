from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="ExplainabilityListConfigsByPipelineResponse500")


@attr.s(auto_attribs=True)
class ExplainabilityListConfigsByPipelineResponse500:
    """  Error response.

        Attributes:
            msg (str):  Error message.
            code (int):  Status code for the error.
     """

    msg: str
    code: int
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        msg = self.msg
        code = self.code

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "msg": msg,
            "code": code,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        msg = d.pop("msg")

        code = d.pop("code")

        explainability_list_configs_by_pipeline_response_500 = cls(
            msg=msg,
            code=code,
        )

        explainability_list_configs_by_pipeline_response_500.additional_properties = d
        return explainability_list_configs_by_pipeline_response_500

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
