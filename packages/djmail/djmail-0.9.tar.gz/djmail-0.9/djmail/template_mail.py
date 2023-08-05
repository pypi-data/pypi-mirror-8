# -*- encoding: utf-8 -*-

from __future__ import print_function

import functools
import logging

from django.conf import settings
from django.core import mail
from django.utils import translation
try:
    # Django >= 1.4.5
    from django.utils.six import string_types
except ImportError:
    # Django < 1.4.5
    string_types = basestring
from django.template import loader, TemplateDoesNotExist

from . import models
from . import exceptions as exc


log = logging.getLogger("djmail")


def _get_body_template_prototype():
    return getattr(settings, "DJMAIL_BODY_TEMPLATE_PROTOTYPE",
                   "emails/{name}-body-{type}.{ext}")


def _get_subject_template_prototype():
    return getattr(settings, "DJMAIL_SUBJECT_TEMPLATE_PROTOTYPE",
                   "emails/{name}-subject.{ext}")


def _get_template_extension():
    return getattr(settings, "DJMAIL_TEMPLATE_EXTENSION", "html")


def _trap_exception(function):
    """
    Simple decorator for catch template exceptions. If exception is throwed,
    this decorator by default returns an empty string.
    """
    @functools.wraps(function)
    def _decorator(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except TemplateDoesNotExist as e:
            log.warning("Template '{0}' does not exists.".format(e))
            return u""

    return _decorator


def _trap_language(function):
    """
    Decorator that intercept a language attribute and set it on context of
    the execution.
    """
    @functools.wraps(function)
    def _decorator(self, context):
        language_new = None
        language_old = translation.get_language()

        # If attr found on context, set a new language
        if "lang" in context:
            language_new = context["lang"]
            translation.activate(language_new)

        try:
            return function(self, context)
        finally:
            if language_new is not None:
                translation.activate(language_old)

    return _decorator


class TemplateMail(object):
    name = None

    def __init__(self, name=None):
        self._email = None
        if name is not None:
            self.name = name

        self._initialize_settings()

    def _initialize_settings(self):
        self._body_template_name = _get_body_template_prototype()
        self._subject_template_name = _get_subject_template_prototype()

    @_trap_exception
    @_trap_language
    def _render_message_body_as_html(self, context):
        template_ext = _get_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name, "type": "html"})

        return loader.render_to_string(template_name, context)

    @_trap_exception
    @_trap_language
    def _render_message_body_as_txt(self, context):
        template_ext = _get_template_extension()
        template_name = self._body_template_name.format(**{
            "ext": template_ext, "name": self.name, "type": "text"})

        return loader.render_to_string(template_name, context)

    def _render_message_subject(self, context):
        template_ext = _get_template_extension()
        template_name = self._subject_template_name.format(**{
            "ext": template_ext, "name": self.name})

        try:
            subject = loader.render_to_string(template_name, context)
        except TemplateDoesNotExist as e:
            raise exc.TemplateNotFound("Template '{0}' does not exists.".format(e))
        return u" ".join(subject.strip().split())

    def _attach_body_to_email_instance(self, email, context):
        body_html = self._render_message_body_as_html(context)
        body_txt = self._render_message_body_as_txt(context)

        if not body_txt and not body_html:
            raise exc.TemplateNotFound("Body of email message shouldn't be empty")

        email.body = body_txt
        if isinstance(email, mail.EmailMultiAlternatives):
            email.attach_alternative(body_html, "text/html")

    def _attach_subject_to_email_instance(self, email, context):
        email.subject = self._render_message_subject(context)

    def make_email_object(self, to, context, **kwargs):
        if not isinstance(to, (list, tuple)):
            to = [to]

        email = mail.EmailMultiAlternatives(**kwargs)
        email.to = to

        self._attach_body_to_email_instance(email, context)
        self._attach_subject_to_email_instance(email, context)
        return email

    def send(self, to, context, **kwargs):
        email = self.make_email_object(to, context, **kwargs)
        return email.send()


class InlineCSSTemplateMail(TemplateMail):

    def _render_message_body_as_html(self, context):
        # Transform CSS into line style attributes
        import premailer
        return premailer.transform(super()._render_message_body_as_html(context))


class MagicMailBuilder(object):
    def __init__(self, email_attr="email", lang_attr="lang",
                 template_mail_cls=TemplateMail):
        self._email_attr = email_attr
        self._lang_attr = lang_attr
        self._template_mail_cls = template_mail_cls

    def __getattr__(self, name):
        def _dynamic_email_generator(to, context, priority=models.PRIORITY_STANDARD):
            lang = None

            if not isinstance(to, string_types):
                if not hasattr(to, self._email_attr):
                    raise AttributeError(
                        "'to' parameter does not "
                        "have '{0}' attribute".format(self._email_attr))

                lang = getattr(to, self._lang_attr, None)
                to = getattr(to, self._email_attr)

            if lang is not None:
                context["lang"] = lang

            template_email = self._template_mail_cls(name=name)
            email_instance = template_email.make_email_object(to, context)
            email_instance.priority = priority

            return email_instance

        return _dynamic_email_generator
