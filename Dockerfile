FROM python:3.11

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /src

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]
