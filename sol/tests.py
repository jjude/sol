from django.test import TestCase
from django.contrib.auth.models import User
import os
import sys
import logging
from cool.sol.models import userprofile

##############################################
# Note: test functions should start with test (case sensitive)
# Ref:http://www.djangoproject.com/documentation/models/test_client/
#    http://www.djangoproject.com/documentation/testing/
#    http://www.satchmoproject.com/trac/browser/satchmo/trunk/satchmo/shop/tests.py?rev=1159
#    http://code.google.com/p/django-firebird/source/browse/trunk/tests/regressiontests/test_client_regress/models.py?r=2
#    http://www.lethain.com/entry/2007/dec/04/two-faced-django-part-2-models-and-django-testing/
##############################################
class SOLTests(TestCase):
    def setUp(self):
        #test data setup applicable for all test cases
        #create a logger
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename= os.getcwd() + os.sep + 'sol.log',
            filemode='w')

        #let us create users for this testing
        newuser = User.objects.create_user(username='jjude',email='jjude@example.com',password='jjude')
        newuser.is_staff=True
        newuser.save()
        #create userprof
        uprof = userprofile(user=newuser, nickname = 'jjude')
        uprof.save()

        newuser = User.objects.create_user(username='bob',email='bob@example.com',password='bob')
        newuser.is_staff=True
        newuser.save()

        #create userprof
        uprof = userprofile(user=newuser, nickname = 'bob')
        uprof.save()


    def test_TemplateUsed(self):
        #test if proper templates are used
        logging.debug('####################################################')
        logging.debug('testing templates used')
        logging.debug('####################################################')

        response=self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

        response=self.client.get('/groups/')
        self.assertTemplateUsed(response,'groups_home.html')

        response=self.client.get('/help/')
        self.assertTemplateUsed(response,'help.html')

        response=self.client.get('/login/')
        self.assertTemplateUsed(response,'login.html')


    def test_Links(self):
        logging.debug('####################################################')
        logging.debug('testing links')
        logging.debug('####################################################')
        response = self.client.get('/')
        self.failUnlessEqual(response.status_code, 200)
        #check if it contains these links
        self.assertContains(response,'<a href="/" title="Home">Home</a>')
        self.assertContains(response,'<a href="/help" title="Help">Help</a>')
        self.assertContains(response,'<a href="/groups">Groups</a>')
        #initially there should be only login; afterwards, log off
        self.assertContains(response,'<a href="/login" title="login">Login</a>')

        #let us login and check userprofile template
        response=self.client.login(username='jjude',password='jjude')
        self.assertEquals(response, True)

        response=self.client.get('/profile/')
        self.assertContains(response,'<input id="id_nickname" type="text" name="nickname" value="jjude" maxlength="30" />')

        response=self.client.get('/')
        #this is a negative condition
        try:
            self.assertContains(response,'<a href="/login" title="login">Login</a>')
        except AssertionError, e:
            self.assertEquals(str(e), "Couldn't find '<a href=\"/login\" title=\"login\">Login</a>' in response")

        #but it should contain logoff now
        self.assertContains(response,'<a href="/logout" title="log off">Logoff</a>')
        response=self.client.logout()
        #now logoff shouldn't be present
        try:
            response=self.client.get('/')
            self.assertContains(response,'<a href="/logout" title="log off">Logoff</a>')
        except AssertionError, e:
            self.assertEquals(str(e), "Couldn't find '<a href=\"/logout\" title=\"log off\">Logoff</a>' in response")

    def test_creategroup(self):
        #groups can be created only after logging in
        #but groups are visible even without logging in
        logging.debug('####################################################')
        logging.debug('testing create groups')
        logging.debug('####################################################')

        #there should be 0 groups
        response=self.client.get('/groups/')
        #i have no idea why this is having a context array
        self.assertEquals(len(response.context[1]['query_list']),0)

        #creation of group not possible without login
        try:
            self.assertContains(response,'<input type="submit" value="Create" />')
        except AssertionError, e:
            self.assertEquals(str(e),"Couldn't find '<input type=\"submit\" value=\"Create\" />' in response")

        #login and create groups
        response=self.client.login(username='jjude',password='jjude')
        self.assertEquals(response, True)

        post_data={'desc':'first group'}
        response = self.client.post('/creategroup/', post_data)

        #now there should be 1 group
        response=self.client.get('/groups/')
        #i have no idea why this is having a context array
        self.assertEquals(len(response.context[1]['query_list']),1)

        self.client.logout()

    def test_createsol(self):
        #sols can be created only after logging in
        #but sols are visible even without logging in
        logging.debug('####################################################')
        logging.debug('testing create sols')
        logging.debug('####################################################')

        #there should be 0 sols
        response=self.client.get('/')
        #i have no idea why this is having a context array
        self.assertEquals(len(response.context[1]['query_list']),0)

        #creation of sol not possible without login
        try:
            self.assertContains(response,'<input type="submit" value="Create" />')
        except AssertionError, e:
            self.assertEquals(str(e),"Couldn't find '<input type=\"submit\" value=\"Create\" />' in response")

        #login and create sol
        response=self.client.login(username='jjude',password='jjude')
        self.assertEquals(response, True)

        post_data={'body':'test sol from testclient', 'group':''}
        response = self.client.post('/createsol/', post_data)

        #create a group and post a sol there
        post_data={'desc':'first group'}
        response = self.client.post('/creategroup/', post_data)

        #post in the group that we just created
        post_data={'body':'second sol from testclient', 'group':'1'}
        response = self.client.post('/createsol/', post_data)

        self.client.logout()

        #now there should be 1 sol
        response=self.client.get('/')
        #i have no idea why this is having a context array
        self.assertEquals(len(response.context[1]['query_list']),2)

    def test_pagination(self):
        #add 100 sols as diff users and test pagination for sols, groups and users
        logging.debug('####################################################')
        logging.debug('testing pagination')
        logging.debug('####################################################')

        #first one has to login
        #login and create groups
        response=self.client.login(username='jjude',password='jjude')
        self.assertEquals(response, True)

        for i in range(105):
            grp_name = 'group_num_%d' % i
            post_data={'desc':grp_name}
            response = self.client.post('/creategroup/', post_data)
            #after creation it will be re directed; so the status code is 302
            self.failUnlessEqual(response.status_code, 302)

        response=self.client.get('/groups/')
        #i have no idea why this is having a context array
        #we added 105; but there will be only 100 coz that is what is set as pagination
        self.assertEquals(len(response.context[1]['query_list']),100)
        #pagination is set for 100 so there should be nextpg in context
        self.assertEquals(response.context[1]['has_next'],True)

        #lets navigate to next page
        response=self.client.get('/groups/p/2/')
        self.assertEquals(response.context[1]['has_next'],False)
        self.assertEquals(response.context[1]['has_previous'],True)

        #try to access an non-existing page
        #this is already handled in views; will be redirected to page_num=0
        response=self.client.get('/groups/p/3/')
        self.assertEquals(response.context[1]['has_next'],True)
        self.assertEquals(response.context[1]['has_previous'],False)


        #let us add sol as one user in first group
        current_user = response.context[0]['user'].username
        for i in range(105):
            sol_body = 'test sol ' + str(i) + ' for user ' + current_user
            post_data = {'body':sol_body, 'group':'1'}
            response = self.client.post('/createsol/', post_data)

        #login as next user and create sols
        self.client.logout()
        response=self.client.login(username='bob',password='bob')
        self.assertEquals(response, True)
        #add sols as this user
        response=self.client.get('/')
        current_user = response.context[0]['user'].username
        for i in range(105):
            sol_body = 'test sol ' + str(i) + ' for user ' + current_user
            post_data = {'body':sol_body, 'group':'2'}
            response = self.client.post('/createsol/', post_data)

        self.client.logout()
        #we got 210 sols now; 105 in 1 grp and 105 in another
        #now let us test pagination for sols
        response=self.client.get('/')
        #i have no idea why this is having a context array
        #there will be only 100 coz that is what is set as pagination
        self.assertEquals(len(response.context[1]['query_list']),100)
        #pagination is set for 100 so there should be nextpg in context
        self.assertEquals(response.context[1]['has_next'],True)

        #lets navigate to next page
        response=self.client.get('/p/2/')
        self.assertEquals(response.context[1]['has_next'],True)
        self.assertEquals(response.context[1]['has_previous'],True)

        #try to access an non-existing page
        #this is already handled in views; will be redirected to page_num=0
        response=self.client.get('/p/6/')
        self.assertEquals(response.context[1]['has_next'],True)
        self.assertEquals(response.context[1]['has_previous'],False)