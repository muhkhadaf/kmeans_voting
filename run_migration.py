from db import init_db

if __name__ == "__main__":
    print("Running database initialization and migration...")
    success = init_db()
    if success:
        print("Migration completed successfully.")
    else:
        print("Migration failed.")
