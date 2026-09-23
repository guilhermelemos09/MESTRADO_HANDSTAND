#!/usr/bin/env python3
import base64
import io
import os
import subprocess
import sys
from pathlib import Path
import qrcode

ARTIFACT_DIR = Path(r"C:\Users\Gui\.gemini\antigravity\brain\68255cfb-6bbc-4763-8804-8d17ea6e143e")
LOCAL_DIR = Path(__file__).resolve().parent

def generate_qr_html(qr_text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=3,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#111827", back_color="#ffffff")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64}"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-6 shadow-md max-w-sm mx-auto text-center">
    <div class="flex items-center justify-center gap-2 mb-3">
      <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
      <h2 class="text-base font-bold text-[var(--foreground)]">Conectar WhatsApp do Mestrado</h2>
    </div>
    <p class="text-xs text-[var(--muted-foreground)] mb-4">
      Abra o WhatsApp &gt; <strong>Aparelhos Conectados</strong> &gt; <strong>Conectar Aparelho</strong> e aponte para o código:
    </p>
    <div class="bg-white p-3 rounded-xl inline-block shadow-inner border border-slate-200">
      <img src="{data_uri}" alt="QR Code WhatsApp" class="w-64 h-64 object-contain mx-auto block" />
    </div>
    <p class="text-[11px] text-[var(--muted-foreground)] mt-3">
      O código renova automaticamente. Aponte a câmera agora!
    </p>
  </div>
</body>
</html>
"""

    # Salva no diretório de artefatos para embed no chat
    artifact_file = ARTIFACT_DIR / "whatsapp_qr.html"
    artifact_file.write_text(html_content, encoding="utf-8")

    # Salva localmente e abre no Firefox para garantir 100% de visibilidade
    local_file = LOCAL_DIR / "whatsapp_qr.html"
    local_file.write_text(html_content, encoding="utf-8")

    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    file_url = f"file:///{str(local_file).replace(chr(92), '/')}"
    if Path(firefox_path).exists():
        ps_cmd = f'Start-Process "{firefox_path}" -ArgumentList "-new-tab", "`"{file_url}`""'
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False)

    return str(artifact_file)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        txt_path = LOCAL_DIR / "qr_code.txt"
        if txt_path.exists():
            text = txt_path.read_text(encoding="utf-8").strip()
        else:
            print("Nenhum texto de QR.")
            sys.exit(1)

    res = generate_qr_html(text)
    print(f"Widget gerado com sucesso: {res}")
