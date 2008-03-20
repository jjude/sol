# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime

#sol models
from cool.sol.models import userprofile, sol, solForm


#for pagination
from django.core.paginator import ObjectPaginator, InvalidPage


#for user profile
from django.contrib.auth.models import SiteProfileNotAvailable
from django.db.models import get_model
from django.conf import settings
from django import newforms as forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from cool.sol.models import solForm
from django.contrib.auth.models import User

#for pagination: http://www.slideshare.net/simon/the-django-web-application-framework/#
#for user profile check django-profile in code.google.com

#page_num = initially it is 0; otherwise the pagenumber to be displayed
def home(request, page_num=0):
	paginate_by = 100
	page_num = int(page_num)
	sol_list = ObjectPaginator(sol.objects.all(), paginate_by)
	has_previous = sol_list.has_previous_page(page_num)
	has_next = sol_list.has_next_page(page_num)
	
	form = solForm()
	
	sol_info_dict = {
		'sol_list' : sol_list.get_page(page_num),
		'has_previous' : has_previous,
		'previous_page' : page_num - 1,
		'has_next' : has_next,
		'next_page' : page_num + 1,
		'site_name' : 'sol',
		#need to set user in the context
		'user' : request.user,
		'solForm': form
		}
	return render_to_response('home.html',sol_info_dict)

#page_num = initially it is 0; otherwise the pagenumber to be displayed
def user_home(request,u_id, page_num=0):
	paginate_by = 100
	page_num = int(page_num)
	sol_list = ObjectPaginator(sol.objects.all().filter(author__username=u_id), paginate_by)
	has_previous = sol_list.has_previous_page(page_num)
	has_next = sol_list.has_next_page(page_num)
	
	user_info_dict = {
		'sol_list' : sol_list.get_page(page_num),
		'has_previous' : has_previous,
		'previous_page' : page_num - 1,
		'has_next' : has_next,
		'next_page' : page_num + 1,
		'u_id' : u_id,
		'nickname' : userprofile.objects.get(user__username=u_id).nickname,
		'site_name' : 'sol'
		}
	return render_to_response('user_home.html',user_info_dict)
		
def logout(request):
		auth.logout(request)
		return HttpResponseRedirect('/')
		
def createsol(request):
	#newsol = sol(request.POST['body'], request.user,datetime.datetime.today())
	if request.POST['body'] == "":
		return HttpResponseRedirect('/')
	
	newsol = sol()
	newsol.author = request.user
	newsol.date = datetime.datetime.today()
	newsol.body = request.POST['body']
	newsol.save()
	return HttpResponseRedirect('/')

def get_profile_model():
    """
    Returns the model class for the currently-active user profile
    model, as defined by the ``AUTH_PROFILE_MODULE`` setting. If that
    setting is missing, raises
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    if (not hasattr(settings, 'AUTH_PROFILE_MODULE')) or \
           (not settings.AUTH_PROFILE_MODULE):
        raise SiteProfileNotAvailable
    profile_mod = get_model(*settings.AUTH_PROFILE_MODULE.split('.'))
    if profile_mod is None:
        raise SiteProfileNotAvailable
    return profile_mod


def get_profile_form():
    """
    Returns a form class (a subclass of the default ``ModelForm``)
    suitable for creating/editing instances of the site-specific user
    profile model, as defined by the ``AUTH_PROFILE_MODULE``
    setting. If that setting is missing, raises
    ``django.contrib.auth.models.SiteProfileNotAvailable``.
    
    """
    profile_mod = get_profile_model()
    class _ProfileForm(forms.ModelForm):
        class Meta:
            model = profile_mod
            exclude = ('user',)
    return _ProfileForm

@login_required
def user_profile(request,form_class=None):
	try:
		profile_obj = request.user.get_profile()
	except ObjectDoesNotExist:
		return HttpResponseRedirect("/")
	
	#if called via template UI, form_class = none
	if form_class is None:
		form_class = get_profile_form()

	if request.method == 'POST':
		form = form_class(data=request.POST, files=request.FILES, instance=profile_obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/")
	#when called from user_profile it will have the instance
	else:
		form = form_class(instance=profile_obj)
	
	
	return render_to_response('user_profile.html',{'form': form,'profile': profile_obj, 'user': request.user})
		
def help(request):
	return render_to_response('help.html')