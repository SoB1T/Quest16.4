from datetime import time

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils import timezone
from ..models import Post, Category
from django.conf import settings
# DEFAULT_FROM_EMAIL ='kir.saweliew2018@yandex.ru'
# SITE_URL = "http://127.0.0.1:8000" # знаю знаю не надо так делать но питон не позволяет импортировать с дерикторий выше
@shared_task
def send_notifications(pk):
    # send_mail(f'{settings.DEFAULT_FROM_EMAIL}', "HI", f"{settings.DEFAULT_FROM_EMAIL}", ['retoreivszombe5@gmail.com'])
    post= Post.objects.get(id=pk)
    categories = post.categories.all()
    subscribers_emails = []
    categories_names=[]
    # global DEFAULT_FROM_EMAIL, SITE_URL
    for category in categories:
        subscribers = category.subcribes.all()
        for subs in subscribers:
            subscribers_emails.append(subs.email)
            categories_names.append(category)

                # subscribers_emails.extend([subscribers.email for subscriber in subscribers])
        category_name=", ".join(str(category_name) for category_name in set(categories_names))
    if subscribers_emails:
        html_contect = render_to_string(
            'mailcat.html',
            {
                'text': post.text,
                'link': f'{settings.SITE_URL}/posts/{id}',
                'category_name': category_name,
                'heading': post.heading,
                'author': post.author
            }

        )
        msg = EmailMultiAlternatives(
            subject="New post!",
            body= post.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers_emails
        )
        msg.attach_alternative(html_contect, "text/html")
        print(send_notifications.name)
        msg.send()


@shared_task
def send_notifications_week():
    start_date = timezone.now() - timezone.timedelta(days=7)

    categories_with_subscribers = Category.objects.annotate(num_subscribers=Count('subcribes')).filter(
        num_subscribers__gt=0)
    for category in categories_with_subscribers:
        recent_posts = Post.objects.filter(date__gte=start_date, categories=category)
        subscribers = category.subcribes.all()
        subscribers_emails = []
        for subs in subscribers:
            subscribers_emails.append(subs.email)
        if subscribers_emails and recent_posts:
            html_contect = render_to_string(
                'mailsched.html',
                {
                    'category_name': str(category),
                    "posts": recent_posts
                }

            )
            msg = EmailMultiAlternatives(
                subject="New post!",
                body=f"Dude, I've been trying to create an HTML letter template.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=subscribers_emails
            )
            msg.attach_alternative(html_contect, "text/html")
            msg.send()



@shared_task
def stupid_task():
    print("Hello, world!")