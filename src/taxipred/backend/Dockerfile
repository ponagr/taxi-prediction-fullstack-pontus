FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN pip install --no-cache-dir .

CMD ["uvicorn", "src.taxipred.backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]