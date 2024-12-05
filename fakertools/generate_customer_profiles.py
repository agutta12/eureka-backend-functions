import csv
from faker import Faker

fake = Faker()

def generate_customer_profiles(count):
    profiles = []
    for _ in range(count):
        profiles.append({
            "id": fake.uuid4(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "company": fake.company(),
            "job_title": fake.job(),
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%Y-%m-%d"),
        })
    return profiles

def generate_and_save_in_batches(batch_size=100, total_count=500, filename="customer_profiles.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = None
        generated_count = 0
        
        while generated_count < total_count:
            profiles = generate_customer_profiles(min(batch_size, total_count - generated_count))
            if writer is None:
                # Initialize writer with header for the first batch
                writer = csv.DictWriter(file, fieldnames=profiles[0].keys())
                writer.writeheader()
            writer.writerows(profiles)
            generated_count += len(profiles)
            print(f"{generated_count}/{total_count} records written.")

generate_and_save_in_batches(batch_size=100, total_count=500)