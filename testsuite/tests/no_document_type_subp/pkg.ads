package Pkg is

   type Base_Node is null record;
   --  @exclude

   type My_Node is new Base_Node;
   --  A node type.

   function Get (Self : My_Node) return My_Node;
   --  Get a node.

   function Get (Self : My_Node) return Base_Node;
   --  Should not appear in the documentation.

   procedure Set (Self : My_Node);
   --  Set a node.

   procedure Set (Self : Base_Node);
   --  Should not appear in the documentation.

end Pkg;
