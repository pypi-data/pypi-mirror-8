socle
=====

This is a simple yet modular SoC configuration utility, very much like
`raspi-config <http://elinux.org/RPi_raspi-config>`_ and others alike.
This one is written in Python and it aims to be extendable.
The name has no other meaning than it's a real word and it starts with SoC ;)


Features
--------

Preliminary support for following has been implemented:

* Configure hostname
* Configure timezone
* Configure wired/wireless network interfaces on Debian
* Switch off bells and whistles if it is used via UART


Boards
------

Following boards will be supported:

* Banana 
* Cubieboard2
* Cubietruck
* Raspberry Pi
* ZYBO
* Radxa

Short term goals
----------------

* Support u-boot configuration parsing, modifying
* Support /etc/modules parsing and modifying
* Support configuring of remote management clients like Puppet and Salt minion
* Support configuring VPN clients like OpenVPN and StrongSwan


Long term goals
---------------

* Support Debian adoption on SoC-s
* Support for generating root filesystem images using debootstrap/febootstrap/arch-bootstrap etc
* Support for managing PL bitstream files


Author
------

`Lauri Võsandi <lauri.vosandi@gmail.com>`_ is embedded systems student currently pursuing his
master degree at KTH.
I am usually present at #linux-sunxi and #linux-rockchip channels on Freenode IRC as *lauri*,
that's also my registered nick there ;)
