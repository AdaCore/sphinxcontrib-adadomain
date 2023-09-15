sphinxcontrib-adadomain basic example
-------------------------------------

This is a very basic example of how to use sphinxcontrib-adadomain, alone and
with [laldoc](https://github.com/AdaCore/libadalang/tree/master/contrib/laldoc).

[pkg.rst](./pkg.rst) contains documentation for an Ada package, with
adadomain syntax. While you can write those kind of files manually, this
domain is better used together with the laldoc documentation generator
mentioned above.

The [Makefile](./Makefile) contains two rules, one to just run the
sphinx-build, one to re-generate `pkg.rst` from the sources contained in
[prj](./prj/).
