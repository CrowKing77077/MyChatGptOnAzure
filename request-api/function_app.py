from typing import Union
import uuid
from fastapi import FastAPI
from dto.question import QuestionRequest
import azure.functions as func
from fastapi.middleware.cors import CORSMiddleware

from util.servicebus import servicebus_client
from util.pubsub import pubsub_client
from util.database import db

fast_app = FastAPI()
fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app = func.AsgiFunctionApp(app=fast_app, http_auth_level=func.AuthLevel.ANONYMOUS)

# 질문 API
# Frontend에 Pub/Sub 토큰 발급 API

@fast_app.get("/channel_id")
async def get_channel_id():
    return {"channel_id": str(uuid.uuid4())}
    # TODO: DB에 중복 있으면 다시 생성

@fast_app.post("/question")
async def send_question(request: QuestionRequest):
    question_data = {
        "channel_id": request.channel_id,
        "content": request.content,
        "type" : "question"
    }
    result = await db.messages.insert_one(question_data)
    question_data["_id"] = str(question_data["_id"])

    await servicebus_client.send_message("process-request-queue", question_data)
    return str(result.inserted_id)


@fast_app.get("/pubsub/token")
async def read_item(channel_id: str):
    return await pubsub_client.get_client_access_token(group=[channel_id], minutes_to_expire=5, roles=['webpubsub.joinLeaveGroup.' + channel_id])
