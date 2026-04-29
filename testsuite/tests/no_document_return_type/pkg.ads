package Pkg is

   type Base_Node is null record;
   --% no-document: True

   type My_Node is new Base_Node;
   --  A node type.

   function Get (Self : My_Node) return My_Node;
   --  Get a node.

   function Get (Self : My_Node) return Base_Node;
   --  Should not appear in the documentation.

end Pkg;
