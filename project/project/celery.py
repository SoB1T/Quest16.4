import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'print_every_5_seconds': {
        'task': 'news.board.tasks.send_notifications_week', #про правила именнование конечно можно было и сказать
        'schedule': crontab(hour="8", day_of_week='monday'),
        'args': (),
    },
}