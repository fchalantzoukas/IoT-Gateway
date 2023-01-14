FROM python:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    libglib2.0-dev

ADD requirements.txt .
ADD room-gtw.py .
ADD .env .
RUN pip3 install -r requirements.txt

CMD python3 gtw.py
