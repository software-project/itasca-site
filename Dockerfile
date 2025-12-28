# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
FROM python:3.12-slim-bookworm

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
&& rm -rf /var/lib/apt/lists/*

# Install Node.js (LTS version)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==20.0.4"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /home/ubuntu/www/itasca as the working directory where the source code is stored.
WORKDIR /home/ubuntu/www/itasca

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Verify Node.js and npm are installed
RUN node --version && npm --version

# Ensure CSS output directory exists
RUN mkdir -p /home/ubuntu/www/itasca/itasca/static/css && chown wagtail:wagtail /home/ubuntu/www/itasca/itasca/static/css

# Install npm dependencies and build CSS (as root, before switching users)
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps
RUN npm run build:css

# Fix ownership of the entire working directory (including node_modules and generated files)
RUN chown -R wagtail:wagtail /home/ubuntu/www/itasca

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
CMD set -xe; python manage.py migrate --noinput; gunicorn itasca.wsgi:application
