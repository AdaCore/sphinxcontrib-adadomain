package Pkg is
    package Q is
    end Q;

    package P renames Q;
    -- A package renaming.
end Pkg;
