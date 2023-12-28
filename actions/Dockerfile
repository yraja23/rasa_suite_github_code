FROM rasa/rasa-sdk

WORKDIR /app

COPY requirements.txt requirements.txt

#COPY trydb /app/trydb

USER root

RUN pip install -r requirements.txt

USER 1001

EXPOSE 5055

# CMD [ "python", "-m", "rasa_sdk", "--actions", "actions" ]

CMD ["start", "--actions", "actions"]


