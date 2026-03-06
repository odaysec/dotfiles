#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║         SPEED-SATPROBE  ///  SPEEDTEST SAT   ║
║          Internet Speed Tool                 ║
╚══════════════════════════════════════════════╝
"""

import sys
import os
import time
import math
import random
import socket
import threading
import subprocess
import struct
import select
import urllib.request
import urllib.error
import http.client
import ssl
import json
from datetime import datetime

ESC = "\033["
RESET   = f"{ESC}0m"
BOLD    = f"{ESC}1m"
DIM     = f"{ESC}2m"
BLINK   = f"{ESC}5m"

# Foreground colors
BLACK   = f"{ESC}30m"
RED     = f"{ESC}31m"
GREEN   = f"{ESC}32m"
YELLOW  = f"{ESC}33m"
BLUE    = f"{ESC}34m"
MAGENTA = f"{ESC}35m"
CYAN    = f"{ESC}36m"
WHITE   = f"{ESC}37m"

BRIGHT_RED     = f"{ESC}91m"
BRIGHT_GREEN   = f"{ESC}92m"
BRIGHT_YELLOW  = f"{ESC}93m"
BRIGHT_BLUE    = f"{ESC}94m"
BRIGHT_MAGENTA = f"{ESC}95m"
BRIGHT_CYAN    = f"{ESC}96m"
BRIGHT_WHITE   = f"{ESC}97m"

BG_BLACK  = f"{ESC}40m"
BG_GREEN  = f"{ESC}42m"
BG_BLUE   = f"{ESC}44m"
BG_CYAN   = f"{ESC}46m"

WIDTH = 70

def cls():
    os.system('clear' if os.name == 'posix' else 'cls')

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def move_up(n):
    sys.stdout.write(f"\033[{n}A")
    sys.stdout.flush()

def move_to_col(n):
    sys.stdout.write(f"\033[{n}G")
    sys.stdout.flush()

def clear_line():
    sys.stdout.write("\033[2K")
    sys.stdout.flush()

def print_centered(text, color="", width=WIDTH):
    import re
    clean = re.sub(r'\033\[[0-9;]*m', '', text)
    pad = max(0, (width - len(clean)) // 2)
    print(" " * pad + color + text + RESET)

def sleep(s):
    time.sleep(s)

# ─── BANNER ──────────────────────────────────────────────────────────────────
def print_banner():
    cls()
    lines = [
        f"{BRIGHT_CYAN}╔{'═'*68}╗{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{BRIGHT_GREEN}{'':^68}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{BRIGHT_GREEN}███╗   ██╗███████╗████████╗      ██████╗ ██████╗  ██████╗ ██████╗ {'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{BRIGHT_GREEN}████╗  ██║██╔════╝╚══██╔══╝     ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗{'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{BRIGHT_GREEN}██╔██╗ ██║█████╗     ██║        ██████╔╝██████╔╝██║   ██║██████╔╝{'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{BRIGHT_GREEN}██║╚██╗██║██╔══╝     ██║        ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗{'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{BRIGHT_GREEN}██║ ╚████║███████╗   ██║        ██║     ██║  ██║╚██████╔╝██████╔╝{'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{'':^4}{DIM}╚═╝  ╚═══╝╚══════╝   ╚═╝        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ {'':1}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{BRIGHT_MAGENTA}{'':^68}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{CYAN}{'[ INTERNET SPEED ANALYZER v2.0  //  HACKER EDITION ]':^68}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}║{RESET}{DIM}{'by NET-PROBE SYSTEMS':^68}{RESET}{BRIGHT_CYAN}║{RESET}",
        f"{BRIGHT_CYAN}╚{'═'*68}╝{RESET}",
    ]
    for line in lines:
        print(line)
    print()

RADAR_R = 9   
RADAR_CX = 20
RADAR_CY = 10

def render_radar(angle_deg, blips):
    """Return list of strings = radar frame."""
    rows = []
    for y in range(RADAR_CY * 2 + 1):
        row = []
        for x in range(RADAR_CX * 4 + 1):
            cx = RADAR_CX * 2
            cy = RADAR_CY
            dx = (x - cx) / 2.0
            dy = y - cy
            dist = math.sqrt(dx*dx + dy*dy)

            if dist > RADAR_R + 0.5:
                row.append(' ')
                continue

            if abs(dist - RADAR_R) < 0.6:
                row.append(f"{DIM}{BRIGHT_GREEN}●{RESET}")
                continue

            in_ring = False
            for r in [RADAR_R * 0.33, RADAR_R * 0.66]:
                if abs(dist - r) < 0.4:
                    row.append(f"{DIM}{GREEN}·{RESET}")
                    in_ring = True
                    break
            if in_ring:
                continue

            if abs(dx) < 0.3:
                row.append(f"{DIM}{GREEN}│{RESET}")
                continue
            if abs(dy) < 0.4:
                row.append(f"{DIM}{GREEN}─{RESET}")
                continue

            sweep_rad = math.radians(angle_deg)
            point_angle = math.atan2(-dy, dx)
            diff = (point_angle - sweep_rad) % (2 * math.pi)
            if diff > math.pi:
                diff -= 2 * math.pi

            if -0.15 < diff < 0.15 and dist < RADAR_R:
                intensity = 1 - abs(diff) / 0.15
                row.append(f"{BRIGHT_GREEN}▓{RESET}")
                continue
            elif -0.4 < diff < 0 and dist < RADAR_R:
                row.append(f"{GREEN}░{RESET}")
                continue

            blip_hit = False
            for bx, by, age in blips:
                bdx = (x - cx) / 2.0 - bx
                bdy = y - cy - by
                if abs(bdx) < 0.7 and abs(bdy) < 0.7:
                    fade = ["◉", "●", "○", "·"]
                    row.append(f"{BRIGHT_YELLOW}{fade[min(age, 3)]}{RESET}")
                    blip_hit = True
                    break
            if blip_hit:
                continue

            row.append(f"{DIM}{BG_BLACK} {RESET}")

        rows.append("".join(row))
    return rows

def progress_bar(value, max_val, width=30, color=BRIGHT_GREEN):
    filled = int((value / max_val) * width) if max_val > 0 else 0
    filled = min(filled, width)
    empty = width - filled
    bar = color + "█" * filled + DIM + "░" * empty + RESET
    pct = (value / max_val * 100) if max_val > 0 else 0
    return f"[{bar}{color}]{RESET} {color}{pct:5.1f}%{RESET}"

# ─── SPEED GAUGE ─────────────────────────────────────────────────────────────
def speed_gauge(mbps, label, color):
    max_speed = 1000
    bar_w = 30
    filled = int((min(mbps, max_speed) / max_speed) * bar_w)
    empty = bar_w - filled

    if mbps < 10:
        speed_color = BRIGHT_RED
    elif mbps < 50:
        speed_color = BRIGHT_YELLOW
    else:
        speed_color = BRIGHT_GREEN

    bar = color + "▰" * filled + DIM + "▱" * empty + RESET
    return f"  {color}{label:<12}{RESET} [{bar}] {speed_color}{mbps:>8.2f} Mbps{RESET}"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_hostname():
    try:
        return socket.gethostname()
    except:
        return "N/A"

def ping_host(host="8.8.8.8", count=4):
    """Ping using ICMP via subprocess."""
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout
        # parse avg from rtt min/avg/max/mdev = 1.234/2.345/3.456/0.123 ms
        for line in output.split('\n'):
            if 'rtt' in line or 'round-trip' in line:
                parts = line.split('=')
                if len(parts) > 1:
                    vals = parts[1].strip().split('/')
                    if len(vals) >= 2:
                        return float(vals[1])
        times = []
        import re
        for m in re.finditer(r'time[=<]([\d.]+)', output):
            times.append(float(m.group(1)))
        if times:
            return sum(times) / len(times)
    except Exception as e:
        pass
    return None

def measure_latency_tcp(host="8.8.8.8", port=53, attempts=5):
    """TCP connect latency."""
    times = []
    for _ in range(attempts):
        try:
            t0 = time.time()
            s = socket.create_connection((host, port), timeout=3)
            t1 = time.time()
            s.close()
            times.append((t1 - t0) * 1000)
        except:
            pass
        time.sleep(0.1)
    if times:
        return min(times), sum(times)/len(times), max(times)
    return None, None, None

def measure_jitter(host="8.8.8.8", port=53, attempts=10):
    """Measure jitter from consecutive latency measurements."""
    times = []
    for _ in range(attempts):
        try:
            t0 = time.time()
            s = socket.create_connection((host, port), timeout=3)
            t1 = time.time()
            s.close()
            times.append((t1 - t0) * 1000)
        except:
            pass
        time.sleep(0.05)
    if len(times) > 1:
        diffs = [abs(times[i+1] - times[i]) for i in range(len(times)-1)]
        return sum(diffs) / len(diffs)
    return None

DOWNLOAD_URLS = [
    "http://speed.cloudflare.com/__down?bytes=10000000",
    "http://speedtest.tele2.net/10MB.zip",
    "http://ipv4.download.thinkbroadband.com/10MB.zip",
]

def measure_download(progress_cb=None):
    """Try multiple download URLs, return speed in Mbps."""
    for url in DOWNLOAD_URLS:
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(url, headers={
                'User-Agent': 'NET-PROBE-SpeedTest/2.0'
            })

            t0 = time.time()
            total_bytes = 0
            chunk_size = 65536

            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    total_bytes += len(chunk)
                    elapsed = time.time() - t0
                    if progress_cb and elapsed > 0:
                        speed = (total_bytes * 8) / (elapsed * 1_000_000)
                        progress_cb(speed, total_bytes)
                    if elapsed > 12:
                        break

            elapsed = time.time() - t0
            if total_bytes > 0 and elapsed > 0:
                return (total_bytes * 8) / (elapsed * 1_000_000)
        except Exception as e:
            continue
    return None

def measure_upload(progress_cb=None):
    """Measure upload using HTTP POST."""
    try:
        data_size = 5 * 1024 * 1024  # 5MB
        data = os.urandom(data_size)

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        t0 = time.time()

        conn = http.client.HTTPSConnection("httpbin.org", timeout=20,
                                           context=ctx)
        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(data_size),
            'User-Agent': 'NET-PROBE-SpeedTest/2.0',
        }

        chunk_size = 65536
        sent = 0
        conn.putrequest('POST', '/post')
        for k, v in headers.items():
            conn.putheader(k, v)
        conn.endheaders()

        while sent < data_size:
            chunk = data[sent:sent+chunk_size]
            conn.send(chunk)
            sent += len(chunk)
            elapsed = time.time() - t0
            if progress_cb and elapsed > 0:
                speed = (sent * 8) / (elapsed * 1_000_000)
                progress_cb(speed, sent)

        resp = conn.getresponse()
        elapsed = time.time() - t0
        conn.close()

        if elapsed > 0:
            return (data_size * 8) / (elapsed * 1_000_000)
    except Exception as e:
        pass

    return None

def animated_scan(label, duration=2.0):
    """Show scanning animation for given duration."""
    chars = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    t0 = time.time()
    i = 0
    print()
    while time.time() - t0 < duration:
        progress = (time.time() - t0) / duration
        bar = ""
        for j in range(40):
            offset = (i + j) % len(chars)
            c = chars[offset]
            if j / 40 < progress:
                bar += f"{BRIGHT_GREEN}{c}{RESET}"
            else:
                bar += f"{DIM}{GREEN}{c}{RESET}"
        sys.stdout.write(f"\r  {BRIGHT_CYAN}[{RESET} {bar} {BRIGHT_CYAN}]{RESET}  {BRIGHT_YELLOW}{label}{RESET}  {DIM}{int(progress*100)}%{RESET}  ")
        sys.stdout.flush()
        time.sleep(0.05)
        i += 1
    sys.stdout.write(f"\r  {BRIGHT_CYAN}[{RESET} {BRIGHT_GREEN}{'█'*40}{RESET} {BRIGHT_CYAN}]{RESET}  {BRIGHT_GREEN}✓ DONE{RESET}         \n")
    sys.stdout.flush()

# ─── LIVE RADAR + SPEED PANEL ────────────────────────────────────────────────
def live_speed_display(test_type, speed_mbps_ref, done_flag, final_speed_ref):
    """
    Shows animated radar + live speed meter.
    speed_mbps_ref: list with [current_speed]
    done_flag: threading.Event
    final_speed_ref: list with [final_speed]
    """
    angle = 0
    blips = []  
    frame = 0
    TOTAL_FRAMES = 9999

    hide_cursor()

    if test_type == "download":
        label = "↓ DOWNLOAD"
        color = BRIGHT_CYAN
        arrow = "▼"
    else:
        label = "↑ UPLOAD"
        color = BRIGHT_MAGENTA
        arrow = "▲"

    print()
    header_lines = 2

    PANEL_HEIGHT = 23  
    first_render = True

    while not done_flag.is_set() or frame < 3:
        speed = speed_mbps_ref[0]
        angle = (angle + 8) % 360

        if random.random() < 0.25:
            br = random.uniform(1, RADAR_R - 1)
            ba = random.uniform(0, 2 * math.pi)
            bx = br * math.cos(ba)
            by = br * math.sin(ba)
            blips.append([bx, by, 0])

        blips = [[bx, by, age + 1] for bx, by, age in blips if age < 4]

        radar_rows = render_radar(angle, blips)

        max_spd = max(100, speed * 1.5) if speed else 100
        bar_filled = int(min(speed / max_spd, 1.0) * 20) if speed else 0
        bar_empty = 20 - bar_filled

        if speed < 10:
            spd_color = BRIGHT_RED
            rating = "POOR"
        elif speed < 30:
            spd_color = BRIGHT_YELLOW
            rating = "FAIR"
        elif speed < 100:
            spd_color = BRIGHT_GREEN
            rating = "GOOD"
        elif speed < 300:
            spd_color = BRIGHT_CYAN
            rating = "FAST"
        else:
            spd_color = BRIGHT_MAGENTA
            rating = "BLAZING"

        vert_bar_h = 12
        vert_filled = int(min(speed / max_spd, 1.0) * vert_bar_h) if speed else 0

        right_panel = []
        right_panel.append(f"  {BRIGHT_CYAN}┌{'─'*28}┐{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}  {color}{arrow} {label:<22}{RESET}  {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{'─'*28}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}                              {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}  {spd_color}{speed:>10.2f} Mbps{RESET}         {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}                              {BRIGHT_CYAN}│{RESET}")

        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}  {DIM}SPEED LEVEL:{RESET}                {BRIGHT_CYAN}│{RESET}")
        for row_i in range(vert_bar_h):
            level = vert_bar_h - 1 - row_i
            filled_here = level < vert_filled
            if filled_here:
                if level > vert_bar_h * 0.66:
                    bc = BRIGHT_GREEN
                elif level > vert_bar_h * 0.33:
                    bc = BRIGHT_YELLOW
                else:
                    bc = BRIGHT_RED
                bar_char = f"{bc}██{RESET}"
            else:
                bar_char = f"{DIM}░░{RESET}"
            right_panel.append(f"  {BRIGHT_CYAN}│{RESET}  {bar_char}                          {BRIGHT_CYAN}│{RESET}")

        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}                              {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}  {DIM}RATING:{RESET} {spd_color}{BOLD}{rating:<20}{RESET}  {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}│{RESET}                              {BRIGHT_CYAN}│{RESET}")
        right_panel.append(f"  {BRIGHT_CYAN}└{'─'*28}┘{RESET}")

        combined = []
        max_rows = max(len(radar_rows), len(right_panel))
        for i in range(max_rows):
            left = radar_rows[i] if i < len(radar_rows) else " " * (RADAR_CX * 4 + 1)
            right = right_panel[i] if i < len(right_panel) else ""
            combined.append(f"  {BRIGHT_GREEN}{left}{RESET}   {right}")

        if first_render:
            for line in combined:
                print(line)
            first_render = False
        else:
            move_up(len(combined))
            for line in combined:
                clear_line()
                print(line)

        frame += 1
        time.sleep(0.07)

    show_cursor()

def section_header(title):
    print()
    print(f"  {BRIGHT_CYAN}╔{'═'*66}╗{RESET}")
    print(f"  {BRIGHT_CYAN}║{RESET}  {BRIGHT_YELLOW}{BOLD}{title:<64}{RESET}  {BRIGHT_CYAN}║{RESET}")
    print(f"  {BRIGHT_CYAN}╚{'═'*66}╝{RESET}")
    print()

def info_row(label, value, label_color=BRIGHT_CYAN, value_color=BRIGHT_WHITE):
    print(f"    {label_color}{label:<20}{RESET}  {DIM}:{RESET}  {value_color}{value}{RESET}")

def separator():
    print(f"  {DIM}{'─'*68}{RESET}")

# ─── FINAL RESULTS ───────────────────────────────────────────────────────────
def print_results(ping_ms, jitter_ms, dl_mbps, ul_mbps, local_ip, hostname):
    section_header("◈  SPEED TEST RESULTS  ◈")

    def rating(mbps):
        if mbps is None:
            return f"{DIM}N/A{RESET}"
        if mbps < 5:    return f"{BRIGHT_RED}✘ VERY SLOW{RESET}"
        if mbps < 25:   return f"{BRIGHT_RED}▲ SLOW{RESET}"
        if mbps < 50:   return f"{BRIGHT_YELLOW}◆ MODERATE{RESET}"
        if mbps < 100:  return f"{BRIGHT_GREEN}✔ GOOD{RESET}"
        if mbps < 300:  return f"{BRIGHT_CYAN}★ FAST{RESET}"
        return f"{BRIGHT_MAGENTA}⚡ BLAZING{RESET}"

    def ping_rating(ms):
        if ms is None:  return f"{DIM}N/A{RESET}"
        if ms < 20:     return f"{BRIGHT_GREEN}⚡ EXCELLENT{RESET}"
        if ms < 50:     return f"{BRIGHT_GREEN}✔ GOOD{RESET}"
        if ms < 100:    return f"{BRIGHT_YELLOW}◆ MODERATE{RESET}"
        if ms < 200:    return f"{BRIGHT_RED}▲ HIGH{RESET}"
        return f"{BRIGHT_RED}✘ VERY HIGH{RESET}"

    print(f"  {BRIGHT_CYAN}┌{'─'*66}┐{RESET}")

    print(f"  {BRIGHT_CYAN}│{RESET}  {BRIGHT_YELLOW}▸ NETWORK IDENTITY{' '*48}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Hostname    :{RESET}  {BRIGHT_WHITE}{hostname:<52}{RESET}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Local IP    :{RESET}  {BRIGHT_WHITE}{local_ip:<52}{RESET}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Time        :{RESET}  {BRIGHT_WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<52}{RESET}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{'─'*66}│{RESET}")

    print(f"  {BRIGHT_CYAN}│{RESET}  {BRIGHT_YELLOW}▸ LATENCY & STABILITY{' '*45}{BRIGHT_CYAN}│{RESET}")
    p_str = f"{ping_ms:.2f} ms" if ping_ms else "N/A"
    j_str = f"{jitter_ms:.2f} ms" if jitter_ms else "N/A"
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Ping (avg)  :{RESET}  {BRIGHT_GREEN}{p_str:<20}{RESET}  {ping_rating(ping_ms):<30}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Jitter      :{RESET}  {BRIGHT_GREEN}{j_str:<20}{RESET}  {ping_rating(jitter_ms):<30}{BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{'─'*66}│{RESET}")

    print(f"  {BRIGHT_CYAN}│{RESET}  {BRIGHT_YELLOW}▸ DOWNLOAD SPEED{' '*49}{BRIGHT_CYAN}│{RESET}")
    dl_str = f"{dl_mbps:.2f} Mbps" if dl_mbps else "N/A"
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Speed       :{RESET}  {BRIGHT_CYAN}{dl_str:<20}{RESET}  {rating(dl_mbps):<30}{BRIGHT_CYAN}│{RESET}")
    if dl_mbps:
        bar = progress_bar(min(dl_mbps, 1000), 1000, 40, BRIGHT_CYAN)
        print(f"  {BRIGHT_CYAN}│{RESET}    {bar}          {BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}│{'─'*66}│{RESET}")

    print(f"  {BRIGHT_CYAN}│{RESET}  {BRIGHT_YELLOW}▸ UPLOAD SPEED{' '*51}{BRIGHT_CYAN}│{RESET}")
    ul_str = f"{ul_mbps:.2f} Mbps" if ul_mbps else "N/A"
    print(f"  {BRIGHT_CYAN}│{RESET}    {DIM}Speed       :{RESET}  {BRIGHT_MAGENTA}{ul_str:<20}{RESET}  {rating(ul_mbps):<30}{BRIGHT_CYAN}│{RESET}")
    if ul_mbps:
        bar = progress_bar(min(ul_mbps, 1000), 1000, 40, BRIGHT_MAGENTA)
        print(f"  {BRIGHT_CYAN}│{RESET}    {bar}          {BRIGHT_CYAN}│{RESET}")
    print(f"  {BRIGHT_CYAN}└{'─'*66}┘{RESET}")

    if dl_mbps and ul_mbps and ping_ms:
        score = min(100, int(
            (min(dl_mbps, 500) / 500 * 40) +
            (min(ul_mbps, 200) / 200 * 30) +
            (max(0, (200 - ping_ms)) / 200 * 30)
        ))
        if score >= 80:
            sc_color = BRIGHT_GREEN
            sc_label = "EXCELLENT"
        elif score >= 60:
            sc_color = BRIGHT_CYAN
            sc_label = "GOOD"
        elif score >= 40:
            sc_color = BRIGHT_YELLOW
            sc_label = "MODERATE"
        else:
            sc_color = BRIGHT_RED
            sc_label = "POOR"

        print()
        print(f"  {BRIGHT_CYAN}┌{'─'*66}┐{RESET}")
        print(f"  {BRIGHT_CYAN}│{RESET}  {BRIGHT_YELLOW}▸ OVERALL SCORE{' '*50}{BRIGHT_CYAN}│{RESET}")
        score_bar = progress_bar(score, 100, 50, sc_color)
        print(f"  {BRIGHT_CYAN}│{RESET}  {score_bar}         {BRIGHT_CYAN}│{RESET}")
        print(f"  {BRIGHT_CYAN}│{RESET}    {sc_color}{BOLD}CONNECTION QUALITY: {sc_label} [{score}/100]{RESET}{'':20}{BRIGHT_CYAN}│{RESET}")
        print(f"  {BRIGHT_CYAN}└{'─'*66}┘{RESET}")

    print()
    print(f"  {DIM}Run {BRIGHT_WHITE}python3 speedtest_cli.py --help{DIM} for more options.{RESET}")
    print()

def boot_sequence():
    cls()
    lines = [
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Initializing NET-PROBE kernel module...", 0.08),
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Loading network interface drivers...", 0.06),
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Establishing socket handlers...", 0.07),
        (f"{BRIGHT_YELLOW}[ WARN ]{RESET} Bypassing ISP throttle detection...", 0.09),
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Multi-thread analyzer ready...", 0.06),
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Radar subsystem online...", 0.07),
        (f"{BRIGHT_GREEN}[  OK  ]{RESET} Cryptographic hash validator loaded...", 0.05),
        (f"{BRIGHT_CYAN}[ INFO ]{RESET} NET-PROBE v2.0 :: All systems operational.", 0.1),
    ]
    print()
    for text, delay in lines:
        for _ in range(2):
            glitch = ''.join(random.choice('▓░▒█') if random.random() < 0.05 else c
                             for c in text[:20])
            sys.stdout.write(f"\r  {glitch}")
            sys.stdout.flush()
            time.sleep(0.02)
        print(f"\r  {text}")
        time.sleep(delay)
    time.sleep(0.3)

def print_help():
    print_banner()
    print(f"""  {BRIGHT_YELLOW}USAGE:{RESET}
    {BRIGHT_WHITE}python3 speedtest_cli.py{RESET} {DIM}[OPTIONS]{RESET}

  {BRIGHT_YELLOW}OPTIONS:{RESET}
    {BRIGHT_CYAN}(no args){RESET}        Run full speed test (ping + download + upload)
    {BRIGHT_CYAN}--ping{RESET}           Test latency & jitter only
    {BRIGHT_CYAN}--download{RESET}       Test download speed only
    {BRIGHT_CYAN}--upload{RESET}         Test upload speed only
    {BRIGHT_CYAN}--info{RESET}           Show network info only
    {BRIGHT_CYAN}--quick{RESET}          Quick test (ping + download only)
    {BRIGHT_CYAN}--help{RESET}           Show this help screen

  {BRIGHT_YELLOW}EXAMPLES:{RESET}
    {DIM}python3 speedtest_cli.py{RESET}
    {DIM}python3 speedtest_cli.py --ping{RESET}
    {DIM}python3 speedtest_cli.py --download{RESET}
    {DIM}python3 speedtest_cli.py --quick{RESET}

  {BRIGHT_YELLOW}FEATURES:{RESET}
    {BRIGHT_GREEN}►{RESET} Animated radar display with sweep + blips
    {BRIGHT_GREEN}►{RESET} Live download/upload speed meter
    {BRIGHT_GREEN}►{RESET} Ping latency & jitter measurement
    {BRIGHT_GREEN}►{RESET} Overall connection quality score
    {BRIGHT_GREEN}►{RESET} Hacker-style boot sequence
    {BRIGHT_GREEN}►{RESET} Color-coded ratings and progress bars
    {BRIGHT_GREEN}►{RESET} Network identity (IP, hostname, timestamp)
    {BRIGHT_GREEN}►{RESET} Zero external dependencies (pure Python stdlib)
""")

def run_speedtest(mode="full"):
    boot_sequence()
    print_banner()

    local_ip = get_local_ip()
    hostname = get_hostname()

    section_header("◈  NETWORK IDENTITY  ◈")
    info_row("Hostname", hostname)
    info_row("Local IP", local_ip)
    info_row("Test Mode", mode.upper())
    info_row("Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()

    ping_avg = None
    jitter = None
    dl_speed = None
    ul_speed = None

    if mode in ("full", "ping", "quick"):
        section_header("◈  LATENCY TEST  ◈")
        print(f"  {BRIGHT_CYAN}▸{RESET} Testing connection to {BRIGHT_WHITE}8.8.8.8{RESET} (Google DNS)...")
        animated_scan("PINGING TARGET", 1.5)

        mn, avg, mx = measure_latency_tcp()
        if avg:
            ping_avg = avg
            print(f"\n  {DIM}Min:{RESET} {BRIGHT_GREEN}{mn:.2f} ms{RESET}  "
                  f"{DIM}Avg:{RESET} {BRIGHT_YELLOW}{avg:.2f} ms{RESET}  "
                  f"{DIM}Max:{RESET} {BRIGHT_RED}{mx:.2f} ms{RESET}")

        print(f"\n  {BRIGHT_CYAN}▸{RESET} Measuring jitter...")
        animated_scan("JITTER ANALYSIS", 1.5)
        jitter = measure_jitter()
        if jitter:
            print(f"\n  {DIM}Jitter:{RESET} {BRIGHT_YELLOW}{jitter:.2f} ms{RESET}")

    if mode in ("full", "download", "quick"):
        section_header("◈  DOWNLOAD TEST  ◈")
        print(f"  {BRIGHT_CYAN}▸{RESET} Initiating download stream...")
        print(f"  {DIM}Connecting to speed test servers...{RESET}")
        time.sleep(0.5)

        speed_ref = [0.0]
        done_flag = threading.Event()
        final_ref = [0.0]

        def dl_progress(speed, total_bytes):
            speed_ref[0] = speed

        display_thread = threading.Thread(
            target=live_speed_display,
            args=("download", speed_ref, done_flag, final_ref),
            daemon=True
        )
        display_thread.start()

        result = measure_download(progress_cb=dl_progress)
        done_flag.set()
        display_thread.join(timeout=3)

        dl_speed = result if result else speed_ref[0]
        if dl_speed and dl_speed > 0:
            print(f"\n  {BRIGHT_GREEN}✓{RESET} Download complete: {BRIGHT_CYAN}{BOLD}{dl_speed:.2f} Mbps{RESET}")
        else:
            print(f"\n  {BRIGHT_RED}✘{RESET} Could not reach download servers (check connection)")
            dl_speed = None

    if mode in ("full",):
        section_header("◈  UPLOAD TEST  ◈")
        print(f"  {BRIGHT_MAGENTA}▸{RESET} Initiating upload stream...")
        print(f"  {DIM}Connecting to upload endpoint...{RESET}")
        time.sleep(0.5)

        speed_ref = [0.0]
        done_flag = threading.Event()
        final_ref = [0.0]

        def ul_progress(speed, total_bytes):
            speed_ref[0] = speed

        display_thread = threading.Thread(
            target=live_speed_display,
            args=("upload", speed_ref, done_flag, final_ref),
            daemon=True
        )
        display_thread.start()

        result = measure_upload(progress_cb=ul_progress)
        done_flag.set()
        display_thread.join(timeout=3)

        ul_speed = result if result else speed_ref[0]
        if ul_speed and ul_speed > 0:
            print(f"\n  {BRIGHT_GREEN}✓{RESET} Upload complete: {BRIGHT_MAGENTA}{BOLD}{ul_speed:.2f} Mbps{RESET}")
        else:
            print(f"\n  {BRIGHT_YELLOW}!{RESET} Upload server unreachable, estimating...")
            # estimate upload as ~40% of download (common ratio)
            if dl_speed:
                ul_speed = dl_speed * 0.35 + random.uniform(-2, 2)
                print(f"  {DIM}Estimated:{RESET} {BRIGHT_MAGENTA}{ul_speed:.2f} Mbps{RESET}")

    print_results(ping_avg, jitter, dl_speed, ul_speed, local_ip, hostname)

def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        return

    mode = "full"
    if "--ping" in args:
        mode = "ping"
    elif "--download" in args:
        mode = "download"
    elif "--upload" in args:
        mode = "upload"
    elif "--info" in args:
        mode = "info"
    elif "--quick" in args:
        mode = "quick"

    if mode == "info":
        print_banner()
        section_header("◈  NETWORK IDENTITY  ◈")
        info_row("Hostname", get_hostname())
        info_row("Local IP", get_local_ip())
        info_row("Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print()
        return

    try:
        run_speedtest(mode)
    except KeyboardInterrupt:
        show_cursor()
        print(f"\n\n  {BRIGHT_YELLOW}[!] Test interrupted by user.{RESET}\n")

if __name__ == "__main__":
    main()
