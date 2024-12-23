from chromadb import AsyncHttpClient, AsyncClientAPI
from chromadb.types import Literal
from chromadb.api.types import IncludeEnum
from src.bot.create_bot import model
import numpy as np
import json

HOST = "62.60.249.194"
PORT = 8000


class VectorDB:

    def __init__(self, client: AsyncClientAPI, user_id: str) -> None:
        self.client = client
        self.user_id = user_id

    async def has_user(self) -> bool:
        user_collection = await self.client.get_or_create_collection("research_links")
        user = await user_collection.get(ids=[self.user_id])
        return bool(user.get("metadatas", None))

    async def add_user(self, form: dict[str, str], username: str, chat_id: str) -> None:
        user_collection = await self.client.get_or_create_collection("research_links")
        form.update({
            "id": self.user_id,
            "viewed": json.dumps([self.user_id]),
            "matched": json.dumps([]),
            "username": username,
            "chat_id": chat_id
        })
        embedding = np.array(model.encode(str(form.get("info", "Error"))))
        await user_collection.add(ids=[self.user_id], documents=[str(form.get("info", "Errors"))], metadatas=[form], embeddings=[embedding])

    async def update_form(self, form_change: str, new_value: str) -> None:
        user_collection = await self.client.get_or_create_collection("research_links")
        user_form = await user_collection.get(ids=[self.user_id])

        if not (isinstance(user_form["metadatas"], list) and isinstance(user_form["metadatas"][0], dict)):
            return None
        new_metadatas = user_form["metadatas"][0]
        new_metadatas[form_change] = new_value

        if form_change == "info":
            embedding = np.array(model.encode(new_value))
            await user_collection.update(ids=[self.user_id], documents=[new_value], metadatas=[new_metadatas], embeddings=[embedding])
        else:
            await user_collection.update(ids=[self.user_id], metadatas=[new_metadatas])

    async def get_form(self, user_id: str) -> dict[str, str]:
        user_collection = await self.client.get_or_create_collection("research_links")
        user_form = await user_collection.get(ids=[user_id])

        if not (isinstance(user_form["metadatas"], list) and isinstance(user_form["metadatas"][0], dict)):
            return {"name": "Error"}
        return user_form["metadatas"][0]

    async def get_self_form(self) -> dict[str, str]:
        form = await self.get_form(self.user_id)
        return form

    async def get_similar_form(self) -> tuple[dict[str, str], str] | None:
        user_collection = await self.client.get_or_create_collection("research_links")
        user_form = await user_collection.get(ids=[self.user_id], include=[IncludeEnum.metadatas, IncludeEnum.embeddings])

        if not (isinstance(user_form["metadatas"], list) and isinstance(user_form["metadatas"][0], dict) and isinstance(
                user_form["embeddings"], np.ndarray)):
            return None

        new_metadatas = user_form["metadatas"][0]
        viewed = new_metadatas.get("viewed", None)
        viewed: list[str] = json.loads(viewed) if isinstance(viewed, str) else [self.user_id]

        other_form = await user_collection.query(query_embeddings=[np.array(user_form["embeddings"][0])],
                                                 n_results=1,
                                                 where={"id": {"$nin": viewed}}) # type: ignore

        if (not isinstance(other_form["metadatas"], list) or not isinstance(other_form["metadatas"][0], list) or not
                bool(other_form["metadatas"][0]) or not isinstance(other_form["metadatas"][0][0], dict)):
            return None

        other_form = other_form["metadatas"][0][0]
        other_id = other_form.get("id", None)
        other_chat_id = other_form.get("chat_id", None)

        if not (isinstance(other_id, str) and isinstance(other_chat_id, str)):
            return None

        viewed.append(other_id)
        new_metadatas["viewed"] = json.dumps(viewed)
        await user_collection.update(ids=[self.user_id], metadatas=[new_metadatas])
        other_form = await self.get_form(other_id)
        return other_form, other_chat_id

    async def match(self, other_id: str) -> None:
        user_collection = await self.client.get_or_create_collection("research_links")
        ids = [self.user_id, other_id]
        users = await user_collection.get(ids=ids)
        metadatas = users["metadatas"]

        if (isinstance(metadatas, list) and len(metadatas) == 2 and
                isinstance(metadatas[0], dict) and isinstance(metadatas[1], dict)):

            for metadata, i in zip(metadatas, [other_id, self.user_id]):
                old_matched = metadata.get("matched", None)
                matched = json.loads(old_matched) if isinstance(old_matched, str) else []
                matched.append(i)
                metadata["matched"] = json.dumps(matched)  # type: ignore

            await user_collection.update(ids=ids, metadatas=metadatas)

    async def get_matched(self, ind: int) -> dict[str, str] | None:
        user_collection = await self.client.get_or_create_collection("research_links")
        user_form = await user_collection.get(ids=[self.user_id])

        if not (isinstance(user_form["metadatas"], list) and isinstance(user_form["metadatas"][0], dict)):
            return None
        metadatas = user_form["metadatas"][0]
        matched = metadatas.get("matched", None)
        matched = json.loads(matched) if isinstance(matched, str) else []
        if not matched:
            return None

        other_id = matched[ind % len(matched)]
        other_form = await self.get_form(other_id)
        return other_form

    async def clean_viewed(self) -> None:
        user_collection = await self.client.get_or_create_collection("research_links")
        user_form = await user_collection.get(ids=[self.user_id])

        if not (isinstance(user_form["metadatas"], list) and isinstance(user_form["metadatas"][0], dict)):
            return None
        new_metadatas = user_form["metadatas"][0]
        new_metadatas["viewed"] = json.dumps([self.user_id])

        await user_collection.update(ids=[self.user_id], metadatas=[new_metadatas])


async def client_connect(user_id: str) -> VectorDB:
    client = await AsyncHttpClient(host=HOST, port=PORT)
    return VectorDB(client, user_id)
