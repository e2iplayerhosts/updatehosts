E2iPlayer HU telepítő host

Install:

~~~
wget --no-check-certificate https://github.com/e2iplayerhosts/updatehosts/archive/master.zip -q -O /tmp/updatehosts.zip
unzip -q -o /tmp/updatehosts.zip -d /tmp
cp -r -f /tmp/updatehosts-master/IPTVPlayer/* /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer
rm -r -f /tmp/updatehosts*
~~~

restart enigma2 GUI
