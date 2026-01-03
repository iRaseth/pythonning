from typing import Protocol, Dict


class DataContract(Protocol):

    def to_dict(self) -> Dict[str, int | str]:
        pass