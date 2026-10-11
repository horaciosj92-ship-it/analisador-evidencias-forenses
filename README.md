# Analisador de Evidências Forenses

Ferramenta desenvolvida em Python para inventariar arquivos digitais, calcular hashes SHA-256, identificar arquivos com conteúdo idêntico e gerar relatórios técnicos em formato TXT.

Projeto de estudo e portfólio voltado à programação Python e à análise preliminar de evidências digitais.

## Funcionalidades

- Inventário recursivo de arquivos e subpastas.
- Cálculo de hash SHA-256 para cada arquivo.
- Registro de caminho, tamanho e extensão dos arquivos.
- Identificação de grupos de arquivos com hashes SHA-256 idênticos.
- Tratamento de erros durante a leitura.
- Geração automática de relatório TXT com data e hora em UTC.
- Testes automatizados das principais funcionalidades.

## Tecnologias utilizadas

- Python 3.9 ou superior.
- `pathlib` — navegação pelo sistema de arquivos.
- `hashlib` — cálculo de hashes SHA-256.
- `datetime` — registro de data e hora.
- `unittest` — testes automatizados.

Não são necessárias bibliotecas externas para executar o analisador e os testes.

## Como executar

Com o Python instalado, abra um terminal na pasta do projeto e execute:

```bash
python analisador.py
```

Informe o caminho da pasta que deseja analisar quando solicitado.

O programa gera um relatório TXT no diretório pai da pasta analisada, com um nome semelhante a:

`relatorio_forense_20261011_201338.txt`

Recomenda-se realizar testes com cópias de arquivos, evitando modificar evidências originais.

## Como executar os testes automatizados

Na pasta do projeto, execute:

```bash
python -m unittest -v test_analisador.py
```

Os sete testes implementados verificam o cálculo de SHA-256, a comparação de arquivos, a identificação de duplicados e a geração do relatório.

## Limitações e cuidados forenses

- O hash SHA-256 permite comparar a integridade do conteúdo, mas, isoladamente, não comprova autoria, origem, data de criação ou autenticidade de uma evidência.
- A ferramenta não implementa aquisição forense, bloqueio de escrita, assinatura digital ou cadeia de custódia auditável.
- Os resultados dependem das condições dos arquivos e do ambiente durante a análise.
- O relatório gerado é técnico e preliminar; não constitui, isoladamente, um laudo pericial oficial.

## Objetivo do projeto

Demonstrar conhecimentos práticos de Python, manipulação de arquivos, integridade digital por hash, geração de relatórios e testes automatizados aplicados à análise preliminar de arquivos digitais.
