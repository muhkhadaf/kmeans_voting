from db import execute_query
from datetime import datetime
import pytz

print("=" * 60)
print("DIAGNOSTIC: Voter Rating Submission Issue")
print("=" * 60)

# 1. Check voting periods
print("\n1. VOTING PERIODS:")
periods = execute_query("""
    SELECT id, title, status, start_time, end_time 
    FROM voting_periods 
    ORDER BY id DESC LIMIT 5
""", fetch=True)

if periods:
    for p in periods:
        print(f"   ID: {p[0]}, Title: {p[1]}, Status: {p[2]}")
        print(f"   Start: {p[3]}, End: {p[4]}")
else:
    print("   ❌ No voting periods found!")

# 2. Check current time and active period
print("\n2. CURRENT TIME & ACTIVE PERIOD:")
tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(tz)
print(f"   Server time: {now}")

active_period = execute_query("""
    SELECT id, title, start_time, end_time, status
    FROM voting_periods 
    WHERE status = 'active' 
    AND start_time <= NOW() 
    AND end_time >= NOW()
    ORDER BY start_time DESC LIMIT 1
""", fetch='one')

if active_period:
    print(f"   ✓ Active period found: {active_period[1]} (ID: {active_period[0]})")
else:
    print("   ❌ No active voting period!")

# 3. Check candidates
print("\n3. CANDIDATES:")
candidates = execute_query("""
    SELECT id, nama, status 
    FROM anggota 
    WHERE status = 'kandidat'
""", fetch=True)

if candidates:
    print(f"   ✓ {len(candidates)} candidates found:")
    for c in candidates:
        print(f"      - {c[1]} (ID: {c[0]})")
else:
    print("   ❌ No candidates found!")

# 4. Check users
print("\n4. USERS:")
users = execute_query("SELECT id, nama, username FROM user", fetch=True)
if users:
    print(f"   ✓ {len(users)} users found")
else:
    print("   ❌ No users found!")

# 5. Check voting records
print("\n5. VOTING RECORDS:")
votes = execute_query("""
    SELECT v.id, u.nama as user_name, a.nama as kandidat_name, 
           v.keaktifan, v.kepemimpinan, v.pengalaman, v.disiplin, v.komunikasi
    FROM voting v
    JOIN user u ON v.user_id = u.id
    JOIN anggota a ON v.kandidat_id = a.id
    ORDER BY v.id DESC LIMIT 10
""", fetch=True)

if votes:
    print(f"   ✓ {len(votes)} voting records found:")
    for v in votes:
        print(f"      - {v[1]} → {v[2]}: K={v[3]}, Kp={v[4]}, P={v[5]}, D={v[6]}, Km={v[7]}")
else:
    print("   ❌ No voting records found!")

# 6. Summary
print("\n" + "=" * 60)
print("SUMMARY:")
if not periods:
    print("❌ ISSUE: No voting periods created")
    print("   → Create a voting period in 'Periode Voting' menu")
elif not active_period:
    print("❌ ISSUE: No active voting period")
    print("   → Start a voting period in 'Periode Voting' menu")
elif not candidates:
    print("❌ ISSUE: No candidates selected")
    print("   → Select candidates in 'Kelola Voting' menu")
elif not votes:
    print("⚠️  WARNING: System is ready but no votes submitted yet")
    print("   → Check if form submission is working")
else:
    print("✓ System appears to be working correctly")
print("=" * 60)
