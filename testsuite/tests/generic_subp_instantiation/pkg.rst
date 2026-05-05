
Pkg
---

.. ada:set_package:: Pkg


.. ada:generic-function:: function Identity (X : Pkg.Identity.T) return Pkg.Identity.T
    :package: Pkg

    :Formals:
        .. ada:type:: type T
            :package: Pkg.Identity


            The element type to identity-convert.


    Generic identity function.

.. ada:generic-subp-instantiation:: function Int_Identity is new Identity
    :package: Pkg

    .. code-block:: ada

        function Int_Identity is new Identity (Integer);

    :instsubp: Pkg.Identity

    Identity function specialized for Integer.

.. ada:generic-subp-instantiation:: function Bool_Identity is new Identity
    :package: Pkg

    .. code-block:: ada

        function Bool_Identity is new Identity (Boolean);

    :instsubp: Pkg.Identity

    Identity function specialized for Boolean.
