FROM python:3.12-alpine
RUN apk add --no-cache ca-certificates && update-ca-certificates
RUN pip install --no-cache-dir redis flower celery==5.4.0
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1
EXPOSE 5555
USER root
