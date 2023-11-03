from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

if TYPE_CHECKING:
  from ..models.assays_create_json_body_baseline_type_0_calculated_type_0 import \
      AssaysCreateJsonBodyBaselineType0CalculatedType0
  from ..models.assays_create_json_body_baseline_type_0_calculated_type_1 import \
      AssaysCreateJsonBodyBaselineType0CalculatedType1
  from ..models.assays_create_json_body_baseline_type_0_calculated_type_2 import \
      AssaysCreateJsonBodyBaselineType0CalculatedType2





T = TypeVar("T", bound="AssaysCreateJsonBodyBaselineType0")


@attr.s(auto_attribs=True)
class AssaysCreateJsonBodyBaselineType0:
    """ 
        Attributes:
            calculated (Union['AssaysCreateJsonBodyBaselineType0CalculatedType0',
                'AssaysCreateJsonBodyBaselineType0CalculatedType1', 'AssaysCreateJsonBodyBaselineType0CalculatedType2']):
     """

    calculated: Union['AssaysCreateJsonBodyBaselineType0CalculatedType0', 'AssaysCreateJsonBodyBaselineType0CalculatedType1', 'AssaysCreateJsonBodyBaselineType0CalculatedType2']
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.assays_create_json_body_baseline_type_0_calculated_type_0 import \
            AssaysCreateJsonBodyBaselineType0CalculatedType0
        from ..models.assays_create_json_body_baseline_type_0_calculated_type_1 import \
            AssaysCreateJsonBodyBaselineType0CalculatedType1
        calculated: Dict[str, Any]

        if isinstance(self.calculated, AssaysCreateJsonBodyBaselineType0CalculatedType0):
            calculated = self.calculated.to_dict()

        elif isinstance(self.calculated, AssaysCreateJsonBodyBaselineType0CalculatedType1):
            calculated = self.calculated.to_dict()

        else:
            calculated = self.calculated.to_dict()




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "calculated": calculated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.assays_create_json_body_baseline_type_0_calculated_type_0 import \
            AssaysCreateJsonBodyBaselineType0CalculatedType0
        from ..models.assays_create_json_body_baseline_type_0_calculated_type_1 import \
            AssaysCreateJsonBodyBaselineType0CalculatedType1
        from ..models.assays_create_json_body_baseline_type_0_calculated_type_2 import \
            AssaysCreateJsonBodyBaselineType0CalculatedType2
        d = src_dict.copy()
        def _parse_calculated(data: object) -> Union['AssaysCreateJsonBodyBaselineType0CalculatedType0', 'AssaysCreateJsonBodyBaselineType0CalculatedType1', 'AssaysCreateJsonBodyBaselineType0CalculatedType2']:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                calculated_type_0 = AssaysCreateJsonBodyBaselineType0CalculatedType0.from_dict(data)



                return calculated_type_0
            except: # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                calculated_type_1 = AssaysCreateJsonBodyBaselineType0CalculatedType1.from_dict(data)



                return calculated_type_1
            except: # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            calculated_type_2 = AssaysCreateJsonBodyBaselineType0CalculatedType2.from_dict(data)



            return calculated_type_2

        calculated = _parse_calculated(d.pop("calculated"))


        assays_create_json_body_baseline_type_0 = cls(
            calculated=calculated,
        )

        assays_create_json_body_baseline_type_0.additional_properties = d
        return assays_create_json_body_baseline_type_0

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
