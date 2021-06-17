FROM python:3-onbuild

EXPOSE 13338
COPY ./src /usr/src/app
WORKDIR /usr/src/app

CMD ["gunicorn", "--bind", "0.0.0.0:13338", "--log-level=debug", "main:app"]
