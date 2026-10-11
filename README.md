# Analisador de Evidências Forenses

Ferramenta em Python para inventário de arquivos, cálculo de hashes
SHA-256, identificação de arquivos com conteúdo idêntico e geração
de relatório técnico em formato TXT.

## Funcionalidades

- Inventário recursivo de arquivos e subpastas.
- Cálculo de hash SHA-256 por arquivo.
- Registro de caminho, tamanho e extensão.
- Identificação de grupos de arquivos com o mesmo SHA-256.
- Tratamento de erros de leitura.
- Geração automática de relatório TXT com data e hora em UTC.

## Requisitos

- Python 3.9 ou superior.
- Nenhuma biblioteca externa é necessária.

## Como executar

Execute no terminal:

```bash
python analisador.py
```

Informe o caminho da pasta que deseja analisar quando solicitado.

O relatório será salvo no diretório pai da pasta analisada,
com um nome semelhante a:

`relatorio_forense_20261011_201338.txt`

## Exemplo de teste

Crie dois arquivos com conteúdo idêntico e um terceiro com conteúdo
diferente. O programa deverá identificar os dois primeiros como um
grupo de duplicados, desde que seus hashes SHA-256 coincidam.

## Limitações e cuidados

- O hash SHA-256 auxilia na verificação de integridade, mas não comprova
  sozinho a autenticidade, a origem ou a cadeia de custódia da evidência.
- Esta versão não implementa aquisição forense, bloqueio de escrita,
  assinatura digital ou registro auditável de cadeia de custódia.
- Faça testes com cópias de arquivos e evite modificar evidências originais.
- O relatório registra os resultados obtidos durante a execução;
  não constitui, isoladamente, um laudo pericial.

## Tecnologias

- Python
- pathlib
- hashlib
- datetime

## Objetivo

Projeto de estudo e portfólio voltado à programação Python aplicada
ao inventário e à análise preliminar de arquivos digitais.
