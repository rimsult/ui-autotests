"""Сверка JUnit, результатов Allure и HTML-отчёта выбранного прогона."""
import argparse
from collections import Counter
import json
from pathlib import Path
import xml.etree.ElementTree as ET


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_name', help='Имя прогона из run_browser_tests.py')
    args = parser.parse_args()
    if not args.run_name.replace('-', '').replace('_', '').isalnum():
        parser.error('Недопустимое имя прогона')
    root = Path(__file__).resolve().parents[1]
    name = args.run_name
    suites = ET.parse(root / 'reports' / f'junit-{name}.xml').getroot()
    cases = list(suites.iter('testcase'))
    assert cases, 'JUnit не содержит тестов'
    assert all(case.find(tag) is None for case in cases for tag in ('failure', 'error', 'skipped'))
    results = [json.loads(p.read_text(encoding='utf-8')) for p in
               (root / 'allure-results' / name).glob('*-result.json')]
    junit_names = Counter(f"{case.get('classname')}.{case.get('name').split('[')[0]}" for case in cases)
    allure_names = Counter(r['fullName'].replace('#', '.') for r in results)
    assert junit_names == allure_names, 'Состав тестов JUnit и Allure различается'
    assert len(results) == len(cases), 'Количество результатов JUnit и Allure различается'
    assert all(r['status'] == 'passed' for r in results)
    report = root / 'reports' / f'allure-{name}'
    summary = json.loads((report / 'widgets' / 'summary.json').read_text(encoding='utf-8'))
    assert summary['statistic']['total'] == len(cases)
    assert summary['statistic']['passed'] == len(cases)
    assert (report / 'index.html').is_file()
    print(f'Проверено: JUnit, Allure и HTML содержат {len(cases)} успешных результатов.')


if __name__ == '__main__':
    main()
