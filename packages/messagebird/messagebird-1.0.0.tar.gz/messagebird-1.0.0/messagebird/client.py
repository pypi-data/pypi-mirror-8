import sys
import requests

try:
  from urllib.parse import urljoin
except ImportError:
  from urlparse import urljoin

from messagebird.base         import Base
from messagebird.balance      import Balance
from messagebird.error        import Error
from messagebird.hlr          import HLR
from messagebird.message      import Message
from messagebird.voicemessage import VoiceMessage

ENDPOINT       = 'https://rest.messagebird.com'
CLIENT_VERSION = '1.0.0'
PYTHON_VERSION = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])

class ErrorException(BaseException):
  def __init__(self, errors):
    self.errors = errors

class Client(object):
  def __init__(self, access_key):
    self.access_key = access_key
    self._supported_status_codes = [200, 201, 204, 401, 404, 405, 422]

  def request(self, path, params={}):
    url = urljoin(ENDPOINT, path)

    headers = {
      'Accept'        : 'application/json',
      'Authorization' : 'AccessKey ' + self.access_key,
      'User-Agent'    : 'MessageBird/ApiClient/%s Python/%s' % (CLIENT_VERSION, PYTHON_VERSION)
    }

    if len(params) == 0:
      response = requests.get(url, verify=True, headers=headers)
    else:
      response = requests.post(url, verify=True, headers=headers, data=params)

    if response.status_code in self._supported_status_codes:
      json_response = response.json()
    else:
      response.raise_for_status()

    if 'errors' in json_response:
      raise(ErrorException([Error().load(e) for e in json_response['errors']]))

    return json_response

  def balance(self):
    """Retrieve your balance."""
    return Balance().load(self.request('balance'))

  def hlr(self, id):
    """Retrieve the information of a specific HLR lookup."""
    return HLR().load(self.request('hlr/' + str(id)))

  def hlr_create(self, msisdn, reference):
    """Perform a new HLR lookup."""
    return HLR().load(self.request('hlr', { 'msisdn' : msisdn, 'reference' : reference }))

  def message(self, id):
    """Retrieve the information of a specific message."""
    return Message().load(self.request('messages/' + str(id)))

  def message_create(self, originator, recipients, body, params={}):
    """Create a new message."""
    if type(recipients) == list:
      recipients = ','.join(recipients)

    params.update({ 'originator' : originator, 'body' : body, 'recipients' : recipients })
    return Message().load(self.request('messages', params))

  def voice_message(self, id):
    "Retrieve the information of a specific voice message."
    return VoiceMessage().load(self.request('voicemessages/' + str(id)))

  def voice_message_create(self, recipients, body, params={}):
    """Create a new voice message."""
    if type(recipients) == list:
      recipients = ','.join(recipients)

    params.update({ 'recipients' : recipients, 'body' : body })
    return VoiceMessage().load(self.request('voicemessages', params))
