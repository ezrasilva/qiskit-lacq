# Cola de comandos

## Git

| Comando | O que faz |
| --- | --- |
| `git config --global user.name "Seu Nome"` | Diz ao Git quem você é (uma vez por máquina) |
| `git config --global user.email "voce@email.com"` | E-mail que assina seus commits |
| `git clone <url>` | Baixa um repositório do GitHub |
| `git status` | Mostra o que mudou e o que está preparado |
| `git add <arquivo>` | Prepara o arquivo para o próximo commit |
| `git commit -m "mensagem"` | Salva um ponto na história, com uma legenda |
| `git push` | Envia seus commits ao GitHub |
| `git pull` | Traz as mudanças do GitHub para a sua máquina |
| `git checkout -b <nome>` | Cria uma branch nova e muda para ela |
| `git log --oneline` | Lista os commits, um por linha |

**No GitHub:** *Fork* cria a sua cópia de um repositório. *Pull request* pede para a sua branch entrar no projeto original. Tecla `.` em qualquer repositório abre o editor web.

## Qiskit 2.x

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(2)      # 2 qubits, todos começam em |0⟩
qc.h(0)                     # Hadamard: superposição
qc.x(1)                     # X: inverte 0 ↔ 1
qc.cx(0, 1)                 # CNOT: controle 0, alvo 1
qc.measure_all()            # mede todos os qubits
qc.draw("mpl")              # desenha o circuito

resultado = StatevectorSampler().run([qc], shots=1000).result()
contagens = resultado[0].data.meas.get_counts()
plot_histogram(contagens)
```

| Porta | Método | Efeito |
| --- | --- | --- |
| Hadamard | `qc.h(q)` | Cria superposição de 0 e 1 |
| X (NOT) | `qc.x(q)` | Troca 0 por 1 |
| Z | `qc.z(q)` | Inverte a fase de 1 |
| CNOT | `qc.cx(c, a)` | Inverte o alvo quando o controle é 1 |

**Leitura dos resultados:** o qubit 0 é o bit mais à direita. `"01"` quer dizer qubit 0 = 1 e qubit 1 = 0.

**Tutorial antigo não funciona?** `execute()` e `qiskit.Aer` foram removidos no Qiskit 1.0. Use as primitivas, como `StatevectorSampler`, mostradas acima.
