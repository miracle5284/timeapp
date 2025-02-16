FROM python:3.10-alpine

RUN mkdir /app

WORKDIR /app

EXPOSE 8000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
RUN python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate

CMD ["gunicorn", "zeero.wsgi:application", "--bind", "0.0.0.0:8000"]