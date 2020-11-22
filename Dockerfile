# Base Image
FROM heroku/heroku:18

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8


# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here

# ENV DEBUG=#####################################
# ENV SECRET_KEY=#####################################
# ENV FRONTEND_ORIGIN=#####################################
# ENV FRONTEND_HOST=#####################################
# ENV DATABASE_HOST=#####################################
# ENV DATABASE_PORT=#####################################
# ENV DATABASE_NAME=#####################################
# ENV DATABASE_USER=#####################################
# ENV DATABASE_PWD=#####################################
# ENV REDIS_URL=#####################################



# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
		g++ \
		libpq-dev \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        postgresql-common \
        python-psycopg2 \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip

# Install project dependencies
# RUN pipenv install --skip-lock --system --dev
RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --noinput

EXPOSE 8000
EXPOSE 5432
