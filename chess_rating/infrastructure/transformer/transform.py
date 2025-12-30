
from chess_rating.infrastructure.Database.profile import Profile

class Transform:

    def transform_data_to_profile(self, data) -> Profile:
        for nazwa, rating in data.items(): #  nazwa, rating = next(iter(data.items())) <- to samo, tylko robimy iterator i szybciej   w ten sposob jest
            return Profile(nazwa=nazwa, rating = rating)
   
