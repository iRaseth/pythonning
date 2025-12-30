from pydantic import BaseModel
from typing import Dict
 
class Profile(BaseModel): #pydantic ma to co napisalem juz XD

    nazwa: str
    rating: int



    def to_dict(self) -> Dict[str, int]:
        return {
            "nazwa": self.nazwa,
            "rating": self.rating
                 }