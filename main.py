import random
import uuid
from datetime import datetime, timedelta
import csv

# Define post types
post_types = ["carousel", "static post", "reel", "static image"]

# Generate random engagement data
def generate_engagement_data(num_records=1000):
    data = []
    
    for i in range(num_records):
        post_id = i+1
        post_type = random.choice(post_types)
        likes = random.randint(50, 5000)
        shares = random.randint(10, 1000)
        comments = random.randint(5, 500)
        timestamp = datetime.now() - timedelta(days=random.randint(0, 365))
        
        data.append({
            "post_id": post_id,
            "post_type": post_type,
            "likes": likes,
            "shares": shares,
            "comments": comments,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return data

# Save data to CSV
def save_to_csv(data, filename="social_media_engagement2.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["post_id", "post_type", "likes", "shares", "comments", "timestamp"])
        writer.writeheader()
        writer.writerows(data)

# Generate and save data
data = generate_engagement_data(1000)
save_to_csv(data)

print("Data generation complete. Saved to social_media_engagement.csv")
