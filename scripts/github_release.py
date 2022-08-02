from pathlib import Path
import os
import requests
import click


VERSION = os.environ.get('FARADAY_VERSION')
TOKEN = os.environ.get('GH_TOKEN')


@click.option("--deb-file", required=True, type=click.Path(exists=True,dir_okay=False,resolve_path=True))
@click.option("--rpm-file", required=True, type=click.Path(exists=True,dir_okay=False,resolve_path=True))
def main(deb_file,rpm_file):
    release_data = {
        "tag_name": f"v{VERSION}",
        "name": f"v{VERSION}",
        "body": Path(
            Path(__file__).parent.parent / 'CHANGELOG' / VERSION / 'white.md'
        ).read_text(),
    }

    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {TOKEN}',
    }

    res = requests.post(
        "https://api.github.com/repos/infobyte/faraday/releases",
        json=release_data,
        headers=headers
    )
    res.raise_for_status()
    release_id = res.json()['id']
    for asset_file_data in [{"file": Path(deb_file), "mimetype": "application/vnd.debian.binary-package"},
                            {"file": Path(rpm_file), "mimetype": "application/x-redhat-package-manager"}]:
        asset_file = asset_file_data["file"]
        res = requests.post(
            f"https://api.github.com/repos/infobyte/faraday/releases/{release_id}/assets",
            headers=headers,
            files={
                'file': (
                    asset_file.name,
                    open(asset_file, mode="rb"),
                    asset_file_data["mimetype"]
                )
            }
        )
        res.raise_for_status()


if __name__ == '__main__':
    main()
