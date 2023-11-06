# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpack_boilerplate',
 'webpack_boilerplate.contrib',
 'webpack_boilerplate.frontend_template.hooks',
 'webpack_boilerplate.management',
 'webpack_boilerplate.management.commands',
 'webpack_boilerplate.templatetags']

package_data = \
{'': ['*'],
 'webpack_boilerplate': ['frontend_template/*',
                         'frontend_template/{{cookiecutter.project_slug}}/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/application/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/components/*',
                         'frontend_template/{{cookiecutter.project_slug}}/src/styles/*',
                         'frontend_template/{{cookiecutter.project_slug}}/vendors/*',
                         'frontend_template/{{cookiecutter.project_slug}}/vendors/images/*',
                         'frontend_template/{{cookiecutter.project_slug}}/webpack/*']}

install_requires = \
['cookiecutter>=1.7.0']

setup_kwargs = {
    'name': 'python-webpack-boilerplate',
    'version': '1.0.2',
    'description': 'Jump start frontend project bundled by Webpack',
    'long_description': '# Jump start frontend project bundled by Webpack\n\n[![Build Status](https://github.com/AccordBox/python-webpack-boilerplate/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/AccordBox/python-webpack-boilerplate/actions/workflows/ci.yml)\n[![PyPI version](https://badge.fury.io/py/python-webpack-boilerplate.svg)](https://badge.fury.io/py/python-webpack-boilerplate)\n[![Documentation](https://img.shields.io/badge/Documentation-link-green.svg)](https://python-webpack-boilerplate.rtfd.io/)\n\n## Difference between django-webpack-loader\n\nWhen using `django-webpack-loader`, you need to create `Webpack` project on your own, which is not easy for many newbie Django developers.\n\n`python-webpack-boilerplate` can let you play with modern frontend tech in Django, even you have no idea how to config Webpack.\n\n## Features\n\n- **Supports Django and Flask** (will support more framework in the future)\n- Automatic multiple entry points\n- Automatic code splitting\n- Hot Module Replacement (HMR) (auto reload web page if you edit JS or SCSS)\n- Easy to config and customize\n- ES6 Support via [babel](https://babeljs.io/) (v7)\n- JavaScript Linting via [eslint](https://eslint.org/)\n- SCSS Support via [sass-loader](https://github.com/jtangelder/sass-loader)\n- Autoprefixing of browserspecific CSS rules via [postcss](https://postcss.org/) and [postcss-preset-env](https://github.com/csstools/postcss-preset-env)\n- Style Linting via [stylelint](https://stylelint.io/)\n\n----\n\nIf you want to import **lightweight modern frontend solution** to your web app, or you do not like **heavy framework** such as React, Vue.\n\nPlease check my book [The Definitive Guide to Hotwire and Django](https://leanpub.com/hotwire-django)\n\n----\n\n## Documentation\n\n1. [Setup With Django](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_django/)\n2. [Setup With Flask](https://python-webpack-boilerplate.readthedocs.io/en/latest/setup_with_flask/)\n3. [Frontend Workflow](https://python-webpack-boilerplate.readthedocs.io/en/latest/frontend/)\n\n## Raising funds\n\nIf you like this project, please consider supporting my work. [Open Collective](https://opencollective.com/python-webpack-boilerplate)\n\n---\n\n<a href="https://opencollective.com/python-webpack-boilerplate#backers" target="_blank"><img src="https://opencollective.com/python-webpack-boilerplate/backers.svg?width=890"></a>\n\n---\n\n## Special Thanks\n\n* [Definitive Guide to Django and Webpack](https://www.accordbox.com/blog/definitive-guide-django-and-webpack/)\n* [django-webpack-loader](https://github.com/owais/django-webpack-loader)\n* [rails/webpacker](https://github.com/rails/webpacker)\n* [wbkd/webpack-starter](https://github.com/wbkd/webpack-starter)\n',
    'author': 'Michael Yin',
    'author_email': 'michaelyin@accordbox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AccordBox/python-webpack-boilerplate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
