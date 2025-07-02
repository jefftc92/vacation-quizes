import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Hotel data: (image_path, short_reason)
hotels = {
    "Bellagio Resort & Casino": ("Hotels/Bellagio.jpg", "You love luxury, iconic Vegas style, and the finer things in life."),
    "Wynn Las Vegas": ("Hotels/Wynn Las Vegas.jpg", "You want modern luxury and the best of everything on the Strip."),
    "The Cosmopolitan of Las Vegas": ("Hotels/The Cosmopolitan.jpg", "Trendy, stylish, and always in the know—this is your scene."),
    "ARIA Resort and Casino": ("Hotels/Aria.jpg", "You appreciate sleek design, tech, and world-class dining."),
    "Caesars Palace": ("Hotels/Caesars Palace.jpg", "You want timeless elegance and classic Vegas experiences."),
    "Flamingo Las Vegas Hotel & Casino": ("Hotels/Flamingo.png", "You love retro vibes and a lively, central Strip location."),
    "Nobu Hotel at Caesars Palace": ("Hotels/Nobu Hotel.jpg", "You want boutique luxury and exclusive experiences."),
    "Paris Las Vegas Hotel & Casino": ("Hotels/Paris Hotel Las Vegas.jpg", "You're romantic, cultured, and love European charm."),
    "Planet Hollywood Resort & Casino": ("Hotels/Planet Hollywood.jpg", "You want high-energy, pop-culture fun, and endless entertainment."),
    "Waldorf Astoria Las Vegas": ("Hotels/Waldorf Astoria.jpg", "You prefer refined, understated luxury and tranquility."),
    "The Cromwell Las Vegas": ("Hotels/The Cromwell.jpg", "You love boutique style and a personal Vegas experience."),
    "Harrah's Las Vegas Hotel & Casino": ("Hotels/Harrahs.png", "You want classic Vegas fun and great value in the center of it all."),
    "Flamingo, a Hilton Grand Vacations Club": ("Hotels/Flamingo a Hilton Grand Vacations Club.png", "You want comfort, space, and a homey Vegas stay."),
    "Horseshoe Las Vegas": ("Hotels/Horseshoe.png", "You love classic gaming and a fresh take on old-school Vegas."),
    "The LINQ Hotel + Experience": ("Hotels/The LINQ.png", "You want a vibrant, social, and modern Vegas vibe."),
    "The Palazzo at The Venetian Resort Las Vegas": ("Hotels/Palazzo.jpg", "You love Italian elegance and spacious luxury suites."),
    "Treasure Island Hotel and Casino": ("Hotels/Treasure Island.jpg", "You want adventure, value, and a unique themed stay."),
    "The Venetian Resort Las Vegas": ("Hotels/The Venetian Resort Las Vegas.jpg", "You love romance, art, and a taste of Italy in Vegas."),
    "Best Western Plus Casino Royale - Center Strip": ("Hotels/Best Western Plus Casino.png", "You want comfort, value, and a perfect Strip location."),
    "Encore at Wynn Las Vegas": ("Hotels/Encore at Wynn.jpg", "You want intimate luxury and exclusive nightlife."),
    "Hilton Grand Vacations Club Paradise Las Vegas": ("Hotels/Hilton_Grand_Vacation_Club.jpg", "You want a residential-style stay with all the comforts of home."),
    "Hilton Vacation Club Polo Towers Las Vegas": ("Hotels/Hilton Vacation Club Polo Towers Las Vegas.png", "You want home-like comfort and a great Strip location."),
    "MGM Grand Hotel & Casino": ("Hotels/MGM Grand.jpg", "You want high-energy, big entertainment, and endless options."),
    "New York-New York Hotel and Casino": ("Hotels/New York New York.jpg", "You love iconic themes and a lively, fun atmosphere."),
    "NoMad Las Vegas": ("Hotels/NoMad Las Vegas.png", "You want boutique luxury and a unique, intimate experience."),
    "Park MGM Las Vegas": ("Hotels/Park MGM Las Vegas.jpg", "You love boutique style, art, and a central location."),
    "W Las Vegas": ("Hotels/The W Las Vegas.png", "You want trendy, stylish, and unique Vegas experiences."),
    "Excalibur Hotel and Casino": ("Hotels/EXCALIBUR_HOTEL.jpg", "You want classic Vegas fun and a family-friendly vibe."),
    "Fontainebleau Las Vegas": ("Hotels/Fontainebleau.png", "You want the newest luxury and cutting-edge design."),
    "Four Seasons Hotel Las Vegas": ("Hotels/Four Seasons Hotel Las Vegas.png", "You want refined, non-gaming luxury and peace."),
    "Resorts World Las Vegas": ("Hotels/ResortWorld Las Vegas.jpg", "You want the newest, trendiest, and most high-tech resort."),
    "Luxor Las Vegas": ("Hotels/Luxor Las Vegas.png", "You love unique architecture and classic Vegas value."),
    "Mandalay Bay Resort and Casino": ("Hotels/Mandalay Bay.jpg", "You want a tropical vibe, beach, and relaxation."),
    "Nirvana Hotel": ("Hotels/Nirvana Hotel.jpg", "You want value, comfort, and a no-frills Strip stay."),
    "Circus Circus Las Vegas": ("Hotels/Circus Circus.jpg", "You want classic fun, family-friendly entertainment, and value."),
    "SAHARA Las Vegas": ("Hotels/Sahara Las Vegas.jpg", "You want boutique style and a reimagined Vegas classic."),
    "The STRAT Hotel, Casino & Tower": ("Hotels/Stratosphere.jpg", "You want thrills, views, and a unique Vegas experience.")
}

QUIZ_NAME = "Which Las Vegas Hotel Are You?"

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

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 630
SAFE_PADDING = 60  # Safe area from all edges for text/branding
CARD_RADIUS = 36
CARD_PADDING = 36
CARD_WIDTH = CANVAS_WIDTH - (SAFE_PADDING * 2)
CARD_HEIGHT = CANVAS_HEIGHT - (SAFE_PADDING * 2)

for hotel, (img_path, reason) in hotels.items():
    try:
        # Colorful ray background
        bg = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), (255, 80, 40))
        draw = ImageDraw.Draw(bg)
        # Draw rays
        num_rays = 18
        center = (CANVAS_WIDTH//2, CANVAS_HEIGHT//2)
        for i in range(num_rays):
            angle1 = (2*math.pi/num_rays) * i
            angle2 = (2*math.pi/num_rays) * (i+1)
            r = CANVAS_WIDTH
            x1 = center[0] + r * math.cos(angle1)
            y1 = center[1] + r * math.sin(angle1)
            x2 = center[0] + r * math.cos(angle2)
            y2 = center[1] + r * math.sin(angle2)
            color = (255, 120, 60) if i % 2 == 0 else (255, 80, 40)
            draw.polygon([center, (x1, y1), (x2, y2)], fill=color)
        
        # White card - positioned in the safe area
        card_x0 = SAFE_PADDING
        card_y0 = SAFE_PADDING
        card = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (255,255,255,255))
        card_draw = ImageDraw.Draw(card)
        card_draw.rounded_rectangle([(0,0),(CARD_WIDTH,CARD_HEIGHT)], radius=CARD_RADIUS, fill=(255,255,255,255))
        
        # Calculate content areas to fit within card
        content_padding = 36
        content_width = CARD_WIDTH - (content_padding * 2)
        
        # Hotel name (top, bold, left-aligned)
        title_font = get_font(44)
        title = hotel
        title_x = content_padding
        title_y = 28
        card_draw.text((title_x, title_y), title, font=title_font, fill=(40,40,40))
        
        # Hotel image (fixed area, object-fit: cover)
        img = Image.open(img_path).convert('RGB')
        img_area_w = content_width
        img_area_h = 260  # Slightly smaller to allow more space for text
        # Crop/resize image to fill area (object-fit: cover)
        aspect_card = img_area_w / img_area_h
        aspect_img = img.width / img.height
        if aspect_img > aspect_card:
            # Image is wider than area: crop width
            new_w = int(img.height * aspect_card)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        else:
            # Image is taller than area: crop height
            new_h = int(img.width / aspect_card)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
        img = img.resize((img_area_w, img_area_h), Image.LANCZOS)
        img_x = content_padding
        img_y = title_y + 60
        card.paste(img, (img_x, img_y))
        
        # Description (fixed 3 lines)
        desc_font = get_font(28)
        desc = f"The best Las Vegas hotel for you is {hotel}. {reason}"
        desc_max_width = content_width
        
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            line = ''
            for word in words:
                test = line + (' ' if line else '') + word
                w = card_draw.textbbox((0,0), test, font=font)[2]
                if w > max_width and line:
                    lines.append(line)
                    line = word
                else:
                    line = test
            if line:
                lines.append(line)
            return lines
        
        desc_lines = wrap_text(desc, desc_font, desc_max_width)
        # Force to 3 lines
        if len(desc_lines) > 3:
            # Truncate and add ellipsis
            desc_lines = desc_lines[:3]
            if len(desc_lines[2]) > 3:
                desc_lines[2] = desc_lines[2][:-3] + '...'
        elif len(desc_lines) < 3:
            desc_lines += [''] * (3 - len(desc_lines))
        
        desc_y = img_y + img_area_h + 18
        for line in desc_lines:
            card_draw.text((title_x, desc_y), line, font=desc_font, fill=(60,60,60))
            desc_y += 36
        
        # Divider line
        divider_y = desc_y + 10
        card_draw.line([(title_x, divider_y), (content_padding + content_width, divider_y)], fill=(220,220,220), width=4)
        
        # Quiz name at the bottom, but at least 60px from the bottom of the card
        quiz_font = get_font(32)
        quiz_text = QUIZ_NAME
        quiz_bbox = card_draw.textbbox((0,0), quiz_text, font=quiz_font)
        quiz_height = quiz_bbox[3] - quiz_bbox[1]
        quiz_y = CARD_HEIGHT - SAFE_PADDING - quiz_height  # 60px from bottom
        card_draw.text((title_x, quiz_y), quiz_text, font=quiz_font, fill=(255,80,40))
        
        # Composite card onto background
        bg.paste(card, (card_x0, card_y0), card)
        
        # Save
        out_name = f"share_images/share_{sanitize_filename(hotel)}.jpg"
        bg.save(out_name, quality=95)
        print(f"Generated: {out_name}")
    except Exception as e:
        print(f"Error processing {hotel}: {e}") 