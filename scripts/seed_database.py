from database.seed import seed_database


def main():
    seed_database()
    print("Database seed completed.")


if __name__ == "__main__":
    main()
