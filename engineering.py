
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import os
import uuid
import re
import json
import requests
import pyttsx3
 
# ================================================================
# CONFIG  — edit these if needed
# ================================================================
FREECAD      = r"C:\Users\Lenovo\AppData\Local\Programs\FreeCAD 1.0\bin\FreeCAD.exe"
OLLAMA_MODEL = "deepseek-r1:3b"   # exact name from: ollama list
OLLAMA_URL   = "http://localhost:11434/api/generate"
 
# ================================================================
# VOICE  (pyttsx3 — free, offline)
# ================================================================
try:
    _engine = pyttsx3.init()
    _engine.setProperty("rate", 160)
except Exception:
    _engine = None
 
def speak(text):
    try:
        if _engine:
            clean = re.sub(r"[^\w\s,.!?]", "", text)[:120]
            threading.Thread(target=lambda: (_engine.say(clean), _engine.runAndWait()), daemon=True).start()
    except Exception:
        pass
 
# ================================================================
# OLLAMA AI BRAIN  (free, local — DeepSeek 3B)
# ================================================================
SYSTEM_PROMPT = """You are Jarvis, a CAD assistant. The user describes a 3D part.
Reply ONLY with a JSON object — no markdown, no explanation, nothing else.
 
JSON fields:
  shape     : one of → arm | box | sphere | cylinder | cone | gear | bolt |
                        bracket | tube | spring | wheel | frame | hex | pipe | plate
  size      : main dimension mm (integer, default 120)
  width     : optional mm
  height    : optional mm
  thickness : optional wall thickness mm
  message   : short confirmation max 10 words
 
Examples:
  "arm 150"              → {"shape":"arm","size":150,"message":"Prosthetic arm on the way!"}
  "hollow box 100x60x40" → {"shape":"box","size":100,"width":60,"height":40,"thickness":5,"message":"Hollow box ready!"}
  "gear 80mm"            → {"shape":"gear","size":80,"message":"Spur gear generating!"}
  "spring 120"           → {"shape":"spring","size":120,"height":120,"message":"Spring coming up!"}
  "wheel 200"            → {"shape":"wheel","size":200,"message":"Wheel launching now!"}
"""
 
def ask_ollama(user_input):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\nUser: {user_input}\nJSON:",
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 250}
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=30)
        r.raise_for_status()
        raw = r.json().get("response", "")
        m = re.search(r"\{[\s\S]*?\}", raw)
        if m:
            return json.loads(m.group())
    except Exception:
        pass
    return None
 
# ================================================================
# FREECAD RUNNER
# ================================================================
def run_cad(code, label="Part"):
    if not os.path.exists(FREECAD):
        return f"❌ FreeCAD not found:\n{FREECAD}"
    uid      = str(uuid.uuid4())[:8]
    filepath = os.path.join(os.path.expanduser("~"), f"cad_{uid}.py")
    indented = "\n".join("    " + ln for ln in code.strip().splitlines())
    script = f"""import FreeCAD as App
import Part
import math
 
doc = App.newDocument("{label}")
try:
{indented}
    doc.recompute()
    Part.show(result)
except Exception as e:
    import sys
    print("CAD ERROR:", e, file=sys.stderr)
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(script)
    subprocess.Popen([FREECAD, filepath])
    return f"✅ {label} launched in FreeCAD!"
 
# ================================================================
# HELPER
# ================================================================
def val(d, key, fallback):
    v = d.get(key)
    try:
        return int(v) if v and int(v) > 0 else fallback
    except Exception:
        return fallback
 
# ================================================================
# CAD SHAPE LIBRARY  (15 shapes)
# ================================================================
 
def cad_arm(p):
    S = val(p, "size", 140)
    code = f"""
S = {S}
outer   = Part.makeCone(S*0.50, S*0.35, S*0.60)
inner   = Part.makeCone(S*0.45, S*0.30, S*0.56)
socket  = outer.cut(inner)
rim     = Part.makeSphere(S*0.20)
rim.translate(App.Vector(0, 0, S*0.60))
socket  = socket.fuse(rim)
shoulder = Part.makeSphere(S*0.22)
shoulder.translate(App.Vector(0, 0, S*0.50))
upper = Part.makeCone(S*0.18, S*0.12, S*1.00)
upper.translate(App.Vector(0, 0, S*0.60))
joint = Part.makeCylinder(S*0.10, S*0.40)
joint.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
joint.translate(App.Vector(0, 0, S*1.60))
fore = Part.makeCone(S*0.14, S*0.10, S*1.00)
fore.translate(App.Vector(0, 0, S*1.60))
wrist = Part.makeSphere(S*0.10)
wrist.translate(App.Vector(0, 0, S*2.60))
palm = Part.makeBox(S*0.50, S*0.35, S*0.18)
palm.translate(App.Vector(-S*0.25, 0, S*2.80))
def make_finger(x):
    r = S*0.035
    f1 = Part.makeCylinder(r,      S*0.17)
    f2 = Part.makeCylinder(r*0.90, S*0.15)
    f3 = Part.makeCylinder(r*0.80, S*0.13)
    f1.translate(App.Vector(x, S*0.35, S*2.90))
    f2.translate(App.Vector(x, S*0.35, S*2.90+S*0.17))
    f3.translate(App.Vector(x, S*0.35, S*2.90+S*0.17+S*0.15))
    return f1.fuse(f2).fuse(f3)
hand = palm
for px in [-S*0.18, -S*0.06, S*0.06, S*0.18]:
    hand = hand.fuse(make_finger(px))
thumb = Part.makeCylinder(S*0.035, S*0.30)
thumb.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 50)
thumb.translate(App.Vector(-S*0.25, S*0.10, S*2.90))
hand = hand.fuse(thumb)
result = socket.fuse(shoulder).fuse(upper).fuse(joint).fuse(fore).fuse(wrist).fuse(hand)
"""
    return code, "Prosthetic Arm"
 
 
def cad_box(p):
    S = val(p,"size",100); W = val(p,"width",60); H = val(p,"height",40); T = val(p,"thickness",5)
    code = f"""
outer = Part.makeBox({S}, {W}, {H})
inner = Part.makeBox({S-T*2}, {W-T*2}, {H-T})
inner.translate(App.Vector({T}, {T}, {T}))
result = outer.cut(inner)
"""
    return code, "Hollow Box"
 
 
def cad_sphere(p):
    S = val(p,"size",80)
    return f"result = Part.makeSphere({S})", "Sphere"
 
 
def cad_cylinder(p):
    S = val(p,"size",60); H = val(p,"height",120); T = val(p,"thickness",6)
    code = f"""
outer  = Part.makeCylinder({S}, {H})
inner  = Part.makeCylinder({max(1,S-T)}, {H})
result = outer.cut(inner)
"""
    return code, "Hollow Cylinder"
 
 
def cad_cone(p):
    S = val(p,"size",50); H = val(p,"height",100)
    return f"result = Part.makeCone({S}, {max(1,S//10)}, {H})", "Cone"
 
 
def cad_gear(p):
    S = val(p,"size",60); TH = val(p,"thickness",20)
    code = f"""
R  = {S}
r  = R * 0.75
th = {TH}
n  = 18
base   = Part.makeCylinder(r, th)
result = base
for i in range(n):
    angle = 2*math.pi*i/n
    tooth = Part.makeBox(r*0.22, r*0.30, th)
    tooth.translate(App.Vector(-r*0.11, 0, 0))
    tooth.rotate(App.Vector(0,0,0), App.Vector(0,0,1), math.degrees(angle))
    cx = r*0.88*math.cos(angle)
    cy = r*0.88*math.sin(angle)
    tooth.translate(App.Vector(cx, cy, 0))
    result = result.fuse(tooth)
hub  = Part.makeCylinder(r*0.28, th)
axle = Part.makeCylinder(r*0.10, th)
result = result.fuse(hub).cut(axle)
"""
    return code, "Spur Gear"
 
 
def cad_bolt(p):
    S = val(p,"size",8); H = val(p,"height",50); TH = val(p,"thickness",12)
    code = f"""
shaft = Part.makeCylinder({S}, {H})
head  = Part.makeCylinder({TH}, {TH//2})
head.translate(App.Vector(0, 0, {H}))
slot  = Part.makeBox({TH*0.8}, {TH*0.15}, {TH//2+1})
slot.translate(App.Vector(-{TH*0.4}, -{TH*0.075}, {H}))
head  = head.cut(slot)
result = shaft.fuse(head)
"""
    return code, "Bolt"
 
 
def cad_bracket(p):
    S = val(p,"size",80); T = val(p,"thickness",6)
    code = f"""
base = Part.makeBox({S}, {T}, {S})
wall = Part.makeBox({T}, {S}, {S})
wall.translate(App.Vector(0, {T}, 0))
h1 = Part.makeCylinder({T//2}, {T}+2)
h1.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
h1.translate(App.Vector({S//2}, -1, {S//4}))
h2 = Part.makeCylinder({T//2}, {T}+2)
h2.rotate(App.Vector(0,0,0), App.Vector(1,0,0), 90)
h2.translate(App.Vector({S//2}, -1, {S*3//4}))
result = base.fuse(wall).cut(h1).cut(h2)
"""
    return code, "L-Bracket"
 
 
def cad_tube(p):
    S = val(p,"size",30); H = val(p,"height",150); T = val(p,"thickness",4)
    code = f"""
outer  = Part.makeCylinder({S}, {H})
inner  = Part.makeCylinder({max(1,S-T)}, {H})
result = outer.cut(inner)
"""
    return code, "Tube"
 
 
def cad_spring(p):
    S = val(p,"size",20); H = val(p,"height",120)
    code = f"""
radius = {S}
wire_r = {max(2, S//8)}
coils  = 10
height = {H}
result = Part.makeTorus(radius, wire_r)
for i in range(1, coils):
    t = Part.makeTorus(radius, wire_r)
    t.translate(App.Vector(0, 0, height*i/coils))
    result = result.fuse(t)
"""
    return code, "Spring"
 
 
def cad_wheel(p):
    S = val(p,"size",100); W = val(p,"width",30); T = val(p,"thickness",8)
    code = f"""
tire  = Part.makeCylinder({S},          {W})
rim   = Part.makeCylinder({max(1,S-T)}, {W})
hub   = Part.makeCylinder({S//5},       {W})
wheel = tire.cut(rim).fuse(hub)
sp_r  = {max(3, S//20)}
for i in range(5):
    sp = Part.makeCylinder(sp_r, {S - S//5 - T})
    sp.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    sp.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 72*i)
    sp.translate(App.Vector({S//5}, 0, {W//2}))
    wheel = wheel.fuse(sp)
axle  = Part.makeCylinder({max(2,S//12)}, {W})
result = wheel.cut(axle)
"""
    return code, "Spoked Wheel"
 
 
def cad_frame(p):
    S = val(p,"size",120); T = val(p,"thickness",6)
    code = f"""
top    = Part.makeBox({S},   {T},   {T})
bottom = Part.makeBox({S},   {T},   {T})
left   = Part.makeBox({T},   {S},   {T})
right  = Part.makeBox({T},   {S},   {T})
bottom.translate(App.Vector(0, {S-T}, 0))
right.translate(App.Vector({S-T}, 0, 0))
result = top.fuse(bottom).fuse(left).fuse(right)
"""
    return code, "Frame"
 
 
def cad_plate(p):
    S = val(p,"size",120); W = val(p,"width",80); T = val(p,"thickness",6)
    code = f"""
plate = Part.makeBox({S}, {W}, {T})
r = {T}
for hx, hy in [({T*2},{T*2}), ({S-T*2},{T*2}), ({T*2},{W-T*2}), ({S-T*2},{W-T*2})]:
    h = Part.makeCylinder(r, {T}+2)
    h.translate(App.Vector(hx, hy, -1))
    plate = plate.cut(h)
result = plate
"""
    return code, "Mounting Plate"
 
 
def cad_hex(p):
    S = val(p,"size",30); TH = val(p,"thickness",15)
    code = f"""
pts = [App.Vector({S}*math.cos(math.pi/6+math.pi*i/3),
                  {S}*math.sin(math.pi/6+math.pi*i/3), 0) for i in range(6)]
pts.append(pts[0])
wire   = Part.makePolygon(pts)
face   = Part.Face(wire)
hex3d  = face.extrude(App.Vector(0, 0, {TH}))
bore   = Part.makeCylinder({max(2,S//3)}, {TH})
result = hex3d.cut(bore)
"""
    return code, "Hex Nut"
 
 
def cad_pipe(p):
    S = val(p,"size",25); H = val(p,"height",200); T = val(p,"thickness",3)
    code = f"""
outer   = Part.makeCylinder({S},           {H})
inner   = Part.makeCylinder({max(1,S-T)},  {H})
flange1 = Part.makeCylinder({S+8}, 8)
flange2 = Part.makeCylinder({S+8}, 8)
flange2.translate(App.Vector(0, 0, {H-8}))
result  = outer.cut(inner).fuse(flange1).fuse(flange2)
"""
    return code, "Flanged Pipe"
 
 
# ================================================================
# SHAPE ROUTER
# ================================================================
SHAPES = {
    "arm": cad_arm, "box": cad_box, "sphere": cad_sphere,
    "cylinder": cad_cylinder, "cone": cad_cone, "gear": cad_gear,
    "bolt": cad_bolt, "bracket": cad_bracket, "tube": cad_tube,
    "spring": cad_spring, "wheel": cad_wheel, "frame": cad_frame,
    "plate": cad_plate, "hex": cad_hex, "pipe": cad_pipe,
}
 
def keyword_parse(text):
    t = text.lower()
    for kw in SHAPES:
        if kw in t:
            nums = re.findall(r"\d+", t)
            return {"shape": kw, "size": int(nums[0]) if nums else 120,
                    "message": f"Generating {kw} in keyword mode."}
    return None
 
# ================================================================
# PROCESS
# ================================================================
def process(cmd, status_cb):
    status_cb("🤖 Asking DeepSeek...")
    parsed = ask_ollama(cmd)
    if not parsed:
        status_cb("⚡ AI offline — keyword mode")
        parsed = keyword_parse(cmd)
    if not parsed:
        status_cb("Ready")
        return ("❓ Not recognised. Try:\n"
                "  arm 150 | gear 80 | spring 120 | box 100x60x40\n"
                "  wheel 200 | bolt 10 | bracket 80 | pipe 25")
    shape = parsed.get("shape", "").lower()
    msg   = parsed.get("message", f"Generating {shape}...")
    fn    = SHAPES.get(shape)
    if not fn:
        status_cb("Ready")
        return f"❓ Unknown shape '{shape}'. Available: {', '.join(SHAPES)}"
    code, label = fn(parsed)
    status_cb("🔨 Launching FreeCAD...")
    result = run_cad(code, label)
    status_cb("Ready")
    speak(msg)
    return f"🤖 {msg}\n{result}"
 
# ================================================================
# GUI  (dark theme, quick buttons, threaded)
# ================================================================
BG      = "#1e1e2e"
PANEL   = "#2a2a3e"
ACCENT  = "#7c6af7"
FG      = "#cdd6f4"
ENT_BG  = "#313244"
C_YOU   = "#f9e2af"
C_JAR   = "#a6e3a1"
C_ERR   = "#f38ba8"
C_INFO  = "#89b4fa"
 
def build_gui():
    root = tk.Tk()
    root.title("Jarvis CAD  v2  •  DeepSeek-R1:3B + FreeCAD")
    root.configure(bg=BG)
    root.geometry("860x640")
 
    # title bar
    tf = tk.Frame(root, bg=ACCENT, height=46)
    tf.pack(fill=tk.X)
    tk.Label(tf, text="⚙  JARVIS CAD ASSISTANT  v2", font=("Segoe UI",13,"bold"),
             bg=ACCENT, fg="white", pady=9).pack(side=tk.LEFT, padx=16)
    tk.Label(tf, text=f"DeepSeek  {OLLAMA_MODEL}  |  FreeCAD  |  pyttsx3",
             font=("Segoe UI",8), bg=ACCENT, fg="#ddd").pack(side=tk.RIGHT, padx=16)
 
    # chat
    chat = ScrolledText(root, bg=PANEL, fg=FG, font=("Consolas",10),
                        bd=0, relief=tk.FLAT, wrap=tk.WORD)
    chat.pack(fill=tk.BOTH, expand=True, padx=14, pady=(10,4))
    chat.tag_config("you",  foreground=C_YOU)
    chat.tag_config("jar",  foreground=C_JAR)
    chat.tag_config("err",  foreground=C_ERR)
    chat.tag_config("info", foreground=C_INFO)
 
    def log(text, tag="info"):
        chat.insert(tk.END, text+"\n", tag)
        chat.see(tk.END)
 
    # quick buttons
    qf = tk.Frame(root, bg=BG)
    qf.pack(fill=tk.X, padx=14, pady=2)
    tk.Label(qf, text="Quick:", bg=BG, fg="#888", font=("Segoe UI",8)).pack(side=tk.LEFT)
    for qc in ["arm 150","gear 80","spring 120","box 100x60x40",
               "wheel 100","bolt 10","bracket 80","pipe 25","hex 30","plate 120"]:
        tk.Button(qf, text=qc, bg=ENT_BG, fg=FG, font=("Segoe UI",8),
                  relief=tk.FLAT, bd=0, padx=5, pady=2,
                  command=lambda c=qc: quick(c)).pack(side=tk.LEFT, padx=2)
 
    # input row
    inf = tk.Frame(root, bg=BG)
    inf.pack(fill=tk.X, padx=14, pady=(6,4))
    entry = tk.Entry(inf, bg=ENT_BG, fg=FG, font=("Segoe UI",11),
                     bd=0, relief=tk.FLAT, insertbackground=FG)
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0,8))
    btn = tk.Button(inf, text="Generate ▶", bg=ACCENT, fg="white",
                    font=("Segoe UI",10,"bold"), relief=tk.FLAT, bd=0, padx=14, pady=6)
    btn.pack(side=tk.LEFT)
 
    # status bar
    sv = tk.StringVar(value="Ready  —  type a command or click a quick button")
    tk.Label(root, textvariable=sv, bg=PANEL, fg="#888",
             font=("Segoe UI",8), anchor=tk.W, pady=4).pack(fill=tk.X, side=tk.BOTTOM)
 
    def set_status(m): sv.set(m); root.update_idletasks()
 
    def do_send(cmd):
        cmd = cmd.strip()
        if not cmd: return
        entry.delete(0, tk.END)
        log(f"\nYou: {cmd}", "you")
        btn.config(state=tk.DISABLED)
        def worker():
            res = process(cmd, set_status)
            tag = "err" if res.startswith("❌") else "jar"
            log(f"Jarvis: {res}", tag)
            btn.config(state=tk.NORMAL)
        threading.Thread(target=worker, daemon=True).start()
 
    def quick(c): entry.delete(0,tk.END); entry.insert(0,c); do_send(c)
 
    btn.config(command=lambda: do_send(entry.get()))
    entry.bind("<Return>", lambda e: do_send(entry.get()))
 
    # welcome
    log("╔══════════════════════════════════════════════╗")
    log("║   JARVIS CAD  v2  •  DeepSeek R1:3B + FreeCAD  ║")
    log("╚══════════════════════════════════════════════╝")
    log("15 shapes: arm | box | sphere | cylinder | cone | gear")
    log("           bolt | bracket | tube | spring | wheel | frame")
    log("           plate | hex | pipe")
    log("\nMake sure Ollama is running before use:")
    log("   ollama run deepseek-r1:3b")
    log("\nFalls back to keyword mode if Ollama is offline.\n")
 
    root.mainloop()
 
if __name__ == "__main__":
    build_gui()
 