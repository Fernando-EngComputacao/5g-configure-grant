#!/usr/bin/env python3
"""Gera uma única figura com os 3 gráficos (10MHz, 20MHz, 40MHz).

O script procura arquivos de atrasos nas pastas irmãs `10mhz`, `20mhz`, `40mhz`
dentro da pasta `metricas` e plota, para cada banda, um boxplot comparando:
  - RB-OFDMA
  - 5GL-OFDMA
  - Sym-OFDMA
  - 5GL-TDMA

Salva a figura em `metricas/geral/geral.png` por padrão.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np


FREQS = ["10MHz", "20MHz", "40MHz"]
FOLDERS = {"10MHz": "10mhz", "20MHz": "20mhz", "40MHz": "40mhz"}

PATTERNS = {
    "sym": "delays_sym*{tag}*.txt",
    "rb": "delays_rb*{tag}*.txt",
    "tdma": "delays_5gl_tdma*{tag}*.txt",
    "gl_ofdma": "delays_5gl_ofdma*{tag}*.txt",
}


def find_file(folder: Path, pattern: str) -> Optional[Path]:
    matches = list(folder.glob(pattern))
    return matches[0] if matches else None


def load_values(path: Path) -> np.ndarray:
    try:
        vals = np.loadtxt(path)
        return np.atleast_1d(vals)
    except Exception:
        # Return empty array on failure
        return np.array([], dtype=float)


def gather_for_freq(metricas_dir: Path, freq_tag: str) -> Dict[str, np.ndarray]:
    folder_name = FOLDERS.get(freq_tag)
    if not folder_name:
        raise ValueError(f"Freq tag {freq_tag} desconhecida")
    folder = metricas_dir / folder_name
    out: Dict[str, np.ndarray] = {}
    for key, pat in PATTERNS.items():
        pattern = pat.format(tag=freq_tag)
        f = find_file(folder, pattern)
        if f:
            out[key] = load_values(f)
        else:
            out[key] = np.array([], dtype=float)
    return out


def plot_all(metricas_dir: Path, out_file: Path, show: bool = False) -> None:
    labels = ["RB-OFDMA", "5GL-OFDMA", "Sym-OFDMA", "5GL-TDMA"]
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))  # Removido sharey=True para ticks independentes

    for ax, freq in zip(axes, FREQS):
        data = gather_for_freq(metricas_dir, freq)
        arrays = [data["rb"], data["gl_ofdma"], data["sym"], data["tdma"]]
        # convert to ms
        arrays_ms = [arr / 1e6 if arr.size else arr for arr in arrays]

        # print basic stats
        print(f"--- {freq} ---")
        for lab, arr in zip(labels, arrays_ms):
            if arr.size:
                print(f"{lab}: n={len(arr)} mean={np.mean(arr):.4f} ms std={np.std(arr):.4f} ms")
            else:
                print(f"{lab}: (arquivo não encontrado ou vazio)")

        # For boxplot, if an array is empty replace with [np.nan] so labels align but will not show
        plot_data = [arr if arr.size else np.array([np.nan]) for arr in arrays_ms]

        ax.boxplot(plot_data, tick_labels=labels, showfliers=False)  # Usar tick_labels em vez de labels (deprecated)
        ax.set_title(freq)
        ax.set_ylabel("Latency (ms)")
        ax.grid(True)

    plt.suptitle("Comparativo de Packet PDCP Delay")  # Adicionado título
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    out_file.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_file)
    print(f"Figura salva em: {out_file}")
    if show:
        plt.show()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Gera figura com 10/20/40 MHz em um único arquivo")
    parser.add_argument("--out", "-o", help="Caminho do arquivo de saída (PNG)", default=None)
    parser.add_argument("--show", action="store_true", help="Mostrar a figura após gerar")
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    metricas_dir = script_dir.parent
    out_file = Path(args.out) if args.out else script_dir / "geral.png"

    plot_all(metricas_dir, out_file, show=args.show)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
