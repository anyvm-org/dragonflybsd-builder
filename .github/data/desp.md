How the images are built:

Each image is built automatically in the
[anyvm-org/dragonflybsd-builder](https://github.com/anyvm-org/dragonflybsd-builder)
repo's GitHub Actions: it downloads the official DragonFly BSD installer
ISO, boots it in QEMU, runs the installation unattended, enables ssh,
pre-installs the packages listed in the conf, and exports the installed
disk as a compressed qcow2 image.

Upstream install media: the official DragonFly BSD ISOs from
https://mirror-master.dragonflybsd.org/iso-images/ (download page:
https://www.dragonflybsd.org/download/).
