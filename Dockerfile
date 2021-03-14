FROM python:3.9

RUN mkdir -p /code/
WORKDIR /code
COPY . /code/
RUN pip install --no-cache-dir -r requirements.txt
