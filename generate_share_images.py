import os
import re
from PIL import Image, ImageDraw, ImageFont

# Hotel data extracted from your code (name: image path)
hotels = {
    "Bellagio Resort & Casino": "Hotels/Bellagio.jpg",
    "Wynn Las Vegas": "Hotels/Wynn Las Vegas.jpg",
    "The Cosmopolitan of Las Vegas": "Hotels/The Cosmopolitan.jpg",
    "ARIA Resort and Casino": "Hotels/Aria.jpg",
    "Caesars Palace": "Hotels/Caesars Palace.jpg",
    "Flamingo Las Vegas Hotel & Casino": "Hotels/Flamingo.png",
    "Nobu Hotel at Caesars Palace": "Hotels/Nobu Hotel.jpg",
    "Paris Las Vegas Hotel & Casino": "Hotels/Paris Hotel Las Vegas.jpg",
    "Planet Hollywood Resort & Casino": "Hotels/Planet Hollywood.jpg",
    "Waldorf Astoria Las Vegas": "Hotels/Waldorf Astoria.jpg",
    "The Cromwell Las Vegas": "Hotels/The Cromwell.jpg",
    "Harrah's Las Vegas Hotel & Casino": "Hotels/Harrahs.png",
    "Flamingo, a Hilton Grand Vacations Club": "Hotels/Flamingo a Hilton Grand Vacations Club.png",
    "Horseshoe Las Vegas": "Hotels/Horseshoe.png",
    "The LINQ Hotel + Experience": "Hotels/The LINQ.png",
    "The Palazzo at The Venetian Resort Las Vegas": "Hotels/Palazzo.jpg",
    "Treasure Island Hotel and Casino": "Hotels/Treasure Island.jpg",
    "The Venetian Resort Las Vegas": "Hotels/The Venetian Resort Las Vegas.jpg",
    "Best Western Plus Casino Royale - Center Strip": "Hotels/Best Western Plus Casino.png",
    "Encore at Wynn Las Vegas": "Hotels/Encore at Wynn.jpg",
    "Hilton Grand Vacations Club Paradise Las Vegas": "Hotels/Hilton_Grand_Vacation_Club.jpg",
    "Hilton Vacation Club Polo Towers Las Vegas": "Hotels/Hilton Vacation Club Polo Towers Las Vegas.png",
    "MGM Grand Hotel & Casino": "Hotels/MGM Grand.jpg",
    "New York-New York Hotel and Casino": "Hotels/New York New York.jpg",
    "NoMad Las Vegas": "Hotels/NoMad Las Vegas.png",
    "Park MGM Las Vegas": "Hotels/Park MGM Las Vegas.jpg",
    "W Las Vegas": "Hotels/The W Las Vegas.png",
    "Excalibur Hotel and Casino": "Hotels/EXCALIBUR_HOTEL.jpg",
    "Fontainebleau Las Vegas": "Hotels/Fontainebleau.png",
    "Four Seasons Hotel Las Vegas": "Hotels/Four Seasons Hotel Las Vegas.png",
    "Resorts World Las Vegas": "Hotels/ResortWorld Las Vegas.jpg",
    "Luxor Las Vegas": "Hotels/Luxor Las Vegas.png",
    "Mandalay Bay Resort and Casino": "Hotels/Mandalay Bay.jpg",
    "Nirvana Hotel": "Hotels/Nirvana Hotel.jpg",
    "Circus Circus Las Vegas": "Hotels/Circus Circus.jpg",
    "SAHARA Las Vegas": "Hotels/Sahara Las Vegas.jpg",
    "The STRAT Hotel, Casino & Tower": "Hotels/Stratosphere.jpg"
}

# Try to use a bold, playful font (fallback to default if not found)
def get_font(size):
    font_paths = [
        "/Library/Fonts/Impact.ttf",  # Mac Impact
        "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",  # Linux Impact
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # DejaVu
        "/Library/Fonts/Arial Bold.ttf",  # Mac Arial Bold
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

os.makedirs('share_images', exist_ok=True)

for hotel, img_path in hotels.items():
    try:
        img = Image.open(img_path).convert('RGB')
        width, height = img.size
        # Banner height
        banner_height = int(height * 0.22)
        total_height = height + banner_height
        # Create new image with space for banner
        new_img = Image.new('RGB', (width, total_height), (255,255,255))
        new_img.paste(img, (0,0))
        draw = ImageDraw.Draw(new_img)
        # Banner background (BuzzFeed blue)
        banner_color = (0, 120, 255)
        draw.rectangle([0, height, width, total_height], fill=banner_color)
        # Text
        text = f"My perfect Las Vegas hotel match is {hotel}"
        font_size = int(banner_height * 0.38)
        font = get_font(font_size)
        # Center text
        # Use textbbox for Pillow 10+ compatibility
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = (width - text_width) // 2
        text_y = height + (banner_height - text_height) // 2
        # Draw text (black with white outline for pop)
        outline_range = 2
        for ox in range(-outline_range, outline_range+1):
            for oy in range(-outline_range, outline_range+1):
                if ox != 0 or oy != 0:
                    draw.text((text_x+ox, text_y+oy), text, font=font, fill=(0,0,0))
        draw.text((text_x, text_y), text, font=font, fill=(255,255,255))
        # Save
        out_name = f"share_images/share_{sanitize_filename(hotel)}.jpg"
        new_img.save(out_name, quality=95)
        print(f"Generated: {out_name}")
    except Exception as e:
        print(f"Error processing {hotel}: {e}") 