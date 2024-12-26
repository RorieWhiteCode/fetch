import os
import requests
from serpapi import GoogleSearch
from PIL import Image
from io import BytesIO

# Configuration
API_KEY = "YOUR_SERPAPI_KEY"
SEARCH_QUERY = "Ned Flanders"
OUTPUT_DIR = "ned_flanders_images"
MAX_IMAGES = 1000

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_image_urls():
    """Fetch image URLs using SerpAPI."""
    image_urls = []
    search_params = {
        "q": SEARCH_QUERY,
        "tbm": "isch",
        "api_key": API_KEY,
        "ijn": 0  # Index of results page
    }
    page = 0
    
    while len(image_urls) < MAX_IMAGES:
        search_params['ijn'] = page
        search = GoogleSearch(search_params)
        results = search.get_dict()
        images = results.get("images_results", [])
        
        for img in images:
            if len(image_urls) >= MAX_IMAGES:
                break
            image_urls.append(img.get("original"))
        
        page += 1
    
    return image_urls

def download_images(image_urls):
    """Download images from the list of URLs."""
    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img_format = img.format if img.format else 'jpg'
                img.save(os.path.join(OUTPUT_DIR, f"ned_flanders_{idx+1}.{img_format}"))
                print(f"Downloaded image {idx+1}/{len(image_urls)}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

if __name__ == '__main__':
    print("Fetching image URLs...")
    image_urls = fetch_image_urls()
    print(f"Fetched {len(image_urls)} image URLs. Starting download...")
    download_images(image_urls)
    print("All images downloaded.")
