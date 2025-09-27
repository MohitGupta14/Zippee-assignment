# Use official Python image
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install build dependencies, libpq-dev, and the dos2unix utility
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    dos2unix \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# FIX 1: Convert Windows line endings (CRLF) to Unix line endings (LF)
RUN dos2unix ./start.sh

# FIX 2: Ensure it is executable
RUN chmod +x start.sh

EXPOSE 3000

# FIX 3: Explicitly execute the script using /bin/sh. 
# This bypasses potential issues with the script's shebang line (#!)
# that can cause the "exec format error".
CMD ["/bin/sh", "./start.sh"]
