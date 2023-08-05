shadowsocks-gtk
===============

A [ShadowSocks](https://github.com/clowwindy/shadowsocks) Client written with python-twisted and pygtk.

###Requirements:
* Debian/Ubuntu/LinuxMint:    
``sudo apt-get install python-twisted-core python-gtk2 python-m2crypto``

###Install and Run:  
* From pip:  
``sudo pip install shadowsocks-gtk``
``shadowsocks-gtk``
* From source:
``python shadowsocks_gtk/shadowsocks.py``

###Build deb packages:
    sudo apt-get install python-setuptools-git python-stdeb python-all build-essential
    python setup.py --command-packages=stdeb.command bdist_deb
    
![Screenshot](https://raw.github.com/apporc/shadowsocks-gtk/master/screenshot.png)


