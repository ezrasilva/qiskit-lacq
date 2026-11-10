# Desafio: seu circuito na galeria

Cada pessoa contribui com **um circuito quântico** neste repositório por meio de um pull request (PR).
Um robô testa o circuito, uma pessoa revisa e, depois do merge, ele aparece na [galeria](GALERIA.md).

## Passo a passo

**1. Fork.** No topo desta página, clique em **Fork**. Você ganha uma cópia em `github.com/<voce>/qiskit-lacq`.

**2. Clone o seu fork e crie uma branch.**

```bash
git clone https://github.com/<voce>/qiskit-lacq.git
cd qiskit-lacq
git checkout -b circuito-<voce>
```

**3. Crie o seu arquivo a partir do modelo.** O nome do arquivo é o seu usuário do GitHub, em minúsculas.

```bash
cp circuitos/_modelo.py circuitos/<voce>.py
```

Abra `circuitos/<voce>.py`, preencha `AUTOR`, `GITHUB`, `TITULO`, `DESCRICAO`, monte o circuito em `montar()` e diga em `ESPERADO` quais resultados você espera medir.

**4. Teste na sua máquina (opcional, mas economiza tempo).**

```bash
python scripts/validar_pr.py circuitos/<voce>.py
```

**5. Commit e push.**

```bash
git add circuitos/<voce>.py
git commit -m "Adiciona circuito de <voce>"
git push -u origin circuito-<voce>
```

**6. Abra o pull request.** O GitHub mostra o botão **Compare & pull request**. Preencha o modelo do PR e envie.

> Sem Git na máquina? Faça tudo pelo site: no seu fork, entre em `circuitos/`, use **Add file › Create new file**, cole o modelo, e na hora de salvar escolha **Create a new branch** e **Propose changes**.

## As regras

| Regra | Por quê |
| --- | --- |
| Um arquivo por pessoa: `circuitos/<seu-usuario>.py` | Ninguém edita o mesmo arquivo, então não há conflito de merge |
| O PR só mexe no seu arquivo | Mantém a revisão simples e o histórico limpo |
| No máximo 6 qubits e pelo menos uma medição | O robô simula tudo em segundos |
| `ESPERADO` tem que bater com o que foi medido | É o seu palpite antes de rodar: é aqui que se aprende |

## O que o robô verifica

Em cada PR roda o check **Validar circuito / Robô do desafio**. Ele:

1. confere se o PR só alterou `circuitos/<seu-usuario>.py`;
2. executa o arquivo e confere os campos do modelo;
3. simula o circuito 1000 vezes;
4. compara os resultados que apareceram em pelo menos 2% das execuções com o seu `ESPERADO`.

✅ verde: vai para a revisão humana. ❌ vermelho: clique em **Details**, leia o motivo, corrija, faça commit e push **na mesma branch**. O PR se atualiza sozinho e o robô roda de novo.

## Erros comuns

| Mensagem do robô | O que fazer |
| --- | --- |
| *o arquivo se chama ... O nome do arquivo deve ser o seu usuário* | Renomeie o arquivo ou corrija `GITHUB` |
| *Preencha TITULO: ainda está com o texto do modelo* | Troque os textos de exemplo pelos seus |
| *Apareceu, mas não estava em ESPERADO: ['01']* | Lembre que o qubit 0 é o bit **mais à direita** |
| *O circuito não mede nada* | Termine `montar()` com `qc.measure_all()` |

## Ideias de circuito

- **Básico:** o estado de Bell sem a CNOT. O que muda?
- **Básico:** troque `h` por `x`. Qual resultado aparece?
- **Intermediário:** o estado GHZ de 3 qubits (`{"000", "111"}`).
- **Desafio:** duas portas `h` seguidas no mesmo qubit. Por que o resultado deixa de ser aleatório?
- **Desafio:** um circuito cujo `ESPERADO` tenha exatamente quatro resultados.

## Revisão e merge

Quem conduz o minicurso revisa os PRs com ✅ ao vivo: comenta, às vezes pede um ajuste e faz o merge.
Depois do merge, o workflow **Atualizar galeria** regenera o `GALERIA.md` em cerca de um minuto.
