import subprocess

modules = [
    'os',
    'asyncio',
    'itertools',
    'telethon',
]

for module in modules:
    subprocess.call(['pip', 'install', module])
    