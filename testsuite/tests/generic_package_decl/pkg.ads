package Pkg is
   -- This file contains a generic package declaration.

   -- Element package documentation.
   generic
      type T is private;
      -- This type is private.
   package Element is

      procedure Set (E : T);
      -- A procedure that sets things.

      procedure Reset;
      -- This one resets things!

      function Get return T;
      -- Oh! A getter, how nice it is!

      function Is_Valid return Boolean;
      -- Return whether this is valid.

      Invalid_Element : exception;
      -- This is raised when this is invalid!

   private
      Value : T;
      Valid : Boolean := False;
   end Element;
end Pkg;
