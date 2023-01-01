FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
RUN flake8
RUN pytest
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
