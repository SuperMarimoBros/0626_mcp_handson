from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit
import requests
import os

app = APIGatewayRestResolver()
logger = Logger()
metrics = Metrics(namespace="Powertools")

SLACK_API_URL = os.environ.get("SLACK_API_URL", "")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN", "")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "")

# 環境変数の検証
if not all([SLACK_API_URL, SLACK_TOKEN, SLACK_CHANNEL]):
    raise ValueError("Required environment variables are not set: SLACK_API_URL, SLACK_TOKEN, SLACK_CHANNEL")

@app.post("/messages/create")
def create_message() -> dict:
    """
    Create a message in the Slack channel.
    This function is triggered by an HTTP POST request to the /messages/create endpoint.
    """
    # Extract the message from the request body
    request_body = app.current_event.json_body

    message = request_body.get("message")

    if not message:
        return {
            "statusCode": 400,
            "body": {"error": "Message content is required"}
        }

    # Log the received message
    logger.info(f"Received message: {message}")

    # Send the message to Slack
    try:
        response = requests.post(
            SLACK_API_URL,
            data={
                "token": SLACK_TOKEN,
                "channel": SLACK_CHANNEL,
                "text": message
            }
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to Slack: {e}")
        return {
            "statusCode": 500,
            "body": {"error": "Failed to send message to Slack"}
        }
    else:
        logger.info("Message sent to Slack successfully")
        metrics.add_metric(name="MessagesSent", unit=MetricUnit.Count, value=1)
        return {
            "statusCode": 200,
            "body": {"message": "Message sent to Slack successfully"}
        }

# Exception handler for uncaught exceptions
@app.exception_handler(Exception)
def handle_exception(e: Exception) -> dict:
    """
    Handle uncaught exceptions and return a 500 response.
    """
    logger.error(f"Unhandled exception: {e}")
    return {
        "statusCode": 500,
        "body": {"error": "An unexpected error occurred"}
    }

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
