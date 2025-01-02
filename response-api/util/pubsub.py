from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
import os

pubsub_client = WebPubSubServiceClient(endpoint=os.environ["PUBSUB_ENDPOINT"],
                                       hub=os.environ["PUBSUB_HUB"],
                                       credential=AzureKeyCredential(os.environ["PUBSUB_KEY"]))

