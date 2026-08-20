# downloader.py

import os
import hashlib
import requests
from config import NCERT_BASE_URL, PDF_SAVE_DIR, SUBJECTS

def get_pdf_url(book_code: str, chapter_num: int) -> str:
    """Build NCERT chapter PDF URL."""
    chapter_str = str(chapter_num).zfill(2)
    return f"{NCERT_BASE_URL}{book_code}{chapter_str}.pdf"

def compute_md5(filepath: str) -> str:
    """Compute MD5 hash of existing local file."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def compute_md5_bytes(content: bytes) -> str:
    """Compute MD5 hash of downloaded content bytes."""
    return hashlib.md5(content).hexdigest()

def download_chapter(subject_key: str, subject_config: dict, chapter_num: int) -> dict:
    """
    Download a single chapter PDF.
    Returns a result dict with status, path, hash, and change flag.
    """
    book_code = subject_config["book_code"]
    url = get_pdf_url(book_code, chapter_num)

    # Build save path
    subject_dir = os.path.join(PDF_SAVE_DIR, subject_key)
    os.makedirs(subject_dir, exist_ok=True)
    chapter_str = str(chapter_num).zfill(2)
    filename = f"chapter_{chapter_str}.pdf"
    filepath = os.path.join(subject_dir, filename)

    result = {
        "chapter": chapter_num,
        "url": url,
        "local_path": filepath,
        "status": "skipped",
        "changed": False,
        "md5": None,
        "error": None
    }

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 404:
            result["status"] = "not_found"
            return result

        response.raise_for_status()
        new_content = response.content
        new_hash = compute_md5_bytes(new_content)

        # Check if file already exists and compare hash
        if os.path.exists(filepath):
            existing_hash = compute_md5(filepath)
            if existing_hash == new_hash:
                result["status"] = "unchanged"
                result["md5"] = new_hash
                return result
            else:
                result["changed"] = True  # Content has changed!

        # Save the (new or updated) PDF
        with open(filepath, "wb") as f:
            f.write(new_content)

        result["status"] = "downloaded"
        result["md5"] = new_hash
        print(f"  ✅ {'UPDATED' if result['changed'] else 'NEW'}: {filepath}")

    except requests.RequestException as e:
        result["status"] = "error"
        result["error"] = str(e)
        print(f"  ❌ ERROR: {url} → {e}")

    return result

def download_all_subjects() -> dict:
    """Download all subjects and chapters. Returns full results map."""
    all_results = {}

    for subject_key, subject_config in SUBJECTS.items():
        print(f"\n📘 Downloading: {subject_config['title']}")
        subject_results = []

        for ch_num in range(1, subject_config["chapters"] + 1):
            result = download_chapter(subject_key, subject_config, ch_num)
            subject_results.append(result)

        all_results[subject_key] = subject_results

    return all_results