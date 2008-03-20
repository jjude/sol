"""
urls for Sol

"""

from django.conf.urls.defaults import *
from cool.sol.models import userprofile, sol, solForm

from django.conf import settings

urlpatterns = patterns('',
     #homepage for sol with pagination enabled
     (r'^p/(\d+)/$', 'cool.sol.views.home'),
     
     #default page number is 0; 
     (r'^$', 'cool.sol.views.home'),
     
     #user homepage; params are passed inline; view is defined in views.py
     (r'^u/(\d+)/p/(\d+)/$', 'cool.sol.views.user_home'),
     
     #login page
     (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     
     #accounts/login called by login_required decorator; have to find a better way to handle
     (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
     
     #logoff
     (r'^logout/$', 'cool.sol.views.logout'),
     
     #create a sol
     (r'^createsol/$', 'cool.sol.views.createsol'),
     
     #help
     (r'^help/$', 'cool.sol.views.help'),
     
     #user profile
     (r'^profile/$', 'cool.sol.views.user_profile'),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

)