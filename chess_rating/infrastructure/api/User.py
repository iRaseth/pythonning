from .client import ApiClient
from ..Database.dataBaseClient import DatabaseClient
from chess_rating.infrastructure.transformer.transform import Transform
from chess_rating.infrastructure.Database.profile import Profile
from typing import Dict, List

class User: 

    def __init__(self,apiClient: ApiClient, dataClient: DatabaseClient, transform: Transform):
        
        self.apiClient = apiClient
        self.dataClient = dataClient
        self.transform = transform

    def get(self,username: str ) -> Dict:
        return self.apiClient.get(username)

    def transform_data_to_profile(self, data: Dict [str,int]) -> Profile:
        self.profile = self.transform.transform_data_to_profile(data)
        return self.profile

    def insert_data(self, data: Profile) -> None:
        self.dataClient.insert_user_data(data)

    def get_and_save(self,username: str ) -> str: 
        data = self.get(username)
        profile = self.transform_data_to_profile(data)
        self.insert_data(profile)
        return "Poprawnie dodano " + username + f" z rankingiem ->{profile.rating}"
    
    def delete_user(self,username: str) -> None:
        self.dataClient.delete_user_by_username(username)
    
    def updateData(self, data: Profile) -> None:
        self.dataClient.insert_user_data(data)

    def get_users(self):
        return self.dataClient.get_users()
    
    def sorting_user_by_rating(self,asc_or_desc: str) -> List[Profile]:
        return self.dataClient.sorting_users_by_rating(asc_or_desc)


apiClient = ApiClient()
dataClient = DatabaseClient("postgresql+psycopg2://postgres:@172.25.240.1:1234/chess_api")
transform = Transform()


UserService = User(apiClient,dataClient,transform)



print(UserService.get_and_save("Niedziaek"))
#print(UserService.transform_data_to_profile(data))