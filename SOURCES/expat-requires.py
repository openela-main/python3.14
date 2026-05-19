import pathlib
import pyexpat
import sys


# This will determine the version of currently installed expat
EXPAT_VERSION = pyexpat.EXPAT_VERSION.removeprefix('expat_')
MAJOR, MINOR, PATCH = (int(i) for i in EXPAT_VERSION.split('.'))
EXPAT_COMBINED_VERSION = 10000*MAJOR + 100*MINOR + PATCH

# For the listed files, we find all XML_COMBINED_VERSION-based #ifs
SRC = pathlib.Path.cwd()
SOURCES = [
    SRC / 'Modules/pyexpat.c',
    SRC / 'Modules/clinic/pyexpat.c.h',
]
versions = set()
for source in SOURCES:
    for line in source.read_text().splitlines():
        if 'XML_COMBINED_VERSION' not in line:
            continue
        words = line.split()
        if words[0] == '#define':
            continue
        if len(words) != 4:
            continue
        if words[0] not in ('#if', '#elif'):
            continue
        if words[1].startswith('(') and words[-1].endswith(')'):
            words[1] = words[1][1:]
            words[-1] = words[-1][:-1]
        if words[1] == 'XML_COMBINED_VERSION':
            version = int(words[3])
            if words[2] == '>':
                versions.add(version+1)
                continue
            if words[2] == '>=':
                versions.add(version)
                continue
        raise ValueError(
            'Unknown line with XML_COMBINED_VERSION, adjust this script:\n\n'
            f'{line}'
        )

# We need the highest satisfiable version used in the #ifs, in x.y.z notation
v = max({v for v in versions if v <= EXPAT_COMBINED_VERSION})
major, minor_patch = divmod(v, 10000)
minor, patch = divmod(minor_patch, 100)
print(f"{major}.{minor}.{patch}")

