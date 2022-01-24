import requests

from agstoolbox.gh import release


def get_releases() -> list[release.Release]:
    response = requests.get("https://api.github.com/repos/adventuregamestudio/ags/releases?per_page=100")
    print(type(response))
    response_json = response.json()
    print(len(response_json))
    releases = [None] * len(response_json)
    count = 0

    for rel in response_json:
        rls = None
        found_asset = False
        version = rel['name'].replace(" ", "").replace("v.", "")
        archive_name = "AGS-" + version + ".zip"
        for asset in rel['assets']:
            if asset['name'] == archive_name:
                rls = release.Release()
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
        rls.tag = rel['tag_name']
        rls.prerelease = rel['prerelease']
        rls.published_at = rel['published_at']
        releases[count] = rls
        count += 1

    releases = list(filter(None, releases))
    return releases
