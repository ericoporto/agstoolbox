from __future__ import annotations  # for python 3.8

from datetime import datetime
from operator import attrgetter

import requests

from agstoolbox.core.gh.agstoolbox_release import AgsToolboxRelease
from agstoolbox.core.version.version_utils import tag_to_version


def list_agstoolbox_releases() -> list[AgsToolboxRelease]:
    response = requests.get(
        "https://api.github.com/repos/ericoporto/agstoolbox/releases?per_page=10", timeout=2.0)
    response_json = response.json()
    return parse_agstoolbox_releases(response_json)


def parse_agstoolbox_releases(response_json) -> list[AgsToolboxRelease]:
    releases = [None] * len(response_json)
    count = 0

    for rel in response_json:
        rls = None
        found_asset = False

        # This can raise a TypeError in some weird condition I don't know what it is
        ## it reads as TypeError: string indices must be integers
        assets = rel['assets']

        for asset in assets:
            # check for agstoolbox release assets and add them
            if asset['name'] == 'agstoolbox.exe':
                if rls is None:
                    rls = AgsToolboxRelease()
                rls.winexe_id = str(asset['id'])
                rls.winexe_name = asset['name']
                rls.winexe_url = asset['browser_download_url']
                rls.winexe_size = int(asset['size'])
                found_asset = True

            if asset['name'] == 'atbx.exe':
                if rls is None:
                    rls = AgsToolboxRelease()
                rls.winatbx_id = str(asset['id'])
                rls.winatbx_name = asset['name']
                rls.winatbx_url = asset['browser_download_url']
                rls.winatbx_size = int(asset['size'])

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
