import mysql.connector
from datetime import datetime, timedelta
import json

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'votings'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def setup_test_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("Setting up test data...")
    
    # 1. Ensure we have a user
    cursor.execute("SELECT * FROM user WHERE email = 'test_voter@example.com'")
    user = cursor.fetchone()
    if not user:
        cursor.execute("""
            INSERT INTO user (nama, email, password, role, has_voted) 
            VALUES ('Test Voter', 'test_voter@example.com', 'password', 'user', 0)
        """)
        user_id = cursor.lastrowid
        print(f"Created test user with ID: {user_id}")
    else:
        user_id = user['id']
        print(f"Using existing test user ID: {user_id}")
        
    # 2. Ensure we have a candidate
    cursor.execute("SELECT * FROM anggota WHERE status = 'kandidat' LIMIT 1")
    candidate = cursor.fetchone()
    if not candidate:
        # Create a dummy candidate if none exists
        cursor.execute("""
            INSERT INTO anggota (nama, pendidikan, status) 
            VALUES ('Test Candidate', 'S1', 'kandidat')
        """)
        candidate_id = cursor.lastrowid
        print(f"Created test candidate with ID: {candidate_id}")
    else:
        candidate_id = candidate['id']
        print(f"Using existing candidate ID: {candidate_id}")
        
    # 3. Ensure active voting period
    now = datetime.now()
    end_time = now + timedelta(days=1)
    cursor.execute("""
        SELECT * FROM voting_periods 
        WHERE status = 'active' 
        AND start_time <= %s 
        AND end_time >= %s
    """, (now, now))
    period = cursor.fetchone()
    
    if not period:
        cursor.execute("""
            INSERT INTO voting_periods (title, start_time, end_time, status)
            VALUES ('Test Period', %s, %s, 'active')
        """, (now, end_time))
        period_id = cursor.lastrowid
        print(f"Created active voting period ID: {period_id}")
    else:
        period_id = period['id']
        print(f"Using existing active period ID: {period_id}")
        
    conn.commit()
    cursor.close()
    conn.close()
    
    return user_id, candidate_id, period_id

def test_submit_rating(user_id, candidate_id, period_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("\nTesting rating submission...")
    
    # Ratings to submit
    ratings = {
        'keaktifan': 80,
        'kepemimpinan': 85,
        'pengalaman': 90,
        'disiplin': 75,
        'komunikasi': 88
    }
    
    # Check for existing vote
    cursor.execute("""
        SELECT * FROM voting 
        WHERE user_id = %s AND kandidat_id = %s AND voting_period_id = %s
    """, (user_id, candidate_id, period_id))
    existing = cursor.fetchone()
    
    if existing:
        print("Updating existing rating...")
        cursor.execute("""
            UPDATE voting 
            SET keaktifan=%s, kepemimpinan=%s, pengalaman=%s, disiplin=%s, komunikasi=%s
            WHERE id=%s
        """, (ratings['keaktifan'], ratings['kepemimpinan'], ratings['pengalaman'], 
              ratings['disiplin'], ratings['komunikasi'], existing['id']))
    else:
        print("Inserting new rating...")
        cursor.execute("""
            INSERT INTO voting (user_id, kandidat_id, voting_period_id, 
                              keaktifan, kepemimpinan, pengalaman, disiplin, komunikasi)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, candidate_id, period_id, 
              ratings['keaktifan'], ratings['kepemimpinan'], ratings['pengalaman'], 
              ratings['disiplin'], ratings['komunikasi']))
              
    conn.commit()
    
    # Verify insertion
    cursor.execute("""
        SELECT * FROM voting 
        WHERE user_id = %s AND kandidat_id = %s AND voting_period_id = %s
    """, (user_id, candidate_id, period_id))
    vote = cursor.fetchone()
    
    if vote:
        print("✅ Rating submitted successfully!")
        print(f"Stored ratings: {vote}")
        
        # Verify values match
        matches = all(vote[k] == v for k, v in ratings.items())
        if matches:
            print("✅ All rating values match expected values.")
        else:
            print("❌ Rating values mismatch!")
    else:
        print("❌ Failed to find submitted rating!")
        
    cursor.close()
    conn.close()

def test_results_calculation(period_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("\nTesting results calculation...")
    
    # Simulate query used in app.py
    query = """
        SELECT a.id, a.nama, COUNT(v.id) as vote_count,
               AVG(v.keaktifan) as avg_keaktifan,
               AVG(v.kepemimpinan) as avg_kepemimpinan,
               AVG(v.pengalaman) as avg_pengalaman,
               AVG(v.disiplin) as avg_disiplin,
               AVG(v.komunikasi) as avg_komunikasi,
               (AVG(v.keaktifan) + AVG(v.kepemimpinan) + AVG(v.pengalaman) + AVG(v.disiplin) + AVG(v.komunikasi)) / 5 as final_score
        FROM anggota a
        LEFT JOIN voting v ON a.id = v.kandidat_id AND v.voting_period_id = %s
        WHERE a.status = 'kandidat'
        GROUP BY a.id, a.nama
        ORDER BY final_score DESC
    """
    
    cursor.execute(query, (period_id,))
    results = cursor.fetchall()
    
    print(f"Found {len(results)} candidates in results.")
    
    for res in results:
        print(f"\nCandidate: {res['nama']}")
        print(f"Vote Count: {res['vote_count']}")
        print(f"Final Score: {res['final_score']}")
        
        if res['vote_count'] > 0:
            print("✅ Candidate has votes and score calculated.")
        else:
            print("ℹ️ Candidate has no votes yet.")
            
    cursor.close()
    conn.close()

if __name__ == "__main__":
    try:
        user_id, candidate_id, period_id = setup_test_data()
        test_submit_rating(user_id, candidate_id, period_id)
        test_results_calculation(period_id)
        print("\n✅ Verification completed successfully!")
    except Exception as e:
        print(f"\n❌ Verification failed: {str(e)}")
