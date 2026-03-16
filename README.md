# itasca-site

Wagtail CMS site for [itasca.pl](https://itasca.pl), running on Django 5.2 with Tailwind CSS.

## Tech Stack

- **Backend:** Django 5.2 / Wagtail 7.2
- **Database:** PostgreSQL 17
- **Styling:** Tailwind CSS 3.4
- **App Server:** Gunicorn behind Nginx reverse proxy
- **SSL:** Let's Encrypt
- **Containerisation:** Docker + Docker Compose

## Local Development

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (for Tailwind)
npm install

# Watch for CSS changes during development
npm run watch:css

# Run the Django dev server
python manage.py runserver
```

## Deploying Changes

### 1. Push your changes

Commit and push to the `main` branch:

```bash
git add .
git commit -m "Describe your change"
git push origin main
```

### 2. SSH into the server

```bash
ssh ubuntu@vps-98d74c7b.vps.ovh.net
```

### 3. Pull the latest code

```bash
cd /home/ubuntu/www/itasca
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_deploy
git pull
docker-compose build
docker-compose down
docker-compose up -d
```

### 4. Rebuild and restart the containers

```bash
docker compose up -d --build
```

This single command will:
- Rebuild the Docker image (installs dependencies, builds Tailwind CSS, collects static files)
- Run database migrations on startup
- Restart the application with zero-downtime container replacement

### 5. Verify the deployment

```bash
# Check that containers are running
docker compose ps

# Tail the logs to spot any errors
docker compose logs -f --tail=50 web
```

### Running One-Off Management Commands

To run Django management commands inside the running container:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell
```

### Rollback

If something goes wrong, revert to the previous commit and rebuild:

```bash
git revert HEAD
docker compose up -d --build
```

### Environment Variables

Production settings are loaded from a `.env` file on the server. Required variables:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames |
| `DB_NAME` | PostgreSQL database name (default: `itasca_db`) |
| `DB_USER` | PostgreSQL user (default: `itasca_user`) |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (default: `db` — the compose service) |
| `DB_PORT` | Database port (default: `5432`) |
| `WAGTAILADMIN_BASE_URL` | Public URL for the Wagtail admin |
| `DEBUG` | Set to `True` only for debugging (default: `False`) |
