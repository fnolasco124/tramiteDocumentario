from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login
#from .views import Logout_View, Login_View


urlpatterns = patterns('',

#	url(r'^$' , Login_View, name='Login_View'),
	url(r'^$' , login, {'template_name':'frmlogin.html'}, name='login'),
	url(r'^$' , logout_then_login, {'template_name':'frmlogin.html'},name='logout'),
#	url(r'^$', Logout_View.as_view(), name ='Logout_View'),

	
)
