FROM python:3.8.1-alpine

# Send python output is set straight to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set the working directory to /backend
WORKDIR /backend

# Install required gcc compilers, bash and 
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        bash \
                        postgresql-dev

# Add timezone required
RUN apk add tzdata

RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install any needed packages specified in requirements.txt
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 1337
