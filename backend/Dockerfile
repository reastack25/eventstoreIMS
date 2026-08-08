FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:${PORT:-5000} 'app:create_app()'"]
