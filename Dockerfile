FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
 gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirments.txt

COPY . .

RUN mkdir -p /app/sessions

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]