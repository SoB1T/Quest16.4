from django.contrib.admin import action
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .board.tasks import send_notifications
from .models import Post, PostCategory
from django.conf import settings
#
#
# def send_notifications(heading, id, text, subcribers,category_name, author):
#     # send_mail(f'{settings.DEFAULT_FROM_EMAIL}', "HI", f"{settings.DEFAULT_FROM_EMAIL}", ['retoreivszombe5@gmail.com'])
#     html_contect = render_to_string(
#         'mailcat.html',
#         {
#             'text': text,
#             'link': f'{settings.SITE_URL}/posts/{id}',
#             'category_name': category_name,
#             'heading': heading,
#             'author': author
#         }
#
#     )
#     msg = EmailMultiAlternatives(
#         subject="New post!",
#         body=text,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subcribers
#     )
#     msg.attach_alternative(html_contect, "text/html")
#
#     msg.send()
#     print("mail send")

#
# # @receiver(post_save, sender=Post)
# # def notify_new_post(sender, instance, **kwargs):
# #     if kwargs["action"] == "post.add":
# #         categories = instance.categories.all()
# #         subscribers_emails = []
# #
# #         for cat in categories:
# #             subscribers = cat.subscribers.all()
# #             subscribers_emails += [s.email for s in subscribers]
# #         send_notifications(instance.heading(), instance.id, instance.text, subscribers_emails)
#
#
@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs["action"] == 'post_add':  # Проверяем, был ли объект только что создан PostCategory.objects.filter(post_id_id= instance.id)
        send_notifications.delay(instance.pk)
