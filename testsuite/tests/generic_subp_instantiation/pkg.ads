package Pkg is

   generic
      type T is private;
      --  The element type to identity-convert.
   function Identity (X : T) return T;
   --  Generic identity function.

   function Int_Identity is new Identity (Integer);
   --  Identity function specialized for Integer.

   function Bool_Identity is new Identity (Boolean);
   --  Identity function specialized for Boolean.

end Pkg;
