# Lyte TestTask

### Challenge

1. Create a new web application using django

2. Scrape the Eventbrite API for public events

    https://www.eventbrite.com/developer/v3/endpoints/events/

    Don't scrape everything (unless you want to) just scrape enough to finish the rest of the project.

3. Store and/or structure the events that you scrape into your django application

4. Inside your django app, create a searchable api endpoint (returns json) allow the api request to search for event name, event start date, organizer name, ticket cost.

5. Inside your application, create 1 API endpoint that accepts json that allows a user to update the locally stored event record, create some arbitrary validations.

6. Send us the code and the url to your hosted application.


### Install

1. Create `.env` file in root folder with following contents. Replace the appropriate values:

```bash
#DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
#APP_WSGI_APPLICATION=app.wsgi.application # with DEBUG=True
APP_WSGI_APPLICATION=app.wsgi:application
DATABASE_URL=postgresql://lyte_user:secret@database:5432/lyte_app
CELERY_BROKER_URL=amqp://lyte_user:secret@rabbitmq:5672/
CELERY_TASK_ALWAYS_EAGER=True
CELERY_LOG_LEVEL=info
ELASTICSEARCH_URL=http://elasticsearch:9200/
ALLOWED_HOSTS=*
TIME_ZONE=Europe/Minsk
EVENBRITE_KEY=your-eventbrite-key
EVENTBRITE_SECRET=your-eventbrite-secret
EVENTBRITE_OAUTH_TOKEN=your-eventbrite-oauth-token
EVENTBRITE_SEARCH_LATITUDE=events-latitude
EVENTBRITE_SEARCH_LONGITUDE=events-longitude
EVENTBRITE_SEARCH_WITHIN=15km
```

2. Run ``` docker-compose up --build -d ```

### Entrypoints:

    - /api/events           [GET]
    - /api/events/<pk>/     [GET, PUT]
    - /api/events/search/   [POST]  (You can find examples in ./requests)
    - /api/signin/          [POST with username & password (json)]
    - /api/refresh/         [POST with token (json)]
    - /api/verify/          [POST with token (json)]
    - /admin/               (as usual :) )
