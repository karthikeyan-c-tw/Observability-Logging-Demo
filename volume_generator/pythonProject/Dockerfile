FROM python:3.11-slim
WORKDIR /app
COPY volume_gen.py .
RUN pip install --no-cache-dir \
    requests \
    streamlit \
    python-logstash \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-grpc

EXPOSE 8501

CMD ["streamlit", "run", "volume_gen.py", "--server.enableCORS=false"]
