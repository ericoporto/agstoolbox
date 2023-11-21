from __future__ import annotations  # for python 3.8

from datetime import datetime
from operator import attrgetter

import requests

from agstoolbox.core.gh.release import Release
from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import tag_to_version


def is_asset_archive(release_name: str, asset_name: str) -> bool:
    nversion = release_name.replace(" ", "").replace("v.", "")
    if nversion.startswith('v'):
        nversion = nversion[1:]
    is_patch = asset_name.startswith("AGS-" + nversion + "-P")
    is_beta = asset_name.startswith("AGS-" + nversion + "-Beta")
    if is_patch:
        patch = asset_name.split(nversion + "-P")[1].split(".")[0]
        nversion += "-P" + patch

    if is_beta:
        beta = asset_name.split(nversion + "-Beta")[1].split(".")[0]
        nversion += "-Beta" + beta

    archive_name = "AGS-" + nversion + ".zip"
    return asset_name == archive_name


def parse_releases(response_json) -> list[Release]:
    releases = [None] * len(response_json)
    count = 0

    for rel in response_json:
        rls = None
        found_asset = False

        # This can raise a TypeError in some weird condition I don't know what it is
        for asset in rel['assets']:
            # check for either predictable or patch release archives
            if is_asset_archive(rel['name'], asset['name']):
                rls = Release()
                rls.archive_id = str(asset['id'])
                rls.archive_name = asset['name']
                rls.archive_url = asset['browser_download_url']
                rls.archive_size = int(asset['size'])
                found_asset = True
                break

        if not found_asset:
            for asset in rel['assets']:
                # check for either predictable or patch release archives
                if is_asset_archive(rel['tag_name'], asset['name']):
                    rls = Release()
                    rls.archive_id = str(asset['id'])
                    rls.archive_name = asset['name']
                    rls.archive_url = asset['browser_download_url']
                    rls.archive_size = asset['size']
                    found_asset = True
                    break

        if not found_asset:
            continue

        rls.text_details = rel['body']
        rls.name = rel['name']
        rls.id = str(rel['id'])
        rls.url = rel['url']
        rls.html_url = rel['html_url']

        tag = rel['tag_name']
        rls.tag = tag
        rls.version = tag_to_version(tag)

        rls.is_pre_release = rel['prerelease']
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


def get_latest_release_family(releases: list[Release], family: str) -> Release | None:
    filtered_releases = [r for r in releases if r.version.family == family]
    filtered_releases.sort(key=attrgetter("version.as_int"), reverse=True)
    if len(filtered_releases) >= 1:
        return filtered_releases[0]
    else:
        return None


def get_release_version(releases: list[Release], version: Version) -> Release | None:
    filtered_releases = [r for r in releases if r.version.as_int == version.as_int]
    if len(filtered_releases) == 1:
        return filtered_releases[0]
    else:
        return None
