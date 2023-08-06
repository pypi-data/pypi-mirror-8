from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django_tequila.tequila_client import TequilaClient
from django_tequila.tequila_client.config import EPFLConfig
from django.conf import settings

class TequilaBackend(RemoteUserBackend):
    """
    Authenticate against a Tequila server, using the TequilaClient class
    This backend is to be used in conjunction with the ``RemoteUserMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.

    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """
    create_unknown_user = True
    
    """ Created user should be inactive by default ?"""
    try:
        set_created_user_at_inactive = settings.TEQUILA_NEW_USER_INACTIVE
    except AttributeError:
        set_created_user_at_inactive = False
    
    """ Set server url"""
    try:
        tequila_server_url = settings.TEQUILA_SERVER_URL
    except AttributeError:
        tequila_server_url = "" 
    
    def authenticate(self, tequila_key):
        """
        The username passed as ``remote_user`` is considered trusted.  This
        method simply returns the ``User`` object with the given username,
        creating a new ``User`` object if ``create_unknown_user`` is ``True``.

        Returns None if ``create_unknown_user`` is ``False`` and a ``User``
        object with the given username is not found in the database.
        """
        if not tequila_key:
            return
        user = None

        if self.tequila_server_url:
            user_attributes = TequilaClient(EPFLConfig(server_url = self.tequila_server_url)).get_attributes(tequila_key)
        else:
            user_attributes = TequilaClient(EPFLConfig()).get_attributes(tequila_key)
        username = user_attributes['username']

        #keep only the first username, not the user@unit or the multiple users
        if username.find(","):
            username = username.split(",")[0]
            if username.find("@"):
                username = username.split("@")[0]

        # Note that this could be accomplished in one try-except clause, but
        # instead we use get_or_create when creating unknown users since it has
        # built-in safeguards for multiple threads.
        if self.create_unknown_user:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user = self.configure_user(user)
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass

        if user:
            self.update_attributes_from_tequila(user, user_attributes)

        return user
    
    def update_attributes_from_tequila(self, user, user_attributes):
        """ Fill the user profile with tequila attributes """
        try:
            profile = user.get_profile()
            profile.sciper = user_attributes.get('uniqueid')
            profile.where = user_attributes.get('where')
            profile.unit = user_attributes.get('allunits')
            profile.group = user_attributes.get('group')
            profile.classe = user_attributes.get('classe')
            profile.statut = user_attributes.get('statut')
            profile.memberof = user_attributes.get('memberof')
            profile.save()
        except Exception:
            pass
        
        ###
        #check for create or update field part
        if user_attributes['firstname']:
            # try a manual truncate if necessary, else allow the truncate warning to be raised
            if len(user_attributes['firstname']) > user._meta.get_field('last_name').max_length and user_attributes['firstname'].find(',') != -1:
                first_name_formatted = user_attributes['firstname'].split(',')[0]
            else:            
                first_name_formatted = user_attributes['firstname']
            
            if user.first_name:
                # need update ?
                if user.first_name != first_name_formatted:
                    user.first_name = first_name_formatted
            else:
                user.first_name = first_name_formatted
        
        if user_attributes['name']:
            if user.last_name:
                if user.last_name != user_attributes['name']:
                    user.last_name = user_attributes['name']
            else:
                user.last_name = user_attributes['name']
        
        if user_attributes['email']:
            if user.email:
                if user.email != user_attributes['email']:
                    user.email = user_attributes['email']
            else:
                user.email = user_attributes['email']
            
        user.save()
        
    def configure_user(self, user):
        """
        Configures a user after creation and returns the updated user.

        By default, returns the user unmodified.
        """
        if self.set_created_user_at_inactive:
            user.is_active = False
            user.save()
        return user