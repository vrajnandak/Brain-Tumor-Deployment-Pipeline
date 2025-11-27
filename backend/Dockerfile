FROM python:3.8-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your backend code
COPY src/api.py .

# --- Cache busting ARG for model ---
ARG MODEL_VERSION=0

# Copy the model file (forces rebuild when MODEL_VERSION changes)
COPY model.h5 /app/model.h5

EXPOSE 5001

CMD ["python", "api.py"]
