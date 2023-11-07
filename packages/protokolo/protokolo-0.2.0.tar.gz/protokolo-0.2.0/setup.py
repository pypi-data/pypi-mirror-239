# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['protokolo']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0']

entry_points = \
{'console_scripts': ['protokolo = protokolo.cli:cli']}

setup_kwargs = {
    'name': 'protokolo',
    'version': '0.2.0',
    'description': 'Protokolo is a change log generator.',
    'long_description': "<!--\nSPDX-FileCopyrightText: 2023 Carmen Bianca BAKKER <carmen@carmenbianca.eu>\n\nSPDX-License-Identifier: CC-BY-SA-4.0 OR GPL-3.0-or-later\n-->\n\n# Protokolo\n\nProtokolo is a change log generator.\n\nProtokolo allows you to maintain your change log entries in separate files, and\nthen finally aggregate them into a new section in CHANGELOG just before release.\n\n## Table of Contents\n\n- [Background](#background)\n- [Install](#install)\n- [Usage](#usage)\n- [Maintainers](#maintainers)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Background\n\nChange logs are [a really good idea](https://keepachangelog.com/).\nUnfortunately, they are also a bit of a pain when combined with version control:\n\n- If two pull requests edit CHANGELOG, there is a non-zero chance that you'll\n  need to resolve a conflict when trying to merge them both.\n- Just after you make a release, you need to create a new section in CHANGELOG\n  for your next release. If you forget this busywork, new feature branches will\n  need to create this section, which increases the chance of merge conflicts.\n- If a feature branch adds a change log entry to the section for the next v1.2.3\n  release, and v1.2.3 subsequently releases without merging that feature branch,\n  then merging that feature branch afterwards would still add the change log\n  entry to the v1.2.3 section, even though it should now go to the v1.3.0\n  section.\n\nLife would be a lot easier if you didn't have to deal with these problems.\n\nEnter Protokolo. The idea is very simple: For every change log entry, create a\nnew file. Finally, just before release, compile the contents of those files into\na new section in CHANGELOG, and delete the files.\n\n## Install\n\nProtokolo is a regular Python package. You can install it using\n`pipx install protokolo`. Make sure that `~/.local/share/bin` is in your `$PATH`\nwith `pipx ensurepath`.\n\n## Usage\n\nTo set up your project for use with Protokolo, run `protokolo init`. This will\ncreate a `CHANGELOG.md` file (if one did not already exist) and a directory\nstructure under `changelog.d`. The directory structure uses the\n[Keep a Changelog](https://keepachangelog.com/) sections, and ends up looking\nlike this:\n\n```\n.\n├── changelog.d\n│\xa0\xa0 ├── added\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 ├── changed\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 ├── deprecated\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 ├── fixed\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 ├── removed\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 ├── security\n│\xa0\xa0 │\xa0\xa0 └── .protokolo.toml\n│\xa0\xa0 └── .protokolo.toml\n└── CHANGELOG.md\n```\n\nThe `.protokolo.toml` files contain metadata for their respective sections; the\nsection title, header level, and order. Their inclusion is mandatory.\n\nTo add a change log entry, create the file `changelog.d/added/my_feature.md`,\nand write something like:\n\n```markdown\n- Added `--my-new-feature` option.\n```\n\nNote the item dash at the start; Protokolo does not add them for you. What you\nwrite is exactly what you get.\n\nYou can add more files. Change log entries in the same section (read: directory)\nare sorted alphabetically by their file name. If you want to make certain that\nsome change log entries go first or last, prefix the file with `000_` or `zzz_`.\nFor example, you can create `changelog.d/added/000_important_feature.md` to make\nit appear first.\n\nFinally, compile your change log with\n`protokolo compile --changelog CHANGELOG.md changelog.d`. This will take all\nchange log entries from `changelog.d` and put them in your `CHANGELOG.md`. If we\nrun it now, the following section is added after the\n`<!-- protokolo-section-tag -->` comment:\n\n```markdown\n## ${version} - 2023-11-08\n\n### Added\n\n- Added important feature.\n\n- Added `--my-new-feature` option.\n```\n\nThe Markdown files in `changelog.d/added/` are deleted. You can manually replace\n`${version}` with a release version, or you can pass the option\n`--format version=1.0.0` to `protokolo compile` to format the header at compile\ntime (TODO: not implemented yet).\n\nFor more documentation and options, read the documentation at TODO.\n\n## Maintainers\n\n- Carmen Bianca BAKKER <carmen@carmenbianca.eu>\n\n## Contributing\n\nThe code and issue tracker is hosted at\n<https://codeberg.org/carmenbianca/protokolo>. You are welcome to open any\nissues. For pull requests, bug fixes are always welcome, but new features should\nprobably be discussed in any issue first.\n\n## License\n\nAll code is licensed under GPL-3.0-or-later.\n\nAll documentation is licensed under CC-BY-SA-4.0 OR GPL-3.0-or-later.\n\nSome configuration files are licensed under CC0-1.0 OR GPL-3.0-or-later.\n\nThe repository is [REUSE](https://reuse.software)-compliant. Check the\nindividual files for their exact licensing.\n",
    'author': 'Carmen Bianca BAKKER',
    'author_email': 'carmen@carmenbianca.eu',
    'maintainer': 'Carmen Bianca BAKKER',
    'maintainer_email': 'carmen@carmenbianca.eu',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
