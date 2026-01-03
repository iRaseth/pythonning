from pydantic import BaseModel
from typing import Dict
 
class Profile(BaseModel):

    nazwa: str
    rating: int



    def to_dict(self) -> Dict[str, int| str ]:
        return {
            "nazwa": self.nazwa,
            "rating": self.rating
                 }