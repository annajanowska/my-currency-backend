FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=mycurrency.settings
ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
EXPOSE 8000

CMD ["gunicorn", "mycurrency.wsgi:application", "--bind", "0.0.0.0:8000"]
