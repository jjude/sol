from django.contrib.auth.models import User
from django.conf import settings
from cool.sol.models import userprofile
import ldap

#autenticate user against LDAP. parameters are defined in settings_local.py

class ActiveDirectoryBackend:

  def authenticate(self,username=None,password=None):
    if not self.is_valid(username,password):
      return None
    #try to get the user object from local database; if not found then
    #find from AD server; if found, get other values for the user and
    #create a userprofile
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
        l = ldap.initialize(settings.AD_LDAP_URL)
        l.simple_bind_s(settings.AD_BIND_DN,settings.AD_BIND_PW)
        ldap_result_id = l.search(settings.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, "sAMAccountName=%s" %username, settings.AD_RETRIEVE_ATTRIBUTES)
        result_type, result_data = l.result(ldap_result_id, 0)
        result = result_data[0][1]

        # givenName == First Name
        if result.has_key('givenName'):
            first_name = result['givenName'][0]
        else:
            first_name = None

        # sn == Last Name (Surname)
        if result.has_key('sn'):
            last_name = result['sn'][0]
        else:
            last_name = None

        # mail == Email Address
        if result.has_key('mail'):
            email = result['mail'][0]
        else:
            email = None

        #create the new user
        newuser = User(username=username,first_name=first_name,last_name=last_name,email=email)
        newuser.is_staff = True
        newuser.is_superuser = False
        newuser.set_password(password)
        newuser.save()
        
        #create the user profile
        uprof = userprofile(user=newuser, nickname = first_name)
        uprof.save()
        
        user=newuser
        
    return user

  def get_user(self,user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None

  def is_valid (self,username=None,password=None):
    binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
    try:
      l = ldap.open(settings.AD_DNS_NAME)
      l.simple_bind_s(binddn,password)
      l.unbind_s()
      return True
    except ldap.LDAPError:
      return False
