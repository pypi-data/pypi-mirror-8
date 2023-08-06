# -*- coding: utf-8 -*-

#from compat import unicode, bytes

# TODO: round-tripping tests

import pytest

from hematite.url import URL, _URL_RE, parse_authority


TEST_URLS = [
    '*',  # e.g., OPTIONS *
    'http://googlewebsite.com/e-shops.aspx',
    'http://example.com:8080/search?q=123&business=Nothing%20Special',
    'http://hatnote.com:9000?arg=1&arg=2&arg=3',
    'https://xn--bcher-kva.ch',
    'http://xn--ggbla1c4e.xn--ngbc5azd/',
    'http://tools.ietf.org/html/rfc3986#section-3.4',
    'http://wiki:pedia@hatnote.com',
    'ftp://ftp.rfc-editor.org/in-notes/tar/RFCs0001-0500.tar.gz',
    'http://[1080:0:0:0:8:800:200C:417A]/index.html',
    'ssh://192.0.2.16:22/',
    'https://[::101.45.75.219]:80/?hi=bye',
    'ldap://[::192.9.5.5]/dc=example,dc=com??sub?(sn=Jensen)',
    'mailto:me@example.com?to=me@example.com&body=hi%20http://wikipedia.org',
    'news:alt.rec.motorcycle',
    'tel:+1-800-867-5309',
    'urn:oasis:member:A00024:x',
    'magnet:?xt=urn:btih:1a42b9e04e122b97a5254e3df77ab3c4b7da725f&dn=Puppy%20Linux%20precise-5.7.1.iso&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.publicbt.com:80&tr=udp://tracker.istole.it:6969&tr=udp://tracker.ccc.de:80&tr=udp://open.demonii.com:1337']


UNICODE_URLS = [
    # 'http://مثال.آزمایشی'
    ('\xd9\x85\xd8\xab\xd8\xa7\xd9\x84'
     '.\xd8\xa2\xd8\xb2\xd9\x85\xd8\xa7'
     '\xdb\x8c\xd8\xb4\xdb\x8c')]


@pytest.fixture(scope="module", params=TEST_URLS)
def test_url(request):
    param = request.param
    #request.addfinalizer(lambda: None)
    return param


@pytest.fixture(scope="module", params=TEST_URLS)
def test_authority(request):
    match = _URL_RE.match(request.param)
    return match.groupdict()['authority']


def test_regex(test_url):
    match = _URL_RE.match(test_url)
    assert match.groupdict()


def test_parse_authorities(test_authority):
    if not test_authority:
        return True
    else:
        _, _, family, host, port = parse_authority(test_authority)
        assert bool(host)  # TODO


def test_basic():
    u1 = URL('http://googlewebsite.com/e-shops.aspx')
    assert isinstance(u1.to_text(), unicode)
    assert u1.host == 'googlewebsite.com'


def test_idna():
    u1 = URL('http://bücher.ch')
    assert u1.host == u'bücher.ch'
    assert u1.to_text(display=False) == 'http://xn--bcher-kva.ch'
    assert u1.to_text(display=True) == u'http://bücher.ch'

    u2 = URL('https://xn--bcher-kva.ch')
    assert u2.host == u'bücher.ch'
    assert u2.to_text(display=False) == 'https://xn--bcher-kva.ch'
    assert u2.to_text(display=True) == u'https://bücher.ch'


def test_urlparse_equiv(test_url):
    from urlparse import urlparse, urlunparse
    url_obj = URL(test_url)
    assert urlunparse(urlparse(test_url)) == urlunparse(url_obj)


def test_query_params(test_url):
    url_obj = URL(test_url)
    if not url_obj.args:
        return True
    assert test_url.endswith(url_obj.get_query_string())


def test_iri_query():
    url = URL(u'http://minerals.rocks.ore/?mountain=\N{MOUNTAIN}')
    assert url.args['mountain'] == u'\N{MOUNTAIN}'
    assert url.args.to_bytes().endswith('%E2%9B%B0')
    assert url.args.to_text().endswith(u'\N{MOUNTAIN}')

    # fails because urlparse assumes query strings are encoded with latin1
    url2 = URL(url.to_bytes())
    assert url2.args['mountain'] == u'\N{MOUNTAIN}'


def test_iri_path():
    url = URL(u'http://minerals.rocks.ore/mountain/\N{MOUNTAIN}/')
    assert url.path == u'/mountain/\N{MOUNTAIN}/'
    assert url.to_bytes().endswith('%E2%9B%B0/')


def test_urlparse_obj_input():
    with pytest.raises(TypeError):
        URL(object())


def test_invalid_url():
    pass
    #with pytest.raises(ValueError):
    #    URL('this is pretty much the furthest thing from a url')  # TODO
    #    URL('???????????????????')  # TODOx2


def test_invalid_port():
    with pytest.raises(ValueError):
        URL('http://reader.googlewebsite.com:neverforget')


def test_invalid_ipv6():
    invalid_ipv6_ips = ['2001::0234:C1ab::A0:aabc:003F',
                        '2001::1::3F']
    for ip in invalid_ipv6_ips:
        with pytest.raises(ValueError):
            URL('http://[' + ip + ']')


def test_is_absolute():
    url = URL('/hi/hello?yes=no')
    assert not url.is_absolute
    url = URL('http://googlewebsite.biz/hi')
    assert url.is_absolute


def _url2parseresult(url_str):
    # TODO: is this necessary anymores?
    from urlparse import ParseResult
    pd = parse_url(url_str)
    parsed = ParseResult(pd['scheme'], pd['authority'], pd['path'],
                         '', pd['query'], pd['fragment'])
    parsed = parsed._replace(netloc=parsed.netloc.decode('idna'))
    return parsed
