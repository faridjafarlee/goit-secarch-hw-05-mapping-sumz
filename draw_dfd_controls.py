#!/usr/bin/env python3
"""ДЗ5: DFD СУМЗ з ДЗ2 + мітки контролів NIST SP 800-53 (dfd_controls.png). Базова нотація DFD з уроку:
прямокутник = зовнішня сутність, овал = процес, дві лінії = сховище, стрілка = потік, червоний пунктир = trust boundary."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 2000, 1330
img = Image.new('RGB', (W, H), 'white')
d = ImageDraw.Draw(img)
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
f = lambda s: ImageFont.truetype(FONT, s)
F_T, F_B, F_S, F_Z = f(30), f(21), f(17), f(19)
INK, BLUE, GREEN, ORANGE, RED, GREY = '#1f2937', '#1d4ed8', '#047857', '#b45309', '#dc2626', '#6b7280'

def text_c(box, txt, font, fill=INK):
    x0, y0, x1, y1 = box
    lines = txt.split('\n')
    hs = [d.textbbox((0, 0), l, font=font) for l in lines]
    th = sum(b[3] - b[1] for b in hs) + 6 * (len(lines) - 1)
    y = (y0 + y1 - th) / 2
    for l, b in zip(lines, hs):
        w = b[2] - b[0]
        d.text(((x0 + x1 - w) / 2, y - b[1]), l, font=font, fill=fill)
        y += b[3] - b[1] + 6

def entity(box, txt):          # зовнішня сутність
    d.rectangle(box, outline=BLUE, width=4, fill='#eff6ff'); text_c(box, txt, F_B)

def process(box, txt):         # процес
    d.ellipse(box, outline=GREEN, width=4, fill='#ecfdf5'); text_c(box, txt, F_B)

def store(box, txt):           # сховище даних
    x0, y0, x1, y1 = box
    d.rectangle(box, fill='#fffbeb')
    d.line([(x0, y0), (x1, y0)], fill=ORANGE, width=4); d.line([(x0, y1), (x1, y1)], fill=ORANGE, width=4)
    d.line([(x0, y0), (x0, y1)], fill=ORANGE, width=4)
    text_c(box, txt, F_B)

def dashed_rect(box, color=RED, dash=16, gap=10, width=3):
    x0, y0, x1, y1 = box
    for (a, b) in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        L = math.dist(a, b); n = int(L // (dash + gap)) + 1
        for i in range(n):
            s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
            d.line([(a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s), (a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e)], fill=color, width=width)

def arrow(p, q, label=None, color=INK, lpos=0.5, loff=(0, -24)):
    d.line([p, q], fill=color, width=3)
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for s in (+1, -1):
        d.line([q, (q[0] - 18 * math.cos(ang + s * 0.4), q[1] - 18 * math.sin(ang + s * 0.4))], fill=color, width=3)
    if label:
        mx, my = p[0] + (q[0] - p[0]) * lpos + loff[0], p[1] + (q[1] - p[1]) * lpos + loff[1]
        b = d.textbbox((0, 0), label, font=F_S)
        d.rectangle((mx - 4, my - 2, mx + b[2] - b[0] + 4, my + b[3] - b[1] + 6), fill='white')
        d.text((mx, my), label, font=F_S, fill=color)

d.text((40, 22), 'DFD СУМЗ «MedRecordsManager» з розміщенням контролів NIST SP 800-53 (ДЗ5)', font=F_T, fill=INK)

def poly(points, label=None, color=INK, seg=0, loff=(8, -26)):
    for a, b in zip(points, points[1:-1]):
        d.line([a, b], fill=color, width=3)
    arrow(points[-2], points[-1], None, color=color)
    if label:
        a, b = points[seg], points[seg + 1]
        mx, my = (a[0] + b[0]) / 2 + loff[0], (a[1] + b[1]) / 2 + loff[1]
        bb = d.textbbox((0, 0), label, font=F_S)
        d.rectangle((mx - 4, my - 2, mx + bb[2] - bb[0] + 4, my + bb[3] - bb[1] + 6), fill='white')
        d.text((mx, my), label, font=F_S, fill=color)

# Зони довіри (trust boundaries)
Z = {'net': (25, 90, 545, 1130), 'dmz': (565, 90, 1100, 800), 'adm': (565, 840, 1100, 1130),
     'data': (1140, 90, 1500, 1130), 'ext': (1540, 90, 1975, 1130)}
for k, box in Z.items():
    dashed_rect(box)
d.text((40, 98), 'TB1 · Інтернет / пристрої користувачів', font=F_Z, fill=RED)
d.text((580, 98), 'TB2 · DMZ: застосункова зона', font=F_Z, fill=RED)
d.text((580, 848), 'TB5 · Адмін-зона (лише через VPN)', font=F_Z, fill=RED)
d.text((1155, 98), 'TB3 · Внутрішня зона даних', font=F_Z, fill=RED)
d.text((1555, 98), 'TB4 · Зовнішні інтеграції', font=F_Z, fill=RED)

# Елементи
P = (45, 170, 225, 250); DR = (45, 500, 225, 580); AD = (45, 930, 225, 1010)
entity(P, 'Пацієнт'); entity(DR, 'Лікар'); entity(AD, 'Адміністратор')
LAB = (1570, 140, 1945, 225); SMS = (1570, 260, 1945, 345); SMTP = (1570, 800, 1945, 885)
entity(LAB, 'Лабораторія (LIS),\nHL7 FHIR'); entity(SMS, 'SMS / OTP-провайдер\n(MFA)'); entity(SMTP, 'E-mail-провайдер\n(SMTP-релей)')
CL = (270, 300, 520, 450); API = (640, 240, 1060, 490); EXP = (650, 580, 1050, 760); ADM = (650, 920, 1030, 1060)
process(CL, 'Веб-застосунок /\nмобільний\nзастосунок'); process(API, 'API Gateway + Backend API\n(автентифікація, авторизація\nRBAC, бізнес-логіка)')
process(EXP, 'Сервіс експорту\n(PDF, e-mail, посилання)'); process(ADM, 'Адмінпанель\n(користувачі, ролі)')
DB = (1170, 400, 1480, 510); FS = (1170, 620, 1480, 720); LOG = (1170, 960, 1480, 1060)
store(DB, 'D1 · БД медичних записів\n(історії хвороб, аналізи,\nконсультації)'); store(FS, 'D2 · Файлове сховище\n(PDF, вкладення)'); store(LOG, 'D3 · Журнал аудиту\n(append-only)')

# Потоки
poly([(225, 210), (395, 210), (395, 300)], 'F1 вхід, запити', seg=0, loff=(-10, -30))
poly([(225, 540), (395, 540), (395, 450)], 'F1 записи, консультації', seg=0, loff=(-60, 8))
poly([(520, 350), (640, 350)], 'F2 HTTPS+JWT', seg=0, loff=(-60, -32))
poly([(640, 405), (520, 405)], 'F3 відповідь', seg=0, loff=(-55, 8))
poly([(1060, 440), (1170, 440)], 'F4 SQL', seg=0, loff=(-40, -30))
poly([(1170, 480), (1040, 480)], None)
poly([(1570, 182), (850, 182), (850, 240)], 'F8 результати аналізів (webhook, FHIR)', seg=0, loff=(-80, -30))
poly([(1030, 300), (1570, 300)], 'F9 OTP-запит', seg=0, loff=(120, -30))
poly([(850, 490), (850, 580)], 'F5 запит експорту', seg=0, loff=(12, -12))
poly([(1050, 670), (1170, 670)], 'F6 PDF', seg=0, loff=(-40, -30))
poly([(990, 740), (1120, 842), (1570, 842)], 'F7 лист / посилання', seg=1, loff=(60, -30))
poly([(1010, 470), (1100, 560), (1170, 640)], 'F13 підписаний URL', color=GREY, seg=0, loff=(22, 22))
poly([(225, 970), (650, 970)], 'F10 VPN + MFA', seg=0, loff=(-40, -30))
poly([(660, 960), (585, 960), (585, 455), (700, 455)], 'F11 ролі', seg=1, loff=(-58, 60))
poly([(1055, 395), (1120, 395), (1120, 1000), (1170, 1000)], None, color=GREY)
d.text((1084, 900), 'F12', font=F_S, fill=GREY)
poly([(1045, 715), (1120, 715)], None, color=GREY)
poly([(1030, 1000), (1120, 1000)], None, color=GREY)


# Мітки контролів (ДЗ5): кожен рядок задано як (загроза, текст); колір = загроза
F_TAG = f(16)
TC = {'S': '#1d4ed8', 'T': '#c2410c', 'I': '#7c3aed', '*': '#374151'}
def tag(x, y, rows, w=None):
    lines = [(TC[k], (k + ': ' if k != '*' else '') + t) for k, t in rows]
    bb = [d.textbbox((0, 0), t, font=F_TAG) for _, t in lines]
    lw = max(b[2] - b[0] for b in bb); lh = 22
    w = w or lw + 20; h = lh * len(lines) + 12
    d.rounded_rectangle((x, y, x + w, y + h), radius=8, fill='#f9fafb', outline='#374151', width=2)
    for i, (c, t) in enumerate(lines):
        d.text((x + 10, y + 6 + i * lh), t, font=F_TAG, fill=c)
    return (x, y, x + w, y + h)

def leader(p, q):
    L = math.dist(p, q); n = int(L // 12)
    for i in range(0, n, 2):
        a = (p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n)
        b = (p[0] + (q[0] - p[0]) * (i + 1) / n, p[1] + (q[1] - p[1]) * (i + 1) / n)
        d.line([a, b], fill='#374151', width=2)

# застосунок (TB1): мітка без виносної лінії, щоб не перетинати F1
tag(40, 650, [('S', 'Застосунок: IA-2, MFA у формі входу'), ('S', '(TOTP/push, згодом FIDO2 для лікарів)'), ('S', 'SC-23: токен лише в httpOnly-cookie')])

# межа TB1→TB2 / API Gateway
tag(575, 128, [('S', 'Gateway: AC-7 · SC-23 · AC-12'), ('I', 'AC-23: квоти, UUID')])
# Backend API
tag(598, 498, [('T', 'API: AC-3 · AC-6 · SI-10'), ('I', 'AC-3 ABAC · AC-6 · SA-11')], w=240)
# D1
tag(1160, 318, [('T', 'D1: SI-7 версії + хеш'), ('T', 'AC-6: RLS, без UPDATE історії')])
# D2
tag(1160, 735, [('I', 'D2: UUID-посилання ≤15 хв')])
# D3
tag(1165, 868, [('*', 'D3: AU-9 WORM · AU-12'), ('*', 'SI-4 / AU-6 → SIEM')])
# вебхук лабораторії F8 (TB4)
tag(1565, 380, [('T', 'F8: SC-8(1) TLS/mTLS'), ('T', 'IA-9: HMAC-підпис вебхука'), ('T', 'SI-10: FHIR-валідація')])
# адмінпанель (TB5)
tag(598, 1068, [('S', 'Адмінпанель: IA-2(1) FIDO2'), ('*', 'AC-6: без медданих · AU-9 лише читання')])

# Легенда
ly = 1195
entity((40, ly, 170, ly + 50), 'Сутність'); process((200, ly - 5, 360, ly + 55), 'Процес'); store((390, ly, 560, ly + 50), 'Сховище')
arrow((600, ly + 25), (720, ly + 25)); d.text((730, ly + 12), 'потік даних', font=F_S, fill=INK)
dashed_rect((880, ly + 5, 1000, ly + 45)); d.text((1010, ly + 12), 'межа довіри (trust boundary)', font=F_S, fill=RED)
d.rounded_rectangle((40, ly + 62, 90, ly + 88), radius=6, fill='#f9fafb', outline='#374151', width=2)
d.text((100, ly + 64), 'мітка = контролі NIST SP 800-53 у цьому місці; колір рядка = загроза:', font=F_S, fill=INK)
for i, (k, c) in enumerate([('S: загроза 1, сесія лікаря', '#1d4ed8'), ('T: загроза 2, зміна аналізу', '#c2410c'), ('I: загроза 3, IDOR', '#7c3aed'), ('сірий: спільні', '#374151')]):
    d.text((740 + i * 330, ly + 64), k, font=F_S, fill=c)
img.save('dfd_controls.png'); print('saved', img.size)
