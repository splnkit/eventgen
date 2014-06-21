#!/usr/bin/env sh

~/Splunk/Dev/spl_egt/bin/splunk stop
rm -rf ~/Splunk/Dev/spl_egt/etc/apps/SA-Eventgen/*
cp -R ~/Dev/Tools/eventgen/* ~/Splunk/Dev/spl_egt/etc/apps/SA-Eventgen
#mv ~/Splunk/Dev/spl_egt/etc/apps/eventgen ~/Splunk/Dev/spl_egt/etc/apps/SA-Eventgen
~/Splunk/Dev/spl_egt/bin/splunk start

#wget -O splunk-6.1.1-207789-darwin-64.tgz 'http://www.splunk.com/page/download_track?file=6.1.1/splunk/osx/splunk-6.1.1-207789-darwin-64.tgz&ac=&wget=true&name=wget&platform=MacOS&architecture=x86_64&version=6.1.1&product=splunk&typed=release'