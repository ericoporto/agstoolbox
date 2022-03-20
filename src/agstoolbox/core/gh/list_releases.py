from __future__ import annotations  # for python 3.8

from datetime import datetime
from operator import attrgetter

import requests

from agstoolbox.core.gh.release import Release
from agstoolbox.core.utils.version import tag_to_version, tag_to_family, family_to_major, \
    family_to_minor


def is_asset_archive(release_name: str, asset_name: str) -> bool:
    version = release_name.replace(" ", "").replace("v.", "")
    is_patch = asset_name.startswith("AGS-" + version + "-P")
    if is_patch:
        patch = asset_name.split(version + "-P")[1].split(".")[0]
        version += "-P" + patch

    archive_name = "AGS-" + version + ".zip"
    return asset_name == archive_name


def parse_releases(response_json) -> list[Release]:
    releases = [None] * len(response_json)
    count = 0

    for rel in response_json:
        rls = None
        found_asset = False

        for asset in rel['assets']:
            # check for either predictable or patch release archives
            if is_asset_archive(rel['name'], asset['name']):
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
        rls.version = tag_to_version(tag)
        rls.version_family = family
        rls.version_major = family_to_major(family)
        rls.version_minor = family_to_minor(family)

        rls.prerelease = rel['prerelease']
        rls.published_at = rel['published_at']
        tstamp = datetime.strptime(rel['published_at'], "%Y-%m-%dT%H:%M:%SZ")
        rls.published_at_timestamp = tstamp.timestamp()
        releases[count] = rls
        count += 1

    releases = list(filter(None, releases))

    releases.sort(key=attrgetter("published_at_timestamp"), reverse=True)

    return releases


def list_releases() -> list[Release]:
    response = requests.get(
        "https://api.github.com/repos/adventuregamestudio/ags/releases?per_page=100")
    response_json = response.json()
    return parse_releases(response_json)
