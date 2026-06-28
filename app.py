from flask import Flask, request, jsonify, make_response, render_template_string, redirect, url_for
import re
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# === CANLI VERİTABANI (BELLEK ÜZERİNDE) ===
DATA_STORE = {
    "macs": [
        {"id": "ATT-01", "mac": "00:1A:79:A1:2B:3C", "type": "MAG / STB Emulator", "expiry": "2027-06-28"}
    ],
    "last_generated": [],  # Son üretilen 100 MAC'i kopyalamak için hafıza odası
    "channels": [
        {"id": "1", "name": "AZTV", "cmd": "ffmpeg http://flussonic.izone.az:80/aztv/mono.m3u8", "genre": "Azərbaycan", "logo": "https://i.postimg.cc/sg126ZT1/a.png"},
        {"id": "2", "name": "İCTİMAİ TV", "cmd": "ffmpeg http://flussonic.izone.az:80/ictimaitv/mono.m3u8", "genre": "Azərbaycan", "logo": "https://i.postimg.cc/3wvx7Q5T/ITV-Azerbaijan-Logo.png"},
        {"id": "3", "name": "CBC SPORT", "cmd": "ffmpeg http://176.65.146.189:8701/play/a09h", "genre": "Sports", "logo": "https://i.postimg.cc/3w4FTNxx/CBC-Sport-TV-loqo.png"},
        {"id": "4", "name": "Yeşilçam", "cmd": "ffmpeg https://catcast-bana-sor.biz-az.workers.dev/index.m3u8?id=by-kerimoff-yesilcam.m3u8", "genre": "Türkiye", "logo": "https://i.postimg.cc/yxsJGXn3/In-Shot-20260619-205118789.png"}
    ]
}

# === ANADOLU TURKEY TAYFASI SİBER PANEL TEMASI ===
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[ ANADOLU TURKEY TAYFASI ]</title>
    <style>
        body { background: #05070b; color: #d1d5db; font-family: 'Courier New', monospace; padding: 20px; margin:0; }
        header { border-bottom: 2px solid #ff3b30; padding-bottom: 10px; margin-bottom: 25px; text-shadow: 0 0 8px #ff3b30; }
        pre { color: #ff3b30; font-size: 0.75rem; margin: 0 0 15px 0; font-weight: bold; line-height: 1.2; }
        h1 { margin: 0; font-size: 1.4rem; color: #ffffff; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 25px; }
        .box { background: #0b0e14; border: 1px solid #1f2937; padding: 20px; border-radius: 6px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        h2 { color: #38bdf8; font-size: 1.1rem; margin-top: 0; border-bottom: 1px solid #1f2937; padding-bottom: 8px; }
        input, select, button { width: 100%; padding: 12px; margin-bottom: 12px; background: #05070b; border: 1px solid #374151; color: #fff; border-radius: 4px; box-sizing: border-box; font-family: monospace; }
        input:focus, select:focus { border-color: #38bdf8; outline: none; }
        button { border-color: #ff3b30; color: #ff3b30; font-weight: bold; cursor: pointer; background: transparent; transition: all 0.3s; }
        button:hover { background: rgba(255,59,48,0.1); box-shadow: 0 0 10px rgba(255,59,48,0.2); }
        .btn-m3u { border-color: #38bdf8; color: #38bdf8; }
        .btn-m3u:hover { background: rgba(56,189,248,0.1); box-shadow: 0 0 10px rgba(56,189,248,0.2); }
        .btn-generator { border-color: #a855f7; color: #a855f7; font-size: 1rem; }
        .btn-generator:hover { background: rgba(168,85,247,0.1); box-shadow: 0 0 10px rgba(168,85,247,0.2); }
        .btn-copy { border-color: #10b981; color: #10b981; font-size: 1rem; }
        .btn-copy:hover { background: rgba(16,185,129,0.1); box-shadow: 0 0 10px rgba(16,185,129,0.2); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #1f2937; font-size: 0.85rem; }
        th { background: #111827; color: #38bdf8; }
        .badge { padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; background: rgba(56,189,248,0.15); color: #38bdf8; }
        .badge-temp { padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; background: rgba(168,85,247,0.15); color: #a855f7; }
        .channel-logo { width: 35px; height: 35px; object-fit: contain; vertical-align: middle; background: #000; border-radius: 4px; border: 1px solid #1f2937; }
        .textarea-hidden { position: absolute; left: -9999px; }
    </style>
    <script>
        function copyToClipboard() {
            var copyText = document.getElementById("macClipboardSource");
            if (copyText.value.trim() === "") {
                alert("Henüz yeni MAC üretilmedi veya kopyalanacak veri yok!");
                return;
            }
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            document.execCommand("copy");
            alert("Son üretilen 100 MAC adresi başarıyla panoya kopyalandı! İstediğin yere yapıştırabilirsin.");
        }
    </script>
</head>
<body>
    <header>
        <pre>
 █▄▄ █▄░█ █▀█ █▀▄ █▀█ █░░ █░█   ▀█▀ █░█ █▀█ █▄░█ █▀▀ █▄█   ▀█▀ ▄▀█ █▀█ █▀▀ ▄▀█ █▀█ █
 █▄█ █░▀█ █▀█ █▄▀ █▄█ █▄▄ █▄█   ░█░ █▄█ █▀▄ █░▀█ █▄▄ ░█░   ░█░ █▀█ █▀▀ █▄▄ █▀█ █▀▄ ▄
        </pre>
        <h1>[ ATT // STALKER CORE PORTAL GATEWAY ]</h1>
    </header>

    <!-- OTOMATİK 100'LÜ MAC ÜRETİCİ VE KOPYALAYICI -->
    <div class="box" style="border-color: #a855f7;">
        <h2>[⚡] Otomatik MAC Adresi Üretim & Kopyalama İstasyonu (100 ADET / 1 GÜNLÜK)</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <form action="/admin/generate-100-macs" method="POST" style="margin: 0;">
                <button type="submit" class="btn-generator">⚡ 100 ADET RASTGELE MAC ÜRET (1 GÜNLÜK)</button>
            </form>
            <button onclick="copyToClipboard()" class="btn-copy">📋 SON ÜRETİLEN 100 ADETİ KOPYALA</button>
        </div>
        <textarea id="macClipboardSource" class="textarea-hidden">{% for m in last_generated %}{{ m }}{{"\n"}}{% endfor %}</textarea>
    </div>

    <div class="grid">
        <!-- MAC ENJEKSİYON ALANI -->
        <div class="box">
            <h2>[+] Manuel MAC Adresi Yetkilendir</h2>
            <form action="/admin/add-mac" method="POST">
                <input type="text" name="mac" placeholder="00:1A:79:XX:XX:XX" required>
                <input type="text" name="type" placeholder="Cihaz Tipi / Profil Adı" required>
                <label style="font-size:0.8rem; color:#9ca3af; display:block; margin-bottom:5px;">Sistem Bitiş Tarihi:</label>
                <input type="date" name="expiry" required>
                <button type="submit">SİSTEME ENJEKTE ET</button>
            </form>
        </div>

        <!-- OTOMATİK M3U YÜKLEME ALANI -->
        <div class="box">
            <h2>[↑] M3U Playlist Otomasyonu (Kanalları Ayıklar)</h2>
            <form action="/admin/upload-m3u" method="POST" enctype="multipart/form-data">
                <label style="font-size:0.8rem; color:#9ca3af; display:block; margin-bottom:10px;">
                    Listenizi (.m3u veya .txt) seçin, sistem otomatik olarak çözüp portala basacaktır:
                </label>
                <input type="file" name="m3u_file" accept=".m3u,.txt" required style="border: 1px dashed #38bdf8; padding:15px; text-align:center;">
                <button type="submit" class="btn-m3u">KANALLARI YÜKLE VE AKTİF ET</button>
            </form>
        </div>
    </div>

    <!-- MAC ADRESLERİ TABLOSU -->
    <div class="box" style="margin-bottom: 25px;">
        <h2>[=] Yetkilendirilmiş MAC Listesi (Toplam: {{ macs|length }})</h2>
        <div style="max-height: 400px; overflow-y: auto;">
            <table>
                <thead>
                    <tr>
                        <th>SIRA ID</th>
                        <th>MAC ADRESİ</th>
                        <th>CİHAZ TIPI</th>
                        <th>EXPIRE DATE (BİTİŞ)</th>
                        <th>DURUM</th>
                    </tr>
                </thead>
                <tbody>
                    {% for m in macs %}
                    <tr>
                        <td>{{ m.id }}</td>
                        <td style="color:#ff3b30; font-weight:bold; font-size:0.95rem;">{{ m.mac.upper() }}</td>
                        <td>{{ m.type }}</td>
                        <td style="color:#38bdf8;">{{ m.expiry }}</td>
                        <td>
                            {% if "AUTO" in m.id %}
                            <span class="badge-temp">1 DAY AUTO</span>
                            {% else %}
                            <span class="badge">ACTIVE</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- KANALLAR TABLOSU -->
    <div class="box">
        <h2>[=] Yayındaki Kanallar (Toplam: {{ channels|length }})</h2>
        <div style="max-height: 400px; overflow-y: auto;">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>LOGO</th>
                        <th>KANAL ADI</th>
                        <th>KATEGORİ</th>
                    </tr>
                </thead>
                <tbody>
                    {% for c in channels %}
                    <tr>
                        <td>{{ c.id }}</td>
                        <td>
                            <img class="channel-logo" src="{{ c.logo }}" onerror="this.src='https://via.placeholder.com/35/000000/ff3b30?text=TV'">
                        </td>
                        <td style="color:#ffffff; font-weight:bold;">{{ c.name }}</td>
                        <td style="color:#9ca3af;">[{{ c.genre }}]</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

# === ADMIN PANEL MANTIK KATI ===

@app.route('/admin')
def admin_dashboard():
    return render_template_string(ADMIN_TEMPLATE, macs=DATA_STORE["macs"], channels=DATA_STORE["channels"], last_generated=DATA_STORE["last_generated"])

# === ⚡ 100 ADET 1 GÜNLÜK MAC ÜRETEN MUKEMMEL ROUTE ⚡ ===
@app.route('/admin/generate-100-macs', methods=['POST'])
def generate_100_macs():
    # Tam 1 gün (24 saat) sonrasını hesapla kanka
    one_day_later = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Kopyalama odasını her basışta tazele
    DATA_STORE["last_generated"] = []
    
    for _ in range(100):
        # Stalker standart başlangıcı 00:1A:79 + 3 çift rastgele hex grubu
        rand_mac = f"00:1A:79:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}:{random.randint(0x10, 0xEF):02X}".upper()
        auto_id = f"AUTO-{len(DATA_STORE['macs']) + 1:04d}"
        
        # Sunucu hafızasına enjekte et
        DATA_STORE["macs"].append({
            "id": auto_id,
            "mac": rand_mac,
            "type": "1-Day Auto Generated Device",
            "expiry": one_day_later
        })
        
        # Tek seferde toplu kopyalanabilmesi için o odaya da gönder
        DATA_STORE["last_generated"].append(rand_mac)
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/add-mac', methods=['POST'])
def add_mac():
    mac = request.form.get('mac').strip().upper()
    device_type = request.form.get('type').strip()
    expiry = request.form.get('expiry')
    
    new_id = f"ATT-{len(DATA_STORE['macs']) + 1:02d}"
    DATA_STORE["macs"].append({"id": new_id, "mac": mac, "type": device_type, "expiry": expiry})
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload-m3u', methods=['POST'])
def upload_m3u():
    file = request.files.get('m3u_file')
    if not file: return redirect(url_for('admin_dashboard'))

    content = file.read().decode('utf-8', errors='ignore')
    lines = content.split('\n')
    parsed_channels = []
    
    current_name, current_logo, current_genre = "", "", "Genel"
    channel_counter = 1

    for line in lines:
        line = line.strip()
        if line.startswith('#EXTINF:'):
            logo_match = re.search(r'tvg-logo=["\'](.*?)["\']', line)
            if logo_match: current_logo = logo_match.group(1)
            
            group_match = re.search(r'group-title=["\'](.*?)["\']', line)
            if group_match: current_genre = group_match.group(1)
            
            if ',' in line:
                current_name = line.split(',', 1)[1].replace('ᵏᵃᵑᵏᵃ', '').strip()
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


# === 🕵️‍♂️ ULTRA UYUMLU STALKER API KATI ===

@app.route('/c/', methods=['GET', 'POST'])
@app.route('/c/portal.php', methods=['GET', 'POST'])
def stalker_portal():
    action = request.args.get('action')
    req_type = request.args.get('type')
    mac = request.args.get('mac') or request.cookies.get('mac') or request.headers.get('Authorization','')
    
    if mac:
        mac = mac.replace("Bearer ", "").strip().upper()

    if not action:
        return jsonify({"js": {"status": "OK", "portal_name": "ANADOLU TURKEY TAYFASI"}})

    if action == 'handshake':
        return jsonify({
            "js": {
                "token": "att_secret_session_matrix_key",
                "random": "888888",
                "status": "1"
            }
        })

    if action == 'get_profile':
        allowed_macs = {m["mac"].upper(): m for m in DATA_STORE["macs"]}
        if mac and mac.upper() in allowed_macs:
            device = allowed_macs[mac.upper()]
            today = datetime.now().strftime('%Y-%m-%d')
            if device["expiry"] >= today:
                return jsonify({
                    "js": {
                        "id": "1",
                        "name": device["type"],
                        "status": "1",
                        "banned": "0",
                        "mac": mac,
                        "phone": "",
                        "pass": "",
                        "ver": "0.2.x"
                    }
                })
        return jsonify({"js": {"banned": "1", "status": "0", "msg": "Cihaz Yetkisiz veya Suresi Dolmus"}}), 403

    if action == 'get_ordered_list':
        if req_type == 'vod':
            return jsonify({"js": [{"id": "vod_att", "title": "ATT Sinema Arşivi", "alias": "movies"}]})
        else:
            genres_set = list(set([ch["genre"] for ch in DATA_STORE["channels"]]))
            genres = []
            for i, g in enumerate(genres_set, 1):
                genres.append({"id": str(i), "title": g, "alias": g, "censored": "0"})
            return jsonify({"js": genres})

    if action == 'get_all_channels':
        stb_channels = []
        for idx, ch in enumerate(DATA_STORE["channels"], 1):
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
                "selected_item": "0",
                "total_items": len(stb_channels)
            }
        })

    if action == 'get_vod_genres':
        return jsonify({"js": [{"id": "vod_att", "title": "ATT Sinema Arşivi"}]})

    return jsonify({"js": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

