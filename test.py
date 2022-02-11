from os import environ, popen
from json import load
from pathlib import Path
latest = 1
root = Path(f'./第{latest}期/杂项/')
pdfs_root = Path('./pdfs/')
with open(root / '目录.json', 'r', encoding='utf8') as f:
    contents = load(f)
for type_ in ('论文', '通讯'):
    articles = [(
        name, author,
        int(next(filter(
            lambda s: s.startswith('NumberOfPages:'),
            popen(f'pdftk {pdfs_root / (name + ".pdf")} dump_data_utf8').read().splitlines(keepends=False)
        )).split(' ')[1])
    ) for name, author in contents[type_]]
    with open(root / f'{type_}.inc', 'w', encoding='utf8') as f:
        print('\\foreach \\fileName\\authorName\\pageNumber in {', file=f)
        for name, author, page in articles:
            print(f'{{{name}}}/{{{author}}}/{page},', file=f)
        print('}{\\addContent}', file=f)
