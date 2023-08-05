import json
import re
import requests
import urllib

from helga.plugins import command

_help_text = 'Look up a definition on urbandictionary.com. \
Usage: helga urban[dictionary] TERM'

_api_host = 'http://urbanscraper.herokuapp.com/search/'


@command('urbandictionary', aliases=['urban'], help=_help_text)
def urbandictionary(client, channel, nick, message, cmd, args):
    """
    Fetch a definition from urban dictionary
    """
    num_requested = 0

    if len(args) == 0:
        return u'You need to give me a term to look up.'
    else:
        # the api spec says that it wants terms RFC3986 encoded but it lies
        pattern = r'\[(-?\d+)\]'
        num_passed = re.match(pattern, args[-1], re.M)
        if num_passed:
            # we subtract one here because def #1 is the 0 item in the list
            num_requested = int(num_passed.groups()[0]) - 1
            args.pop(-1)

        term = urllib.quote(''.join(args))
        response = requests.get(_api_host + term)
        error_response = 'No definition found or a problem talking to the api.'
        if response.status_code != 200:
            return error_response
        response_list = json.loads(response.content)
        if not response_list:
            return error_response

        result_list = json.loads(response.content)
        num_requested = min(num_requested, len(result_list) - 1)
        num_requested = max(0, num_requested)
        result = result_list[num_requested].get(
            'definition', error_response)
        return result + ' [{0} of {1}]'.format(
            num_requested + 1, len(result_list))
