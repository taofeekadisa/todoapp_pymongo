def user_serializer(user_document) -> dict:
    return {
        "id": str(user_document.get("_id")),
        "username": user_document.get("username"),
        "created_at": str(user_document.get("created_at"))
    }


def users_serializer(user_documents) -> list:
    return [user_serializer(user_document) for user_document in user_documents]
