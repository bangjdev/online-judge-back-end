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
ENV DEBUG=True
ENV PORT=8000
ENV SECRET_KEY=3zq%s_=iq@9o^s93-39*)jz&q3aj#%+3kxd*xsb)vj$)qdrddt
ENV FRONTEND_ORIGIN=http://localhost:3000
ENV FRONTEND_HOST=*
ENV DATABASE_HOST=db
ENV DATABASE_PORT=5432
ENV DATABASE_NAME=codegang
ENV DATABASE_USER=admin
ENV DATABASE_PWD=123456

ENV REDIS_URL=redis://redis:6379/



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
