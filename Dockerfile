FROM python:3.11-slim

# Instalar dependencias necesarias para compilar bcrypt
RUN apt-get update && apt-get install -y gcc libffi-dev musl-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
