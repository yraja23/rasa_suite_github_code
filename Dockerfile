FROM rasa/rasa:3.5.5

WORKDIR /app

COPY . /app

USER root

COPY ./data /app/data
#COPY ./20230519-115614-bright-wake.tar.gz /app/models
COPY ./config.yml /app/config.yml
COPY ./credentials.yml /app/credentials.yml
COPY ./endpoints.yml /app/endpoints.yml

VOLUME /app
VOLUME /app/data
VOLUME /app/models

EXPOSE 5005

CMD ["run", "-m", "/app/models", "--enable-api", "--cors", "*", "--debug"]


