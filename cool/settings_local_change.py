DEBUG = True
TEMPLATE_DEBUG = DEBUG

# don't want emails while developing
ADMINS = ()
MANAGERS = ADMINS

## Fill these values
DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''


SECRET_KEY = 'secret'

### ACTIVE DIRECTORY SETTINGS ###

#for example look at: http://grotan.com/ldap/python-ldap-samples.html
#for spec: http://python-ldap.sourceforge.net/doc/python-ldap/ldap-objects.html

# AD_DNS_NAME should set to the AD DNS name of the domain (ie; example.com)  
# If you are not using the AD server as your DNS, it can also be set to 
# FQDN or IP of the AD server.

AD_DNS_NAME = 'ipaddress'
AD_LDAP_PORT = 389
#URL with port
AD_LDAP_URL = 'ldap://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)

#this is like 'mailid@example.com'
AD_BIND_DN = ''
#password for the above user id
AD_BIND_PW = ''

#this is search base; if it is at the root level, most probably 'DC=example, DC=com'
AD_SEARCH_DN = ''
#what are we going to get back
AD_RETRIEVE_ATTRIBUTES = ['mail','givenName','sn','sAMAccountName']

# This is the NT4/Samba domain name; most probably 'example'
AD_NT4_DOMAIN = ''

#add this as new authentication module
AUTHENTICATION_BACKENDS = ('cool.sol.auth.ActiveDirectoryBackend',)