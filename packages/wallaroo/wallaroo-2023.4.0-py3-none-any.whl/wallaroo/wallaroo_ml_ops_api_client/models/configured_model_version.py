from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

import attr

if TYPE_CHECKING:
  from ..models.model_config import ModelConfig
  from ..models.model_version import ModelVersion





T = TypeVar("T", bound="ConfiguredModelVersion")


@attr.s(auto_attribs=True)
class ConfiguredModelVersion:
    """ 
        Attributes:
            config (ModelConfig): Wrapper struct to add a realized database ID to an underlying data struct.
            model_version (ModelVersion):
     """

    config: 'ModelConfig'
    model_version: 'ModelVersion'
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        config = self.config.to_dict()

        model_version = self.model_version.to_dict()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "config": config,
            "model_version": model_version,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.model_config import ModelConfig
        from ..models.model_version import ModelVersion
        d = src_dict.copy()
        config = ModelConfig.from_dict(d.pop("config"))




        model_version = ModelVersion.from_dict(d.pop("model_version"))




        configured_model_version = cls(
            config=config,
            model_version=model_version,
        )

        configured_model_version.additional_properties = d
        return configured_model_version

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
