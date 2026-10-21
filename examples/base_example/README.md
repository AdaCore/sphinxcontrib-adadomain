sphinxcontrib-adadomain basic example
-------------------------------------

This is a very basic example of how to use sphinxcontrib-adadomain, alone and
with [GNATdoc](https://github.com/AdaCore/gnatdoc).

The `ada___*.rst` files (one per package, such as
[ada___pkg___spec.rst](./ada___pkg___spec.rst)) contain documentation for an
Ada package, with adadomain syntax. While you can write those kind of files
manually, this domain is better used together with the RST backend of the
GNATdoc documentation generator mentioned above.

The [Makefile](./Makefile) contains two rules, one to just run the
sphinx-build, one to re-generate the `ada___*.rst` files from the sources
contained in [prj](./prj/).
