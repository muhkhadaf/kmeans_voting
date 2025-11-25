from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import numpy as np
from db import init_db, get_db, close_db, execute_query
import json
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Ganti dengan secret key yang aman

# Set timezone untuk server (Indonesia)
SERVER_TIMEZONE = pytz.timezone('Asia/Jakarta')

def get_server_time():
    """Get current server time in Indonesia timezone"""
    return datetime.now(SERVER_TIMEZONE).replace(tzinfo=None)

def format_server_time(dt_string):
    """Convert datetime string to server timezone"""
    if dt_string:
        dt = datetime.fromisoformat(dt_string)
        return dt.replace(tzinfo=pytz.UTC).astimezone(SERVER_TIMEZONE).replace(tzinfo=None)
    return None

# Initialize database on startup
with app.app_context():
    init_db()

@app.teardown_appcontext
def close_db_connection(error):
    close_db(error)

# Voting Period Management Functions
def get_current_voting_period():
    """Get the currently active voting period"""
    current_time = get_server_time()
    return execute_query("""
        SELECT * FROM voting_periods 
        WHERE start_time <= %s AND end_time > %s AND status = 'active' AND manually_stopped = 0
        ORDER BY start_time DESC LIMIT 1
    """, (current_time, current_time), fetch='one')

def get_voting_period_status():
    """Get the status of voting periods"""
    current_time = get_server_time()
    
    # Check for active period
    active_period = get_current_voting_period()
    if active_period:
        return {
            'status': 'active',
            'period': active_period,
            'start_time': active_period[3],
            'end_time': active_period[4],
            'time_remaining': (active_period[4] - current_time).total_seconds()
        }
    
    # Check for scheduled period
    scheduled = execute_query("""
        SELECT * FROM voting_periods 
        WHERE start_time > %s AND status = 'scheduled'
        ORDER BY start_time ASC LIMIT 1
    """, (current_time,), fetch='one')
    
    if scheduled:
        return {
            'status': 'scheduled',
            'period': scheduled,
            'start_time': scheduled[3],
            'end_time': scheduled[4],
            'time_until_start': (scheduled[3] - current_time).total_seconds()
        }
    
    # Check for recently ended period
    ended = execute_query("""
        SELECT * FROM voting_periods 
        WHERE end_time <= %s OR manually_stopped = 1
        ORDER BY end_time DESC LIMIT 1
    """, (current_time,), fetch='one')
    
    if ended:
        return {
            'status': 'ended',
            'period': ended,
            'start_time': ended[3],
            'end_time': ended[4]
        }
    
    return {
        'status': 'none', 
        'period': None,
        'start_time': None,
        'end_time': None
    }

def is_voting_allowed():
    """Check if voting is currently allowed"""
    period_status = get_voting_period_status()
    return period_status['status'] == 'active'

# K-Means Algorithm Implementation
class KMeansCluster:
    def __init__(self, k=3, max_iters=100):
        self.k = k
        self.max_iters = max_iters
    
    def fit(self, data):
        # Initialize centroids randomly
        self.centroids = data[np.random.choice(data.shape[0], self.k, replace=False)]
        
        for _ in range(self.max_iters):
            # Assign points to closest centroid
            distances = np.sqrt(((data - self.centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)
            
            # Update centroids
            new_centroids = np.array([data[labels == i].mean(axis=0) for i in range(self.k)])
            
            # Check for convergence
            if np.allclose(self.centroids, new_centroids):
                break
                
            self.centroids = new_centroids
        
        return labels
    
    def get_cluster_stats(self, data, labels):
        stats = []
        for i in range(self.k):
            cluster_data = data[labels == i]
            if len(cluster_data) > 0:
                avg_score = np.mean(cluster_data)
                stats.append({
                    'cluster': i,
                    'count': len(cluster_data),
                    'avg_score': avg_score
                })
        
        # Sort by average score (highest first)
        stats.sort(key=lambda x: x['avg_score'], reverse=True)
        
        # Assign labels
        cluster_labels = ['Sangat Layak', 'Cukup Layak', 'Kurang Layak']
        for idx, stat in enumerate(stats):
            stat['label'] = cluster_labels[idx] if idx < len(cluster_labels) else f'Cluster {idx+1}'
        
        return stats

# Routes
@app.route('/')
def index():
    if 'admin_logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = execute_query(
            "SELECT * FROM admin WHERE username = %s", 
            (username,), 
            fetch='one'
        )
        
        if admin and check_password_hash(admin[2], password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin[0]
            session['admin_username'] = admin[1]
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get statistics
    total_anggota_result = execute_query("SELECT COUNT(*) FROM anggota", fetch='one')
    total_kandidat_result = execute_query("SELECT COUNT(*) FROM anggota WHERE status = 'kandidat'", fetch='one')
    total_users_result = execute_query("SELECT COUNT(*) FROM user", fetch='one')
    total_votes_result = execute_query("SELECT COUNT(*) FROM voting", fetch='one')
    
    total_anggota = total_anggota_result[0] if total_anggota_result else 0
    total_kandidat = total_kandidat_result[0] if total_kandidat_result else 0
    total_users = total_users_result[0] if total_users_result else 0
    total_votes = total_votes_result[0] if total_votes_result else 0
    
    stats = {
        'total_anggota': total_anggota,
        'total_kandidat': total_kandidat,
        'total_users': total_users,
        'total_votes': total_votes
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/anggota')
def anggota():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    members = execute_query("SELECT * FROM anggota ORDER BY nama", fetch=True)
    return render_template('anggota.html', members=members)

@app.route('/anggota/add', methods=['POST'])
def add_anggota():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    nama = request.form['nama']
    pendidikan = request.form['pendidikan']
    visi_misi = request.form['visi_misi']
    
    execute_query(
        """INSERT INTO anggota (nama, pendidikan, visi_misi) 
           VALUES (%s, %s, %s)""",
        (nama, pendidikan, visi_misi)
    )
    
    flash('Anggota berhasil ditambahkan!', 'success')
    return redirect(url_for('anggota'))

@app.route('/anggota/edit/<int:id>', methods=['POST'])
def edit_anggota(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    nama = request.form['nama']
    pendidikan = request.form['pendidikan']
    visi_misi = request.form['visi_misi']
    
    execute_query(
        """UPDATE anggota SET nama=%s, pendidikan=%s, visi_misi=%s WHERE id=%s""",
        (nama, pendidikan, visi_misi, id)
    )
    
    flash('Data anggota berhasil diupdate!', 'success')
    return redirect(url_for('anggota'))

@app.route('/anggota/delete/<int:id>')
def delete_anggota(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    execute_query("DELETE FROM anggota WHERE id = %s", (id,))
    flash('Anggota berhasil dihapus!', 'success')
    return redirect(url_for('anggota'))

@app.route('/analisis')
def analisis():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get members with rating count
    members = execute_query("""
        SELECT 
            a.id,
            a.nama,
            a.pendidikan,
            a.visi_misi,
            COUNT(p.id) as rating_count
        FROM anggota a
        LEFT JOIN penilaian p ON a.id = p.anggota_id
        GROUP BY a.id, a.nama, a.pendidikan, a.visi_misi
        ORDER BY a.nama
    """, fetch=True)
    return render_template('analisis.html', members=members)

@app.route('/run_kmeans', methods=['POST'])
def run_kmeans():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get average ratings for each member from user assessments
    members_ratings = execute_query("""
        SELECT 
            a.id,
            a.nama,
            AVG(p.keaktifan) as avg_keaktifan,
            AVG(p.kepemimpinan) as avg_kepemimpinan,
            AVG(p.pengalaman) as avg_pengalaman,
            AVG(p.disiplin) as avg_disiplin,
            AVG(p.komunikasi) as avg_komunikasi,
            COUNT(p.id) as rating_count
        FROM anggota a
        LEFT JOIN penilaian p ON a.id = p.anggota_id
        GROUP BY a.id, a.nama
        HAVING rating_count > 0
    """, fetch=True)
    
    if not members_ratings or len(members_ratings) < 3:
        flash('Minimal 3 anggota dengan penilaian diperlukan untuk analisis K-Means!', 'error')
        return redirect(url_for('analisis'))
    
    # Prepare data for clustering
    data = []
    member_ids = []
    
    for member in members_ratings:
        # member = (id, nama, avg_keaktifan, avg_kepemimpinan, avg_pengalaman, avg_disiplin, avg_komunikasi, rating_count)
        features = [member[2], member[3], member[4], member[5], member[6]]  # All average criteria
        data.append(features)
        member_ids.append(member[0])
    
    data = np.array(data, dtype=float)
    
    # Normalize data (0-100 scale) with safe division
    data_min = data.min(axis=0)
    data_max = data.max(axis=0)
    data_range = data_max - data_min
    
    # Avoid division by zero: if range is 0, keep original values
    data_range[data_range == 0] = 1
    
    data_normalized = (data - data_min) / data_range * 100
    
    # Run K-Means
    kmeans = KMeansCluster(k=3)
    labels = kmeans.fit(data_normalized)
    
    # Get cluster statistics
    cluster_stats = kmeans.get_cluster_stats(data_normalized, labels)
    
    # Update database with cluster assignments
    for i, member_id in enumerate(member_ids):
        execute_query(
            "UPDATE anggota SET cluster = %s WHERE id = %s",
            (int(labels[i]), member_id)
        )
    
    flash('Analisis K-Means berhasil dijalankan!', 'success')
    return redirect(url_for('hasil_analisis'))

@app.route('/hasil_analisis')
def hasil_analisis():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get members with cluster assignments and their average ratings
    members_data = execute_query("""
        SELECT 
            a.id,
            a.nama,
            a.pendidikan,
            a.cluster,
            AVG(p.keaktifan) as avg_keaktifan,
            AVG(p.kepemimpinan) as avg_kepemimpinan,
            AVG(p.pengalaman) as avg_pengalaman,
            AVG(p.disiplin) as avg_disiplin,
            AVG(p.komunikasi) as avg_komunikasi,
            COUNT(p.id) as rating_count
        FROM anggota a
        LEFT JOIN penilaian p ON a.id = p.anggota_id
        WHERE a.cluster IS NOT NULL
        GROUP BY a.id, a.nama, a.pendidikan, a.cluster
        ORDER BY a.cluster, a.nama
    """, fetch=True)
    
    # Group by cluster
    clusters = {}
    for member in members_data:
        cluster = member[3]  # cluster column
        if cluster not in clusters:
            clusters[cluster] = []
        clusters[cluster].append(member)
    
    # Calculate cluster statistics
    cluster_stats = []
    cluster_labels = ['Sangat Layak', 'Cukup Layak', 'Kurang Layak']
    
    for cluster_id in sorted(clusters.keys()):
        members_in_cluster = clusters[cluster_id]
        total_score = 0
        count = len(members_in_cluster)
        
        for member in members_in_cluster:
            # Calculate average score for each member (avg of 5 criteria)
            if member[4] is not None:  # Check if ratings exist
                score = (member[4] + member[5] + member[6] + member[7] + member[8]) / 5
                total_score += score
        
        avg_score = total_score / count if count > 0 else 0
        
        cluster_stats.append({
            'cluster_id': cluster_id,
            'label': cluster_labels[cluster_id] if cluster_id < len(cluster_labels) else f'Cluster {cluster_id}',
            'count': count,
            'avg_score': round(avg_score, 2),
            'members': members_in_cluster
        })
    
    # Sort by average score (highest first)
    cluster_stats.sort(key=lambda x: x['avg_score'], reverse=True)
    
    return render_template('hasil_analisis.html', cluster_stats=cluster_stats)

@app.route('/set_kandidat', methods=['POST'])
def set_kandidat():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    selected_members = request.form.getlist('selected_members')
    
    if not selected_members:
        flash('Pilih minimal 1 anggota untuk dijadikan kandidat!', 'error')
        return redirect(url_for('hasil_analisis'))
    
    # Reset all candidates first
    execute_query("UPDATE anggota SET status = 'anggota'")
    
    # Set selected members as candidates
    for member_id in selected_members:
        execute_query(
            "UPDATE anggota SET status = 'kandidat' WHERE id = %s",
            (member_id,)
        )
    
    flash(f'{len(selected_members)} kandidat berhasil ditetapkan!', 'success')
    return redirect(url_for('voting_page'))

# Voting Period Management Routes
@app.route('/voting_periods')
def voting_periods():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get all voting periods
    periods_data = execute_query("""
        SELECT * FROM voting_periods 
        ORDER BY created_at DESC
    """, fetch=True)
    
    # Convert tuple data to objects for template access
    periods = []
    if periods_data:
        for period_tuple in periods_data:
            # Get vote count for this period
            vote_count_result = execute_query("""
                SELECT COUNT(*) FROM voting WHERE voting_period_id = %s
            """, (period_tuple[0],), fetch='one')
            vote_count = vote_count_result[0] if vote_count_result else 0
            
            period_obj = {
                'id': period_tuple[0],
                'title': period_tuple[1],
                'description': period_tuple[2],
                'start_time': period_tuple[3] if period_tuple[3] else None,
                'end_time': period_tuple[4] if period_tuple[4] else None,
                'status': period_tuple[5],
                'created_at': period_tuple[6],
                'created_by': period_tuple[7],
                'manually_stopped': period_tuple[8],
                'stopped_at': period_tuple[9] if period_tuple[9] else None,
                'extended_count': period_tuple[10],
                'vote_count': vote_count
            }
            periods.append(period_obj)
    
    # Get current period status
    period_status = get_voting_period_status()
    
    # Prepare current_status for template
    current_status = None
    if period_status['status'] != 'none' and period_status['period']:
        current_period = period_status['period']
        current_status = {
            'status': period_status['status'],
            'period_id': current_period[0],
            'title': current_period[1],
            'description': current_period[2],
            'start_time': period_status.get('start_time'),
            'end_time': period_status.get('end_time'),
            'time_remaining': period_status.get('time_remaining'),
            'time_until_start': period_status.get('time_until_start')
        }
    
    # Get current server time for display
    server_time = get_server_time()
    
    return render_template('voting_periods.html', 
                         periods=periods, 
                         period_status=period_status, 
                         current_status=current_status,
                         server_time=server_time)

@app.route('/voting_periods/create', methods=['POST'])
def create_voting_period():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('name', '')
    description = request.form.get('description', '')
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    
    try:
        # Validate times
        start_dt = datetime.fromisoformat(start_time.replace('T', ' '))
        end_dt = datetime.fromisoformat(end_time.replace('T', ' '))
        
        if start_dt >= end_dt:
            flash('Waktu mulai harus lebih awal dari waktu berakhir!', 'error')
            return redirect(url_for('voting_periods'))
        
        # Allow start time to be current time or future (with 1 minute tolerance for past)
        current_time = get_server_time()
        tolerance = timedelta(minutes=1)
        if start_dt < (current_time - tolerance):
            flash('Waktu mulai tidak boleh lebih dari 1 menit yang lalu!', 'error')
            return redirect(url_for('voting_periods'))
        
        # Check for overlapping periods
        overlapping = execute_query("""
            SELECT COUNT(*) FROM voting_periods 
            WHERE status != 'ended' AND (
                (start_time <= %s AND end_time > %s) OR
                (start_time < %s AND end_time >= %s) OR
                (start_time >= %s AND end_time <= %s)
            )
        """, (start_time, start_time, end_time, end_time, start_time, end_time), fetch='one')
        
        if overlapping and overlapping[0] > 0:
            flash('Periode voting bertabrakan dengan periode lain yang sudah ada!', 'error')
            return redirect(url_for('voting_periods'))
        
        execute_query("""
            INSERT INTO voting_periods (title, description, start_time, end_time, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, description, start_time, end_time, session.get('admin_username', 'admin')))
        
        flash('Periode voting berhasil dibuat!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('voting_periods'))

@app.route('/voting_periods/<int:period_id>/start', methods=['POST'])
def start_voting_period(period_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    try:
        # Check if period exists and is scheduled
        period = execute_query("""
            SELECT * FROM voting_periods WHERE id = %s AND status = 'scheduled'
        """, (period_id,), fetch='one')
        
        if not period:
            flash('Periode voting tidak ditemukan atau sudah aktif!', 'error')
            return redirect(url_for('voting_periods'))
        
        # Update status to active
        execute_query("""
            UPDATE voting_periods SET status = 'active' WHERE id = %s
        """, (period_id,))
        
        # Reset user voting status for new period
        execute_query("UPDATE user SET has_voted = 0")
        
        flash('Periode voting berhasil dimulai!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('voting_periods'))

@app.route('/voting_periods/<int:period_id>/stop', methods=['POST'])
def stop_voting_period(period_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    try:
        execute_query("""
            UPDATE voting_periods 
            SET manually_stopped = 1, stopped_at = %s, status = 'ended'
            WHERE id = %s AND status = 'active'
        """, (datetime.now(), period_id))
        
        flash('Periode voting berhasil dihentikan!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('voting_periods'))

@app.route('/voting_periods/<int:period_id>/extend', methods=['POST'])
def extend_voting_period(period_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    try:
        extension_hours = int(request.form.get('extension_hours', 1))
        
        # Get current period
        period = execute_query("""
            SELECT * FROM voting_periods WHERE id = %s AND status = 'active'
        """, (period_id,), fetch='one')
        
        if not period:
            flash('Periode voting tidak ditemukan atau tidak aktif!', 'error')
            return redirect(url_for('voting_periods'))
        
        # Calculate new end time
        current_end = datetime.fromisoformat(period[4])
        new_end = current_end + timedelta(hours=extension_hours)
        
        execute_query("""
            UPDATE voting_periods 
            SET end_time = %s, extended_count = extended_count + 1
            WHERE id = %s
        """, (new_end, period_id))
        
        flash(f'Periode voting berhasil diperpanjang {extension_hours} jam!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('voting_periods'))

@app.route('/api/voting_status')
def api_voting_status():
    """API endpoint for real-time voting status"""
    period_status = get_voting_period_status()
    return jsonify(period_status)

@app.route('/voting')
def voting_page():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get candidates
    candidates = execute_query(
        "SELECT * FROM anggota WHERE status = 'kandidat' ORDER BY nama",
        fetch=True
    )
    
    # Get users
    users = execute_query("SELECT * FROM user ORDER BY nama", fetch=True)
    
    # Get voting results
    voting_results = execute_query("""
        SELECT a.id, a.nama, COUNT(v.id) as vote_count
        FROM anggota a
        LEFT JOIN voting v ON a.id = v.kandidat_id
        WHERE a.status = 'kandidat'
        GROUP BY a.id, a.nama
        ORDER BY vote_count DESC, a.nama
    """, fetch=True)
    
    return render_template('voting.html', candidates=candidates, users=users, voting_results=voting_results)

@app.route('/user/add', methods=['POST'])
def add_user():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    nama = request.form['nama']
    username = request.form['username']
    password = generate_password_hash(request.form['password'])
    
    try:
        execute_query(
            "INSERT INTO user (nama, username, password) VALUES (%s, %s, %s)",
            (nama, username, password)
        )
        flash('User berhasil ditambahkan!', 'success')
    except:
        flash('Username sudah digunakan!', 'error')
    
    return redirect(url_for('voting_page'))

@app.route('/user/delete/<int:id>')
def delete_user(id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get user info before deleting
    user = execute_query("SELECT nama FROM user WHERE id = %s", (id,), fetch='one')
    
    if user:
        # Delete user (cascade will delete related penilaian and voting)
        execute_query("DELETE FROM user WHERE id = %s", (id,))
        flash(f'User "{user[0]}" berhasil dihapus!', 'success')
    else:
        flash('User tidak ditemukan!', 'error')
    
    return redirect(url_for('voting_page'))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = execute_query(
            "SELECT * FROM user WHERE username = %s",
            (username,),
            fetch='one'
        )
        
        if user and check_password_hash(user[3], password):
            session['user_logged_in'] = True
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('user_penilaian'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('user_login.html')

@app.route('/user_penilaian')
def user_penilaian():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    # Get all members
    members = execute_query("SELECT * FROM anggota ORDER BY nama", fetch=True)
    
    # Get user's existing ratings
    user_ratings = execute_query("""
        SELECT anggota_id FROM penilaian WHERE user_id = %s
    """, (session['user_id'],), fetch=True)
    
    rated_member_ids = [r[0] for r in user_ratings] if user_ratings else []
    
    return render_template('user_penilaian.html', members=members, rated_member_ids=rated_member_ids)

@app.route('/submit_penilaian', methods=['POST'])
def submit_penilaian():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    anggota_id = int(request.form['anggota_id'])
    keaktifan = int(request.form['keaktifan'])
    kepemimpinan = int(request.form['kepemimpinan'])
    pengalaman = int(request.form['pengalaman'])
    disiplin = int(request.form['disiplin'])
    komunikasi = int(request.form['komunikasi'])
    user_id = session['user_id']
    
    # Check if user already rated this member
    existing = execute_query(
        "SELECT * FROM penilaian WHERE user_id = %s AND anggota_id = %s",
        (user_id, anggota_id),
        fetch='one'
    )
    
    if existing:
        # Update existing rating
        execute_query("""
            UPDATE penilaian 
            SET keaktifan=%s, kepemimpinan=%s, pengalaman=%s, disiplin=%s, komunikasi=%s
            WHERE user_id=%s AND anggota_id=%s
        """, (keaktifan, kepemimpinan, pengalaman, disiplin, komunikasi, user_id, anggota_id))
        flash('Penilaian berhasil diupdate!', 'success')
    else:
        # Insert new rating
        execute_query("""
            INSERT INTO penilaian (user_id, anggota_id, keaktifan, kepemimpinan, pengalaman, disiplin, komunikasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, anggota_id, keaktifan, kepemimpinan, pengalaman, disiplin, komunikasi))
        flash('Penilaian berhasil disimpan!', 'success')
    
    return redirect(url_for('user_penilaian'))

@app.route('/user_vote')
def user_vote():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    # Check voting period status
    if not is_voting_allowed():
        period_status = get_voting_period_status()
        if period_status['status'] == 'scheduled':
            flash('Voting belum dimulai. Silakan tunggu hingga periode voting aktif.', 'warning')
        elif period_status['status'] == 'ended':
            flash('Periode voting telah berakhir.', 'info')
        else:
            flash('Tidak ada periode voting yang aktif saat ini.', 'warning')
        return render_template('user_voting.html', candidates=[], period_status=period_status)
    
    # Get current voting period
    current_period = get_current_voting_period()
    
    # Check if user already voted in current period
    existing_vote = execute_query(
        "SELECT * FROM voting WHERE user_id = %s AND voting_period_id = %s",
        (session['user_id'], current_period[0] if current_period else None),
        fetch='one'
    )
    
    if existing_vote:
        flash('Anda sudah melakukan voting pada periode ini!', 'info')
        return redirect(url_for('vote_success'))
    
    # Get candidates with their average ratings
    candidates = execute_query("""
        SELECT 
            a.id,
            a.nama,
            a.pendidikan,
            a.visi_misi,
            AVG(p.keaktifan) as avg_keaktifan,
            AVG(p.kepemimpinan) as avg_kepemimpinan,
            AVG(p.pengalaman) as avg_pengalaman,
            AVG(p.disiplin) as avg_disiplin,
            AVG(p.komunikasi) as avg_komunikasi,
            COUNT(p.id) as rating_count
        FROM anggota a
        LEFT JOIN penilaian p ON a.id = p.anggota_id
        WHERE a.status = 'kandidat'
        GROUP BY a.id, a.nama, a.pendidikan, a.visi_misi
        ORDER BY a.nama
    """, fetch=True)
    
    # Get period status for countdown
    period_status = get_voting_period_status()
    
    return render_template('user_voting.html', candidates=candidates, period_status=period_status)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    # Check voting period status
    if not is_voting_allowed():
        flash('Voting tidak diizinkan saat ini. Periode voting mungkin belum dimulai atau sudah berakhir.', 'error')
        return redirect(url_for('user_vote'))
    
    # Get current voting period
    current_period = get_current_voting_period()
    if not current_period:
        flash('Tidak ada periode voting yang aktif!', 'error')
        return redirect(url_for('user_vote'))
    
    kandidat_id = request.form['kandidat_id']
    user_id = session['user_id']
    
    # Check if user already voted in current period
    existing_vote = execute_query(
        "SELECT * FROM voting WHERE user_id = %s AND voting_period_id = %s",
        (user_id, current_period[0]),
        fetch='one'
    )
    
    if existing_vote:
        flash('Anda sudah melakukan voting pada periode ini!', 'error')
        return redirect(url_for('user_vote'))
    
    # Submit vote with period tracking
    execute_query(
        "INSERT INTO voting (user_id, kandidat_id, voting_period_id) VALUES (%s, %s, %s)",
        (user_id, kandidat_id, current_period[0])
    )
    
    # Update user voting status
    execute_query(
        "UPDATE user SET has_voted = 1 WHERE id = %s",
        (user_id,)
    )
    
    flash('Vote berhasil disimpan!', 'success')
    return redirect(url_for('vote_success'))

@app.route('/vote_success')
def vote_success():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    return render_template('vote_success.html')

@app.route('/user_change_password', methods=['GET', 'POST'])
def user_change_password():
    if 'user_logged_in' not in session:
        return redirect(url_for('user_login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Get user data
        user = execute_query(
            "SELECT * FROM user WHERE id = %s",
            (session['user_id'],),
            fetch='one'
        )
        
        if not user:
            flash('User tidak ditemukan!', 'error')
            return redirect(url_for('user_change_password'))
        
        # Verify current password
        if not check_password_hash(user[3], current_password):
            flash('Password lama salah!', 'error')
            return redirect(url_for('user_change_password'))
        
        # Validate new password
        if len(new_password) < 6:
            flash('Password baru minimal 6 karakter!', 'error')
            return redirect(url_for('user_change_password'))
        
        if new_password != confirm_password:
            flash('Password baru dan konfirmasi tidak cocok!', 'error')
            return redirect(url_for('user_change_password'))
        
        # Update password
        hashed_password = generate_password_hash(new_password)
        execute_query(
            "UPDATE user SET password = %s WHERE id = %s",
            (hashed_password, session['user_id'])
        )
        
        flash('Password berhasil diubah!', 'success')
        return redirect(url_for('user_penilaian'))
    
    return render_template('user_change_password.html')

@app.route('/user_logout')
def user_logout():
    session.pop('user_logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('user_login'))

@app.route('/hasil')
def hasil():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    # Get period filter from query parameter
    period_id = request.args.get('period_id', type=int)
    
    # Build query based on period filter
    if period_id:
        # Get results for specific period
        results = execute_query("""
            SELECT a.id, a.nama, COUNT(v.id) as vote_count,
                   a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
            FROM anggota a
            LEFT JOIN voting v ON a.id = v.kandidat_id AND v.voting_period_id = %s
            WHERE a.status = 'kandidat'
            GROUP BY a.id, a.nama, a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
            ORDER BY vote_count DESC, a.nama
        """, (period_id,), fetch=True)
        
        # Get total votes for specific period
        total_votes_result = execute_query(
            "SELECT COUNT(*) FROM voting WHERE voting_period_id = %s", 
            (period_id,), fetch='one'
        )
        total_votes = total_votes_result[0] if total_votes_result else 0
        
        # Get period info
        period_info = execute_query("""
            SELECT id, title, start_time, end_time, status 
            FROM voting_periods WHERE id = %s
        """, (period_id,), fetch='one')
    else:
        # Get results for current/latest period
        current_period = get_current_voting_period()
        if current_period:
            results = execute_query("""
                SELECT a.id, a.nama, COUNT(v.id) as vote_count,
                       a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
                FROM anggota a
                LEFT JOIN voting v ON a.id = v.kandidat_id AND v.voting_period_id = %s
                WHERE a.status = 'kandidat'
                GROUP BY a.id, a.nama, a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
                ORDER BY vote_count DESC, a.nama
            """, (current_period[0],), fetch=True)
            
            total_votes_result = execute_query(
                "SELECT COUNT(*) FROM voting WHERE voting_period_id = %s", 
                (current_period[0],), fetch='one'
            )
            total_votes = total_votes_result[0] if total_votes_result else 0
            period_info = current_period
        else:
            # No active period, show all results
            results = execute_query("""
                SELECT a.id, a.nama, COUNT(v.id) as vote_count,
                       a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
                FROM anggota a
                LEFT JOIN voting v ON a.id = v.kandidat_id
                WHERE a.status = 'kandidat'
                GROUP BY a.id, a.nama, a.keaktifan, a.kepemimpinan, a.pengalaman, a.disiplin, a.pendidikan, a.usia
                ORDER BY vote_count DESC, a.nama
            """, fetch=True)
            
            total_votes_result = execute_query("SELECT COUNT(*) FROM voting", fetch='one')
            total_votes = total_votes_result[0] if total_votes_result else 0
            period_info = None
    
    # Get all periods for dropdown
    all_periods = execute_query("""
        SELECT id, title, start_time, end_time, status,
               (SELECT COUNT(*) FROM voting WHERE voting_period_id = voting_periods.id) as vote_count
        FROM voting_periods 
        ORDER BY start_time DESC
    """, fetch=True)
    
    # Get total users count
    total_users_result = execute_query("SELECT COUNT(*) FROM user", fetch='one')
    total_users = total_users_result[0] if total_users_result else 0
    
    # Get K-Means cluster results for display
    cluster_results = {}
    try:
        # Get all members with their cluster assignments
        members = execute_query("""
            SELECT nama, keaktifan, kepemimpinan, pengalaman, disiplin, pendidikan, usia, cluster
            FROM anggota 
            WHERE cluster IS NOT NULL
            ORDER BY cluster, nama
        """, fetch=True)
        
        if members:
            for member in members:
                cluster_name = ""
                if member[7] == 0:  # cluster 0
                    cluster_name = "Sangat Layak"
                elif member[7] == 1:  # cluster 1
                    cluster_name = "Cukup Layak"
                else:  # cluster 2
                    cluster_name = "Kurang Layak"
                
                if cluster_name not in cluster_results:
                    cluster_results[cluster_name] = []
                
                # Add member data with average score
                avg_score = (member[1] + member[2] + member[3] + member[4] + member[5]) / 5
                member_data = list(member) + [avg_score]
                cluster_results[cluster_name].append(member_data)
    except:
        cluster_results = {}
    
    return render_template('hasil.html', 
                         voting_results=results, 
                         total_votes=total_votes,
                         total_users=total_users,
                         cluster_results=cluster_results,
                         current_period=period_info,
                         all_periods=all_periods,
                         selected_period_id=period_id)

@app.route('/reset_voting', methods=['POST'])
def reset_voting():
    if 'admin_logged_in' not in session:
        return redirect(url_for('login'))
    
    execute_query("DELETE FROM voting")
    execute_query("UPDATE anggota SET status = 'anggota'")
    
    flash('Data voting berhasil direset!', 'success')
    return redirect(url_for('voting_page'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)