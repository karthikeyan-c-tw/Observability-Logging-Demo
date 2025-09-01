import requests
import os
import streamlit as st
import logging
import logstash
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# ------------------------------
# ENV VARS
# ------------------------------
MSG_URL = os.environ.get("MSG_URL", "http://localhost:7000/message/")
COUNT = int(os.environ.get("COUNT", 1000))

LOGSTASH_HOST = os.environ.get("LOGSTASH_HOST", "logstash")
LOGSTASH_PORT = int(os.environ.get("LOGSTASH_PORT", 5000))
OTLP_COLLECTOR = os.environ.get("OTEL_COLLECTOR", "otel-collector:4317")

# ------------------------------
# Logging to Logstash
# ------------------------------
logger = logging.getLogger("volume-generator")
logger.setLevel(logging.INFO)

logstash_handler = logstash.TCPLogstashHandler(LOGSTASH_HOST, LOGSTASH_PORT, version=1)
logger.addHandler(logstash_handler)

common_log_data = {
    'data_stream': {
        'type': 'logs',
        'dataset': 'volume-generator',
        'namespace': 'default'
    }
}

# ------------------------------
# OpenTelemetry Metrics
# ------------------------------
exporter = OTLPMetricExporter(endpoint=OTLP_COLLECTOR, insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter("volume-generator")

# Custom metrics
request_counter = meter.create_counter(
    name="message_api_requests",
    description="Counts successful message requests",
    unit="1"
)

error_counter = meter.create_counter(
    name="message_api_errors",
    description="Counts failed message requests",
    unit="1"
)

# ------------------------------
# Volume Generation Logic
# ------------------------------


def generate_volume(count, message="JohnDoe"):
    for i in range(count):
        try:
            response = requests.get(MSG_URL + message)
            if response.status_code == 200:
                logger.info(f"Message {i+1}: {response.text}", extra={
                    **common_log_data,
                    'event': 'generate',
                    'status': 'success',
                    'msg_url': MSG_URL
                })
                request_counter.add(1, {"status": "success"})
            else:
                logger.warning(f"Failed to get message {i+1}: Status {response.status_code}", extra={
                    **common_log_data,
                    'event': 'generate',
                    'status': 'http_error',
                    'msg_url': MSG_URL
                })
                error_counter.add(1, {"status": "http_error"})
        except Exception as e:
            logger.exception(f"Error occurred while fetching message {i+1}", exc_info=e, extra={
                **common_log_data,
                'event': 'generate',
                'status': 'exception',
                'msg_url': MSG_URL
            })
            error_counter.add(1, {"status": "exception"})

# ------------------------------
# Streamlit UI
# ------------------------------


st.title("API Load Generator")

user_input = st.text_input("Enter the message", "JohnDoe")
user_count = st.number_input("Enter the count", min_value=1, max_value=100000, value=COUNT, step=1)

if st.button("Generate Volume"):
    logger.info(f"Volume generation started for {user_input}", extra={
        **common_log_data,
        'event': 'start',
        'msg_url': MSG_URL,
        'count': user_count
    })
    generate_volume(user_count, user_input)
