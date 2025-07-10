#!/usr/bin/env python3
import os
import re

def get_hotel_safe_name(filename):
    """Extract hotel safe name from result filename"""
    # Remove 'result_' prefix and '.html' suffix
    safe_name = filename.replace('result_', '').replace('.html', '')
    return safe_name

def fix_copy_button_logic(filepath):
    """Fix the copy button to copy only the share link"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    hotel_safe_name = get_hotel_safe_name(os.path.basename(filepath))
    
    # Find the hotel name from the content
    hotel_name_match = re.search(r'const hotelName = "([^"]+)"', content)
    if not hotel_name_match:
        print(f"Could not find hotel name in {filepath}")
        return False
    
    hotel_name = hotel_name_match.group(1)
    
    # Create the new JavaScript section
    new_js = f'''    <script>
        // Set up social sharing for this specific result page
        const hotelName = "{hotel_name}";
        const shareSafeName = "{hotel_safe_name}";
        const shareUrl = `https://travelhen.com/share_${{shareSafeName}}.html`;
        const text = encodeURIComponent(`I got ${{hotelName}} as my perfect Las Vegas hotel match! Take the quiz to find yours!`);

        // Facebook share
        document.getElementById('share-facebook').onclick = function(e) {{
            e.preventDefault();
            const fbUrl = `https://www.facebook.com/sharer/sharer.php?u=${{encodeURIComponent(shareUrl)}}`;
            window.open(fbUrl, '_blank');
        }};
        // Twitter share
        document.getElementById('share-twitter').onclick = function(e) {{
            e.preventDefault();
            const twitterUrl = `https://twitter.com/intent/tweet?text=${{text}}&url=${{encodeURIComponent(shareUrl)}}`;
            window.open(twitterUrl, '_blank');
        }};
        // Copy results button
        document.getElementById('copy-results').onclick = function() {{
            if (navigator.clipboard && window.isSecureContext) {{
                navigator.clipboard.writeText(shareUrl).then(function() {{
                    const button = document.getElementById('copy-results');
                    const originalTitle = button.title;
                    button.title = 'Copied!';
                    button.classList.add('copied');
                    setTimeout(function() {{
                        button.title = originalTitle;
                        button.classList.remove('copied');
                    }}, 2000);
                }});
            }} else {{
                // Fallback for older browsers
                const tempInput = document.createElement('input');
                tempInput.value = shareUrl;
                document.body.appendChild(tempInput);
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                const button = document.getElementById('copy-results');
                const originalTitle = button.title;
                button.title = 'Copied!';
                button.classList.add('copied');
                setTimeout(function() {{
                    button.title = originalTitle;
                    button.classList.remove('copied');
                }}, 2000);
            }}
        }};
    </script>'''
    
    # Replace the entire script section
    # Find the script section and replace it
    script_pattern = r'<script>\s*// Set up social sharing.*?</script>'
    if re.search(script_pattern, content, re.DOTALL):
        content = re.sub(script_pattern, new_js, content, flags=re.DOTALL)
        
        # Also update the button title
        content = re.sub(r'title="Copy link to result"', 'title="Copy share link"', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    else:
        print(f"Could not find script section in {filepath}")
        return False

def main():
    """Fix all result pages"""
    result_files = [f for f in os.listdir('.') if f.startswith('result_') and f.endswith('.html') and f != 'result_template.html']
    
    print("Fixing copy buttons for all hotel result pages...")
    print("=" * 60)
    
    fixed_count = 0
    for filename in sorted(result_files):
        hotel_name = filename.replace('result_', '').replace('.html', '').replace('_', ' ')
        print(f"Fixing: {hotel_name}")
        
        if fix_copy_button_logic(filename):
            fixed_count += 1
            print(f"  ✓ Fixed")
        else:
            print(f"  ✗ Failed")
    
    print("=" * 60)
    print(f"Fixed {fixed_count} out of {len(result_files)} files")

if __name__ == "__main__":
    main() 