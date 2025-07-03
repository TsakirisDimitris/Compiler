L0:
# 0: jump, _, _, Main
		j LMain
LMain:
L1:
	sw ra, -0(sp)
L2:
# 2: *, x, 2, t@1
	lw t0, -4(sp)
	addi t0, t0, -12
	lw t1, 0(t0)
	li t2, 2
	mul t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -28
	sw t1, 0(t0)
L3:
# 3: :=, t@1, _, y
	lw t0, -4(sp)
	addi t0, t0, -28
	lw t1, 0(t0)
L4:
# 4: :=, 0, _, α
	li t1, 0
	lw t0, -4(sp)
	addi t0, t0, -12
	sw t1, 0(t0)
L5:
# 5: :=, 1, _, β
	li t1, 1
	lw t0, -4(sp)
	addi t0, t0, -16
	sw t1, 0(t0)
L6:
# 6: :=, 0, _, ι1
	li t1, 0
	lw t0, -4(sp)
	addi t0, t0, -20
	sw t1, 0(t0)
L7:
# 7: out, ι1, _, _
	lw t3, -20(sp)
		...
L8:
# 8: +, ι1, 1, t@2
	lw t0, -4(sp)
	addi t0, t0, -20
	lw t1, 0(t0)
	li t2, 1
	add t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -40
	sw t1, 0(t0)
L9:
# 9: :=, t@2, _, ι1
	lw t0, -4(sp)
	addi t0, t0, -40
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -20
	sw t1, 0(t0)
L10:
# 10: label, _, _, L1
L11:
# 11: <, ι1, 1, L2
	lw t0, -4(sp)
	addi t0, t0, -20
	lw t1, 0(t0)
	li t2, 1
	blt t1, t2, L2
L12:
# 12: jump, _, _, L3
	j L3
L13:
# 13: label, _, _, L2
L14:
# 14: out, ι1, _, _
	lw t3, -20(sp)
		...
L15:
# 15: +, α, β, t@3
	lw t0, -4(sp)
	addi t0, t0, -12
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -16
	lw t2, 0(t0)
	add t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -44
	sw t1, 0(t0)
L16:
# 16: :=, t@3, _, τ
	lw t0, -4(sp)
	addi t0, t0, -44
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -28
	sw t1, 0(t0)
L17:
# 17: :=, β, _, α
	lw t0, -4(sp)
	addi t0, t0, -16
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -12
	sw t1, 0(t0)
L18:
# 18: :=, τ, _, β
	lw t0, -4(sp)
	addi t0, t0, -28
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -16
	sw t1, 0(t0)
L19:
# 19: +, ι1, 1, t@4
	lw t0, -4(sp)
	addi t0, t0, -20
	lw t1, 0(t0)
	li t2, 1
	add t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -48
	sw t1, 0(t0)
L20:
# 20: :=, t@4, _, ι1
	lw t0, -4(sp)
	addi t0, t0, -48
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -20
	sw t1, 0(t0)
L21:
# 21: out, α, _, _
	lw t1, -12(sp)
		...
L22:
# 22: jump, _, _, L1
	j L1
L23:
# 23: label, _, _, L3
L24:
# 24: :=, 0, _, ι2
	li t1, 0
	lw t0, -4(sp)
	addi t0, t0, -24
	sw t1, 0(t0)
L25:
# 25: :=, 1, _, π
	li t1, 1
	lw t0, -4(sp)
	addi t0, t0, -32
	sw t1, 0(t0)
L26:
# 26: label, _, _, L4
L27:
# 27: +, ι2, 1, t@5
	lw t0, -4(sp)
	addi t0, t0, -24
	lw t1, 0(t0)
	li t2, 1
	add t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -52
	sw t1, 0(t0)
L28:
# 28: :=, t@5, _, ι2
	lw t0, -4(sp)
	addi t0, t0, -52
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -24
	sw t1, 0(t0)
L29:
# 29: *, π, ι2, t@6
	lw t0, -4(sp)
	addi t0, t0, -32
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -24
	lw t2, 0(t0)
	mul t1, t1, t2
	lw t0, -4(sp)
	addi t0, t0, -56
	sw t1, 0(t0)
L30:
# 30: :=, t@6, _, π
	lw t0, -4(sp)
	addi t0, t0, -56
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -32
	sw t1, 0(t0)
L31:
# 31: out, π, _, _
	lw t6, -32(sp)
		...
L32:
# 32: >=, ι2, 7, L5
	lw t0, -4(sp)
	addi t0, t0, -24
	lw t1, 0(t0)
	li t2, 7
	bge t1, t2, L5
L33:
# 33: jump, _, _, L4
	j L4
L34:
# 34: label, _, _, L5
L35:
# 35: :=, 6, _, x
	li t1, 6
	lw t0, -4(sp)
	addi t0, t0, -12
	sw t1, 0(t0)
L36:
# 36: par, x, _, CV
	lw t0, -4(sp)
	addi t0, t0, -12
	lw t0, 0(t0)
	sw t0, -12(sp)
L37:
# 37: par, t@7, _, RET
	addi t0, sp, -60
	sw t0, -8(sp)
L38:
# 38: call, διπλάσιο, _, _
	sw ra, 0(sp)
	jal L2
	lw ra, 0(sp)
L39:
# 39: :=, t@7, _, τ
	lw t0, -4(sp)
	addi t0, t0, -60
	lw t1, 0(t0)
	lw t0, -4(sp)
	addi t0, t0, -28
	sw t1, 0(t0)
L40:
# 40: out, τ, _, _
	lw t5, -28(sp)
		...
L41:
# 41: halt, _, _, _
	li a7, 10
	ecall
L42:
# 42: end_block, Main, _, _
