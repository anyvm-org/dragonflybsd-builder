How the images are built:

Each image in this repo's releases is built automatically in GitHub
Actions by `build.py`: it downloads the official DragonFly BSD installer
ISO, boots it in QEMU, runs the installation unattended, enables ssh,
pre-installs the packages listed in the conf, and exports the installed
disk as a compressed qcow2 image.

Upstream install media: the official DragonFly BSD ISOs from
https://mirror-master.dragonflybsd.org/iso-images/ (download page:
https://www.dragonflybsd.org/download/).
