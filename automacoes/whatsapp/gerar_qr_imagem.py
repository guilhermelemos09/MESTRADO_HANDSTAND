#!/usr/bin/env python3
"""
Gera imagem PNG do QR Code e abre na tela para fácil leitura com o celular.
"""
import os
import sys
from pathlib import Path
import qrcode

def generate_and_open_qr(qr_text, auto_open=True):
    base_dir = Path(__file__).resolve().parent
    img_path = base_dir / "qr_code.png"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(str(img_path))
    print(f"QR Code salvo em: {img_path}")

    if auto_open:
        try:
            os.startfile(str(img_path))
            print("Imagem do QR Code aberta na tela para leitura!")
        except Exception as e:
            print(f"Não foi possível abrir automaticamente a imagem: {e}")

    return str(img_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        txt_path = Path(__file__).resolve().parent / "qr_code.txt"
        if txt_path.exists():
            text = txt_path.read_text(encoding="utf-8").strip()
        else:
            print("Nenhum dado de QR code fornecido.")
            sys.exit(1)

    generate_and_open_qr(text)
