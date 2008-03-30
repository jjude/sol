from django.db import models
import django.contrib.auth.models as auth
from django.newforms import ModelForm
from django import newforms as forms
import os #for path related functions

from django.conf import settings

# models for sol
#TODO: profile photo; blog_url etc
class userprofile(models.Model):
	user = models.ForeignKey(auth.User, unique=True)
	#here goes the profile details
	nickname = models.CharField(max_length=30)
	#profphoto = models.ImageField("Your Avatar", upload_to=settings.MEDIA_URL, blank=True,null=True)
	#blog_url = models.URLField(blank=True,null=True)
		
	def __unicode__(self):
		return self.nickname
	
	#change the image avatar filename to the userid
	#ref: http://gulopine.gamemusic.org/2007/nov/07/customizing-filenames-without-patching/
	def _save_FIELD_file(self, field, filename, raw_contents, save=True):
		img_name = self.get_profphoto_filename()
		#if there is already an avatar, then delete it
		if os.path.exists(img_name):
			os.remove(img_name)
		(name,ext) = os.path.splitext(filename)
		filename = "%s%s" % (self.user,ext)		
		
		super(userprofile, self)._save_FIELD_file(field, filename, raw_contents, save)

	#def save(self):	
		#if os.path.exists():
		#	os.remove(get_profphoto_filename())
		#resize the image that is uploaded; use PIL for that
		#refer: http://superjared.com/static/code/photo_model.py
		
		#from PIL import Image
		#img_to_save = Image.open(self.get_profphoto_filename())

		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		
		#img_to_save.thumbnail(settings.AVATAR_SIZE, Image.ANTIALIAS)
		
		#save it
		#img_to_save.save(self.get_profphoto_filename())
		
		#super(userprofile,self).save()
	
	class Admin:
		list_display = ('user','nickname')
	class Meta:
		ordering = ['nickname']

class group(models.Model):
	desc = models.TextField(max_length=25)
	
	def __unicode__(self):
		return unicode(self.id)
	
	def get_absolute_url(self):
		return "/g/%s" % unicode(self.id)
		
	class Admin:
		list_display = ('id','desc')
	class Meta:
		ordering = ['-id']

class sol(models.Model):
	body = models.TextField(max_length=150)
	author = models.ForeignKey(auth.User)
	date = models.DateTimeField('Date')
	group = models.ForeignKey(group)
		
	def __unicode__(self):
		return unicode(self.id)

	def get_absolute_url(self):
		return "/sol/%s/" % unicode(self.id)
		
	def get_author_url(self):
		return "/u/%s/p/0" % (self.author)
		
	def get_author_nickname(self):
		return userprofile.objects.get(user=self.author).nickname
	
	def get_author_avatar_url(self):
		return userprofile.objects.get(user=self.author).get_profphoto_url()
				
	class Admin:
		list_display = ('author', 'body', 'date')
		date_hierarchy = 'date'
	class Meta:
		ordering = ['-date']
	
class solForm(ModelForm):
	"""
	
	"""
	body = forms.CharField(max_length=150, widget=forms.Textarea(attrs={'rows':2, 'cols': 40}),label= 'Your Sol:')
	author = forms.CharField(widget=forms.HiddenInput)
	date = forms.CharField(widget=forms.HiddenInput)
	group = forms.CharField(widget=forms.HiddenInput)
						   
	class Meta:
		model = sol
	
class grpForm(ModelForm):
	"""
	
	"""
	desc = forms.CharField(max_length=25, label= 'Create Your Group:')
							   
	class Meta:
		model = group