FROM python:3.9-slim-buster
WORKDIR /app
RUN apt-get update && apt-get install unzip -y && rm -rf /var/lib/apt/lists/*
ADD https://github.com/mjmcfalls/Interview_challenges/archive/main.zip /tmp
RUN unzip /tmp/main.zip -d /tmp/ \
    && cp /tmp/Interview_challenges-main/Ally/*.py /app \
    && pip install -r /tmp/Interview_challenges-main/Ally/requirements.txt \
    && rm -Rf /tmp
ENTRYPOINT [ "python",  "iss_api.py" ]
