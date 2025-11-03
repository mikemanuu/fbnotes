Production deployment files for fb-notes

Files included in this folder:
- Dockerfile
- docker-compose.prod.yml
- nginx/nginx.conf
- .env.example
- .dockerignore
- prod_settings_snippet.txt

Instructions:
1. Copy .env.example to .env and set SECRET_KEY and ALLOWED_HOSTS appropriately.
2. Update your Django project settings.py to use the production settings snippet (or merge values).
3. Build and start services:
   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d
4. Run collectstatic:
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
5. Create superuser:
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
6. Check logs:
   docker-compose -f docker-compose.prod.yml logs -f
7. For SSL, set up Certbot/Nginx proxy on the host or use a managed load balancer.

Notes:
- Ensure ports 80/443 are open on your host if deploying to a server.
- Use strong secrets and a secrets manager in production.
