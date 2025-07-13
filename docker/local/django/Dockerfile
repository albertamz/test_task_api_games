FROM python:3.11-slim

# to see logs in real-time
ENV PYTHONUNBUFFERED=1 \
    # prevent creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip vars
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # directory for the project
    PROJECT_DIR="/code"

# Встановлюємо системні залежності для mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    python3-dev \
    build-essential \
    pkg-config \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /$PROJECT_DIR

# set work directory
WORKDIR $PROJECT_DIR
ADD . $PROJECT_DIR

# update pip
RUN pip install --upgrade pip setuptools
ADD ./requirements.txt ./

RUN mkdir logs
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN chmod +x docker/local/django/start.sh
ENTRYPOINT ["docker/local/django/start.sh"]