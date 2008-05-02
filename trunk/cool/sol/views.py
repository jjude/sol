# Create your views here.
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime

#sol models
from sol.models import userprofile, sol, solForm, group, grpForm

#for pagination
from django.core.paginator import ObjectPaginator, InvalidPage

#for user profile
from django.contrib.auth.models import SiteProfileNotAvailable
from django.db.models import get_model
from django.conf import settings
from django import newforms as forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

#for pagination: http://www.slideshare.net/simon/the-django-web-application-framework/#
#for user profile check django-profile in code.google.com

#generic view function for homepage (solhome), userhome and group home
#object is one of the param; object="u" -> user; g->group; s->sol, which is default home page
#object id : for u & g the respective ids; for sol nothing; defaults to sol(0)
#pagenum : for pagination; default is 0 otherwise the pagenumber to be displayed in the input

def home(request, model="s",objectId="0",page_num=0, template='home.html'):
	paginate_by = settings.PAGINATE_BY
	#what we get as parameter is always a string
	page_num = int(page_num)
	if model == 'u': #for user we need to filter for the user
		info_list = ObjectPaginator(sol.objects.all().filter(author__username=objectId),paginate_by)
	elif model== 's': #for sol; home page
		info_list = ObjectPaginator(sol.objects.all(),paginate_by)
	elif model =='g': #for group
		if objectId == '0':
			info_list = ObjectPaginator(group.objects.all(),paginate_by)
		else:
			info_list = ObjectPaginator(sol.objects.all().filter(group=group.objects.get(id=objectId)),paginate_by)

	#if the user altered the URL for a particular page that doesn't exist
	try:
		page_info = info_list.get_page(page_num)
	except InvalidPage:
		page_num = 0
		page_info = info_list.get_page(page_num)

	has_previous = info_list.has_previous_page(page_num)
	has_next = info_list.has_next_page(page_num)



	info_dict = {
		'query_list' : info_list.get_page(page_num),
		'has_previous' : has_previous,
		'previous_page' : page_num - 1,
		'has_next' : has_next,
		'next_page' : page_num + 1,
		'site_name' : 'sol',
		'user' : request.user,
	}

	if model == 's':
		form = solForm()
		#this is how you append to a dict
		info_dict['solForm'] = form

	if model == 'u':
		#this is how you append to a dict
		info_dict['u_id'] = objectId
		info_dict['nickname'] = userprofile.objects.get(user__username=objectId).nickname

	if model == 'g':
		info_dict['grpForm'] = grpForm()
		if objectId == '0':
			info_dict['solForm'] = solForm()
		else:
			info_dict['solForm'] = solForm(initial={'group': group.objects.get(id=objectId)})
			info_dict['grpName'] = group.objects.get(id=objectId).desc

	return render_to_response(template, info_dict)


def logout(request):
		auth.logout(request)
		return HttpResponseRedirect('/')

@login_required
def createsol(request):
	#newsol = sol(request.POST['body'], request.user,datetime.datetime.today())
	#if there is nothing in the text field, do nothing
	if request.POST['body'] == "":
		return HttpResponseRedirect('/')

	newsol = sol()
	newsol.author = request.user
	newsol.date = datetime.datetime.today()
	newsol.body = request.POST['body']
	if request.POST['group'] <> '':
		newsol.group = group.objects.get(id=request.POST['group'])
	newsol.save()
	return HttpResponseRedirect('/')

@login_required
def creategroup(request):
	if request.POST['desc'] == "":
		return HttpResponseRedirect('/groups/')

	newgrp = group()
	newgrp.desc = request.POST['desc']
	newgrp.save()
	return HttpResponseRedirect('/groups/')

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
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = profile_mod
            exclude = ('user',)
    return ProfileForm

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