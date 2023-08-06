import logging
from flask import current_app as app
from apps.auth.errors import NotFoundAuthError
import superdesk
from .ldap import ADAuth
from superdesk.utc import utcnow


logger = logging.getLogger(__name__)


class ImportUserProfileFromADCommand(superdesk.Command):
    """
    Responsible for importing a user profile from Active Directory (AD) to Mongo.
    This command runs on assumption that the user executing this command and
    the user whose profile need to be imported need not to be the same. Uses ad_username and ad_password to bind to AD
    and then searches for a user identified by username_to_import and if found imports into Mongo.
    """

    option_list = (
        superdesk.Option('--ad_username', '-adu', dest='ad_username', required=True),
        superdesk.Option('--ad_password', '-adp', dest='ad_password', required=True),
        superdesk.Option('--username_to_import', '-u', dest='username', required=True),
        superdesk.Option('--admin', '-a', dest='admin', required=False),
    )

    def run(self, ad_username, ad_password, username, admin='false'):
        """
        Imports or Updates a User Profile from AD to Mongo.
        :param ad_username: Active Directory Username
        :param ad_password: Password of Active Directory Username
        :param username: Username as in Active Directory whose profile needs to be imported to Superdesk.
        :return: User Profile.
        """

        # force type conversion to boolean
        user_type = 'administrator' if admin.lower() == 'true' else 'user'

        # Authenticate and fetch profile from AD
        settings = app.settings
        ad_auth = ADAuth(settings['LDAP_SERVER'], settings['LDAP_SERVER_PORT'], settings['LDAP_BASE_FILTER'],
                         settings['LDAP_USER_FILTER'], settings['LDAP_USER_ATTRIBUTES'], settings['LDAP_FQDN'])

        user_data = ad_auth.authenticate_and_fetch_profile(ad_username, ad_password, username)

        if len(user_data) == 0:
            raise NotFoundAuthError()

        # Check if User Profile already exists in Mongo
        user = superdesk.get_resource_service('users').find_one(username=username, req=None)
        user_data[app.config['LAST_UPDATED']] = utcnow()

        if user:
            superdesk.get_resource_service('users').patch(user.get('_id'), user_data)
            return user_data
        else:
            user_data[app.config['DATE_CREATED']] = user_data[app.config['LAST_UPDATED']]
            user_data['username'] = username
            user_data['user_type'] = user_type
            superdesk.get_resource_service('users').post([user_data])
            return user_data

superdesk.command('users:copyfromad', ImportUserProfileFromADCommand())
