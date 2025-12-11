import json
from database import get_snacks_collection

def seed_snacks():
    snacks_col = get_snacks_collection()
    
    # Check if already seeded
    if snacks_col.count_documents({}) > 0:
        print("Database already seeded.")
        return

    try:
        with open("snack_catalog.json", "r") as f:
            snacks = json.load(f)
            
        if snacks:
            snacks_col.insert_many(snacks)
            print(f"Seeded {len(snacks)} snacks into MongoDB.")
        else:
            print("No snacks found in snack_catalog.json")
            
    except FileNotFoundError:
        print("snack_catalog.json not found.")
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_snacks()
