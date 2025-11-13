
Pkg
---

.. ada:set_package:: Pkg

Top-level package documentation.  I'm baby la croix drinking vinegar
actually, photo booth pinterest raw denim coloring book occupy meggings
church-key yr. Waistcoat tofu bruh mustache cornhole butcher normcore
forage Brooklyn ramps. Sus PBR&B, cupping VHS swag tofu poutine authentic
godard actually chia.

Header
``````

Shoreditch you probably haven't heard of them four loko yr, pour-over
typewriter try-hard beard. Roof party live-edge jean shorts tilde iPhone,
everyday carry small batch knausgaard disrupt solarpunk tacos. Ascot yes
plz live-edge ramps narwhal heirloom pok pok. Pour-over kombucha
intelligentsia, salvia health goth gatekeep butcher wayfarers lo-fi
succulents.

* List
* Of elements

Stumptown cornhole you probably haven't heard of them ramps, try-hard pork
belly bodega boys bushwick meditation grailed keytar gorpcore marxism
portland lo-fi.

.. ada:type:: type T
    :package: Pkg

    :component Standard.Integer A:
        Documentation for A, B, C
    :component Standard.Integer B:
        Documentation for A, B, C
    :component Standard.Integer C:
        Documentation for A, B, C

    Documentation for record T

    .. ada:procedure:: procedure Foo (Self : Pkg.T)
        :package: Pkg


    .. ada:function:: function Create (A, B, C : Standard.Integer) return Pkg.T
        :package: Pkg

        Constructor function for :ada:ref:`T`

    .. ada:function:: function Poo (Self : Pkg.T) return Standard.Boolean
        :package: Pkg

        Check whether the ``@`` shortcut syntax is handled correctly by
        referencing :ada:ref:`U.D`

    .. ada:object:: Singleton : T
        :package: Pkg

        :objtype: Pkg.T
        :defval: ``(1, 2, 3)``

        Documentation for Singleton

    .. ada:object:: Singleton2 : T
        :package: Pkg

        :objtype: Pkg.T

        Documentation for Singleton 2

.. ada:type:: type U
    :package: Pkg

    :component Standard.Float C:
    :component Standard.Float D:
    :component Standard.Float E:


    .. ada:procedure:: procedure Primitive_Of_Both (Self : Pkg.T; Other : Pkg.U)
        :package: Pkg

        This is a primitive of both types. We want to test that thanks to the
        ``belongs-to`` annotation, it is correctly attached to :ada:ref:`U`.


.. ada:generic_package:: Pkg.Gen_Package


    Documentation for Singleton 2

    :Formals:
        .. ada:type:: type F
            :package: Pkg.Gen_Package


            The main type for this generic package

        .. ada:function:: function Frobulize (Self : Pkg.Gen_Package.F) return Standard.Boolean
            :package: Pkg.Gen_Package

            A way to frobulize instances

.. ada:exception:: Froob
    :package: Pkg

    A custom exception, raised in the implementation of :ada:ref:`U`


.. ada:package:: Pkg.Nested_Package


    This is a nested package

    .. ada:function:: function Barize (Inst : Pkg.T; Other_Inst : Pkg.U) return Standard.Boolean
        :package: Pkg.Nested_Package

        Barize the items
