FROM python:3.11-slim
WORKDIR /app
COPY volume_gen.py .
RUN pip install requests

CMD ["python", "volume_gen.py"]
