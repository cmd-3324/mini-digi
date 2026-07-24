# FROM python:3.13-slim

# WORKDIR /app

# # Use official Docker Hub mirror
# RUN sed -i 's|deb.debian.org|mirror.arvancloud.ir|g' /etc/apt/sources.list.d/debian.sources && \
#     apt-get update && \
#     apt-get install -y gettext && \
#     rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#--------------------------------------------------
# FROM python:3.13-slim

# WORKDIR /app

# # Standard update (GitHub's fast, uncensored internet will handle this fine)
# RUN apt-get update && \
#     apt-get install -y gettext && \
#     rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libssl-dev \
    libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]