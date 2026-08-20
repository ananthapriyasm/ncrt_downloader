# main.py

from downloader import download_all_subjects
from metadata_writer import build_metadata, save_metadata
import json

def main():
    print("🚀 Starting NCERT Class 10 Chapter Downloader...")
    print("=" * 60)

    # Step 1: Download all chapters
    results = download_all_subjects()

    # Step 2: Build and save metadata
    metadata = build_metadata(results)
    save_metadata(metadata)

    # Step 3: Print summary
    print("\n" + "=" * 60)
    print("📊 DOWNLOAD SUMMARY:")
    for subject, chapters in results.items():
        downloaded = sum(1 for c in chapters if c["status"] == "downloaded")
        unchanged = sum(1 for c in chapters if c["status"] == "unchanged")
        errors = sum(1 for c in chapters if c["status"] == "error")
        print(f"  {subject:30s} | ✅ {downloaded} new/updated | ⏭️ {unchanged} unchanged | ❌ {errors} errors")

    print("\n✅ Done!")

if __name__ == "__main__":
    main()