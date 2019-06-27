FROM python:3.7-alpine

ENV APP_USER    app
ENV APP_GRP     app
ENV APP_HOME    /opt/application
ENV PYTHONPATH  /opt/application
ENV PATH        /entrypoint:$PATH

RUN apk update && \
 apk add libpq postgresql-dev build-base libintl && \
 apk add --no-cache git supervisor openssh && \
 apk add --virtual .build-deps gcc musl-dev gettext && \
 cp /usr/bin/envsubst /usr/local/bin/envsubst && \
 apk --purge del .build-deps && \
 mkdir -p /etc/supervisor/conf.d/ /opt/run/ /var/log/supervisor/

RUN cat etc/supervisord.conf
WORKDIR ${APP_HOME}
RUN adduser -h ${APP_HOME} -D ${APP_USER} && \
 addgroup ${APP_GRP} ${APP_USER} && \
 chown ${APP_USER}:${APP_GRP} /etc/supervisord.conf /etc/supervisor/conf.d/ /opt/run/
COPY ./app ${APP_HOME}
COPY Pipfile ${APP_HOME}/Pipfile
COPY Pipfile.lock ${APP_HOME}/Pipfile.lock
RUN pip install -U pip && pip install pipenv && pipenv install --system --deploy

COPY bin/entrypoint.sh /entrypoint/entrypoint.sh
COPY bin/wait.sh /entrypoint/wait.sh
RUN chmod -R 755 /entrypoint/
COPY bin/supervisor /etc/supervisor

CMD ["/entrypoint/entrypoint.sh"]
