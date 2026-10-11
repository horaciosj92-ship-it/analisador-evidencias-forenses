
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
import hashlib
import json
import sys

PROJETO = Path("/content/analisador-evidencias-forenses")
IMAGEM = Path("/content/capa_shorts_causos_biblicos.png")
MANIFESTO = Path("/content/manifesto_c2pa_capa.json")
PREVIA = Path("/content/previa_relatorio.jpg")

if not IMAGEM.is_file():
    raise FileNotFoundError(f"Imagem não encontrada: {IMAGEM}")
if not MANIFESTO.is_file():
    raise FileNotFoundError(f"Manifesto não encontrado: {MANIFESTO}")

def sha256(caminho):
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()

# Recalcula dados do arquivo no momento da execução.
momento = datetime.now(timezone.utc).isoformat()
hash_imagem = sha256(IMAGEM)
dados_imagem = {
    "nome": IMAGEM.name,
    "caminho": str(IMAGEM),
    "tamanho_bytes": IMAGEM.stat().st_size,
    "sha256": hash_imagem,
}
with Image.open(IMAGEM) as img:
    dados_imagem["formato"] = img.format
    dados_imagem["dimensoes_pixels"] = list(img.size)
    dados_imagem["modo_cor"] = img.mode
    dados_imagem["metadados_info_chaves"] = list(img.info.keys())

manifesto_texto = MANIFESTO.read_text(encoding="utf-8")
try:
    manifesto_json = json.loads(manifesto_texto)
except json.JSONDecodeError:
    manifesto_json = {"conteudo_textual_original": manifesto_texto}

dados_previa = None
if PREVIA.is_file():
    dados_previa = {
        "nome": PREVIA.name,
        "tamanho_bytes": PREVIA.stat().st_size,
        "sha256": sha256(PREVIA),
    }
    with Image.open(PREVIA) as img:
        dados_previa["formato"] = img.format
        dados_previa["dimensoes_pixels"] = list(img.size)

registro = {
    "tipo_documento": "Relatório técnico preliminar",
    "data_geracao_utc": momento,
    "metodo": "Inventário de arquivo, SHA-256, leitura de propriedades da imagem e inclusão do manifesto C2PA disponível.",
    "imagem": dados_imagem,
    "manifesto_c2pa": {
        "arquivo": str(MANIFESTO),
        "sha256_arquivo_manifesto": sha256(MANIFESTO),
        "conteudo": manifesto_json,
    },
    "previa": dados_previa,
    "limitacoes": [
        "Este relatório não é laudo pericial oficial.",
        "A geração deste documento não autentica a identidade do autor da imagem.",
        "O hash identifica o arquivo analisado, mas não comprova autoria nem data original.",
        "O manifesto é documentado como fornecido; não se presume confiança plena da credencial.",
        "Não se infere uso ou ausência de inteligência artificial sem evidência específica.",
        "A data de geração deste relatório não é a data de criação original da imagem.",
    ],
}

# Guarda o conjunto de dados para auditoria e reprodução.
json_saida = PROJETO / "evidencias_capa.json"
json_saida.write_text(
    json.dumps(registro, ensure_ascii=False, indent=2, default=str),
    encoding="utf-8"
)

pdf_saida = PROJETO / "laudo_tecnico_preliminar_capa.pdf"

estilos = getSampleStyleSheet()
estilos.add(ParagraphStyle(
    name="CapaTitulo", parent=estilos["Title"],
    fontName="Helvetica-Bold", fontSize=20, leading=25,
    alignment=TA_CENTER, textColor=colors.HexColor("#17324D"),
    spaceAfter=14
))
estilos.add(ParagraphStyle(
    name="Secao", parent=estilos["Heading1"],
    fontName="Helvetica-Bold", fontSize=13, leading=17,
    textColor=colors.HexColor("#17324D"), spaceBefore=10, spaceAfter=6
))
estilos.add(ParagraphStyle(
    name="Texto", parent=estilos["BodyText"],
    fontName="Helvetica", fontSize=9, leading=12, spaceAfter=6
))
estilos.add(ParagraphStyle(
    name="Pequeno", parent=estilos["BodyText"],
    fontName="Helvetica", fontSize=7.5, leading=9.5,
    textColor=colors.HexColor("#475569"), spaceAfter=4
))
estilos.add(ParagraphStyle(
    name="Aviso", parent=estilos["BodyText"],
    fontName="Helvetica-Bold", fontSize=9, leading=12,
    borderColor=colors.HexColor("#94A3B8"), borderWidth=0.7,
    borderPadding=8, backColor=colors.HexColor("#F1F5F9"),
    spaceBefore=5, spaceAfter=8
))

def P(texto, estilo="Texto"):
    return Paragraph(texto, estilos[estilo])

def rodape(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(2*cm, 1.5*cm, A4[0]-2*cm, 1.5*cm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(2*cm, 1.05*cm, "Relatório técnico preliminar — evidência digital")
    canvas.drawRightString(A4[0]-2*cm, 1.05*cm, f"Página {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(
    str(pdf_saida), pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=1.8*cm, bottomMargin=2*cm,
    title="Relatório técnico preliminar — capa Causos Bíblicos",
    author="Projeto Analisador de Evidências Forenses"
)

conteudo = [
    Spacer(1, 2*cm),
    P("RELATÓRIO TÉCNICO PRELIMINAR", "CapaTitulo"),
    P("Análise técnica de imagem e documentação de evidências digitais", "Texto"),
    Spacer(1, 0.5*cm),
    HRFlowable(width="70%", thickness=1, color=colors.HexColor("#54758F"), hAlign="CENTER"),
    Spacer(1, 0.6*cm),
    P("<b>Objeto:</b> capa de Short do canal Causos Bíblicos."),
    P("<b>Projeto:</b> Analisador de Evidências Forenses — Python."),
    P(f"<b>Gerado em UTC:</b> {momento}"),
    Spacer(1, 0.4*cm),
    P("AVISO: este documento é um relatório técnico preliminar produzido por script. Não é laudo pericial oficial nem certificação definitiva de autoria.", "Aviso"),
    PageBreak(),
    P("1. Objetivo e método", "Secao"),
    P("Documentar as propriedades do arquivo de imagem disponível no ambiente, calcular novamente seu SHA-256, registrar o conteúdo do manifesto C2PA fornecido e guardar os dados estruturados em JSON. A análise é limitada aos arquivos disponíveis no momento da execução."),
    P("O procedimento não altera deliberadamente a imagem original. O JSON contém a data de execução, os dados calculados e o conteúdo do manifesto lido."),
    P("2. Identificação da imagem", "Secao"),
]

linhas = [[P("<b>Campo</b>", "Pequeno"), P("<b>Resultado</b>", "Pequeno")]]
for rotulo, valor in [
    ("Arquivo", dados_imagem["nome"]),
    ("Caminho de análise", dados_imagem["caminho"]),
    ("Formato", str(dados_imagem["formato"])),
    ("Dimensões", " × ".join(map(str, dados_imagem["dimensoes_pixels"])) + " pixels"),
    ("Modo de cor", dados_imagem["modo_cor"]),
    ("Tamanho", f'{dados_imagem["tamanho_bytes"]:,} bytes'),
    ("SHA-256", hash_imagem),
    ("Chaves de metadados expostas pela biblioteca", ", ".join(map(str, dados_imagem["metadados_info_chaves"])) or "Nenhuma"),
]:
    linhas.append([P(rotulo, "Pequeno"), P(str(valor), "Pequeno")])

tabela = Table(linhas, colWidths=[5*cm, 10.3*cm], repeatRows=1)
tabela.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#E8EEF4")),
    ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#CBD5E1")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
]))
conteudo += [tabela, Spacer(1, 8)]
conteudo += [
    P("O SHA-256 permite conferir se um arquivo posteriormente obtido é idêntico, byte a byte, ao arquivo que produziu este hash. Não identifica o autor e não determina, por si só, quando o arquivo foi criado."),
    P("3. Manifesto C2PA", "Secao"),
    P(f"Arquivo do manifesto: {MANIFESTO.name}. SHA-256 do arquivo JSON: {sha256(MANIFESTO)}."),
    P("O conteúdo completo do manifesto está preservado em evidencias_capa.json. Os campos abaixo são extraídos quando encontrados no formato JSON; a estrutura pode variar conforme a ferramenta exportadora."),
]

def procurar_chaves(obj, alvos, achados=None, prefixo=""):
    if achados is None:
        achados = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            caminho = f"{prefixo}.{k}" if prefixo else k
            if k.lower() in alvos and not isinstance(v, (dict, list)):
                achados.append((caminho, str(v)))
            procurar_chaves(v, alvos, achados, caminho)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            procurar_chaves(v, alvos, achados, f"{prefixo}[{i}]")
    return achados

alvos = {
    "claim_generator", "format", "action", "when", "softwareagent",
    "alg", "issuer", "commonname", "validation_status", "code", "explanation"
}
achados = procurar_chaves(manifesto_json, alvos)
if achados:
    for chave, valor in achados[:40]:
        conteudo.append(P(f"<b>{chave}:</b> {valor[:700]}", "Pequeno"))
else:
    conteudo.append(P("Não foi possível extrair automaticamente os campos principais. Consulte o conteúdo integral preservado no JSON.", "Texto"))

conteudo += [
    P("Interpretação: a existência de um manifesto C2PA deve ser analisada junto aos resultados completos de validação. Um aviso de credencial não confiável impede afirmar que a credencial é plenamente confiável. O registro não comprova sozinho quem operou o aplicativo nem a autoria humana."),
    P("4. Arquivo de prévia", "Secao"),
]
if dados_previa:
    conteudo.append(P(
        f"Arquivo: {dados_previa['nome']}; formato: {dados_previa.get('formato')}; "
        f"dimensões: {dados_previa.get('dimensoes_pixels')}; tamanho: "
        f"{dados_previa['tamanho_bytes']} bytes; SHA-256: {dados_previa['sha256']}."
    ))
    conteudo.append(P("Este relatório registra a identidade da prévia, mas não executa nesta etapa um teste perceptual nem conclui qual arquivo veio primeiro. A semelhança visual e a cronologia devem ser avaliadas separadamente."))
else:
    conteudo.append(P("A prévia não estava disponível no momento da execução."))

conteudo += [
    P("5. Projeto e rastreabilidade", "Secao"),
    P("O código do projeto deve ser mantido versionado junto dos arquivos de relatório. O histórico Git pode documentar alterações do código e dos relatórios versionados, mas não comprova sozinho a data original de criação da imagem."),
    P("O relatório e o JSON são gerados dentro da pasta do repositório. Para que permaneçam no GitHub, será necessário revisar os arquivos, evitar incluir evidências privadas desnecessárias e executar o commit/push de forma consciente."),
    P("6. Limitações", "Secao"),
    P("• O relatório não é laudo pericial oficial.<br/>"
      "• A execução do script não autentica a identidade do criador da imagem.<br/>"
      "• O hash não prova autoria nem data de criação.<br/>"
      "• A data deste relatório é a data da execução, não a data original da imagem.<br/>"
      "• A presença ou ausência de metadados não permite concluir isoladamente se houve uso de IA.<br/>"
      "• Não foi realizada aquisição forense independente do dispositivo nem validada uma cadeia de custódia formal."),
    P("7. Conclusão técnica preliminar", "Secao"),
    P("Este relatório documenta as propriedades calculadas do PNG disponível e preserva em JSON o manifesto C2PA fornecido. Qualquer conclusão sobre autoria, cronologia original ou valor probatório exige evidências adicionais, validação independente e análise do contexto de criação e publicação."),
    P("8. Arquivos gerados", "Secao"),
    P(f"PDF: {pdf_saida.name}<br/>JSON: {json_saida.name}"),
    Spacer(1, 8),
    P("Gerado automaticamente pelo script gerar_laudo.py. Revise o conteúdo antes de qualquer uso externo ou jurídico.", "Aviso"),
]

doc.build(conteudo, onFirstPage=rodape, onLaterPages=rodape)

print("RELATÓRIO GERADO")
print("PDF:", pdf_saida)
print("PDF bytes:", pdf_saida.stat().st_size)
print("JSON:", json_saida)
print("JSON bytes:", json_saida.stat().st_size)
print("SHA-256 da imagem:", hash_imagem)
print("Data de geração UTC:", momento)
