FROM python:3.10

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
ENV FLASK_APP flaskapp_slave.py

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5001", "--with-threads"]