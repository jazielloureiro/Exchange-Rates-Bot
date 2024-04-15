FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py .

CMD [ "gunicorn", "server:app", "-b=0.0.0.0" ]