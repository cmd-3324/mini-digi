FROM python:3.13-slim

WORKDIR /app

# Use German mirror (faster than default)
RUN sed -i 's/deb.debian.org/ftp.de.debian.org/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y gettext && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]