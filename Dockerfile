FROM python:3.13-slim

RUN python -m venv /venv 
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /src

WORKDIR /src

RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1


# RUN python manage.py migrate --noinput

# CMD python manage.py runserver 0.0.0.0:8888

CMD gunicorn --bind :8888 superlists.wsgi:application