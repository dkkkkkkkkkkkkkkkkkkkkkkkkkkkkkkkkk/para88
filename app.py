import os
import re
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "guvenpanel_2026_gizli_anahtar"

# ============================================================
# VERİTABANI
# ============================================================
def init_db():
    conn = sqlite3.connect('iptv.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT, 
                  server_url TEXT,
                  expiry_date TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS channels 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  url TEXT, 
                  category TEXT,
                  logo TEXT,
                  stream_type TEXT DEFAULT 'live')''')

    c.execute('''CREATE TABLE IF NOT EXISTS m3u_sources 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  url TEXT,
                  last_import TEXT)''')

    # Admin hesabı
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password, server_url, expiry_date) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin123', 'https://guvenpanel.com', 'Sınırsız'))

    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('iptv.db')
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================
# M3U / XTREAM PARSE
# ============================================================
def parse_m3u_content(m3u_text):
    """M3U içeriğini parse et - live, vod, series ayırt et"""
    channels = []
    lines = m3u_text.strip().split('\n')
    i = 0
    
    # Önce #EXTM3U header'ını kontrol et
    has_extm3u = any(l.strip().startswith('#EXTM3U') for l in lines[:5])
    
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            logo = ""
            category = "Genel"
            name = "İsimsiz"
            stream_type = "live"
            
            # tvg-logo
            logo_match = re.search(r'tvg-logo="([^"]*)"', line)
            if logo_match:
                logo = logo_match.group(1)
            
            # group-title
            group_match = re.search(r'group-title="([^"]*)"', line)
            if group_match:
                category = group_match.group(1)
            
            # Kanal adı - son virgülden sonra
            name_match = re.search(r',(.+)$', line)
            if name_match:
                name = name_match.group(1).strip()
            
            # Stream tipini belirle (VOD/Series için)
            if 'movie' in line.lower() or 'vod' in line.lower():
                stream_type = "vod"
            elif 'series' in line.lower():
                stream_type = "series"
            
            # Bir sonraki satır URL
            if i + 1 < len(lines):
                url = lines[i + 1].strip()
                if url and not url.startswith('#'):
                    channels.append({
                        'name': name,
                        'url': url,
                        'category': category,
                        'logo': logo,
                        'stream_type': stream_type
                    })
                i += 2
                continue
        i += 1
    
    return channels

def fetch_and_import_m3u(m3u_url):
    """M3U URL'sinden kanalları çek ve veritabanına ekle"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(m3u_url, headers=headers, timeout=30)
        resp.raise_for_status()
        
        # Encoding kontrolü
        resp.encoding = resp.apparent_encoding or 'utf-8'
        m3u_text = resp.text
        
        channels = parse_m3u_content(m3u_text)
        
        if not channels:
            return 0, "M3U içeriğinde kanal bulunamadı"
        
        conn = get_db()
        eklenen = 0
        for ch in channels:
            # Aynı URL varsa atla
            var = conn.execute('SELECT id FROM channels WHERE url = ?', (ch['url'],)).fetchone()
            if not var:
                conn.execute('''INSERT INTO channels (name, url, category, logo, stream_type) 
                                VALUES (?, ?, ?, ?, ?)''',
                             (ch['name'], ch['url'], ch['category'], ch['logo'], ch['stream_type']))
                eklenen += 1
        
        conn.commit()
        conn.close()
        return eklenen, f"{len(channels)} kanal bulundu, {eklenen} yeni eklendi"
    
    except requests.exceptions.Timeout:
        return 0, "M3U linki zaman aşımına uğradı"
    except requests.exceptions.RequestException as e:
        return 0, f"M3U linki alınamadı: {str(e)}"
    except Exception as e:
        return 0, f"Hata: {str(e)}"

# ============================================================
# HTML ŞABLONLARI - GÜVEN PANEL
# ============================================================

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GÜVEN PANEL - IPTV</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0a0f;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', sans-serif;
            background-image: 
                linear-gradient(135deg, rgba(255,0,0,0.02) 0%, transparent 50%, rgba(255,255,255,0.01) 100%);
            position: relative;
            overflow: hidden;
        }
        body::before {
            content: 'GÜVEN';
            position: fixed;
            top: -30%; right: -10%;
            font-size: 25rem;
            font-weight: 900;
            color: rgba(255,0,0,0.02);
            pointer-events: none;
            font-family: 'Barlow Condensed', sans-serif;
            transform: rotate(15deg);
            letter-spacing: 10px;
        }
        body::after {
            content: 'PANEL';
            position: fixed;
            bottom: -20%; left: -5%;
            font-size: 18rem;
            font-weight: 900;
            color: rgba(255,255,255,0.01);
            pointer-events: none;
            font-family: 'Barlow Condensed', sans-serif;
            transform: rotate(-10deg);
            letter-spacing: 15px;
        }
        .login-card {
            background: rgba(12,12,20,0.97);
            border: 1px solid rgba(255,0,0,0.1);
            border-radius: 16px;
            padding: 2.5rem 2rem;
            width: 420px;
            backdrop-filter: blur(20px);
            box-shadow: 0 30px 80px rgba(0,0,0,0.8), 0 0 30px rgba(255,0,0,0.02);
            position: relative;
            overflow: hidden;
        }
        .login-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #ff0000, transparent);
        }
        .brand-icon {
            width: 75px; height: 75px;
            margin: 0 auto 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, rgba(255,0,0,0.08), rgba(255,255,255,0.02));
            border-radius: 50%;
            border: 1px solid rgba(255,0,0,0.15);
            font-size: 28px;
            color: #ff0000;
        }
        .brand-name {
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 2.8rem;
            font-weight: 900;
            letter-spacing: 8px;
            text-align: center;
            color: #fff;
            text-shadow: 0 0 20px rgba(255,0,0,0.08);
        }
        .brand-name span { color: #ff0000; }
        .brand-sub {
            text-align: center;
            color: #333;
            font-size: 0.7rem;
            letter-spacing: 6px;
            text-transform: uppercase;
            margin-bottom: 24px;
        }
        .form-control {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 8px;
            color: #ccc;
            padding: 12px 16px;
            font-size: 0.85rem;
            transition: all 0.3s;
        }
        .form-control:focus {
            background: rgba(255,255,255,0.05);
            border-color: #ff0000;
            box-shadow: 0 0 20px rgba(255,0,0,0.06);
            color: #fff;
        }
        .form-control::placeholder { color: #333; }
        .form-label { color: #555; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
        .input-icon { position: relative; }
        .input-icon i {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: #333;
            font-size: 0.85rem;
            z-index: 2;
        }
        .input-icon .form-control { padding-left: 38px; }
        .btn-login {
            background: linear-gradient(135deg, #cc0000, #ff0000);
            border: none;
            color: #fff;
            font-weight: 700;
            letter-spacing: 3px;
            padding: 12px;
            border-radius: 8px;
            transition: all 0.3s;
            font-size: 0.85rem;
            text-transform: uppercase;
        }
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(255,0,0,0.2);
            color: #fff;
        }
        .footer-text { text-align: center; margin-top: 18px; color: #1a1a1a; font-size: 0.7rem; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="brand-icon"><i class="fas fa-shield-halved"></i></div>
        <div class="brand-name">GÜVEN <span>PANEL</span></div>
        <div class="brand-sub">Premium IPTV Platform</div>
        {% if error %}
        <div class="alert" style="background:rgba(255,0,0,0.06); border:1px solid rgba(255,0,0,0.1); color:#ff4444; border-radius:8px; padding:10px 14px; font-size:0.8rem; text-align:center; margin-bottom:16px;">
            <i class="fas fa-exclamation-circle me-1"></i>{{ error }}
        </div>
        {% endif %}
        <form method="POST">
            <div class="mb-3">
                <label class="form-label"><i class="fas fa-server me-1"></i>Server</label>
                <div class="input-icon">
                    <i class="fas fa-globe"></i>
                    <input type="text" name="server_url" class="form-control" required placeholder="ornek.com:8080">
                </div>
            </div>
            <div class="mb-3">
                <label class="form-label"><i class="fas fa-user me-1"></i>Kullanıcı</label>
                <div class="input-icon">
                    <i class="fas fa-user"></i>
                    <input type="text" name="username" class="form-control" required placeholder="kullanıcı adı">
                </div>
            </div>
            <div class="mb-4">
                <label class="form-label"><i class="fas fa-lock me-1"></i>Şifre</label>
                <div class="input-icon">
                    <i class="fas fa-lock"></i>
                    <input type="password" name="password" class="form-control" required placeholder="••••••••">
                </div>
            </div>
            <button type="submit" class="btn btn-login w-100">GİRİŞ YAP</button>
        </form>
        <div class="footer-text">GÜVEN PANEL v2.0</div>
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
    <title>GÜVEN PANEL - Player</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0a0f;
            color: #ccc;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden;
            height: 100vh;
        }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,0,0,0.15); border-radius: 4px; }

        .sidebar {
            background: rgba(8,8,15,0.98);
            border-right: 1px solid rgba(255,0,0,0.05);
            height: 100vh;
            overflow-y: auto;
            padding: 0;
        }
        .sidebar-header {
            padding: 18px 16px 10px;
            border-bottom: 1px solid rgba(255,0,0,0.05);
        }
        .sidebar-brand {
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.4rem;
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
        }
        .sidebar-brand span { color: #ff0000; }
        .sidebar-brand small { font-size: 0.5rem; color: #333; letter-spacing: 4px; margin-left: 4px; }
        .sidebar-user {
            padding: 10px 14px;
            background: rgba(255,0,0,0.02);
            margin: 8px 12px;
            border-radius: 6px;
            border-left: 2px solid rgba(255,0,0,0.1);
            font-size: 0.75rem;
        }
        .sidebar-user .label { color: #444; font-size: 0.6rem; text-transform: uppercase; }
        .sidebar-user .value { color: #ff4444; font-weight: 600; }
        .cat-btn {
            display: block;
            padding: 8px 16px;
            color: #555;
            text-decoration: none;
            font-size: 0.8rem;
            border-left: 2px solid transparent;
            transition: all 0.2s;
        }
        .cat-btn:hover, .cat-btn.active {
            color: #ff4444;
            background: rgba(255,0,0,0.02);
            border-left-color: #ff0000;
        }
        .cat-btn i { width: 16px; margin-right: 6px; font-size: 0.75rem; }

        .main-area { height: 100vh; padding: 0; overflow-y: auto; }
        .player-wrap {
            background: #000;
            border-bottom: 1px solid rgba(255,0,0,0.04);
            position: relative;
        }
        #playing-title {
            position: absolute;
            bottom: 12px;
            left: 16px;
            color: #fff;
            font-size: 0.8rem;
            font-weight: 600;
            text-shadow: 0 2px 10px rgba(0,0,0,0.9);
            background: rgba(0,0,0,0.6);
            padding: 4px 14px;
            border-radius: 16px;
            border-left: 2px solid #ff0000;
            pointer-events: none;
            z-index: 2;
        }
        .channels-section { padding: 16px 20px; }
        .channels-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
        .channels-header h5 {
            color: #fff;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0;
        }
        .channels-header h5 span { color: #ff0000; }
        .channels-header .count { color: #333; font-size: 0.75rem; }
        .channel-card {
            background: rgba(255,255,255,0.01);
            border: 1px solid rgba(255,255,255,0.03);
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 4px;
        }
        .channel-card:hover {
            background: rgba(255,0,0,0.02);
            border-color: rgba(255,0,0,0.08);
            transform: translateX(2px);
        }
        .channel-card .ch-name { font-weight: 500; font-size: 0.8rem; color: #bbb; }
        .channel-card .ch-cat { font-size: 0.6rem; color: #ff4444; opacity: 0.4; }
        .channel-card img {
            width: 22px; height: 22px; object-fit: contain;
            border-radius: 3px; margin-right: 8px;
        }
        .top-btn {
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            color: #888;
            border-radius: 5px;
            padding: 3px 10px;
            font-size: 0.65rem;
            text-decoration: none;
            transition: all 0.2s;
        }
        .top-btn:hover { background: rgba(255,255,255,0.04); color: #ccc; }
        .top-btn.admin { border-color: rgba(255,0,0,0.15); color: #ff4444; }
        .top-btn.admin:hover { background: rgba(255,0,0,0.04); }
        .top-btn.logout { border-color: rgba(255,255,255,0.05); }

        /* Stream tipi badge */
        .type-badge {
            font-size: 0.55rem;
            padding: 1px 6px;
            border-radius: 3px;
            margin-left: 4px;
        }
        .type-live { background: rgba(0,200,80,0.1); color: #00cc44; }
        .type-vod { background: rgba(255,200,0,0.1); color: #ffcc00; }
        .type-series { background: rgba(0,150,255,0.1); color: #0099ff; }
    </style>
</head>
<body>
    <div class="container-fluid h-100">
        <div class="row h-100">
            <div class="col-md-2 sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-brand">GÜVEN <span>PANEL</span><small>IPTV</small></div>
                </div>
                <div class="sidebar-user">
                    <div class="label"><i class="fas fa-user me-1"></i>Abone</div>
                    <div class="value">{{ session['user'] }}</div>
                    <div class="label mt-2"><i class="fas fa-server me-1"></i>Server</div>
                    <div class="value" style="font-size:0.65rem; word-break:break-all;">{{ session.get('server', '-') }}</div>
                    <div class="label mt-2"><i class="far fa-clock me-1"></i>Bitiş</div>
                    <div class="value">{{ expiry }}</div>
                </div>
                <a href="/index?category=Hepsi" class="cat-btn {% if current_category == 'Hepsi' %}active{% endif %}">
                    <i class="fas fa-th-large"></i> Tümü
                </a>
                {% for cat in categories %}
                <a href="/index?category={{ cat.category }}" class="cat-btn {% if current_category == cat.category %}active{% endif %}">
                    <i class="fas fa-folder"></i> {{ cat.category }}
                </a>
                {% endfor %}
            </div>

            <div class="col-md-10 main-area">
                <div class="player-wrap">
                    <div class="ratio ratio-16x9">
                        <video id="my-video" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" data-setup='{"html5":{"hls":{"overrideNative":true}}}'>
                            <source id="video-source" src="" type="application/x-mpegURL">
                        </video>
                    </div>
                    <div id="playing-title"><i class="fas fa-play me-1"></i>Kanal seçin</div>
                </div>

                <div class="channels-section">
                    <div class="channels-header">
                        <h5><i class="fas fa-list me-2"></i><span>{{ current_category }}</span></h5>
                        <div>
                            {% if session['user'] == 'admin' %}
                            <a href="/admin" class="top-btn admin me-1"><i class="fas fa-cog me-1"></i>Panel</a>
                            {% endif %}
                            <a href="/logout" class="top-btn logout"><i class="fas fa-sign-out-alt me-1"></i>Çıkış</a>
                            <span class="count ms-2">{{ channels|length }}</span>
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
                                    <div class="ch-name text-truncate">
                                        {{ channel.name }}
                                        {% if channel.stream_type == 'vod' %}<span class="type-badge type-vod">VOD</span>{% endif %}
                                        {% if channel.stream_type == 'series' %}<span class="type-badge type-series">SERIES</span>{% endif %}
                                    </div>
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
            // M3U8 için daha iyi hls.js entegrasyonu
            player.src({ 
                src: url, 
                type: 'application/x-mpegURL'
            });
            player.play();
            document.getElementById('playing-title').innerHTML = '<i class="fas fa-play me-1"></i>' + name;
        }
        
        // Video.js hata yönetimi
        document.addEventListener('DOMContentLoaded', function() {
            var player = videojs('my-video');
            player.on('error', function() {
                console.log('Stream hatası, yeniden deneniyor...');
            });
        });
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
    <title>GÜVEN PANEL - Yönetim</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;700;900&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background: #0a0a0f; color: #ccc; font-family: 'Segoe UI', sans-serif; }
        
        .admin-header {
            background: rgba(8,8,15,0.98);
            border-bottom: 1px solid rgba(255,0,0,0.05);
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .admin-header h3 {
            font-family: 'Barlow Condensed', sans-serif;
            font-weight: 900;
            letter-spacing: 4px;
            color: #fff;
            margin: 0;
            font-size: 1.3rem;
        }
        .admin-header h3 span { color: #ff0000; }
        
        .card-glass {
            background: rgba(10,10,18,0.94);
            border: 1px solid rgba(255,0,0,0.05);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .card-glass .card-title {
            color: #fff;
            font-weight: 600;
            font-size: 0.85rem;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(255,0,0,0.05);
            padding-bottom: 10px;
        }
        .card-glass .card-title i { color: #ff0000; }
        
        .form-control, .form-select {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 8px;
            color: #ccc;
            padding: 9px 12px;
            font-size: 0.82rem;
        }
        .form-control:focus, .form-select:focus {
            background: rgba(255,255,255,0.05);
            border-color: #ff0000;
            box-shadow: 0 0 12px rgba(255,0,0,0.05);
            color: #fff;
        }
        .form-label { color: #444; font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
        
        .btn-prime {
            background: linear-gradient(135deg, #cc0000, #ff0000);
            border: none;
            color: #fff;
            font-weight: 700;
            padding: 9px 18px;
            border-radius: 8px;
            font-size: 0.78rem;
            transition: all 0.3s;
            letter-spacing: 1px;
        }
        .btn-prime:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(255,0,0,0.15); color: #fff; }
        .btn-prime-sm {
            background: rgba(255,0,0,0.06);
            border: 1px solid rgba(255,0,0,0.1);
            color: #ff4444;
            border-radius: 5px;
            padding: 3px 10px;
            font-size: 0.65rem;
            transition: all 0.2s;
        }
        .btn-prime-sm:hover { background: rgba(255,0,0,0.1); color: #ff4444; }
        
        .table-cyber { color: #888; font-size: 0.78rem; margin: 0; }
        .table-cyber thead th {
            border-bottom: 1px solid rgba(255,0,0,0.04);
            color: #444;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.6rem;
            letter-spacing: 1px;
            padding: 6px 10px;
        }
        .table-cyber td { border-bottom: 1px solid rgba(255,255,255,0.02); padding: 6px 10px; vertical-align: middle; }
        .table-cyber tr:hover { background: rgba(255,0,0,0.01); }
        
        .badge-cat {
            background: rgba(255,0,0,0.05);
            color: #ff4444;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.6rem;
        }
        
        .msg-alert {
            background: rgba(255,0,0,0.03);
            border: 1px solid rgba(255,0,0,0.06);
            color: #ff4444;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 0.8rem;
        }
        
        .stat-box {
            text-align: center;
            padding: 8px;
            border-radius: 6px;
            background: rgba(255,0,0,0.02);
            border: 1px solid rgba(255,0,0,0.03);
        }
        .stat-box .number { font-family: 'Barlow Condensed', sans-serif; color: #ff0000; font-size: 1.8rem; font-weight: 900; }
        .stat-box .label { color: #444; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="admin-header">
        <h3><i class="fas fa-shield-halved me-2"></i>GÜVEN <span>PANEL</span></h3>
        <a href="/index" class="btn btn-prime btn-sm"><i class="fas fa-play me-1"></i>Oyuncu</a>
    </div>

    <div class="container-fluid p-4">
        {% if msg %}
        <div class="msg-alert mb-3"><i class="fas fa-check-circle me-1"></i>{{ msg }}</div>
        {% endif %}

        <!-- İSTATİSTİK -->
        <div class="row g-2 mb-4">
            <div class="col-md-3"><div class="stat-box"><div class="number">{{ users|length }}</div><div class="label">Kullanıcı</div></div></div>
            <div class="col-md-3"><div class="stat-box"><div class="number">{{ channels|length }}</div><div class="label">Kanal</div></div></div>
            <div class="col-md-3"><div class="stat-box"><div class="number">{{ categories|length }}</div><div class="label">Kategori</div></div></div>
            <div class="col-md-3"><div class="stat-box"><div class="number">GÜVEN</div><div class="label">Panel</div></div></div>
        </div>

        <div class="row g-3">
            <!-- KULLANICI ÜRET -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100">
                    <div class="card-title"><i class="fas fa-user-plus me-2"></i>Kullanıcı + Server Oluştur</div>
                    <form method="POST">
                        <input type="hidden" name="action" value="add_user">
                        <div class="mb-2">
                            <label class="form-label">Kullanıcı Adı</label>
                            <input type="text" name="username" class="form-control" required placeholder="kullanıcı">
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Şifre</label>
                            <input type="text" name="password" class="form-control" required placeholder="••••••">
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Server URL</label>
                            <input type="text" name="server_url" class="form-control" required placeholder="https://sizinpanel.com:8080">
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Bitiş Süresi</label>
                            <select name="expiry_option" class="form-select">
                                <option value="1">1 Gün</option>
                                <option value="3">3 Gün</option>
                                <option value="7">7 Gün</option>
                                <option value="15">15 Gün</option>
                                <option value="30" selected>30 Gün</option>
                                <option value="90">3 Ay</option>
                                <option value="180">6 Ay</option>
                                <option value="365">1 Yıl</option>
                                <option value="0">Sınırsız</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-prime w-100">Kullanıcı Oluştur</button>
                    </form>
                </div>
            </div>

            <!-- M3U İMPORT -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100">
                    <div class="card-title"><i class="fas fa-upload me-2"></i>M3U Kanal İmport</div>
                    <form method="POST">
                        <input type="hidden" name="action" value="import_m3u">
                        <div class="mb-2">
                            <label class="form-label">M3U Linki (URL)</label>
                            <input type="url" name="m3u_url" class="form-control" placeholder="https://ornek.com/liste.m3u">
                        </div>
                        <div class="mb-2">
                            <label class="form-label">veya M3U İçeriğini Yapıştır</label>
                            <textarea name="m3u_content" class="form-control" rows="4" placeholder="#EXTM3U..."></textarea>
                        </div>
                        <button type="submit" class="btn btn-prime w-100">Kanalları İçe Aktar</button>
                    </form>
                    <hr style="border-color:rgba(255,255,255,0.03); margin:12px 0;">
                    <p class="small text-muted mb-0">VOD, Series ve Live kanalları otomatik algılanır.</p>
                </div>
            </div>

            <!-- BİLGİ -->
            <div class="col-lg-4">
                <div class="card card-glass p-4 h-100 d-flex align-items-center justify-content-center text-center">
                    <div style="font-family:'Barlow Condensed',sans-serif; font-size:4rem; color:#ff0000; opacity:0.1; font-weight:900;">GV</div>
                    <div style="color:#333; font-size:0.8rem; letter-spacing:4px; text-transform:uppercase;">Güven Panel</div>
                    <div style="color:#222; font-size:0.65rem; margin-top:6px;">Server + Kullanıcı Yönetimi</div>
                    <div style="color:#222; font-size:0.6rem; margin-top:4px;">M3U &bull; XTREAM &bull; IPTV</div>
                </div>
            </div>
        </div>

        <div class="row g-3 mt-3">
            <!-- KULLANICI LİSTESİ -->
            <div class="col-lg-6">
                <div class="card card-glass p-4">
                    <div class="card-title"><i class="fas fa-users me-2"></i>Kullanıcılar</div>
                    <table class="table table-cyber">
                        <thead><tr><th>Kullanıcı</th><th>Şifre</th><th>Server</th><th>Bitiş</th><th></th></tr></thead>
                        <tbody>
                            {% for u in users %}
                            <tr>
                                <td><i class="fas fa-user me-1" style="color:#333;"></i>{{ u.username }}</td>
                                <td style="font-family:monospace; color:#555;">{{ u.password }}</td>
                                <td style="font-size:0.65rem; color:#666; word-break:break-all;">{{ u.server_url }}</td>
                                <td><span style="color:#ffc107;">{{ u.expiry_date }}</span></td>
                                <td>
                                    {% if u.username != 'admin' %}
                                    <a href="/delete_user/{{ u.id }}" class="btn-prime-sm" onclick="return confirm('Emin misin?')"><i class="fas fa-trash"></i></a>
                                    {% else %}
                                    <span style="color:#333; font-size:0.6rem;">ADMIN</span>
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
                    <div class="card-title"><i class="fas fa-tv me-2"></i>Kanallar <span style="color:#444;font-weight:400;font-size:0.7rem;">({{ channels|length }})</span></div>
                    <div style="max-height:350px; overflow-y:auto;">
                        <table class="table table-cyber">
                            <thead><tr><th>Kanal</th><th>Kategori</th><th>Tip</th><th></th></tr></thead>
                            <tbody>
                                {% for c in channels %}
                                <tr>
                                    <td>{% if c.logo %}<img src="{{ c.logo }}" style="width:14px;height:14px;object-fit:contain;margin-right:4px;" onerror="this.style.display='none'">{% endif %}{{ c.name }}</td>
                                    <td><span class="badge-cat">{{ c.category }}</span></td>
                                    <td style="font-size:0.6rem; color:#555;">{{ c.stream_type }}</td>
                                    <td><a href="/delete_channel/{{ c.id }}" class="btn-prime-sm" onclick="return confirm('Sil?')"><i class="fas fa-trash"></i></a></td>
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
        server_url = request.form['server_url']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            # Süre kontrolü
            if user['username'] != 'admin' and user['expiry_date'] != 'Sınırsız':
                try:
                    exp_date = datetime.strptime(user['expiry_date'], '%Y-%m-%d')
                    if datetime.now() > exp_date:
                        error = "Bu hesabın kullanım süresi dolmuştur!"
                        return render_template_string(LOGIN_HTML, error=error)
                except ValueError:
                    pass
            
            # Server kontrolü (admin hariç)
            if user['username'] != 'admin' and user['server_url'] != server_url:
                error = "Server bilgisi hatalı!"
                return render_template_string(LOGIN_HTML, error=error)
            
            session['user'] = username
            session['expiry'] = user['expiry_date']
            session['server'] = user['server_url']
            return redirect(url_for('index'))
        else:
            error = "Kullanıcı adı, şifre veya server hatalı!"
    
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    category_filter = request.args.get('category', 'Hepsi')
    conn = get_db()
    categories = conn.execute('SELECT DISTINCT category FROM channels ORDER BY category').fetchall()
    
    if category_filter == 'Hepsi':
        channels = conn.execute('SELECT * FROM channels ORDER BY category, name').fetchall()
    else:
        channels = conn.execute('SELECT * FROM channels WHERE category = ? ORDER BY name', 
                               (category_filter,)).fetchall()
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
    conn = get_db()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add_user':
            username = request.form['username']
            password = request.form['password']
            server_url = request.form['server_url']
            expiry_option = request.form['expiry_option']
            
            if expiry_option == '0':
                expiry_date = 'Sınırsız'
            else:
                days = int(expiry_option)
                expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            try:
                conn.execute('INSERT INTO users (username, password, server_url, expiry_date) VALUES (?, ?, ?, ?)',
                            (username, password, server_url, expiry_date))
                conn.commit()
                msg = f"Kullanıcı '{username}' oluşturuldu. Server: {server_url} - Bitiş: {expiry_date}"
            except sqlite3.IntegrityError:
                msg = "Hata: Bu kullanıcı adı zaten mevcut!"
        
        elif action == 'import_m3u':
            m3u_text = request.form.get('m3u_content', '').strip()
            m3u_url = request.form.get('m3u_url', '').strip()
            
            if m3u_url and not m3u_text:
                adet, mesaj = fetch_and_import_m3u(m3u_url)
                msg = mesaj
            elif m3u_text:
                channels = parse_m3u_content(m3u_text)
                if channels:
                    eklenen = 0
                    for ch in channels:
                        var = conn.execute('SELECT id FROM channels WHERE url = ?', (ch['url'],)).fetchone()
                        if not var:
                            conn.execute('''INSERT INTO channels (name, url, category, logo, stream_type) 
                                            VALUES (?, ?, ?, ?, ?)''',
                                        (ch['name'], ch['url'], ch['category'], ch['logo'], ch['stream_type']))
                            eklenen += 1
                    conn.commit()
                    msg = f"{eklenen} kanal içe aktarıldı (toplam: {len(channels)})"
                else:
                    msg = "M3U içeriğinde kanal bulunamadı!"
            else:
                msg = "M3U linki veya içeriği girin!"
    
    users = conn.execute('SELECT * FROM users').fetchall()
    channels = conn.execute('SELECT * FROM channels ORDER BY category, name').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM channels').fetchall()
    conn.close()
    
    return render_template_string(ADMIN_HTML, users=users, channels=channels, categories=categories, msg=msg)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute('DELETE FROM users WHERE id = ? AND username != "admin"', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/delete_channel/<int:id>')
def delete_channel(id):
    if 'user' not in session or session['user'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute('DELETE FROM channels WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
