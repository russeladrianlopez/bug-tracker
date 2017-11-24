web: gunicorn config.wsgi:application
worker: celery worker --app=bug_report_tool.taskapp --loglevel=info
