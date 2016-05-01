# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(sender, instance, **kwargs):
    context = {
        'phone': instance.phone,
        'site': Site.objects.get_current()
    }
    mname = sender._meta.model_name
    if mname == 'request':
        context['course'] = instance.content_object
        context['name'] = instance.name
        context['email'] = instance.email
        context['comment'] = instance.comment
    else:
        context['day'] = instance.get_day_display()
        context['time'] = instance.time

    subject = render_to_string('feedback/email/email_' + mname + '_subject.txt', context)
    body = render_to_string('feedback/email/email_' + mname + '_body.html', context)
    msg = EmailMultiAlternatives(subject, body, mname + '@' + Site.objects.get_current().name,
                                 ['info@emaestro.ru', 'hukutatlt@mail.ru', 'shaper2010@yandex.ru'])
    msg.content_subtype = 'html'
    msg.send()
