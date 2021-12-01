FROM python:3.8-slim
RUN pip install minio
COPY monitor.py monitor.py

CMD ["python", "monitor.py"]