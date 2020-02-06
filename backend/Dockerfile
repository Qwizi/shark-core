FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code/
RUN cd /code/
RUN mkdir /backend/

WORKDIR /code/backend/

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/backend/
RUN pipenv install --system

COPY . /code/backend/