from flask import Flask, request, jsonify, render_template_string, redirect, url_for
import sqlite3, requests, re
from datetime import datetime, timedelta

app = Flask(__name__)
DB_FILE = "xtream_system.db"
M3U_URL = "https://raw.githubusercontent.com/rideordie16/tv/main/tv2.m3u" 

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, status TEXT DEFAULT 'Active',
                exp_date INTEGER NOT NULL, created_at TEXT NOT NULL
            )
        """)
init_db()

def parse_m3u_channels(url):
    try:
        response = requests.get(url, timeout=10)
        lines = response.text.splitlines()
        channels, current = [], {}
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                name = re.search(r',([^,]+)$', line)
                logo = re.search(r'tvg-logo="([^"]+)"', line)
                group = re.search(r'group-title="([^"]+)"', line)
                current = {
                    "name": name.group(1).strip() if name -match else "Kanal",
                    "logo": logo.group(1) if logo else "",
                    "group": group.group(1) if group else "Canlı"
                }
            elif line.startswith("http") or line.startswith("rtmp"):
                if current:
                    current["url"] = line
                    channels.append(current)
                    current = {}
        return channels
    except: return []

ADMIN_TEMPLATE = """
<!DOCTYPE html><html><head><title>Xtream Panel</title>
<style>body{background:#0c0f12;color:#e2e8f0;font-family:sans-serif;padding:20px;}
.c{max-width:800px;margin:0 auto;background:#1e293b;padding:20px;border-radius:8px;}
input,select,button{background:#1e293b;border:1px solid #475569;color:#fff;padding:10px;margin:5px;border-radius:4px;}</style>
</head><body><div class="c"><h2>👤 Hesap Oluştur</h2>
<form action="/admin/create" method="POST">
<input type="text" name="username" placeholder="User" required>
<input type="text" name="password" placeholder="Pass" required>
<select name="duration"><option value="24h">24 Saat (Test)</option><option value="1m">1 Ay</option><option value="3m">3 Ay</option><option value="12m">12 Ay</option></select>
<button type="submit">Oluştur</button></form>
<h2>📋 Kullanıcılar</h2><table><tr><th>User</th><th>Pass</th><th>Bitiş</th><th>İşlem</th></tr>
{% for r in users %}<tr><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[6]}}</td><td><a href="/admin/delete/{{r[0]}}" style="color:red;">[Sil]</a></td></tr>{% endfor %}
</table></div></body></html>"""

@app.route('/admin')
def admin_index():
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.cursor().execute("SELECT * FROM users").fetchall()
        p = []
        for r in rows:
            d = list(r)
            d.append(datetime.fromtimestamp(r[4]).strftime('%Y-%m-%d %H:%M'))
            p.append(d)
    return render_template_string(ADMIN_TEMPLATE, users=p)

@app.route('/admin/create', methods=['POST'])
def admin_create():
    u, p, dur = request.form.get('username'), request.form.get('password'), request.form.get('duration')
    now = datetime.now()
    if dur == "24h": exp = now + timedelta(hours=24)
    elif dur == "1m": exp = now + timedelta(days=30)
    elif dur == "3m": exp = now + timedelta(days=90)
    else: exp = now + timedelta(days=365)
    with sqlite3.connect(DB_FILE) as conn:
        try: conn.cursor().execute("INSERT INTO users (username,password,exp_date,created_at) VALUES (?,?,?,?)",(u,p,int(exp.timestamp()),now.strftime('%Y-%m-%d'))), conn.commit()
        except: pass
    return redirect(url_for('admin_index'))

@app.route('/admin/delete/<int:uid>')
def admin_delete(uid):
    with sqlite3.connect(DB_FILE) as conn: conn.cursor().execute("DELETE FROM users WHERE id=?",(uid,)), conn.commit()
    return redirect(url_for('admin_index'))

@app.route('/player_api.php')
def xtream_api_engine():
    u, p, act = request.args.get('user'), request.args.get('password'), request.args.get('action')
    with sqlite3.connect(DB_FILE) as conn: res = conn.cursor().execute("SELECT exp_date FROM users WHERE username=? AND password=?",(u,p)).fetchone()
    if not res or int(datetime.now().timestamp()) > res[0]: return jsonify({"user_info":{"auth":0}}), 403
    ch = parse_m3u_channels(M3U_URL)
    if not act: return jsonify({"user_info":{"auth":1,"status":"Active","exp_date":str(res[0])},"server_info":{"url":request.host,"port":"80"}})
    cats = list(set([c['group'] for c in ch]))
    if act == "get_live_categories": return jsonify([{"category_id":str(i+1),"category_name":c,"parent_id":"0"} for i,c in enumerate(cats)])
    if act == "get_live_streams": return jsonify([{"num":i+1,"name":c['name'],"stream_id":i+1,"stream_icon":c['logo'],"category_id":str(cats.index(c['group'])+1),"direct_source":c['url']} for i,c in enumerate(ch)])
    return jsonify([])

@app.route('/get.php')
def get_m3u_output():
    u, p = request.args.get('user'), request.args.get('password')
    with sqlite3.connect(DB_FILE) as conn: res = conn.cursor().execute("SELECT exp_date FROM users WHERE username=? AND password=?",(u,p)).fetchone()
    if not res or int(datetime.now().timestamp()) > res[0]: return "Hata", 403
    ch = parse_m3u_channels(M3U_URL)
    out = "#EXTM3U\n"
    for c in ch: out += f'#EXTINF:-1 tvg-logo="{c["logo"]}" group-title="{c["group"]}",{c["name"]}\n{c["url"]}\n'
    return out, 200, {'Content-Type':'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)