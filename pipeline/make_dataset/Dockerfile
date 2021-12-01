FROM python:3.8-slim

RUN pip install pillow numpy scikit-learn

COPY image_to_npz.py image_to_npz.py

CMD ["python", "image_to_npz.py"]
