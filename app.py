from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import re
import random
from datetime import datetime, timedelta

app = Flask(name)

# === MERKEZİ IPTV VERİ DEPOSU ===

DATA_STORE = {
    "macs": [],
    "last_generated": [],  
    "channels": []         
}

# === [ PROFESYONEL IPTV YÖNETİM PANELİ TASARIMI ] ===

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPTV Stalker Portal Gateway Management</title>
    <style>
        :root {
            --bg-main: #0b0f19;
            --bg-card: #131a2c;
            --border-color: #22314d;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --brand-blue: #2563eb;
            --brand-blue-hover: #1d4ed8;
            --action-green: #10b981;
            --action-purple: #7c3aed;
            --accent-red: #ef4444;
        }

        body { 
            background: var(--bg-main); 
            color: var(--text-primary); 
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; 
            padding: 30px; 
            margin: 0;
            line-height: 1.5;
        }

        .container { max-width: 1400px; margin: 0 auto; }

        header { 
            border-bottom: 1px solid var(--border-color); 
            padding-bottom: 20px; 
            margin-bottom: 30px; 
        }

        h1 { margin: 0; font-size: 1.7rem; font-weight: 700; color: #ffffff; letter-spacing: -0.5px; }
        h1 span { color: var(--brand-blue); }
        .subtitle { margin: 5px 0 0 0; font-size: 0.9rem; color: var(--text-secondary); }

        .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 25px; margin-bottom: 30px; }

        .box { 
            background: var(--bg-card); 
            border: 1px solid var(--border-color); 
            padding: 24px; 
            border-radius: 12px; 
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.4);
        }

        h2 { 
            color: #ffffff; 
            font-size: 1.2rem; 
            margin-top: 0; 
            margin-bottom: 20px;
            font-weight: 600;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
        }

        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 6px; font-weight: 500; }

        input, select, button { 
            width: 100%; 
            padding: 12px 16px; 
            background: #090d16; 
            border: 1px solid var(--border-color); 
            color: #fff; 
            border-radius: 8px; 
            box-sizing: border-box; 
            font-family: inherit;
            font-size: 0.9rem;
            transition: all 0.2s ease;
        }
        input:focus, select:focus { border-color: var(--brand-blue); outline: none; box-shadow: 0 0 0 3px rgba(37,99,235,0.2); }

        button { 
            background: var(--brand-blue);
            border: none;
            color: #ffffff; 
            font-weight: 600; 
            cursor: pointer; 
            margin-top: 5px;
        }
        button:hover { background: var(--brand-blue-hover); box-shadow: 0 4px 12px rgba(37,99,235,0.3); }

        .btn-m3u { background: transparent; border: 1px solid var(--brand-blue); color: var(--brand-blue); }
        .btn-m3u:hover { background: var(--brand-blue); color: #fff; }

        .btn-generator { background: var(--action-purple); }
        .btn-generator:hover { background: #6d28d9; box-shadow: 0 4px 12px rgba(124,58,237,0.3); }

        .btn-copy { background: var(--action-green); }
        .btn-copy:hover { background: #059669; box-shadow: 0 4px 12px rgba(16,185,129,0.3); }

        .table-wrapper { max-height: 450px; overflow-y: auto; border: 1px solid var(--border-color); border-radius: 8px; background: #090d16; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 14px 16px; font-size: 0.9rem; border-bottom: 1px solid var(--border-color); }
        th { background: #0c1220; color: var(--text-secondary); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; position: sticky; top: 0; z-index: 10; }
        tr:last-child td { border-bottom: none; }
        tr:hover td { background: rgba(255,255,255,0.02); }

        .badge { padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.75rem; background: rgba(37,99,235,0.1); color: var(--brand-blue); border: 1px solid rgba(37,99,235,0.2); }
        .badge-temp { padding: 4px 10px; border-radius: 20px; font-weight: 600; font-size: 0.75rem; background: rgba(124,58,237,0.1); color: #a78bfa; border: 1px solid rgba(124,58,237,0.2); }
        
        .channel-logo { width: 38px; height: 38px; object-fit: contain; background: #000; border-radius: 8px; border: 1px solid var(--border-color); }
        .textarea-hidden { position: absolute; left: -9999px; }
        
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #090d16; }
        ::-webkit-scrollbar-thumb { background: #22314d; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #334155; }
    </style>
    <script>
        function copyToClipboard() {
            var copyText = document.getElementById("macClipboardSource");
            if (copyText.value.trim() === "") {
                alert("Kopyalanacak veri bulunamadı! Lütfen önce MAC üretin.");
                return;
            }
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Sistem: 1000 Adet MAC adresi başarıyla panoya kopyalanamıştır.");
        }
    </script>
</head>
<body>
    <div class="container">
        <header>
            <h1>IPTV <span>//</span> STALKER PORTAL GATEWAY MASTER</h1>
            <p class="subtitle">Stalker Middleware Tabanlı Cihaz Yetkilendirme ve M3U Playlist Yönetim Paneli</p>
        </header>

        <div class="box" style="margin-bottom: 30px; border-color: var(--action-purple);">
            <h2>Otomatik Seri MAC Üretim Merkezi (1000 ADET / 24 SAATLİK GEÇERLİ)</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <form action="/admin/generate-1000-macs" method="POST" style="margin: 0;">
                    <button type="submit" class="btn-generator">⚡ 1000 ADET YENİ MAC ADRESİ ÜRET</button>
                </form>
                <button onclick="copyToClipboard()" class="btn-copy">📋 ÜRETİLEN LİSTEYİ PANOMUZA KOPYALA</button>
            </div>
            <textarea id="macClipboardSource" class="textarea-hidden">{% for m in last_generated %}{{ m }}{{"\\n"}}{% endfor %}</textarea>
        </div>

        <div class="grid-2">
            <div class="box">
                <h2>Manuel MAC Adresi Ekleme</h2>
                <form action="/admin/add-mac" method="POST">
                    <div class="form-group">
                        <label>MAC Adresi</label>
                        <input type="text" name="mac" placeholder="00:1A:79:XX:XX:XX" required style="font-family: monospace;">
                    </div>
                    <div class="form-group">
                        <label>Cihaz Tanımı / Kullanıcı Bilgisi</label>
                        <input type="text" name="type" placeholder="Örn: MAG Cihazı / STB Emulator" required>
                    </div>
                    <div class="form-group">
                        <label>Hesap Bitiş Tarihi</label>
                        <input type="date" name="expiry" required>
                    </div>
                    <button type="submit">CİHAZI YETKİLENDİR</button>
                </form>
            </div>

            <div class="box">
                <h2>M3U Playlist Veri Yükleme</h2>
                <form action="/admin/upload-m3u" method="POST" enctype="multipart/form-data" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                    <div class="form-group">
                        <label>Uzantı: .m3u veya .txt formatındaki yayın listeniz</label>
                        <input type="file" name="m3u_file" accept=".m3u,.txt" required style="border: 1px dashed var(--brand-blue); padding: 30px; text-align: center; background: #090d16; cursor: pointer;">
                    </div>
                    <button type="submit" class="btn-m3u" style="margin-top: auto;">YAYIN LİSTESİNİ ÇÖZÜMLE VE AKTİF ET</button>
                </form>
            </div>
        </div>

        <div class="grid-2">
            <div class="box">
                <h2>Yetkilendirilmiş Cihaz Listesi (Toplam: {{ macs|length }})</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>MAC ADRESİ</th>
                                <th>CİHAZ TIPI</th>
                                <th>VADE TARİHİ</th>
                                <th>DURUM</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for m in macs %}
                            <tr>
                                <td style="color: var(--text-secondary); font-family: monospace;">{{ m.id }}</td>
                                <td style="color: var(--accent-red); font-weight: 700; font-family: monospace; font-size: 0.95rem;">{{ m.mac.upper() }}</td>
                                <td>{{ m.type }}</td>
                                <td style="color: var(--brand-blue); font-family: monospace;">{{ m.expiry }}</td>
                                <td>
                                    {% if "AUTO" in m.id %}
                                    <span class="badge-temp">OTOMATİK</span>
                                    {% else %}
                                    <span class="badge">SABİT</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="box">
                <h2>Dinamik Çözümlenen Kanallar (Toplam: {{ channels|length }})</h2>
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>LOGO</th>
                                <th>KANAL ADI</th>
                                <th>KATEGORİ / GRUP</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for c in channels[:200] %}
                            <tr>
                                <td style="color: var(--text-secondary); font-family: monospace;">{{ c.id }}</td>
                                <td>
                                    <img class="channel-logo" src="{{ c.logo }}" onerror="this.src='https://via.placeholder.com/38/000000/2563eb?text=TV'">
                                </td>
                                <td style="font-weight: 600; color: #fff;">{{ c.name }}</td>
                                <td style="color: var(--text-secondary);"><span style="color: var(--brand-blue); font-weight:600;">[</span> {{ c.genre }} <span style="color: var(--brand-blue); font-weight:600;">]</span></td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="4" style="text-align: center; color: var(--text-secondary); padding: 30px;">
                                    Henüz M3U listesi yüklenmedi veya liste boş.
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# === ADMIN PANEL İŞLEMLERİ ===

@app.route('/admin')
def admin_dashboard():
    return render_template_string(ADMIN_TEMPLATE, macs=DATA_STORE["macs"], channels=DATA_STORE["channels"], last_generated=DATA_STORE["last_generated"])

@app.route('/admin/generate-1000-macs', methods=['POST'])
def generate_1000_macs():
    one_day_later = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    DATA_STORE["last_generated"] = []
    
    for _ in range(1000):
        rand_mac = f"00:1A:79:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}".upper()
        auto_id = f"AUTO-{len(DATA_STORE['macs']) + 1:05d}"
        
        DATA_STORE["macs"].append({
            "id": auto_id,
            "mac": rand_mac,
            "type": "Otomatik Üretilen Geçici Cihaz",
            "expiry": one_day_later
        })
        DATA_STORE["last_generated"].append(rand_mac)
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-mac', methods=['POST'])
def add_mac():
    mac = request.form.get('mac').strip().upper()
    device_type = request.form.get('type').strip()
    expiry = request.form.get('expiry')
    
    new_id = f"IPTV-{len(DATA_STORE['macs']) + 1:02d}"
    DATA_STORE["macs"].append({"id": new_id, "mac": mac, "type": device_type, "expiry": expiry})
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload-m3u', methods=['POST'])
def upload_m3u():
    file = request.files.get('m3u_file')
    if not file: return redirect(url_for('admin_dashboard'))

    content = file.read().decode('utf-8', errors='ignore')
    lines = content.split('\n')
    parsed_channels = []
    channel_counter = 1
    current_name, current_logo, current_genre = "", "", "Genel"

    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            logo_match = re.search(r'tvg-logo=["\'](.*?)["\']', line)
            if logo_match: current_logo = logo_match.group(1)
            group_match = re.search(r'group-title=["\'](.*?)["\']', line)
            if group_match: current_genre = group_match.group(1)
            if ',' in line:
                current_name = line.split(',', 1)[1].strip()
        elif line.startswith('http://') or line.startswith('https://'):
            if current_name:
                parsed_channels.append({
                    "id": str(channel_counter),
                    "name": current_name,
                    "cmd": f"ffmpeg {line}",
                    "genre": current_genre,
                    "logo": current_logo
                })
                channel_counter += 1
                current_name, current_logo, current_genre = "", "", "Genel"

    if parsed_channels:
        DATA_STORE["channels"] = parsed_channels
    return redirect(url_for('admin_dashboard'))


# === PORTAL BAĞLANTI KATMANI (STALKER STANDARTLARI) ===

PORTAL_ROUTES = [
    '/c/', '/c/portal.php', '/portal.php', 
    '/stalker_portal/c/', '/stalker_portal/c/portal.php',
    '/server/load.php', '/c/server/load.php', '/stalker_portal/server/load.php'
]

def process_portal_request():
    action = request.args.get('action')
    req_type = request.args.get('type')
    
    # MAC Adresi Yakalama Alanı
    mac = request.args.get('mac') or request.cookies.get('mac') or request.headers.get('Authorization', '')
    if mac:
        mac = mac.replace("Bearer ", "").strip().upper()

    # Uygulama el sıkışma (Handshake / Auth Kontrolleri)
    if not action or action == 'handshake':
        return jsonify({"js": {"token": "iptv_session_secure_token_key", "random": "123456", "status": "1"}})

    if action == 'get_localization':
        return jsonify({"js": {"result": {"language": "en", "country": "US"}}})

    if action == 'get_profile':
        # Cihaz yetkilendirmesi esnetildi (Eğer veritabanı boşsa veya test ediyorsan direkt izin verir)
        cleaned_req_mac = mac.strip().upper() if mac else ""
        allowed_macs = {m["mac"].strip().upper(): m for m in DATA_STORE["macs"]}
        
        # Eğer hiç MAC eklenmemişse test kolaylığı için izin ver, eklenmişse doğrula
        if not DATA_STORE["macs"] or cleaned_req_mac in allowed_macs:
            return jsonify({
                "js": {
                    "id": "1",
                    "name": "STB Emulator Client",
                    "status": "1",
                    "banned": "0",
                    "mac": cleaned_req_mac,
                    "ver": "0.2.x"
                }
            })
        return jsonify({"js": {"banned": "1", "status": "0", "msg": "Access Denied"}}), 403

    if action == 'get_ordered_list':
        if req_type == 'vod':
            return jsonify({"js": []})
        else:
            genres_set = list(set([ch["genre"] for ch in DATA_STORE["channels"]]))
            genres = []
            for i, g in enumerate(genres_set, 1):
                genres.append({"id": str(i), "title": g, "alias": g, "censored": "0"})
            return jsonify({"js": genres})

    # === KRİTİK ALAN: SAYFALAMA DESTEKLİ KANAL ÇEKİMİ ===
    if action == 'get_all_channels':
        # Uygulama sayfa bazlı istiyorsa limit uygula, istemiyorsa emülatör çökmesin diye max 1000 kanal dön
        try:
            p = int(request.args.get('p', 0))
        except:
            p = 0
            
        page_size = 500  # Cihazın tek seferde rahatça işleyebileceği kanal sayısı
        start_offset = p * page_size
        end_offset = start_offset + page_size
        
        target_channels = DATA_STORE["channels"][start_offset:end_offset] if DATA_STORE["channels"] else []
        
        stb_channels = []
        for idx, ch in enumerate(target_channels, start_offset + 1):
            stb_channels.append({
                "id": str(ch["id"]),
                "name": ch["name"],
                "cmd": ch["cmd"],
                "logo": ch["logo"],
                "tvg_id": f"tvg_{ch['id']}",
                "number": str(idx),
                "type": "itv",
                "status": "1",
                "hd": "1",
                "is_stb": "1",
                "lock": "0",
                "fav": 0
            })
            
        return jsonify({
            "js": {
                "data": stb_channels, 
                "selected_item": 0, 
                "total_items": len(DATA_STORE["channels"])
            }
        })

    return jsonify({"js": []})

for route in PORTAL_ROUTES:
    app.add_url_rule(route, endpoint=f"route_{route.replace('/', '_').replace('.', '_')}", view_func=process_portal_request, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
