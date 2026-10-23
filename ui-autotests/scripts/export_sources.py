"""Собрать полный текст исходников для удобного просмотра и передачи."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = []
for directory in ('pages', 'components', 'tests', 'utils', 'config', 'scripts'):
    paths.extend((root / directory).glob('*.py'))
paths.extend(root / name for name in ('requirements.txt', 'pytest.ini', '.env.example', '.gitignore', 'README.md'))
parts = ['# Полное содержимое файлов UI-автотестов\n']
for path in sorted(paths):
    language = 'python' if path.suffix == '.py' else 'text'
    parts.append(f'\n## {path.relative_to(root).as_posix()}\n\n````{language}\n{path.read_text(encoding="utf-8")}\n````\n')
output = root / 'reports' / 'project-sources.md'
output.parent.mkdir(exist_ok=True)
output.write_text(''.join(parts), encoding='utf-8')
print(output)
