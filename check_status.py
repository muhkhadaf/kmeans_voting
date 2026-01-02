import sys
sys.path.insert(0, 'c:\\program_freelance\\kmeans_voting')

from db import execute_query

print("Checking voting system status...")
print("=" * 60)

# Check active period
try:
    period = execute_query(
        "SELECT id, title, status FROM voting_periods WHERE status='active'", 
        fetch='one'
    )
    if period:
        print(f"✓ Active period: {period[1]} (ID: {period[0]})")
    else:
        print("✗ No active period found")
except Exception as e:
    print(f"✗ Error checking period: {e}")

# Check candidates
try:
    candidates = execute_query(
        "SELECT id, nama FROM anggota WHERE status='kandidat'", 
        fetch=True
    )
    if candidates:
        print(f"✓ {len(candidates)} candidates found:")
        for c in candidates:
            print(f"  - {c[1]} (ID: {c[0]})")
    else:
        print("✗ No candidates found")
except Exception as e:
    print(f"✗ Error checking candidates: {e}")

# Check votes
try:
    votes = execute_query("SELECT COUNT(*) FROM voting", fetch='one')
    print(f"Total votes in database: {votes[0] if votes else 0}")
except Exception as e:
    print(f"✗ Error checking votes: {e}")

# Check voting table structure
try:
    columns = execute_query("""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'voting'
        ORDER BY ORDINAL_POSITION
    """, fetch=True)
    if columns:
        print("\nVoting table structure:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
except Exception as e:
    print(f"✗ Error checking table structure: {e}")

print("=" * 60)
