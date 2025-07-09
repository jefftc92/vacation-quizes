#!/usr/bin/env python3
import os
import re

def fix_twitter_cards_comprehensive(filepath):
    """Comprehensive fix for Twitter Card meta tags"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the hotel name for logging
    hotel_name_match = re.search(r'const hotelName = "([^"]+)"', content)
    hotel_name = hotel_name_match.group(1) if hotel_name_match else "Unknown"
    
    # Extract the share image URL from existing meta tags
    og_image_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    if og_image_match:
        image_url = og_image_match.group(1)
    else:
        print(f"❌ No og:image found for {hotel_name}")
        return content
    
    # Extract the title and description
    og_title_match = re.search(r'<meta property="og:title" content="([^"]+)"', content)
    og_desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', content)
    
    title = og_title_match.group(1) if og_title_match else f"My perfect Las Vegas hotel match is {hotel_name}!"
    description = og_desc_match.group(1) if og_desc_match else "Take the quiz to find your perfect Las Vegas hotel match!"
    
    # Remove any existing Twitter Card tags that might be misplaced
    content = re.sub(r'<meta name="twitter:[^"]+"[^>]*>', '', content)
    
    # Find the position right after the existing Open Graph tags
    og_tags_end = content.find('<!-- Twitter Card Meta Tags -->')
    if og_tags_end == -1:
        # If no Twitter Card comment, find the end of Open Graph tags
        og_tags_end = content.find('</head>')
    
    if og_tags_end != -1:
        # Create comprehensive Twitter Card tags
        twitter_tags = f'''
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:site" content="@vacationquizzes" />
    <meta name="twitter:creator" content="@vacationquizzes" />
    <meta name="twitter:title" content="{title}" />
    <meta name="twitter:description" content="{description}" />
    <meta name="twitter:image" content="{image_url}" />
    <meta name="twitter:image:alt" content="{title}" />
    <meta name="twitter:domain" content="jefftc92.github.io" />'''
        
        # Insert the Twitter tags before </head>
        content = content[:og_tags_end] + twitter_tags + content[og_tags_end:]
        print(f"✅ Added comprehensive Twitter Card tags for {hotel_name}")
        return content
    
    print(f"❌ Could not find proper insertion point for {hotel_name}")
    return content

def main():
    """Update all hotel result pages"""
    result_files = [f for f in os.listdir('.') if f.startswith('result_') and f.endswith('.html')]
    
    if not result_files:
        print("No result files found!")
        return
    
    print(f"Found {len(result_files)} hotel result files")
    print("Adding comprehensive Twitter Card meta tags...")
    
    for filepath in sorted(result_files):
        try:
            updated_content = fix_twitter_cards_comprehensive(filepath)
            with open(filepath, 'w') as f:
                f.write(updated_content)
        except Exception as e:
            print(f"❌ Error updating {filepath}: {e}")
    
    print(f"\n✅ Updated Twitter Card meta tags for {len(result_files)} hotel result pages")
    print("Twitter thumbnails should now display properly with comprehensive meta tags")

if __name__ == "__main__":
    main() 