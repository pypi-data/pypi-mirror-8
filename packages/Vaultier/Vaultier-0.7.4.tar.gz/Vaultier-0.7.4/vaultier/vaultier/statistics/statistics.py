import requests
import json
from django.conf import settings
from accounts.models import User, Member
from cards.models import Card
from secrets.models import Secret
from vaults.models import Vault
from workspaces.models import Workspace
import pkg_resources
import hashlib


class StatisticsManager(object):
    """
    Collects statistics about count of Vaultier objects and sends them
    to central endpoint.
    """
    STATISTICS_ENDPOINT = 'http://www.vaultier.org/api/ping/'

    @staticmethod
    def send_statistics():

        enabled = settings.VAULTIER.get('allow_anonymous_usage_statistics')
        if not enabled:
            return

        uid = hashlib.sha256(settings.SITE_URL).hexdigest()
        workspace_count = Workspace.objects.all().count()
        vault_count = Vault.objects.all().count()
        card_count = Card.objects.all().count()
        secret_count = Secret.objects.all().count()
        user_count = User.objects.all().count()
        member_count = Member.objects.all().count()
        version = pkg_resources.get_distribution("Vaultier").version

        payload = {
            'uid': uid,
            'workspaces': workspace_count,
            'vaults': vault_count,
            'cards': card_count,
            'secrets': secret_count,
            'users': user_count,
            'members': member_count,
            'version': version
        }

        requests.post(StatisticsManager.STATISTICS_ENDPOINT,
                      data=json.dumps(payload),
                      headers={'content-type': 'application/json'})
