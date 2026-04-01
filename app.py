"""Render/Gunicorn compatibility entrypoint.

Exposes the Django WSGI application as `app` so commands like
`gunicorn app:app` continue to work.
"""

from cura.wsgi import application

app = application
