FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code
COPY src/api.py .

# Copy the model file or folder
COPY model.h5 ./model.h5

EXPOSE 5001

CMD ["python", "api.py"]