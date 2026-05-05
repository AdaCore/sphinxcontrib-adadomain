package Pkg is

   generic
      type T is private;
      --  The element type.
   package Container is
      --  Generic container package.
   end Container;

   package Int_Container is new Container (Integer);
   --  Container specialized for Integer.

   package Bool_Container is new Container (Boolean);
   --  Container specialized for Boolean.

end Pkg;
