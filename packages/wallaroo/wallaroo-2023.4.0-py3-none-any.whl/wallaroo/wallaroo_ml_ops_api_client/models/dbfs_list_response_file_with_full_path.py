from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="DbfsListResponseFileWithFullPath")


@attr.s(auto_attribs=True)
class DbfsListResponseFileWithFullPath:
    """ This is the return value from a Dbfs List call, but with the full path added for convenience.

        Attributes:
            file_size (int):
            full_path (str): This is added by Wallaroo
            is_dir (bool):
            modification_time (int):
            path (str):
     """

    file_size: int
    full_path: str
    is_dir: bool
    modification_time: int
    path: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        file_size = self.file_size
        full_path = self.full_path
        is_dir = self.is_dir
        modification_time = self.modification_time
        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_size": file_size,
            "full_path": full_path,
            "is_dir": is_dir,
            "modification_time": modification_time,
            "path": path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file_size = d.pop("file_size")

        full_path = d.pop("full_path")

        is_dir = d.pop("is_dir")

        modification_time = d.pop("modification_time")

        path = d.pop("path")

        dbfs_list_response_file_with_full_path = cls(
            file_size=file_size,
            full_path=full_path,
            is_dir=is_dir,
            modification_time=modification_time,
            path=path,
        )

        dbfs_list_response_file_with_full_path.additional_properties = d
        return dbfs_list_response_file_with_full_path

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
