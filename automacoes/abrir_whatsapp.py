#!/usr/bin/env python3
"""
Abre a conversa do WhatsApp Web no Mozilla Firefox com a mensagem já digitada (1 clique).
"""
import argparse
import subprocess
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def format_whatsapp_number(num):
    cleaned = "".join(filter(str.isdigit, str(num)))
    if len(cleaned) in [10, 11]:
        cleaned = f"55{cleaned}"
    return cleaned

def open_whatsapp_chat(phone, text, open_folder=None):
    clean_phone = format_whatsapp_number(phone)
    msg_encoded = urllib.parse.quote(text)
    
    # URL oficial que vai direto para a conversa no WhatsApp Web
    url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={msg_encoded}"
    
    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    if Path(firefox_path).exists():
        ps_cmd = f'Start-Process "{firefox_path}" -ArgumentList "-new-tab", "`"{url}`""'
    else:
        ps_cmd = f'Start-Process "`"{url}`""'

    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    print(f"WhatsApp Web aberto no Firefox para o número: {clean_phone}")

    # Se houver pasta ou arquivo para anexar, abre o Windows Explorer junto
    if open_folder and Path(open_folder).exists():
        folder_to_open = open_folder if Path(open_folder).is_dir() else Path(open_folder).parent
        subprocess.run(["powershell", "-NoProfile", "-Command", f'Start-Process explorer.exe -ArgumentList "`"{folder_to_open}`""'], check=False)
        print(f"Pasta de anexos aberta na tela: {folder_to_open}")

    return url

def main():
    parser = argparse.ArgumentParser(description="Abrir conversa no WhatsApp Web")
    parser.add_argument("--phone", required=True, help="Número de telefone com DDD")
    parser.add_argument("--text", required=True, help="Texto da mensagem")
    parser.add_argument("--anexo", help="Caminho do arquivo ou pasta para abrir no Explorer")

    args = parser.parse_args()
    open_whatsapp_chat(args.phone, args.text, args.anexo)

if __name__ == "__main__":
    main()
