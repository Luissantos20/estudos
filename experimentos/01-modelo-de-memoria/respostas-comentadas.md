# Respostas comentadas — Aula 1: modelo de memória

Para cada questão do `aula.md`: a minha resposta (ver `minhas-respostas.md`), o veredito, a resposta certa e o porquê. No fim, as dúvidas que tirei durante a aula.

Legenda: ✅ certo · ⚠️ parcialmente certo · ❌ errado · — não respondi

---

## Previsões

### 1. Pergunta 0 ⚠️
**Certo:** `a` é uma referência para a lista.
**Errado:** os valores 1, 2 e 3 não moram dentro da lista. A lista guarda **referências** para objetos `int`, que vivem em outro lugar da memória. Esse detalhe explica o trecho 3.

### 2. Trecho 1 ⚠️ (2 de 3)
**Real:** `[1, 2, 3, 4] True True`
**Por quê:** `a is b` é a mesma pergunta que `id(a) == id(b)`, e `id()` devolve a identidade do objeto. As duas não podem discordar, então `True False` era impossível. `b = a` só colou um segundo nome no mesmo objeto.

### 2. Trecho 2 ⚠️
**Real:** `[1, 2] [1, 2]`
**Certo:** percebi que o `1` sobrevive entre chamadas.
**Faltou:** (a) por que ele sobrevive: o default é criado uma vez só, no `def`; (b) o `print` recebe as duas chamadas já executadas, e as duas devolvem o mesmo objeto, que no momento do print já é `[1, 2]`.

### 2. Trecho 3 ❌
**Real:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]`
**Por quê:** `[linha] * 3` repete três referências para a **mesma** linha. Alterar `grid[0][0]` altera essa única linha, e as três posições mostram a mudança.

## Experimentos

### 4. `[linha for _ in range(3)]` ❌
**Real:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]`, com o mesmo `id` quatro vezes (as três linhas e o próprio `linha`).
**Por quê:** a comprehension reexecuta a expressão `linha`, que só **busca** o objeto pelo nome. Nenhuma lista é criada dentro do `for`. O nome não cria objeto: ele é uma etiqueta num objeto que já existe.

### 5. `linha.append(9)` —
**Real:** `[[0, 0, 0, 9], [0, 0, 0, 9], [0, 0, 0, 9]]`. Com `[linha[:] for _ in range(3)]`, o `grid` não muda.
**Por quê:** é a prova de que o `grid` só guarda referências para `linha`.

### 6. `fatiamento.py` opção (b) ❌
**Real:** `[[1, 0, 0], [1, 0, 0], [1, 0, 0]]`, `grid_b[0] is grid_b[1]` → `True`, quatro `id` iguais.
**Por quê:** o `[:]` roda uma vez, no fim, e copia a lista **de fora**. A cópia rasa copia as referências, não os objetos internos.
**Opção (a):** `[[1, 0, 0], [0, 0, 0], [0, 0, 0]]`, `False`, três `id` diferentes, porque o `[:]` roda dentro da expressão, uma vez por volta.

## Desafios

### 7. Reescrever o `grid` ✅
`[[0] * 3 for _ in range(3)]`: o `[0] * 3` executa a cada volta e cria três listas.

### 8. Reescrever o `add` —
```python
def add_ok(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst
```
A lista é criada dentro da função, ou seja, a cada chamada.

## Checagem

### 9. Comprehension no trecho 3 —
Sim, muda: só a primeira linha vira `[1, 0, 0]`, porque cada volta cria uma lista nova.

### 10. `y += 1` vs `b.append(4)` —
`int` é imutável: o `+=` cria um objeto novo e recola o nome. O `append` altera a lista no lugar.

### 11. Onde aparece numa API FastAPI —
Em qualquer objeto mutável criado uma vez, no nível do módulo, e usado por todos os requests. Exemplo: `historico = []` global para o chat, que vaza as mensagens de um usuário para o contexto do LLM de outro.

### 12. `print(add_ok(1), add_ok(2))` ✅
`[1] [2]`. O raciocínio está certo: a lista nasce a cada chamada.

### 13. `r1.append(100)` ✅
`add_bug.__defaults__` vira `([1, 2, 3, 100],)`: uma **tupla** que contém a lista. O raciocínio está certo: `r1` e o default são o mesmo objeto.

### 14. `[[]] * 3` ✅
`[['a'], ['a'], ['a']]`, com aspas porque `"a"` é string. Três referências para a mesma lista vazia.

### 15. `a = a + [3]` vs `a += [3]` —
- `a = a + [3]`: o `+` cria uma lista nova e recola `a`. `print(b)` → `[1, 2]`.
- `a += [3]`: em lista, o `+=` altera no lugar. `print(b)` → `[1, 2, 3]`.

### 16. `is None` vs `if not lst` —
`not lst` é `True` também para `[]`. Uma lista vazia passada de propósito seria trocada por uma nova, e a do chamador ficaria vazia. `is None` testa exatamente "não me passaram nada".

### 17. `copy` vs `deepcopy` na config —
`deepcopy`: a config é pequena, e vazamento entre requests é o pior bug possível. Melhor ainda: tornar a config imutável, para que o aliasing não possa acontecer.

### 18. Cria ou busca ⚠️ (3 de 4)
1. ✅ cria
2. ✅ busca
3. ✅ cria
4. ❌ só **busca**. O `x` aponta para um objeto diferente a cada volta, mas todos já existiam na lista de origem. O que a comprehension cria é só a lista de fora. `[x for x in origem]` é uma cópia rasa.

## Diagnóstico ❌
Eu disse que `[linha for _ in range(3)]` "cria uma lista `[0, 0, 0]` 3 vezes". Essa era a crença errada que causou os erros 4, 6 e 18.
- Nenhuma lista é criada dentro desse `for`: `linha` só busca o objeto. **Nome busca, construtor cria.**
- O resultado seria `[linha, linha, linha]`, não `[[linha], [linha], [linha]]`. Os colchetes extras criariam três listas novas.

---

## Dúvidas que tirei

### Python 3.11 ou 3.12?
O 3.11.9 serve para a aula. Instalar a 3.12 não quebra o trabalho: no Windows as versões convivem lado a lado (launcher `py -3.11`, `py -3.12`) e cada projeto tem seu venv. O risco é só a 3.12 virar o `python` padrão para scripts sem venv. No projeto-eixo, a versão que importa é a da imagem Docker. Decisão adiada para quando o projeto nascer.

### Por que a lista aparece duas vezes no `print(add_bug(1), add_bug(2))`?
O `print` recebeu dois argumentos e imprime cada um. O Python calcula os dois antes de chamar o `print`. As duas chamadas devolvem o mesmo objeto, que já virou `[1, 2]`. Separando em `print(add_bug(1))` e `print(add_bug(2))`, aparecem `[1]` e depois `[1, 2]`.

### Por que `r1 is add_bug(4)` é `True`?
Não é porque a função "altera o objeto de `r1`". É porque `add_bug(4)` **devolve o mesmo objeto** que já está em `r1`. A alteração explica o conteúdo `[1, 2, 3, 4]`; o `True` vem só de ser o mesmo objeto. E quem adiciona o `3` é o `add_bug(3)`: `r1` é só um nome.

### Por que a comprehension cria 3 listas e a multiplicação não?
A diferença é quantas vezes `[0] * 3` executa. Na multiplicação, roda uma vez e o `*` copia a referência. Na comprehension, a expressão antes do `for` roda a cada volta. Experimento: uma função `nova_linha()` com `print` mostra uma execução no primeiro caso e três no segundo.

### O que é `[:]`?
Fatiamento: `lista[início:fim]` cria uma lista nova com um pedaço da original. `[:]` pega tudo e faz uma cópia rasa, igual a `copy.copy(lista)` ou `list(lista)`. Cada execução de `[:]` cria uma lista nova.

### Regra final
> Dentro de uma comprehension, nasce um objeto novo a cada volta **somente quando a expressão antes do `for` contém código que constrói um objeto**. Se a expressão só cita um nome, ela devolve o mesmo objeto em todas as voltas.
