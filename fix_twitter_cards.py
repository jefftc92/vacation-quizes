#!/usr/bin/env python3
import os
import re

def fix_twitter_cards(filepath):
    """Add missing Twitter Card meta tags for proper thumbnail display"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the hotel name for logging
    hotel_name_match = re.search(r'const hotelName = "([^"]+)"', content)
    hotel_name = hotel_name_match.group(1) if hotel_name_match else "Unknown"
    
    # Check if twitter:site and twitter:creator tags are missing
    has_twitter_site = re.search(r'<meta name="twitter:site"', content)
    has_twitter_creator = re.search(r'<meta name="twitter:creator"', content)
    
    if not has_twitter_site or not has_twitter_creator:
        # Find the position after the existing Twitter Card tags
        twitter_card_pos = content.find('<!-- Twitter Card Meta Tags -->')
        if twitter_card_pos != -1:
            # Find the end of the Twitter Card section
            end_pos = content.find('</head>', twitter_card_pos)
            if end_pos != -1:
                # Insert missing Twitter Card tags
                additional_tags = '''
    <meta name="twitter:site" content="@vacationquizzes" />
    <meta name="twitter:creator" content="@vacationquizzes" />
    <meta name="twitter:image:alt" content="My perfect Las Vegas hotel match is {}!" />'''.format(hotel_name)
                
                # Insert before </head>
                content = content[:end_pos] + additional_tags + content[end_pos:]
                print(f"✅ Added missing Twitter Card tags for {hotel_name}")
                return content
    
    print(f"ℹ️  Twitter Card tags already present for {hotel_name}")
    return content

def main():
    """Update all hotel result pages"""
    result_files = [f for f in os.listdir('.') if f.startswith('result_') and f.endswith('.html')]
    
    if not result_files:
        print("No result files found!")
        return
    
    print(f"Found {len(result_files)} hotel result files")
    print("Adding missing Twitter Card meta tags...")
    
    for filepath in sorted(result_files):
        try:
            updated_content = fix_twitter_cards(filepath)
            with open(filepath, 'w') as f:
                f.write(updated_content)
        except Exception as e:
            print(f"❌ Error updating {filepath}: {e}")
    
    print(f"\n✅ Updated Twitter Card meta tags for {len(result_files)} hotel result pages")
    print("Twitter thumbnails should now display properly")

if __name__ == "__main__":
    main() 