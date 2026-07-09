"""
Initialize database and create default data.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.database.session import init_db, SessionLocal
from src.database.models import User
from src.auth.authentication import AuthenticationManager
from src.utils.logger import setup_logging

def main():
    """Initialize database with default data."""
    # Setup logging
    setup_logging(level="INFO")
    
    print("🔧 Initializing LogisticSmart database...")
    
    # Initialize database tables
    init_db()
    print("✅ Database tables created")
    
    # Create default users
    db = SessionLocal()
    try:
        # Check if admin user exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if not existing_admin:
            auth_manager = AuthenticationManager()
            
            # Create default users
            default_users = [
                {
                    "username": "admin",
                    "password": "admin123",
                    "name": "Administrador",
                    "role": "admin",
                    "email": "admin@logisticsmart.com"
                },
                {
                    "username": "visitante",
                    "password": "fasebeta",
                    "name": "Visitante",
                    "role": "viewer",
                    "email": "visitor@logisticsmart.com"
                },
                {
                    "username": "neo",
                    "password": "matrix",
                    "name": "Neo",
                    "role": "admin",
                    "email": "neo@logisticsmart.com"
                }
            ]
            
            for user_data in default_users:
                user = User(
                    username=user_data["username"],
                    password_hash=auth_manager._hash_password(user_data["password"]),
                    name=user_data["name"],
                    role=user_data["role"],
                    email=user_data["email"],
                    active=True
                )
                db.add(user)
                print(f"✅ Created user: {user_data['username']}")
            
            db.commit()
            print("✅ Default users created")
        else:
            print("ℹ️ Default users already exist")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating users: {e}")
        raise
    finally:
        db.close()
    
    print("\n🎉 Database initialization completed!")
    print("\n📝 Default credentials:")
    print("  - Admin: admin / admin123")
    print("  - Visitante: visitante / fasebeta")
    print("  - Neo: neo / matrix")

if __name__ == "__main__":
    main()
