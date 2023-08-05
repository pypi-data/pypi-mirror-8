import BaseHTTPServer
import datetime
import errno
import hashlib
import httplib
import json
import logging
import logging.handlers
import os
import urllib2
import random
import shutil
import ssl
import subprocess
import tempfile
import threading
import time
import traceback
import unittest
import slapos.libnetworkcache
import slapos.signature
import sys
from cStringIO import StringIO

logging.basicConfig()


class NCHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def __init__(self, request, address, server):
    self.__server = server
    self.tree = server.tree
    BaseHTTPServer.BaseHTTPRequestHandler.__init__(
      self, request, address, server)

  def handle(self):
    try:
      BaseHTTPServer.BaseHTTPRequestHandler.handle(self)
    except Exception:
      traceback.print_exc()
      raise

  def do_KILL(self):
    raise SystemExit

  def do_GET(self):
    path = os.path.abspath(os.path.join(self.tree, *self.path.split('/')))
    if not (
      ((path == self.tree) or path.startswith(self.tree + os.path.sep))
      and
      os.path.exists(path)
      ):
      self.send_response(404, 'Not Found')
      return
    self.send_response(200)
    out = open(path, 'rb').read()
    self.send_header('Content-Length', len(out))
    self.end_headers()
    self.wfile.write(out)

  def do_PUT(self):
    assert 'shadir' in self.path
    assert self.headers.getheader('content-type') == 'application/json'
    path = os.path.abspath(os.path.join(self.tree, *self.path.split('/')))
    if not os.path.exists(os.path.dirname(path)):
      os.makedirs(os.path.dirname(path))
    data = self.rfile.read(int(self.headers.getheader('content-length')))
    cksum = hashlib.sha512(data).hexdigest()
    if os.path.exists(path):
      with open(path, 'rb') as f:
        json_data_list = json.loads(f.read().strip())
    else:
      json_data_list = []
    json_data_list.append(json.loads(data))
    data = json.dumps(json_data_list)

    open(path, 'wb').write(data)
    self.send_response(201)
    self.send_header('Content-Length', str(len(cksum)))
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(cksum)
    return

  def do_POST(self):
    assert 'shacache' in self.path
    assert self.headers.getheader('content-type') == 'application/octet-stream'
    path = os.path.abspath(os.path.join(self.tree, *self.path.split('/')))
    if not os.path.exists(path):
      os.makedirs(path)
    data = self.rfile.read(int(self.headers.getheader('content-length')))
    cksum = hashlib.sha512(data).hexdigest()
    path = os.path.join(path, cksum)

    # Although real server would accept the request,
    # clients should avoid uploading same content twice.
    assert not os.path.exists(path)
    open(path, 'wb').write(data)
    self.send_response(201)
    self.send_header('Content-Length', str(len(cksum)))
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(cksum)
    return


class NCHandlerPOST200(NCHandler):
  def do_POST(self):
    self.send_response(200)
    return


class NCHandlerReturnWrong(NCHandler):
  def do_POST(self):
    cksum = 'incorrect'
    self.send_response(201)
    self.send_header('Content-Length', str(len(cksum)))
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    self.wfile.write(cksum)
    return


class Server(BaseHTTPServer.HTTPServer):
  def __init__(self, tree, *args):
    BaseHTTPServer.HTTPServer.__init__(self, *args)
    self.tree = os.path.abspath(tree)

  __run = True

  @classmethod
  def run(cls, *args, **kw):
    thread = threading.Thread(target=cls(*args, **kw).serve_forever)
    thread.daemon = True
    thread.start()
    return thread

  def serve_forever(self):
    while self.__run:
      self.handle_request()

  def handle_error(self, *_):
    self.__run = False


class OfflineTest(unittest.TestCase):
  shacache_url = 'http://localhost:1/shacache'
  shadir_url = 'http://localhost:1/shadir'
  host = 'localhost'
  port = 1
  shacache_path = '/shacache'
  shadir_path = '/shadir'

  def test_download_offline(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache_url,
      self.shadir_url)
    self.assertRaises(IOError, nc.download, 'sha512sum')

  def test_upload_offline(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache_url,
      self.shadir_url)
    self.assertRaises(IOError, nc.upload, StringIO())


class OnlineMixin:
  handler = NCHandler
  schema = 'http'

  def setUp(self):
    self.host = "127.0.0.1"
    self.port = 8080
    self.url = '%s://%s:%s/' % (self.schema, self.host, self.port)
    self.shacache = os.environ.get('TEST_SHA_CACHE', self.url + 'shacache')
    self.shadir = os.environ.get('TEST_SHA_DIR', self.url + 'shadir')
    if not 'TEST_SHA_CACHE' in os.environ and not 'TEST_SHA_DIR' in os.environ:
      self.tree = tempfile.mkdtemp()
      self.thread = Server.run(self.tree, (self.host, self.port), self.handler)
    self.test_string = str(random.random())
    self.test_data = StringIO(self.test_string)
    self.test_shasum = hashlib.sha512(self.test_string).hexdigest()
    self.handler = logging.handlers.BufferingHandler(float('inf'))
    slapos.libnetworkcache.logger.addHandler(self.handler)

  def tearDown(self):
    if not 'TEST_SHA_CACHE' in os.environ and not 'TEST_SHA_DIR' in os.environ:
      try:
        httplib.HTTPConnection(self.host, self.port).request('KILL', '/')
      except Exception:
        pass

      if self.thread is not None:
        self.thread.join()
      shutil.rmtree(self.tree)
    slapos.libnetworkcache.logger.removeHandler(self.handler)
    del self.handler

  def assertRaised(self, exc_type):
    self.assertIs(exc_type, self.handler.buffer.pop(0).args[0][0])

  def assertLog(self, msg=None):
    try:
      self.assertTrue(self.handler.buffer.pop(0).message.startswith(msg))
    except IndexError:
      self.assertEqual(msg, None)

  def select(self, nc, key, *args):
    try:
      return nc.download(nc.select(key).next()['sha512'])
    except StopIteration:
      for msg in args:
        self.assertLog(msg)
      self.assertLog()

  key = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDDrOO87nSiDcXOf+xGc4Iqcdjfwd0RTOxEkO9z8mPZVg2bTPwt
/GwtPgmIC4po3bJdsCpJH21ZJwfmUpaQWIApj3odDAbRXQHWhNiw9ZPMHTCmf8Zl
yAJBxy9KI9M/fJ5RA67CJ6UYFbpF7+ZrXdkvG+0hdRX5ub0WyTPxc6kEIwIDAQAB
AoGBAIgUj1jQGKqum1bt3dps8CQmgqWyA9TJQzK3/N8MveXik5niYypz9qNMFoLX
S818CFRhdDbgNUKgAz1pSC5gbdfCDHYQTBrIt+LGpNSpdmQwReu3XoWOPZp4VWnO
uCpAkDVt+88wbxtMbZ5/ExNFs2xTO66Aad1dG12tPWoyAf4pAkEA4tCLPFNxHGPx
tluZXyWwJfVZEwLLzJ9gPkYtWrq843JuKlai2ziroubVLGSxeovBXvsjxBX95khn
U6G9Nz5EzwJBANzal8zebFdFfiN1DAyGQ4QYsmz+NsRXDbHqFVepymUId1jAFAp8
RqNt3Y78XlWOj8z5zMd4kWAR62p6LxJcyG0CQAjCaw4qXszs4zHaucKd7v6YShdc
3UgKw6nEBg5h9deG3NBPxjxXJPHGnmb3gI8uBIrJgikZfFO/ahYlwev3QKsCQGJ0
kHekMGg3cqQb6eMrd63L1L8CFSgyJsjJsfoCl1ezDoFiH40NGfCBaeP0XZmGlFSs
h73k4eoSEwDEt3dYJYECQQCBssN92KuYCOfPkJ+OV1tKdJdAsNwI13kA//A7s7qv
wHQpWKk/PLmpICMBeIiE0xT+CmCfJVOlQrqDdujganZZ
-----END RSA PRIVATE KEY-----
"""

  certificate = """-----BEGIN CERTIFICATE-----
MIICgDCCAekCADANBgkqhkiG9w0BAQsFADCBiDELMAkGA1UEBhMCVUwxETAPBgNV
BAgTCEJlZSBZYXJkMRgwFgYDVQQKEw9CZWUtS2VlcGVyIEx0ZC4xGDAWBgNVBAsT
D0hvbmV5IEhhcnZlc3RlcjEVMBMGA1UEAxMMTWF5YSB0aGUgQmVlMRswGQYJKoZI
hvcNAQkBFgxNYXlhIHRoZSBCZWUwHhcNMTEwODI0MDc1MTU2WhcNMTIwODI0MDc1
MTU2WjCBiDELMAkGA1UEBhMCVUwxETAPBgNVBAgTCEJlZSBZYXJkMRgwFgYDVQQK
Ew9CZWUtS2VlcGVyIEx0ZC4xGDAWBgNVBAsTD0hvbmV5IEhhcnZlc3RlcjEVMBMG
A1UEAxMMTWF5YSB0aGUgQmVlMRswGQYJKoZIhvcNAQkBFgxNYXlhIHRoZSBCZWUw
gZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMOs47zudKINxc5/7EZzgipx2N/B
3RFM7ESQ73PyY9lWDZtM/C38bC0+CYgLimjdsl2wKkkfbVknB+ZSlpBYgCmPeh0M
BtFdAdaE2LD1k8wdMKZ/xmXIAkHHL0oj0z98nlEDrsInpRgVukXv5mtd2S8b7SF1
Ffm5vRbJM/FzqQQjAgMBAAEwDQYJKoZIhvcNAQELBQADgYEAaT4yamJJowDKMSD2
eshUW8pjctg6O3Ncm5XDIKd77sRf7RwPjFh+BR59lfFf9xvOu8WymhtUU7FoPDW3
MYZmKV7A3nFehN9A+REz+WU3I7fE6vQRh9jKeuxnQLRv0TdP9CEdPcYcs/EQpIDb
8du+N7wcN1ZO8veWSafBzcqgCwg=
-----END CERTIFICATE-----
"""

  alternate_certificate = """-----BEGIN CERTIFICATE-----
MIIB4DCCAUkCADANBgkqhkiG9w0BAQsFADA5MQswCQYDVQQGEwJGUjEZMBcGA1UE
CBMQRGVmYXVsdCBQcm92aW5jZTEPMA0GA1UEChMGTmV4ZWRpMB4XDTExMDkxNTA5
MDAwMloXDTEyMDkxNTA5MDAwMlowOTELMAkGA1UEBhMCRlIxGTAXBgNVBAgTEERl
ZmF1bHQgUHJvdmluY2UxDzANBgNVBAoTBk5leGVkaTCBnzANBgkqhkiG9w0BAQEF
AAOBjQAwgYkCgYEApYZv6OstoqNzxG1KI6iE5U4Ts2Xx9lgLeUGAMyfJLyMmRLhw
boKOyJ9Xke4dncoBAyNPokUR6iWOcnPHtMvNOsBFZ2f7VA28em3+E1JRYdeNUEtX
Z0s3HjcouaNAnPfjFTXHYj4um1wOw2cURSPuU5dpzKBbV+/QCb5DLheynisCAwEA
ATANBgkqhkiG9w0BAQsFAAOBgQBCZLbTVdrw3RZlVVMFezSHrhBYKAukTwZrNmJX
mHqi2tN8tNo6FX+wmxUUAf3e8R2Ymbdbn2bfbPpcKQ2fG7PuKGvhwMG3BlF9paEC
q7jdfWO18Zp/BG7tagz0jmmC4y/8akzHsVlruo2+2du2freE8dK746uoMlXlP93g
QUUGLQ==
-----END CERTIFICATE-----
"""

  ca_cert = """-----BEGIN CERTIFICATE-----
MIID3zCCAsegAwIBAgIJAK6xwAnLgupDMA0GCSqGSIb3DQEBBQUAMIGFMQswCQYD
VQQGEwJQTDENMAsGA1UECAwETGFrYTELMAkGA1UEBwwCVWwxEDAOBgNVBAoMB1Bh
c2lla2ExKDAmBgNVBAMMH0F1dG9tYXRpYyBDZXJ0aWZpY2F0ZSBBdXRob3JpdHkx
HjAcBgkqhkiG9w0BCQEWD2x1a2VAbmV4ZWRpLmNvbTAeFw0xMTA4MzAwOTEwNDda
Fw00MTA4MjIwOTEwNDdaMIGFMQswCQYDVQQGEwJQTDENMAsGA1UECAwETGFrYTEL
MAkGA1UEBwwCVWwxEDAOBgNVBAoMB1Bhc2lla2ExKDAmBgNVBAMMH0F1dG9tYXRp
YyBDZXJ0aWZpY2F0ZSBBdXRob3JpdHkxHjAcBgkqhkiG9w0BCQEWD2x1a2VAbmV4
ZWRpLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMc1jUTwrPAC
mLUL8hwTcOpu3UxZFsAiz/XDNdNpwfEN5RzZrNeW4rJpyqCgPpXtnuQRv2Ru3c2w
oOJbL+JvGicpjleHrpU+DKw3njic7GkBYCYL+UdI4+F7a5coj+FDDHYHcY6XiIMf
3to7eJLmHeAAQe5z1MIKV4mUZGrRB494g0x2Z8rdxZkDSi8YhcwHRkMIA1p6wWY6
1ROXYdUROQ22X1mUO03fCOyyJrfuUQd3WXBtA96c9qZ1Kr8Z6qTFrTU2syRSMK1O
acZ2mSvaRYM7OuS97YqI5WBdqjQ1DRAhIsMbp42MAgEb+CxJflr6viibfw5sWqx6
WcQfHcDO8EsCAwEAAaNQME4wHQYDVR0OBBYEFIwXY1hTrkII98JBWU1o4XcLSJJm
MB8GA1UdIwQYMBaAFIwXY1hTrkII98JBWU1o4XcLSJJmMAwGA1UdEwQFMAMBAf8w
DQYJKoZIhvcNAQEFBQADggEBAEO1lmm0DTLQD0fJHYwIG+WJX2k/ThzNEE7s246m
4Hk+2ws78sdCWPkfvQHiUvCFBnfBNBfTSBToPJKaPxHi85I8VrV52/JjoA1La6pH
yr1bU9WAHv/oHRRaZcHiMqLz8/L8UM2M4VXq39BZ695tu5PI8Zu410u/62G7avht
2QjD1Xsfo5yx4LaFnTJNqq0Qn1pEVWK1QWFqntqu0l+y1zIw2R3dyxaYAkcqKO4R
euQB4LKEfrfwEBoBRK7/YXL2hewKyb/2h/5i6QazkwebLSAKOpV6LpShRbEn6O92
Ev5yliJ0c6fLy1PT0ZDevGEMigbUQo/+Bd2vIDzlrEw7mH8=
-----END CERTIFICATE-----
"""

  auth_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDA8zHDYIYDIYsq
okplkfQWac24b67/nTEXANDLjftbBGNj1/fFFK2GuVgcvdtMnqbyD1RMSMoEJa1a
uMldazh3XENTDBxUrdmEoe0Qckh9KScPjQWvxiIjaitpKEZJWZU9lK1v3EZYOweE
Ch50iiV3hIA8pbWphM8C631YxLorBGovGEDBq8q+KHBmZa3U0bByuytxCrCZP34H
NRZQM7rf+webXjqygJ+sVq2miLr5Dr2zxo44enguGsP2VZXzc5xoflQlLRgcl2IM
0u/s7H0p2XlaCBhzgjcTInYqE8I6fKCuZQWRVUkySF1omMmg3bthhGlz66aQZudK
a7HkMj4rAgMBAAECggEAG1ebGqun8fOj6/O5hTEsnKx7mYJCEzjsRu03qVDCaMBz
cSeelc/7UxcatF/3HqFw2OZxNKov7myEZ1G+Pz29b7SkWbViomFMbK4hkO4Q9aOK
RHrgbmsuVURrSGiLpUNLkcFq3mohkckzpHNmo28cJhahsXZuCsqmJyzFw3mFRCkJ
+OGaPzx0llDRkHPVMWxeQsuadDLrT5Kv4u4E7vPWmMBJ9p5Yy/xKUAX8vrtheSjo
eiHM4RW63xedmDQ6G3ofJgAiCLPCyodTtwJJnGY3ZXpCjfX0t0eyGYNkgqOM0eYw
670avZSBABCDCM7ff/w2HzxE9uY2It2VxG7Wr4WtUQKBgQDlvLMf4kE5gAtcpan4
5TJHblm1fNIVP1VMMq1WexeDnY3FHvW5FCCndJAUBW7N+ILDZVtQ+EWEcQF2hASw
6KdxBa/K/F5dLm2UUb4YLUh5ERLN+FPu7Q1jjYQtHVSsS/54YRivjV90PHnrW4G3
xljtp74+TZ/SSp3Rxnk8u8ILmQKBgQDXAemMk0LgxnDhG5PwjY6aoV6WSy4B9rT7
EXrhTDL4QZpdVlTzdGPuSSI74xbjT9B84fD8gLh+1rGVHyDlDOLduxdOuatgs2P8
zaIEBvwX15DVVINves/5gFb5FOd007LsLwfZrTSG9kLL4MR5qzl24d74z3zlB75Q
6xuU/G8SYwKBgHONyntLDouhgBWFrkzm27daJf1HX1QYmwrMoqtRFq643Mo9nFMP
cK1Jz/6CDQ3E5eDqZlf/yNepD5dRKBrjqvUKazWqYrxz0eI8i2UVwdJDaDX5ph4T
Vhyw3b7jdeeEAecCz6vdbBnHIXvkdwa82ZYQPXyRBsZ7iY4uSmTl++BhAoGAC/EX
P6+OL13WNyqI9PtnyD7eOgrC62kAdFFsOcc5rYA3SqfY4Ay+4CU/uYPLaaStN8J0
2BFuLd1Oz7GC6jXlA9u4V68ITb6o9wmUzhR1O/3FFZQ0GKUBmCIAsqTulhaMAYI7
NWPhXv2eiCRbxUY1Ut0IvVkI3s+nSmdEiOncYXECgYEAschHLdYaVl/1tvFUEubC
acabL1CwvSPh/1+xd05w2SUBZguN4q6b5zan2z34E6njRWrXbMpZ8jHroyaCFQha
CkvUOu+kXxjhuolc3LdtVssf2Zupkdwo9u07DR31t6RmJPIi/p461wgtVUI8pCK9
/59DljkBXEter7wmdnitIJg=
-----END PRIVATE KEY-----
"""

  auth_certificate = """-----BEGIN CERTIFICATE-----
MIID2TCCAsGgAwIBAgIBBDANBgkqhkiG9w0BAQUFADCBhTELMAkGA1UEBhMCUEwx
DTALBgNVBAgMBExha2ExCzAJBgNVBAcMAlVsMRAwDgYDVQQKDAdQYXNpZWthMSgw
JgYDVQQDDB9BdXRvbWF0aWMgQ2VydGlmaWNhdGUgQXV0aG9yaXR5MR4wHAYJKoZI
hvcNAQkBFg9sdWtlQG5leGVkaS5jb20wHhcNMTEwODMwMDkzOTExWhcNMjEwODI3
MDkzOTExWjBdMQswCQYDVQQGEwJQTDENMAsGA1UECAwETGFrYTEQMA4GA1UECgwH
UGFzaWVrYTENMAsGA1UEAwwEbWF5YTEeMBwGCSqGSIb3DQEJARYPbHVrZUBuZXhl
ZGkuY29tMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwPMxw2CGAyGL
KqJKZZH0FmnNuG+u/50xFwDQy437WwRjY9f3xRSthrlYHL3bTJ6m8g9UTEjKBCWt
WrjJXWs4d1xDUwwcVK3ZhKHtEHJIfSknD40Fr8YiI2oraShGSVmVPZStb9xGWDsH
hAoedIold4SAPKW1qYTPAut9WMS6KwRqLxhAwavKvihwZmWt1NGwcrsrcQqwmT9+
BzUWUDO63/sHm146soCfrFatpoi6+Q69s8aOOHp4LhrD9lWV83OcaH5UJS0YHJdi
DNLv7Ox9Kdl5WggYc4I3EyJ2KhPCOnygrmUFkVVJMkhdaJjJoN27YYRpc+umkGbn
Smux5DI+KwIDAQABo3sweTAJBgNVHRMEAjAAMCwGCWCGSAGG+EIBDQQfFh1PcGVu
U1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNVHQ4EFgQU8fr/I1bRXGM7e14s
jzNA7Tx/nVswHwYDVR0jBBgwFoAUjBdjWFOuQgj3wkFZTWjhdwtIkmYwDQYJKoZI
hvcNAQEFBQADggEBAJ6q6sx+BeIi/Ia4fbjwCrw0ZahGn24fpoD7g8/eZ9XbmBMx
y4o5UlFS5LW1M0RywV0XksztU8jyQZOB8uhWw1eEdMovGqvTWmer0T0PPo14TJhN
iQh+KE90apiM8ohKJoBZ+v6s9+99YDmeW7UOw0o1wtOdT9oyT3ZbjQ57lCEUljjk
7VevyRXKYweEogzNe0lEpKiZLqiOkVtRhIY/O5eB+RYPomLmd/wWFQJrYpdRzWnj
RWYLHZ9aoSO3icgl8uvxT7WYD8fmAxXjdRd0DQVA3Jv8v8QiV+u5rxP1gcG63Bwd
08ckPaJcFIVx2H1euT4xwVDORmvuX8N3uaZLyZQ=
-----END CERTIFICATE-----
"""


class OnlineTest(OnlineMixin, unittest.TestCase):
  """Online tests against real HTTP server"""
  def test_upload(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    nc.upload(self.test_data)

  def test_upload_shadir(self):
    """Check scenario with shadir used"""
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    urlmd5 = str(random.random())
    nc.upload(self.test_data, 'mykey', urlmd5=urlmd5, file_name='my file')

  def test_upload_shadir_select(self):
    """Check scenario with shadir used"""
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    urlmd5 = str(random.random())
    key = 'somekey' + str(random.random())
    nc.upload(self.test_data, key, urlmd5=urlmd5, file_name='my file')
    result = self.select(nc, key)
    self.assertEqual(result.read(), self.test_string)

  def test_upload_shadir_select_not_exists(self):
    """Check scenario with shadir used"""
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    urlmd5 = str(random.random())
    key = 'somekey' + str(random.random())
    nc.upload(self.test_data, key, urlmd5=urlmd5, file_name='my file')
    with nc:
      nc.select('key_another_key' + str(random.random())).next()
    self.assertRaised(urllib2.HTTPError)

  def test_upload_shadir_no_filename(self):
    """Check scenario with shadir used, but not filename passed"""
    with slapos.libnetworkcache.NetworkcacheClient(self.shacache,
                                                   self.shadir) as nc:
      nc.upload(self.test_data, 'somekey', str(random.random()))
    self.assertLog('file_name and urlmd5 are required for non-generic upload')

  def test_upload_twice_same(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    nc.upload(self.test_data)
    nc.upload(self.test_data)

  def test_download(self):
    # prepare some test data

    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)

    # upload them
    nc.upload(self.test_data)

    # now try to download them
    result = nc.download(self.test_shasum)

    # is it correctly downloaded
    self.assertEqual(result.read(), self.test_string)

  def test_download_not_exists(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    try:
      nc.download(self.test_shasum)
      self.fail("HTTPError not raised")
    except urllib2.HTTPError, error:
      self.assertEqual(error.code, httplib.NOT_FOUND)

  def test_select_signed_content(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    key_file = tempfile.NamedTemporaryFile()
    key_file.write(self.key)
    key_file.flush()
    signed_nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir, key_file.name, [self.certificate])
    signed_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    result = self.select(signed_nc, key)
    self.assertEqual(result.read(), self.test_string)

  def test_select_signed_content_several_certificates(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    key_file = tempfile.NamedTemporaryFile()
    key_file.write(self.key)
    key_file.flush()
    signed_nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir, key_file.name,
      (self.alternate_certificate, self.certificate))
    signed_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    result = self.select(signed_nc, key)
    self.assertEqual(result.read(), self.test_string)

  def test_select_signed_content_multiple(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    key_file = tempfile.NamedTemporaryFile()
    key_file.write(self.key)
    key_file.flush()
    signed_nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir, key_file.name, [self.certificate])
    signed_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    signed_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    result = self.select(signed_nc, key)
    self.assertEqual(result.read(), self.test_string)

  def test_select_no_entries(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir)
    self.assertEqual(self.test_shasum, nc.upload(self.test_data,
        key, urlmd5=urlmd5, file_name=file_name))
    f = os.path.join(self.tree, 'shadir', key)
    # now remove the entry from shacache
    open(f, 'w').write(json.dumps([]))
    self.assertEqual(self.select(nc, key), None)

  def test_select_no_json_response(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir)
    self.assertEqual(self.test_shasum, nc.upload(self.test_data,
        key, urlmd5=urlmd5, file_name=file_name))
    with open(os.path.join(self.tree, 'shadir', key), 'w') as f:
      # now remove the entry from shacache
      f.write('This is not a json.')
    with nc:
      nc.select(key).next()
    self.assertLog('Failed to parse json response')

  def test_select_json_no_in_json_response(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir)
    self.assertEqual(self.test_shasum, nc.upload(self.test_data,
        key, urlmd5=urlmd5, file_name=file_name))
    with open(os.path.join(self.tree, 'shadir', key), 'w') as f:
      # now remove the entry from shacache
      f.write(json.dumps([['This is not a json.', 'signature']]))
    self.select(nc, key, 'Failed to parse json-in-json response')

  def test_select_json_in_json_no_dict(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir)
    self.assertEqual(self.test_shasum, nc.upload(self.test_data,
        key, urlmd5=urlmd5, file_name=file_name))
    with open(os.path.join(self.tree, 'shadir', key), 'w') as f:
      # now remove the entry from shacache
      f.write(json.dumps([[json.dumps('This is a string'), 'signature']]))
    self.select(nc, key, 'Bad or missing sha512 in directory response')

  def test_select_signed_content_server_hacked(self):
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    key_file = tempfile.NamedTemporaryFile()
    key_file.write(self.key)
    key_file.flush()
    signed_nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir, key_file.name, [self.certificate])

    signed_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    # Hacker entered the server...
    f = os.path.join(self.tree, 'shadir', key)
    original_data = open(f).read()
    original_json = json.loads(original_data)
    hacked_entry_json = json.loads(original_json[0][0])
    # ...he modifies something...
    hacked_entry_json['file'] = 'hacked'
    hacked_json = original_json[:]
    # ...and stores...
    hacked_json[0][0] = json.dumps(hacked_entry_json)
    # ...but as he has no access to key, no way to sign data..
    # hacked_json[0][1] is still a good key
    open(f, 'w').write(json.dumps(hacked_json))
    self.assertEqual(self.select(signed_nc, key), None)

  def test_DirectoryNotFound_non_trustable_entry(self):
    key_file = tempfile.NamedTemporaryFile()
    key_file.write(self.key)
    key_file.flush()

    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    key = 'somekey' + str(random.random())
    urlmd5 = str(random.random())
    file_name = 'my file'
    nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    signed_nc = slapos.libnetworkcache.NetworkcacheClient(
      self.shacache, self.shadir, signature_certificate_list=[
          self.certificate])
    # when no signature is used, all works ok
    selected = self.select(nc, key).read()
    self.assertEqual(selected, self.test_string)
    # but when signature is used, networkcache will complain
    self.assertEqual(self.select(signed_nc, key), None)

    # of course if proper key will be used to sign the content uploaded
    # into shacache all will work
    upload_nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache,
      self.shadir, signature_private_key_file=key_file.name)
    upload_nc.upload(self.test_data, key, urlmd5=urlmd5, file_name=file_name)
    selected = self.select(signed_nc, key).read()
    self.assertEqual(selected, self.test_string)


@unittest.skipUnless(os.environ.get('TEST_SHA_CACHE', '') != '',
    "Requires standalone test server")
class OnlineTestSSLServer(OnlineMixin, unittest.TestCase):
  schema = 'https'

  def setUp(self):
    self.keyfile = tempfile.NamedTemporaryFile()
    self.keyfile.write(self.auth_key)
    self.keyfile.flush()
    self.certfile = tempfile.NamedTemporaryFile()
    self.certfile.write(self.auth_certificate)
    self.certfile.flush()
    OnlineMixin.setUp(self)

  def test_upload_to_ssl_auth_no_auth(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    try:
      nc.upload(self.test_data)
    except ssl.SSLError, e:
      self.assertTrue('alert handshake failure' in str(e))

  def test_upload_to_ssl_auth(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir,
        shacache_key_file=self.keyfile.name,
        shacache_cert_file=self.certfile.name)
    nc.upload(self.test_data)

  def test_upload_with_key_with_ssl_auth_no_dir_auth(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir,
        shacache_key_file=self.keyfile.name,
        shacache_cert_file=self.certfile.name)
    try:
      nc.upload(self.test_data, key=str(random.random()),
          file_name=str(random.random()), urlmd5=str(random.random()))
    except ssl.SSLError, e:
      self.assertTrue('alert handshake failure' in str(e))

  def test_upload_with_key_with_ssl_auth(self):
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir,
        shacache_key_file=self.keyfile.name,
        shacache_cert_file=self.certfile.name,
        shadir_key_file=self.keyfile.name,
        shadir_cert_file=self.certfile.name)
    nc.upload(self.test_data, key=str(random.random()),
          file_name=str(random.random()), urlmd5=str(random.random()))


class OnlineTestPOST200(OnlineMixin, unittest.TestCase):
  handler = NCHandlerPOST200

  def test_upload_wrong_return_code(self):
    """Check reaction on HTTP return code different then 201"""
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    self.assertRaises(slapos.libnetworkcache.NetworkcacheException, nc.upload,
      self.test_data)


class OnlineTestWrongChecksum(OnlineMixin, unittest.TestCase):
  handler = NCHandlerReturnWrong

  def test_upload_wrong_return_sha(self):
    """Check reaction in case of wrong sha returned"""
    nc = slapos.libnetworkcache.NetworkcacheClient(self.shacache, self.shadir)
    self.assertRaises(slapos.libnetworkcache.NetworkcacheException, nc.upload,
      self.test_data)


class GenerateSignatureScriptTest(unittest.TestCase):
  ''' Class which must test the signature.py script. '''
  def setUp(self):
    self.key = os.path.join(tempfile.gettempdir(), tempfile.gettempprefix() +
      str(random.random()))
    self.certificate = os.path.join(tempfile.gettempdir(), tempfile.gettempprefix()
      + str(random.random()))
    self.common_name = str(random.random())

  def tearDown(self):
    for f in self.key, self.certificate:
      if os.path.lexists(f):
        os.unlink(f)

  def test_generate_certificate(self):
    slapos.signature.generateCertificate(self.certificate, self.key,
      self.common_name)
    today = datetime.date.today()
    result = subprocess.check_output(['openssl', 'x509', '-noout', '-subject',
      '-in', self.certificate])
    self.assertEqual('subject= /CN=%s' % self.common_name, result.strip())
    result = subprocess.check_output(['openssl', 'x509', '-noout', '-enddate',
      '-in', self.certificate])
    self.assertTrue(' %s ' % (today.year + 100) in result)

  def test_generate_key_exists(self):
    with tempfile.NamedTemporaryFile() as key:
      self.assertRaises(ValueError, slapos.signature.generateCertificate,
        self.certificate, key.name, self.common_name)

  def test_generate_cert_exists(self):
    with tempfile.NamedTemporaryFile() as cert:
      self.assertRaises(ValueError, slapos.signature.generateCertificate,
        cert.name, self.key, self.common_name)
