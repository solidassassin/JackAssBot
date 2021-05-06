FROM python:3

WORKDIR /usr/src/app/JackAssBot

RUN git clone https://github.com/solidassassin/JackAssBot.git .
COPY config.py ./data
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./launch.py" ]
