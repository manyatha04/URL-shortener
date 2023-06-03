import pymongo
import sys
import random
import string

# Establish a connection to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["url_shortener_sample"]
collection = db["urls"]

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

def shorten_url(original_url):
    # Check if the original URL already exists in the collection
    existing_url = collection.find_one({"original_url": original_url})
    if existing_url:
        return existing_url["short_url"]

    # Generate a unique short URL
    short_url = generate_short_url()

    # Insert the new URL mapping into the collection
    collection.insert_one({"original_url": original_url, "short_url": short_url})

    return short_url

def get_short_url(original_url):
    short_url = shorten_url(original_url)
    return short_url

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the original URL as a command-line argument.")
        sys.exit(1)
    
    original_url = sys.argv[1]
    short_url = get_short_url(original_url)
    if short_url:
        print("Shortened URL: ", short_url)
    else:
        print("Failed to retrieve or generate the shortened URL.")
