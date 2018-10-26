# TODO: change tag to latest
FROM frictionlessdata/datapackage-pipelines:v2.0.0rc

RUN apk --update --no-cache add libpq postgresql-dev libffi libffi-dev build-base python3-dev ca-certificates
RUN update-ca-certificates
RUN apk add --update nodejs nodejs-npm
RUN npm install -g data-cli

WORKDIR /app
RUN apk add --update postgresql-client

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app

RUN mkdir -p ~/.config/datahub
RUN cp secrets/* ~/.config/datahub/

CMD ["server"]
