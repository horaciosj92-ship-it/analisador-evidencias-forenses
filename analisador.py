from pathlib import Path
from datetime import datetime, timezone
import hashlib


def calcular_sha256(caminho):
    """Calcula o hash SHA-256 de um arquivo."""
    sha256 = hashlib.sha256()

    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


def inventariar_arquivos(pasta):
    """Inventaria arquivos, calcula hashes e gera relatório."""
    diretorio = Path(pasta).expanduser().resolve()

    if not diretorio.is_dir():
        print(f"Pasta não encontrada: {diretorio}")
        return

    inicio = datetime.now(timezone.utc)
    registros = []
    hashes = {}

    for item in sorted(diretorio.rglob("*")):
        if not item.is_file():
            continue

        try:
            tamanho = item.stat().st_size
            extensao = item.suffix.lower() or "(sem extensão)"
            hash_sha256 = calcular_sha256(item)

            registro = {
                "caminho": str(item),
                "tamanho": tamanho,
                "extensao": extensao,
                "sha256": hash_sha256,
            }
            registros.append(registro)
            hashes.setdefault(hash_sha256, []).append(str(item))

            print(f"Arquivo: {item}")
            print(f"Tamanho: {tamanho} bytes")
            print(f"Extensão: {extensao}")
            print(f"SHA-256: {hash_sha256}")
            print("-" * 50)

        except OSError as erro:
            print(f"Erro ao ler {item}: {erro}")

    fim = datetime.now(timezone.utc)
    duplicados = [
        caminhos for caminhos in hashes.values()
        if len(caminhos) > 1
    ]

    linhas = [
        "RELATÓRIO DE INVENTÁRIO FORENSE DIGITAL",
        "=" * 50,
        f"Pasta analisada: {diretorio}",
        f"Início UTC: {inicio.isoformat()}",
        f"Fim UTC: {fim.isoformat()}",
        f"Arquivos analisados: {len(registros)}",
        f"Grupos de duplicados: {len(duplicados)}",
        "",
        "ARQUIVOS E HASHES SHA-256",
        "-" * 50,
    ]

    for registro in registros:
        linhas.extend([
            f"Caminho: {registro['caminho']}",
            f"Tamanho: {registro['tamanho']} bytes",
            f"Extensão: {registro['extensao']}",
            f"SHA-256: {registro['sha256']}",
            "",
        ])

    linhas.extend(["GRUPOS DE DUPLICADOS", "-" * 50])

    if duplicados:
        for numero, caminhos in enumerate(duplicados, start=1):
            linhas.append(f"Grupo {numero}:")
            linhas.extend(f"  - {caminho}" for caminho in caminhos)
            linhas.append("")
    else:
        linhas.append("Nenhum arquivo duplicado encontrado.")

    # O relatório fica fora da pasta analisada para evitar
    # incluir o próprio relatório no inventário.
    relatorio = diretorio.parent / (
        f"relatorio_forense_{inicio.strftime('%Y%m%d_%H%M%S')}.txt"
    )

    try:
        relatorio.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    except OSError as erro:
        print(f"Não foi possível salvar o relatório: {erro}")
        return

    print("\n=== RESUMO ===")
    print(f"Arquivos analisados: {len(registros)}")
    print(f"Grupos de duplicados: {len(duplicados)}")
    print(f"Relatório salvo em: {relatorio}")


if __name__ == "__main__":
    pasta = input("Caminho da pasta de teste: ").strip()
    inventariar_arquivos(pasta)
