addi a2 0
addi a3 100

Loop:
    beq a2 a3 done
    mvi a4 4
    mul a4 a4 a2 #偏移量
    add a4 a4 t1 #得到B[i]的地址
    lw  a5 0(a4) #a5存放B[i]
    lw  a6 0(t2) #a6存放C
    mul a5 a5 a6 #结果
    add a6 a4 t0 #得到A[i]的地址
    sw  a5 0(a6) #结果存入A[i]
    j   Loop



done:
    mv a0 0(t0)
    ret
    