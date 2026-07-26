<!-- arch-label: x86_64 = x86_64(amd64) -->
Note: sshfs is not offered on DragonFlyBSD -- the sshfs (FUSE) mount is
read-only in practice (the guest can read the shared dir, but writing a file
back into the mount fails), so only rsync / scp / nfs are listed.
