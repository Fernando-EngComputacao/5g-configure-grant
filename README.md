# Extração de atrasos (Packet PDCP delay)

Este repositório contém um arquivo de logs (por exemplo `Sym_20Hz.txt`) e uma pequena ferramenta para extrair os valores de "Packet PDCP delay" que serão usados nas métricas.

## 1. Objetivo

Extrair as linhas relevantes do log que contêm "Packet PDCP delay" e gerar um arquivo com os valores numéricos (em nanosegundos). Isso facilita cálculo de médias, plotagem e comparação entre cenários (por exemplo, Sym e RB).

## 2. Comandos Unix/Linux sugeridos (conforme sua mensagem)

Se você estiver num ambiente Linux ou macOS com `grep` e `awk` disponíveis, use:

```sh
# Para o cenário Sym (exemplo)
grep "Packet PDCP delay" Sym_20Hz.txt | awk '{print $4}' > delays_sym.txt

# Para o cenário RB (se tiver outro arquivo chamado RB_20Hz.txt)
grep "Packet PDCP delay" RB_20Hz.txt | awk '{print $4}' > delays_rb.txt
```

Isso cria arquivos `delays_sym.txt` e `delays_rb.txt` contendo apenas os valores (em ns), uma linha por valor.

## 3. Alternativas para PowerShell (Windows)

No PowerShell (Windows), `grep`/`awk` normalmente não estão presentes. Use:

```powershell
# Extrai o token onde costuma estar o número (4º token) e grava em delays_sym.txt
Get-Content Sym_20Hz.txt | Select-String "Packet PDCP delay" | ForEach-Object { ($_ -split '\s+')[3] } | Set-Content delays_sym.txt

# Conversão para milissegundos (opcional)
Get-Content delays_sym.txt | ForEach-Object { [double]$_/1e6 } | Set-Content delays_sym_ms.txt
```

Observação: adaptações podem ser necessárias se a estrutura da linha variar; veja abaixo uma alternativa em Python mais robusta.

## 4. Utilitário Python (cross-platform)

Incluí um pequeno script `extract_delays.py` que faz a extração de forma robusta (procura pelo primeiro número na linha) e pode opcionalmente converter para ms.

Uso básico:

```sh
# Extrai valores de Sym_20Hz.txt e salva em delays_sym.txt
python extract_delays.py Sym_20Hz.txt --out delays_sym.txt

# Extrai e converte para ms
python extract_delays.py Sym_20Hz.txt --out delays_sym_ms.txt --to-ms
```

Se quiser processar múltiplos arquivos, passe vários nomes de arquivo na chamada.

## 5. Próximos passos sugeridos

- Calcular estatísticas (média, mediana, desvio padrão) e plotar histogramas/CCDFs com `matplotlib`/`numpy`/`pandas`.
- Comparar cenários: usar arquivos `delays_sym.txt` e `delays_rb.txt` gerados para plotar curvas lado a lado.

Exemplo rápido em Python para estatísticas (pode ser usado em um REPL):

```python
import numpy as np
vals = np.loadtxt('delays_sym.txt')  # em ns
print('count', len(vals))
print('mean (ms)', vals.mean()/1e6)
print('median (ms)', np.median(vals)/1e6)
print('std (ms)', vals.std()/1e6)
```

## 6. Notas e cuidados

- Os valores extraídos estão em nanosegundos (ns). Converter para ms facilita interpretação humana (1 ms = 1e6 ns).
- Verifique linhas atípicas (não numéricas) — o script Python ignora linhas sem números.
- Se o número não estiver no 4º token em todas as linhas, prefira a extração por regex (script Python) em vez de pegar o 4º token.

---

Se quiser, posso também:
- Rodar o script aqui para extrair de `Sym_20Hz.txt` e salvar `delays_sym.txt` no workspace.
- Adicionar um script de análise simples (estatísticas + plots).

Diga qual opção prefere que eu executo a seguir.