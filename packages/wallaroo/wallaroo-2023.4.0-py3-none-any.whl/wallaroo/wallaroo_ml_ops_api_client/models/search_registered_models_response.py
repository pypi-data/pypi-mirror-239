from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.registered_model import RegisteredModel





T = TypeVar("T", bound="SearchRegisteredModelsResponse")


@attr.s(auto_attribs=True)
class SearchRegisteredModelsResponse:
    """ The structure of the response from a 2.0 MLFlow API.

        Attributes:
            registered_models (List['RegisteredModel']):
            next_page_token (Union[Unset, None, str]):
     """

    registered_models: List['RegisteredModel']
    next_page_token: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        registered_models = []
        for registered_models_item_data in self.registered_models:
            registered_models_item = registered_models_item_data.to_dict()

            registered_models.append(registered_models_item)




        next_page_token = self.next_page_token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "registered_models": registered_models,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.registered_model import RegisteredModel
        d = src_dict.copy()
        registered_models = []
        _registered_models = d.pop("registered_models")
        for registered_models_item_data in (_registered_models):
            registered_models_item = RegisteredModel.from_dict(registered_models_item_data)



            registered_models.append(registered_models_item)


        next_page_token = d.pop("next_page_token", UNSET)

        search_registered_models_response = cls(
            registered_models=registered_models,
            next_page_token=next_page_token,
        )

        search_registered_models_response.additional_properties = d
        return search_registered_models_response

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
