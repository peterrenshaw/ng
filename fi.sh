#!/bin/sh
# ~*~ encoding: utf-8 ~*~

#---
# name: fi.sh
# date: 2013OCT27
# prog: pr
# desc: sick of typing in stuff, reduce to:
#           - sh fi.sh win32
#           - fi.sh *inux
# refs: <http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-2.html>
#---

# kill old install
echo '--- autobuild ---'
echo 'rm -fr *crap*'
rm -fr build distro ng.egg-info

# rebuild
echo 'python setup install'
python setup.py install

echo '--- ack ---'

# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
