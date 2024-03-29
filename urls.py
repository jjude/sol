"""
urls for Sol
"""

from django.conf.urls.defaults import *
from sol.feeds import *
from sol.models import userprofile, sol, solForm

from django.conf import settings

#the views for these are defined in cool.sol.view
urlpatterns = patterns('sol.views',
     #homepage for sol with pagination enabled
     #url like: http://sol.com/p/0
     (r'^p/(?P<page_num>\d+)/$', 'home',{'template':'home.html', 'model':'s'}),
     
     #default page number is 0;
     #url like: http://sol.com/
     (r'^$', 'home'),

     #user homepage - login for normal employees with employee ids as numbers;
     #params are passed inline; view is defined in views.py
     #url like: http://sol.com/u/1029/p/0
     (r'^u/(?P<objectId>\d+)/p/(?P<page_num>\d+)/$', 'home',{'template':'user_home.html', 'model':'u'}),

     #url for individual sol
     #url like: http://sol.com/sol/10
     (r'^sol/(?P<objectId>\d+)/$', 'home',{'template':'sol.html', 'model':'s'}),
     

    #user homepage - login for contract employees with employee ids as chars;
    #url like: http://sol.com/u/jjude/p/0
     (r'^u/(?P<objectId>[A-Za-z]+)/p/(\d+)/$', 'home',{'template':'user_home.html', 'model':'u'}),

     #groups homepage
     #params are passed inline; view is defined in views.py
     #url like: http://sol.com/groups/ or http://sol.com/groups/p/0
     (r'^groups/$', 'home',{'template':'groups_home.html', 'model':'g'}),
     (r'^groups/p/(?P<page_num>\d+)/$', 'home',{'template':'groups_home.html', 'model':'g'}),

     #homepage for a particular group
     #url like: http://sol.com/g/100/p/0
     (r'^g/(?P<objectId>\d+)/$', 'home',{'template':'group_home.html', 'model':'g'}),
     (r'^g/(?P<objectId>\d+)/p/(?P<page_num>\d+)/$', 'home',{'template':'group_home.html', 'model':'g'}),

     #logoff
     (r'^logout/$', 'logout'),

     #create a sol; called by form action
     (r'^createsol/$', 'createsol'),

     #create a group; called by form action
     (r'^creategroup/$', 'creategroup'),

     #help
     (r'^help/$', 'help'),

     #user profile
     (r'^profile/$', 'user_profile'),
)

# RSS Feed
urlpatterns += patterns('django.contrib.syndication.views',
    (r'^feeds/(?P<url>.*)/$', 'feed', {'feed_dict': {
            'latest': LatestSOLs,
            'user': UserSOLs,            
            'group': GroupSOLs}
        }
    ),
)

#these are derived from admin
urlpatterns += patterns('',
        #login page
        (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
        #admin page
        (r'^admin/', include('django.contrib.admin.urls')),

)
#serve css files for this site, if in development mode
if settings.INSTANCE==0 or settings.INSTANCE==1:
    urlpatterns += patterns('',
        #this is to serve css
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL}, ),
        #this is to serve image files
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_URL + 'files/' }),
    )