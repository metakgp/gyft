FROM python:3.13-slim

ENV TZ="Asia/Kolkata"

# Install dependencies for OpenCV (libGL, fonts, etc.)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY metaploy/ ./

RUN chmod +x ./postinstall.sh

COPY . .

RUN python download-calendar.py

CMD [ "./postinstall.sh", "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app" ]
