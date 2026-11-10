"""
Modelo para o desafio "Seu circuito na galeria".

Como usar:
  1. Copie este arquivo para  circuitos/<seu-usuario-do-github>.py
     (ex.: circuitos/maria-silva.py)
  2. Preencha AUTOR, GITHUB, TITULO e DESCRICAO.
  3. Monte o seu circuito dentro de montar().
  4. Diga em ESPERADO quais resultados você espera medir.

Lembrete: o Qiskit escreve o qubit 0 como o bit mais à DIREITA.
Num circuito de 2 qubits com X só no qubit 0, o resultado é "01".
"""

from qiskit import QuantumCircuit

AUTOR = "Esdras"
GITHUB = "ezrasilva"
TITULO = "Estado de bell"
DESCRICAO = "cria uma superposição com 2 qubits."

# Resultados que você espera ver ao medir (strings de bits).
# Estado de Bell, por exemplo: {"00", "11"}
ESPERADO = {"00", "11"}


def montar() -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc
