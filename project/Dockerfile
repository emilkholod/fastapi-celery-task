# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
