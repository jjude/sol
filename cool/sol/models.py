from django.db import models
import django.contrib.auth.models as auth
from django.newforms import ModelForm
from django import newforms as forms



# models for sol
#TODO: profile photo; blog_url etc
class userprofile(models.Model):
	user = models.ForeignKey(auth.User, unique=True)
	#here goes the profile details
	nickname = models.CharField(max_length=30)
	#profphoto = models.ImageField(upload_to='/profphoto', blank=True,null=True)
	#blog_url = models.URLField(blank=True,null=True)
	
	
	def __unicode__(self):
		return self.nickname
	
	class Admin:
		list_display = ('user','nickname')
	class Meta:
		ordering = ['nickname']

class sol(models.Model):
	body = models.TextField(max_length=150)
	author = models.ForeignKey(auth.User)
	date = models.DateTimeField('Date')
	#is it a reply to another sol?if not store the same id
	#replyto = models.ForeignKey('self')
		
	def __unicode__(self):
		return unicode(self.id)

	def get_absolute_url(self):
		return "/sol/%s/" % unicode(self.id)
		
	def get_author_url(self):
		return "/u/%s/p/0" % (self.author)
		
	def get_author_nickname(self):
		return userprofile.objects.get(user=self.author).nickname
				
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
	
						   
	class Meta:
		model = sol