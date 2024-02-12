add all variables to .env:

CELERY_BROKER_URL=redis://redis:6379/0

CELERY_RESULT_BACKEND=redis://redis:6379/0

SECRET_KEY= your secret key

DEBUG=True

NAME_BD=prediction

USER_BD=prediction

PASSWORD_BD=prediction

HOST_BD=postgres

PORT_BD=5432

EMAIL_HOST_PASSWORD= your google password

EMAIL_HOST_USER= your google email

GITHUB_CLIENT_ID=git hub client id

GITHUB_CLIENT_SECRET=git hub client secret

GOOGLE_CLIENT_ID=google client id

GOOGLE_CLIENT_SECRET=google client secret

and

sudo docker compose up
