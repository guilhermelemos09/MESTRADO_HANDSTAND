#!/usr/bin/env python3
"""
Envio automatizado de e-mails via Gmail API utilizando OAuth2 oficial do Google.
Compatível com contas Google Workspace institucionais (como @usp.br).
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]

def get_paths():
    base_dir = Path(__file__).resolve().parent
    return {
        "credentials": base_dir / "credentials.json",
        "token": base_dir / "token.json",
    }

def get_gmail_service():
    paths = get_paths()
    creds = None

    if paths["token"].exists():
        creds = Credentials.from_authorized_user_file(str(paths["token"]), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not paths["credentials"].exists():
                raise FileNotFoundError(
                    f"Arquivo '{paths['credentials'].name}' não encontrado na pasta '{paths['credentials'].parent}'.\n"
                    "Baixe o arquivo de credenciais OAuth (Desktop) no Google Cloud Console e salve nessa pasta."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(paths["credentials"]), SCOPES)
            print("Abrindo navegador para autorização da conta Google...", file=sys.stderr)
            creds = flow.run_local_server(port=0)

        with open(paths["token"], "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def send_email_oauth(to_addrs, subject, body, is_html=False, attachments=None, cc=None, bcc=None):
    service = get_gmail_service()

    msg = EmailMessage()
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

    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    sent = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

    return {
        "status": "success",
        "message_id": sent.get("id"),
        "thread_id": sent.get("threadId"),
        "to": msg["To"],
        "subject": subject,
        "attachments": [Path(p).name for p in (attachments or [])]
    }

def authenticate_only():
    """Apenas autentica e salva o token.json."""
    service = get_gmail_service()
    profile = service.users().getProfile(userId="me").execute()
    return {
        "status": "success",
        "message": f"Autenticado com sucesso para: {profile.get('emailAddress')}",
        "email": profile.get("emailAddress")
    }

def main():
    parser = argparse.ArgumentParser(description="Envio de e-mails via Gmail API (OAuth2)")
    parser.add_argument("--to", nargs="+", help="Destinatário(s)")
    parser.add_argument("--subject", help="Assunto do e-mail")
    parser.add_argument("--body", help="Corpo da mensagem")
    parser.add_argument("--html", action="store_true", help="Indica que o corpo é HTML")
    parser.add_argument("--attach", nargs="*", help="Caminhos de arquivos para anexar")
    parser.add_argument("--cc", nargs="*", help="Destinatário(s) em cópia")
    parser.add_argument("--bcc", nargs="*", help="Destinatário(s) em cópia oculta")
    parser.add_argument("--login", action="store_true", help="Executa apenas o fluxo de autenticação e validação")

    args = parser.parse_args()

    if args.login:
        try:
            res = authenticate_only()
            print(json.dumps(res, indent=2, ensure_ascii=False))
            sys.exit(0)
        except Exception as e:
            err = {"status": "error", "message": str(e)}
            print(json.dumps(err, indent=2, ensure_ascii=False))
            sys.exit(1)

    if not args.to or not args.subject or not args.body:
        parser.error("Os argumentos --to, --subject e --body são obrigatórios (ou use --login).")

    try:
        res = send_email_oauth(
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
