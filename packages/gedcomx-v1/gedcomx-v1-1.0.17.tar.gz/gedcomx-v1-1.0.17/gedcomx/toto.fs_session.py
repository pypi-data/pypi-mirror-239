# global imports
import sys
import time

import requests

STATO_INIT = 0
STATO_KONEKTITA = 1
STATO_PASVORTA_ERARO = -1
STATO_ERARO = -2

vorteco=1

#from objbrowser import browse ;browse(locals())
#import pdb; pdb.set_trace()

class FsSession:
    """Create a FamilySearch session
    :param username and password: valid FamilySearch credentials
    :param verbose: True to active verbose mode
    :param logfile: a file object or similar
    :param timeout: time before retry a request
    """

    def __init__(self, username, password, verbose=False, logfile=False, timeout=60, lingvo=None):
        self.username = username
        self.password = password
        self.verbose = verbose
        self.logfile = logfile
        self.timeout = timeout
        self.fid = self.display_name = None
        self.counter = 0
        self.lingvo = lingvo
        self.stato = STATO_INIT
        self.session = requests.session()
        self.logged = self.login()

    def write_log(self, text):
        """write text in the log file"""
        log = "[%s]: %s\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), text)
        if self.verbose or vorteco>0:
            sys.stderr.write(log)
        if self.logfile:
            self.logfile.write(log)

    def login(self):
        """retrieve FamilySearch session ID
        (https://www.familysearch.org/developers/docs/guides/oauth2)
        """
        nbtry = 1
        while True:
            if nbtry > 1 :
              self.stato = STATO_ERARO
              print("too many errors")
              return False

            try:
                nbtry = nbtry + 1
                # étape 1 : on appelle login, pour récupérer client_id et redirect_uri
                url = "https://www.familysearch.org/auth/familysearch/login"
                headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
                #headers ["Accept-Language"] = self.lingvo
                if vorteco >0 :
                  print("*FS login 1 : url = "+url)
                r = self.session.get(url, params={"ldsauth": False}, allow_redirects=False, headers=headers)
                if vorteco >0 :
                  print("+FS login 1 : r.next.url = "+r.next.url)
                import urllib
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(r.next.url).query)
                if qs.get('client_id') :
                  self.client_id = qs.get('client_id')[0]
                #self.client_id='MBVS-G7J8-7TSY-SPG3-G8ZT-7Q9N-MXRS-L8DK'
                if qs.get('client_secret') :
                  self.client_secret = qs.get('client_secret')
                if qs.get('redirect_uri') :
                  self.redirect_uri = qs['redirect_uri'][0]
                if vorteco >0 :
                  print("+FS login 1 : redirect_uri = "+self.redirect_uri)
                  print("*FS login 2 : r.next.url = "+str(r.next.url))
                # étape 2 : on appelle authorization, pour récupérer params
                r = self.session.send(r.next)
                if vorteco >0 :
                  print("+FS login 2 ")
                idx = r.text.index('name="params" value="')
                span = r.text[idx + 21 :].index('"')
                params = r.text[idx + 21 : idx + 21 + span]
                if vorteco >0 :
                  print("+FS login 2 : params = "+params)
                # étape 3 : on appelle authorization avec params, username et password
                #          , on récupère le code

                url = "https://ident.familysearch.org/cis-web/oauth2/v3/authorization"
                if vorteco >0 :
                  print("*FS login 3 : url= "+url)
                r = self.session.post(
                    url,
                    data={
                        "params": params,
                        "userName": self.username,
                        "password": self.password,
                    },
                    timeout=self.timeout,
                    allow_redirects=False,headers=headers,
                )
                if vorteco >0 :
                  print("+FS login 3: next.url = "+r.next.url)
                  print("+FS login 3: headers = "+str(r.headers))
                  if r.text :
                    print("+FS login 3: next.url = "+r.text)

                if "The username or password was incorrect" in r.text:
                    self.write_log("The username or password was incorrect")
                    self.stato = STATO_PASVORTA_ERARO
                    return False

                if "Invalid Oauth2 Request" in r.text:
                    self.write_log("Invalid Oauth2 Request")
                    time.sleep(self.timeout)
                    continue

                if vorteco >0 :
                  print("+FS login 3: r.next.url = "+r.next.url)
                # get the authorization code from redirect url :
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(r.next.url).query)
                if qs.get('code') :
                  self.code = qs['code'][0]
                  if vorteco >0 :
                    print("+FS login 3: code = "+self.code)
                else :
                  print("FS login : code ne trovita")
                  print("   headers = "+r.headers)
                  continue
                self.fssessionid = r.next._cookies["familysearch-sessionid"]
                if vorteco >0 :
                  print("+FS login 3: sessionid = "+self.fssessionid)
                # étape 4 : on valide la session
                url = r.headers["Location"]
                self.write_log("Downloading: " + url)
                r = requests.get(url, allow_redirects=False, headers=headers)
                self.fssessionid = r.cookies["fssessionid"]
                if vorteco >0 :
                  print("+FS login 3: sessionid = "+self.fssessionid)
                self.stato = STATO_KONEKTITA
#                # étape 4 : on demande un token
#                url = 'https://ident.familysearch.org/cis-web/oauth2/v3/token'
#                data = {
#                       "code": self.code,
#                       "client_id": self.client_id,
#                       "grant_type": 'password',
#                        "username": self.username,
#                        "password": self.password,
#                      }
#                if vorteco >0 :
#                  print("*FS login 4: headers = "+str(headers))
#                  print("*FS login 4: data = "+str(data))
#                  print("*FS login 4: url = "+str(url))
#                # if hasattr(self,'client_secret') :
#                r = self.session.post(
#                    url,
#                    timeout=self.timeout,
#                    headers=headers,
#                    data=data,
#                    allow_redirects=False
#                )
#                if vorteco >0 :
#                  print("+FS login 4: r.text = "+r.text)
#                json = r.json()
#                if json and json.get('access_token') :
#                  self.access_token = r.json()['access_token']
#                  if vorteco >0 :
#                    print("+FS login 4: access_token = "+self.access_token)
#                else :
#                  if vorteco >0 :
#                    print("+FS login 4: pas d'access_token ")
            except requests.exceptions.ReadTimeout:
                self.write_log("Read timed out")
                continue
            except requests.exceptions.ConnectionError:
                self.write_log("Connection aborted")
                time.sleep(self.timeout)
                continue
            except requests.exceptions.HTTPError:
                self.write_log("HTTPError")
                time.sleep(self.timeout)
                continue
            except KeyError:
                self.write_log("KeyError")
                print(r.content)
                time.sleep(self.timeout)
                continue
            except ValueError:
                self.write_log("ValueError")
                time.sleep(self.timeout)
                continue

            self.stato = STATO_KONEKTITA
            url = "/platform/users/current"
            r = self.session.get(
                    "https://www.familysearch.org" + url,
                    timeout=self.timeout,
                    headers=headers,
                    allow_redirects=False
                )
            try:
              data=r.json()
              if data:
                self.fid = data["users"][0]["personId"]
                if not self.lingvo :
                  self.lingvo = data["users"][0]["preferredLanguage"]
                self.display_name = data["users"][0]["displayName"]
                if vorteco >0 :
                  print("+FS login 5: display_name = "+self.display_name)
            except Exception as e:
              self.write_log("WARNING: corrupted file from %s, error: %s" % (url, e))
              print(r.content)
            return True

    def post_url(self, url, datumoj, headers=None):
        if headers is None:
            headers = {"Accept": "application/x-gedcomx-v1+json","Content-Type": "application/x-gedcomx-v1+json"}
        headers.update( {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        cookies = None
        if hasattr(self,'access_token') :
          headers ["Authorization"] = 'Bearer '+self.access_token
        else :
          cookies = {"fssessionid": self.fssessionid}
        nbtry = 1
        while True:
            try:
                if nbtry > 3 :
                  self.stato = STATO_ERARO
                  return None
                nbtry = nbtry + 1
                self.write_log("post_url, Downloading :" + url)
                r = self.session.post(
                    "https://api.familysearch.org" + url,
                    timeout=self.timeout,
                    headers=headers,
                    data=datumoj,
                    cookies=cookies,
                    allow_redirects=False
                )
            except requests.exceptions.ReadTimeout:
                self.write_log("Read timed out")
                continue
            except requests.exceptions.ConnectionError:
                self.write_log("Connection aborted")
                time.sleep(self.timeout)
                continue
            self.write_log("Status code: %s" % r.status_code)
            if vorteco >0 :
              print("Status code: %s" % r.status_code)
            if r.status_code == 204:
                self.write_log("headers="+str(r.headers))
                return r
            if r.status_code == 401:
                self.login()
                continue
            if r.status_code in {400, 404, 405, 406, 410, 500}:
                self.write_log("WARNING: " + url)
                self.write_log(r)
                return r
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                self.write_log("HTTPError")
                if r.status_code == 403:
                    if (
                        "message" in r.json()["errors"][0]
                        and r.json()["errors"][0]["message"]
                        == "Unable to get ordinances."
                    ):
                        self.write_log(
                            "Unable to get ordinances. "
                            "Try with an LDS account or without option -c."
                        )
                        return "error"
                    self.write_log(
                        "WARNING: code 403 from %s %s"
                        % (url, r.json()["errors"][0]["message"] or "")
                    )
                    return r
                time.sleep(self.timeout)
                continue
            try:
                return r
            except Exception as e:
                self.write_log("WARNING: corrupted file from %s, error: %s" % (url, e))
                return None

    def head_url(self, url, headers=None):
        self.counter += 1
        if headers is None:
            headers = {"Accept": "application/x-gedcomx-v1+json"}
        if "Accept-Language" not in headers and self.lingvo :
            headers ["Accept-Language"] = self.lingvo
        headers.update( {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        cookies = None
        if hasattr(self,'access_token') :
          headers ["Authorization"] = 'Bearer '+self.access_token
        else :
          cookies = {"fssessionid": self.fssessionid}
        nbtry = 1
        while True:
            try:
                if nbtry > 3 :
                  self.stato = STATO_ERARO
                  return None
                nbtry = nbtry + 1
                self.write_log("head_url, Downloading :" + url)
                r = self.session.head(
                    "https://www.familysearch.org" + url,
                    timeout=self.timeout,
                    headers=headers,
                    cookies=cookies,
                )
                if vorteco >0 :
                  print("Status code: %s" % r.status_code)
            except requests.exceptions.ReadTimeout:
                self.write_log("Read timed out")
                continue
            except requests.exceptions.ConnectionError:
                self.write_log("Connection aborted")
                time.sleep(self.timeout)
                continue
            if r.status_code == 401:
                self.login()
                continue
            return r

    def get_url(self, url, headers=None):
        self.counter += 1
        if headers is None:
            headers = {"Accept": "application/x-gedcomx-v1+json"}
        if "Accept-Language" not in headers and self.lingvo:
            headers ["Accept-Language"] = self.lingvo
        headers.update( {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
        cookies = None
        if hasattr(self,'access_token') :
          headers ["Authorization"] = 'Bearer '+self.access_token
        else :
          cookies = {"fssessionid": self.fssessionid}
        nbtry = 0
        import pdb; pdb.set_trace()
        while True:
            nbtry = nbtry + 1
            if nbtry > 3 :
              self.stato = STATO_ERARO
              return None
            try:
                self.write_log("get_url, Downloading :" + url)
                r = self.session.get(
                    "https://www.familysearch.org" + url,
                    timeout=self.timeout,
                    headers=headers,
                    cookies=cookies,
                    allow_redirects=False
                )
                if vorteco >0 :
                  print("Status code: %s" % r.status_code)
            except requests.exceptions.ReadTimeout:
                self.write_log("Read timed out")
                continue
            except requests.exceptions.ConnectionError:
                self.write_log("Connection aborted")
                time.sleep(self.timeout)
                continue
            if r.status_code == 204 or r.status_code == 301:
                print("headers="+str(r.headers))
                return r
            if r.status_code == 401:
                return r
                self.login()
                continue
            if r.status_code in {400, 404, 405, 406, 410, 500}:
                self.write_log("WARNING: " + url)
                self.write_log(r.text)
                return None
            #else:
            #    self.write_log("WARNING: " + url)
            #    self.write_log(r.json())
            #    return None
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                self.write_log("HTTPError")
                if r.status_code == 403:
                    if (
                        "message" in r.json()["errors"][0]
                        and r.json()["errors"][0]["message"]
                        == "Unable to get ordinances."
                    ):
                        self.write_log(
                            "Unable to get ordinances. "
                            "Try with an LDS account or without option -c."
                        )
                        return "error"
                    self.write_log(
                        "WARNING: code 403 from %s %s"
                        % (url, r.json()["errors"][0]["message"] or "")
                    )
                    return None
                time.sleep(self.timeout)
                continue
            return r

    def get_jsonurl(self, url, headers=None):
        """retrieve JSON structure from a FamilySearch URL"""
        r = self.get_url(url,headers)
        if r:
          try:
            return r.json()
          except Exception as e:
            self.write_log("WARNING: corrupted file from %s, error: %s" % (url, e))
            print(r.content)
            return None

    def set_current(self):
        """retrieve FamilySearch current user ID, name and language"""
        url = "/platform/users/current"
        data = self.get_jsonurl(url)
        if data:
            self.fid = data["users"][0]["personId"]
            if not self.lingvo :
              self.lingvo = data["users"][0]["preferredLanguage"]
            self.display_name = data["users"][0]["displayName"]

    def _(self, string):
        """translate a string into user's language
        TODO replace translation file for gettext format
        """
        if string in translations and self.lingvo in translations[string]:
            return translations[string][self.lingvo]
        return string
