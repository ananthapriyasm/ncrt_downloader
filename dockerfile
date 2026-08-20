FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create PDF directory
RUN mkdir -p pdfs

CMD ["python", "main.py"]