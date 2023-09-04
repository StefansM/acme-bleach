# Bleach

[![Read the documentation at https://acme-bleach.readthedocs.io/](https://img.shields.io/readthedocs/acme-bleach/latest.svg?label=Read%20the%20Docs)][read the docs]

[read the docs]: https://acme-bleach.readthedocs.io/
[tests]: https://github.com/stefansm/acme-bleach/actions?workflow=Tests

Remove unsightly visible characters from your code. Inspired by the [`Acme::Bleach` Perl module][acme::bleach] by Damian
Conway.

[acme::bleach]: https://metacpan.org/pod/Acme::Bleach

## Installation

You can install _Bleach_ via [pip] from [PyPI]:

```console
$ pip install acme-bleach
```

## Usage

Let's start with the following Python script, `hello.py`:

```python
print("Hello, world!")
```

### Bleaching

To bleach it, run the following command:

```console
$ bleach bleach hello.py -o hello-bleached.py
```

The result is a bleached version of the original script. The contents of
`hello-bleached.py` are (representing tabs with `»»»»` and spaces with `·`):

```
# coding=bleach
»»»»···»»»»»»»»»»»»»»»»»···»»»»»·»»»»»»»··»»·»»»»»»»·»»»··»»···»»»»»···»·»»»»»»»
»»»»»»»»·»»»·»»»»»»»»»»»»»»»»»»»·»»»»»»»»»»»·»»»»»»»·»»»»»»»·»»»»»»»»»»»»»»»··»»»»»»·»»»·»»»··»»··»»»»»»
»»»»··»»··»»»»»»»»»»··»»····»»»»»»»»·»»»··»»»»»»»»»»»»»»·»»»»»»»»»»»»»»»»»»»»»»»···»···
»»»»··»»····»»»»···»»»»»·»»»»»»»··»»··»»»»»»»»»»··»»»»»»·»»»»»»»»»»»»»»»·»»»»»»»»»»»»»»»·
»»»»»»»»·»»»»»»»»»»»·»»»»»»»»»»»·»»»·»»»»»»»·»»»»»»»»»»»»»»»·»»»·»»»
```

### Running

You can run the bleached file using `bleach run`:

```console
$ bleach run hello-bleached.py
Hello, world!
```

### Unbleaching

You can unbleach the file using `bleach unbleach`:

```console
$ bleach unbleach hello-bleached.py -o hello-unbleached.py
$ cat hello-unbleached.py
print("Hello, world!")
```

### Installing the bleach codec

Running scripts with `bleach run` is far too much effort. If you want to run bleached scripts directly, you can install
the `bleach` codec:

```console
$ bleach install
Wrote /home/stefans/bleach/.venv/lib/python3.10/site-packages/bleach.pth
$ python hello-bleached.py
Hello, world!
```

Installing the codec will attempt to write a `.pth` file to the `site-packages` directory of the current Python
interpreter. Note the `import` in the `.pth` file will be evaluated every time the current Python runs, so there is a
tiny amount of overhead.

## License

Distributed under the terms of the [MIT license][license],
_Bleach_ is free and open source software.

## Credits

This project was generated from a variant of [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/stefansm/acme-bleach/blob/main/LICENSE
[command-line reference]: https://acme-bleach.readthedocs.io/en/latest/usage.html
