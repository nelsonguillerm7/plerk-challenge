FROM python:3.8

ENV APP_DIR /app

COPY . ${APP_DIR}/
WORKDIR ${APP_DIR}

RUN pip install pipenv
RUN pipenv install --skip-lock --deploy --system

RUN chmod +x entrypoint.sh
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]