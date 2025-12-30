from app import create_app
from backend.database import db

app = create_app()

with app.app_context():
    try:
        # Check and add alert_type column
        try:
            db.session.execute(db.text("ALTER TABLE alerts ADD COLUMN alert_type VARCHAR(50) DEFAULT 'estimation'"))
            print("✓ Added alert_type column")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ alert_type column already exists")
            else:
                print(f"! Error adding alert_type: {e}")
        
        # Check and add created_at column
        try:
            db.session.execute(db.text("ALTER TABLE alerts ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
            print("✓ Added created_at column")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ created_at column already exists")
            else:
                print(f"! Error adding created_at: {e}")
        
        # Update flood_predictions to allow NULL video_id
        try:
            db.session.execute(db.text("ALTER TABLE flood_predictions MODIFY video_id INT NULL"))
            print("✓ video_id now allows NULL")
        except Exception as e:
            print(f"! Error modifying video_id: {e}")
        
        db.session.commit()
        print("\n✓✓✓ Database migration completed successfully! ✓✓✓")
        print("You can now restart Flask and try creating alerts again.")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        db.session.rollback()
