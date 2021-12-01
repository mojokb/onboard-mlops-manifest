FROM python:3.8-slim

RUN pip install opencv-python 
RUN apt-get update
RUN apt-get install -y libgl1-mesa-glx wget gzip libglib2.0-0
RUN pip install requests numpy
COPY run.py /run.py
CMD ["python", "/run.py"]

