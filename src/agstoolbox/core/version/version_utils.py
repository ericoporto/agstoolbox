from __future__ import annotations

from agstoolbox.core.version.version import Version


def tag_to_version_str(tag: str) -> str:
    tks = tag.split(".")
    if len(tks) <= 2 or len(tks) > 5:
        return tag

    first_tk = 0
    if (tks[0][0] == 'v' and len(tks[0]) <= 2) or tks[0] == "version":
        first_tk = 1

    major = tks[first_tk].strip()
    minor = tks[first_tk+1].strip()
    improv = tks[first_tk+2].strip()
    patch = tks[first_tk+3].strip()

    return major + "." + minor + "." + improv + "." + patch


def tag_to_family(tag: str) -> str:
    tks = tag.split(".")
    if len(tks) <= 1 or len(tks) > 5:
        return tag

    first_tk = 0
    if tks[0] == "v":
        first_tk = 1

    major = tks[first_tk]
    minor = tks[first_tk+1]

    family = major + "." + minor
    return family


def family_to_major(family: str) -> str:
    tks = family.split(".")
    if len(tks) <= 1 or len(tks) >= 3:
        return family

    return tks[0]


def family_to_minor(family: str) -> str:
    tks = family.split(".")
    if len(tks) <= 1 or len(tks) >= 3:
        return family

    return tks[1]


def version_to_family(version: str) -> str:
    return tag_to_family(version)


def version_str_to_int(version: str) -> int:
    v = tag_to_version_str(version)

    tks = v.split(".")
    tks_count = len(tks)
    if tks_count > 4 or tks_count <= 2:
        return -1

    version_as_int = 0
    for i in range(tks_count):
        tk = tks[i]
        tk_val = 0
        try:
            tk_val = int(tk)
        except ValueError:
            return -1
        version_as_int += tk_val*(1000**(3-i))

    return version_as_int


def family_str_to_int(family: str) -> int:
    fam = tag_to_family(family)

    tks = fam.split(".")
    tks_count = len(tks)
    if tks_count > 3:
        return -1

    family_as_int = 0
    for i in range(tks_count):
        tk = tks[i]
        tk_val = 0
        try:
            tk_val = int(tk)
        except ValueError:
            return -1

        family_as_int += tk_val*(1000**(3-i))

    return family_as_int


def tag_to_version(tag: str) -> Version:
    v = Version()
    v.as_str = tag_to_version_str(tag)
    v.family = tag_to_family(tag)
    v.major = family_to_major(v.family)
    v.minor = family_to_minor(v.family)
    v.as_int = version_str_to_int(v.as_str)
    v.family_as_int = family_str_to_int(v.family)
    return v


def version_str_to_version(version_str: str) -> Version:
    return tag_to_version(version_str)
