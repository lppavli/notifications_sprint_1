FROM python:3.9.9-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install -r /code/requirements.txt
COPY . /code/
WORKDIR /code
CMD ["python", "/code/consumer.py"]