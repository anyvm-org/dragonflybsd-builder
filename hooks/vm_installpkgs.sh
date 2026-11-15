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
#
# The 6.4.0 ISO ships pkg 1.14.4, which names the catalogue after meta.conf's
# packing_format and asks for packagesite.txz. dports stopped publishing that
# file (2026-11, only packagesite.pkg is left), so this pkg cannot update at
# all -- postBuild's `pkg install -y pkg` fails the same way. The packages
# themselves are still xz, so the old pkg-static can install the current pkg
# straight from All/ of the Avalon repo; the new pkg reads the catalogue.
case "$(pkg -v)" in
1.*)
  _all="https://mirror-master.dragonflybsd.org/dports/$(pkg config ABI)/LATEST/All"
  # Anchor on the href quotes: a bare pkg-<ver> also matches the tail of
  # names like py312-buildbot-pkg-4.3.0.pkg.
  _pkg=$(fetch -qo - "$_all/" | grep -o '"pkg-[0-9][^"]*\.pkg"' | tr -d '"' | sort -u | tail -1)
  if [ -z "$_pkg" ]; then
    echo "no pkg package found in $_all/" >&2
    exit 1
  fi
  pkg-static add -f "$_all/$_pkg"
  ;;
esac
pkg upgrade -y
pkg install -y $ANYVM_PKGS
