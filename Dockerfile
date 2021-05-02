FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE todos_app.settings
ENV ENVIRONMENT 'development'
ENV DATABASE_NAME 'todos-db'
ENV DATABASE_USER 'root'
ENV DATABASE_PASS 'password'
ENV DATABASE_HOST '172.17.0.1'
ENV DATABASE_PORT '3308'

RUN mkdir /todos_app
COPY ./ /todos_app
VOLUME ["/todos_app"]

# entrypoint
COPY docker-entrypoint.sh /entrypoint.sh
RUN [ "chmod", "755", "/entrypoint.sh" ]
ENTRYPOINT [ "/entrypoint.sh" ]

EXPOSE 8000

WORKDIR /todos_app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]