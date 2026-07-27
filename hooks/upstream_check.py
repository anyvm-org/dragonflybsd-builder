#!/usr/bin/env python3
# Print the newest DragonFly BSD x86_64 _REL release version, e.g. "6.4.2".
# Empty output means "nothing detected" and is not an error; a non-zero exit
# means detection itself is broken (network error, HTTP error, or a page
# that no longer matches the expected shape) and must be reported by the
# caller, never swallowed. A failure must NEVER print a plausible-but-
# wrong version -- the version is only printed after every step below has
# succeeded.
#
# Source of truth: https://mirror-master.dragonflybsd.org/iso-images/
# (this is the exact host conf/dragonflybsd-*.conf's VM_ISO_LINK points at,
# e.g. ".../iso-images/dfly-x86_64-6.4.2_REL.iso").
#
# Fetched and confirmed by hand (2026-07-26): the directory is a plain
# Apache-style autoindex, one row per file, e.g.
#   <a href="dfly-x86_64-6.4.2_REL.iso">dfly-x86_64-6.4.2_REL.iso</a>  ... 748M
#   <a href="dfly-x86_64-6.4.2_REL.img">dfly-x86_64-6.4.2_REL.img</a>  ... 1.9G
#   <a href="dfly-x86_64-6.4.2_REL.iso.bz2">...</a>  ... 260M
# Both a bare .iso and a .iso.bz2 (and a raw .img/.img.bz2) exist for every
# release; the conf uses the bare .iso, so the pattern anchors on the exact
# ".iso" filename ending (not ".iso.bz2" or ".img"). The same listing also
# carries RELEASE CANDIDATE builds, e.g.
#   dfly-x86_64-6.0.0_RC1.iso.bz2
# which must never be picked -- the pattern requires the literal "_REL"
# marker (not "_RC<n>") right before the version's file extension, so a
# candidate build never matches. At fetch time the newest real release was
# 6.4.2 (2025-07-24), matching the current conf/dragonflybsd-6.4.2.conf.
#
# stdlib only (urllib.request, re, sys, os) -- no external dependencies.

import os
import re
import sys
import urllib.request

URL = "https://mirror-master.dragonflybsd.org/iso-images/"
TIMEOUT = 60
USER_AGENT = "anyvm-org-upstream-watcher/1.0"

# Only the bare "_REL.iso" file counts -- never "_REL.iso.bz2", "_REL.img",
# or a "_RC<n>" candidate build.
PATTERN = re.compile(r'href="dfly-x86_64-(\d+\.\d+\.\d+)_REL\.iso"')


def resolve_natural_key():
    """Return the engine's own natural_key, or fail loudly.

    watch.yml clones base-builder INTO the builder repo root, so at
    detection time it sits at "base-builder/" (relative to this hook's
    cwd, the builder repo root). A local checkout instead has it as a
    sibling, "../base-builder". Try both, in that order.

    There is deliberately NO local fallback copy. Ordering must be the
    single rule the engine uses -- a per-hook duplicate would have to be
    kept in sync by hand across every builder and would drift silently,
    and a hook that ranks versions differently from watch.py is worse
    than one that refuses to run. Both real contexts (CI and a local
    sibling checkout) always provide base-builder, so an ImportError here
    means the environment is wrong: report it as broken detection rather
    than guessing an order.
    """
    for candidate in ("base-builder", os.path.join("..", "base-builder")):
        if not os.path.isdir(candidate):
            continue
        path = os.path.abspath(candidate)
        if path not in sys.path:
            sys.path.insert(0, path)
        try:
            import gendata
            return gendata.natural_key
        except ImportError:
            continue
    raise ImportError(
        "base-builder/gendata.py not importable from %s; expected it at "
        "./base-builder (CI) or ../base-builder (local checkout)"
        % os.getcwd())


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.read().decode("utf-8", "replace")


def main():
    try:
        key = resolve_natural_key()
    except ImportError as e:
        sys.stderr.write("upstream_check: %s\n" % e)
        return 1
    try:
        html = fetch(URL)
    except Exception as e:
        sys.stderr.write("upstream_check: fetch of %s failed: %s\n"
                         % (URL, e))
        return 1
    versions = PATTERN.findall(html)
    if not versions:
        sys.stderr.write("upstream_check: no dfly-x86_64-*_REL.iso file "
                         "found in %s; page shape may have changed\n" % URL)
        return 1
    newest = sorted(set(versions), key=key)[-1]
    print(newest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
