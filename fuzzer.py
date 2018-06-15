import http.cookiejar
import json
import time
import urllib.parse
import urllib.request

import bs4


def init_cookies():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    return cj, opener


def unauthed_session():
    cj, opener = init_cookies()
    return opener, ''


def auth(endpoint, email, password, type='user'):
    print('Authing on', endpoint, 'with', email)
    (cj, opener) = init_cookies()
    with opener.open(endpoint) as resp:
        response = resp.read().decode('utf-8')
        soup = bs4.BeautifulSoup(response, 'html.parser')
        csrf_token = soup.select('meta[name=csrf-token]')[0].attrs.get('content')

    print("CSRF token", csrf_token)

    login_form = urllib.parse.urlencode({
        'authenticity_token': csrf_token,
        (type + '[email]'): email,
        (type + '[password]'): password,
        (type + '[remember_me]'): 0,
        'commit': 'Login'
    })
    login_form = login_form.encode('ascii')

    req = urllib.request.Request(endpoint, login_form)

    with opener.open(req, login_form) as f:
        print("Cookies", cj._cookies['localhost.local']['/'])

    return opener, csrf_token


def fuzz(session, route, html_path=None, json_payload=False, custom_headers=None, data=None, method=None):
    """
    Issues requests to an endpoint, trying authed, unauthed, and csrf-token-less requests

    :param session: the pair returned by either auth() or unauthed_session()
    :param route: the route to test
    :param html_path: whet
    :param json_payload: if true, will post data as json instead of form data
    :param custom_headers: a list of any additional headers to add to the request
    :param data: if present, makes the request a POST with this data.  Otherwise the request will be a GET.
    :param method: an optional override if you need a request method other than GET or POST.
    """
    print("Posting to", route, "with", data)
    request_to(session, route, html_path, json_payload, custom_headers, data, method, use_token=True)
    request_to(session, route, html_path, json_payload, custom_headers, data, method, use_token=False)
    print("  Unauthed:")
    request_to(unauthed_session(), route, html_path, json_payload, custom_headers, data, method, use_token=False)


def request_to(session, route, html_path=None, json_payload=False, custom_headers=None, data=None, method=None,
               use_token=False):
    opener, csrf_token = session
    print('\tWith token:' if use_token else '\tWithout token:')
    if json_payload:
        data = data and json.dumps(data).encode('ascii')
    else:
        data = data and urllib.parse.urlencode(data).encode('ascii')
    req = urllib.request.Request('http://localhost:3000' + route, data, method=method)
    if use_token:
        req.add_header('X-CSRF-Token', csrf_token)
    else:
        req.add_header('X-CSRF-Token',
                       'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO000')
    if custom_headers is None:
        if json_payload:
            req.add_header('Content-Type', 'application/json')
    else:
        for name, value in custom_headers:
            req.add_header(name, value)

    start = time.time()
    try:
        with opener.open(req) as resp:
            end = time.time()
            print('\t', resp.status)
            response = resp.read().decode('utf-8')
            if html_path:
                soup = bs4.BeautifulSoup(response, 'html.parser')
                print('\t Element found in response: ', soup.select(html_path)[0].contents)
            else:
                print('\t Response: ', response)
    except Exception as e:
        end = time.time()
        print('\t', e)
    return end - start


user_session = auth('http://localhost:3000/users/sign_in', 'tester@example.com', 'some-dev-account-password')
fuzz(user_session, '/some-user-authenticated-post-endpoint', data={'foo': 'bar'})
