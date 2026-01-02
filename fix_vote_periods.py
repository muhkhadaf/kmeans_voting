import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='votings'
)
cursor = conn.cursor()

print("Fixing vote-period linkage...")
print("=" * 60)

# 1. Get active period
cursor.execute("SELECT id, title FROM voting_periods WHERE status='active' LIMIT 1")
active_period = cursor.fetchone()

if not active_period:
    print("ERROR: No active voting period found!")
    print("Please create and activate a voting period first.")
    cursor.close()
    conn.close()
    exit(1)

period_id = active_period[0]
period_title = active_period[1]
print(f"Active period: {period_title} (ID: {period_id})")

# 2. Check votes without period or with wrong period
cursor.execute("""
    SELECT COUNT(*) FROM voting 
    WHERE voting_period_id IS NULL OR voting_period_id != %s
""", (period_id,))
unlinked_count = cursor.fetchone()[0]

if unlinked_count == 0:
    print("All votes are already linked to the active period!")
else:
    print(f"Found {unlinked_count} votes not linked to active period")
    
    # 3. Update votes to link to active period
    cursor.execute("""
        UPDATE voting 
        SET voting_period_id = %s 
        WHERE voting_period_id IS NULL OR voting_period_id != %s
    """, (period_id, period_id))
    
    conn.commit()
    print(f"✓ Updated {cursor.rowcount} votes to period ID {period_id}")

# 4. Verify
cursor.execute("SELECT COUNT(*) FROM voting WHERE voting_period_id = %s", (period_id,))
linked_count = cursor.fetchone()[0]
print(f"\nTotal votes now linked to active period: {linked_count}")

print("=" * 60)
print("Fix complete! Refresh the hasil page to see results.")

cursor.close()
conn.close()
