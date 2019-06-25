# -*- coding: utf-8 -*-
###################################################
# 2019-06-26 by Alec - updatehosts HU host telepítő
###################################################
HOST_VERSION = "2.8"
###################################################
# LOCAL import
###################################################
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import TranslateTXT as _, SetIPTVPlayerLastHostError
from Plugins.Extensions.IPTVPlayer.components.ihost import CHostBase, CBaseHostClass
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG, printExc, byteify, rm, rmtree, mkdirs, DownloadFile, GetIPTVPlayerVerstion, GetBinDir, GetTmpDir, GetFileSize, MergeDicts, GetConfigDir, Which
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
from Components.config import config, ConfigText, ConfigYesNo, getConfigListEntry, configfile
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
config.plugins.iptvplayer.boxtipus = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.boxrendszer = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.hostmentes_dir = ConfigText(default = "/hdd", fixed_size = False)
config.plugins.iptvplayer.hostmentes_file = ConfigText(default = "hostbeallitasok.backup", fixed_size = False)
config.plugins.iptvplayer.b_urllist_dir = ConfigText(default = "/hdd", fixed_size = False)
config.plugins.iptvplayer.b_urllist_file = ConfigText(default = "urllist.stream", fixed_size = False)
config.plugins.iptvplayer.updatehosts_id = ConfigYesNo(default = False)
config.plugins.iptvplayer.autohu_rtlmost_login = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.autohu_rtlmost_password = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.autohu_id = ConfigYesNo(default = False)
config.plugins.iptvplayer.webhuplayer_dir = ConfigText(default = "/hdd/webhuplayer", fixed_size = False)
config.plugins.iptvplayer.webmedia_dir = ConfigText(default = "/hdd/webmedia", fixed_size = False)
config.plugins.iptvplayer.ytmedia_dir = ConfigText(default = "/hdd/ytmedia", fixed_size = False)
config.plugins.iptvplayer.webhuplayer_nezettseg = ConfigYesNo(default = False)
config.plugins.iptvplayer.m4sport_id = ConfigYesNo(default = False)
config.plugins.iptvplayer.mindigohu_login = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.mindigohu_password = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.mytvtelenorhu_login = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.mytvtelenorhu_password = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.rtlmosthu_login = ConfigText(default = "", fixed_size = False)
config.plugins.iptvplayer.rtlmosthu_password = ConfigText(default = "", fixed_size = False)

def GetConfigList():
    optionList = []
    optionList.append(getConfigListEntry("Set-top-Box típusa (például, Dreambox DM920):", config.plugins.iptvplayer.boxtipus))
    optionList.append(getConfigListEntry("Image típusa (például, openATV 6.x):", config.plugins.iptvplayer.boxrendszer))
    optionList.append(getConfigListEntry("Host beállítások mentési könyvtára:", config.plugins.iptvplayer.hostmentes_dir))
    optionList.append(getConfigListEntry("Host beállítások backup fájl neve:", config.plugins.iptvplayer.hostmentes_file))
    optionList.append(getConfigListEntry("Urllist könyvtár:", config.plugins.iptvplayer.b_urllist_dir))
    optionList.append(getConfigListEntry("Urllist fájl:", config.plugins.iptvplayer.b_urllist_file))
    optionList.append(getConfigListEntry("id:", config.plugins.iptvplayer.updatehosts_id))
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
        self.EHH = zlib.decompress(base64.b64decode('eJzTTy1J1k/Ny0zPTTTSBwAfugRt'))
        self.iphg = self.EHH + zlib.decompress(base64.b64decode('eJzLLCgpK8hJrEwtysgvLilOL8ovLSjWyyrOzwMAlt0LCg=='))
        self.ipudg = self.EHH + zlib.decompress(base64.b64decode('eJzLLCgpK8hJrEwtKi1OLUpJTcvMS01JL8ovLdDLKs7PAwDSYgz0'))
        self.vivn = GetIPTVPlayerVerstion()
        self.porv = self.gits()
        self.pbtp = '-'
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
        self.M4SPORT = zlib.decompress(base64.b64decode('eJzLNSkuyC8qAQAK3gLa'))
        self.VIDEA = zlib.decompress(base64.b64decode('eJwry0xJTQQABk4CCg=='))
        self.aid = config.plugins.iptvplayer.updatehosts_id.value
        self.aid_ki = ''
        self.btps = config.plugins.iptvplayer.boxtipus.value
        self.brdr = config.plugins.iptvplayer.boxrendszer.value
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
            #vszt = self.muves('1')
            if not self.ebbtit(): return
            if self.btps != '' and self.brdr != '': self.pbtp = self.btps.strip() + ' - ' + self.brdr.strip()
            n_hst = self.malvadst('1', '9', 'updatehosts_hostok')
            if n_hst != '' and self.aid:
                self.aid_ki = 'ID: ' + n_hst + '\n'
            else:
                self.aid_ki = ''
            msg_host = self.aid_ki + 'v' + HOST_VERSION + '  |  Magyar Hostok listája  -  telepítés, frissítés\n\nA hostok betöltése több időt vehet igénybe!  A letöltés ideje függ az internet sebességétől, illetve a gyűjtő oldal leterheltségétől is...\nVárd meg míg a hostok listája megjelenik. Ez eltarthat akár 1-2 percig is.\nA host gyűjtő oldalán néha hiba előfordulhat...'
            n_mgyr = self.malvadst('1', '9', 'updatehosts_magyaritas')
            if n_mgyr != '' and self.aid:
                self.aid_ki = 'ID: ' + n_mgyr + '\n'
            else:
                self.aid_ki = ''
            msg_magyar = self.aid_ki + 'Az E2iPlayer magyarítását lehet itt végrehajtani...'
            n_mbm = self.malvadst('1', '9', 'updatehosts_beall_ment')
            if n_mbm != '' and self.aid:
                self.aid_ki = 'ID: ' + n_mbm + '\n'
            else:
                self.aid_ki = ''
            msg_beall_ment = self.aid_ki + 'E2iPlayer magyar hostok beállításainak mentése/visszatöltése...'
            n_jav = self.malvadst('1', '9', 'updatehosts_javitas')
            if n_jav != '' and self.aid:
                self.aid_ki = 'ID: ' + n_jav + '\n'
            else:
                self.aid_ki = ''
            msg_javitas = self.aid_ki + 'Az E2iPlayer különböző hibáinak javítására nyilik itt lehetőség...\n(YouTube, parserek, egyéb belső fúnkciók)'
            n_hu_min = self.malvadst('1', '9', 'updatehosts_hu_minimal_fo')
            if n_hu_min != '' and self.aid:
                self.aid_ki = 'ID: ' + n_hu_min + '\n'
            else:
                self.aid_ki = ''
            msg_magyar_minimal = self.aid_ki + 'Az E2iPlayer "Magyar minimál stílus" beállítása...'
            n_bulst = self.malvadst('1', '9', 'updatehosts_burllist')
            if n_bulst != '' and self.aid:
                self.aid_ki = 'ID: ' + n_bulst + '\n'
            else:
                self.aid_ki = ''
            msg_urllist = self.aid_ki + 'Blindspot féle urllist.stream fájlt lehet itt telepíteni, frissíteni.\nA stream fájlt az "Urllists player" hosttal (Egyéb csoport) lehet lejátszani a Live streams menüpontban...\n\nA "WEB HU PLAYER" host használatát javasoljuk, mert hamarosan a tartalom csak ott lesz elérhető!!!'
            MAIN_CAT_TAB = [{'category': 'list_main', 'title': 'Magyar hostok telepítése, frissítése', 'tab_id': 'hostok', 'desc': msg_host},
                            {'category': 'list_main', 'title': 'Magyar hostok beállításainak mentése/visszatöltése', 'tab_id': 'beall_ment', 'desc': msg_beall_ment},
                            {'category': 'list_main', 'title': 'E2iPlayer magyarítása', 'tab_id': 'magyaritas', 'desc': msg_magyar},
                            {'category': 'list_main', 'title': 'E2iPlayer hibajavításai', 'tab_id': 'javitas', 'desc': msg_javitas},
                            {'category': 'list_main', 'title': 'Magyar minimál stílus', 'tab_id': 'magyar_minimal', 'desc': msg_magyar_minimal},
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
            elif tabID == 'beall_ment':
                self.Beall_ment(cItem)
            elif tabID == 'javitas':
                self.Javitas(cItem)
            elif tabID == 'magyar_minimal':
                self.Magyar_minimal(cItem)    
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
                self.susn('2', '9', 'updatehosts_hostok')
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
                HOST_CAT_TAB.append(self.menuItem(self.M4SPORT))
                HOST_CAT_TAB.append(self.menuItem(self.VIDEA))
                HOST_CAT_TAB = sorted(HOST_CAT_TAB, key=lambda i: (i['azon'], i['title']))
                self.listsTab(HOST_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def hostleirasa(self, host):
        ls = ''
        if host != '':
            if host == self.UPDATEHOSTS:
                ls = '\n(HU Telepítő keretrendszer, mely telepíti az itt lévő magyar hostokat)'
            if host == self.SONYPLAYER:
                ls = '\n(AXN, Viasat, SonyMAX, SonyMovie tartalmait jeleníti meg)'
            if host == self.MYTVTELENOR:
                ls = '\n(A Telenor MyTV tartalmait jeleníti meg. Regisztráció szükséges, de ingyenes tartalmak is elérhetők)'
            if host == self.RTLMOST:
                ls = '\n(A magyar RTLKLUB csatorna rtlmost.hu tartalmait jeleníti meg. Regisztráció szükséges)'
            if host == self.MINDIGO:
                ls = '\n(A mindiGO TV adásait jeleníti meg. Regisztráció szükséges)'
            if host == self.MOOVIECC:
                ls = '\n(A moovie.cc tartalmait jeleníti meg. Filmek és sorozatok minden mennyiségben)'
            if host == self.MOZICSILLAG:
                ls = '\n(A mozicsillag.me tartalmait jeleníti meg. Filmek és sorozatok minden mennyiségben)'
            if host == self.FILMEZZ:
                ls = '\n(A filmezz.eu tartalmait jeleníti meg. Filmek és sorozatok minden mennyiségben)'
            if host == self.WEBHUPLAYER:
                ls = '\n(Webes tartalmak (Filmek, Gasztro, TV csatornák, Időkép, Tájak, ...) Blindspot szerkesztésében, YouTube tartalmak megjelenítése)'
            if host == self.AUTOHU:
                ls = '\n(Magyar autós műsorakat jelenít meg - AUTOGRAM, GARAZS, SUPERCAR, TOTALCAR, FORMA1)'
            if host == self.M4SPORT:
                ls = '\n(Az m4sport.hu sport műsorait jeleníti meg - Boxutca, Magyar foci, UEFA Bajnokok Ligája foci, Sporthírek, Sportközvetítések)'
            if host == self.VIDEA:
                ls = '\n(A videa.hu videóit jeleníti meg különböző kategóriákban, csatornákban)'
        return ls
            
    def Magyaritas(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                self.susn('2', '9', 'updatehosts_magyaritas')
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
                self.susn('2', '9', 'updatehosts_javitas')
                n_yjt = self.malvadst('1', '9', 'updatehosts_yt_javitas')
                if n_yjt != '' and self.aid:
                    self.aid_ki = 'ID: ' + n_yjt + '\n'
                else:
                    self.aid_ki = ''
                msg_jav = self.aid_ki + '2019.04.24. | 2019.06.23.\n\nAz alábbi hibákra ad megoldást ez a javítás:\n"token" parameter not in video info,  "Encryption function name extraction failed!"\n\n(Csak egyszer kell végrehajtani, ha a hiba jelentkezik!)'
                HIBAJAV_CAT_TAB = [{'category': 'list_second', 'title': 'YouTube hiba javítása', 'tab_id': 'hibajav_youtube', 'desc': msg_jav}
                                  ]
                self.listsTab(HIBAJAV_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Magyar_minimal(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                self.susn('2', '9', 'updatehosts_hu_minimal_fo')
                n_mmsb = self.malvadst('1', '9', 'updatehosts_hu_minimal_beal')
                if n_mmsb != '' and self.aid:
                    self.aid_ki = 'ID: ' + n_mmsb + '\n'
                else:
                    self.aid_ki = ''
                msg_beallit = self.aid_ki + 'Az E2iPlayer a "Magyar minimál stílus" beállítással indul.\nCsak a "Magyar", "Felhasználó által meghatározott", "Összes" és "Konfiguráció" csoportok látszódnak.\nKönnyű és gyors használat a magyar tartalmakhoz...'
                n_mast = self.malvadst('1', '9', 'updatehosts_hu_minimal_alaph')
                if n_mast != '' and self.aid:
                    self.aid_ki = 'ID: ' + n_mast + '\n'
                else:
                    self.aid_ki = ''
                msg_visszaallit = self.aid_ki + 'Az E2iPlayer alapértelmezett indítási csoportjainak visszaállítása.\nA program telepítésekor létrejött "Alapértelmezett" csoportok jelennek meg!'
                MIN_CAT_TAB = [{'category': 'list_second', 'title': 'Magyar minimál stílus beállítása', 'tab_id': 'minimal_beallit', 'desc': msg_beallit},
                               {'category': 'list_second', 'title': 'Alapértelmezett stílus visszaállítása', 'tab_id': 'minimal_visszaallit', 'desc': msg_visszaallit}
                              ]
                self.listsTab(MIN_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Beall_ment(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                self.susn('2', '9', 'updatehosts_beall_ment')
                n_mmsb = self.malvadst('1', '9', 'updatehosts_beall_kiment')
                if n_mmsb != '' and self.aid:
                    self.aid_ki = 'ID: ' + n_mmsb + '\n'
                else:
                    self.aid_ki = ''
                msg_beallit = self.aid_ki + 'Az E2iPlayer host beállításainak a mentését lehet itt végrehajtani...\nCsak az azonos "HU Telepítő" keretrendszerrel készített backup fájlok paraméterei tölthetők vissza!'
                n_mast = self.malvadst('1', '9', 'updatehosts_beall_vissza')
                if n_mast != '' and self.aid:
                    self.aid_ki = 'ID: ' + n_mast + '\n'
                else:
                    self.aid_ki = ''
                msg_visszaallit = self.aid_ki + 'Az E2iPlayer host beállításainak a visszatöltését  lehet itt végrehajtani...   Bacukup fájlnak léteznie kell!\nCsak az azonos "HU Telepítő" keretrendszerhez tartozó backup fájlok paraméterei töltődnek vissza!\n\nElőször telepítsd vissza azokat a hostokat amiket idáig használtál, s utána futtasd a visszatöltést...'
                MEN_CAT_TAB = [{'category': 'list_second', 'title': 'Beállítások mentése', 'tab_id': 'beall_kiment', 'desc': msg_beallit},
                               {'category': 'list_second', 'title': 'Beállítások visszatöltése', 'tab_id': 'beall_vissza', 'desc': msg_visszaallit}
                              ]
                self.listsTab(MEN_CAT_TAB, cItem)
            else:
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            printExc()
            
    def Urllist_stream(self, cItem):
        try:
            valasz, msg = self._usable()
            if valasz:
                self.susn('2', '9', 'updatehosts_burllist')
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
                self.susn('2', '9', 'updatehosts_e2_magyaritas')
                self.hun_telepites()
            elif tabID == 'urllist':
                if self.cpve(config.plugins.iptvplayer.b_urllist_dir.value) and self.cpve(config.plugins.iptvplayer.b_urllist_file.value):
                    msg = 'A telepítés, frissítés helye:  ' + config.plugins.iptvplayer.b_urllist_dir.value + '/' + config.plugins.iptvplayer.b_urllist_file.value + '\nFolytathatom?'
                    msg += '\n\nHa máshova szeretnéd, akkor a KÉK gomb, majd az Oldal beállításai.\nAdatok megadása, s utána a ZÖLD gomb (Mentés) megnyomása!'
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        self.susn('2', '9', 'updatehosts_blind_urlist')
                        self.urllist_telepites()
                else:
                    msg = 'A KÉK gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa megfelelőek az előre beállított értékek, akkor ZÖLD gomb (Mentés) megnyomása!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            elif tabID == 'hibajav_youtube':
                self.susn('2', '9', 'updatehosts_yt_javitas')
                self.ytjv()
            elif tabID == 'minimal_beallit':
                self.susn('2', '9', 'updatehosts_hu_minimal_beal')
                self.mlmsbt()
            elif tabID == 'minimal_visszaallit':
                self.susn('2', '9', 'updatehosts_hu_minimal_alaph')
                self.mlvat()
            elif tabID == 'beall_kiment':
                self.ehbkmt()
            elif tabID == 'beall_vissza':
                self.ehbvts()
            elif tabID == self.UPDATEHOSTS:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.UPDATEHOSTS,True,False,'HU host telepítő, frissítő')
            elif tabID == self.SONYPLAYER:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.SONYPLAYER,True,True,'Sony Player HU')
            elif tabID == self.MYTVTELENOR:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.MYTVTELENOR,True,True,'https://mytv.telenor.hu/')
            elif tabID == self.RTLMOST:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.RTLMOST,True,True,'https://rtlmost.hu/')
            elif tabID == self.MINDIGO:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.MINDIGO,True,True,'https://tv.mindigo.hu/')
            elif tabID == self.MOOVIECC:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.MOOVIECC,True,False,'https://moovie.cc/')
            elif tabID == self.MOZICSILLAG:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.MOZICSILLAG,True,False,'https://mozicsillag.me/')
            elif tabID == self.FILMEZZ:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.FILMEZZ,True,False,'https://filmezz.eu/')
            elif tabID == self.WEBHUPLAYER:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.WEBHUPLAYER,True,False,'Web HU Player')
            elif tabID == self.AUTOHU:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.AUTOHU,True,False,'auto.HU')
            elif tabID == self.M4SPORT:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.M4SPORT,True,False,'https://www.m4sport.hu')
            elif tabID == self.VIDEA:
                self.susn('2', '9', 'host_' + tabID)
                self.host_telepites(self.VIDEA,True,False,'https://videa.hu')
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
                            dest_dir = config.plugins.iptvplayer.b_urllist_dir.value + '/' + config.plugins.iptvplayer.b_urllist_file.value
                            if mkdirs(config.plugins.iptvplayer.b_urllist_dir.value):
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
            
    def cfadbvt(self, vltz='', rtk=''):
        bv = False
        bvrtk = vltz
        try:
            if vltz != '' and rtk != '':
                if vltz == 'autohu_rtlmost_login':
                    config.plugins.iptvplayer.autohu_rtlmost_login.value = rtk
                    config.plugins.iptvplayer.autohu_rtlmost_login.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'autohu_rtlmost_password':
                    config.plugins.iptvplayer.autohu_rtlmost_password.value = rtk
                    config.plugins.iptvplayer.autohu_rtlmost_password.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'autohu_id':
                    if rtk in ['False','false','True','true']:
                        if rtk in ['False','false']:
                            config.plugins.iptvplayer.autohu_id.value = False
                        else:
                            config.plugins.iptvplayer.autohu_id.value = True
                        config.plugins.iptvplayer.autohu_id.save()
                        configfile.save()
                        bvrtk = ''
                        bv = True
                if vltz == 'webhuplayer_dir':
                    config.plugins.iptvplayer.webhuplayer_dir.value = rtk
                    config.plugins.iptvplayer.webhuplayer_dir.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'webmedia_dir':
                    config.plugins.iptvplayer.webmedia_dir.value = rtk
                    config.plugins.iptvplayer.webmedia_dir.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'ytmedia_dir':
                    config.plugins.iptvplayer.ytmedia_dir.value = rtk
                    config.plugins.iptvplayer.ytmedia_dir.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'webhuplayer_nezettseg':
                    if rtk in ['False','false','True','true']:
                        if rtk in ['False','false']:
                            config.plugins.iptvplayer.webhuplayer_nezettseg.value = False
                        else:
                            config.plugins.iptvplayer.webhuplayer_nezettseg.value = True
                        config.plugins.iptvplayer.webhuplayer_nezettseg.save()
                        configfile.save()
                        bvrtk = ''
                        bv = True
                if vltz == 'm4sport_id':
                    if rtk in ['False','false','True','true']:
                        if rtk in ['False','false']:
                            config.plugins.iptvplayer.m4sport_id.value = False
                        else:
                            config.plugins.iptvplayer.m4sport_id.value = True
                        config.plugins.iptvplayer.m4sport_id.save()
                        configfile.save()
                        bvrtk = ''
                        bv = True
                if vltz == 'mindigohu_login':
                    config.plugins.iptvplayer.mindigohu_login.value = rtk
                    config.plugins.iptvplayer.mindigohu_login.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'mindigohu_password':
                    config.plugins.iptvplayer.mindigohu_password.value = rtk
                    config.plugins.iptvplayer.mindigohu_password.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'mytvtelenorhu_login':
                    config.plugins.iptvplayer.mytvtelenorhu_login.value = rtk
                    config.plugins.iptvplayer.mytvtelenorhu_login.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'mytvtelenorhu_password':
                    config.plugins.iptvplayer.mytvtelenorhu_login.value = rtk
                    config.plugins.iptvplayer.mytvtelenorhu_login.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'rtlmosthu_login':
                    config.plugins.iptvplayer.rtlmosthu_login.value = rtk
                    config.plugins.iptvplayer.rtlmosthu_login.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                if vltz == 'rtlmosthu_password':
                    config.plugins.iptvplayer.rtlmosthu_password.value = rtk
                    config.plugins.iptvplayer.rtlmosthu_password.save()
                    configfile.save()
                    bvrtk = ''
                    bv = True
                return bv, bvrtk  
        except Exception:
            return False, bvrtk
            
    def pfmahr(self, ided='', idefw='', idef=''):
        encoding = 'utf-8'
        try:
            if ided != '' and idefw != '' and idef != '':
                if os.path.isdir(ided):
                    fpw = codecs.open(idefw, 'w', encoding, 'replace')
                else:
                    if mkdirs(ided): 
                        fpw = codecs.open(idefw, 'w', encoding, 'replace')
                    else:
                        msg = 'A Host beállítások mentési könyvtára nem hozható létre!\nA KÉK gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa megfelelőek az előre beállított értékek, akkor ZÖLD gomb (Mentés) megnyomása!'
                        self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
                        return True
                fpw.write("# HU Telepítő - v" + HOST_VERSION + "   |   Ne módosítsd ezt a fájlt!!!\n")
                if self.cpve(config.plugins.iptvplayer.autohu_rtlmost_login.value) or self.cpve(config.plugins.iptvplayer.autohu_rtlmost_password.value) or self.cpve(config.plugins.iptvplayer.autohu_id.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: autohu\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.autohu_rtlmost_login.value):
                        fpw.write("%s=%s\n" % ('autohu_rtlmost_login',config.plugins.iptvplayer.autohu_rtlmost_login.value))
                    if self.cpve(config.plugins.iptvplayer.autohu_rtlmost_password.value):
                        fpw.write("%s=%s\n" % ('autohu_rtlmost_password',config.plugins.iptvplayer.autohu_rtlmost_password.value))
                    if self.cpve(config.plugins.iptvplayer.autohu_id.value):
                        fpw.write("%s=%s\n" % ('autohu_id',config.plugins.iptvplayer.autohu_id.value))
                    fpw.write("\n")
                if self.cpve(config.plugins.iptvplayer.webhuplayer_dir.value) or self.cpve(config.plugins.iptvplayer.webmedia_dir.value) or self.cpve(config.plugins.iptvplayer.ytmedia_dir.value) or self.cpve(config.plugins.iptvplayer.webhuplayer_nezettseg.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: webhuplayer\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.webhuplayer_dir.value):
                        fpw.write("%s=%s\n" % ('webhuplayer_dir',config.plugins.iptvplayer.webhuplayer_dir.value))
                    if self.cpve(config.plugins.iptvplayer.webmedia_dir.value):
                        fpw.write("%s=%s\n" % ('webmedia_dir',config.plugins.iptvplayer.webmedia_dir.value))
                    if self.cpve(config.plugins.iptvplayer.ytmedia_dir.value):
                        fpw.write("%s=%s\n" % ('ytmedia_dir',config.plugins.iptvplayer.ytmedia_dir.value))
                    if self.cpve(config.plugins.iptvplayer.webhuplayer_nezettseg.value):
                        fpw.write("%s=%s\n" % ('webhuplayer_nezettseg',config.plugins.iptvplayer.webhuplayer_nezettseg.value))
                    fpw.write("\n")
                if self.cpve(config.plugins.iptvplayer.m4sport_id.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: m4sport\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.m4sport_id.value):
                        fpw.write("%s=%s\n" % ('m4sport_id',config.plugins.iptvplayer.m4sport_id.value))
                    fpw.write("\n")
                if self.cpve(config.plugins.iptvplayer.mindigohu_login.value) or self.cpve(config.plugins.iptvplayer.mindigohu_password.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: mindigo\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.mindigohu_login.value):
                        fpw.write("%s=%s\n" % ('mindigohu_login',config.plugins.iptvplayer.mindigohu_login.value))
                    if self.cpve(config.plugins.iptvplayer.mindigohu_password.value):
                        fpw.write("%s=%s\n" % ('mindigohu_password',config.plugins.iptvplayer.mindigohu_password.value))
                    fpw.write("\n")
                if self.cpve(config.plugins.iptvplayer.mytvtelenorhu_login.value) or self.cpve(config.plugins.iptvplayer.mytvtelenorhu_password.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: mytvtelenor\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.mytvtelenorhu_login.value):
                        fpw.write("%s=%s\n" % ('mytvtelenorhu_login',config.plugins.iptvplayer.mytvtelenorhu_login.value))
                    if self.cpve(config.plugins.iptvplayer.mytvtelenorhu_password.value):
                        fpw.write("%s=%s\n" % ('mytvtelenorhu_password',config.plugins.iptvplayer.mytvtelenorhu_password.value))
                    fpw.write("\n")
                if self.cpve(config.plugins.iptvplayer.rtlmosthu_login.value) or self.cpve(config.plugins.iptvplayer.rtlmosthu_password.value):
                    fpw.write("##################################################\n")
                    fpw.write("# HOST: rtlmost\n")
                    fpw.write("##################################################\n")
                    if self.cpve(config.plugins.iptvplayer.rtlmosthu_login.value):
                        fpw.write("%s=%s\n" % ('rtlmosthu_login',config.plugins.iptvplayer.rtlmosthu_login.value))
                    if self.cpve(config.plugins.iptvplayer.rtlmosthu_password.value):
                        fpw.write("%s=%s\n" % ('rtlmosthu_password',config.plugins.iptvplayer.rtlmosthu_password.value))
                    fpw.write("\n")
                fpw.flush()
                os.fsync(fpw.fileno())
                fpw.close()
                os.rename(idefw, ided + '/' + idef)
                if fileExists(idefw):
                    rm(idefw)
                return False
            else:
                return True
        except Exception:
            if fileExists(idefw):
                rm(idefw)
            return True
        
    def ehbvts(self):
        hiba = False
        nsk = False
        msg = ''
        hpsz = ''
        tmb = []
        encoding = 'utf-8'
        try:
            if self.cpve(config.plugins.iptvplayer.hostmentes_dir.value) and self.cpve(config.plugins.iptvplayer.hostmentes_file.value):
                ided = config.plugins.iptvplayer.hostmentes_dir.value
                idef = config.plugins.iptvplayer.hostmentes_file.value
                if ided != '' and ided.endswith('/'):
                    ided = ided[:-1]
                idefp = ided + '/' + idef.strip()
                try:
                    if fileExists(idefp):
                        self.susn('2', '9', 'updatehosts_beall_vissza')
                        with codecs.open(idefp, 'r', encoding, 'replace') as fpr:
                            data = fpr.read()
                        if len(data) > 0:
                            if type(data) == type(u''): data = data.encode('utf-8', 'replace')
                            data = self.cm.ph.getAllItemsBeetwenMarkers(data, '###', '\n\n', False)
                            if len(data) > 0:
                                for item in data:
                                    tstm = item.split('\n')
                                    if len(tstm) > 2:
                                        if len(tstm[1]) > 0:
                                            if '# HOST:' in tstm[1]:
                                                hn = tstm[1].replace('# HOST:','').strip()
                                                if fileExists(self.IH + self.HS + '/host' + hn + '.py'):
                                                    for it in tstm:
                                                        if it == '' or it == '\n' or it.startswith('#'):
                                                            continue
                                                        tit = it.replace('/n','').strip()
                                                        ltp = tit.find('=')
                                                        if -1 < ltp:
                                                            try:
                                                                tit_k = tit[:ltp].strip()
                                                                tit_v = tit[ltp+1:].strip()
                                                                if tit_k == '' and tit_v == '': continue
                                                                skr, bvrtk = self.cfadbvt(tit_k,tit_v)
                                                                if not skr:
                                                                    hpsz = hpsz + ',  ' + bvrtk
                                                                    nsk = True
                                                            except Exception:
                                                                continue
                                                        else:
                                                            hpsz = hpsz + ', ' + tit
                                                            nsk = True
                                                            continue
                                                else:
                                                    continue
                                            else:
                                                continue
                                        else:
                                            continue
                                    else:
                                        continue
                            else:
                                hiba = True
                        else:
                            hiba = True
                        if hiba:
                            if msg == '':
                                msg = 'Hiba: 701 - Nemsikerült a Beállítások visszatöltése!'
                            title = 'A Beállítások visszatöltése nemsikerült!'
                            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
                        else:
                            if nsk:
                                if hpsz.startswith(','): hpsz = hpsz[3:]
                                szvg = 'Hiba ezeknél a soroknál:  ' + hpsz
                                msg = 'Hibás visszatöltés!!!\n\nVárj, mindjárt megtudod, hogy hol található a hiba...'
                                title = 'A Beállítások visszatöltése végrehajtva - Hibák vannak'
                                desc = 'Hibásak a ' + ided.replace('/',' / ').strip() + ' / ' + idef.strip() + ' fájlban lévő egyes paraméterek!\n\nNézd át és javítsd ki azokat, majd futtasd ismét a "Beállítások visszatöltése"-t!  Ha ezeket nem teszed meg az hibás működést eredményez!!!\nNyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón és javítsd ki a hibát.\n\n' + szvg
                                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 10 )
                            else:
                                szvg = ''
                                msg = 'Sikerült a Beállítások visszatöltése!\n' + szvg + '\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                                title = 'A Beállítások visszatöltése végrehajtva'
                                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszatöltés!!!'
                                try:
                                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                                    if ret[0]:
                                        try:
                                            desc = 'A kezelőfelület most újraindul...'
                                            quitMainloop(3)
                                        except Exception:
                                            msg = 'Hiba: 702 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszatöltés!!!'
                                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                                except Exception:
                                    msg = 'Hiba: 703 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszatöltés!!!'
                                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                    else:
                        desc = 'A backup fájl nem található itt:   ' + ided.replace('/',' / ').strip() + ' / ' + idef.strip() + '\n\nHiányzik a fájl, vagy rossz az Oldal beállítás (KÉK gomb)!\nNyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                        title = 'Beállítások visszatöltése nemsikerült'
                except Exception:
                    title = 'Hiba: 705 - A Beállítások visszatöltése nemsikerült!'
                    desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                params = dict()
                params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'beall_vissza', 'desc': desc})
                self.addDir(params)
            else:
                msg = 'Nem sikerült a beállítások visszatöltése!\n\nA KÉK gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa megfelelőek az előre beállított értékek, akkor ZÖLD gomb (Mentés) megnyomása!'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            msg = 'Nem sikerült a beállítások visszatöltése!'
            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        
    def ehbkmt(self):
        msg = ''
        encoding = 'utf-8'
        try:
            if self.cpve(config.plugins.iptvplayer.hostmentes_dir.value) and self.cpve(config.plugins.iptvplayer.hostmentes_file.value):
                ided = config.plugins.iptvplayer.hostmentes_dir.value
                idef = config.plugins.iptvplayer.hostmentes_file.value
                if ided != '' and ided.endswith('/'):
                    ided = ided[:-1]
                idefw = ided + '/' + idef + '.writing'
                msg = 'A mentés helye:  ' + ided.replace('/',' / ').strip() + ' / ' + idef.strip() + '\nFolytathatom?'
                msg += '\n\nHa máshova szeretnéd, akkor itt nem - utána KÉK gomb, majd az Oldal beállításai.\nOtt az adatok megadása, s utána a ZÖLD gomb (Mentés) megnyomása!'
                ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                if ret[0]:
                    self.susn('2', '9', 'updatehosts_beall_kiment')
                    if not self.pfmahr(ided, idefw, idef):
                        desc = 'A mentés sikerült!  A backup fájl itt található:  ' + ided.replace('/',' / ').strip() + ' / ' + idef.strip() + '\n\nNyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                        title = 'Beállítások mentése - sikerült'
                        params = dict()
                        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'beall_kiment', 'desc': desc})
                        self.addDir(params)
                    else:
                        if fileExists(idefw):
                            rm(idefw)
                        desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                        title = 'Beállítások mentése nemsikerült'
                        params = dict()
                        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'beall_kiment', 'desc': desc})
                        self.addDir(params)
                else:
                    desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                    title = 'Beállítások mentése'
                    params = dict()
                    params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'beall_kiment', 'desc': desc})
                    self.addDir(params)
            else:
                msg = 'Nem sikerült a beállítások mentése!\n\nA KÉK gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa megfelelőek az előre beállított értékek, akkor ZÖLD gomb (Mentés) megnyomása!'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            msg = 'Nem sikerült a beállítások mentése!'
            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        
    def mlvat(self):
        hiba = False
        msg = ''
        fnb = self.iphg
        fnu = self.ipudg
        try:
            if fileExists(fnb + '.bak'):
                try:
                    if self._mycopy(fnb + '.bak',fnb):
                        if fileExists(fnb):
                            if GetFileSize(fnb) > 0:
                                if fileExists(fnu + '.bak'):
                                    if self._mycopy(fnu + '.bak',fnu):
                                        if fileExists(fnu):
                                            if GetFileSize(fnu) > 0:
                                                hiba = False
                                            else:
                                                hiba = True
                                                msg = 'Hiba: 501 - A visszaállított fájl üres'    
                                        else:
                                            hiba = True
                                            msg = 'Hiba: 502 - Nem létezik a visszaállított fájl'    
                                    else:
                                        hiba = True
                                        msg = 'Hiba: 503 - Nem sikerült a visszaállítás másolása'
                                else:
                                    if fileExists(fnu):
                                        rm(fnu)
                                    hiba = False
                            else:
                                hiba = True
                                msg = 'Hiba: 504 - A visszaállított fájl üres'    
                        else:
                            hiba = True
                            msg = 'Hiba: 505 - Nem létezik a visszaállított fájl'    
                    else:
                        hiba = True
                        msg = 'Hiba: 506 - Nem sikerült a visszaállítás másolása'
                    if hiba:
                        if msg == '':
                            msg = 'Hiba: 507 - Nem sikerült a visszaállítás!'
                        title = 'Az Alapértelmezett stílus visszaállítása nemsikerült!'
                        desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                        self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
                    else:
                        msg = 'Sikerült az Alapértelmezett stílus visszaállítása!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                        title = 'Az Alapértelmezett stílus visszaállítása végrehajtva'
                        desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszaállítás!!!'
                        try:
                            ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                            if ret[0]:
                                try:
                                    desc = 'A kezelőfelület most újraindul...'
                                    quitMainloop(3)
                                except Exception:
                                    msg = 'Hiba: 508 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszaállítás!!!'
                                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                        except Exception:
                            msg = 'Hiba: 509 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a visszaállítás!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    title = 'Az Alapértelmezett stílus visszaállítása nemsikerült!'
                    desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                    printExc()
                params = dict()
                params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'minimal_visszaallit', 'desc': desc})
                self.addDir(params)
            else:
                msg = 'Nincs mit visszaállítani!\nCsak a "Magyar minimál stílus" csoportosítását lehet visszaállítani\naz Alapértelmezett csoportosításra.'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
        except Exception:
            msg = 'Nincs mit visszaállítani!\nCsak a "Magyar minimál stílus" csoportosítását lehet visszaállítani\naz Alapértelmezett csoportosításra.'
            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            
    def mlmsbt(self):
        encoding = 'utf-8'
        hiba = False
        msg = ''
        fnb = self.iphg
        fnbw = self.iphg + '.writing'
        fnu = self.ipudg
        try:
            if self.cfnbbak(fnb):
                if fileExists(fnb + '.bak'):
                    if GetFileSize(fnb + '.bak') > 0:
                        try:
                            datsz = {"disabled_groups": ["moviesandseries", "cartoonsandanime", "music", "sport", "live", "documentary", "science", "polish", "english", "german", "french", "russian", "arabic", "greek", "latino", "italian", "swedish", "balkans", "others"], "version": 0, "groups": [{"name": "hungarian"}, {"name": "userdefined"}]}
                            datsz = json_dumps(datsz)
                            fpw = codecs.open(fnbw, 'w', encoding, 'replace')
                            fpw.write(datsz)
                            fpw.flush()
                            os.fsync(fpw.fileno())
                            fpw.close()
                            os.rename(fnbw, self.iphg)
                        except Exception:
                            if fileExists(fnbw):
                                rm(fnbw)
                            hiba = True
                            msg = 'Hiba: 601 - A magyar minimál stílus beállítása nem sikerült!'
                        finally:
                            if fileExists(fnbw):
                                rm(fnbw)
                        if not hiba and not fileExists(fnu):
                            try:
                                datszm = {"disabled_hosts": [], "version": 0, "hosts": ["favourites", "localmedia", "urllist"]}
                                datszm = json_dumps(datszm)
                                with codecs.open(self.ipudg, 'w', encoding, 'replace') as fuw:
                                    fuw.write(datszm)
                                hiba = False
                            except Exception:    
                                hiba = True
                                msg = 'Hiba: 602 - A user fájl írása nem sikerült!' 
                                if fileExists(self.ipudg):
                                    rm(self.ipudg)
                    else:
                        hiba = True
                        msg = 'Hiba: 603 - A magyar minimál stílus beállítása nem sikerült!'    
                else:
                    hiba = True
                    msg = 'Hiba: 604 - A magyar minimál stílus beállítása nem sikerült!'    
            else:
                hiba = True
                msg = 'Hiba: 605 - A magyar minimál stílus beállítása nem sikerült!'
            if hiba:
                if msg == '':
                    msg = 'Hiba: 607 - A magyar minimál stílus beállítása nem sikerült!'
                title = 'A Magyar minimál stílus beállítása nemsikerült!'
                desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_ERROR, timeout = 20 )
            else:
                msg = 'Sikerült a Magyar minimál stílus beállítása!\n\nKezelőfelület újraindítása szükséges. Újraindítsam most?'
                title = 'A Magyar minimál stílus beállítása végrehajtva'
                desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a Magyar minimál stílus beállítás!!!'
                try:
                    ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                    if ret[0]:
                        try:
                            desc = 'A kezelőfelület most újraindul...'
                            quitMainloop(3)
                        except Exception:
                            msg = 'Hiba: 608 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                            desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a Magyar minimál stílus beállítás!!!'
                            self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
                except Exception:
                    msg = 'Hiba: 609 - Nem sikerült az újraindítás. Indítsd újra a Kezelőfelületet manuálisan!'
                    desc = 'Nyomd meg a Kilépés gombot!  -  PIROS gomb a távirányítón,\n\nmajd Kezelőfelület újraindítása, vagy reboot.  =>  Meg kell tenni ezt, mert csak így sikeres a Magyar minimál stílus beállítás!!!'
                    self.sessionEx.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout = 15 )
        except Exception:
            title = 'A Magyar minimál stílus beállítása nemsikerült!'
            desc = 'Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
            printExc()
        params = dict()
        params.update({'good_for_fav': False, 'category': 'list_second', 'title': title, 'tab_id': 'minimal_beallit', 'desc': desc})
        self.addDir(params)
        
    def cfnbbak(self, fnb=''):
        skt = False
        encoding = 'utf-8'
        try:
            if fnb != '':
                datsz = {"disabled_groups": [], "version": 0, "groups": [{"name": "hungarian"}, {"name": "userdefined"}, {"name": "moviesandseries"}, {"name": "cartoonsandanime"}, {"name": "music"}, {"name": "sport"}, {"name": "live"}, {"name": "documentary"}, {"name": "science"}, {"name": "polish"}, {"name": "english"}, {"name": "german"}, {"name": "french"}, {"name": "russian"}, {"name": "arabic"}, {"name": "greek"}, {"name": "latino"}, {"name": "italian"}, {"name": "swedish"}, {"name": "balkans"}, {"name": "others"}]}
                datsz = json_dumps(datsz)
                with codecs.open(fnb + '.bak', 'w', encoding, 'replace') as fuw:
                    fuw.write(datsz)
                skt = True
            return skt
        except Exception:
            skt = False
            return skt
        
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
        
    def muves(self, i_md=''):
        uhe = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUL0stTtQvS8wD0SlJegUZBQAQzBQG'))
        pstd = {'md':i_md}
        vzt = {}
        try:
            if i_md != '':
                sts, data = self.cm.getPage(uhe, self.defaultParams, pstd)
                if not sts: return vzt
                if len(data) == 0: return vzt
                data = self.cm.ph.getDataBeetwenMarkers(data, '<div id="div_a_div', '</div>')[1]
                if len(data) == 0: return vzt
                data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<input', '/>')
                if len(data) == 0: return vzt
                for item in data:
                    t_i = self.cm.ph.getSearchGroups(item, 'id=[\'"]([^"^\']+?)[\'"]')[0]
                    t_v = self.cm.ph.getSearchGroups(item, 'value=[\'"]([^"^\']+?)[\'"]')[0]
                    if t_i != '' and t_v != '':
                        vzt[t_i] = t_v
            return vzt
        except Exception:
            return vzt
            
    def malvadst(self, i_md='', i_hgk='', i_mpu=''):
        uhe = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUL04sSdQvS8wD0ilJegUZBQD8FROZ'))
        pstd = {'md':i_md, 'hgk':i_hgk, 'mpu':i_mpu }
        t_s = ''
        temp_vn = ''
        temp_vni = ''
        try:
            if i_md != '' and i_hgk != '' and i_mpu != '':
                sts, data = self.cm.getPage(uhe, self.defaultParams, pstd)
                if not sts: return t_s
                if len(data) == 0: return t_s
                data = self.cm.ph.getDataBeetwenMarkers(data, '<div id="div_a_div', '</div>')[1]
                if len(data) == 0: return t_s
                data = self.cm.ph.getAllItemsBeetwenMarkers(data, '<input', '/>')
                if len(data) == 0: return t_s
                for item in data:
                    t_i = self.cm.ph.getSearchGroups(item, 'id=[\'"]([^"^\']+?)[\'"]')[0]
                    if t_i == 'vn':
                        temp_vn = self.cm.ph.getSearchGroups(item, 'value=[\'"]([^"^\']+?)[\'"]')[0]
                    elif t_i == 'vni':
                        temp_vni = self.cm.ph.getSearchGroups(item, 'value=[\'"]([^"^\']+?)[\'"]')[0]
                if temp_vn != '':
                    t_s = temp_vn
            return t_s
        except Exception:
            return t_s
        
    def susn(self, i_md='', i_hgk='', i_mpu=''):
        uhe = zlib.decompress(base64.b64decode('eJzLKCkpsNLXLy8v10vLTK9MzclNrSpJLUkt1sso1c9IzanUL04sSdQvS8wD0ilJegUZBQD8FROZ'))
        pstd = {'md':i_md, 'hgk':i_hgk, 'mpu':i_mpu, 'hv':self.vivn, 'orv':self.porv, 'bts':self.pbtp}
        try:
            if i_md != '' and i_hgk != '' and i_mpu != '':
                sts, data = self.cm.getPage(uhe, self.defaultParams, pstd)
            return
        except Exception:
            return
            
    def gits(self):
        bv = '-'
        tt = []
        try:
            if fileExists(zlib.decompress(base64.b64decode('eJzTTy1J1s8sLi5NBQATXQPE'))):
                fr = open(zlib.decompress(base64.b64decode('eJzTTy1J1s8sLi5NBQATXQPE')),'r')
                for ln in fr:
                    ln = ln.rstrip('\n')
                    if ln != '':
                        tt.append(ln)
                fr.close()
                if len(tt) == 1:
                    bv = tt[0].strip()[:-6].capitalize()
                if len(tt) == 2:
                    bv = tt[1].strip()[:-6].capitalize()
            return bv
        except:
            return '-'
        
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
        hl = ''
        id = 0
        if host == self.UPDATEHOSTS:
            host_title = 'HU Telepítő keretrendszer'
        else:
            host_title = host
        hl = self.hostleirasa(host)
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
        n_hst = self.malvadst('1', '9', 'host_' + host)
        if n_hst != '' and self.aid:
            self.aid_ki = 'ID: ' + n_hst + '\n'
        else:
            self.aid_ki = ''
        desc = self.aid_ki + host + msg + hl + '\n\nHelyi verzió szám:  ' + local_host_version + '\nTávoli verzió szám:  ' + remote_host_version
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
        
    def ebbtit(self):
        try:
            if '' == self.btps.strip() or '' == self.brdr.strip():
                msg = 'A Set-top-Box típusát és a használt rendszer (image) nevét egyszer meg kell adni!\n\nA kompatibilitás és a megfelelő használat miatt kellenek ezek az adatok a programnak.\nKérlek, a helyes működéshez a valóságnak megfelelően írd be azokat.\n\nA KÉK gomb, majd az Oldal beállításai segítségével megadhatod a kért adatokat.\nHa ott beírtad az értékeket, akkor ZÖLD gomb (Mentés) megnyomása!\n\nKilépek innen és utána megnyomom a KÉK gombot?'
                ret = self.sessionEx.waitForFinishOpen(MessageBox, msg, type=MessageBox.TYPE_YESNO, default=True)
                return False
            else:
                return True
        except Exception:
            return False
        
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
        n_hst = self.malvadst('1', '9', 'updatehosts_e2_magyaritas')
        if n_hst != '' and self.aid:
            self.aid_ki = 'ID: ' + n_hst + '\n'
        else:
            self.aid_ki = ''
        desc = self.aid_ki + 'A magyarítás' + msg + '\n\nHelyi verzió szám:  ' + local_hun_version + '\nTávoli verzió szám:  ' + remote_hun_version
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
                msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.b_urllist_dir.value + '/' + config.plugins.iptvplayer.b_urllist_file.value
                title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Telepítés szükséges'
        elif local_urllist_version == 'ismeretlen verzió':
            id = 1
            if remote_urllist_version == 'ismeretlen verzió':
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az Urllist fájl telepítése betöltését!\nNem javasolt a telepítés!!!  Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
                title = 'Urllist.stream  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
            else:
                msg = ' telepítéséhez nyomd meg az OK gombot a távirányítón!'
                msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.b_urllist_dir.value + '/' + config.plugins.iptvplayer.b_urllist_file.value
                title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Telepítés szükséges'
        else:        
            try:
                lhv = float(local_urllist_version)
                rhv = float(remote_urllist_version)
                if lhv < rhv:
                    id = 2
                    title = 'Urllist.stream  (v' + remote_urllist_version + ')  -  Frissítés szükséges'
                    msg = ' frissítéséhez nyomd meg az OK gombot a távirányítón!'
                    msg += '\nA telepítés, frissítés helye:  ' + config.plugins.iptvplayer.b_urllist_dir.value + '/' + config.plugins.iptvplayer.b_urllist_file.value
                if lhv >= rhv:
                    id = 3
                    title = 'Urllist.stream  (v' + remote_urllist_version + ')'
                    msg = ' napra kész, nincs semmi teendő!'
            except Exception:
                id = 1
                title = 'Urllist.stream  (ismeretlen verzió)  -  Ismételt ellenörzés szükséges'
                msg = ' távoli verzió száma nem érhető el!  Próbáld meg ismét az Urllist fájl telepítése betöltését!\nNem javasolt a telepítés!!!  Nyomd meg a Vissza gombot!  -  EXIT / BACK gomb a távirányítón'
        n_hst = self.malvadst('1', '9', 'updatehosts_blind_urlist')
        if n_hst != '' and self.aid:
            self.aid_ki = 'ID: ' + n_hst + '\n'
        else:
            self.aid_ki = ''
        desc = self.aid_ki + 'Az Urllist.stream ' + msg + '\n\nHelyi verzió szám:  ' + local_urllist_version + '\nTávoli verzió szám:  ' + remote_urllist_version
        params = {'category':'list_second', 'title': title, 'tab_id': 'urllist', 'azon': id, 'desc': desc}
        return params
    
    def handleService(self, index, refresh = 0, searchPattern = '', searchType = ''):
        CBaseHostClass.handleService(self, index, refresh, searchPattern, searchType)
        name     = self.currItem.get("name", '')
        category = self.currItem.get("category", '')
        mode     = self.currItem.get("mode", '')
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
