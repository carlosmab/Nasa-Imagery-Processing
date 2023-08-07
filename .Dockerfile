FROM python:3.10

ENV NASA_API_KEY='raAuAKYJcwjZ7BOVs1m5mCHISSaIrRQqE6h7DZGw'
ENV NASA_EARTH_IMAGERY_API_URL='https://api.nasa.gov/planetary/earth/imagery'
ENV BUCKET_NAME="bucket-fields-imagery"
ENV REGION_NAME='us-east-1'
ENV S3_MAX_CONNECTIONS=10
ENV AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'
ENV AWS_ACCESS_KEY_ID='AWS_ACCESS_KEY_ID'

WORKDIR /app

COPY .requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

# Create a cronjob to execute doily
RUN apt-get update && apt-get -y install cron
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob


EXPOSE 5000

# ENV MY_ENV_VAR value

CMD ["python", "src/main.py"]
