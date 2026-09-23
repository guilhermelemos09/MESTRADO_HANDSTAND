#!/usr/bin/env node
import { makeWASocket, useMultiFileAuthState, DisconnectReason, Browsers } from '@whiskeysockets/baileys';
import qrcodeTerminal from 'qrcode-terminal';
import pino from 'pino';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const AUTH_DIR = path.join(__dirname, 'auth_info');
const QR_TXT = path.join(__dirname, 'qr_code.txt');
const STATUS_FILE = path.join(__dirname, 'status.json');

const logger = pino({ level: 'silent' });

function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i].startsWith('--')) {
            const key = args[i].replace(/^--/, '');
            const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
            parsed[key] = val;
        }
    }
    return parsed;
}

function triggerQrImage(qrText) {
    fs.writeFileSync(QR_TXT, qrText, 'utf-8');
    const pyScript = path.join(__dirname, 'gerar_html_qr.py');
    exec(`python "${pyScript}"`, (err, stdout) => {
        if (!err && stdout) {
            console.log('[QR Code HTML gerado e atualizado no Firefox e chat]');
        }
    });
}

function cleanNumber(num) {
    let cleaned = String(num).replace(/\D/g, '');
    if (cleaned.length === 10 || cleaned.length === 11) {
        cleaned = '55' + cleaned;
    }
    return cleaned;
}

async function connectToWhatsApp(onSuccess) {
    const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);

    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
        logger: logger,
        browser: Browsers.windows('Chrome'),
        syncFullHistory: false,
        generateHighQualityLinkPreview: false
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect, qr } = update;

        if (qr) {
            console.log('\n================ QR CODE ATUALIZADO ================');
            qrcodeTerminal.generate(qr, { small: true });
            console.log('====================================================\n');
            triggerQrImage(qr);
        }

        if (connection === 'open') {
            console.log('\n[SUCESSO] Conexão com o WhatsApp estabelecida com sucesso!');
            const user = sock.user;
            fs.writeFileSync(STATUS_FILE, JSON.stringify({
                connected: true,
                user: user,
                updated_at: new Date().toISOString()
            }, null, 2));
            if (onSuccess) onSuccess(sock);
        }

        if (connection === 'close') {
            const statusCode = lastDisconnect?.error?.output?.statusCode;
            const isLoggedOut = statusCode === DisconnectReason.loggedOut;

            if (isLoggedOut) {
                console.log('[AVISO] Sessão desconectada pelo aparelho.');
                fs.rmSync(AUTH_DIR, { recursive: true, force: true });
                if (fs.existsSync(STATUS_FILE)) fs.unlinkSync(STATUS_FILE);
            } else {
                console.log('[Reconectando WhatsApp...]');
                setTimeout(() => connectToWhatsApp(onSuccess), 2000);
            }
        }
    });

    return sock;
}

async function sendWhatsAppMessage({ to, text, filePath }) {
    if (!fs.existsSync(AUTH_DIR) || !fs.readdirSync(AUTH_DIR).length) {
        throw new Error('WhatsApp ainda não conectado. Conecte primeiro via QR code: node client.js --action connect');
    }

    return new Promise((resolve, reject) => {
        let sent = false;
        connectToWhatsApp(async (sock) => {
            if (sent) return;
            sent = true;

            try {
                const rawNumber = cleanNumber(to);
                let targetJid = `${rawNumber}@s.whatsapp.net`;

                try {
                    const [onWa] = await sock.onWhatsApp(targetJid);
                    if (onWa && onWa.exists) {
                        targetJid = onWa.jid;
                    }
                } catch (e) {}

                console.log(`[Enviando para] ${targetJid}`);

                if (filePath) {
                    const absPath = path.resolve(filePath);
                    if (!fs.existsSync(absPath)) {
                        throw new Error(`Arquivo não encontrado: ${absPath}`);
                    }
                    const fileName = path.basename(absPath);
                    const fileBuffer = fs.readFileSync(absPath);
                    const ext = path.extname(absPath).toLowerCase();

                    let payload = {
                        document: fileBuffer,
                        mimetype: ext === '.pdf' ? 'application/pdf' : 'application/octet-stream',
                        fileName: fileName,
                        caption: text || ''
                    };

                    await sock.sendMessage(targetJid, payload);
                    console.log(`[OK] Arquivo "${fileName}" enviado com sucesso!`);
                } else if (text) {
                    await sock.sendMessage(targetJid, { text });
                    console.log(`[OK] Mensagem de texto enviada com sucesso!`);
                }

                await new Promise(r => setTimeout(r, 2000));
                resolve();
                process.exit(0);
            } catch (err) {
                reject(err);
                process.exit(1);
            }
        });
    });
}

async function main() {
    const args = parseArgs();
    const action = args.action || 'connect';

    try {
        if (action === 'connect') {
            console.log('[Iniciando] Gerando QR Code para conexão...');
            connectToWhatsApp((sock) => {
                console.log(`[Pronto] Aparelho conectado! Telefone: ${sock.user?.id || 'OK'}`);
                setTimeout(() => process.exit(0), 4000);
            });
        } else if (action === 'send') {
            if (!args.to) {
                throw new Error('Argumento --to é obrigatório para envio.');
            }
            await sendWhatsAppMessage({
                to: args.to,
                text: args.text,
                filePath: args.file
            });
        } else if (action === 'status') {
            const hasAuth = fs.existsSync(AUTH_DIR) && fs.readdirSync(AUTH_DIR).length > 0;
            let status = { authenticated: hasAuth };
            if (fs.existsSync(STATUS_FILE)) {
                status = { ...status, ...JSON.parse(fs.readFileSync(STATUS_FILE, 'utf-8')) };
            }
            console.log(JSON.stringify(status, null, 2));
            process.exit(0);
        }
    } catch (err) {
        console.error('[Erro]:', err.message);
        process.exit(1);
    }
}

main();
