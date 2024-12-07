import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Donor, Donation
from faker import Faker
import random
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# print(sys.path)

DATABASE_URL = "postgresql+psycopg2://postgres:uwinezahono@localhost/dts_fastapi"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

fake = Faker()

def generate_random_donors(num_donors: int):
    donors = []
    for _ in range(num_donors):
        donor = Donor(
            name=fake.name(),
            password=fake.password(),
            is_admin=random.choice([0, 1]),  
        )
        donors.append(donor)
    return donors

def generate_random_donations(num_donations: int, donor_ids: list):
    donations = []
    for _ in range(num_donations):
        donation = Donation(
            amount=round(random.uniform(10.0, 500.0), 2),
            method=random.choice(["Credit Card", "Cash", "Bank Transfer"]), 
            date=fake.date_this_year(),  
            donor_id=random.choice(donor_ids),
        )
        donations.append(donation)
    return donations

def export_and_describe_data():
    db = SessionLocal()

    try:
        num_donors = 500000 
        donors = generate_random_donors(num_donors)

        db.add_all(donors)
        db.commit()  

        donor_ids = [donor.id for donor in donors]

        num_donations = 500000
        donations = generate_random_donations(num_donations, donor_ids)

        db.add_all(donations)
        db.commit()  

        donor_df = pd.read_sql(db.query(Donor).statement, db.bind)
        donation_df = pd.read_sql(db.query(Donation).statement, db.bind)

        donor_part1 = donor_df[['id', 'name', 'is_admin']]
        donor_part2 = donor_df[['id', 'name', 'password']]

        donor_part1.to_csv("donors_part1.csv", index=False)
        donor_part2.to_csv("donors_part2.csv", index=False)

        concatenated_donors = pd.concat([donor_part1, donor_part2[['password']]], axis=1)
        concatenated_donors.to_csv("concatenated_donors.csv", index=False)

        print("Data has been exported and concatenated successfully.")

        print("\nFirst 5 rows from Donors Table:")
        print(donor_df.head())

        print("\nFirst 5 rows from Donations Table:")
        print(donation_df.head())

    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()  
    finally:
        db.close()

if __name__ == "__main__":
    export_and_describe_data()
