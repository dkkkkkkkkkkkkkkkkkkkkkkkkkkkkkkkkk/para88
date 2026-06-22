import os
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "kozmos55_gizli_anahtar_9988"

# ============================================================
# VERİTABANI
# ============================================================
def init_db():
    conn = sqlite3.connect('iptv.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT UNIQUE, 
                       password TEXT, 
                       expiry_date TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS channels 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       url TEXT, 
                       category TEXT,
                       logo TEXT)''')

    # Admin hesabı
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, expiry_date) VALUES ('admin', 'admin123', 'Sınırsız')")

    # ----- KANALLAR -----
    cursor.execute("SELECT COUNT(*) FROM channels")
    if cursor.fetchone()[0] == 0:
        kanallar = [
            ("Vostok TV [KOZMOS55]", "http://911play.ru:3456/live/VostokSite/cdnVostaoc911tv123456/489.m3u8", "Rusiya", "https://i.postimg.cc/NfmDy569/2018.png"),
            ("Live TV RU [KOZMOS55]", "https://tv.mobyservice.ru/livetv/index.m3u8", "Rusiya", "https://i.postimg.cc/DwZXkgsV/In-Shot-20260105-102529648.png"),
            ("Horror Cinema [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-horror.m3u8", "Films", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Hind Filmləri [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimof-hind-filmleri.m3u8", "Films", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Retro Cinema [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-azeri-retro-filmle.m3u8", "Films", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Retro Cinema 2 [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-retro-filmler-2.m3u8", "Films", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("DigiNET Cinema [KOZMOS55]", "https://a8.radyotelekom.com.tr:3276/stream/play.m3u8", "Films", "https://i.postimg.cc/5N4mghBq/In-Shot-20260510-202245174.png"),
            ("STV Sinema [KOZMOS55]", "https://a8.radyotelekom.com.tr:3179/stream/play.m3u8", "Films", "https://i.postimg.cc/BbWfvvFG/IMG-20260405-094134-027.jpg"),
            ("CBC SPORT [KOZMOS55]", "http://erlyvideo.RUSIYA 2.az:80/cbcsporthd/mono.m3u8", "Sports", "https://i.postimg.cc/3w4FTNxx/CBC-Sport-TV-loqo.png"),
            ("CBC SPORT★ [KOZMOS55]", "http://176.65.146.189:8701/play/a09h", "Sports", "https://i.postimg.cc/3w4FTNxx/CBC-Sport-TV-loqo.png"),
            ("IDMAN TV [KOZMOS55]", "http://flussonic.izone.az:80/idmanaz/mono.m3u8", "Sports", "https://i.postimg.cc/7LfmZXmD/dman-TV-logo.png"),
            ("IDMAN TV★ [KOZMOS55]", "http://str.yodacdn.net/idmantele/index.m3u8", "Sports", "https://i.postimg.cc/7LfmZXmD/dman-TV-logo.png"),
            ("Qaydasız Döyüşlər [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-gaydasiz-doyusler.m3u8", "Sports", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Bu Seherde [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-bu-seherde.m3u8", "Türkiye", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Bu Seherde 2 [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-bu-seherde2.m3u8", "Türkiye", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Yeşilçam [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-yesilcam.m3u8", "Türkiye", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("Kemal Sunal [KOZMOS55]", "https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=ksunal.m3u8", "Türkiye", "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"),
            ("FLUX TV [KOZMOS55]", "https://a8.radyotelekom.com.tr:3232/stream/play.m3u8", "Türkiye", "https://i.postimg.cc/br7hSHP2/In-Shot-20260531-073742477.png"),
            ("İsmayıllı TV [KOZMOS55]", "https://a8.radyotelekom.com.tr:3973/hybrid/play.m3u8", "Türkiye", "https://i.postimg.cc/2jW1tzhV/In-Shot-20260426-173635086.png"),
            ("Kanal 12 [KOZMOS55]", "https://live.artidijitalmedya.com/artidijital_kanal12/kanal12/playlist.m3u8", "Türkiye", "https://i.postimg.cc/PqNdMwTt/In-Shot-20250502-204654847.png"),
            ("AZTV [KOZMOS55]", "http://flussonic.izone.az:80/aztv/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/sg126ZT1/a.png"),
            ("AZTV★ [KOZMOS55]", "http://str.yodacdn.net/azertv/index.m3u8", "Azərbaycan", "https://i.postimg.cc/sg126ZT1/a.png"),
            ("İCTİMAİ TV [KOZMOS55]", "http://flussonic.izone.az:80/ictimaitv/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/3wvx7Q5T/ITV-Azerbaijan-Logo.png"),
            ("İCTİMAİ TV★ [KOZMOS55]", "https://live.itv.az/itv.m3u8", "Azərbaycan", "https://i.postimg.cc/3wvx7Q5T/ITV-Azerbaijan-Logo.png"),
            ("MƏDƏNİYYƏT TV [KOZMOS55]", "http://flussonic.izone.az:80/medeniyyet/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/0Q12yXPJ/M-d-niyy-t-TV-loqo.png"),
            ("MƏDƏNİYYƏT TV★ [KOZMOS55]", "http://str.yodacdn.net/medeniyyettele/index.m3u8", "Azərbaycan", "https://i.postimg.cc/0Q12yXPJ/M-d-niyy-t-TV-loqo.png"),
            ("ATV [KOZMOS55]", "http://flussonic.izone.az:80/azadazerbaycan/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/T1YxKZSh/785cfca9083712aedfed84b91a0f00e8.png"),
            ("ATV★ [KOZMOS55]", "http://str.yodacdn.net/atv/index.m3u8", "Azərbaycan", "https://i.postimg.cc/T1YxKZSh/785cfca9083712aedfed84b91a0f00e8.png"),
            ("XƏZƏR TV [KOZMOS55]", "http://flussonic.izone.az:80/xezertv/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/bYFW0DSm/X-z-r-TV-2023.png"),
            ("XƏZƏR TV★ [KOZMOS55]", "https://raw.githubusercontent.com/UzunMuhalefet/streams/main/myvideo-az/xezer-tv.m3u8", "Azərbaycan", "https://i.postimg.cc/bYFW0DSm/X-z-r-TV-2023.png"),
            ("SPACE TV [KOZMOS55]", "http://flussonic.izone.az:80/spacetv/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/c1Qrztms/In-Shot-20251103-071346014.png"),
            ("SPACE TV★ [KOZMOS55]", "http://str.yodacdn.net/space/index.m3u8", "Azərbaycan", "https://i.postimg.cc/c1Qrztms/In-Shot-20251103-071346014.png"),
            ("ARB TV [KOZMOS55]", "http://flussonic.izone.az:80/arb/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/zfJxY8RL/ARB-Media-Qrup.png"),
            ("ARB TV★ [KOZMOS55]", "https://raw.githubusercontent.com/UzunMuhalefet/streams/main/myvideo-az/arb.m3u8", "Azərbaycan", "https://i.postimg.cc/zfJxY8RL/ARB-Media-Qrup.png"),
            ("ARB 24 [KOZMOS55]", "http://flussonic.izone.az:80/arb24/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/hjvMhssc/ARB-24.png"),
            ("ARB 24★ [KOZMOS55]", "http://str.yodacdn.net/arb24/index.m3u8", "Azərbaycan", "https://i.postimg.cc/hjvMhssc/ARB-24.png"),
            ("ARB GÜNƏŞ [KOZMOS55]", "http://flussonic.izone.az:80/arbgunesh/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/4nk1Lggx/ARB-Gunesh-Logo.png"),
            ("ARB GÜNƏŞ★ [KOZMOS55]", "https://raw.githubusercontent.com/UzunMuhalefet/streams/main/myvideo-az/arb-gunes.m3u8", "Azərbaycan", "https://i.postimg.cc/4nk1Lggx/ARB-Gunesh-Logo.png"),
            ("BAKU TV [KOZMOS55]", "https://raw.githubusercontent.com/UzunMuhalefet/streams/refs/heads/main/myvideo-az/baku-tv.m3u8", "Azərbaycan", "https://i.postimg.cc/pXfSw016/hd-logo.png"),
            ("BAKU TV★ [KOZMOS55]", "http://str.yodacdn.net/bakutv/index.m3u8", "Azərbaycan", "https://i.postimg.cc/pXfSw016/hd-logo.png"),
            ("REAL TV [KOZMOS55]", "http://flussonic.izone.az:80/realtv/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/KcNLCBD5/Real-TV-Azerbaijan-Logo.png"),
            ("REAL TV★ [KOZMOS55]", "http://str.yodacdn.net/real/index.m3u8", "Azərbaycan", "https://i.postimg.cc/KcNLCBD5/Real-TV-Azerbaijan-Logo.png"),
            ("DÜNYA TV [KOZMOS55]", "https://stream.ftv.az/live/dunyatv.m3u8", "Azərbaycan", "https://i.postimg.cc/7YG1Fbst/D-nya-TV-2019-h-h.png"),
            ("CBC [KOZMOS55]", "http://flussonic.izone.az:80/cbc/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/BbWhyD53/CBC-Azerbaijan-Logo.png"),
            ("CBC★ [KOZMOS55]", "http://str.yodacdn.net/cbc/index.m3u8", "Azərbaycan", "https://i.postimg.cc/BbWhyD53/CBC-Azerbaijan-Logo.png"),
            ("GÜNAZ TV [KOZMOS55]", "https://tv.gunaz.tv/hls/live.m3u8", "Azərbaycan", "https://i.postimg.cc/QCbpbW00/Gunaz-tv-svg.png"),
            ("QAFQAZ TV [KOZMOS55]", "http://str.yodacdn.net/qafkaz/index.m3u8", "Azərbaycan", "https://i.postimg.cc/SxR28nX0/Qafqaz-TV-2017-h-h.png"),
            ("NAXÇIVAN TV [KOZMOS55]", "http://str.yodacdn.net/ntv/tracks-v1a1/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/ZY355z4D/In-Shot-20251027-110042165.png"),
            ("APA TV [KOZMOS55]", "http://stream.apa.tv/apastream/index.m3u8", "Azərbaycan", "https://i.postimg.cc/ry97JfJr/In-Shot-20251027-110247292.png"),
            ("KANAL 35 [KOZMOS55]", "http://str.yodacdn.net/kanal35/tracks-v1a1/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/C5Cr0Zxt/Kanal-35-loqo.png"),
            ("KƏPƏZ TV [KOZMOS55]", "http://85.132.78.122:8050/hls/stream/index.m3u8", "Azərbaycan", "https://i.postimg.cc/HkgvYQ7P/K-p-z-TV-2019.png"),
            ("TV MUSAVAT [KOZMOS55]", "https://stream.musavat.tv/tv.m3u8", "Azərbaycan", "https://i.postimg.cc/pTCb4jcy/logo.png"),
            ("YENİÇAĞ TV [KOZMOS55]", "https://live.euromediacenter.com/yenicagtv/tracks-v1a1/mono.m3u8", "Azərbaycan", "https://i.postimg.cc/2yvLGLdS/In-Shot-20260602-122025256.png"),
        ]
        cursor.executemany("INSERT INTO channels (name, url, category, logo) VALUES (?, ?, ?, ?)", kanallar)
        conn.commit()

    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('iptv.db')
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# HTML ŞABLONLARI - KOZMOS55 TASARIMI
# ============================================================

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kozmos55 - IPTV</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #050508;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
            background-image:
                radial-gradient(ellipse at 30% 50%, rgba(0,255,102,0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(0,200,80,0.03) 0%, transparent 60%);
            position: relative;
            overflow: hidden;
        }
        body::before {
            content: 'KOZMOS55';
            position: fixed;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            font-size: 30rem;
            font-weight: 900;
            color: rgba(0,255,102,0.015);
            pointer-events: none;
            font-family: 'Orbitron', monospace;
            transform: rotate(-15deg);
            letter-spacing: 20px;
        }
        .login-card {
            background: rgba(8,8,14,0.96);
            border: 1px solid rgba(0,255,102,0.12);
            border-radius: 20px;
            padding: 2.8rem 2.2rem;
            width: 420px;
            backdrop-filter: blur(20px);
            box-shadow: 0 30px 80px rgba(0,0,0,0.7), 0 0 50px rgba(0,255,102,0.03);
            position: relative;
            overflow: hidden;
        }
        .login-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00ff66, transparent);
            animation: scanLine 3s ease-in-out infinite;
        }
        @keyframes scanLine {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }
        .brand-icon {
            width: 80px; height: 80px;
            margin: 0 auto 12px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .brand-icon .outer {
            position: absolute;
            width: 100%; height: 100%;
            border: 2px solid rgba(0,255,102,0.2);
            border-radius: 50%;
            animation: pulseRing 3s ease-in-out infinite;
        }
        .brand-icon .inner {
            width: 55px; height: 55px;
            background: linear-gradient(135deg, rgba(0,255,102,0.12), rgba(0,200,80,0.05));
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 26px;
            color: #00ff66;
            border: 1px solid rgba(0,255,102,0.15);
        }
        @keyframes pulseRing {
            0% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.08); opacity: 0.1; }
            100% { transform: scale(1); opacity: 0.5; }
        }
        .brand-name {
            font-family: 'Orbitron', monospace;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 8px;
            color: #00ff66;
            text-align: center;
            text-shadow: 0 0 30px rgba(0,255,102,0.15);
        }
        .brand-sub {
            text-align: center;
            color: #2a2a2a;
            font-size: 0.7rem;
            letter-spacing: 12px;
            text-transform: uppercase;
            margin-bottom: 28px;
            font-weight: 300;
        }
        .form-control {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px;
            color: #ccc;
            padding: 13px 16px;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        .form-control:focus {
            background: rgba(255,255,255,0.05);
            border-color: #00ff66;
            box-shadow: 0 0 25px rgba(0,255,102,0.08);
            color: #fff;
        }
        .form-control::placeholder { color: #333; }
        .form-label { color: #555; font-size: 0.75rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
        .input-group-icon { position: relative; }
        .input-group-icon i {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #333;
            font-size: 0.9rem;
            z-index: 2;
        }
        .input-group-icon .form-control { padding-left: 40px; }
        .btn-login {
            background: linear-gradient(135deg, #00ff66, #00cc52);
            border: none;
            color: #000;
            font-weight: 800;
            letter-spacing: 4px;
            padding: 13px;
            border-radius: 10px;
            transition: all 0.3s;
            font-size: 0.85rem;
            text-transform: uppercase;
            font-family: 'Orbitron', monospace;
        }
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 35px rgba(0,255,102,0.25);
            color: #000;
        }
        .login-footer { text-align: center; margin-top: 20px; color: #1a1a1a; font-size: 0.7rem; letter-spacing: 2px; }
        .error-alert {
            background: rgba(255,0,50,0.06);
            border: 1px solid rgba(255,0,50,0.1);
            color: #ff4466;
            border-radius: 8px;
            padding: 10px 14px;
            font-size: 0.8rem;
            text-align: center;
            margin-bottom: 16px;
        }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="brand-icon">
            <div class="outer"></div>
            <div class="inner"><i class="fas fa-satellite-dish"></i></div>
        </div>
        <div class="brand-name">KOZMOS55</div>
        <div class="brand-sub">Premium IPTV</div>
        {% if error %}
        <div class="error-alert"><i class="fas fa-exclamation-circle me-1"></i>{{ error }}</div>
        {% endif %}
        <form method="POST">
            <div class="mb-3">
                <label class="form-label"><i class="fas fa-user me-1"></i>Kullanıcı Adı</label>
                <div class="input-group-icon">
                    <i class="fas fa-user"></i>
                    <input type="text" name="username" class="form-control" required autocomplete="off" placeholder="kullanıcı adı">
                </div>
            </div>
            <div class="mb-4">
                <label class="form-label"><i class="fas fa-lock me-1"></i>Şifre</label>
                <div class="input-group-icon">
                    <i class="fas fa-lock"></i>
                    <input type="password" name="password" class="form-control" required placeholder="••••••••">
                </div>
            </div>
            <button type="submit" class="btn btn-login w-100">Giriş</button>
        </form>
        <div class="login-footer">KOZMOS55 &bull; v2.0</div>
    </div>
</body>
</html>
'''

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kozmos55 Player</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #050508;
            color: #ccc;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden;
            height: 100vh;
        }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,255,102,0.2); border-radius: 4px; }

        /* SIDEBAR */
        .sidebar {
            background: rgba(6,6,12,0.98);
            border-right: 1px solid rgba(0,255,102,0.06);
            height: 100vh;
            overflow-y: auto;
            padding: 0;
        }
        .sidebar-header {
            padding: 20px 16px 12px;
            border-bottom: 1px solid rgba(0,255,102,0.06);
        }
        .sidebar-brand {
            font-family: 'Orbitron', monospace;
            font-size: 1.2rem;
            font-weight: 900;
            letter-spacing: 4px;
            color: #00ff66;
            text-shadow: 0 0 20px rgba(0,255,102,0.1);
        }
        .sidebar-brand small { font-size: 0.55rem; color: #2a2a2a; letter-spacing: 6px; margin-left: 4px; }
        .sidebar-user {
            padding: 10px 16px;
            background: rgba(0,255,102,0.02);
            margin: 8px 12px;
            border-radius: 8px;
            border-left: 2px solid rgba(0,255,102,0.15);
            font-size: 0.78rem;
        }
        .sidebar-user .label { color: #444; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; }
        .sidebar-user .value { color: #00ff66; font-weight: 600; }
        .cat-btn {
            display: block;
            padding: 9px 18px;
            color: #555;
            text-decoration: none;
            font-size: 0.82rem;
            border-left: 2px solid transparent;
            transition: all 0.2s;
            margin: 1px 0;
        }
        .cat-btn:hover, .cat-btn.active {
            color: #00ff66;
            background: rgba(0,255,102,0.03);
            border-left-color: #00ff66;
        }
        .cat-btn i { width: 18px; margin-right: 8px; }

        /* MAIN */
        .main-area {
            height: 100vh;
            padding: 0;
            overflow-y: auto;
        }
        .player-wrap {
            background: #000;
            border-bottom: 1px solid rgba(0,255,102,0.06);
            position: relative;
        }
        .player-wrap .ratio { border-radius: 0 !important; }
        #playing-title {
            position: absolute;
            bottom: 14px;
            left: 18px;
            color: #fff;
            font-size: 0.85rem;
            font-weight: 600;
            text-shadow: 0 2px 12px rgba(0,0,0,0.9);
            background: rgba(0,0,0,0.6);
            padding: 5px 16px;
            border-radius: 20px;
            border-left: 2px solid #00ff66;
            pointer-events: none;
            z-index: 2;
            backdrop-filter: blur(5px);
        }
        .channels-section { padding: 18px 22px; }
        .channels-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
        }
        .channels-header h5 {
            color: #00ff66;
            font-weight: 600;
            font-size: 0.95rem;
            margin: 0;
            font-family: 'Orbitron', monospace;
            letter-spacing: 1px;
        }
        .channels-header .count { color: #333; font-size: 0.78rem; }
        .channel-card {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.03);
            border-radius: 10px;
            padding: 9px 12px;
            cursor: pointer;
            transition: all 0.25s;
            margin-bottom: 5px;
        }
        .channel-card:hover {
            background: rgba(0,255,102,0.03);
            border-color: rgba(0,255,102,0.12);
            transform: translateX(3px);
        }
        .channel-card .ch-name {
            font-weight: 500;
            font-size: 0.82rem;
            color: #bbb;
        }
        .channel-card .ch-cat {
            font-size: 0.65rem;
            color: #00ff66;
            opacity: 0.4;
        }
        .channel-card img {
            width: 26px;
            height: 26px;
            object-fit: contain;
            border-radius: 4px;
            margin-right: 10px;
        }
        .top-btn {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            color: #888;
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 0.7rem;
            text-decoration: none;
            transition: all 0.2s;
        }
        .top-btn:hover { background: rgba(255,255,255,0.06); color: #ccc; }
        .top-btn.admin { border-color: rgba(255,193,7,0.2); color: #ffc107; }
        .top-btn.admin:hover { background: rgba(255,193,7,0.08); }
        .top-btn.logout { border-color: rgba(255,0,0,0.15); color: #f55; }
        .top-btn.logout:hover { background: rgba(255,0,0,0.06); }
    </style>
</head>
<body>
    <div class="container-fluid h-100">
        <div class="row h-100">
            <!-- SIDEBAR -->
            <div class="col-md-2 sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-brand">KOZMOS<small>55</small></div>
                </div>
                <div class="sidebar-user">
                    <div class="label"><i class="fas fa-user me-1"></i>Abone</div>
                    <div class="value">{{ session['user'] }}</div>
                    <div class="label mt-2"><i class="far fa-clock me-1"></i>Bitiş</div>
                    <div class="value">{{ expiry }}</div>
                </div>
                <a href="/index?category=Hepsi" class="cat-btn {% if current_category == 'Hepsi' %}active{% endif %}">
                    <i class="fas fa-th-large"></i> Tüm Kanallar
                </a>
                {% for cat in categories %}
                <a href="/index?category={{ cat.category }}" class="cat-btn {% if current_category == cat.category %}active{% endif %}">
                    <i class="fas fa-folder"></i> {{ cat.category }}
                </a>
                {% endfor %}
            </div>

            <!-- MAIN -->
            <div class="col-md-10 main-area">
                <div class="player-wrap">
                    <div class="ratio ratio-16x9">
                        <video id="my-video" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" data-setup='{}'>
                            <source id="video-source" src="" type="application/x-mpegURL">
                        </video>
                    </div>
                    <div id="playing-title"><i class="fas fa-play me-1"></i>Kanal seçin</div>
                </div>

                <div class="channels-section">
                    <div class="channels-header">
                        <h5><i class="fas fa-list me-2"></i>{{ current_category }}</h5>
                        <div>
                            {% if session['user'] == 'admin' %}
                            <a href="/admin" class="top-btn admin me-1"><i class="fas fa-cog me-1"></i>Panel</a>
                            {% endif %}
                            <a href="/logout" class="top-btn logout"><i class="fas fa-sign-out-alt me-1"></i>Çıkış</a>
                            <span class="count ms-2">{{ channels|length }} kanal</span>
                        </div>
                    </div>
                    <div class="row g-1">
                        {% for channel in channels %}
                        <div class="col-lg-3 col-md-4 col-sm-6">
                            <div class="channel-card d-flex align-items-center" onclick="changeChannel('{{ channel.url }}', '{{ channel.name }}')">
                                {% if channel.logo %}
                                <img src="{{ channel.logo }}" alt="" onerror="this.style.display='none'">
                                {% endif %}
                                <div class="flex-grow-1 min-width-0">
                                    <div class="ch-name text-truncate">{{ channel.name }}</div>
                                    <div class="ch-cat">{{ channel.category }}</div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function changeChannel(url, name) {
            var player = videojs('my-video');
            player.src({ src: url, type: 'application/x-mpegURL' });
            player.play();
            document.getElementById('playing-title').innerHTML = '<i class="fas fa-play me-1"></i>' + name;
        }
    </script>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kozmos55 - Yönetim</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background: #050508; color: #ccc; font-family: 'Segoe UI', sans-serif; }
        .admin-header {
            background: rgba(6,6,12,0.98);
            border-bottom: 1px solid rgba(0,255,102,0.06);
            padding: 14px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .admin-header h3 {
            font-family: 'Orbitron', monospace;
            font-weight: 900;
            letter-spacing: 4px;
            color: #00ff66;
            margin: 0;
            font-size: 1.2rem;
            text-shadow: 0 0 20px rgba(0,255,102,0.08);
        }
        .card-glass {
            background: rgba(8,8,14,0.94);
            border: 1px solid rgba(0,255,102,0.06);
            border-radius: 14px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        }
        .card-glass .card-title {
            color: #00ff66;
            font-weight: 600;
            font-size: 0.9rem;
            letter-spacing: 2px;
            border-bottom: 1px solid rgba(0,255,102,0.06);
            padding-bottom: 12px;
            font-family: 'Orbitron', monospace;
        }
        .form-control {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            color: #ccc;
            padding: 10px 14px;
            font-size: 0.85rem;
        }
        .form-control:focus {
            background: rgba(255,255,255,0.05);
            border-color: #00ff66;
            box-shadow: 0 0 15px rgba(0,255,102,0.06);
            color: #fff;
        }
        .form-select {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            color: #ccc;
            padding: 10px 14px;
            font-size: 0.85rem;
        }
        .form-select:focus {
            border-color: #00ff66;
            box-shadow: 0 0 15px rgba(0,255,102,0.06);
        }
        .form-label { color: #444; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
        .btn-primary-cyber {
            background: linear-gradient(135deg, #00ff66, #00cc52);
            border: none;
            color: #000;
            font-weight: 800;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 0.8rem;
            transition: all 0.3s;
            letter-spacing: 2px;
            font-family: 'Orbitron', monospace;
        }
        .btn-primary-cyber:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0,255,102,0.2); color: #000; }
        .btn-danger-cyber {
            background: rgba(255,0,50,0.06);
            border: 1px solid rgba(255,0,50,0.1);
            color: #f55;
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 0.7rem;
            transition: all 0.2s;
        }
        .btn-danger-cyber:hover { background: rgba(255,0,50,0.1); color: #f55; }
        .table-cyber { color: #999; font-size: 0.8rem; margin: 0; }
        .table-cyber thead th {
            border-bottom: 1px solid rgba(0,255,102,0.05);
            color: #444;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.65rem;
            letter-spacing: 1px;
            padding: 8px 10px;
        }
        .table-cyber td { border-bottom: 1px solid rgba(255,255,255,0.02); padding: 8px 10px; vertical-align: middle; }
        .table-cyber tr:hover { background: rgba(0,255,102,0.02); }
        .badge-cat {
            background: rgba(0,255,102,0.06);
            color: #00ff66;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.65rem;
        }
        .msg-alert {
            background: rgba(0,255,102,0.04);
            border: 1px solid rgba(0,255,102,0.08);
            color: #00ff66;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 0.82rem;
        }
        .stat-box {
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            background: rgba(0,255,102,0.02);
            border: 1px solid rgba(0,255,102,0.04);
        }
        .stat-box .number { font-family: 'Orbitron', monospace; color: #00ff66; font-size: 1.6rem; font-weight: 900; }
        .stat-box .label { color: #444; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
    </style>
</head>
<body>
    <div class="admin-header">
        <h3><i class="fas fa-shield-alt me-2"></i>KOZMOS55 PANEL</h3>
        <a href="/index" class="btn btn-primary-cyber btn-sm"><i class="fas fa-play me-1"></i>Oyuncu</a>
    </div>

    <div class="container-fluid p-4">
        {% if msg %}
        <div class="msg-alert mb-4"><i class="fas fa-check-circle me-1"></i>{{ msg }}</div>
        {% endif %}

        <!-- İSTATİSTİKLER -->
        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="stat-box">
                    <div class="number">{{ users|length }}</div>
                    <div class="label">Kullanıcı</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-box">
                    <div class="number">{{ channels|length }}</div>
                    <div class="label">Kanal</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-box">
                    <div class="number">{{ categories|length }}</div>
                    <div class="label">Kategori</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-box">
                    <div class="number">55</div>
                    <div class="label">Kozmos</div>
                </div>
            </div>
        </div>

        <div class="row g-4">
            <!-- KULLANICI ÜRET -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100">
                    <div class="card-title"><i class="fas fa-user-plus me-2"></i>Kullanıcı Üret</div>
                    <form method="POST">
                        <input type="hidden" name="action" value="add_user">
                        <div class="mb-3">
                            <label class="form-label">Kullanıcı Adı</label>
                            <input type="text" name="username" class="form-control" required autocomplete="off" placeholder="kullanıcı adı">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Şifre</label>
                            <input type="text" name="password" class="form-control" required placeholder="••••••••">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Bitiş Süresi</label>
                            <select name="expiry_option" class="form-select">
                                <option value="1">1 Günlük</option>
                                <option value="3">3 Günlük</option>
                                <option value="7">7 Günlük</option>
                                <option value="15">15 Günlük</option>
                                <option value="30" selected>30 Günlük</option>
                                <option value="90">3 Aylık</option>
                                <option value="180">6 Aylık</option>
                                <option value="365">1 Yıllık</option>
                                <option value="0">Sınırsız</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-primary-cyber w-100">Oluştur</button>
                    </form>
                </div>
            </div>

            <!-- KANAL EKLE -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100">
                    <div class="card-title"><i class="fas fa-plus-circle me-2"></i>Kanal Ekle</div>
                    <form method="POST">
                        <input type="hidden" name="action" value="add_channel">
                        <div class="mb-3">
                            <label class="form-label">Kanal Adı</label>
                            <input type="text" name="name" class="form-control" required placeholder="TRT 1">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">M3U8 Linki</label>
                            <input type="url" name="url" class="form-control" required placeholder="http://...m3u8">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Kategori</label>
                            <input type="text" name="category" class="form-control" required placeholder="Spor, Sinema...">
                        </div>
                        <button type="submit" class="btn btn-primary-cyber w-100">Kaydet</button>
                    </form>
                </div>
            </div>

            <!-- HIZLI BİLGİ -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100 d-flex align-items-center justify-content-center text-center">
                    <div style="font-family:'Orbitron',monospace; font-size:3rem; color:#00ff66; opacity:0.15;">55</div>
                    <div style="color:#333; font-size:0.8rem; letter-spacing:4px; text-transform:uppercase;">Kozmos55 Premium</div>
                    <div style="color:#222; font-size:0.7rem; margin-top:8px;">IPTV Management Panel</div>
                </div>
            </div>
        </div>

        <div class="row g-4 mt-2">
            <!-- KULLANICI LİSTESİ -->
            <div class="col-lg-6">
                <div class="card card-glass p-4">
                    <div class="card-title"><i class="fas fa-users me-2"></i>Kullanıcılar</div>
                    <table class="table table-cyber">
                        <thead><tr><th>Kullanıcı</th><th>Şifre</th><th>Bitiş</th><th></th></tr></thead>
                        <tbody>
                            {% for u in users %}
                            <tr>
                                <td><i class="fas fa-user me-1" style="color:#333;"></i>{{ u.username }}</td>
                                <td style="font-family:monospace; color:#555;">{{ u.password }}</td>
                                <td><span style="color:#ffc107;">{{ u.expiry_date }}</span></td>
                                <td>
                                    {% if u.username != 'admin' %}
                                    <a href="/delete_user/{{ u.id }}" class="btn btn-danger-cyber" onclick="return confirm('Emin misin?')"><i class="fas fa-trash"></i></a>
                                    {% else %}
                                    <span style="color:#333; font-size:0.65rem;">ADMIN</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- KANAL LİSTESİ -->
            <div class="col-lg-6">
                <div class="card card-glass p-4">
                    <div class="card-title"><i class="fas fa-tv me-2"></i>Kanallar <span style="color:#444; font-weight:400; font-size:0.75rem;">({{ channels|length }})</span></div>
                    <div style="max-height:350px; overflow-y:auto;">
                        <table class="table table-cyber">
                            <thead><tr><th>Kanal</th><th>Kategori</th><th></th></tr></thead>
                            <tbody>
                                {% for c in channels %}
                                <tr>
                                    <td>
                                        {% if c.logo %}<img src="{{ c.logo }}" style="width:16px; height:16px; object-fit:contain; margin-right:6px;" onerror="this.style.display='none'">{% endif %}
                                        {{ c.name }}
                                    </td>
                                    <td><span class="badge-cat">{{ c.category }}</span></td>
                                    <td><a href="/delete_channel/{{ c.id }}" class="btn btn-danger-cyber" onclick="return confirm('Sil?')"><i class="fas fa-trash"></i></a></td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

# ============================================================
# ROTALAR
# ============================================================

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            if user['username'] != 'admin' and user['expiry_date'] != 'Sınırsız':
                try:
                    exp_date = datetime.strptime(user['expiry_date'], '%Y-%m-%d')
                    if datetime.now() > exp_date:
                        error = "Bu hesabın kullanım süresi dolmuştur!"
                        return render_template_string(LOGIN_HTML, error=error)
                except ValueError:
                    pass
            session['user'] = username
            session['expiry'] = user['expiry_date']
            return redirect(url_for('index'))
        else:
            error = "Hatalı kullanıcı adı veya şifre!"
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    category_filter = request.args.get('category', 'Hepsi')
    conn = get_db_connection()
    categories = conn.execute('SELECT DISTINCT category FROM channels').fetchall()
    if category_filter == 'Hepsi':
        channels = conn.execute('SELECT * FROM channels').fetchall()
    else:
        channels = conn.execute('SELECT * FROM channels WHERE category = ?', (category_filter,)).fetchall()
    conn.close()
    return render_template_string(INDEX_HTML,
                                  channels=channels,
                                  categories=categories,
                                  current_category=category_filter,
                                  expiry=session.get('expiry', 'Sınırsız'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    msg = None
    conn = get_db_connection()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_user':
            username = request.form['username']
            password = request.form['password']
            expiry_option = request.form['expiry_option']
            
            if expiry_option == '0':
                expiry_date = 'Sınırsız'
            else:
                days = int(expiry_option)
                expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            try:
                conn.execute('INSERT INTO users (username, password, expiry_date) VALUES (?, ?, ?)',
                             (username, password, expiry_date))
                conn.commit()
                msg = f"Kullanıcı '{username}' oluşturuldu. Bitiş: {expiry_date}"
            except sqlite3.IntegrityError:
                msg = "Hata: Bu kullanıcı adı zaten mevcut!"
        elif action == 'add_channel':
            name = request.form['name']
            url = request.form['url']
            category = request.form['category']
            conn.execute('INSERT INTO channels (name, url, category, logo) VALUES (?, ?, ?, ?)',
                         (name, url, category, ''))
            conn.commit()
            msg = f"Kanal '{name}' eklendi."

    users = conn.execute('SELECT * FROM users').fetchall()
    channels = conn.execute('SELECT * FROM channels').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM channels').fetchall()
    conn.close()
    return render_template_string(ADMIN_HTML, users=users, channels=channels, categories=categories, msg=msg)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ? AND username != "admin"', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_channel/<int:id>')
def delete_channel(id):
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM channels WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('expiry', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
