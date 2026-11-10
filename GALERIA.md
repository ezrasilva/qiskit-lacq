# Galeria de circuitos

Circuitos criados pela turma do minicurso **GitHub + Qiskit** no Qiskit Fall Fest 2026 (LACQ / UFPA).
Cada um entrou por um pull request, foi validado pelo robô e revisado antes do merge.

> Este arquivo é gerado automaticamente por `scripts/gerar_galeria.py`. Não edite à mão.

**1 circuito** · 2 qubits no total · 1000 execuções cada

| # | Circuito | Autor | Qubits | Profundidade | Resultados medidos |
|---|---|---|---|---|---|
| 1 | **Estado de bell**<br>cria uma superposição com 2 qubits. | [Esdras](https://github.com/ezrasilva) | 2 | 3 | `00` 50% · `11` 50% |

## Os circuitos

<details>
<summary><b>Estado de bell</b> · Esdras</summary>

```text
        ┌───┐      ░ ┌─┐   
   q_0: ┤ H ├──■───░─┤M├───
        └───┘┌─┴─┐ ░ └╥┘┌─┐
   q_1: ─────┤ X ├─░──╫─┤M├
             └───┘ ░  ║ └╥┘
meas: 2/══════════════╩══╩═
                      0  1 
```
</details>

