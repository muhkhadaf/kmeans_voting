import mysql.connector
from datetime import datetime, timedelta

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'votings'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def test_null_handling():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    print("Testing NULL handling for candidates with no votes...")
    
    # 1. Create a dummy candidate with NO votes
    cursor.execute("INSERT INTO anggota (nama, pendidikan, status) VALUES ('Null Test Candidate', 'S1', 'kandidat')")
    candidate_id = cursor.lastrowid
    conn.commit()
    print(f"Created candidate with ID: {candidate_id}")
    
    try:
        # 2. Run the query used in app.py (with COALESCE)
        # We need a valid period ID, let's get one
        cursor.execute("SELECT id FROM voting_periods WHERE status='active' LIMIT 1")
        period = cursor.fetchone()
        period_id = period['id'] if period else 0
        
        print(f"Testing with period ID: {period_id}")
        
        query = """
            SELECT a.id, a.nama, COUNT(v.id) as vote_count,
                   COALESCE(AVG(v.keaktifan), 0) as avg_keaktifan,
                   (COALESCE(AVG(v.keaktifan), 0) + COALESCE(AVG(v.kepemimpinan), 0) + COALESCE(AVG(v.pengalaman), 0) + COALESCE(AVG(v.disiplin), 0) + COALESCE(AVG(v.komunikasi), 0)) / 5 as final_score
            FROM anggota a
            LEFT JOIN voting v ON a.id = v.kandidat_id AND v.voting_period_id = %s
            WHERE a.id = %s
            GROUP BY a.id, a.nama
        """
        
        cursor.execute(query, (period_id, candidate_id))
        result = cursor.fetchone()
        
        if result:
            print(f"Result: {result}")
            final_score = result['final_score']
            print(f"Final Score type: {type(final_score)}")
            print(f"Final Score value: {final_score}")
            
            if final_score is not None and float(final_score) == 0.0:
                print("✅ SUCCESS: Final score is 0.0 as expected (not None).")
            else:
                print(f"❌ FAILURE: Final score is {final_score} (expected 0.0).")
        else:
            print("❌ FAILURE: No result found for candidate.")
            
    finally:
        # Cleanup
        cursor.execute("DELETE FROM anggota WHERE id = %s", (candidate_id,))
        conn.commit()
        cursor.close()
        conn.close()

if __name__ == "__main__":
    test_null_handling()
