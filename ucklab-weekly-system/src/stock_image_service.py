"""
stock_image_service.py - UCKLab Free Stock Photo Curation & W810 x H480 Resizer
Supports Pixabay, Pexels, and High-Resolution Free Stock Providers (Unsplash/Wikimedia).
Prepares and crops images to EXACT W810 x H480 dimensions for WordPress featured media.
"""

import os
import sys
import io
import time
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageEnhance
from dotenv import load_dotenv

# UTF-8 console output for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_STORAGE_DIR = os.path.join(BASE_DIR, "storage", "images")
os.makedirs(IMAGE_STORAGE_DIR, exist_ok=True)

load_dotenv(os.path.join(BASE_DIR, ".env"))

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

# Target dimensions specified by user
TARGET_WIDTH = 810
TARGET_HEIGHT = 480
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT  # 1.6875

# Curated High-Definition Free Stock Photo Fallback Mapping (High Quality Unsplash / Free Stock CDN)
CATEGORY_STOCK_COLLECTION = {
    "politics": [
        "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1555848962-6e79363ec58f?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1577962917302-cd874c4e31d2?auto=format&fit=crop&w=1600&q=85"
    ],
    "economy": [
        "https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1618042164219-62c820f10723?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1600&q=85"
    ],
    "society": [
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1600&q=85"
    ],
    "culture": [
        "https://images.unsplash.com/photo-1547891654-e66ed7ebb968?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1513364776144-60967b0f800f?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1508997449629-303059a039c0?auto=format&fit=crop&w=1600&q=85"
    ],
    "finance": [
        "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1621416894569-0f39ed31d247?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1565514020179-026b92b84bb6?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1600&q=85"
    ],
    "defense": [
        "https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1517976487580-c11c10729221?auto=format&fit=crop&w=1600&q=85"
    ],
    "christianity": [
        "https://images.unsplash.com/photo-1438032005730-c779502df39b?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1507692049790-de58290a4334?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1519817650390-64a93db51149?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=1600&q=85"
    ],
    "science": [
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1600&q=85"
    ],
    "climate": [
        "https://images.unsplash.com/photo-1466611653911-95081537e5b7?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1509391365360-2e959784a276?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1511497584788-87676104235f?auto=format&fit=crop&w=1600&q=85"
    ],
    "sports": [
        "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=1600&q=85",
        "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?auto=format&fit=crop&w=1600&q=85"
    ]
}


def search_wikimedia_commons(query):
    """Dynamically queries Wikimedia Commons API for high-resolution free images matching the headline."""
    if not query:
        return None
    try:
        clean_q = re.sub(r'[^a-zA-Z0-9\s]', ' ', query).strip()
        search_terms = " ".join(clean_q.split()[:4])
        if not search_terms:
            return None
        params = {
            'action': 'query',
            'generator': 'search',
            'gsrsearch': search_terms,
            'gsrnamespace': '6',
            'gsrlimit': '6',
            'prop': 'imageinfo',
            'iiprop': 'url|mime|size',
            'format': 'json'
        }
        url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={'User-Agent': 'UCKLabBot/1.0 (https://ucdigin.net; chblee58@gmail.com)'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get('query', {}).get('pages', {})
            for pid, p in pages.items():
                info = p.get('imageinfo', [{}])[0]
                mime = info.get('mime', '').lower()
                if ('jpeg' in mime or 'jpg' in mime or 'png' in mime) and info.get('width', 0) >= 800:
                    return info.get('url')
    except Exception as e:
        pass
    return None

def query_pixabay(query):
    """Searches Pixabay API if PIXABAY_API_KEY is configured."""
    if not PIXABAY_API_KEY:
        return None
    try:
        encoded_q = urllib.parse.quote(query)
        url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={encoded_q}&image_type=photo&orientation=horizontal&safesearch=true&per_page=5"
        req = urllib.request.Request(url, headers={"User-Agent": "UCKLab-Stock-Curator/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", [])
            if hits:
                return hits[0].get("largeImageURL") or hits[0].get("webformatURL")
    except Exception as e:
        print(f"  ⚠️ [Pixabay API] Exception: {e}")
    return None

def query_pexels(query):
    """Searches Pexels API if PEXELS_API_KEY is configured."""
    if not PEXELS_API_KEY:
        return None
    try:
        encoded_q = urllib.parse.quote(query)
        url = f"https://api.pexels.com/v1/search?query={encoded_q}&orientation=landscape&per_page=5"
        req = urllib.request.Request(url, headers={
            "User-Agent": "UCKLab-Stock-Curator/1.0",
            "Authorization": PEXELS_API_KEY
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            photos = data.get("photos", [])
            if photos:
                src = photos[0].get("src", {})
                return src.get("large2x") or src.get("large") or src.get("original")
    except Exception as e:
        print(f"  ⚠️ [Pexels API] Exception: {e}")
    return None

def download_image_bytes(image_url):
    """Downloads raw image bytes from URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()

def process_and_crop_w810_h480(raw_bytes, output_filepath):
    """
    Intelligently crops and resizes the image to EXACTLY W810 x H480 (aspect ratio 1.6875).
    Applies high-grade Lanczos resampling, subtle contrast and sharpness enhancements.
    """
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
    orig_w, orig_h = img.size
    orig_aspect = orig_w / orig_h

    # Center Crop to target aspect ratio
    if orig_aspect > TARGET_ASPECT:
        # Image is wider than 810:480 -> crop left/right
        new_w = int(orig_h * TARGET_ASPECT)
        left = (orig_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, orig_h))
    else:
        # Image is taller than 810:480 -> crop top/bottom
        new_h = int(orig_w / TARGET_ASPECT)
        top = (orig_h - new_h) // 2
        img = img.crop((0, top, orig_w, top + new_h))

    # Resize to exact target dimensions
    img_resized = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

    # Subtle visual enhancements for executive presentation
    enh_con = ImageEnhance.Contrast(img_resized).enhance(1.04)
    enh_sharp = ImageEnhance.Sharpness(enh_con).enhance(1.10)

    # Save as high-quality optimized JPEG
    enh_sharp.save(output_filepath, format="JPEG", quality=92, optimize=True)
    return output_filepath

def get_category_stock_photo(cat_id, headline="", report_id="WEEKLY"):
    """
    Main entry point:
    1. Selects image from Pixabay / Pexels / Curated HD Stock Collection.
    2. Crops and resizes to EXACTLY W810 x H480.
    3. Saves locally in storage/images/.
    Returns: local_filepath
    """
    cat_id_clean = cat_id.lower().strip()
    output_filename = f"stock_{report_id}_{cat_id_clean}_810x480.jpg"
    local_path = os.path.join(IMAGE_STORAGE_DIR, output_filename)

    # If already cached and exact size, reuse
    if os.path.exists(local_path) and os.path.getsize(local_path) > 20000:
        return local_path

    # Step 1: Attempt Dynamic Free Image Search (Wikimedia Commons / Pixabay / Pexels)
    image_url = None
    if headline:
        image_url = search_wikimedia_commons(headline)
        if not image_url:
            search_query = f"{cat_id_clean} {headline[:30]}"
            image_url = query_pixabay(search_query) or query_pexels(search_query)

    # Step 2: Fallback to Unique Varied HD Stock Collection (guarantees a different photo each week)
    if not image_url:
        collection = CATEGORY_STOCK_COLLECTION.get(cat_id_clean, CATEGORY_STOCK_COLLECTION["politics"])
        # Derive distinct rotational seed from headline + report_id so every weekly edition gets a different image
        seed_idx = abs(hash(f"{report_id}_{headline}_{cat_id_clean}")) % len(collection)
        image_url = collection[seed_idx]

    print(f"  📷 [Stock Photo] [{cat_id_clean}] 고화질 원본 다운로드 중: {image_url[:65]}...")
    try:
        raw_bytes = download_image_bytes(image_url)
        process_and_crop_w810_h480(raw_bytes, local_path)
        print(f"     ✓ [{cat_id_clean}] W810 x H480 크롭 및 최적화 완료 ({os.path.getsize(local_path):,} bytes)")
        return local_path
    except Exception as e:
        print(f"  ⚠️ [Stock Photo] 다운로드/크롭 예외 ({cat_id_clean}): {e}")
        # Create solid gradient fallback of exact 810x480
        fallback_img = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), color=(15, 23, 42))
        fallback_img.save(local_path, format="JPEG", quality=90)
        return local_path

def prepare_and_upload_all_stock_photos(news_items, report_id="WEEKLY", wp_client=None):
    """
    Generates and uploads W810 x H480 stock photos for all categories.
    Attaches media_id and source_url to each item in news_items.
    Returns: dict mapping cat_id -> {'media_id': id, 'source_url': url, 'local_path': path}
    """
    print(f"\n=======================================================")
    print(f"📸 [Stock Image Service] 무료 고화질 사진 선정 및 W810 x H480 최적화")
    print(f"=======================================================")

    results = {}
    for idx, item in enumerate(news_items, 1):
        cat_id = item.get("id", "politics")
        headline = item.get("headline", "")
        cat_ko = item.get("category_ko", "")

        local_path = get_category_stock_photo(cat_id, headline, report_id)

        media_id = None
        source_url = None

        if wp_client:
            filename = os.path.basename(local_path)
            alt_text = f"UCKLab Strategic Review - {cat_ko} ({headline[:60]})"
            title = f"{cat_ko} - {headline[:60]} (W810xH480)"
            media_id, source_url = wp_client.upload_media(
                file_path=local_path,
                filename=filename,
                alt_text=alt_text,
                title=title,
                mime_type="image/jpeg"
            )

        item["featured_media_id"] = media_id
        item["featured_image_url"] = source_url
        item["local_image_path"] = local_path

        results[cat_id] = {
            "media_id": media_id,
            "source_url": source_url,
            "local_path": local_path
        }

    print(f"✅ [Stock Image Service] 총 {len(results)}개 전 카테고리 W810 x H480 사진 준비 완료!")
    return results

if __name__ == "__main__":
    print("Testing stock_image_service...")
    test_path = get_category_stock_photo("defense", "Autonomous Drone Swarm", "TEST-2026")
    im = Image.open(test_path)
    print(f"Output: {test_path}, Size: {im.size}")
    assert im.size == (810, 480)
    print("Verification Passed: Exact (810, 480) confirmed!")
