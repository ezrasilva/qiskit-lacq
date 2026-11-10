"""
Valida um pull request do desafio "Seu circuito na galeria".

Regras:
  - o PR só pode adicionar ou alterar circuitos/<login-de-quem-abriu>.py
  - o circuito precisa seguir o modelo e produzir os resultados de ESPERADO

Uso no GitHub Actions (ver .github/workflows/validar.yml):
  python scripts/validar_pr.py --base <sha> --login <usuario>

Uso local, para testar antes de abrir o PR:
  python scripts/validar_pr.py circuitos/seu-usuario.py
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from circuito_util import SHOTS, avaliar, resumo_contagens  # noqa: E402


def arquivos_do_pr(base: str) -> list[tuple[str, str]]:
    saida = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", base, "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout
    pares = []
    for linha in saida.splitlines():
        status, caminho = linha.split("\t", 1)
        pares.append((status, caminho))
    return pares


def checar_regras(pares: list[tuple[str, str]], login: str) -> tuple[list[str], list[Path]]:
    erros = []
    permitido = f"circuitos/{login.lower()}.py"
    validar = []
    for status, caminho in pares:
        if caminho.lower() != permitido:
            erros.append(
                f"`{caminho}` ({'removido' if status == 'D' else 'alterado'}): "
                f"neste desafio o PR só pode mexer em `{permitido}`."
            )
        elif status == "D":
            erros.append(f"`{caminho}` foi removido. O PR deve adicionar o seu circuito.")
        else:
            validar.append(Path(caminho))
    if not pares:
        erros.append(f"O PR não tem mudanças. Crie `{permitido}` a partir de `circuitos/_modelo.py`.")
    return erros, validar


def escrever_resumo(texto: str) -> None:
    destino = os.environ.get("GITHUB_STEP_SUMMARY")
    if destino:
        with open(destino, "a", encoding="utf-8") as f:
            f.write(texto + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arquivos", nargs="*", help="arquivos para validar localmente")
    p.add_argument("--base", help="commit base do PR")
    p.add_argument("--login", help="usuário do GitHub que abriu o PR")
    p.add_argument("--dono", default=os.environ.get("GITHUB_REPOSITORY_OWNER", ""),
                   help="dono do repositório; os PRs dele não passam pela regra de arquivos")
    args = p.parse_args()

    erros_regra: list[str] = []
    if args.base and args.login:
        pares = arquivos_do_pr(args.base)
        if args.login.lower() == args.dono.lower():
            print(f"PR do dono do repositório ({args.login}): regra de arquivos ignorada.")
            alvos = [Path(c) for s, c in pares
                     if s != "D" and c.startswith("circuitos/") and c.endswith(".py")
                     and not Path(c).name.startswith("_")]
        else:
            erros_regra, alvos = checar_regras(pares, args.login)
    else:
        alvos = [Path(a) for a in args.arquivos]
        if not alvos:
            p.error("informe um arquivo, ex.: python scripts/validar_pr.py circuitos/seu-usuario.py")

    relatorios = [avaliar(a) for a in alvos]
    tudo_ok = not erros_regra and all(r.ok for r in relatorios)

    linhas = ["## ✅ Circuito aprovado pelo robô" if tudo_ok else "## ❌ Ainda falta ajustar", ""]
    for e in erros_regra:
        linhas.append(f"- {e}")
    for r in relatorios:
        linhas += ["", f"### `{r.arquivo}`", ""]
        if r.titulo:
            linhas.append(f"**{r.titulo}** · {r.autor} · {r.qubits} qubits · profundidade {r.profundidade}")
            linhas.append("")
        if r.contagens:
            linhas.append(f"Resultado em {SHOTS} execuções: {resumo_contagens(r.contagens, limite=8)}")
            linhas.append("")
            linhas.append(f"ESPERADO: {', '.join(f'`{x}`' for x in sorted(r.esperado))}")
            linhas.append("")
        for e in r.erros:
            linhas.append(f"- ❌ {e}")
        if r.desenho:
            linhas += ["", "```text", r.desenho, "```"]
    if tudo_ok:
        linhas += ["", "Agora é com a revisão humana: aguarde o comentário no PR."]
    else:
        linhas += ["", "Corrija, faça commit e push na mesma branch: o PR atualiza sozinho e o robô roda de novo."]

    texto = "\n".join(linhas)
    print(texto)
    escrever_resumo(texto)
    return 0 if tudo_ok else 1


if __name__ == "__main__":
    sys.exit(main())
