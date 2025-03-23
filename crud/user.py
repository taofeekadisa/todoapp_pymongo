from serializers import user as serializer
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from schemas.user import UserCreate
from database import user_collection
from datetime import datetime

class UserCrud:

    @staticmethod
    def create_user(user_data: UserCreate):
        user_data = jsonable_encoder(user_data)
        user_data["created_at"] = datetime.now()
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)

    @staticmethod
    def get_users():
        users = user_collection.find()
        return serializer.users_serializer(users)
    
    @staticmethod
    def get_user(user_id:str):
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)

    @staticmethod
    def update_user(user_id: str, update_data: dict):
        if not ObjectId.is_valid(user_id):
            return {"error": "Invalid ObjectId format"}

        if not update_data:
            return {"error": "Update data cannot be empty"}

        update_result = user_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )

        if update_result.matched_count == 0:
            return {"error": "User not found"}

        return {"message": "User updated successfully", "modified_count": update_result.modified_count}
    
    @staticmethod
    def delete_user(user_id: str):
        delete_result = user_collection.delete_one({"_id": ObjectId(user_id)})
        
        if delete_result.deleted_count == 0:
            return {"error": "User not found"}
        return {"message": "User deleted successfully", "deleted_count": delete_result.deleted_count}

user_crud = UserCrud()
