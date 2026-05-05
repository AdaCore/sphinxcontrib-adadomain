
Pkg
---

.. ada:set_package:: Pkg



.. ada:generic_package:: Pkg.Container



    :Formals:
        .. ada:type:: type T
            :package: Pkg.Container


            The element type.

.. ada:generic-package-instantiation:: package Int_Container is new Container
    :package: Pkg

    .. code-block:: ada

        package Int_Container is new Container (Integer);

    :instpkg: Pkg.Container

    Container specialized for Integer.

.. ada:generic-package-instantiation:: package Bool_Container is new Container
    :package: Pkg

    .. code-block:: ada

        package Bool_Container is new Container (Boolean);

    :instpkg: Pkg.Container

    Container specialized for Boolean.
