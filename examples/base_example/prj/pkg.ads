-- Top-level package documentation.  I'm baby la croix drinking vinegar
-- actually, photo booth pinterest raw denim coloring book occupy meggings
-- church-key yr. Waistcoat tofu bruh mustache cornhole butcher normcore
-- forage Brooklyn ramps. Sus PBR&B, cupping VHS swag tofu poutine authentic
-- godard actually chia.
--
-- Header
-- ``````
--
-- Shoreditch you probably haven't heard of them four loko yr, pour-over
-- typewriter try-hard beard. Roof party live-edge jean shorts tilde iPhone,
-- everyday carry small batch knausgaard disrupt solarpunk tacos. Ascot yes
-- plz live-edge ramps narwhal heirloom pok pok. Pour-over kombucha
-- intelligentsia, salvia health goth gatekeep butcher wayfarers lo-fi
-- succulents.
--
-- * List
-- * Of elements
--
-- Stumptown cornhole you probably haven't heard of them ramps, try-hard pork
-- belly bodega boys bushwick meditation grailed keytar gorpcore marxism
-- portland lo-fi.

package Pkg is

   type T is record
      A, B, C : Integer;
      --  Documentation for A, B, C
   end record;
   --  Documentation for record T

   type U is record
      C, D, E : Float;
   end record;

   procedure Foo (Self : T);

   function Create (A, B, C : Integer) return T;
   --  Constructor function for :ada:ref:`T`

   function Poo (Self : T) return Boolean;
   --  Check whether the ``@`` shortcut syntax is handled correctly by
   --  referencing @U.D

   procedure Primitive_Of_Both (Self : T; Other : U);
   --% belongs-to: U
   --  This is a primitive of both types. We want to test that thanks to the
   --  ``belongs-to`` annotation, it is correctly attached to :ada:ref:`U`.

   Singleton : T := (1, 2, 3);
   --  Documentation for Singleton

   Singleton2 : T := (1, 2, 3);
   --% document-value: False
   --  Documentation for Singleton 2

   generic
      type F is private;
      --  The main type for this generic package

      with function Frobulize (Self : F) return Boolean;
      --  A way to frobulize instances
   package Gen_Package is
   end Gen_Package;
   --  This package is bla bla bla prout.

   Froob : exception;
   --  A custom exception, raised in the implementation of :ada:ref:`U`

   --  This is a nested package
   package Nested_Package is
      function Barize (Inst : T; Other_Inst : U) return Boolean;
      --  Barize the items
   end Nested_Package;

   function Dont_Document return Boolean is (True);
   --% no-document: True

end Pkg;
