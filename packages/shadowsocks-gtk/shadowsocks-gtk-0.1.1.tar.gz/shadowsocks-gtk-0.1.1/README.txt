shadowsocks-gtk
===============

A [ShadowSocks](https://github.com/clowwindy/shadowsocks) Client written with python-twisted and pygtk.

Requirements:
Debian/Ubuntu/LinuxMint:    
    sudo apt-get python-twisted-core python-gtk2 python-m2crypto

Install and Run:  
From pip:  
    sudo pip install shadowsocks-gtk
    shadowsocks-gtk
From source:
    python shadowsocks_gtk/shadowsocks.py

Build deb packages:
    sudo apt-get install setuptools-git python-stdeb
    python setup.py --command-packages=stdeb.command bdist_deb
    
