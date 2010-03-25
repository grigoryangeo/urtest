# File encoding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_to_request(request, *args, **kwargs):
    """render_to_response с передачей RequestContext"""
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)