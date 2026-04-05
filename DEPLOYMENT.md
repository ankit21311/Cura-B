# Deployment Guide for Render

## Prerequisites
- Neon PostgreSQL database (Already configured with `DATABASE_URL` in `.env`)
- Render account (https://render.com)
- GitHub repository with this code

## Deployment Steps

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit: Render deployment ready"
git branch -M main
git remote add origin https://github.com/your-username/cura.git
git push -u origin main
```

### 2. Deploy on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name:** cura
   - **Runtime:** Python 3.14
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn cura.wsgi:application --bind 0.0.0.0:$PORT`

### 3. Set Environment Variables on Render

Add these in the Render dashboard under "Environment":

| Key | Value | Notes |
|-----|-------|-------|
| `DEBUG` | `False` | Production mode |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Only send over HTTPS |
| `CSRF_COOKIE_SECURE` | `True` | Only send over HTTPS |
| `SECRET_KEY` | Generate a new one | Use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DATABASE_URL` | Your Neon PostgreSQL URL | From `.env` |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` | Your actual domain |
| `OPENAI_API_KEY` | Your API key | Keep this secret! |

### 4. Deploy
Click "Deploy" and monitor the build logs. Once deployed, your app will be available at:
```
https://cura.onrender.com
```

## Troubleshooting

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly in Render
- Check Neon database connection string
- Run migrations: `python manage.py migrate`

### CSRF Token Errors
- Check `CSRF_TRUSTED_ORIGINS` in settings.py
- Ensure your domain is in the allowed list

### 500 Errors
- Check Render logs in the dashboard
- View Django logs: `python manage.py shell` and test database connection

## Production Checklist

- [x] DEBUG = False
- [x] SECRET_KEY environment variable set
- [x] ALLOWED_HOSTS configured
- [x] Database migrated
- [x] Static files collected
- [x] SSL/HTTPS enabled
- [x] secure cookies configured
- [x] CSRF protection configured
- [x] Gunicorn as WSGI server
- [x] WhiteNoise for static files

## Useful Commands

### Local Testing Before Deployment
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run local server
python manage.py runserver
```

### Monitor Deployment
```bash
# View logs in Render dashboard or use:
# SSH into Render instance if needed
```

## Post-Deployment

1. Create superuser:
   - SSH into Render instance or use Render console
   - Run: `python manage.py createsuperuser`

2. Access admin:
   - Go to `https://yourdomain.onrender.com/admin`

3. Monitor logs:
   - Watch Render dashboard for errors

## Support

For issues, check:
- Render docs: https://render.com/docs
- Django docs: https://docs.djangoproject.com
- Neon docs: https://neon.tech/docs
