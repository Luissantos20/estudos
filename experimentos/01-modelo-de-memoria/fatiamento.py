linha = [0] * 3

# Opção (a): o [:] fica dentro da comprehension
grid_a = [linha[:] for _ in range(3)]
grid_a[0][0] = 1
print("a:", grid_a)
print("a: grid[0] is grid[1] ->", grid_a[0] is grid_a[1])
print("a: ids ->", [id(l) for l in grid_a])

# Opção (b): o [:] fica fora, copiando a lista externa
linha = [0] * 3
grid_b = [linha for _ in range(3)][:]
grid_b[0][0] = 1
print("b:", grid_b)
print("b: grid[0] is grid[1] ->", grid_b[0] is grid_b[1])
print("b: ids ->", [id(l) for l in grid_b], "linha:", id(linha))