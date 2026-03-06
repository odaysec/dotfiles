#!/usr/bin/env python3

import sys, os, time, math, random, socket, threading, subprocess
import urllib.request, urllib.error, http.client, ssl, struct, select
from datetime import datetime

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"

C0  = "\033[38;5;232m"   
C1  = "\033[38;5;235m"   
C2  = "\033[38;5;240m" 
C3  = "\033[38;5;245m"  
C4  = "\033[38;5;252m" 
C5  = "\033[38;5;255m"   

A1  = "\033[38;5;208m"   
A2  = "\033[38;5;220m"   
A3  = "\033[38;5;202m"   

G1  = "\033[38;5;22m"   
G2  = "\033[38;5;28m"   
G3  = "\033[38;5;40m"   

T1  = "\033[38;5;23m"    
T2  = "\033[38;5;30m"    
T3  = "\033[38;5;37m"    

RE1 = "\033[38;5;88m"    
RE2 = "\033[38;5;124m"   
RE3 = "\033[38;5;160m"  

BG_DARK = "\033[48;5;232m"
BG_MID  = "\033[48;5;234m"

W = 78   

def cls():      os.system('clear' if os.name != 'nt' else 'cls')
def hide():     sys.stdout.write("\033[?25l"); sys.stdout.flush()
def show():     sys.stdout.write("\033[?25h"); sys.stdout.flush()
def up(n):      sys.stdout.write(f"\033[{n}A"); sys.stdout.flush()
def clr():      sys.stdout.write("\033[2K"); sys.stdout.flush()
def p(s=""):    print(s)
def w(s):       sys.stdout.write(s); sys.stdout.flush()

def strip_ansi(s):
    import re
    return re.sub(r'\033\[[0-9;]*[mA-Z]', '', s)

def rpad(s, n):
    """Pad string to width n, accounting for ANSI codes."""
    clean = strip_ansi(s)
    diff = n - len(clean)
    return s + (" " * max(0, diff))

def banner():
    cls()
    ts = datetime.now().strftime("%Y-%m-%d  %H:%M:%S UTC")
    sid = ''.join(random.choices('0123456789ABCDEF', k=8))
    p(f"{C2}  {'─'*74}{R}")
    p(f"{C2}  │{R}  {A1}{B}NETPROBE INTELLIGENCE SUITE{R}  {C3}v3.1.0{R}  {DIM}{C2}·  CLASSIFIED NETWORK ANALYSIS{R}  {C2}│{R}")
    p(f"{C2}  │{R}  {DIM}{C2}SESSION:{R} {C3}{sid}{R}   {DIM}{C2}TIMESTAMP:{R} {C3}{ts}{R}                          {C2}│{R}")
    p(f"{C2}  {'─'*74}{R}")
    p()

def boot():
    cls()

    header = [
        f"",
        f"  {A1}{'▄'*72}{R}",
        f"  {A1}█{R}{B}{C5}{'  N E T P R O B E   I N T E L L I G E N C E   S U I T E':^70}{R}{A1}█{R}",
        f"  {A1}█{R}{C3}{'  CLASSIFIED  ·  NETWORK ANALYSIS SYSTEM  ·  OPERATIONAL SECURITY':^70}{R}{A1}█{R}",
        f"  {A1}{'▀'*72}{R}",
        f"",
    ]
    for ln in header:
        p(ln)

    init_sequence = [
        ("KERNEL MODULE",        "netprobe_core.ko",       True,  0.07),
        ("SOCKET LAYER",         "AF_INET  AF_INET6",       True,  0.05),
        ("INTERFACE SCAN",       "eth0  lo  wlan0",         True,  0.08),
        ("SSL CONTEXT",          "TLSv1.3 cipher suite",   True,  0.06),
        ("RADAR SUBSYSTEM",      "sweep engine v2.1",       True,  0.07),
        ("TELEMETRY ENGINE",     "multi-thread handler",    True,  0.05),
        ("CLASSIFICATION SYS",   "CONFIDENTIAL tier",       True,  0.09),
        ("ISP FINGERPRINT",      "bypass mode active",      True,  0.07),
        ("OPERATIONAL STATUS",   "ALL SYSTEMS GO",          True,  0.10),
    ]

    for module, detail, ok, delay in init_sequence:
        status = f"{G3}[ ONLINE ]{R}" if ok else f"{RE3}[ FAILED ]{R}"
        dots = "." * random.randint(12, 22)
        line = f"  {DIM}{C3}INIT{R}  {A1}{module:<22}{R}  {DIM}{C2}{dots}{R}  {DIM}{C3}{detail:<28}{R}  {status}"

    for _ in range(1):
            gline = ''.join(
                random.choice('▒░█▓') if (random.random() < 0.04 and c.isalpha()) else c
                for c in line[:40]
            ) + line[40:]
            w(f"\r{gline}")
            time.sleep(0.015)
        w(f"\r{line}\n")
        time.sleep(delay)

    time.sleep(0.2)
    p()
    p(f"  {G3}▶{R}  {C4}System initialized.{R}  {DIM}{C2}Awaiting tasking...{R}")
    time.sleep(0.4)

def divider(label="", style="thin"):
    if style == "thick":
        p(f"\n  {A1}{'━'*74}{R}\n")
    elif style == "section":
        if label:
            pad = 74 - len(label) - 4
            p(f"\n  {C2}┌─{R}  {A1}{B}{label}{R}  {C2}{'─'*pad}┐{R}")
        else:
            p(f"  {C2}{'─'*74}{R}")
    elif style == "close":
        p(f"  {C2}└{'─'*74}┘{R}\n")
    else:
        p(f"  {C2}{'─'*74}{R}")

def label_val(key, val, kw=22, kcolor=C2, vcolor=C4):
    p(f"  {DIM}{kcolor}{key:<{kw}}{R}  {DIM}{C2}│{R}  {vcolor}{val}{R}")

def label_val_inline(key, val, kw=22, kcolor=C2, vcolor=C4):
    return f"  {DIM}{kcolor}{key:<{kw}}{R}  {DIM}{C2}│{R}  {vcolor}{val}{R}"

def scan_bar(label, duration=2.0, color=A1):
    """Horizontal scanning progress bar."""
    BW = 48
    t0 = time.time()
    frames = "▏▎▍▌▋▊▉█"
    p()
    while True:
        elapsed = time.time() - t0
        pct = min(elapsed / duration, 1.0)
        filled = int(pct * BW)
        partial_idx = int((pct * BW - filled) * len(frames))
        partial = frames[partial_idx] if filled < BW else ""
        empty = BW - filled - (1 if partial else 0)

        bar = (f"{color}{B}{'█'*filled}{R}"
               f"{color}{partial}{R}"
               f"{DIM}{C1}{'░'*empty}{R}")

        status = f"{G3}COMPLETE{R}" if pct >= 1.0 else f"{A1}SCANNING{R}"
        w(f"\r  {DIM}{C2}{label:<20}{R}  [{bar}]  {DIM}{C2}{int(pct*100):3d}%{R}  {status}  ")

        if pct >= 1.0:
            w("\n")
            break
        time.sleep(0.04)

RADAR_R  = 9
RADAR_CX = 11   
RADAR_CY = 10

def render_radar(angle_deg, blips, sweep_trail=True):
    rows = []
    sweep_rad = math.radians(angle_deg)

    for y in range(RADAR_CY * 2 + 1):
        row_chars = []
        for x in range(RADAR_CX * 4 + 1):
            cx = RADAR_CX * 2
            cy = RADAR_CY
            dx = (x - cx) / 2.0
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > RADAR_R + 0.6:
                row_chars.append('  ')
                continue

            if abs(dist - RADAR_R) < 0.65:
                row_chars.append(f"{C2}· {R}")
                continue

            ring_hit = False
            for r_frac in [0.33, 0.66]:
                if abs(dist - RADAR_R * r_frac) < 0.38:
                    row_chars.append(f"{DIM}{C1}· {R}")
                    ring_hit = True
                    break
            if ring_hit:
                continue

            if abs(dx) < 0.22:
                row_chars.append(f"{DIM}{C2}│ {R}")
                continue
            if abs(dy) < 0.35:
                row_chars.append(f"{DIM}{C2}──{R}")
                continue

            blip_hit = False
            for bx, by, age in blips:
                bdx = (x - cx) / 2.0 - bx
                bdy = y - cy - by
                if abs(bdx) < 0.65 and abs(bdy) < 0.65:
                    symbols = [
                        f"{A2}{B}◈ {R}",
                        f"{A1}◆ {R}",
                        f"{C3}◇ {R}",
                        f"{DIM}{C2}· {R}",
                    ]
                    row_chars.append(symbols[min(age, 3)])
                    blip_hit = True
                    break
            if blip_hit:
                continue

            point_angle = math.atan2(-dy, dx)
            diff = (point_angle - sweep_rad) % (2 * math.pi)
            if diff > math.pi:
                diff -= 2 * math.pi

            if sweep_trail:
                if -0.12 < diff < 0.12 and dist < RADAR_R:
                    row_chars.append(f"{A1}{B}▓▓{R}")
                    continue
                elif -0.35 < diff < 0 and dist < RADAR_R:
                    fade_intensity = 1 - abs(diff) / 0.35
                    if fade_intensity > 0.6:
                        row_chars.append(f"{A1}▒▒{R}")
                    else:
                        row_chars.append(f"{DIM}{C3}░░{R}")
                    continue

            row_chars.append(f"{DIM}{C0}  {R}")

        rows.append("".join(row_chars))
    return rows

def _vert_bar(speed, max_spd, height=14):
    """Return list of strings for vertical speed bar."""
    filled = int(min(speed / max_spd, 1.0) * height) if max_spd > 0 else 0
    lines = []
    for i in range(height - 1, -1, -1):
        if i < filled:
            frac = i / height
            if frac > 0.66:   color = G3
            elif frac > 0.33: color = A1
            else:              color = RE3
            lines.append(f"{color}██{R}")
        else:
            lines.append(f"{DIM}{C1}░░{R}")
    return lines

def live_panel(test_type, speed_ref, done_evt):
    is_dl = test_type == "download"
    label  = "DOWNLINK ANALYSIS" if is_dl else "UPLINK ANALYSIS"
    arrow  = "▼" if is_dl else "▲"
    color  = T3 if is_dl else A1

    angle  = 0
    blips  = []
    first  = True
    HEIGHT = 21   

    def fmt_speed(s):
        if s < 1:    return f"{s*1000:.1f} Kbps"
        if s < 1000: return f"{s:.2f} Mbps"
        return f"{s/1000:.2f} Gbps"

    def speed_class(s):
        if s < 5:    return f"{RE3}CRITICAL {R}", RE3
        if s < 20:   return f"{RE2}DEGRADED {R}", RE2
        if s < 50:   return f"{A1}NOMINAL  {R}", A1
        if s < 150:  return f"{G3}OPTIMAL  {R}", G3
        if s < 500:  return f"{T3}SUPERIOR {R}", T3
        return f"{A2}{B}MAXIMUM  {R}", A2

    hide()
    p()

    while not done_evt.is_set() or not first:
        speed = speed_ref[0]
        angle = (angle + 7) % 360

        if random.random() < 0.22:
            br = random.uniform(1.2, RADAR_R - 1)
            ba = random.uniform(0, 2 * math.pi)
            blips.append([br * math.cos(ba), br * math.sin(ba), 0])
        blips = [[bx, by, a+1] for bx, by, a in blips if a < 4]

        radar = render_radar(angle, blips)

        max_s = max(100, speed * 1.5 + 10)
        cls_str, cls_color = speed_class(speed)
        vbar = _vert_bar(speed, max_s, 14)
        bar_pct = min(speed / max_s, 1.0)
        hbar_w = 24
        hbar_f = int(bar_pct * hbar_w)
        hbar = f"{cls_color}{'█'*hbar_f}{DIM}{C1}{'░'*(hbar_w-hbar_f)}{R}"
        spd_str = fmt_speed(speed)

        ts = datetime.now().strftime("%H:%M:%S")
        samp = random.randint(1, 99)

        rp = []
        rp.append(f"  {DIM}{C2}┌{'─'*32}┐{R}")
        rp.append(f"  {DIM}{C2}│{R}  {color}{B}{arrow} {label:<26}{R}  {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{'─'*32}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  {DIM}{C2}LIVE THROUGHPUT{R}                {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  {cls_color}{B}{spd_str:>20}{R}          {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  [{hbar}]     {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{'─'*32}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  {DIM}{C2}SIGNAL LEVEL{R}     {DIM}{C2}SAMPLES{R}        {DIM}{C2}│{R}")
        for i, vb in enumerate(vbar):
            rp.append(f"  {DIM}{C2}│{R}  {vb}                             {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{'─'*32}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  {DIM}{C2}STATUS:{R}  {cls_str}                 {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}│{R}  {DIM}{C2}TS:{R} {C3}{ts}{R}  {DIM}{C2}PKT #{R}{C3}{samp:04d}{R}           {DIM}{C2}│{R}")
        rp.append(f"  {DIM}{C2}└{'─'*32}┘{R}")

        combined = []
        for i in range(max(len(radar), len(rp))):
            left  = f"  {radar[i]}" if i < len(radar) else " " * 48
            right = rp[i] if i < len(rp) else ""
            combined.append(f"{left}  {right}")

        if first:
            for ln in combined:
                p(ln)
            first = False
        else:
            up(len(combined))
            for ln in combined:
                clr()
                p(ln)

        time.sleep(0.065)

        if done_evt.is_set():
            break

    show()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)); ip = s.getsockname()[0]; s.close(); return ip
    except: return "UNAVAILABLE"

def get_hostname():
    try: return socket.gethostname()
    except: return "UNKNOWN"

def tcp_latency(host="8.8.8.8", port=53, n=8):
    times = []
    for _ in range(n):
        try:
            t0 = time.time()
            s = socket.create_connection((host, port), timeout=3)
            t1 = time.time()
            s.close()
            times.append((t1-t0)*1000)
        except: pass
        time.sleep(0.05)
    if times:
        return min(times), sum(times)/len(times), max(times)
    return None, None, None

def measure_jitter(host="8.8.8.8", port=53, n=12):
    times = []
    for _ in range(n):
        try:
            t0 = time.time()
            s = socket.create_connection((host, port), timeout=3)
            t1 = time.time()
            s.close()
            times.append((t1-t0)*1000)
        except: pass
        time.sleep(0.04)
    if len(times) > 1:
        diffs = [abs(times[i+1]-times[i]) for i in range(len(times)-1)]
        return sum(diffs)/len(diffs)
    return None

def measure_packet_loss(host="8.8.8.8", port=53, n=10):
    sent = 0; recv = 0
    for _ in range(n):
        sent += 1
        try:
            s = socket.create_connection((host, port), timeout=2)
            s.close(); recv += 1
        except: pass
        time.sleep(0.05)
    return round((1 - recv/sent)*100, 1) if sent else None

DOWNLOAD_URLS = [
    "http://speed.cloudflare.com/__down?bytes=10000000",
    "http://speedtest.tele2.net/10MB.zip",
    "http://ipv4.download.thinkbroadband.com/10MB.zip",
]

def measure_download(progress_cb=None):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    for url in DOWNLOAD_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'NETPROBE/3.1'})
            t0 = time.time(); total = 0
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                while True:
                    chunk = resp.read(65536)
                    if not chunk: break
                    total += len(chunk)
                    e = time.time()-t0
                    if progress_cb and e > 0:
                        progress_cb((total*8)/(e*1_000_000), total)
                    if e > 14: break
            e = time.time()-t0
            if total > 0 and e > 0:
                return (total*8)/(e*1_000_000)
        except: continue
    return None

def measure_upload(progress_cb=None):
    try:
        data = os.urandom(5*1024*1024)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
        conn = http.client.HTTPSConnection("httpbin.org", timeout=20, context=ctx)
        conn.putrequest('POST', '/post')
        conn.putheader('Content-Type', 'application/octet-stream')
        conn.putheader('Content-Length', str(len(data)))
        conn.putheader('User-Agent', 'NETPROBE/3.1')
        conn.endheaders()
        t0 = time.time(); sent = 0
        while sent < len(data):
            chunk = data[sent:sent+65536]
            conn.send(chunk); sent += len(chunk)
            e = time.time()-t0
            if progress_cb and e > 0:
                progress_cb((sent*8)/(e*1_000_000), sent)
        conn.getresponse(); e = time.time()-t0; conn.close()
        if e > 0: return (len(data)*8)/(e*1_000_000)
    except: pass
    return None

def print_results(ping_min, ping_avg, ping_max, jitter, pkt_loss,
                  dl, ul, local_ip, hostname):

    def tier(mbps, thresholds, labels):
        for t, l in zip(thresholds, labels):
            if mbps is not None and mbps < t: return l
        return labels[-1]

    def color_speed(mbps):
        if mbps is None: return C3, "N/A"
        if mbps < 10:  return RE3, f"{mbps:.2f} Mbps"
        if mbps < 50:  return A1,  f"{mbps:.2f} Mbps"
        if mbps < 200: return G3,  f"{mbps:.2f} Mbps"
        return T3, f"{mbps:.2f} Mbps"

    def color_ping(ms):
        if ms is None: return C3, "N/A"
        if ms < 20:  return G3,  f"{ms:.1f} ms"
        if ms < 60:  return A1,  f"{ms:.1f} ms"
        if ms < 150: return RE2, f"{ms:.1f} ms"
        return RE3, f"{ms:.1f} ms"

    def rating_bar(val, max_val, width=28, color=G3):
        if val is None: return f"{DIM}{C1}{'░'*width}{R}"
        filled = min(int((val/max_val)*width), width)
        return f"{color}{'█'*filled}{DIM}{C1}{'░'*(width-filled)}{R}"

    p()
    p(f"  {A1}{'━'*74}{R}")
    p(f"  {A1}█{R}  {B}{C5}{'OPERATIONAL INTELLIGENCE REPORT':^70}{R}  {A1}█{R}")
    p(f"  {A1}█{R}  {DIM}{C3}{'NETWORK ASSESSMENT  ·  CONFIDENTIAL  ·  '+datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'):^70}{R}  {A1}█{R}")
    p(f"  {A1}{'━'*74}{R}")
    p()

    p(f"  {DIM}{C2}┌─ ASSET IDENTIFICATION {'─'*50}┐{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C2}HOSTNAME{R}              {DIM}{C2}│{R}  {C4}{hostname}{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C2}LOCAL ADDRESS{R}         {DIM}{C2}│{R}  {C4}{local_ip}{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C2}ANALYSIS TIMESTAMP{R}    {DIM}{C2}│{R}  {C4}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C2}CLASSIFICATION{R}        {DIM}{C2}│{R}  {A1}CONFIDENTIAL // EYES ONLY{R}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()

    p(f"  {DIM}{C2}┌─ LATENCY ASSESSMENT {'─'*51}┐{R}")

    pc, pv = color_ping(ping_avg)
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'PING  MIN':14}{R}  {DIM}{C2}│{R}  {color_ping(ping_min)[0]}{color_ping(ping_min)[1]:<16}{R}  {rating_bar(ping_min, 200, 28, G3)}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'PING  AVG':14}{R}  {DIM}{C2}│{R}  {pc}{pv:<16}{R}  {rating_bar(ping_avg, 200, 28, A1)}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'PING  MAX':14}{R}  {DIM}{C2}│{R}  {color_ping(ping_max)[0]}{color_ping(ping_max)[1]:<16}{R}  {rating_bar(ping_max, 200, 28, RE2)}")
    jc, jv = color_ping(jitter)
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'JITTER':14}{R}  {DIM}{C2}│{R}  {jc}{jv:<16}{R}  {rating_bar(jitter, 100, 28, A1)}")

    pl_color = G3 if (pkt_loss or 0) < 1 else (A1 if (pkt_loss or 0) < 5 else RE3)
    pl_str = f"{pkt_loss:.1f}%" if pkt_loss is not None else "N/A"
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'PACKET LOSS':14}{R}  {DIM}{C2}│{R}  {pl_color}{pl_str:<16}{R}  {rating_bar(100-(pkt_loss or 0), 100, 28, pl_color)}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()

    p(f"  {DIM}{C2}┌─ THROUGHPUT ANALYSIS {'─'*50}┐{R}")

    dc, dv = color_speed(dl)
    dl_tier = tier(dl or 0,
        [5,    25,    50,   100,   300,   float('inf')],
        ["CRITICAL","MARGINAL","OPERATIONAL","PROFICIENT","SUPERIOR","MAXIMUM"])
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'DOWNLINK':14}{R}  {DIM}{C2}│{R}  {dc}{B}{dv:<16}{R}  {rating_bar(dl, 1000, 28, T3)}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'':14}{R}  {DIM}{C2}│{R}  {DIM}{C2}TIER:{R}  {dc}{dl_tier}{R}")
    p()

    uc, uv = color_speed(ul)
    ul_tier = tier(ul or 0,
        [2,   10,   25,    50,   150,   float('inf')],
        ["CRITICAL","MARGINAL","OPERATIONAL","PROFICIENT","SUPERIOR","MAXIMUM"])
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'UPLINK':14}{R}  {DIM}{C2}│{R}  {uc}{B}{uv:<16}{R}  {rating_bar(ul, 500, 28, A1)}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}{'':14}{R}  {DIM}{C2}│{R}  {DIM}{C2}TIER:{R}  {uc}{ul_tier}{R}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()

    if dl and ul and ping_avg is not None:
        score = min(100, int(
            (min(dl,  500)/500  * 40) +
            (min(ul,  200)/200  * 25) +
            (max(0, (150 - ping_avg))/150 * 20) +
            (max(0, (50  - (jitter or 50)))/50  * 10) +
            (max(0, (100 - (pkt_loss or 0)))/100 * 5)
        ))
        if score >= 85:   sg, sl, sc = G3,  "SUPERIOR CAPABILITY    ", G3
        elif score >= 65: sg, sl, sc = T3,  "OPERATIONAL CAPABILITY ", T3
        elif score >= 45: sg, sl, sc = A1,  "LIMITED CAPABILITY     ", A1
        elif score >= 25: sg, sl, sc = RE2, "DEGRADED CAPABILITY    ", RE2
        else:              sg, sl, sc = RE3, "CRITICAL FAILURE       ", RE3

        sb_w = 50
        sb_f = int((score/100)*sb_w)
        score_bar = f"{sc}{'█'*sb_f}{DIM}{C1}{'░'*(sb_w-sb_f)}{R}"

        p(f"  {A1}┌─ COMPOSITE THREAT ASSESSMENT {'─'*43}┐{R}")
        p(f"  {A1}│{R}  {score_bar}")
        p(f"  {A1}│{R}  {DIM}{C3}CAPABILITY INDEX:{R}  {sg}{B}{score:3d} / 100{R}   {DIM}{C2}│{R}  {sc}{B}{sl}{R}")
        p(f"  {A1}└{'─'*72}┘{R}")
    p()

    rnd = ''.join(random.choices('0123456789ABCDEF', k=16))
    p(f"  {DIM}{C2}{'─'*74}{R}")
    p(f"  {DIM}{C2}REPORT ID:{R}  {C3}{rnd}{R}  {DIM}{C2}·  END OF ASSESSMENT  ·  DESTROY AFTER READING{R}")
    p(f"  {DIM}{C2}{'─'*74}{R}")
    p()

def print_help():
    boot()
    banner()
    p(f"  {A1}{'━'*74}{R}")
    p(f"  {A1}█{R}  {B}{C5}{'COMMAND REFERENCE  ·  NETPROBE INTELLIGENCE SUITE':^70}{R}  {A1}█{R}")
    p(f"  {A1}{'━'*74}{R}")
    p()
    cmds = [
        ("(no args)",    "Full spectrum analysis  [ PING + DOWNLINK + UPLINK ]"),
        ("--ping",       "Latency & stability assessment only"),
        ("--download",   "Downlink throughput analysis only"),
        ("--upload",     "Uplink throughput analysis only"),
        ("--quick",      "Rapid assessment  [ PING + DOWNLINK ]"),
        ("--info",       "Asset identification — network identity report"),
        ("--help",       "Display this command reference"),
    ]
    p(f"  {DIM}{C2}┌─ COMMANDS {'─'*62}┐{R}")
    for cmd, desc in cmds:
        p(f"  {DIM}{C2}│{R}  {A1}{cmd:<16}{R}  {DIM}{C2}│{R}  {C3}{desc}{R}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()
    p(f"  {DIM}{C2}┌─ CAPABILITIES {'─'*58}┐{R}")
    caps = [
        "Animated radar sweep with contact tracking",
        "Live throughput meter with signal-level visualisation",
        "TCP latency  ·  min / avg / max  ·  jitter  ·  packet loss",
        "Composite capability index  [0–100]",
        "Hacker-style boot sequence with glitch effects",
        "Color-coded tier classification system",
        "Network asset identification  (hostname · IP · timestamp)",
        "Zero external dependencies  ·  pure Python stdlib",
    ]
    for c in caps:
        p(f"  {DIM}{C2}│{R}  {G3}►{R}  {C3}{c}{R}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()
    p(f"  {DIM}{C2}USAGE:{R}  {C4}python3 netprobe.py {DIM}[OPTION]{R}")
    p()

def run(mode="full"):
    boot()
    banner()

    local_ip = get_local_ip()
    hostname = get_hostname()

    p(f"  {DIM}{C2}┌─ ASSET IDENTIFICATION {'─'*50}┐{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}HOSTNAME{R}          {DIM}{C2}│{R}  {C4}{hostname}{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}LOCAL ADDRESS{R}     {DIM}{C2}│{R}  {C4}{local_ip}{R}")
    p(f"  {DIM}{C2}│{R}  {DIM}{C3}ANALYSIS MODE{R}     {DIM}{C2}│{R}  {A1}{mode.upper()}{R}")
    p(f"  {DIM}{C2}└{'─'*72}┘{R}")
    p()

    ping_min = ping_avg = ping_max = jitter = pkt_loss = None
    dl = ul = None

    if mode in ("full", "ping", "quick"):
        p(f"  {A1}▸{R}  {C4}TASKING:{R}  {C3}Latency & stability assessment  ·  target 8.8.8.8:53{R}")
        scan_bar("TCP PROBE", 2.0, A1)

        mn, avg, mx = tcp_latency()
        ping_min, ping_avg, ping_max = mn, avg, mx
        if avg:
            p(f"\n  {DIM}{C3}LATENCY{R}  "
              f"{DIM}{C2}min{R} {G3}{mn:.1f}ms{R}  "
              f"{DIM}{C2}avg{R} {A1}{avg:.1f}ms{R}  "
              f"{DIM}{C2}max{R} {RE2}{mx:.1f}ms{R}")
        else:
            p(f"\n  {RE3}TARGET UNREACHABLE{R}")

        scan_bar("JITTER ANALYSIS", 1.8, A1)
        jitter = measure_jitter()
        if jitter: p(f"\n  {DIM}{C3}JITTER{R}  {A1}{jitter:.2f} ms{R}")

        scan_bar("PACKET LOSS PROBE", 2.0, RE2)
        pkt_loss = measure_packet_loss()
        if pkt_loss is not None: p(f"\n  {DIM}{C3}PACKET LOSS{R}  {A1}{pkt_loss:.1f}%{R}")
        p()

    if mode in ("full", "download", "quick"):
        p(f"  {T3}▸{R}  {C4}TASKING:{R}  {C3}Downlink throughput analysis  ·  multi-server{R}")
        p()

        speed_ref = [0.0]
        done_evt  = threading.Event()

        def dl_cb(s, _): speed_ref[0] = s

        t = threading.Thread(target=live_panel, args=("download", speed_ref, done_evt), daemon=True)
        t.start()

        result = measure_download(dl_cb)
        done_evt.set()
        t.join(timeout=3)

        dl = result or (speed_ref[0] if speed_ref[0] > 0 else None)
        if dl:
            p(f"\n  {G3}✓{R}  {C4}DOWNLINK CONFIRMED:{R}  {T3}{B}{dl:.2f} Mbps{R}")
        else:
            p(f"\n  {RE3}✘{R}  {C3}DOWNLINK UNREACHABLE  ·  check connectivity{R}")
        p()

    if mode in ("full",):
        p(f"  {A1}▸{R}  {C4}TASKING:{R}  {C3}Uplink throughput analysis  ·  POST endpoint{R}")
        p()

        speed_ref = [0.0]
        done_evt  = threading.Event()

        def ul_cb(s, _): speed_ref[0] = s

        t = threading.Thread(target=live_panel, args=("upload", speed_ref, done_evt), daemon=True)
        t.start()

        result = measure_upload(ul_cb)
        done_evt.set()
        t.join(timeout=3)

        ul = result or (speed_ref[0] if speed_ref[0] > 0 else None)
        if ul:
            p(f"\n  {G3}✓{R}  {C4}UPLINK CONFIRMED:{R}  {A1}{B}{ul:.2f} Mbps{R}")
        else:
            if dl:
                ul = max(0.5, dl * 0.30 + random.uniform(-1, 1))
                p(f"\n  {A1}!{R}  {C3}UPLINK ESTIMATED:{R}  {A1}{ul:.2f} Mbps{R}  {DIM}{C2}(endpoint unreachable){R}")
            else:
                p(f"\n  {RE3}✘{R}  {C3}UPLINK UNREACHABLE{R}")
        p()

    print_results(ping_min, ping_avg, ping_max, jitter, pkt_loss,
                  dl, ul, local_ip, hostname)

def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print_help(); return

    mode = "full"
    if   "--ping"     in args: mode = "ping"
    elif "--download" in args: mode = "download"
    elif "--upload"   in args: mode = "upload"
    elif "--info"     in args: mode = "info"
    elif "--quick"    in args: mode = "quick"

    if mode == "info":
        boot(); banner()
        p(f"  {DIM}{C2}┌─ ASSET IDENTIFICATION {'─'*50}┐{R}")
        p(f"  {DIM}{C2}│{R}  {DIM}{C3}HOSTNAME{R}          {DIM}{C2}│{R}  {C4}{get_hostname()}{R}")
        p(f"  {DIM}{C2}│{R}  {DIM}{C3}LOCAL ADDRESS{R}     {DIM}{C2}│{R}  {C4}{get_local_ip()}{R}")
        p(f"  {DIM}{C2}│{R}  {DIM}{C3}TIMESTAMP{R}         {DIM}{C2}│{R}  {C4}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{R}")
        p(f"  {DIM}{C2}└{'─'*72}┘{R}"); p(); return

    try:
        run(mode)
    except KeyboardInterrupt:
        show()
        p(f"\n\n  {A1}[!]{R}  {C3}OPERATION ABORTED  ·  user interrupt{R}\n")

if __name__ == "__main__":
    main()
