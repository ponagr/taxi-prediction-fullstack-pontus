FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get clean

RUN pip install --no-cache-dir .

CMD ["streamlit", "run", "src/taxipred/frontend/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]