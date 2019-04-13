#!/bin/sh
echo "updatehosts.sh: start"
cp $1/iptvupdate/custom/updatehosts.sh $2/iptvupdate/custom/updatehosts.sh
status=$?
if [ $status -ne 0 ]; then
	echo "updatehosts.sh: Critical error. The $0 file can not be copied, error[$status]."
	exit 1
fi
cp $1/hosts/hostupdatehosts.py $2/hosts/
hosterr=$?
cp $1/icons/logos/updatehostslogo.png $2/icons/logos/
logoerr=$?
cp $1/icons/PlayerSelector/updatehosts*.png $2/icons/PlayerSelector/
iconerr=$?
if [ $hosterr -ne 0 ] || [ $logoerr -ne 0 ] || [ $iconerr -ne 0 ]; then
	echo "updatehosts.sh: copy error from source hosterr[$hosterr], logoerr[$logoerr, iconerr[$iconerr]"
fi
wget --no-check-certificate https://github.com/e2iplayerhosts/updatehosts/archive/master.zip -q -O /tmp/updatehosts.zip
if [ -s /tmp/updatehosts.zip ] ; then
	unzip -q -o /tmp/updatehosts.zip -d /tmp
	cp -r -f /tmp/updatehosts-master/IPTVPlayer/hosts/hostupdatehosts.py $2/hosts/
	hosterr=$?
	cp -r -f /tmp/updatehosts-master/IPTVPlayer/icons/* $2/icons/
	iconerr=$?
	if [ $hosterr -ne 0 ] || [ $iconerr -ne 0 ]; then
		echo "updatehosts.sh: copy error from updatehosts-master hosterr[$hosterr], iconerr[$iconerr]"
	fi
else
	echo "updatehosts.sh: updatehosts.zip could not be downloaded."
fi
rm -r -f /tmp/updatehosts*
echo "updatehosts.sh: exit 0"
exit 0