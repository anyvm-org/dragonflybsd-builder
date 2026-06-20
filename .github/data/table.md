

| Release | x86_64(amd64)  |
|---------|---------|
| 6.4.0   |  ✅ (rsync,scp,nfs)     |
| 6.4.1   |  ✅ (rsync,scp,nfs)     |
| 6.4.2   |  ✅ (rsync,scp,nfs)     |

Note: sshfs is not offered on DragonFlyBSD -- the sshfs (FUSE) mount is
read-only in practice (the guest can read the shared dir, but writing a file
back into the mount fails), so only rsync / scp / nfs are listed.

