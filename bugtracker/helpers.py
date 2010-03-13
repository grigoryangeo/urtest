# File encoding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.hashcompat import sha_constructor

def render_to_request(request, *args, **kwargs):
    """render_to_response с передачей RequestContext"""
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)

def get_activation_key(user):
    """Возвращает ключ активации для пользователя"""
    username = user.username
    salt = 'v0.1 MUST DIE'
    return sha_constructor(salt + username).hexdigest()
