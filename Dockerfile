FROM python:3.8.20

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./client /app/client
COPY ./server /app/server
COPY ./main.py /app/main.py

EXPOSE 8080

CMD [ "python", "main.py" ]