#!/usr/bin/env python3
"""Operador automatizado del guion de calibracion-01 (panel D-M9x). Logea todo."""
import json, os, subprocess, sys, time

REPO = r"C:\dev\verai-lab-caja"
MOTOR = r"C:\Users\avich\OneDrive - GENUINE LAB\Documents\AUDIO\spec-dlc\plugins\verai\skills\dlc-orquesta-ops\assets\verai_motor.py"
EVID = r"C:\dev\_verai-evidencia\calibracion-01"
CMD = [sys.executable, MOTOR, "run", "--repo", REPO, "--lote", "calibracion-01",
       "--max-concurrent", "2", "--max-retries", "1", "--stall-timeout", "600", "--gate-timeout", "180"]
os.makedirs(EVID, exist_ok=True)
LOG = open(os.path.join(EVID, "operador.log"), "a", encoding="utf-8")

def log(m):
    linea = f"{time.strftime('%H:%M:%S')} [OP] {m}"
    print(linea, flush=True); LOG.write(linea + "\n"); LOG.flush()

def estado():
    try:
        return json.load(open(os.path.join(REPO, ".verai", "state.json"), encoding="utf-8"))["uws"]
    except Exception:
        return {}

def costo():
    return sum(u.get("costo_usd", 0) for u in estado().values())

def lanzar(tag):
    f = open(os.path.join(EVID, f"motor.{tag}.log"), "w", encoding="utf-8")
    p = subprocess.Popen(CMD, stdout=f, stderr=subprocess.STDOUT, cwd=REPO)
    log(f"motor lanzado ({tag}) pid={p.pid}")
    return p

def esperar(pred, desc, timeout=1500, proc=None):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if costo() > 4.5:
            log(f"CORTE DE PRESUPUESTO (${costo():.2f}) — STOP"); open(os.path.join(REPO, ".verai", "STOP"), "w").close()
            return "budget"
        if pred(estado()):
            log(f"condición alcanzada: {desc}"); return True
        if proc is not None and proc.poll() is not None:
            log(f"motor terminó (exit {proc.returncode}) esperando: {desc}"); return "motor_exit"
        time.sleep(2)
    log(f"TIMEOUT esperando: {desc}"); return False

def kill_pid(pid, arbol):
    r = subprocess.run(["taskkill", "/PID", str(pid)] + (["/T"] if arbol else []) + ["/F"], capture_output=True, text=True)
    log(f"taskkill pid={pid} arbol={arbol} → {r.returncode} {r.stdout.strip()[:80]}{r.stderr.strip()[:80]}")

st = lambda e, u: e.get(u, {}).get("estado")

# ── Fase 1: lanzar y esperar la ventana UW-02∥UW-03 RUNNING ──
p1 = lanzar("fase1")
r = esperar(lambda e: st(e, "UW-02") == "RUNNING" and st(e, "UW-03") == "RUNNING",
            "UW-02 y UW-03 RUNNING (ventana de colisión)", proc=p1)
if r is True:
    time.sleep(6)  # que los workers arranquen de verdad
    # KILL A: matar el MOTOR sin /T → workers vivos
    pid_motor = json.load(open(os.path.join(REPO, ".verai", "motor.lock"), encoding="utf-8"))["pid"]
    pids_w = {u: json.load(open(os.path.join(REPO, ".verai", "leases", f"{u}.json"), encoding="utf-8"))["pid"]
              for u in ("UW-02", "UW-03") if os.path.exists(os.path.join(REPO, ".verai", "leases", f"{u}.json"))}
    log(f"KILL A: motor={pid_motor}, workers vivos={pids_w}")
    kill_pid(pid_motor, arbol=False)
    time.sleep(2)
    # relanzar → debe ABORTAR por worker vivo (anti doble despacho)
    ra = subprocess.run(CMD, capture_output=True, text=True, cwd=REPO, timeout=120)
    abortado = "VIVO" in (ra.stdout + ra.stderr)
    log(f"relanzamiento con workers vivos → exit {ra.returncode}; abortó por worker VIVO: {abortado}")
    open(os.path.join(EVID, "killA_relanzamiento.log"), "w", encoding="utf-8").write(ra.stdout + ra.stderr)
    # KILL B: matar workers huérfanos y relanzar → lease huérfano → retoma
    for u, pid in pids_w.items():
        kill_pid(pid, arbol=True)
    time.sleep(2)
    p2 = lanzar("fase2-resume")
else:
    log(f"ventana de colisión no capturada ({r}); el lote sigue sin kill (plan B del panel: se pierde sub-caso)")
    p2 = p1

# ── Fase 3: STOP mientras los reintentos corren, antes de UW-06 ──
r = esperar(lambda e: (st(e, "UW-02") == "RUNNING" or st(e, "UW-03") == "RUNNING") and st(e, "UW-06") == "PENDING",
            "reintentos de UW-02/03 RUNNING con UW-06 aún PENDING (ventana STOP)", timeout=900, proc=p2)
if r is True:
    subprocess.run([sys.executable, MOTOR, "stop", "--repo", REPO], capture_output=True)
    log("STOP emitido; espero a que el motor pare solo")
    for _ in range(300):
        if p2.poll() is not None:
            break
        time.sleep(2)
    log(f"motor paró (exit {p2.returncode if p2.poll() is not None else 'aún vivo!'})")
    # rearme
    try:
        os.remove(os.path.join(REPO, ".verai", "STOP"))
    except OSError:
        pass
    p3 = lanzar("fase4-rearme")
else:
    log(f"ventana STOP no capturada ({r}); sigo con el motor vigente")
    p3 = p2

# ── Fase final: dejar terminar ──
while p3.poll() is None:
    if costo() > 4.5:
        log(f"presupuesto ${costo():.2f} — STOP final"); open(os.path.join(REPO, ".verai", "STOP"), "w").close()
    time.sleep(5)
log(f"motor final exit={p3.returncode} · costo total=${costo():.3f}")
fin = {u: {"estado": v["estado"], "intentos": v["intentos"], "usd": v.get("costo_usd", 0)} for u, v in estado().items()}
log("estado final: " + json.dumps(fin, ensure_ascii=False))
