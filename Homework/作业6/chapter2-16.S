swap:
    lw a2 0(t0)#a2=tmp=a
    lw a1 0(t1)#a1=b
    sw a1 0(t0)
    sw a2 0(t1)
    ret