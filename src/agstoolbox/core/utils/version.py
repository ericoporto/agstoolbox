from __future__ import annotations


def tag_to_version(tag: str) -> str:
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
