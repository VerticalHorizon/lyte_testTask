#!/bin/sh

set -eo pipefail

/entrypoint/wait.sh;

if ! [ -z "$APP_MIGRATE" ]; then
  python manage.py migrate
fi

if ! [ -z "$APP_CREATE_SUPERUSER" ]; then
  echo "from django.contrib.auth import get_user_model; bool(get_user_model().objects.filter(username='admin').count()) or get_user_model().objects.create_superuser('admin', 'admin@example.com', 'secret')" | python manage.py shell
fi

main() {
    config
    exec /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf
}

config() {
    export APP_WSGI_APPLICATION=${APP_WSGI_APPLICATION:-"app.wsgi:application"}
    export APP_GUNICORN_MAX_REQUESTS=${APP_GUNICORN_MAX_REQUESTS:-"1000"}

    # (2 Workers * CPU Cores) + 1
    APP_WORKERS_DEFAULT=$(($(nproc) * 2 + 1))
    export APP_WORKERS=${APP_WORKERS:-$APP_WORKERS_DEFAULT}

    export APP_HOST=${APP_HOST:-"0.0.0.0"}
    export APP_PORT=${APP_PORT:-"8000"}

    # Start application depend on ROLE
    if [ "${CONTAINER_ROLE}" = 'worker' ] ; then
        envsubst < "/etc/supervisor/celery.conf" > /etc/supervisor/conf.d/celery.conf
    elif [ "${CONTAINER_ROLE}" = 'monitor' ] ; then
        envsubst < "/etc/supervisor/flower.conf" > /etc/supervisor/conf.d/flower.conf
    else
        if ! [ -z "$DEBUG" ]; then
            python manage.py runserver ${APP_HOST}:${APP_PORT}
        else
            python manage.py collectstatic --noinput
            envsubst < "/etc/supervisor/gunicorn.conf" > /etc/supervisor/conf.d/gunicorn.conf
        fi
    fi
}

main "$@"