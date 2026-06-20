

[![Build](https://github.com/anyvm-org/dragonflybsd-builder/actions/workflows/build.yml/badge.svg)](https://github.com/anyvm-org/dragonflybsd-builder/actions/workflows/build.yml)

Latest: v2.0.6


The image builder for `dragonflybsd`


All the supported releases are here:



| Release | x86_64(amd64)  |
|---------|---------|
| 6.4.0   |  ✅ (rsync,scp,nfs)     |
| 6.4.1   |  ✅ (rsync,scp,nfs)     |
| 6.4.2   |  ✅ (rsync,scp,nfs)     |

Note: sshfs is not offered on DragonFlyBSD -- the sshfs (FUSE) mount is
read-only in practice (the guest can read the shared dir, but writing a file
back into the mount fails), so only rsync / scp / nfs are listed.





How to build:

1. Use the [manual.yml](.github/workflows/manual.yml) to build manually.
   
    Run the workflow manually, you will get a view-only webconsole from the output of the workflow, just open the link in your web browser.
   
    You will also get an interactive VNC connection port from the output, you can connect to the vm by any vnc client.

2. Run the builder locally on your Ubuntu machine.

    Just clone the repo. and run:
    ```bash
    python3 build.py conf/dragonflybsd-6.4.2.conf
    ```
   
