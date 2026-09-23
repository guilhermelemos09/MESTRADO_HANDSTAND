#!/usr/bin/env python3
"""
Abre o Gmail da USP (perfil /u/1/) diretamente no Mozilla Firefox pronto para envio.
"""
import argparse
import subprocess
import urllib.parse
from pathlib import Path

def open_gmail_compose(to, subject, body, account_index="1"):
    params = {
        "view": "cm",
        "fs": "1",
        "to": to,
        "su": subject,
        "body": body
    }

    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = f"https://mail.google.com/mail/u/{account_index}/?{query_string}"
    
    firefox_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    if Path(firefox_path).exists():
        ps_cmd = f'Start-Process "{firefox_path}" -ArgumentList "-new-tab", "`"{url}`""'
    else:
        ps_cmd = f'Start-Process "`"{url}`""'

    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    print(f"Janela aberta com sucesso no Firefox na conta USP (/u/{account_index}/)!")
    print(f"Destinatário: {to}")
    print(f"Assunto: {subject}")
    return url

def main():
    parser = argparse.ArgumentParser(description="Abrir composição no Gmail da USP")
    parser.add_argument("--to", required=True, help="Destinatário")
    parser.add_argument("--subject", required=True, help="Assunto")
    parser.add_argument("--body", required=True, help="Corpo da mensagem")
    parser.add_argument("--account", default="1", help="Índice da conta Google (padrão USP: 1)")

    args = parser.parse_args()
    open_gmail_compose(args.to, args.subject, args.body, args.account)

if __name__ == "__main__":
    main()
