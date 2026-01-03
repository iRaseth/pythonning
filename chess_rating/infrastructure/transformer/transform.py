
from chess_rating.infrastructure.Database.profile import Profile
from typing import Dict

class Transform:

    def transform_data_to_profile(self, data: Dict[str,int]) -> Profile:
        for nazwa, rating in data.items(): 
            return Profile(nazwa= nazwa, rating=rating)
   
