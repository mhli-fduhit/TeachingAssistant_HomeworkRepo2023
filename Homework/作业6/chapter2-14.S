main:
    bgt a0 a1 L1
    sub a2 a0 a1
    j end

L1:
    add a2 a0 a1
    j end

end:
    ret