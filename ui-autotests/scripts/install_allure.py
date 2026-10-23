"""Локальная установка официального Allure 2 без изменения PATH."""
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / '.tools'


def main() -> None:
    """Загрузить ZIP последнего стабильного выпуска из официального репозитория."""
    request = urllib.request.Request(
        'https://api.github.com/repos/allure-framework/allure2/releases/latest',
        headers={'User-Agent': 'ui-autotests-local-installer'},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        release = json.load(response)
    asset = next(item for item in release['assets'] if item['name'].endswith('.zip'))
    TOOLS.mkdir(exist_ok=True)
    archive = TOOLS / asset['name']
    destination = TOOLS / archive.stem
    if not (destination / 'bin' / 'allure.bat').exists():
        print('Download:', asset['browser_download_url'], flush=True)
        urllib.request.urlretrieve(asset['browser_download_url'], archive)
        with zipfile.ZipFile(archive) as source:
            for member in source.infolist():
                if not (TOOLS / member.filename).resolve().is_relative_to(TOOLS.resolve()):
                    raise ValueError('Небезопасный путь в архиве')
            source.extractall(TOOLS)
    (TOOLS / 'allure-path.txt').write_text(str(destination), encoding='utf-8')
    print('Allure:', destination, flush=True)


if __name__ == '__main__':
    main()
