import hashlib
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from analisador import calcular_sha256, inventariar_arquivos


class TestAnalisadorForense(unittest.TestCase):

    def test_sha256_conhecido(self):
        with tempfile.TemporaryDirectory() as temp:
            arquivo = Path(temp) / "teste.txt"
            arquivo.write_bytes(b"conteudo de teste")
            esperado = hashlib.sha256(b"conteudo de teste").hexdigest()
            self.assertEqual(calcular_sha256(arquivo), esperado)

    def test_arquivos_identicos_tem_mesmo_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "a.txt"
            b = Path(temp) / "b.txt"
            a.write_bytes(b"igual")
            b.write_bytes(b"igual")
            self.assertEqual(calcular_sha256(a), calcular_sha256(b))

    def test_arquivos_diferentes_tem_hashes_diferentes(self):
        with tempfile.TemporaryDirectory() as temp:
            a = Path(temp) / "a.txt"
            b = Path(temp) / "b.txt"
            a.write_bytes(b"primeiro")
            b.write_bytes(b"segundo")
            self.assertNotEqual(calcular_sha256(a), calcular_sha256(b))

    def test_relatorio_e_criado(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            pasta = base / "evidencias"
            pasta.mkdir()
            (pasta / "arquivo.txt").write_text("teste", encoding="utf-8")

            with redirect_stdout(StringIO()):
                inventariar_arquivos(pasta)

            relatorios = list(base.glob("relatorio_forense_*.txt"))
            self.assertEqual(len(relatorios), 1)

    def test_quantidade_de_arquivos_no_relatorio(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            pasta = base / "evidencias"
            pasta.mkdir()
            (pasta / "a.txt").write_text("A", encoding="utf-8")
            (pasta / "b.txt").write_text("B", encoding="utf-8")

            with redirect_stdout(StringIO()):
                inventariar_arquivos(pasta)

            relatorio = next(base.glob("relatorio_forense_*.txt"))
            texto = relatorio.read_text(encoding="utf-8")
            self.assertIn("Arquivos analisados: 2", texto)

    def test_duplicados_sao_identificados(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            pasta = base / "evidencias"
            subpasta = pasta / "subpasta"
            subpasta.mkdir(parents=True)
            (pasta / "a.txt").write_bytes(b"igual")
            (subpasta / "b.txt").write_bytes(b"igual")
            (pasta / "c.txt").write_bytes(b"diferente")

            with redirect_stdout(StringIO()):
                inventariar_arquivos(pasta)

            relatorio = next(base.glob("relatorio_forense_*.txt"))
            texto = relatorio.read_text(encoding="utf-8")
            self.assertIn("Grupos de duplicados: 1", texto)
            self.assertIn("a.txt", texto)
            self.assertIn("b.txt", texto)

    def test_sem_duplicados(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            pasta = base / "evidencias"
            pasta.mkdir()
            (pasta / "a.txt").write_bytes(b"A")
            (pasta / "b.txt").write_bytes(b"B")

            with redirect_stdout(StringIO()):
                inventariar_arquivos(pasta)

            relatorio = next(base.glob("relatorio_forense_*.txt"))
            texto = relatorio.read_text(encoding="utf-8")
            self.assertIn("Grupos de duplicados: 0", texto)
            self.assertIn("Nenhum arquivo duplicado encontrado.", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
