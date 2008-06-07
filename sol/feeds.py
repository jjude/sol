#Implements feeds for SOL
#ref: http://www.djangoproject.com/documentation/syndication_feeds/
#ref: http://www.andrlik.org/blog/2007/aug/03/fun-with-django-feeds/
from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist

from sol.models import sol, userprofile, group
from django.conf import settings

class LatestSOLs(Feed):
    title = '%s : Latest SOLs' % settings.SITE_NAME
    link = '/'
    description = 'Latest entries to %s' % settings.SITE_NAME

    def items(self):
        return sol.objects.order_by('-date')[:settings.FEED_SIZE]

#/feeds/category/django/
#The slug is 'category' and the params is 'django'
#ref http://blog.michaeltrier.com/2007/8/5/digging-into-django-syndication-framework
#to pass parameters to feeds

class UserSOLs(Feed):
    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'
    
    def get_object(self, bits):        
        if len(bits) < 1:
            raise ObjectDoesNotExist                
        return userprofile.objects.get(user__username__exact=bits[0])

    def title(self, obj):
        return "SOLs of '%s'" % obj.nickname

    def link(self, obj):
        return "/"

    def description(self, obj):
        return "SOLs recently posted by %s" % obj.nickname

    def items(self, obj):
        return sol.objects.filter(author__username=obj.user.username).order_by('-date')[:settings.FEED_SIZE]

class GroupSOLs(Feed):
    title_template = 'feeds/title.html'
    description_template = 'feeds/description.html'
    
    def get_object(self, bits):        
        if len(bits) < 1:
            raise ObjectDoesNotExist                
        return group.objects.get(id__exact=bits[0])

    def title(self, obj):
        return "SOLs in '%s'" % obj.desc

    def link(self, obj):
        return "/"

    def description(self, obj):
        return "SOLs recently posted in %s" % obj.desc

    def items(self, obj):
        return sol.objects.filter(group=group.objects.get(id=obj.id)).order_by('-date')[:settings.FEED_SIZE]
