FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1

ENV APP_HOME /app
ENV SRC_HOME $APP_HOME/src
ENV VENV_HOME $APP_HOME/venv

ENV PYW_USER pyw
ENV PYW_USER_UID 1000
ENV PYW_GROUP pyw
ENV PYW_GROUP_GID 1000

RUN set -eux; \
    apt-get -qq update; \
    apt-get -qqy install  \
        apt-utils \
        python-virtualenv \
        build-essential; \
    rm -rf /var/lib/apt/lists/*;

RUN groupadd -r -g $PYW_GROUP_GID $PYW_GROUP && useradd -r -u $PYW_USER_UID -d $APP_HOME -g $PYW_GROUP $PYW_USER
RUN mkdir -p $SRC_HOME && mkdir -p $VENV_HOME
RUN chown -R $PYW_USER:$PYW_GROUP $SRC_HOME $VENV_HOME

WORKDIR $APP_HOME
RUN virtualenv -p python $VENV_HOME
COPY ./requirements.txt $SRC_HOME
SHELL ["/bin/bash", "-c"]
RUN source $VENV_HOME/bin/activate && pip install -r $SRC_HOME/requirements.txt
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
COPY . $SRC_HOME
RUN chmod +x /docker-entrypoint.sh && chown $PYW_USER:$PYW_GROUP /docker-entrypoint.sh && chown $PYW_USER:$PYW_GROUP $SRC_HOME
USER $PYW_USER

ENTRYPOINT ["/docker-entrypoint.sh"]