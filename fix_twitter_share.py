#!/usr/bin/env python3
import os
import re

def fix_twitter_share(filepath):
    """Update Twitter share to only include the link, no text"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the hotel name for logging
    hotel_name_match = re.search(r'const hotelName = "([^"]+)"', content)
    hotel_name = hotel_name_match.group(1) if hotel_name_match else "Unknown"
    
    # Update the Twitter share URL to only include the link
    old_twitter_pattern = r'const twitterUrl = `https://twitter\.com/intent/tweet\?text=\${text}&url=\${encodeURIComponent\(shareUrl\)}`;'
    new_twitter_url = 'const twitterUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}`;'
    
    if re.search(old_twitter_pattern, content):
        content = re.sub(old_twitter_pattern, new_twitter_url, content)
        print(f"✅ Updated Twitter share for {hotel_name}")
        return content
    else:
        print(f"⚠️  No Twitter share found for {hotel_name}")
        return content

def main():
    """Update all hotel result pages"""
    result_files = [f for f in os.listdir('.') if f.startswith('result_') and f.endswith('.html')]
    
    if not result_files:
        print("No result files found!")
        return
    
    print(f"Found {len(result_files)} hotel result files")
    print("Updating Twitter share functionality...")
    
    for filepath in sorted(result_files):
        try:
            updated_content = fix_twitter_share(filepath)
            with open(filepath, 'w') as f:
                f.write(updated_content)
        except Exception as e:
            print(f"❌ Error updating {filepath}: {e}")
    
    print(f"\n✅ Updated Twitter share for {len(result_files)} hotel result pages")
    print("Twitter share now only includes the link (no text)")

if __name__ == "__main__":
    main() 