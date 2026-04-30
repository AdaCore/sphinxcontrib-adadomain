--  Overloads package documentation

package Overloads is

   type R is new Integer;
   --  Type R

   type A is new Integer;
   --  Type A

   procedure Set (X : A);
   --  Set with A

   function Get (X : A) return R;
   --  Get with A return R

   type B is new Integer;
   --  Type B

   procedure Set (X : B);
   -- Set with B

   function Get (X : B) return R;
   --  Get with B return R

end Overloads;
