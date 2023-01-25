FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
EXPOSE 8000
ENV DJANGO_KEY="!71egb@s_(ru$%0xgb5-ps7y%xk6-85v)u9obasd3f($e(f&a5"
ENV SENTRY_DSN="https://a14ff77438124b4682d4e9e8131a2d1c@o4504553854992384.ingest.sentry.io/4504553874128896"
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "oc_lettings_site.wsgi"]
