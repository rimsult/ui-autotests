"""Проверить настоящие результаты Allure, включая вложения упавших тестов."""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for directory in (root / 'allure-results').iterdir():
    if not directory.is_dir():
        continue
    results = [json.loads(p.read_text(encoding='utf-8')) for p in directory.glob('*-result.json')]
    if not results:
        continue
    print(directory.name, dict(Counter(r['status'] for r in results)))
    for result in results:
        labels = {label['name'] for label in result['labels']}
        assert {'feature', 'story', 'severity'} <= labels, result['name']
        if directory.name == 'verified-final':
            assert result.get('steps'), result['name']
        if result['status'] in {'failed', 'broken'}:
            attachments = result.get('attachments', [])
            types = {a['type'] for a in attachments}
            assert {'image/png', 'text/html'} <= types, result['name']
            for attachment in attachments:
                assert (directory / attachment['source']).stat().st_size > 0
            print('  Диагностика подтверждена:', ascii(result['name']))
print('Проверка метаданных и вложений Allure завершена')
