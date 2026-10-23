"""Проверка метаданных, шагов и диагностических вложений выбранного прогона."""
import argparse
from collections import Counter
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path, help='Каталог результатов одного прогона Allure')
    args = parser.parse_args()
    files = sorted(args.results.glob('*-result.json'))
    if not files:
        parser.error('В каталоге нет результатов тестов')
    results = [json.loads(path.read_text(encoding='utf-8')) for path in files]
    for result in results:
        labels = {label['name'] for label in result.get('labels', [])}
        assert {'feature', 'story', 'severity'} <= labels, result['name']
        assert result.get('steps'), result['name']
        attachments = result.get('attachments', [])
        if result['status'] in {'failed', 'broken'}:
            types = {attachment['type'] for attachment in attachments}
            assert {'image/png', 'text/html'} <= types, result['name']
        for attachment in attachments:
            assert (args.results / attachment['source']).stat().st_size > 0
    print(f'Проверено {len(results)} результатов:', dict(Counter(r['status'] for r in results)))


if __name__ == '__main__':
    main()
