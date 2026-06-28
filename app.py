from flask import Flask, request, jsonify, make_response, render_template_string, redirect, url_for
import re
from datetime import datetime

app = Flask(__name__)

# === MERKEZİ VERİTABANI (Bellek Üzerinde) ===
DATA_STORE = {
    "macs": [
        {"id": "KOZ-M01", "mac": "00:1A:79:A1:2B:3C", "type": "MAG 322", "status": "Active", "expiry": "2027-06-28"},
        {"id": "KOZ-M02", "mac": "00:1A:79:4F:89:DE", "type": "MAG 420", "status": "Active", "expiry": "2026-12-31"}
    ],
    "channels": [
        {"id": "1", "name": "AZTV", "cmd": "ffmpeg http://flussonic.izone.az:80/aztv/mono.m3u8", "genre": "Azərbaycan", "logo": "https://i.postimg.cc/sg126ZT1/a.png"}
    ]
}

# === ADMIN PANEL ARAYÜZÜ (HTML / CSS / JS) ===
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[ KOZMOS55 MASTER PORTAL ]</title>
    <style>
        body { background: #06070d; color: #e2e4ed; font-family: 'Courier New', monospace; padding: 20px; margin:0; }
        header { border-bottom: 2px solid #00ff66; padding-bottom: 10px; margin-bottom: 20px; box-shadow: 0 0 10px rgba(0,255,102,0.2); }
        h1 { color: #00ff66; margin: 0; font-size: 1.5rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .box { background: #0c0e17; border: 1px solid #1e2235; padding: 20px; border-radius: 4px; position: relative; }
        h2 { color: #00e5ff; font-size: 1.1rem; margin-top: 0; border-bottom: 1px solid #1e2235; padding-bottom: 8px; }
        input, select, button { width: 100%; padding: 12px; margin-bottom: 12px; background: #06070d; border: 1px solid #1e2235; color: #fff; border-radius: 4px; box-sizing: border-box; font-size: 0.9rem; }
        input:focus, select:focus { border-color: #00e5ff; outline: none; }
        button { border-color: #00ff66; color: #00ff66; font-weight: bold; cursor: pointer; background: transparent; transition: all 0.2s; }
        button:hover { background: rgba(0,255,102,0.1); box-shadow: 0 0 8px rgba(0,255,102,0.3); }
        .btn-m3u { border-color: #ffaa00; color: #ffaa00; }
        .btn-m3u:hover { background: rgba(255,170,0,0.1); box-shadow: 0 0 8px rgba(255,170,0,0.3); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #1e2235; font-size: 0.85rem; }
        th { background: rgba(30, 34, 53, 0.4); color: #00e5ff; }
        .badge { padding: 3px 6px; border-radius: 3px; font-weight: bold; font-size: 0.75rem; background: rgba(0,255,102,0.15); color: #00ff66; }
        .channel-logo { width: 30px; height: 30px; object-fit: contain; vertical-align: middle; margin-right: 8px; background: #000; border-radius: 3px; }
    </style>
</head>
<body>
    <header>
        <h1>[ KOZMOS55 // AUTOMATED STALKER MATRIX MULTI-PANEL ]</h1>
    </header>

    <div class="grid">
        <div class="box">
            <h2>[+] MAC Adresi Girişi & Yetkilendirme</h2>
            <form action="/admin/add-mac" method="POST">
                <input type="text" name="mac" placeholder="00:1A:79:XX:XX:XX" required>
                <input type="text" name="type" placeholder="Cihaz Modeli (MAG, Formuler, STB Emu)" required>
                
                <label style="font-size:0.8rem; color:#70758d; display:block; margin-bottom:5px;">Sistem Bitiş Tarihi (Expiration):</label>
                <input type="date" name="expiry" required>
                
                <button type="submit">CİHAZI SİSTEME EKLE</button>
            </form>
        </div>

        <div class="box">
            <h2>[↑] M3U / TXT Playlist Otomasyonu</h2>
            <form action="/admin/upload-m3u" method="POST" enctype="multipart/form-data">
                <label style="font-size:0.8rem; color:#70758d; display:block; margin-bottom:10px;">
                    Listenizi (.m3u veya .txt formatında) seçin ve tek tıkla tüm kanalları portala aktarın:
                </label>
                <input type="file" name="m3u_file" accept=".m3u,.txt" required style="border: 1px dashed #ffaa00; padding:20px; text-align:center;">
                <button type="submit" class="btn-m3u">KANALLARI AKTAR & YÜKLE</button>
            </form>
        </div>
    </div>

    <div class="box" style="margin-bottom: 20px;">
        <h2>[=] Portala Kayıtlı Güncel MAC Cihazları (Toplam: {{ macs|length }})</h2>
        <table>
            <thead>
                <tr>
                    <th>SIRA ID</th>
                    <th>MAC ADRESİ</th>
                    <th>CİHAZ TİPİ</th>
                    <th>BİTİŞ TARİHİ</th>
                    <th>DURUM</th>
                </tr>
            </thead>
            <tbody>
                {% for m in macs %}
                <tr>
                    <td>{{ m.id }}</td>
                    <td style="color:#00e5ff; font-weight:bold;">{{ m.mac.upper() }}</td>
                    <td>{{ m.type }}</td>
                    <td style="color:#ffaa00;">{{ m.expiry }}</td>
                    <td><span class="badge">ACTIVE</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="box">
        <h2>[=] Veritabanına Aktarılan Yayındaki Kanallar (Toplam: {{ channels|length }})</h2>
        <div style="max-height: 400px; overflow-y: auto;">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>LOGO</th>
                        <th>KANAL ADI</th>
                        <th>KATEGORİ</th>
                        <th>SOURCE URL (STREAM)</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in channels %}
                    <tr>
                        <td>{{ c.id }}</td>
                        <td>
                            {% if c.logo %}
                            <img class="channel-logo" src="{{ c.logo }}" onerror="this.src='https://via.placeholder.com/30/000000/00ff66?text=TV'">
                            {% else %}
                            <img class="channel-logo" src="https://via.placeholder.com/30/000000/00ff66?text=TV">
                            {% endif %}
                        </td>
                        <td style="color:#00ff66; font-weight:bold;">{{ c.name }}</td>
                        <td style="color:#ffaa00; font-size:0.8rem;">[{{ c.genre }}]</td>
                        <td style="color:#70758d; font-size:0.75rem;">{{ c.cmd }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# === ADMIN PANEL ROUTE VE PARSER İŞLEMLERİ ===

@app.route('/admin')
def admin_dashboard():
    return render_template_string(ADMIN_TEMPLATE, macs=DATA_STORE["macs"], channels=DATA_STORE["channels"])

@app.route('/admin/add-mac', methods=['POST'])
def add_mac():
    mac = request.form.get('mac').strip()
    device_type = request.form.get('type').strip()
    expiry = request.form.get('expiry') # HTML Date Picker'dan gelen YYYY-MM-DD tarihi
    
    new_id = f"KOZ-M{len(DATA_STORE['macs']) + 1:02d}"
    DATA_STORE["macs"].append({
        "id": new_id, 
        "mac": mac, 
        "type": device_type, 
        "status": "Active", 
        "expiry": expiry
    })
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload-m3u', methods=['POST'])
def upload_m3u():
    if 'm3u_file' not in request.files:
        return redirect(url_for('admin_dashboard'))
    
    file = request.files['m3u_file']
    if file.filename == '':
        return redirect(url_for('admin_dashboard'))

    content = file.read().decode('utf-8', errors='ignore')
    
    # M3U Parser Algoritması (Gelişmiş regex ile kanka.txt formatını çözer)
    lines = content.split('\n')
    parsed_channels = []
    
    current_name = ""
    current_logo = ""
    current_genre = "Genel"
    
    channel_counter = len(DATA_STORE["channels"]) + 1

    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            # Logo çekme alanı
            logo_match = re.search(r'tvg-logo=["\'](.*?)["\']', line)
            if logo_match:
                current_logo = logo_match.group(1)
            
            # Kategori (group-title) çekme alanı
            group_match = re.search(r'group-title=["\'](.*?)["\']', line)
            if group_match:
                current_genre = group_match.group(1)
            
            # Kanal ismi temizleme alanı (virgülden sonrasını alır, kanka taglerini ayıklar)
            if ',' in line:
                name_part = line.split(',', 1)[1]
                current_name = name_part.replace('ᵏᵃᵑᵏᵃ', '').strip()
                
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
                # Değişkenleri sıfırla
                current_name = ""
                current_logo = ""
                current_genre = "Genel"

    # Eğer geçerli kanallar bulunduysa ana listeye ekle
    if parsed_channels:
        DATA_STORE["channels"] = parsed_channels # Eski listeyi yenisiyle günceller

    return redirect(url_for('admin_dashboard'))


# === HAKİKİ MAG / STALKER PLAYER API ALTYAPISI ===

@app.route('/c/', methods=['GET', 'POST'])
@app.route('/c/portal.php', methods=['GET', 'POST'])
def stalker_portal():
    action = request.args.get('action')
    mac = request.args.get('mac') or request.cookies.get('mac')
    
    if action == 'handshake':
        return jsonify({"js": {"token": "kozmos55_secure_key", "random": "987654"}})

    if action == 'get_profile':
        # Canlı veritabanındaki kayıtlı ve süresi geçmemiş MAC kontrolü
        allowed_macs = {m["mac"].upper(): m for m in DATA_STORE["macs"]}
        if mac and mac.upper() in allowed_macs:
            device = allowed_macs[mac.upper()]
            # Tarih kontrolü yapıyoruz
            today = datetime.now().strftime('%Y-%m-%d')
            if device["expiry"] >= today:
                return jsonify({"js": {"id": "1", "name": device["type"], "status": "1", "banned": "0", "mac": mac}})
        return jsonify({"js": {"banned": "1", "status": "0"}}), 403

    if action == 'get_ordered_list':
        genres_set = list(set([ch["genre"] for ch in DATA_STORE["channels"]]))
        genres = [{"id": str(i+1), "title": g} for i, g in enumerate(genres_set)]
        return jsonify({"js": genres})

    if action == 'get_all_channels':
        stb_channels = []
        for idx, ch in enumerate(DATA_STORE["channels"], 1):
            stb_channels.append({
                "id": ch["id"],
                "name": ch["name"],
                "cmd": ch["cmd"],
                "logo": ch["logo"],
                "tvg_id": f"tvg_{idx}",
                "number": str(idx)
            })
        return jsonify({"js": {"data": stb_channels}})

    return jsonify({"js": {"status": "OK"}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
