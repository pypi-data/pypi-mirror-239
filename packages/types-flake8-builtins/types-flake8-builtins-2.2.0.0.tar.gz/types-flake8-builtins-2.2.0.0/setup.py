from setuptools import setup

name = "types-flake8-builtins"
description = "Typing stubs for flake8-builtins"
long_description = '''
## Typing stubs for flake8-builtins

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`flake8-builtins`](https://github.com/gforcada/flake8-builtins) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`flake8-builtins`.

This version of `types-flake8-builtins` aims to provide accurate annotations
for `flake8-builtins==2.2.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/flake8-builtins. All fixes for
types and metadata should be contributed there.

This stub package is marked as [partial](https://peps.python.org/pep-0561/#partial-stub-packages).
If you find that annotations are missing, feel free to contribute and help complete them.


See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `1c51689b2625a84868ef1a182c9655f8e4070278` and was tested
with mypy 1.6.1, pyright 1.1.334, and
pytype 2023.10.17.
'''.lstrip()

setup(name=name,
      version="2.2.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/flake8-builtins.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['flake8_builtins-stubs'],
      package_data={'flake8_builtins-stubs': ['__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
