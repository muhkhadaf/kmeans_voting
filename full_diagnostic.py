import sys
sys.path.insert(0, 'c:\\program_freelance\\kmeans_voting')

from db import get_db, close_db
import mysql.connector

# Direct database connection to avoid app context issues
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='votings'
)
cursor = conn.cursor()

print("=" * 70)
print("COMPREHENSIVE DATABASE DIAGNOSTIC")
print("=" * 70)

# 1. Check voting table
print("\n1. VOTING TABLE DATA:")
cursor.execute("SELECT * FROM voting")
votes = cursor.fetchall()
if votes:
    print(f"   ✓ Found {len(votes)} vote records")
    for v in votes[:5]:  # Show first 5
        print(f"   - Vote ID: {v[0]}, User: {v[1]}, Kandidat: {v[2]}, Period: {v[3]}")
        if len(v) > 4:
            print(f"     Ratings: K={v[4]}, Kp={v[5]}, P={v[6]}, D={v[7]}, Km={v[8]}")
else:
    print("   ✗ NO VOTES IN DATABASE")

# 2. Check voting periods
print("\n2. VOTING PERIODS:")
cursor.execute("SELECT id, title, status, start_time, end_time FROM voting_periods")
periods = cursor.fetchall()
if periods:
    print(f"   ✓ Found {len(periods)} period(s)")
    for p in periods:
        print(f"   - ID: {p[0]}, Title: {p[1]}, Status: {p[2]}")
        print(f"     Start: {p[3]}, End: {p[4]}")
else:
    print("   ✗ NO PERIODS IN DATABASE")

# 3. Check candidates
print("\n3. CANDIDATES:")
cursor.execute("SELECT id, nama, status FROM anggota WHERE status='kandidat'")
candidates = cursor.fetchall()
if candidates:
    print(f"   ✓ Found {len(candidates)} candidate(s)")
    for c in candidates:
        print(f"   - ID: {c[0]}, Name: {c[1]}")
else:
    print("   ✗ NO CANDIDATES")

# 4. Check users
print("\n4. USERS:")
cursor.execute("SELECT id, nama FROM user")
users = cursor.fetchall()
if users:
    print(f"   ✓ Found {len(users)} user(s)")
    for u in users:
        print(f"   - ID: {u[0]}, Name: {u[1]}")
else:
    print("   ✗ NO USERS")

# 5. Cross-check votes with periods
if votes and periods:
    print("\n5. VOTE-PERIOD MATCHING:")
    period_ids = [p[0] for p in periods]
    vote_period_ids = set([v[3] for v in votes])
    print(f"   Period IDs in database: {period_ids}")
    print(f"   Period IDs in votes: {list(vote_period_ids)}")
    
    for vpid in vote_period_ids:
        if vpid in period_ids:
            print(f"   ✓ Votes with period_id {vpid} MATCH existing period")
        elif vpid is None:
            print(f"   ✗ Some votes have NULL period_id!")
        else:
            print(f"   ✗ Votes with period_id {vpid} DON'T MATCH any period!")

# 6. Test the actual hasil query
if periods:
    active_period = [p for p in periods if p[2] == 'active']
    if active_period:
        period_id = active_period[0][0]
        print(f"\n6. TESTING HASIL QUERY (Period ID: {period_id}):")
        
        query = """
            SELECT a.id, a.nama, COUNT(v.id) as vote_count,
                   COALESCE(AVG(v.keaktifan), 0) as avg_keaktifan,
                   COALESCE(AVG(v.kepemimpinan), 0) as avg_kepemimpinan,
                   COALESCE(AVG(v.pengalaman), 0) as avg_pengalaman,
                   COALESCE(AVG(v.disiplin), 0) as avg_disiplin,
                   COALESCE(AVG(v.komunikasi), 0) as avg_komunikasi
            FROM anggota a
            LEFT JOIN voting v ON a.id = v.kandidat_id AND v.voting_period_id = %s
            WHERE a.status = 'kandidat'
            GROUP BY a.id, a.nama
        """
        cursor.execute(query, (period_id,))
        results = cursor.fetchall()
        
        if results:
            print(f"   ✓ Query returned {len(results)} result(s):")
            for r in results:
                final_score = (r[3] + r[4] + r[5] + r[6] + r[7]) / 5
                print(f"   - {r[1]}: votes={r[2]}, score={final_score:.2f}")
        else:
            print("   ✗ Query returned NO results")
    else:
        print("\n6. ✗ NO ACTIVE PERIOD")

print("\n" + "=" * 70)
print("DIAGNOSIS:")
if not votes:
    print("❌ PROBLEM: No votes in database - users haven't submitted ratings")
elif not periods:
    print("❌ PROBLEM: No voting periods - create one in admin panel")
elif not candidates:
    print("❌ PROBLEM: No candidates - select candidates in 'Kelola Voting'")
elif votes and periods:
    vote_period_ids = set([v[3] for v in votes if v[3] is not None])
    period_ids = [p[0] for p in periods]
    if not vote_period_ids.intersection(period_ids):
        print("❌ PROBLEM: Votes exist but don't match any period ID")
        print("   SOLUTION: Update votes to use correct period_id")
    else:
        active = [p for p in periods if p[2] == 'active']
        if not active:
            print("❌ PROBLEM: Period exists but not active")
            print("   SOLUTION: Activate the period in admin panel")
        else:
            print("✓ Everything looks OK - check hasil route logic")
print("=" * 70)

cursor.close()
conn.close()
