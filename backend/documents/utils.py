import tempfile
from io import BytesIO
from pathlib import Path

import qrcode
from django.conf import settings
from django.template.loader import render_to_string


def generate_qr_code(url: str) -> str:
    """
    Gera um QR code temporario e retorna o caminho do arquivo PNG.
    """
    media_dir = Path(settings.MEDIA_ROOT)
    media_dir.mkdir(parents=True, exist_ok=True)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="qr_", dir=str(media_dir))
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(tmp_file.name)
    return tmp_file.name


def generate_pdf(template_name: str, context: dict) -> BytesIO:
    """
    Renderiza template HTML e retorna PDF em memoria.
    """
    # Importar no runtime para evitar falha em ambientes sem libs no import inicial
    from weasyprint import HTML

    html_content = render_to_string(template_name, context)
    pdf_io = BytesIO()
    base_url = Path(settings.BASE_DIR).as_posix()
    HTML(string=html_content, base_url=base_url).write_pdf(pdf_io)
    pdf_io.seek(0)
    return pdf_io
