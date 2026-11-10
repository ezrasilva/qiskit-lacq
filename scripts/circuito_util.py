"""Funções compartilhadas pela validação dos PRs e pela galeria."""

from __future__ import annotations

import importlib.util
import re
from dataclasses import dataclass, field
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

SHOTS = 1000
SEMENTE = 42
LIMIAR = 0.02  # resultados abaixo de 2% dos disparos contam como ruído estatístico
MAX_QUBITS = 6
CAMPOS = ("AUTOR", "GITHUB", "TITULO", "DESCRICAO", "ESPERADO")
PADROES_DO_MODELO = {
    "AUTOR": "Seu Nome",
    "GITHUB": "seu-usuario",
    "TITULO": "Nome curto do circuito",
    "DESCRICAO": "Uma frase explicando o que o circuito faz.",
}


@dataclass
class Relatorio:
    arquivo: Path
    erros: list[str] = field(default_factory=list)
    autor: str = ""
    github: str = ""
    titulo: str = ""
    descricao: str = ""
    esperado: set[str] = field(default_factory=set)
    contagens: dict[str, int] = field(default_factory=dict)
    qubits: int = 0
    profundidade: int = 0
    desenho: str = ""

    @property
    def ok(self) -> bool:
        return not self.erros

    @property
    def observados(self) -> set[str]:
        return {r for r, n in self.contagens.items() if n / SHOTS >= LIMIAR}


def carregar_modulo(caminho: Path):
    nome = "circuito_" + re.sub(r"\W", "_", caminho.stem)
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def avaliar(caminho: Path, checar_nome: bool = True) -> Relatorio:
    rel = Relatorio(arquivo=caminho)

    try:
        mod = carregar_modulo(caminho)
    except Exception as e:  # erro de sintaxe, import errado etc.
        rel.erros.append(f"O arquivo não pôde ser executado: {type(e).__name__}: {e}")
        return rel

    faltando = [c for c in CAMPOS if not hasattr(mod, c)]
    if not hasattr(mod, "montar"):
        faltando.append("montar()")
    if faltando:
        rel.erros.append("Faltam campos do modelo: " + ", ".join(faltando))
        return rel

    rel.autor = str(mod.AUTOR).strip()
    rel.github = str(mod.GITHUB).strip()
    rel.titulo = str(mod.TITULO).strip()
    rel.descricao = str(mod.DESCRICAO).strip()

    for campo, padrao in PADROES_DO_MODELO.items():
        if str(getattr(mod, campo)).strip() == padrao:
            rel.erros.append(f"Preencha {campo}: ainda está com o texto do modelo.")

    if checar_nome and rel.github.lower() != caminho.stem.lower():
        rel.erros.append(
            f"GITHUB = \"{rel.github}\", mas o arquivo se chama {caminho.name}. "
            f"O nome do arquivo deve ser o seu usuário: circuitos/{rel.github.lower()}.py"
        )

    esperado = mod.ESPERADO
    if isinstance(esperado, str) or not all(isinstance(r, str) for r in esperado):
        rel.erros.append('ESPERADO deve ser um conjunto de strings entre aspas, como {"00", "11"}.')
        return rel
    rel.esperado = {r.replace(" ", "") for r in esperado}

    try:
        qc = mod.montar()
    except Exception as e:
        rel.erros.append(f"montar() deu erro: {type(e).__name__}: {e}")
        return rel

    if not isinstance(qc, QuantumCircuit):
        rel.erros.append("montar() deve retornar um QuantumCircuit.")
        return rel

    rel.qubits = qc.num_qubits
    rel.profundidade = qc.depth()
    rel.desenho = str(qc.draw(output="text", fold=-1))

    if qc.num_qubits > MAX_QUBITS:
        rel.erros.append(f"Use no máximo {MAX_QUBITS} qubits (o seu tem {qc.num_qubits}).")
        return rel
    if qc.count_ops().get("measure", 0) == 0:
        rel.erros.append("O circuito não mede nada. Termine com qc.measure_all().")
        return rel

    try:
        sampler = StatevectorSampler(seed=SEMENTE)
        resultado = sampler.run([qc], shots=SHOTS).result()[0]
        rel.contagens = dict(resultado.join_data().get_counts())
    except Exception as e:
        rel.erros.append(f"A simulação falhou: {type(e).__name__}: {e}")
        return rel

    faltam = rel.esperado - rel.observados
    sobram = rel.observados - rel.esperado
    if faltam or sobram:
        msg = "O resultado não bateu com ESPERADO."
        if faltam:
            msg += f" Esperado, mas não apareceu: {sorted(faltam)}."
        if sobram:
            msg += f" Apareceu, mas não estava em ESPERADO: {sorted(sobram)}."
        msg += " Dica: o qubit 0 é o bit mais à direita."
        rel.erros.append(msg)

    return rel


def resumo_contagens(contagens: dict[str, int], limite: int = 4) -> str:
    ordenado = sorted(contagens.items(), key=lambda kv: (-kv[1], kv[0]))
    partes = [f"`{r}` {n / SHOTS:.0%}" for r, n in ordenado[:limite]]
    if len(ordenado) > limite:
        partes.append(f"+{len(ordenado) - limite}")
    return " · ".join(partes)
