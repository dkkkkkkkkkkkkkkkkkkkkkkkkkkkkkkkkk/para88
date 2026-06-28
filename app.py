from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import re
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# === MERKEZİ IPTV VERİ DEPOSU ===
DATA_STORE = {
    "macs": [],
    "last_generated": [],  
    "channels": []         
}

VALID_TOKEN = "iptv_session_secure_token_key"

# === [ PROFESYONEL IPTV YÖNETİM PANELİ TASARIMI ] ===
ADMIN_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IPTV Stalker Portal Gateway Management</title>
    <style>
        :root {
            --bg-main: #0b0f19; --bg-card: #131a2c; --border-color: #22314d;
            --text-primary: #f8fafc; --text-secondary: #94a3b8; --brand-blue: #2563eb;
            --brand-blue-hover: #1d4ed8; --action-green: #10b981; --action-purple: #7c3aed; --accent-red: #ef4444;
        }
        body { background: var(--bg-main); color: var(--text-primary); font-family: 'Segoe UI', sans-serif; padding: 30px; margin: 0; }
        .container { max-width: 1400px; margin: 0 auto; }
        header { border-bottom: 1px solid var(--border-color); padding-bottom: 20px; margin-bottom: 30px; }
        h1 { margin: 0; font-size: 1.7rem; color: #ffffff; }
        h1 span { color: var(--brand-blue); }
        .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 25px; margin-bottom: 30px; }
        .box { background: var(--bg-card); border: 1px solid var(--border-color); padding: 24px; border-radius: 12px; }
        h2 { color: #ffffff; font-size: 1.2rem; margin-top: 0; padding-bottom: 12px; border-bottom: 1px solid var(--border-color); }
        input, select, button { width: 100%; padding: 12px; background: #090d16; border: 1px solid var(--border-color); color: #fff; border-radius: 8px; box-sizing: border-box; }
        button { background: var(--brand-blue); border: none; font-weight: 600; cursor: pointer; margin-top: 5px; }
        button:hover { background: var(--brand-blue-hover); }
        .btn-m3u { background: transparent; border: 1px solid var(--brand-blue); color: var(--brand-blue); }
        .btn-generator { background: var(--action-purple); }
        .btn-copy { background: var(--action-green); }
        .table-wrapper { max-height: 400px; overflow-y: auto; border: 1px solid var(--border-color); border-radius: 8px; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td { padding: 12px; font-size: 0.9rem; border-bottom: 1px solid var(--border-color); }
        th { background: #0c1220; color: var(--text-secondary); position: sticky; top: 0; }
        .channel-logo { width: 35px; height: 35px; object-fit: contain; background: #000; border-radius: 6px; }
        .textarea-hidden { position: absolute; left: -9999px; }
    </style>
    <script>
        function copyToClipboard() {
            var copyText = document.getElementById("macClipboardSource");
            if (copyText.value.trim() === "") { alert("Önce MAC üretin!"); return; }
            copyText.select(); document.execCommand("copy"); alert("1000 Adet MAC kopyalandı!");
        }
    </script>
</head>
<body>
    <div class="container">
        <header>
            <h1>IPTV <span>//</span> STALKER PORTAL GATEWAY MASTER</h1>
            <p style="color: var(--text-secondary); margin: 5px 0 0 0;">Yüklenen Toplam Kanal Sayısı: {{ channels|length }}</p>
        </header>

        <div class="box" style="margin-bottom: 30px; border-color: var(--action-purple);">
            <h2>Otomatik 1000 MAC Üretim Merkezi</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <form action="/admin/generate-1000-macs" method="POST"><button type="submit" class="btn-generator">⚡ 1000 ADET MAC ÜRET</button></form>
                <button onclick="copyToClipboard()" class="btn-copy">📋 LİSTEYİ KOPYALA</button>
            </div>
            <textarea id="macClipboardSource" class="textarea-hidden">{% for m in last_generated %}{{ m }}{{"\n"}}{% endfor %}</textarea>
        </div>

        <div class="grid-2">
            <div class="box">
                <h2>Manuel MAC Ekle</h2>
                <form action="/admin/add-mac" method="POST">
                    <input type="text" name="mac" placeholder="00:1A:79:XX:XX:XX" required style="margin-bottom: 10px;">
                    <input type="text" name="type" placeholder="STB Emulator" required style="margin-bottom: 10px;">
                    <input type="date" name="expiry" required style="margin-bottom: 10px;">
                    <button type="submit">CİHAZI YETKİLENDİR</button>
                </form>
            </div>
            <div class="box">
                <h2>M3U Yükle</h2>
                <form action="/admin/upload-m3u" method="POST" enctype="multipart/form-data">
                    <input type="file" name="m3u_file" accept=".m3u,.txt" required style="margin-bottom: 20px; padding: 20px; border: 1px dashed var(--brand-blue);">
                    <button type="submit" class="btn-m3u">PLAYLISTİ AKTİF ET</button>
                </form>
            </div>
        </div>

        <div class="grid-2">
            <div class="box">
                <h2>Cihazlar ({{ macs|length }})</h2>
                <div class="table-wrapper">
                    <table>
                        <thead><tr><th>MAC</th><th>TIPI</th><th>VADE</th></tr></thead>
                        <tbody>
                            {% for m in macs %}
                            <tr><td style="color:var(--accent-red); font-weight:bold;">{{ m.mac }}</td><td>{{ m.type }}</td><td>{{ m.expiry }}</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="box">
                <h2>Kanallar (Gösterilen: {{ channels[:100]|length }} / {{ channels|length }})</h2>
                <div class="table-wrapper">
                    <table>
                        <thead><tr><th>ID</th><th>LOGO</th><th>AD</th><th>KATEGORİ</th></tr></thead>
                        <tbody>
                            {% for c in channels[:100] %}
                            <tr><td>{{ c.id }}</td><td><img class="channel-logo" src="{{ c.logo }}"></td><td>{{ c.name }}</td><td>{{ c.genre }}</td></tr>
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

# === ADMIN ENDPOINTS ===
@app.route('/admin')
def admin_dashboard():
    return render_template_string(ADMIN_TEMPLATE, macs=DATA_STORE["macs"], channels=DATA_STORE["channels"], last_generated=DATA_STORE["last_generated"])

@app.route('/admin/generate-1000-macs', methods=['POST'])
def generate_1000_macs():
    one_day_later = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    DATA_STORE["last_generated"] = []
    for _ in range(1000):
        rand_mac = f"00:1A:79:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}".upper()
        DATA_STORE["macs"].append({"mac": rand_mac, "type": "Geçici Cihaz", "expiry": one_day_later})
        DATA_STORE["last_generated"].append(rand_mac)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-mac', methods=['POST'])
def add_mac():
    mac = request.form.get('mac').strip().upper()
    DATA_STORE["macs"].append({"mac": mac, "type": request.form.get('type'), "expiry": request.form.get('expiry')})
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload-m3u', methods=['POST'])
def upload_m3u():
    file = request.files.get('m3u_file')
    if not file: return redirect(url_for('admin_dashboard'))
    content = file.read().decode('utf-8', errors='ignore')
    
    parsed_channels = []
    channel_counter = 1
    current_name, current_logo, current_genre = "", "", "Genel"
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('#EXTINF:'):
            logo_match = re.search(r'tvg-logo=["\'](.*?)["\']', line)
            if logo_match: current_logo = logo_match.group(1)
            group_match = re.search(r'group-title=["\'](.*?)["\']', line)
            if group_match: current_genre = group_match.group(1)
            if ',' in line: current_name = line.split(',', 1)[1].strip()
        elif line.startswith('http://') or line.startswith('https://'):
            if current_name:
                parsed_channels.append({
                    "id": str(channel_counter), "name": current_name,
                    "cmd": f"ffmpeg {line}", "genre": current_genre, "logo": current_logo
                })
                channel_counter += 1
                current_name, current_logo, current_genre = "", "", "Genel"
                
    if parsed_channels: DATA_STORE["channels"] = parsed_channels
    return redirect(url_for('admin_dashboard'))


# === PORTAL BAĞLANTI KATMANI (STALKER PROTOKOLÜ) ===
PORTAL_ROUTES = [
    '/c/', '/c/portal.php', '/portal.php', 
    '/server/load.php', '/c/server/load.php', '/stalker_portal/server/load.php'
]

def process_portal_request():
    action = request.args.get('action')
    req_type = request.args.get('type', '')
    
    # MAC Adresi yakalama
    mac = request.args.get('mac') or request.headers.get('Authorization', '')
    mac = mac.replace("Bearer ", "").strip().upper() if mac else ""

    # 1. El Sıkışma
    if not action or action == 'handshake':
        return jsonify({"js": {"token": VALID_TOKEN, "random": "123456", "status": "1"}})

    # 2. Dil/Bölge Ayarı
    if action == 'get_localization':
        return jsonify({"js": {"result": {"language": "en", "country": "US"}}})

    # 3. Profil Doğrulama (Hata Toleranslı Yapıldı)
    if action == 'get_profile':
        return jsonify({
            "js": {
                "id": "1", 
                "name": "Eren Premium Gateway", 
                "status": "1",
                "banned": "0", 
                "mac": mac, 
                "ver": "0.2.x",
                "active": 1
            }
        })

    # 4. Kategorileri Çekme
    if action == 'get_ordered_list':
        if req_type == 'vod':
            return jsonify({"js": []})
        
        genres_set = list(set([ch["genre"] for ch in DATA_STORE["channels"]])) if DATA_STORE["channels"] else ["Genel"]
        genres = []
        for i, g in enumerate(genres_set, 1):
            genres.append({"id": str(i), "title": g, "alias": g, "censored": "0"})
        return jsonify({"js": genres})

    # 5. KANALLARI LİSTELEME (Süper Kararlı Yapı)
    if action == 'get_all_channels':
        try:
            p = int(request.args.get('p', 0))
        except:
            p = 0
            
        page_size = 400  # MySTB emülatörün zaman aşımına uğramaması için ideal boyut
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
                "number": idx,
                "type": "itv",
                "status": 1,
                "hd": 1,
                "is_stb": 1,
                "lock": 0,
                "fav": 0
            })
            
        # Hem 'js' sarmalı hem de ham data sarmalı eklenerek tüm emülatörlerle tam uyum sağlandı
        response_data = {
            "data": stb_channels, 
            "selected_item": 0, 
            "total_items": len(DATA_STORE["channels"]),
            "max_page_items": page_size
        }
        return jsonify({"js": response_data, "data": stb_channels, "total_items": len(DATA_STORE["channels"])})

    return jsonify({"js": []})

for route in PORTAL_ROUTES:
    app.add_url_rule(route, endpoint=f"route_{route.replace('/', '_').replace('.', '_')}", view_func=process_portal_request, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

