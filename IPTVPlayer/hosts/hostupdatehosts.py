# -*- coding: utf-8 -*-
###################################################
# 2019-04-24 by Alec - updatehosts HU host telepítő
###################################################
HOST_VERSION = "1.8"
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _, SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, byteify, rm, rmtree, mkdirs, DownloadFile, GetBinDir, GetTmpDir, GetFileSize, MergeDicts, GetConfigDir, Which
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads, dumps as json_dumps
from Plugins.Extensions.IPTVPlayer.libs import ph
###################################################

###################################################
# FOREIGN import
###################################################
from urllib2 import Request, urlopen, URLError, HTTPError
import urlparse
import re
import urllib
import urllib2
import random
import os
import datetime
import time
import zlib
import cookielib
import base64
import traceback
try:
    import subprocess
    FOUND_SUB = True
except Exception:
    FOUND_SUB = False
import codecs
from Tools.Directories import resolveFilename, fileExists, SCOPE_PLUGINS
from os import rename as os_rename
from enigma import quitMainloop
from copy import deepcopy
try:
    import json
except Exception:
    import simplejson as json
from Components.config import config, ConfigText, getConfigListEntry
from datetime import datetime
from time import sleep
from hashlib import sha1
###################################################

###################################################
# E2 GUI COMMPONENTS 
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvmultipleinputbox import IPTVMultipleInputBox
from Screens.MessageBox import MessageBox
###################################################

###################################################
# Config options for HOST
###################################################
config.plugins.iptvplayer.webhuplayer_dir = ConfigText(default = "/hdd", fixed_size = False)
config.plugins.iptvplayer.webhuplayer_file = ConfigText(default = "urllist.stream", fixed_size = False)

def GetConfigList():
    optionList = []
    optionList.append(getConfigListEntry("Web HU Player könyvtár:", config.plugins.iptvplayer.webhuplayer_dir))
    optionList.append(getConfigListEntry("Web HU Player fájl:", config.plugins.iptvplayer.webhuplayer_file))
    return optionList
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
        self.HLM = self.IH + zlib.decompress(base64.b64decode('eJzTz8lPTsxJ1c8o1fdxjvd1DQ52dHcNBgBVsAch'))
        self.UPDATEHOSTS = zlib.decompress(base64.b64decode('eJwrLUhJLEnNyC8uKQYAHAAEtQ=='))
        self.SONYPLAYER = zlib.decompress(base64.b64decode('eJwrzs+rLMhJrEwtAgAYFQRX'))
        self.MYTVTELENOR = zlib.decompress(base64.b64decode('eJzLrSwpK0nNSc3LLwIAHQwEyg=='))
        self.RTLMOST = zlib.decompress(base64.b64decode('eJwrKsnJzS8uAQAMVAMW'))
        self.MINDIGO = zlib.decompress(base64.b64decode('eJzLzcxLyUzPBwALpgLo'))
        self.MOOVIECC = zlib.decompress(base64.b64decode('eJzLzc8vy0xNTgYAD10DVg=='))
        self.MOZICSILLAG = zlib.decompress(base64.b64decode('eJzLza/KTC7OzMlJTAcAHDMEnw=='))
        self.FILMEZZ = zlib.decompress(base64.b64decode('eJxLy8zJTa2qAgALtAMC'))
        self.WEBHUPLAYER = zlib.decompress(base64.b64decode('eJwrT03KKC3ISaxMLQIAG+YEqQ=='))
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
            msg_host = 'Magyar Hostok listája\n\nA hostok betöltése több időt vehet igénybe!  A letöltés ideje függ az internet sebességétől, illetve a gyűjtő oldal leterheltségétől is...\nVárd meg míg a hostok listája megjelenik. Ez eltarthat akár 3 percig is.\nA host gyűjtő oldalán néha hiba előfordulhat...'
            msg_magyar = 'Az E2iPlayer magyarítását lehet itt végrehajtani.'
            msg_javitas = 'Az E2iPlayer különböző hibáinak javítására nyilik itt lehetőség.'
            msg_urllist = 'Blindspot féle urllist.stream fájlt lehet itt telepíteni, frissíteni.\n\nA stream fájlt az "Urllists player" hosttal (Egyéb csoport) lehet lejátszani a Live streams menüpontban... '
            MAIN_CAT_TAB = [{'category': 'list_main', 'title': 'Magyar hostok', 'tab_id': 'hostok', 'desc': msg_host},
                            {'category': 'list_main', 'title': 'E2iPlayer magyarítása', 'tab_id': 'magyaritas', 'desc': msg_magyar},
                            {'category': 'list_main', 'title': 'E2iPlayer hibajavításai', 'tab_id': 'javitas', 'desc': msg_javitas},
                            {'category': 'list_main', 'title': 'Urllist fájl telepítése', 'tab_id': 'urllist', 'desc': msg_urllist}
                           ]
            self.listsTab(MAIN_CAT_TAB, cItem)
        except Exception:
            printExc()
            
    def listMainItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
            if tabID == 'hostok':
                self.Hostok_listaja(cItem)
            elif tabID == 'magyaritas':
                self.Magyaritas(cItem)
            elif tabID == 'javitas':
                self.Javitas(cItem)
            elif tabID == 'urllist':
                self.Urllist_stream(cItem)
            else:
                return
        except Exception:
            printExc()
            
    def Hostok_listaja(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                HOST_CAT_TAB = []
                HOST_CAT_TAB.append(self.menuItem(self.UPDATEHOSTS))
                HOST_CAT_TAB.append(self.menuItem(self.SONYPLAYER))
                HOST_CAT_TAB.append(self.menuItem(self.MYTVTELENOR))
                HOST_CAT_TAB.append(self.menuItem(self.RTLMOST))
                HOST_CAT_TAB.append(self.menuItem(self.MINDIGO))
                HOST_CAT_TAB.append(self.menuItem(self.MOOVIECC))
                HOST_CAT_TAB.append(self.menuItem(self.MOZICSILLAG))
                HOST_CAT_TAB.append(self.menuItem(self.FILMEZZ))
                HOST_CAT_TAB.append(self.menuItem(self.WEBHUPLAYER))
                HOST_CAT_TAB.append(self.menuItem(self.AUTOHU))
                HOST_CAT_TAB = sorted(HOST_CAT_TAB, key=lambda i: (i['azon'], i['title']))
                self.listsTab(HOST_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Magyaritas(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                HUN_CAT_TAB = []
                HUN_CAT_TAB.append(self.menuItemHun())
                self.listsTab(HUN_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Javitas(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                msg_jav = '2019.04.24.\n\nAz alábbi hibára ad megoldást ez a javítás:\n"token" parameter not in video info'
                HIBAJAV_CAT_TAB = [{'category': 'list_second', 'title': 'YouTube hiba javítása', 'tab_id': 'hibajav_youtube', 'desc': msg_jav}
                                  ]
                self.listsTab(HIBAJAV_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Urllist_stream(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                URLLIST_CAT_TAB = []
                URLLIST_CAT_TAB.append(self.menuItemUrllist())
                self.listsTab(URLLIST_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()

    def listSecondItems(self, cItem):
        try:
            tabID = cItem.get('tab_id', '')
            if tabID == 'magyaritas':
                self.hun_telepites()
            elif tabID == 'urllist':
                if self.cpve(config.plugins.iptvplayer.webhuplayer_dir.value) and self.cpve(config.plugins.iptvplayer.webhuplayer_file.value):
                    msg = 'A telepítés, frissítés helye:  ' + config.plugins.iptvplayer.webhuplayer_dir.value + '/' + config.plugins.iptvplayer.webhuplayer_file.value + '\nFolytathatom?'
                    msg += '\n\nHa máshova szeretnéd, akkor a KÉK gomb, majd az Oldal beállításai.\nAdatok megadása, s utána a ZÖLD gomb (Mentés) megnyomása!'
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        self.urllist_telepites()
                else:
                    msg = 'A kék gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa megfelelőek az előre beállított értékek, akkor ZÖLD gomb (Mentés) megnyomása!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            elif tabID == 'hibajav_youtube':
                self.ytjv()
            elif tabID == self.UPDATEHOSTS:
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
            elif tabID == self.WEBHUPLAYER:
                self.host_telepites(self.WEBHUPLAYER,True,False,'Web HU Player')
            elif tabID == self.AUTOHU:
                self.host_telepites(self.AUTOHU,True,False,'auto.HU')
            else:
                return
        except Exception:
            printExc()
            
    def ytjv(self):
        url = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUr8wvLSlNStUrqAQAfOkRHA=='))
        destination = zlib.decompress(base64.b64decode('eJzTL8kt0K/MLy0pTUrVK6gEAC2KBdQ='))
        local_hely = self.IH + zlib.decompress(base64.b64decode('eJzTz8lMKtavzC8tKU1KjU/J0U+tKClKTC7JLwIAh0EKUA=='))
        local_filename = zlib.decompress(base64.b64decode('eJyrzC8tKU1KBQAMkQMO'))
        local_ext1 = zlib.decompress(base64.b64decode('eJzTK6jMBwADbQGH'))
        local_ext2 = zlib.decompress(base64.b64decode('eJzTK6gEAAHmARg='))
        local_file1 = local_hely + '/' + local_filename + local_ext1
        local_file2 = local_hely + '/' + local_filename + local_ext2
        hiba = False
        msg = ''
        if fileExists(destination):
            rm(destination)
        try:
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
                        if fileExists(local_file1):
                            try:
                                if not fileExists(local_file1 + 'bak'):
                                    os_rename(local_file1, local_file1 + 'bak')
                            except Exception:
                                hiba = True
                                msg = 'Hiba: 404 - Nem sikerült a fájl átnevezése!'
                            if not hiba:
                                if self._mycopy(destination,local_file2):
                                    hiba = False
                                else:
                                    hiba = True
                                    msg = 'Hiba: 405 - Nem sikerült letöltött fájl másolása a helyére'                                
                        else:
                            hiba = True
                            msg = 'Hiba: 403 - Nincs ilyen fájl!'
                    else:
                        hiba = True
                        msg = 'Hiba: 402 - A letöltött fájl üres!'
                else:
                    hiba = True
                    msg = 'Hiba: 401 - Hibás a letöltött fájl!'
            else:
                hiba = True
                msg = 'Hiba: 400 - Nem sikerült a fájl letöltése!'
            if hiba:
                if msg == '':
                    msg = 'Hiba: 410 - Nem sikerült a Youtube hiba javítása!'
                title = 'A YouTube hiba javítása nemsikerült!'
                desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            else:
                msg = 'Sikerült a YouTube hiba javítása!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                title = 'YouTube hiba javítása végrehajtva'
                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                try:
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        try:
                            desc = 'A kezelőfelület most újraindul...'
                            quitMainloop(3)
                        except Exception:
                            msg = 'Hiba: 411 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    msg = 'Hiba: 412 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
        except Exception:
            title = 'A YouTube hiba javítása nemsikerült!'
            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
            printExc()            
        params = dict()
        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'hibajav_youtube', 'desc': desc})
        self.addDir(params)            
        if fileExists(destination):
            rm(destination)            
        return
            
    def hun_telepites(self):
        hiba = False
        msg = ''
        url = zlib.decompress(base64.b64decode('eJwFwVEKgEAIBcAb7YM+u40tkoKLom5Qp29GuqNO4NaWfY3pC3xoGL2c4tUF2eaTjEE5RR/GomrO8Wn8zdsXcg=='))
        destination = self.TEMP + zlib.decompress(base64.b64decode('eJzTzyjNyU9OzEnVq8osAAAiHgT+'))
        destination_dir = self.TEMP + zlib.decompress(base64.b64decode('eJzTzyjNyU9OzEnVzU0sLkktAgAzPwY2'))
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
                        if self._mycall(unzip_command) == 0:
                            filename = zlib.decompress(base64.b64decode('eJzTL8kt0M8ozclPTsxJ1c1NLC5JLdL3DAgJC8hJrAQyIRJAFfo+zvG+rsHBju6uwUgK9HLzATUCF54='))
                            dest_dir = self.HLM
                            if self._mycopy(filename,dest_dir):
                                filename = zlib.decompress(base64.b64decode('eJzTL8kt0M8ozclPTsxJ1c1NLC5JLdL3DAgJC8hJrAQyIRJAFfo+zvG+rsHBju6uwUgK9AryATUIF6E='))
                                dest_dir = self.HLM
                                if self._mycopy(filename,dest_dir):
                                    hiba = False
                                else:
                                    hiba = True
                                    msg = 'Hiba: 200 - Nem sikerült a po fájl másolása'
                            else:
                                hiba = True
                                msg = 'Hiba: 201 - Nem sikerült a mo fájl másolása'
                        else:
                            hiba = True
                            msg = 'Hiba: 202 - Nem sikerült a fájl kitömörítése!'
                    else:
                        hiba = True
                        msg = 'Hiba: 208 - A letöltött fájl üres!'
                else:
                    hiba = True
                    msg = 'Hiba: 203 - Hibás a letöltött fájl!'
            else:
                hiba = True
                msg = 'Hiba: 204 - Nem sikerült a fájl letöltése!'
            if hiba:
                if msg == '':
                    msg = 'Hiba: 205 - Nem sikerült a magyarítás telepítése!'
                title = 'A magyarítás telepítése nemsikerült!'
                desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            else:
                msg = 'Sikerült a magyarítás telepítése!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                title = 'Magyarítás telepítése végrehajtva'
                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                try:
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        try:
                            desc = 'A kezelőfelület most újraindul...'
                            quitMainloop(3)
                        except Exception:
                            msg = 'Hiba: 206 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    msg = 'Hiba: 207 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
        except Exception:
            title = 'A magyarítás telepítése nemsikerült!'
            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
            printExc()
        params = dict()
        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'magyaritas', 'desc': desc})
        self.addDir(params)
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        return
        
    def cpve(self, cfpv=''):
        vissza = False
        try:
            if cfpv != '':
                mk = cfpv
                if mk != '':
                    vissza = True
        except Exception:
            printExc()
        return vissza
        
    def urllist_telepites(self):
        hiba = False
        msg = ''
        url = zlib.decompress(base64.b64decode('eJwFwUEKgDAMBMAfdcGjv4klmEBKS7IV9PXOGLnqBG6n7av1OaCHr5BX02axsDPCi5Ds5o9iSFGzfb5+uZcXNA=='))
        destination = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7Rq8osAAAzigZA'))
        destination_dir = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7RzU0sLkktAgBIcQd4'))
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
                        if self._mycall(unzip_command) == 0:
                            filename = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7RzU0sLkktgnH1ikuKUhNzAedBDXA='))
                            dest_dir = config.plugins.iptvplayer.webhuplayer_dir.value + '/' + config.plugins.iptvplayer.webhuplayer_file.value
                            if mkdirs(config.plugins.iptvplayer.webhuplayer_dir.value):
                                if self._mycopy(filename,dest_dir):
                                    if fileExists(destination):
                                        if GetFileSize(destination) > 0:
                                            hiba = False
                                        else:
                                            hiba = True
                                            msg = 'Hiba: 301 - A letöltött stream fájl üres'    
                                    else:
                                        hiba = True
                                        msg = 'Hiba: 302 - Nem létezik a letöltött stream fájl'    
                                else:
                                    hiba = True
                                    msg = 'Hiba: 303 - Nem sikerült a stream fájl másolása'
                            else:
                                hiba = True
                                msg = 'Hiba: 311 - Nem sikerült a könyvtárt létrehozni'
                        else:
                            hiba = True
                            msg = 'Hiba: 304 - Nem sikerült a fájl kitömörítése!'
                    else:
                        hiba = True
                        msg = 'Hiba: 305 - A letöltött fájl üres!'
                else:
                    hiba = True
                    msg = 'Hiba: 306 - Hibás a letöltött fájl!'
            else:
                hiba = True
                msg = 'Hiba: 307 - Nem sikerült a fájl letöltése!'
            if hiba:
                if msg == '':
                    msg = 'Hiba: 308 - Nem sikerült az Urllist.stream telepítése!'
                title = 'Az Urllist.stream telepítése nemsikerült!'
                desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            else:
                msg = 'Sikerült az Urllist.stream telepítése!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                title = 'Az Urllist.stream telepítése végrehajtva'
                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                try:
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        try:
                            desc = 'A kezelőfelület most újraindul...'
                            quitMainloop(3)
                        except Exception:
                            msg = 'Hiba: 309 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    msg = 'Hiba: 310 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a telepítés, frissítés!!!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
        except Exception:
            title = 'Az Urllist.stream telepítése nemsikerült!'
            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
            printExc()
        params = dict()
        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'urllist', 'desc': desc})
        self.addDir(params)
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        return
        
    def host_telepites(self, host='', logo_kell=True, sh_kell=False, atx=''):
        hiba = False
        msg = ''
        url = zlib.decompress(base64.b64decode('eJzLKCkpKLbS10/PLMkoTdJLzs/VTzXKLMhJrEwtysgvLinWBwDeFwzY')) + host + zlib.decompress(base64.b64decode('eJzTTyxKzsgsS9XPTSwuSS3Sq8osAABHKAdO'))
        destination = self.TEMP + '/' + host + '.zip'
        destination_dir = self.TEMP + '/' + host + zlib.decompress(base64.b64decode('eJzTzU0sLkktAgAKGQK6'))
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        try:
            if host == '' or atx == '':
                hiba = True
            else:            
                if fileExists(destination):
                    rm(destination)
                    rmtree(destination_dir, ignore_errors=True)
                if self.dflt(url,destination):
                    if fileExists(destination):
                        if GetFileSize(destination) > 0:
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
                            msg = 'Hiba: 16 - A letöltött fájl üres!'
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
        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': host, 'desc': desc})
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
            if Which('python2') == '':
                msg = 'Hiba: 100 - Python 2.7 kell a használathoz!'
            elif Which('unzip') == '':
                msg = 'Hiba: 101 - unzip kell a használathoz, kérjük telepítsd azt!'
            elif Which('cp') == '':
                msg = 'Hiba: 102 - cp kell a használathoz, kérjük telepítsd azt!'
            elif not os.path.isdir(self.IH):
                msg = 'Hiba: 103 - Nem megfelelő E2iPlayer könyvtár!'
            elif FOUND_SUB == False:
                msg = 'Hiba: 104 - Sajnos nem kompatibilis a set-top-box rendszered a használathoz!\nsubprocess kell a használathoz, telepítsd azt!'
            else:
                valasz = True
        except Exception:
            printExc()
        return valasz, msg
        
    def dflt(self, url, fnm, hsz=2, ved=3):
        vissza = False
        try:
            if url == '' or fnm == '' or type(hsz) != int or type(ved) != int:
                return vissza
            for i in range(hsz):
                tmp = DownloadFile(url,fnm)
                if tmp:
                    vissza = True
                    break
                else:
                    sleep(ved)
        except Exception:
            printExc()
        return vissza
        
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
        verzio = 'ismeretlen verzió'
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
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
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
            if remote_host_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét a Magyar hostok betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = host_title + '  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                title = host_title + '  (v' + remote_host_version + ')  -  Telepítés szükséges'
        elif local_host_version == 'ismeretlen verzió':
            id = 1
            if remote_host_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét a Magyar hostok betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = host_title + '  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                title = host_title + '  (v' + remote_host_version + ')  -  Telepítés szükséges'
        else:        
            try:
                lhv = float(local_host_version)
                rhv = float(remote_host_version)
                if lhv < rhv:
                    id = 2
                    title = host_title + '  (v' + remote_host_version + ')  -  Frissítés szükséges'
                    msg = ' frissítéséhez nyomd meg az OK gombot a távirányítón!'
                if lhv >= rhv:
                    id = 3
                    title = host_title + '  (v' + remote_host_version + ')'
                    msg = ' napra kész, nincs semmi teendő!'
            except Exception:
                id = 1
                title = host_title + '  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét a Magyar hostok betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
        desc = host + msg + '\n\nHelyi verzió szám:  ' + local_host_version + '\nTávoli verzió szám:  ' + remote_host_version
        params = {'category':'list_second', 'title': title, 'tab_id': host, 'azon': id, 'desc': desc}
        return params
        
    def getHunVersion_local(self):
        verzio = 'ismeretlen verzió'
        verzio_tmp = ''
        try:
            f = open(self.HLM + zlib.decompress(base64.b64decode('eJzT9wwICQvISaxMLdIryAcAIlQE7Q==')), 'r')
            data = f.read()
            f.close
            if len(data) == 0: return verzio
            tmp = self.cm.ph.getDataBeetwenMarkers(data, '"Project-Id-Version:', '\n"')[1]
            m = re.search(r'\d+.\d+',tmp)
            if m is not None:
                verzio_tmp = m.group(0)
            if verzio_tmp == '':
                verzio = 'ismeretlen verzió'
            else:
                try:
                    verzio_float = float(verzio_tmp)
                    verzio = verzio_tmp
                except Exception:
                    verzio = 'ismeretlen verzió'
        except Exception:
            verzio = 'nincs helyi verzio'        
            printExc()
        return verzio
        
    def getHunVersion_remote(self):
        verzio = 'ismeretlen verzió'
        verzio_tmp = ''
        url = zlib.decompress(base64.b64decode('eJwFwVEKgEAIBcAb7YM+u40tkoKLom5Qp29GuqNO4NaWfY3pC3xoGL2c4tUF2eaTjEE5RR/GomrO8Wn8zdsXcg=='))
        destination = self.TEMP + zlib.decompress(base64.b64decode('eJzTzyjNyU9OzEnVq8osAAAiHgT+'))
        destination_dir = self.TEMP + zlib.decompress(base64.b64decode('eJzTzyjNyU9OzEnVzU0sLkktAgAzPwY2'))
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
                        if self._mycall(unzip_command) == 0:
                            filename = zlib.decompress(base64.b64decode('eJzTL8kt0M8ozclPTsxJ1c1NLC5JLdL3DAgJC8hJrAQyIRJAFfo+zvG+rsHBju6uwUgK9AryATUIF6E='))
                            if fileExists(filename):
                                try:
                                    f = open(filename, 'r')
                                    data = f.read()
                                    f.close
                                    if len(data) == 0: return verzio
                                    tmp = self.cm.ph.getDataBeetwenMarkers(data, '"Project-Id-Version:', '\n"')[1]
                                    m = re.search(r'\d+.\d+',tmp)
                                    if m is not None:
                                        verzio_tmp = m.group(0)
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
        
    def menuItemHun(self):
        msg = ''
        title = ''
        desc = ''
        id = 0
        params = dict()
        local_hun_version = self.getHunVersion_local()
        remote_hun_version = self.getHunVersion_remote()
        if local_hun_version == 'nincs helyi verzio':
            id = 1
            local_hun_version = 'nincs helyi verziószám'
            if remote_hun_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az E2iPlayer magyarítás betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = 'Magyarítás  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                title = 'Magyarítás  (v' + remote_hun_version + ')  -  Telepítés szükséges'
        elif local_hun_version == 'ismeretlen verzió':
            id = 1
            if remote_hun_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az E2iPlayer magyarítás betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = 'Magyarítás  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                title = 'Magyarítás  (v' + remote_hun_version + ')  -  Telepítés szükséges'
        else:        
            try:
                lhv = float(local_hun_version)
                rhv = float(remote_hun_version)
                if lhv < rhv:
                    id = 2
                    title = 'Magyarítás  (v' + remote_hun_version + ')  -  Frissítés szükséges'
                    msg = ' frissítéséhez nyomd meg az OK gombot a távirányítón!'
                if lhv >= rhv:
                    id = 3
                    title = 'Magyarítás  (v' + remote_hun_version + ')'
                    msg = ' napra kész, nincs semmi teendő!'
            except Exception:
                id = 1
                title = 'Magyarítás  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az E2iPlayer magyarítás betöltését!\nNem javasolt a telepítés!!! Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
        desc = 'A magyarítás' + msg + '\n\nHelyi verzió szám:  ' + local_hun_version + '\nTávoli verzió szám:  ' + remote_hun_version
        params = {'category':'list_second', 'title': title, 'tab_id': 'magyaritas', 'azon': id, 'desc': desc}
        return params
        
    def getUrllistVersion_local(self):
        verzio = 'ismeretlen verzió'
        verzio_tmp = ''
        try:
            f = open(zlib.decompress(base64.b64decode('eJzTz0hJ0S8tysnJLC7RKy4pSk3MBQBGjAdY')), 'r')
            fl = f.readline()
            f.close
            if len(fl) == '': return verzio
            m = re.search(r'\d+.\d+',fl)
            if m is not None:
                verzio_tmp = m.group(0)
            if verzio_tmp == '':
                verzio = 'ismeretlen verzió'
            else:
                try:
                    verzio_float = float(verzio_tmp)
                    verzio = verzio_tmp
                except Exception:
                    verzio = 'ismeretlen verzió'
        except Exception:
            verzio = 'nincs helyi verzio'        
            printExc()
        return verzio
        
    def getUrllistVersion_remote(self):
        verzio = 'ismeretlen verzió'
        verzio_tmp = ''
        url = zlib.decompress(base64.b64decode('eJwFwUEKgDAMBMAfdcGjv4klmEBKS7IV9PXOGLnqBG6n7av1OaCHr5BX02axsDPCi5Ds5o9iSFGzfb5+uZcXNA=='))
        destination = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7Rq8osAAAzigZA'))
        destination_dir = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7RzU0sLkktAgBIcQd4'))
        unzip_command = ['unzip', '-q', '-o', destination, '-d', self.TEMP]
        if fileExists(destination):
            rm(destination)
            rmtree(destination_dir, ignore_errors=True)
        try:        
            if self.dflt(url,destination):
                if fileExists(destination):
                    if GetFileSize(destination) > 0:
                        if self._mycall(unzip_command) == 0:
                            filename = zlib.decompress(base64.b64decode('eJzTL8kt0C8tysnJLC7RzU0sLkktgnH1ikuKUhNzAedBDXA='))
                            if fileExists(filename):
                                try:
                                    f = open(filename, 'r')
                                    fl = f.readline()
                                    f.close
                                    if len(fl) == '': return verzio
                                    m = re.search(r'\d+.\d+',fl)
                                    if m is not None:
                                        verzio_tmp = m.group(0)
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
        
    def menuItemUrllist(self):
        msg = ''
        title = ''
        desc = ''
        id = 0
        params = dict()
        local_urllist_version = self.getUrllistVersion_local()
        remote_urllist_version = self.getUrllistVersion_remote()
        if local_urllist_version == 'nincs helyi verzio':
            id = 1
            local_urllist_version = 'nincs helyi verziószám'
            if remote_urllist_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az Urllist fájl telepítése betöltését!\nNem javasolt a telepítés!!!  Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = 'Urllist.stream  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.webhuplayer_dir.value + '/' + config.plugins.iptvplayer.webhuplayer_file.value
                title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Telepítés szükséges'
        elif local_urllist_version == 'ismeretlen verzió':
            id = 1
            if remote_urllist_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az Urllist fájl telepítése betöltését!\nNem javasolt a telepítés!!!  Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = 'Urllist.stream  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.webhuplayer_dir.value + '/' + config.plugins.iptvplayer.webhuplayer_file.value
                title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Telepítés szükséges'
        else:        
            try:
                lhv = float(local_urllist_version)
                rhv = float(remote_urllist_version)
                if lhv < rhv:
                    id = 2
                    title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Frissítés szükséges'
                    msg = ' frissítéséhez nyomd meg az OK gombot a távirányítón!'
                    msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.webhuplayer_dir.value + '/' + config.plugins.iptvplayer.webhuplayer_file.value
                if lhv >= rhv:
                    id = 3
                    title = 'Urllist.stream  (v' + remote_urllist_version + ')'
                    msg = ' napra kész, nincs semmi teendő!'
            except Exception:
                id = 1
                title = 'Urllist.stream  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az Urllist fájl telepítése betöltését!\nNem javasolt a telepítés!!!  Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
        desc = 'Az Urllist.stream ' + msg + '\n\nHelyi verzió szám:  ' + local_urllist_version + '\nTávoli verzió szám:  ' + remote_urllist_version
        params = {'category':'list_second', 'title': title, 'tab_id': 'urllist', 'azon': id, 'desc': desc}
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
        elif category == 'list_second':
            self.listSecondItems(self.currItem)
        else:
            printExc()
        CBaseHostClass.endHandleService(self, index, refresh)

class IPTVHost(CHostBase):

    def __init__(self):
        CHostBase.__init__(self, updatehosts(), True, [])
