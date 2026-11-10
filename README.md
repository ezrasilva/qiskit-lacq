# GitHub + Qiskit · Qiskit Fall Fest 2026 (LACQ / UFPA)

Repositório do minicurso **GitHub + Qiskit: do primeiro commit ao primeiro circuito quântico**.

Ao final, cada pessoa terá:

1. um repositório próprio no GitHub, com o primeiro commit;
2. um notebook Qiskit com o estado de Bell rodando;
3. um circuito seu na [galeria da turma](GALERIA.md), entregue por pull request.

## O que tem aqui

| Caminho | Para quê |
| --- | --- |
| [`notebooks/bell.ipynb`](notebooks/bell.ipynb) | Atividade 2: do qubit em superposição ao estado de Bell |
| [`circuitos/_modelo.py`](circuitos/_modelo.py) | Atividade 3: modelo do seu circuito |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Atividade 3: passo a passo do pull request e regras do desafio |
| [`COLA.md`](COLA.md) | Cola de comandos Git e Qiskit |
| [`GALERIA.md`](GALERIA.md) | Mural com os circuitos aceitos, atualizado sozinho a cada merge |

## Começar sem instalar nada

Abra o notebook no Google Colab:

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ezrasilva/qiskit-lacq/blob/main/notebooks/bell.ipynb)

## Ou na sua máquina

```bash
git clone https://github.com/ezrasilva/qiskit-lacq.git
cd qiskit-lacq
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/bell.ipynb               # ou abra no VS Code
```

## Atividades

**1 · Primeiro commit.** Crie no GitHub um repositório seu chamado `meu-qiskit` (marque *Add a README file*), clone, edite o README, faça commit e push. Os comandos estão na [cola](COLA.md).

**2 · Estado de Bell.** Rode `notebooks/bell.ipynb`, complete a célula marcada e salve uma cópia no seu `meu-qiskit` (no Colab: *Arquivo › Salvar uma cópia no GitHub*).

**3 · Seu circuito na galeria.** Siga o [CONTRIBUTING.md](CONTRIBUTING.md): fork, branch, um arquivo em `circuitos/`, pull request. Um robô valida o circuito e, depois da revisão, ele entra na galeria.

## Para continuar estudando

- [Documentação do Qiskit](https://quantum.cloud.ibm.com/docs)
- [IBM Quantum Platform](https://quantum.cloud.ibm.com), para rodar em hardware real
- [Qiskit no GitHub](https://github.com/Qiskit/qiskit): o mesmo fluxo de pull request que você usou hoje
