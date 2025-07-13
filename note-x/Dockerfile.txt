# Dockerfile
FROM python:3.10-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy app
COPY . .

# Expose Flask port
EXPOSE 8000

# Default command
CMD ["gunicorn", "-b", "0.0.0.0:8000", "run:create_app()"]
