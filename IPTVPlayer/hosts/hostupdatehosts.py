# -*- coding: utf-8 -*-
###################################################
# 2019-04-14 by Alec - updatehosts HU host telepítő
###################################################
HOST_VERSION = "1.1"
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _, SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, byteify, rm, rmtree, GetTmpDir, MergeDicts, GetConfigDir, Which
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
import urlparse
import re
import urllib
import random
import os
import datetime
import time
import zlib
import cookielib
import base64
import traceback
import subprocess
import codecs
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
from enigma import quitMainloop
from copy import deepcopy
try:    import json
except Exception: import simplejson as json
from Components.config import config, ConfigText, getConfigListEntry
from datetime import datetime
from hashlib import sha1
###################################################

###################################################
# E2 GUI COMMPONENTS 
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvmultipleinputbox import IPTVMultipleInputBox
from Screens.MessageBox import MessageBox
###################################################

def gettytul():
    return 'updatehosts HU'

class updatehosts(CBaseHostClass):
 
    def __init__(self):
        CBaseHostClass.__init__(self, {'history':'updatehosts', 'cookie':'updatehosts.cookie'})
        self.USER_AGENT = 'User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.HEADER = self.cm.getDefaultHeader()
        self.TEMP = zlib.decompress(base64.b64decode('eJzTL8ktAAADZgGB'))
        self.DEFAULT_ICON_URL = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1S8tSEksSc3ILy4pjs/JT8/XyypIBwDb2BNK'))
        self.IH = resolveFilename(SCOPE_PLUGINS, zlib.decompress(base64.b64decode('eJxzrShJzSvOzM8r1vcMCAkLyEmsTC0CAFlVCBA=')))
        self.HS = zlib.decompress(base64.b64decode('eJzTz8gvLikGAAeYAmE='))
        self.ILS = zlib.decompress(base64.b64decode('eJzTz0zOzyvWz8lPzy8GAByVBJ8='))
        self.IPSR = zlib.decompress(base64.b64decode('eJzTz0zOzyvWD8hJrEwtCk7NSU0uyS8CAFYtCCk='))
        self.ICM = zlib.decompress(base64.b64decode('eJzTzywoKSstSEksSdVPLi0uyc8FAENzB0A='))
        self.HRG = GetConfigDir(zlib.decompress(base64.b64decode('eJzLLCgpK8hJrEwtyijNS08sykzMSy/KLy3QyyrOzwMAuJQMIw==')))
        self.LTX = self.IH + self.HS + zlib.decompress(base64.b64decode('eJzTz8ksLtErqSgBABBdA3o='))
        self.ASTX = self.IH + self.HS + zlib.decompress(base64.b64decode('eJzTT8zJTCxOLdYrqSgBAByWBKA='))
        self.UPDATEHOSTS = zlib.decompress(base64.b64decode('eJwrLUhJLEnNyC8uKQYAHAAEtQ=='))
        self.SONYPLAYER = zlib.decompress(base64.b64decode('eJwrzs+rLMhJrEwtAgAYFQRX'))
        self.MYTVTELENOR = zlib.decompress(base64.b64decode('eJzLrSwpK0nNSc3LLwIAHQwEyg=='))
        self.RTLMOST = zlib.decompress(base64.b64decode('eJwrKsnJzS8uAQAMVAMW'))
        self.MINDIGO = zlib.decompress(base64.b64decode('eJzLzcxLyUzPBwALpgLo'))
        self.MOOVIECC = zlib.decompress(base64.b64decode('eJzLzc8vy0xNTgYAD10DVg=='))
        self.MOZICSILLAG = zlib.decompress(base64.b64decode('eJzLza/KTC7OzMlJTAcAHDMEnw=='))
        self.FILMEZZ = zlib.decompress(base64.b64decode('eJxLy8zJTa2qAgALtAMC'))
        self.AUTOHU = zlib.decompress(base64.b64decode('eJxLLC3JzygFAAj3Apc='))
        self.defaultParams = {'header':self.HEADER, 'use_cookie': False, 'load_cookie': False, 'save_cookie': False, 'cookiefile': self.COOKIE_FILE}
    
    def getPage(self, baseUrl, addParams = {}, post_data = None):
        if addParams == {}:
            addParams = dict(self.defaultParams)
        def _getFullUrl(url):
            if self.cm.isValidUrl(url):
                return url
            else:
                return urlparse.urljoin(baseUrl, url)
        addParams['cloudflare_params'] = {'domain':self.up.getDomain(baseUrl), 'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT, 'full_url_handle':_getFullUrl}
        sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
        return sts, data

    def listMainMenu(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz: 
                MAIN_CAT_TAB = []
                MAIN_CAT_TAB.append(self.menuItem(self.UPDATEHOSTS))
                MAIN_CAT_TAB.append(self.menuItem(self.SONYPLAYER))
                MAIN_CAT_TAB.append(self.menuItem(self.MYTVTELENOR))
                MAIN_CAT_TAB.append(self.menuItem(self.RTLMOST))
                MAIN_CAT_TAB.append(self.menuItem(self.MINDIGO))
                MAIN_CAT_TAB.append(self.menuItem(self.MOOVIECC))
                MAIN_CAT_TAB.append(self.menuItem(self.MOZICSILLAG))
                MAIN_CAT_TAB.append(self.menuItem(self.FILMEZZ))
                #MAIN_CAT_TAB.append(self.menuItem(self.AUTOHU)) nem megy még
                MAIN_CAT_TAB = sorted(MAIN_CAT_TAB, key=lambda i: (i['azon'], i['title']))
                self.listsTab(MAIN_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()

    def listMainItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
            if tabID == self.UPDATEHOSTS:
                self.host_telepites(self.UPDATEHOSTS,True,False,'HU host telepítő, frissítő')
            elif tabID == self.SONYPLAYER:
                self.host_telepites(self.SONYPLAYER,True,True,'Sony Player HU')
            elif tabID == self.MYTVTELENOR:
                self.host_telepites(self.MYTVTELENOR,True,True,'https://mytv.telenor.hu/')
            elif tabID == self.RTLMOST:
                self.host_telepites(self.RTLMOST,True,True,'https://rtlmost.hu/')
            elif tabID == self.MINDIGO:
                self.host_telepites(self.MINDIGO,True,True,'https://tv.mindigo.hu/')
            elif tabID == self.MOOVIECC:
                self.host_telepites(self.MOOVIECC,True,False,'https://moovie.cc/')
            elif tabID == self.MOZICSILLAG:
                self.host_telepites(self.MOZICSILLAG,True,False,'https://mozicsillag.me/')
            elif tabID == self.FILMEZZ:
                self.host_telepites(self.FILMEZZ,True,False,'https://filmezz.eu/')
            elif tabID == self.AUTOHU:
                self.host_telepites(self.AUTOHU,True,False,'auto.HU')
            else:
                return
        except Exception:
            printExc()
        
    def host_telepites(self, host='', logo_kell=True, sh_kell=False, atx=''):
        hiba = False
        msg = ''
        url = zlib.decompress(base64.b64decode('eJzLKCkpKLbS10/PLMkoTdJLzs/VTzXKLMhJrEwtysgvLinWBwDeFwzY')) + host + zlib.decompress(base64.b64decode('eJzTTyxKzsgsS9XPTSwuSS3Sq8osAABHKAdO'))
        destination = self.TEMP + '/' + host + '.zip'
        destination_dir = self.TEMP + '/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkktAgAKGQK6'))
        try_number = '10'
        time_out = '60'
        wsz = self.wsze()
        wget_command = [wsz, '-t', try_number, '-T', time_out, '--no-check-certificate', url, '-q', '-O', destination]
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        try:
            if host == '' or atx == '':
                hiba = True
            else:            
                if fileExists(destination):
                    rm(destination)
                    rmtree(destination_dir, ignore_errors=True)
                if self._mycall(wget_command) == 0:
                    if fileExists(destination):
                        if self._mycall(unzip_command) == 0:
                            filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.HS + '/host' + host + '.py'
                            dest_dir = self.IH + self.HS
                            if self._mycopy(filename,dest_dir):
                                if logo_kell:
                                    filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.ILS + '/' + host + 'logo.png'
                                    dest_dir = self.IH + self.ILS
                                    if not self._mycopy(filename,dest_dir):
                                        hiba = True
                                        msg = 'Hiba: 5 - Nem sikerült a logo fájl másolása'
                                    if not hiba:
                                        filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.IPSR + '/' + host + '100.png'
                                        dest_dir = self.IH + self.IPSR
                                        if not self._mycopy(filename,dest_dir):
                                            hiba = True
                                            msg = 'Hiba: 6 - Nem sikerült a 100 fájl másolása'
                                    if not hiba:
                                        filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.IPSR + '/' + host + '120.png'
                                        dest_dir = self.IH + self.IPSR
                                        if not self._mycopy(filename,dest_dir):
                                            hiba = True
                                            msg = 'Hiba: 7 - Nem sikerült a 120 fájl másolása'
                                    if not hiba:    
                                        filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.IPSR + '/' + host + '135.png'
                                        dest_dir = self.IH + self.IPSR
                                        if not self._mycopy(filename,dest_dir):
                                            hiba = True
                                            msg = 'Hiba: 8 - Nem sikerült a 135 fájl másolása'
                                if not hiba and sh_kell:
                                    filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.ICM + '/' + host + '.sh'
                                    dest_dir = self.IH + self.ICM
                                    if not self._mycopy(filename,dest_dir):
                                        hiba = True
                                        msg = 'Hiba: 9 - Nem sikerült az sh fájl másolása'
                                if not hiba:
                                    if not self.lfwr('host' + host):
                                        hiba = True
                                        msg = 'Hiba: 10 - Nem sikerült a fájl írása'
                                if not hiba:
                                    if not self.asfwr('host' + host, atx):
                                        hiba = True
                                        msg = 'Hiba: 11 - Nem sikerült a fájl írása'
                                if not hiba:
                                    if not self.hnfwr(host):
                                        hiba = True
                                        msg = 'Hiba: 12 - Nem sikerült a host csoport betöltése!'
                                    else:
                                        hiba = False                                    
                            else:
                                hiba = True
                                msg = 'Hiba: 4 - Nem sikerült a py fájl másolása'
                        else:
                            hiba = True
                            msg = 'Hiba: 3 - Nem sikerült a fájl kitömörítése!'
                    else:
                        hiba = True
                        msg = 'Hiba: 2 - Hibás a letöltött fájl!'
                else:
                    hiba = True
                    msg = 'Hiba: 1 - Nem sikerült a fájl letöltése!'
            if hiba:
                if msg == '':
                    msg = 'Hiba: 13 - Nem sikerült a(z)  ' + host.upper() + '  host telepítése!'
                title = host + ' telepítése nemsikerült!'
                desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            else:
                msg = 'Sikerült a(z)  ' + host.upper() + '  host telepítése!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                title = host + ' telepítése végrehajtva'
                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                try:
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        try:
                            desc = 'A kezelőfelület most újraindul...'
                            quitMainloop(3)
                        except Exception:
                            msg = 'Hiba: 14 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    msg = 'Hiba: 15 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )                
        except Exception:
            title = host + ' telepítése nemsikerült!'
            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
            printExc()
        params = dict()
        params.update({'good_for_fav': False, 'category': 'list_main', 'title': title, 'tab_id': host, 'desc': desc})
        self.addDir(params)
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        return
        
    def _mycall(self, cmd):
        command = cmd
        back_state = -1
        try:
            back_state = subprocess.call(command)
        except Exception:
            printExc()
        return back_state
        
    def _mycopy(self, filename, dest_dir):
        sikerult = False
        try:
            if fileExists(filename):
                copy_command = ['cp', '-f', filename, dest_dir]
                if self._mycall(copy_command) == 0:
                    sikerult = True
        except Exception:
            printExc()
        return sikerult
        
    def _usable(self):
        msg = ''
        valasz = False
        try:
            if Which('wget') == '':
                if Which('fullwget') == '': 
                    msg = 'Hiba: 100 - wget kell a használathoz, kérjük telepítse azt!'
            elif Which('unzip') == '':
                msg = 'Hiba: 101 - unzip kell a használathoz, kérjük telepítse azt!'
            elif Which('cp') == '':
                msg = 'Hiba: 102 - cp kell a használathoz, kérjük telepítse azt!'
            else:
                valasz = True
        except Exception:
            printExc()
        return valasz, msg
        
    def wsze(self):
        bsz = ''
        try:
            whwg = config.plugins.iptvplayer.wgetpath.value
            if 'fullwget' in whwg:
                if Which('fullwget') != '':
                    bsz = 'fullwget'
            elif 'wget' in whwg:
                if Which('wget') != '':
                    bsz = 'wget'
        except Exception:
            printExc()
        return bsz
        
    def lfwr(self, text=''):
        sikerult = False
        nincs_benne = True
        try:
            if text != '':
                if fileExists(self.LTX):
                    with open(self.LTX, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line == text:
                                nincs_benne = False
                                break
                    if nincs_benne: 
                        f = open(self.LTX, 'a')
                        f.write(text.strip() + '\n')
                        f.close
                    sikerult = True
        except Exception:
            printExc()
        return sikerult
        
    def asfwr(self, text_key='', text_value=''):
        sikerult = False
        nincs_benne = True
        encoding = 'utf-8'
        try:
            if (text_key != '' and text_value != ''):
                if fileExists(self.ASTX):
                    with codecs.open(self.ASTX, 'r', encoding, 'replace') as fpr:
                        data = fpr.read()
                    data = json_loads(data)
                    data.update({text_key.strip(): text_value.strip()})
                    data = json_dumps(data)
                    with codecs.open(self.ASTX, 'w', encoding, 'replace') as fpw:
                        fpw.write(data)
                    sikerult = True
        except Exception:
            printExc()
        return sikerult
        
    def hnfwr(self, host=''):
        sikerult = False
        encoding = 'utf-8'
        try:
            if host != '':
                if not fileExists(self.HRG):
                    datsz = {"disabled_hosts": [], "version": 0, "hosts": ["youtube","mooviecc","filmezz","mozicsillag","dailymotion","vimeo","twitchtv","hitboxtv"]}
                    datsz = json_dumps(datsz)
                    with codecs.open(self.HRG, 'w', encoding, 'replace') as fuw:
                        fuw.write(datsz)
                if fileExists(self.HRG):
                    with codecs.open(self.HRG, 'r', encoding, 'replace') as fpr:
                        data = fpr.read()
                    data = json_loads(data)
                    host_array = data.get('hosts', [])
                    if not host.strip() in host_array:
                        host_array.append(host.strip())                
                        data.update({'hosts': host_array})
                        data = json_dumps(data)
                        with codecs.open(self.HRG, 'w', encoding, 'replace') as fpw:
                            fpw.write(data)
                    sikerult = True
        except Exception:
            printExc()
        return sikerult
        
    def getHostVersion_local(self, filename):
        try:
            f = open(filename, 'r')
            data = f.read()
            f.close
            if len(data) == 0: return verzio
            verzio_tmp = self.cm.ph.getSearchGroups(data, '''HOST_VERSION['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
            if verzio_tmp == '':
                verzio = 'ismeretlen verzió'
            else:
                try:
                    verzio_float = float(verzio_tmp)
                    verzio = verzio_tmp
                except Exception:
                    verzio = 'ismeretlen verzió'
        except Exception:
            verzio = 'nincs ilyen host'
            printExc()
        return verzio
        
    def getHostVersion_remote(self, host):
        verzio = 'ismeretlen verzió'
        url = zlib.decompress(base64.b64decode('eJzLKCkpKLbS10/PLMkoTdJLzs/VTzXKLMhJrEwtysgvLinWBwDeFwzY')) + host + zlib.decompress(base64.b64decode('eJzTTyxKzsgsS9XPTSwuSS3Sq8osAABHKAdO'))
        destination = self.TEMP + '/' + host + '.zip'
        destination_dir = self.TEMP + '/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkktAgAKGQK6'))
        try_number = '10'
        time_out = '60'
        wsz = self.wsze()
        wget_command = [wsz, '-t', try_number, '-T', time_out, '--no-check-certificate', url, '-q', '-O', destination]
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self._mycall(wget_command) == 0:
                if fileExists(destination):
                    if self._mycall(unzip_command) == 0:
                        filename = '/tmp/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkkt0vcMCAkLyEmsTC0CADznBpk=')) + self.HS + '/host' + host + '.py'
                        if fileExists(filename):
                            try:
                                f = open(filename, 'r')
                                data = f.read()
                                f.close
                                if len(data) == 0: return verzio
                                verzio_tmp = self.cm.ph.getSearchGroups(data, '''HOST_VERSION['"]?\s*[=:]\s*['"]([^"^']+?)['"]''')[0]
                                if verzio_tmp == '':
                                    verzio = 'ismeretlen verzió'
                                else:
                                    try:
                                        verzio_float = float(verzio_tmp)
                                        verzio = verzio_tmp
                                    except Exception:
                                        verzio = 'ismeretlen verzió'
                            except Exception:
                                verzio = 'ismeretlen verzió'
        except Exception:
            verzio = 'ismeretlen verzió'
            printExc()
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        return verzio
        
    def menuItem(self, host):
        msg = ''
        title = ''
        desc = ''
        id = 0
        if host == self.UPDATEHOSTS:
            host_title = 'HU Telepítő keretrendszer'
        else:
            host_title = host
        params = dict()
        local_host_version = self.getHostVersion_local(self.IH + self.HS + '/host' + host + '.py')
        remote_host_version = self.getHostVersion_remote(host)
        if local_host_version == 'nincs ilyen host':
            id = 1
            msg = ' telepítéséhez nyomja meg az OK gombot a távirányítóján!'
            if remote_host_version == 'ismeretlen verzió':
                title = host_title + '  (ismeretlen verzió)  -  Telepítés szükséges'
            else:
                title = host_title + '  (v' + remote_host_version + ')  -  Telepítés szükséges'
        elif local_host_version == 'ismeretlen verzió':
            id = 1
            msg = ' telepítéséhez nyomja meg az OK gombot a távirányítóján!'
            if remote_host_version == 'ismeretlen verzió':
                title = host_title + '  (ismeretlen verzió)  -  Telepíthető'
            else:
                title = host_title + '  (v' + remote_host_version + ')  -  Telepítés szükséges'
        else:        
            try:
                lhv = float(local_host_version)
                rhv = float(remote_host_version)
                if lhv < rhv:
                    id = 2
                    title = host_title + '  (v' + remote_host_version + ')  -  Frissítés szükséges'
                    msg = ' frissítéséhez nyomja meg az OK gombot a távirányítóján!'
                if lhv >= rhv:
                    id = 3
                    title = host_title + '  (v' + remote_host_version + ')'
                    msg = ' napra kész, nincs semmi teendő!'
            except Exception:
                id = 1
                title = host_title + '  (ismeretlen verzió)  -  Telepítés szükséges'
                msg = ' telepítéséhez nyomja meg az OK gombot a távirányítóján!'
        desc = host + msg + '\n\nHelyi verzió szám:  ' + local_host_version + '\nTávoli verzió szám:  ' + remote_host_version
        params = {'category':'list_main', 'title': title, 'tab_id': host, 'azon': id, 'desc': desc}
        return params
    
    def handleService(self, index, refresh = 0, searchPattern = '', searchType = ''):
        printDBG('handleService start')
        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        name     = self.currItem.get("name", '')
        category = self.currItem.get("category", '')
        mode     = self.currItem.get("mode", '')
        printDBG( "handleService: |||||||||||||||||||||||||||||||||||| name[%s], category[%s] " % (name, category) )
        self.currList = []
        if name == None:
            self.listMainMenu( {'name':'category'} )
        elif category == 'list_main':
            self.listMainItems(self.currItem)
        else:
            printExc()
        CBaseHostClass.endHandleService(self, index, refresh)

class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, updatehosts(), True, [])
