FROM python:3.13-slim

RUN python -m venv /venv 
ENV PATH="/venv/bin:$PATH"

RUN pip install "django<6" gunicorn whitenoise

COPY src /src

WORKDIR /src

# RUN python manage.py migrate --noinput

# CMD python manage.py runserver 0.0.0.0:8888

CMD gunicorn --bind :8888 superlists.wsgi:application