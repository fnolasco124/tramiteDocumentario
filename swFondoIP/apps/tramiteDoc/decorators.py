#! /usr/bin/env python
# -*- encoding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from functools import wraps
from django.shortcuts import render_to_response
from django.template import RequestContext

def access_permission(permission):
	def decorator(func):
		def inner_decorator(request, *args, **kwargs):
			try:
				a = int(request.user.TipoUsuario)
				if permission.__contains__(int(request.user.TipoUsuario)) :
					return func(request, *args, **kwargs)
				else:
					return render_to_response('404.html', context_instance=RequestContext(request))
			except AttributeError as ae:
					return HttpResponseRedirect('/')
			
		return wraps(func)(inner_decorator)
	return decorator
