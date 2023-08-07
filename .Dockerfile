FROM python:3.10

WORKDIR /app

COPY .requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob


EXPOSE 5000

# ENV MY_ENV_VAR value

CMD ["python", "src/main.py"]
