from app import create_app
from database.seed import seed_database


def main():
    create_app()
    seed_database()
    print("Database seed completed.")


if __name__ == "__main__":
    main()
