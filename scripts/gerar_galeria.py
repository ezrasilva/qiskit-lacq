"""
Gera GALERIA.md com todos os circuitos de circuitos/ (exceto arquivos que começam com _).

Roda sozinho no GitHub Actions a cada merge (ver .github/workflows/galeria.yml).
Para gerar na sua máquina:  python scripts/gerar_galeria.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from circuito_util import SHOTS, avaliar, resumo_contagens  # noqa: E402

CABECALHO = """# Galeria de circuitos

Circuitos criados pela turma do minicurso **GitHub + Qiskit** no Qiskit Fall Fest 2026 (LACQ / UFPA).
Cada um entrou por um pull request, foi validado pelo robô e revisado antes do merge.

> Este arquivo é gerado automaticamente por `scripts/gerar_galeria.py`. Não edite à mão.
"""


def main() -> None:
    arquivos = sorted(
        (a for a in (RAIZ / "circuitos").glob("*.py") if not a.name.startswith("_")),
        key=lambda a: a.name.lower(),
    )
    relatorios = [avaliar(a) for a in arquivos]
    validos = [r for r in relatorios if r.ok]
    com_problema = [r for r in relatorios if not r.ok]

    linhas = [CABECALHO]
    if not validos:
        linhas.append("_Nenhum circuito ainda. O primeiro PR aceito aparece aqui._")
    else:
        total_qubits = sum(r.qubits for r in validos)
        n = len(validos)
        rotulo = "circuito" if n == 1 else "circuitos"
        linhas.append(f"**{n} {rotulo}** · {total_qubits} qubits no total · {SHOTS} execuções cada\n")
        linhas.append("| # | Circuito | Autor | Qubits | Profundidade | Resultados medidos |")
        linhas.append("|---|---|---|---|---|---|")
        for i, r in enumerate(validos, 1):
            autor = f"[{r.autor}](https://github.com/{r.github})"
            linhas.append(
                f"| {i} | **{r.titulo}**<br>{r.descricao} | {autor} | {r.qubits} | "
                f"{r.profundidade} | {resumo_contagens(r.contagens)} |"
            )
        linhas.append("\n## Os circuitos\n")
        for r in validos:
            linhas += [
                "<details>",
                f"<summary><b>{r.titulo}</b> · {r.autor}</summary>\n",
                "```text",
                r.desenho,
                "```",
                "</details>\n",
            ]

    if com_problema:
        linhas.append("\n## Fora da galeria por enquanto\n")
        for r in com_problema:
            linhas.append(f"- `{r.arquivo.relative_to(RAIZ)}`: {r.erros[0]}")

    (RAIZ / "GALERIA.md").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"GALERIA.md: {len(validos)} circuito(s), {len(com_problema)} com problema.")


if __name__ == "__main__":
    main()
