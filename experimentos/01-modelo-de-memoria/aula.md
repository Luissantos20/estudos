# Aula 1 — Modelo de memória do Python

Ciclo 1 · Semana 1 · Fundamentos · 10–11/11/2026
Código da aula: `memoria.py` e `fatiamento.py` (nesta pasta)

## Objetivo

Entender o que o `=` faz de verdade em Python e por que, às vezes, mexer numa variável altera outra.
Tópicos: referência vs cópia, mutabilidade, `id()`, `is` vs `==`, cópia rasa vs profunda.

## A ideia central

> Em Python, toda variável é um **nome colado num objeto**.
> O `=` nunca copia: ele só cola o nome no objeto que está à direita.

Uma lista **não guarda valores**: guarda **referências** para outros objetos. No CPython, uma lista é um array de ponteiros, e não um array de valores como em C.

```
a = [1, 2, 3]

  a ──► ┌─ list ──────────┐
        │ ref ─► int 1    │
        │ ref ─► int 2    │
        │ ref ─► int 3    │
        └─────────────────┘
```

**Regra do bug de aliasing:** dois nomes no mesmo objeto **+** objeto mutável. Se faltar um dos dois, o bug não acontece.

**Regra da criação de objetos:** nome busca, construtor cria. Um objeto novo só nasce quando executa código que constrói um (`[]`, `[0] * 3`, `lista[:]`, `list(...)`, `copy.copy(...)`). Citar um nome nunca cria nada.

---

## Pergunta 0

O que o Python faz quando executa `a = [1, 2, 3]`? Quantas "coisas" passam a existir na memória, e qual é a relação entre elas?

## Trecho 1 — `b = a`

```python
a = [1, 2, 3]
b = a
b.append(4)
print(a, a is b, id(a) == id(b))
print(id(a), id(b))
```

**Conceitos**
- `id(x)` devolve a **identidade** do objeto (no CPython, o endereço de memória). Só vale dentro de uma execução: muda a cada vez que o programa roda.
- `a is b` faz exatamente a mesma pergunta que `id(a) == id(b)`.
- `b = a` não cria lista nova: cola um segundo nome no mesmo objeto.

**Contraste com imutável**
```python
x = 5
y = x
y += 1
print(x, y)   # 5 6
```
`int` é imutável: `y += 1` cria um `int` novo e recola `y` nele. A lista é alterada no lugar; o int é substituído.

**Pegadinha:** em lista, `a += [3]` altera **no lugar** (`__iadd__`), mas `a = a + [3]` **cria** uma lista nova. Os dois só são equivalentes para tipos imutáveis.

## Trecho 2 — default mutável

```python
def add(x, lst=[]):
    lst.append(x)
    return lst
print(add(1), add(2))
```

**Conceitos**
- O valor padrão é avaliado **uma vez, quando o `def` executa**, e fica guardado em `add.__defaults__`. Toda chamada sem `lst` reusa o mesmo objeto.
- Os argumentos de uma função são todos calculados, da esquerda para a direita, **antes** da chamada. O `print` só olha a lista depois que as duas chamadas já a alteraram.
- `return lst` devolve o objeto, não uma "foto" dele.

**Correção (padrão da comunidade)**
```python
def add_ok(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst
```
Use `is None` e não `if not lst`: o `not lst` trataria uma lista vazia passada de propósito como "ausente" e a substituiria.

**Trade-off:** o default mutável às vezes é usado de propósito como cache barato. Ele é rápido e não exige global, mas o estado fica escondido, é compartilhado por todos os chamadores e quebra testes.

## Trecho 3 — `* 3` copia referências

```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```

**Conceitos**
- `[0] * 3` roda **uma vez** e cria uma lista L. `[L] * 3` repete a **referência** a L três vezes. O `*` não sabe refazer o `[0] * 3`: ele só copia referências.
- `[0] * 3` não dá problema porque `int` é imutável.

**Correção**
```python
grid = [[0] * 3 for _ in range(3)]
```
Numa comprehension, a **expressão antes do `for` é reexecutada a cada volta**. Se ela constrói um objeto, nascem objetos novos; se só cita um nome, devolve o mesmo objeto em todas as voltas.

```python
linha = [0] * 3
[linha for _ in range(3)]     # busca: 3 referências para a mesma linha (bug)
[linha[:] for _ in range(3)]  # cria: 3 cópias independentes
[linha for _ in range(3)][:]  # bug: o [:] copia só a lista de fora
```

`[x for x in origem]` é uma **cópia rasa** de `origem`: a lista de fora é nova, os elementos são os mesmos.

## Seção 4 — cópia rasa vs profunda

```python
import copy
orig = [[1, 2], [3, 4]]
rasa = copy.copy(orig)        # o mesmo que orig[:] ou list(orig)
funda = copy.deepcopy(orig)
orig[0].append(99)
print(rasa, funda)            # [[1, 2, 99], [3, 4]] [[1, 2], [3, 4]]
```

- **Rasa:** lista de fora nova, objetos internos compartilhados.
- **Profunda:** copia tudo recursivamente.
- **Trade-off:** `deepcopy` dá isolamento total, mas custa O(tamanho total da estrutura) em tempo e memória. Para estruturas compartilhadas, uma alternativa melhor costuma ser torná-las imutáveis (tuplas, `frozen` dataclass, Pydantic `frozen=True`).

## Seção 5 — `is` vs `==`

- `==` compara **valor** (chama `__eq__`).
- `is` compara **identidade** (é o mesmo objeto?).
- Use `is` só com singletons: `None`, `True`, `False`.

## Ligação com produção (FastAPI / AI Engineering)

Qualquer objeto mutável criado uma vez e compartilhado entre requests vira bug de aliasing. O caso clássico: um `historico = []` no nível do módulo para o chat. Funciona no teste local, com um usuário, e em produção vaza as mensagens de um usuário para o contexto do LLM de outro.

---

## Questões da aula

**Previsões**
1. Pergunta 0 (acima).
2. Saída dos trechos 1, 2 e 3.

**Experimentos**
3. `print(add.__defaults__)`, `r1 = add(3)`, `print(r1 is add(4))`, `print([id(linha) for linha in grid])`.
4. `linha = [0] * 3; grid = [linha for _ in range(3)]; grid[0][0] = 1`: quais linhas mudam e quantos `id` diferentes aparecem?
5. `linha.append(9)` depois de montar `grid = [linha for _ in range(3)]`: o que acontece com o `grid`?
6. `fatiamento.py`: opções (a) e (b), quais linhas mudam e o valor de `grid[0] is grid[1]`.

**Desafios**
7. Reescrever o `grid` para que `grid[0][0] = 1` mude só a primeira linha.
8. Reescrever o `add` para que cada chamada sem `lst` comece com uma lista vazia nova.

**Checagem**
9. `[[0] * 3 for _ in range(3)]` muda o resultado do trecho 3?
10. Por que `y += 1` não altera o `x`, enquanto `b.append(4)` alterou o `a`?
11. Onde esse bug apareceria numa API FastAPI?
12. O que imprime `print(add_ok(1), add_ok(2))`?
13. Depois de `r1 = add_bug(3)`, o que `r1.append(100)` faz com `add_bug.__defaults__`?
14. `x = [[]] * 3; x[0].append("a"); print(x)`.
15. `a = [1, 2]; b = a; a = a + [3]; print(b)`. E com `a += [3]`?
16. Por que `lst is None` e não `if not lst`?
17. Config em `dict` com listas, compartilhada entre requests: `copy.copy` ou `copy.deepcopy`?
18. Cria ou busca: `[[] for _ in range(3)]`, `[linha for _ in range(3)]`, `[list(linha) for _ in range(3)]`, `[x for x in [1, 2, 3]]`.

## Não coberto nesta aula

- Trecho 5: `x = 257; y = 257; print(x is y)` no REPL vs em script (cache de inteiros).
