FROM python:3.7-alpine3.8
RUN mkdir /app && mkdir /runctx && mkdir /cachedir
ENV ISSUECOUNTER_CACHE_FOLDER=/cachedir
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install .
WORKDIR /runctx
ENTRYPOINT ["issue_counter"]
