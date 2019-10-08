FROM python:latest

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8085

ENTRYPOINT python3 -m briw.api.flask_server