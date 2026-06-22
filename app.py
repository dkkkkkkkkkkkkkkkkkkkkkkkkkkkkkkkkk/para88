import os
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, session, render_template_string, jsonify

app = Flask(__name__)
app.secret_key = "kozmos55_gizli_anahtar_9988"

# --- VERİTABANI YAPILANDIRMASI ---
def init_db():
    conn = sqlite3.connect('iptv.db')
    cursor = conn.cursor()
    # Kullanıcılar tablosuna 'expiry_date' (bitiş tarihi) alanı eklendi
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       username TEXT UNIQUE, 
                       password TEXT, 
                       expiry_date TEXT)''')
    
    # Kanallar tablosu
    cursor.execute('''CREATE TABLE IF NOT EXISTS channels 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, 
                       url TEXT, 
                       category TEXT)''')
    
    # Varsayılan yönetici hesabı kontrolü
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, expiry_date) VALUES ('admin', 'admin123', 'Sınırsız')")
        
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    conn = sqlite3.connect('iptv.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- HTML ŞABLONLARI (TEK DOSYADA TOPLAMAK İÇİN STRING OLARAK TANIMLANDI) ---

LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kozmos IPTV - Giriş</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #0a0a0a; color: #00ffcc; font-family: monospace; }
        .login-card { background: #141414; border: 1px solid #00ffcc; border-radius: 10px; box-shadow: 0 0 15px #00ffcc; }
        .form-control { background: #222; border: 1px solid #333; color: #fff; }
        .form-control:focus { background: #222; color: #fff; border-color: #00ffcc; box-shadow: 0 0 5px #00ffcc; }
        .btn-cyber { background: transparent; border: 1px solid #00ffcc; color: #00ffcc; }
        .btn-cyber:hover { background: #00ffcc; color: #000; box-shadow: 0 0 10px #00ffcc; }
    </style>
</head>
<body class="d-flex align-items-center justify-content-center vh-100">
    <div class="card login-card p-4" style="width: 22rem;">
        <h3 class="text-center mb-4">KOZMOS IPTV</h3>
        {% if error %}
            <div class="alert alert-danger py-2 text-center" style="background:#300; border:1px solid #f00; color:#fff;">{{ error }}</div>
        {% endif %}
        <form action="/" method="POST">
            <div class="mb-3">
                <label class="form-label">Kullanıcı Adı</label>
                <input type="text" name="username" class="form-control" required autocomplete="off">
            </div>
            <div class="mb-3">
                <label class="form-label">Şifre</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-cyber w-100 mt-2">GİRİŞ YAP</button>
        </form>
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
    <title>Kozmos Player</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://vjs.zencdn.net/7.20.3/video-js.css" rel="stylesheet" />
    <script src="https://vjs.zencdn.net/7.20.3/video.min.js"></script>
    <style>
        body { background-color: #0d0d0d; color: #fff; font-family: sans-serif; }
        .sidebar { background: #141414; border-right: 1px solid #222; height: 100vh; overflow-y: auto; }
        .cat-btn { background: #222; color: #aaa; border: none; text-align: left; margin-bottom: 5px; width: 100%; padding: 10px; border-radius: 5px;}
        .cat-btn.active, .cat-btn:hover { background: #00ffcc; color: #000; font-weight: bold; }
        .channel-item { background: #1a1a1a; border: 1px solid #333; cursor: pointer; transition: 0.2s; margin-bottom: 8px;}
        .channel-item:hover { border-color: #00ffcc; background: #222; }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- Sol Menü: Kategoriler -->
            <div class="col-md-3 sidebar p-3">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-info m-0">Kozmos Player</h5>
                    <div>
                        {% if session['user'] == 'admin' %}
                            <a href="/admin" class="btn btn-sm btn-warning me-1">Panel</a>
                        {% endif %}
                        <a href="/logout" class="btn btn-sm btn-danger">Çıkış</a>
                    </div>
                </div>
                <div class="mb-2 text-secondary small">Hesap Bitiş: <span class="text-warning">{{ expiry }}</span></div>
                <hr style="border-color: #333;">
                <a href="/index?category=Hepsi" class="btn cat-btn {% if current_category == 'Hepsi' %}active{% endif %}">📺 Tüm Kanallar</a>
                {% for cat in categories %}
                <a href="/index?category={{ cat.category }}" class="btn cat-btn {% if current_category == cat.category %}active{% endif %}">📁 {{ cat.category }}</a>
                {% endfor %}
            </div>

            <!-- Sağ Alan: Video Oynatıcı ve Kanal Listesi -->
            <div class="col-md-9 p-4">
                <div class="row">
                    <!-- Oynatıcı Ekranı -->
                    <div class="col-12 mb-4">
                        <div class="ratio ratio-16x9 bg-black rounded border border-secondary">
                            <video id="my-video" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" data-setup='{}'>
                                <source id="video-source" src="" type="application/x-mpegURL">
                            </video>
                        </div>
                        <h4 id="playing-title" class="mt-3 text-success">Lütfen izlemek istediğiniz kanalı seçin...</h4>
                    </div>

                    <!-- Kanallar Listesi -->
                    <div class="col-12">
                        <h5>Kanallar ({{ current_category }})</h5>
                        <div class="row">
                            {% for channel in channels %}
                            <div class="col-md-4">
                                <div class="card channel-item p-3" onclick="changeChannel('{{ channel.url }}', '{{ channel.name }}')">
                                    <div class="fw-bold text-white">{{ channel.name }}</div>
                                    <small class="text-muted">{{ channel.category }}</small>
                                </div>
                            </div>
                            {% endfor %}
                        </div>
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
            document.getElementById('playing-title').innerText = "Oynatılıyor: " + name;
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
    <title>Yönetim Paneli</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #121212; color: #fff; font-family: monospace; }
        .card-custom { background: #1c1c1c; border: 1px solid #333; border-radius: 8px; }
        .text-green { color: #00ff66 !important; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom pb-3">
            <h1 class="text-warning">⚙️ KOZMOS ADMIN PANEL</h1>
            <a href="/index" class="btn btn-outline-info">Oyuncuya Dön</a>
        </div>

        {% if msg %}
            <div class="alert alert-success bg-dark text-green border-success p-2 text-center mb-4">{{ msg }}</div>
        {% endif %}

        <div class="row">
            <!-- 1. KULLANICI ÜRETME -->
            <div class="col-md-6 mb-4">
                <div class="card card-custom p-4 h-100">
                    <h3 class="text-info border-bottom pb-2">👤 Kullanıcı Üret</h3>
                    <form method="POST">
                        <input type="hidden" name="action" value="add_user">
                        <div class="mb-3">
                            <label class="form-label">Kullanıcı Adı</label>
                            <input type="text" name="username" class="form-control bg-dark text-white border-secondary" required autocomplete="off">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Şifre</label>
                            <input type="text" name="password" class="form-control bg-dark text-white border-secondary" required autocomplete="off">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Bitiş Tarihi (Örn: 2026-12-31 veya Sınırsız)</label>
                            <input type="text" name="expiry_date" class="form-control bg-dark text-white border-secondary" placeholder="YYYY-MM-DD" value="Sınırsız" required>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Üret</button>
                    </form>
                </div>
            </div>

            <!-- 2. KANAL EKLEME -->
            <div class="col-md-6 mb-4">
                <div class="card card-custom p-4 h-100">
                    <h3 class="text-info border-bottom pb-2">📺 Kanal Yönetimi</h3>
                    <form method="POST">
                        <input type="hidden" name="action" value="add_channel">
                        <div class="mb-3">
                            <label class="form-label">Kanal Adı</label>
                            <input type="text" name="name" class="form-control bg-dark text-white border-secondary" required placeholder="Örn: TRT 1">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">M3U8 Yayın Linki</label>
                            <input type="url" name="url" class="form-control bg-dark text-white border-secondary" required placeholder="http://.../live.m3u8">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Kategori</label>
                            <input type="text" name="category" class="form-control bg-dark text-white border-secondary" required placeholder="Örn: Spor, Ulusal, Sinema">
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Kaydet</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <!-- MEVCUT KULLANICILAR VE SİLME -->
            <div class="col-md-6 mb-4">
                <h3>Kayıtlı Kullanıcılar</h3>
                <div class="table-responsive">
                    <table class="table table-dark table-striped align-middle">
                        <thead>
                            <tr><th>Kullanıcı</th><th>Şifre</th><th>Bitiş Tarihi</th><th>İşlem</th></tr>
                        </thead>
                        <tbody>
                            {% for u in users %}
                            <tr>
                                <td>{{ u.username }}</td>
                                <td>{{ u.password }}</td>
                                <td><span class="text-warning">{{ u.expiry_date }}</span></td>
                                <td>
                                    {% if u.username != 'admin' %}
                                    <a href="/delete_user/{{ u.id }}" class="btn btn-sm btn-danger" onclick="return confirm('Bu kullanıcıyı kaldırmak istediğinize emin misiniz?')">Kaldır</a>
                                    {% else %}
                                    <span class="badge bg-secondary">Sistem</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- MEVCUT KANALLAR VE SİLME -->
            <div class="col-md-6 mb-4">
                <h3>Ekli Kanallar</h3>
                <div class="table-responsive" style="max-height: 400px; overflow-y: auto;">
                    <table class="table table-dark table-striped align-middle">
                        <thead>
                            <tr><th>Kanal Adı</th><th>Kategori</th><th>İşlem</th></tr>
                        </thead>
                        <tbody>
                            {% for c in channels %}
                            <tr>
                                <td>{{ c.name }}</td>
                                <td><span class="badge bg-info">{{ c.category }}</span></td>
                                <td>
                                    <a href="/delete_channel/{{ c.id }}" class="btn btn-sm btn-danger" onclick="return confirm('Kanalı silmek istediğinize emin misiniz?')">Sil</a>
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
'''

# --- BACKEND MANTIĞI VE ROTALAR ---

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
            # Hesap bitiş tarihi kontrolü (Admin hariç)
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
            expiry_date = request.form['expiry_date']
            try:
                conn.execute('INSERT INTO users (username, password, expiry_date) VALUES (?, ?, ?)', 
                             (username, password, expiry_date))
                conn.commit()
                msg = "KAYDEDİLDİ" # Yeşil renkte gösterilecek mesaj
            except sqlite3.IntegrityError:
                msg = "Hata: Bu kullanıcı adı zaten mevcut!"
                
        elif action == 'add_channel':
            name = request.form['name']
            url = request.form['url']
            category = request.form['category']
            conn.execute('INSERT INTO channels (name, url, category) VALUES (?, ?, ?)', (name, url, category))
            conn.commit()
            msg = "KAYDEDİLDİ"
            
    users = conn.execute('SELECT * FROM users').fetchall()
    channels = conn.execute('SELECT * FROM channels').fetchall()
    conn.close()
    
    return render_template_string(ADMIN_HTML, users=users, channels=channels, msg=msg)

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

