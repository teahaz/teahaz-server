FROM python:3-onbuild

EXPOSE 13337
COPY ./src /usr/src/app
WORKDIR /usr/src/app

CMD ["gunicorn", "--bind", "127.0.0.1:13337", "--log-level=debug", "main:app"]
