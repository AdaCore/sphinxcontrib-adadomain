==========
Ada Domain
==========

Originally written by Tero Koskinen <tero.koskinen@iki.fi>, forked and modified
by Raphaël Amiard <amiard@adacore.com> for AdaCore.

About
=====

This extension adds Ada domain support to Sphinx. While you can write files
documenting Ada code manually with this domain, it is mostly meant to be used
together with the laldoc documentation generator, which is part of
`Libadalang`_.

This extension requires Python 3.7 minimum.

Architecture
------------

The aim of the ada domain is to make it easy for an automatic tool to generate
sphinx that documents Ada constructs, easy for a manual doc writer to
*reference* generated doc, and not horribly hard for a manual API ref writer to
write this by hand if he so chooses (even though we don't see why that would
happen).

For this reason, profiles for Ada entities are written in almost Ada. The
domain can use `Libadalang`_ to parse function profiles if it is available, but
will fall-back on a simplistic regex in the case it's not.

Cross references
^^^^^^^^^^^^^^^^

Unlike the old version of the Ada domain developed by Tero Koskinen, cross
references are stored in one unique namespace (which is equivalent to the
language semantics).

Fully qualified names should work already (so that if you write
``:ada:type:`Root_Pkg.Child.My_Type``` in a docstring or a ReST file it should
generate the proper cross referenced). Relative names are planned but not
implemented.

.. attention:: Cross references for overloaded subprograms **are not handled
    yet**. Only the first subprogram with a given FQN will be registered and
    referenceable. We have not yet chosen the scheme we want to use for this.
    The old scheme based on arity was very complex and not correct - since
    arity is not sufficient.

Available directives
--------------------

This is a (non exhaustive for the moment) list of directives that this
extension exposes.

``function``/``procedure`` directives
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Those directives are used to document subprograms. They're of the form::

    .. ada:function:: function Foo (A, B : Integer) return Integer

        Documentation for the ``Foo`` function.

    .. ada:procedure:: procedure Foo (A, B : Integer)

        Documentation for the ``Foo`` procedure.

:field types: ``parameter``, ``returnvalue``

``object`` directive
^^^^^^^^^^^^^^^^^^^^

This directive is used to document object declarations. It's of the form::

    .. ada:object:: No_Such_Element : constant Element

        Documentation for the constant

        :defval: `(null record)`
        :objtype: Element

It **doesn't** include the default value in the profile, but as a field.

:field types: ``objtype``, ``renames``, ``defval``

``exception`` directive
^^^^^^^^^^^^^^^^^^^^^^^

This directive is used to document exceptions. It's of the form::

    .. ada:exception:: Custom_Exception

        Documentation for the exception

``generic-package-instantiation`` directive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This directive is used to document generic package instantiations. It's of the form::


    .. ada:generic-package-instantiation:: package Charset is new Parse_Option

        Documentation for the generic package instantiation.

        :instpkg: GNATCOLL.Opt_Parse.Parse_Option

``package`` directive
^^^^^^^^^^^^^^^^^^^^^

This directive is used to document the current package. It's a top-level
directive rather than a nesting one. you use it like this::

    .. ada:package:: Current_Package

    Doc for the package with corresponding directives

    .. ada:function: ....

``type`` directive
^^^^^^^^^^^^^^^^^^

This directive is used to document types. You use it like this::

    .. ada:type:: type My_Type

        Documentation for My_Type.

        :discriminant Boolean Kind:
        :component Integer My_Int_1:
        :component Integer My_Int_2:

:field types: ``discriminant``, ``component``

.. _Libadalang: https://github.com/AdaCore/libadalang
