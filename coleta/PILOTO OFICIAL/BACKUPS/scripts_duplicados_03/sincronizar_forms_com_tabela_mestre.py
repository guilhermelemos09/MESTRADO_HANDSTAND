import os
import sys
import subprocess

dir_scripts = os.path.dirname(os.path.abspath(__file__))
script_gerenciar = os.path.join(dir_scripts, "gerenciar_recrutamento_agendamento.py")

if __name__ == "__main__":
    print("[SINCRONIZAÇÃO] Disparando rotina de sincronização dos formulários Google...")
    cmd = [sys.executable, script_gerenciar, "--sincronizar"]
    subprocess.run(cmd)
