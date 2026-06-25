from pathlib import Path
import zipfile

root = Path('dist')
dest = Path('OpenSeismoLite_build.zip')

with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as z:
    for path in sorted(root.rglob('*')):
        if path.is_file():
            z.write(path, path.relative_to(root))

print(dest.name, dest.stat().st_size)
