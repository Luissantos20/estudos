"""
Aula 1 — Modelo de memória do Python (semana 1, 10–11/11/2026)

A ideia central, que explica tudo abaixo:
    Em Python, toda variável é um NOME colado num OBJETO.
    O `=` nunca copia: ele só cola o nome no objeto que está à direita.

Bug de aliasing = dois nomes no mesmo objeto + objeto mutável.
Sem um dos dois, o bug não acontece.

Rode com:  python3 memoria.py
"""

import copy


def titulo(texto):
    print(f"\n=== {texto} ===")


# ---------------------------------------------------------------------------
# 1) ALIASING: `b = a` não cria uma lista nova
# ---------------------------------------------------------------------------
# Conceito: `a` e `b` são dois nomes para o MESMO objeto list.
#   a ──┐
#       ├──► [1, 2, 3]
#   b ──┘
# Mexer no objeto por um nome aparece pelo outro.
#
# id(x)  = identidade do objeto (no CPython, o endereço de memória).
# a is b = exatamente o mesmo que id(a) == id(b).
#
# Sua previsão: [1, 2, 3, 4] True False
# Real:         [1, 2, 3, 4] True True
# Por quê: `is` e `id()` fazem a mesma pergunta; não podem discordar.

titulo("1) aliasing")
a = [1, 2, 3]
b = a
b.append(4)
print(a, a is b, id(a) == id(b))  # [1, 2, 3, 4] True True
print(id(a), id(b))               # o mesmo número duas vezes

# Contraste: com um objeto IMUTÁVEL (int), não existe "mexer no objeto".
# `y += 1` cria um int NOVO e recola o nome y nele; x continua no 5.
x = 5
y = x
y += 1
print(x, y, x is y)  # 5 6 False


# ---------------------------------------------------------------------------
# 2) DEFAULT MUTÁVEL: `lst=[]` é criado uma vez só
# ---------------------------------------------------------------------------
# Conceito: os valores padrão são avaliados quando o `def` EXECUTA,
# não a cada chamada. A lista fica guardada em add_bug.__defaults__
# e toda chamada sem `lst` reusa o MESMO objeto.
#
# Segunda armadilha: print(add_bug(1), add_bug(2)) executa as DUAS chamadas
# antes de imprimir. As duas devolvem o mesmo objeto, que já é [1, 2].
# `return lst` devolve o objeto, não uma "foto" dele.
#
# Sua previsão: [1] [1, 2]
# Real:         [1, 2] [1, 2]

titulo("2) default mutável")


def add_bug(x, lst=[]):
    lst.append(x)
    return lst


print(add_bug.__defaults__)        # ([],)  -> a lista nasceu no `def`
print(add_bug(1), add_bug(2))      # [1, 2] [1, 2]
print(add_bug.__defaults__)        # ([1, 2],) -> é a mesma lista, crescendo
r1 = add_bug(3)
print(r1 is add_bug(4))            # True -> toda chamada devolve o mesmo objeto
print(r1)                          # [1, 2, 3, 4]


# CORREÇÃO (padrão da comunidade): use None como sentinela
# e crie a lista DENTRO da função, ou seja, a cada chamada.
def add_ok(x, lst=None):
    if lst is None:        # `is None` e não `== None`: None é um objeto único
        lst = []
    lst.append(x)
    return lst


print(add_ok(1), add_ok(2))        # [1] [2]
print(add_ok(3) is add_ok(4))      # False -> cada chamada tem a sua lista


# ---------------------------------------------------------------------------
# 3) `* 3` COPIA REFERÊNCIAS, não objetos
# ---------------------------------------------------------------------------
# Conceito: uma lista guarda REFERÊNCIAS para objetos, não os valores.
# [linha] * 3 cria 3 referências para a MESMA linha:
#   grid ──► [ ref, ref, ref ]
#               └────┼────┘
#                    ▼
#               [0, 0, 0]   <- uma linha só
#
# [0] * 3 não dá problema porque int é imutável:
# grid[0][0] = 1 troca a referência daquela posição, não altera o 0.
#
# Sua previsão: [[1,0,0],[0,0,0],[0,0,0]]
# Real:         [[1,0,0],[1,0,0],[1,0,0]]

titulo("3) multiplicação de lista")
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)                               # as 3 linhas mudaram
print([id(linha) for linha in grid])      # o MESMO id 3 vezes

# CORREÇÃO (a sua, e está certa): a comprehension executa [0] * 3
# a cada volta do loop, criando 3 listas diferentes.
grid1 = [[0] * 3 for _ in range(3)]
grid1[0][0] = 1
print(grid1)                              # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
print([id(linha) for linha in grid1])     # 3 ids diferentes


# ---------------------------------------------------------------------------
# 4) CÓPIA RASA vs PROFUNDA
# ---------------------------------------------------------------------------
# copy.copy (rasa): cria uma lista externa NOVA, mas com as MESMAS
#                   referências para as listas internas.
# copy.deepcopy:    copia tudo, recursivamente.
#
# Regra prática: se a lista tem coisas mutáveis dentro, a rasa não protege.

titulo("4) cópia rasa vs profunda")
orig = [[1, 2], [3, 4]]
rasa = copy.copy(orig)          # o mesmo que orig[:] ou list(orig)
funda = copy.deepcopy(orig)
orig[0].append(99)
print(rasa)                     # [[1, 2, 99], [3, 4]] -> compartilha as internas
print(funda)                    # [[1, 2], [3, 4]]     -> independente
print(rasa is orig, rasa[0] is orig[0], funda[0] is orig[0])  # False True False


# ---------------------------------------------------------------------------
# 5) `is` vs `==`
# ---------------------------------------------------------------------------
# ==  compara VALOR    (chama __eq__)
# is  compara IDENTIDADE (é o mesmo objeto?)
# Use `is` só para singletons: None, True, False.

titulo("5) is vs ==")
l1 = [1, 2]
l2 = [1, 2]
print(l1 == l2, l1 is l2)       # True False -> mesmo valor, objetos diferentes