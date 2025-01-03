import logging
import azure.functions as func
from openai import OpenAI
import json
from util.servicebus import servicebus_client

app = func.FunctionApp()
client = OpenAI()

@app.service_bus_queue_trigger(arg_name="msg", queue_name="process-request-queue",
                               connection="SB_CONNECTION_URL") 
async def process_request(msg: func.ServiceBusMessage):
    message = json.loads(msg.get_body().decode('utf-8'))
    completion = client.chat.completions.create(
        model="o1",
        messages=[
            {"role": "system", "content": "질문에 대해 한국어로 대답해."},
            {
                "role": "user",
                "content": message["content"]
            }
        ]
    )
    answer_data = {
        "channel_id": message["channel_id"],
        "content": completion.choices[0].message.content,
        "type" : "answer"
    }
    # logging.debug(completion.choices[0].message.content)
    await servicebus_client.send_message("process-response-queue", answer_data)
    # logging.debug("메세지 전송")

