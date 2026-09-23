#!/usr/bin/env python3
"""
Utilitário para envio automatizado de e-mails via Gmail (SMTP SSL).
"""
import argparse
import json
import mimetypes
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

def get_env_paths():
    current_dir = Path(__file__).resolve().parent
    return [
        current_dir / ".env",
        current_dir.parent / ".env",
    ]

def load_credentials():
    env_vars = {}
    for env_path in get_env_paths():
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip("'\"")

    user = os.environ.get("GMAIL_USER") or env_vars.get("GMAIL_USER", "")
    password = os.environ.get("GMAIL_APP_PASSWORD") or env_vars.get("GMAIL_APP_PASSWORD", "")
    
    # O Google costuma gerar a senha de app com espaços (ex: 'abcd efgh ijkl mnop')
    password = password.replace(" ", "")

    return user.strip(), password.strip()

def send_email(to_addrs, subject, body, is_html=False, attachments=None, cc=None, bcc=None):
    user, password = load_credentials()
    
    if not user or not password:
        raise ValueError(
            "Credenciais não encontradas. Certifique-se de preencher GMAIL_USER e GMAIL_APP_PASSWORD no arquivo .env"
        )

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = ", ".join(to_addrs) if isinstance(to_addrs, list) else to_addrs
    msg["Subject"] = subject

    if cc:
        msg["Cc"] = ", ".join(cc) if isinstance(cc, list) else cc
    if bcc:
        msg["Bcc"] = ", ".join(bcc) if isinstance(bcc, list) else bcc

    if is_html:
        msg.set_content("Esta mensagem requer um cliente de e-mail compatível com HTML.")
        msg.add_alternative(body, subtype="html")
    else:
        msg.set_content(body)

    if attachments:
        for file_path_str in attachments:
            file_path = Path(file_path_str)
            if not file_path.exists():
                raise FileNotFoundError(f"Anexo não encontrado: {file_path}")
            
            ctype, encoding = mimetypes.guess_type(str(file_path))
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
            maintype, subtype = ctype.split("/", 1)

            with open(file_path, "rb") as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data,
                    main_type=maintype,
                    sub_type=subtype,
                    filename=file_path.name
                )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(user, password)
        server.send_message(msg)

    return {
        "status": "success",
        "from": user,
        "to": msg["To"],
        "subject": subject,
        "attachments": [Path(p).name for p in (attachments or [])]
    }

def test_connection():
    user, password = load_credentials()
    if not user or not password:
        return {"status": "error", "message": "GMAIL_USER ou GMAIL_APP_PASSWORD não definidos."}
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(user, password)
        return {"status": "success", "message": f"Conexão com o Gmail autenticada com sucesso para {user}!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Envio de e-mails via Gmail")
    parser.add_argument("--to", nargs="+", help="Destinatário(s)")
    parser.add_argument("--subject", help="Assunto do e-mail")
    parser.add_argument("--body", help="Corpo da mensagem")
    parser.add_argument("--html", action="store_true", help="Indica que o corpo é HTML")
    parser.add_argument("--attach", nargs="*", help="Caminhos de arquivos para anexar")
    parser.add_argument("--cc", nargs="*", help="Destinatário(s) em cópia")
    parser.add_argument("--bcc", nargs="*", help="Destinatário(s) em cópia oculta")
    parser.add_argument("--test", action="store_true", help="Apenas testa a conexão e credenciais")

    args = parser.parse_args()

    if args.test:
        res = test_connection()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res["status"] == "success" else 1)

    if not args.to or not args.subject or not args.body:
        parser.error("Os argumentos --to, --subject e --body são obrigatórios (ou use --test).")

    try:
        res = send_email(
            to_addrs=args.to,
            subject=args.subject,
            body=args.body,
            is_html=args.html,
            attachments=args.attach,
            cc=args.cc,
            bcc=args.bcc
        )
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        err = {"status": "error", "message": str(e)}
        print(json.dumps(err, indent=2, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
