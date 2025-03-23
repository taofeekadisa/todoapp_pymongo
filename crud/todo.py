from serializers import todo as serializer
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from schemas.todo import TodoCreate
from database import todo_collection


class TodoCrud:

    @staticmethod
    def create_todo(todo_data: TodoCreate):
        todo_data = jsonable_encoder(todo_data)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)

    @staticmethod
    def get_todos():
        todos = todo_collection.find()
        return serializer.todos_serializer(todos)

    @staticmethod
    def get_todo(todo_id: str):
        if not ObjectId.is_valid(todo_id):
            return {"error": "Invalid ObjectId format"}

        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if not todo:
            return {"error": "Todo not found"}

        return serializer.todo_serializer(todo)

    @staticmethod
    def update_todo(todo_id: str, update_data: dict):
        if not ObjectId.is_valid(todo_id):
            return {"error": "Invalid ObjectId format"}

        if not update_data:
            return {"error": "Update data cannot be empty"}

        update_result = todo_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": update_data}
        )

        if update_result.matched_count == 0:
            return {"error": "Todo not found"}

        return {"message": "Todo updated successfully", "modified_count": update_result.modified_count}

    @staticmethod
    def delete_todo(todo_id: str):
        if not ObjectId.is_valid(todo_id):
            return {"error": "Invalid ObjectId format"}

        delete_result = todo_collection.delete_one({"_id": ObjectId(todo_id)})

        if delete_result.deleted_count == 0:
            return {"error": "Todo not found"}

        return {"message": "Todo deleted successfully", "deleted_count": delete_result.deleted_count}
todo_crud = TodoCrud()
