FROM python:3.8-slim
RUN pip install minio
COPY upload.py upload.py

CMD ["python", "upload.py"]