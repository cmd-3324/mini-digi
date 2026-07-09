FROM python:3.13-slim

WORKDIR /app

# Use official Docker Hub mirror
RUN sed -i 's|deb.debian.org|mirrors.docker.com|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]