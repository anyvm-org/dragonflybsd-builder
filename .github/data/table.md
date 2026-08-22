

| Release | x86_64(amd64) |
|---------|---------|
| 6.4.2 | ✅ (rsync,scp,nfs,tar) |
| 6.4.1 | ✅ (rsync,scp,nfs,tar) |
| 6.4.0 | ✅ (rsync,scp,nfs,tar) |

<!-- arch-label: x86_64 = x86_64(amd64) -->
Note: sshfs is not offered on DragonFlyBSD -- the sshfs (FUSE) mount is
read-only in practice (the guest can read the shared dir, but writing a file
back into the mount fails), so only rsync / scp / nfs are listed.

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
