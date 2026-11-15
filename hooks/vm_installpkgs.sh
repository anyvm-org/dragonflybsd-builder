# In-guest install script for dragonflybsd (piped into the guest sh by
# build.py with ANYVM_PKGS prepended; runs under set -e, so a failed upgrade
# fails the build instead of shipping a half-upgraded image).
#
# The 6.4.x ISOs ship packages (openssl, curl, git-lite, ...) built against
# the dports of their release date. dports later moved security/openssl from
# 3.0 to 3.5 (libssl.so.12 -> .17, 2026-11), and a package records its
# openssl dependency by name only, so a plain `pkg install rsync` pulls an
# rsync that needs libcrypto.so.17 but keeps the old openssl -- rsync then
# cannot start. Upgrade everything first so the image ships one consistent
# package set.
pkg upgrade -y
pkg install -y $ANYVM_PKGS
