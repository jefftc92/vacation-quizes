#!/usr/bin/env python3
import os
import re

def fix_copy_button_desktop(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove any .copy-results and .copy-results svg rules outside media queries
    content = re.sub(r'\.copy-results \{[^}]*\}', '', content)
    content = re.sub(r'\.copy-results svg \{[^}]*\}', '', content)

    # Insert the correct desktop CSS just before </style>
    desktop_css = '''.copy-results {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ffdc00 60%, #ff7a00 100%);
    box-shadow: 0 2px 8px rgba(255,208,0,0.10);
    cursor: pointer;
    border: none;
    transition: background 0.2s, color 0.2s, transform 0.2s;
    margin: 0;
    padding: 0;
}
.copy-results svg {
    width: 28px;
    height: 28px;
    display: block;
}
'''
    content = re.sub(r'</style>', desktop_css + '\n</style>', content, count=1)

    with open(filepath, 'w') as f:
        f.write(content)
    return True

def main():
    result_files = [f for f in os.listdir('.') if f.startswith('result_') and f.endswith('.html') and f != 'result_template.html']
    print("Fixing copy button for desktop on all hotel result pages...")
    print("=" * 60)
    fixed_count = 0
    for filename in sorted(result_files):
        print(f"Fixing: {filename}")
        if fix_copy_button_desktop(filename):
            fixed_count += 1
            print(f"  ✓ Fixed")
        else:
            print(f"  ✗ Failed")
    print("=" * 60)
    print(f"Fixed {fixed_count} out of {len(result_files)} files")
    print("\nCopy button desktop fix complete!")
    print("- Desktop: 48px/28px, inline-flex centering, no extra margin/padding")

if __name__ == "__main__":
    main() 