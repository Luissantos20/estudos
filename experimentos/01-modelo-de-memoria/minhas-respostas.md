# Minhas respostas — Aula 1: modelo de memória

Registro do que eu respondi durante a aula (10–11/11/2026), com as minhas palavras e antes de ver a resposta certa. Os números seguem as questões do `aula.md`.

## Previsões

**1. Pergunta 0** — o que acontece em `a = [1, 2, 3]`?
- Primeira resposta: "ele atribui 3 espaços da memória para `a`?"
- Depois de pensar: "`a` é a referência do espaço de memória que aponta pra lista, e os valores 1, 2, 3 moram dentro dos espaços de memória atribuídos."

**2. Saída dos trechos**
- Trecho 1: `[1, 2, 3, 4] True False`
  - Por quê: "`is` verifica se o espaço de memória é o mesmo. Não sei o que o `id` devolve."
- Trecho 2: `[1] [1, 2]`
  - Por quê: "o 1 veio do primeiro append."
- Trecho 3: primeiro "não faço ideia", depois "vai virar uma matriz 3x3?"
  - Previsão do `print(grid)`: `[[1, 0, 0], [0, 0, 0], [0, 0, 0]]`

## Experimentos

**4. `grid = [linha for _ in range(3)]`, depois `grid[0][0] = 1`**
- Valor: `[[0, 0, 0], [0, 0, 0], [0, 0, 0]]`, e "o que muda é que agora cada referência da lista tem um nome `linha`?"
- Depois de `grid[0][0] = 1`: `[[1, 0, 0], [0, 0, 0], [0, 0, 0]]`
- ids: "o id de cada linha vai ser diferente, e o id de `linha` diferente de todos."

**5. `linha.append(9)` depois de montar o grid** — sem resposta registrada.

**6. `fatiamento.py`, opção (b)**
- `grid_b = [[1, 0, 0], [0, 0, 0], [0, 0, 0]]`
- `grid_b[0] is grid_b[1]` → `False`
- "o id de cada linha vai ser diferente e o id de `linha` é diferente de todos."
- Opção (a): sem previsão registrada.

## Desafios

**7. Reescrever o `grid`**
```python
grid = [[0] * 3 for _ in range(3)]
```

**8. Reescrever o `add`** — não tentei.

## Checagem

**9 a 11** — não respondi.

**12. `print(add_ok(1), add_ok(2))`**
"`[1]`, `[2]`, e eles não apontam para o mesmo objeto porque a lista nasce a cada chamada. Se ela nascesse no `def`, toda operação estaria alterando esse objeto."

**13. `r1.append(100)`**
"`[1, 2, 3, 100]`, porque o append adiciona um item à lista, e fazer append no `r1` vai estar alterando o objeto do `add_bug`."

**14. `x = [[]] * 3; x[0].append("a")`**
"`x = [[a], [a], [a]]`?"

**15 a 17** — não respondi.

**18. Cria ou busca**
1. cria
2. busca
3. cria
4. "busca e cria?"

## Diagnóstico

Pergunta: o que acontece em cada volta de `[linha for _ in range(3)]`?
"Cria uma lista `[0, 0, 0]` 3 vezes dentro de uma lista. E como `linha` já referencia a lista `[0, 0, 0]`, ficaria `[[linha], [linha], [linha]]`?"
