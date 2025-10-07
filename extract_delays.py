#!/usr/bin/env python3
"""extract_delays.py

Pequeno utilitário para extrair valores de atraso (Packet PDCP delay) de arquivos de log.

Uso:
  python extract_delays.py arquivo1.txt [arquivo2.txt ...] [--out FILE] [--to-ms] [--force]

Se --out não for fornecido e for passado somente um arquivo de entrada, o arquivo de saída será
  delays_<basename>.txt

O script procura o primeiro número em cada linha que contenha a string 'Packet PDCP delay'
e grava um valor por linha no arquivo de saída. Linhas sem número são ignoradas.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, Optional


NUM_RE = re.compile(r"(-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)")
MATCH_KEY = "Packet PDCP delay"


def extract_from_lines(lines: Iterable[str]) -> List[float]:
    out: List[float] = []
    for ln in lines:
        if MATCH_KEY in ln:
            m = NUM_RE.search(ln)
            if m:
                try:
                    val = float(m.group(1))
                    out.append(val)
                except Exception:
                    # ignore unparsable
                    continue
    return out


def process_file(path: Path) -> List[float]:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return extract_from_lines(f)


def write_values(path: Path, vals: Iterable[float], to_ms: bool = False) -> None:
    with path.open("w", encoding="utf-8") as f:
        for v in vals:
            if to_ms:
                f.write(f"{v/1e6:.6f}\n")
            else:
                # preserve integer-like formatting when possible
                if abs(v - int(v)) < 1e-9:
                    f.write(f"{int(v)}\n")
                else:
                    f.write(f"{v}\n")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Extrai valores 'Packet PDCP delay' de arquivos de log")
    p.add_argument("inputs", nargs="+", help="Arquivos de log de entrada")
    p.add_argument("--out", "-o", help="Arquivo de saída (se múltiplos inputs, sobrescreve neste arquivo)")
    p.add_argument("--to-ms", action="store_true", help="Converter os valores de ns para ms")
    p.add_argument("--force", action="store_true", help="Permitir sobrescrever arquivo de saída")
    p.add_argument("--verbose", "-v", action="store_true", help="Mais informação")
    args = p.parse_args(argv)

    input_paths = [Path(x) for x in args.inputs]

    if args.out:
        out_path = Path(args.out)
        if out_path.exists() and not args.force:
            p.error(f"Arquivo de saída {out_path} já existe. Use --force para sobrescrever")
        all_vals: List[float] = []
        for ip in input_paths:
            if args.verbose:
                print(f"Lendo {ip}...")
            if not ip.exists():
                print(f"Aviso: {ip} não encontrado, pulando")
                continue
            vals = process_file(ip)
            if args.verbose:
                print(f"  encontrados {len(vals)} valores em {ip}")
            all_vals.extend(vals)
        write_values(out_path, all_vals, to_ms=args.to_ms)
        if args.verbose:
            print(f"Escrito {len(all_vals)} valores em {out_path}")
        return 0
    else:
        # sem --out: para cada input, gerar delays_<basename>.txt
        for ip in input_paths:
            if not ip.exists():
                print(f"Aviso: {ip} não encontrado, pulando")
                continue
            vals = process_file(ip)
            out_name = ip.parent / f"delays_{ip.stem}.txt"
            if out_name.exists() and not args.force:
                print(f"Arquivo {out_name} já existe. Use --force para sobrescrever ou passe --out")
                continue
            write_values(out_name, vals, to_ms=args.to_ms)
            if args.verbose:
                print(f"Escrito {len(vals)} valores em {out_name}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
