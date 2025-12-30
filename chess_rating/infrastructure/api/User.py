from .client import ApiClient
from ..Database.dataBaseClient import DatabaseClient
from chess_rating.infrastructure.transformer.transform import Transform
from chess_rating.infrastructure.Database.profile import Profile
from typing import Dict

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

    def insertData(self, data: Profile) -> None:
        self.dataClient.insertData(data)

    def get_and_save(self,username: str ) -> str: 
        data = self.get(username)
        profile = self.transform_data_to_profile(data)
        self.insertData(profile)
        return "Poprawnie dodano " + username + f" z rankingiem ->{profile.rating}"
    
    def delete_user(self,username: str) -> None:
        self.dataClient.delete_user(username)
    
    def updateData(self, data: Profile) -> None:
        self.dataClient.insertData(data)

    def get_users(self):
        return self.dataClient.get_users()


apiClient = ApiClient()
dataClient = DatabaseClient("postgresql+psycopg2://postgres:Innominate12@172.25.240.1:1234/chess_api")
transform = Transform()


UserService = User(apiClient,dataClient,transform)

#data = UserService.get_and_save("hikaru")
print(UserService.delete_user("hikaru"))

#print(UserService.transform_data_to_profile(data))