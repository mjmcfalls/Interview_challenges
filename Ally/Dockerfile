FROM python:3.9-slim-buster
WORKDIR /app
ADD iss_api.py /app/
ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt
ENTRYPOINT [ "python",  "iss_api.py" ]
