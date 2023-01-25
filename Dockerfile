FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
EXPOSE 8000
ENV DJANGO_KEY=$Env:DJANGO_KEY
ENV SENTRY_DSN=$Env:SENTRY_DSN
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "oc_lettings_site.wsgi"]
