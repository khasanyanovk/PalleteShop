FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    gettext \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

COPY . /app/

RUN mkdir -p /app/staticfiles /app/media

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
