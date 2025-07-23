# app/infra/aws/Dockerfile

# 1. Base image
FROM python:3.11-slim

# 2. Environment tweaks
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Working directory
WORKDIR /app

# 4. Install dependencies
#    Copies `app/requirements.txt` into the image
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 5. Copy your application code
#    This brings in everything under `app/src/`
COPY . .

# 6. Expose port and set the startup command
EXPOSE 80
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
