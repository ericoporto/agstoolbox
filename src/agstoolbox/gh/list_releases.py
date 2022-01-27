from __future__ import annotations  # for python 3.8
import requests

from agstoolbox.gh.release import Release


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


def parse_releases(response_json) -> list[Release]:
    releases = [None] * len(response_json)
    count = 0

    for rel in response_json:
        rls = None
        found_asset = False
        version = rel['name'].replace(" ", "").replace("v.", "")
        archive_name = "AGS-" + version + ".zip"
        for asset in rel['assets']:
            if asset['name'] == archive_name:
                rls = Release()
                rls.archive_id = asset['id']
                rls.archive_name = asset['name']
                rls.archive_url = asset['browser_download_url']
                rls.archive_size = asset['size']
                found_asset = True
                break

        if not found_asset:
            continue

        rls.text_details = rel['body']
        rls.name = rel['name']
        rls.id = rel['id']
        rls.url = rel['url']

        tag = rel['tag_name']
        family = tag_to_family(tag)
        rls.tag = tag
        rls.version_family = family
        rls.version_major = family_to_major(family)
        rls.version_minor = family_to_minor(family)

        rls.prerelease = rel['prerelease']
        rls.published_at = rel['published_at']
        releases[count] = rls
        count += 1

    releases = list(filter(None, releases))
    return releases


def list_releases() -> list[Release]:
    response = requests.get(
        "https://api.github.com/repos/adventuregamestudio/ags/releases?per_page=100")
    response_json = response.json()
    return parse_releases(response_json)
