
from pathlib import Path
import hashlib


def calcular_sha256(caminho):
    """Calcula o hash SHA-256 de um arquivo."""
    sha256 = hashlib.sha256()

    with caminho.open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(65536), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


def inventariar_arquivos(pasta):
    """Lista arquivos e calcula seus hashes."""
    diretorio = Path(pasta)

    if not diretorio.is_dir():
        print(f"Pasta não encontrada: {diretorio}")
        return

    for arquivo in sorted(diretorio.rglob("*")):
        if not arquivo.is_file():
            continue

        try:
            tamanho = arquivo.stat().st_size
            extensao = arquivo.suffix.lower() or "(sem extensão)"
            hash_sha256 = calcular_sha256(arquivo)

            print(f"Arquivo: {arquivo}")
            print(f"Tamanho: {tamanho} bytes")
            print(f"Extensão: {extensao}")
            print(f"SHA-256: {hash_sha256}")
            print("-" * 50)

        except OSError as erro:
            print(f"Erro ao ler {arquivo}: {erro}")


if __name__ == "__main__":
    pasta = input("Caminho da pasta de teste: ")
    inventariar_arquivos(pasta)

