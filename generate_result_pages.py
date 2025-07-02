import os
import re

# Hotel data (name, description)
hotels = {
    "Bellagio Resort & Casino": "You're sophisticated, elegant, and appreciate the finer things in life! The Bellagio is your perfect match with its iconic fountains, luxury accommodations, fine dining, and central Strip location. You'll love the upscale pool area, world-class art gallery, and the elegant casino. The Bellagio perfectly balances classic Vegas glamour with modern luxury - just like you!",
    "Wynn Las Vegas": "Modern luxury, world-class dining, and a refined casino experience. Wynn Las Vegas is perfect for those who want the best of everything on the north Strip.",
    "The Cosmopolitan of Las Vegas": "Trendy, stylish, and always in the know - that's you! The Cosmopolitan matches your Instagram-worthy lifestyle with its chic design, stunning terrace rooms, and vibrant atmosphere. You'll love the Marquee dayclub/nightclub, eclectic restaurant collection, and the perfect center-Strip location. The Cosmopolitan attracts a fashionable crowd that appreciates both luxury and a lively social scene - your perfect match!",
    "ARIA Resort and Casino": "Modern, sophisticated, and tech-savvy - the ARIA is your ideal Vegas match! You appreciate contemporary luxury with all the latest amenities. ARIA's sleek design, cutting-edge technology, and world-class dining options perfectly complement your refined taste. The stunning pool deck and exclusive nightlife venues will make your stay unforgettable!",
    "Caesars Palace": "You appreciate timeless elegance and iconic Vegas experiences! Caesars Palace matches your taste for the classics with its Roman-inspired luxury, legendary status, and central Strip location. You'll love the Garden of the Gods pool oasis, Forum Shops, and celebrity chef restaurants. Caesars Palace offers that perfect blend of Vegas history and modern indulgence you're looking for!",
    "Flamingo Las Vegas Hotel & Casino": "Retro-loving, drawn to Vegas history, and looking for a lively atmosphere - the Flamingo is your ideal match! As the oldest resort still operating on the Strip, it offers that classic Vegas vibe with modern amenities. You'll love the lush wildlife habitat, vibrant casino, and the perfect center-Strip location at a value-conscious price point!",
    "Nobu Hotel at Caesars Palace": "Sophisticated, design-conscious, and appreciative of unique experiences - Nobu Hotel is your perfect match! This boutique hotel within Caesars Palace offers an intimate, luxurious atmosphere with world-class dining and service. You'll love the exclusive pool access, celebrity chef restaurants, and the perfect blend of privacy and excitement!",
    "Paris Las Vegas Hotel & Casino": "Romantic, cultured, and drawn to European charm - Paris Las Vegas is your ideal match! You'll be transported to the City of Light with its Eiffel Tower, charming streets, and authentic French cuisine. The romantic atmosphere, diverse dining options, and central Strip location make this the perfect choice for your Vegas adventure!",
    "Planet Hollywood Resort & Casino": "Pop-culture enthusiast, trend-conscious, and looking for a high-energy experience - Planet Hollywood is your perfect Vegas match! You'll love the contemporary Hollywood vibe, celebrity-chef restaurants, and vibrant casino floor. With its center-Strip location and connection to the Miracle Mile Shops, this resort offers endless entertainment options for your Vegas adventure!",
    "Waldorf Astoria Las Vegas": "Refined, sophisticated, and appreciative of understated luxury - the Waldorf Astoria is your perfect match! This non-gaming hotel offers an elegant escape from the typical Vegas experience. You'll love the impeccable service, sophisticated dining options, and the serene atmosphere that lets you enjoy Vegas on your own terms!",
    "The Cromwell Las Vegas": "Trendy, boutique-loving, and looking for an intimate Vegas experience - The Cromwell is your perfect match! This boutique hotel offers a more personal, sophisticated take on Vegas. You'll love the stylish rooms, celebrity chef restaurants, and the perfect location for exploring the Strip's best attractions!",
    "Harrah's Las Vegas Hotel & Casino": "Fun-loving, value-conscious, and looking for a classic Vegas experience - Harrah's is your ideal match! You'll enjoy the lively casino floor, diverse dining options, and the perfect center-Strip location. Harrah's offers that quintessential Vegas experience with comfortable accommodations and entertainment options that won't break the bank!",
    "Flamingo, a Hilton Grand Vacations Club": "Family-oriented, comfort-seeking, and looking for a home away from home - Flamingo HGV is your perfect match! These spacious suites offer all the comforts of home with the excitement of Vegas just steps away. You'll love the full kitchens, separate living areas, and access to all the Flamingo's amenities!",
    "Horseshoe Las Vegas": "Gaming enthusiast, value-conscious, and looking for a classic Vegas experience - Horseshoe is your ideal match! Formerly Bally's, this rebranded property offers a fresh take on classic Vegas gaming. You'll love the updated casino floor, diverse dining options, and the perfect center-Strip location!",
    "The LINQ Hotel + Experience": "Social, fun-loving, and looking for a vibrant Vegas experience - The LINQ is your perfect match! You'll love the energetic atmosphere, the famous LINQ Promenade, and the High Roller observation wheel. This hotel offers a modern, social experience perfect for those who want to be in the middle of the action!",
    "The Palazzo at The Venetian Resort Las Vegas": "Spacious, luxurious, and appreciative of Italian elegance - The Palazzo is your ideal match! You'll love the all-suite accommodations, world-class shopping, and sophisticated atmosphere. The Palazzo offers a more refined take on the Venetian experience, perfect for those who appreciate luxury and space!",
    "Treasure Island Hotel and Casino": "Adventure-seeking, value-conscious, and looking for a unique Vegas experience - Treasure Island is your perfect match! You'll love the pirate-themed atmosphere, diverse dining options, and the perfect location for exploring the Strip. TI offers a fun, themed experience without breaking the bank!",
    "The Venetian Resort Las Vegas": "Romantic, artistic, and drawn to European charm - the Venetian is your ideal Vegas match! You'll be transported to Italy with the Grand Canal Shoppes, gondola rides, and Renaissance-inspired architecture. The all-suite accommodations, world-class spa, and diverse dining options perfectly suit your taste for luxury with a touch of whimsy!",
    "Best Western Plus Casino Royale - Center Strip": "Budget-conscious, location-focused, and looking for a comfortable stay - Casino Royale is your perfect match! You'll appreciate the value-priced rooms, on-site casino, and the perfect center-Strip location. This hotel offers a comfortable, no-frills experience that lets you save money for Vegas adventures!",
    "Encore at Wynn Las Vegas": "Sophisticated, detail-oriented, and appreciative of the finer things - Encore is your perfect match! You'll be enchanted by the elegant design, world-class dining, and exclusive nightlife venues. Encore offers a more intimate, luxurious experience that complements the Wynn's offerings!",
    "Hilton Grand Vacations Club Paradise Las Vegas": "Family-focused, comfort-seeking, and looking for a residential-style stay - HGV Paradise is your ideal match! These spacious suites offer all the comforts of home with the excitement of Vegas nearby. You'll love the full kitchens, separate living areas, and the perfect location for exploring the Strip!",
    "Hilton Vacation Club Polo Towers Las Vegas": "Comfort-seeking, value-conscious, and looking for a home-like experience - Polo Towers is your perfect match! These spacious suites offer all the comforts of home with the excitement of Vegas just steps away. You'll love the full kitchens, separate living areas, and the perfect location for exploring the Strip!",
    "MGM Grand Hotel & Casino": "Energetic, fun-loving, and ready for anything - the MGM Grand is your perfect Vegas match! You'll love the massive casino, incredible entertainment options, and the famous Wet Republic Ultra Pool. With its central location and endless dining and nightlife options, the MGM Grand offers the high-energy Vegas experience you're looking for!",
    "New York-New York Hotel and Casino": "Fun-loving, drawn to iconic themes, and looking for a lively atmosphere - New York-New York is your perfect Vegas match! You'll love the Big Apple skyline, roller coaster, and energetic casino floor. With diverse dining options, live entertainment, and a central Strip location, this resort captures the excitement of both NYC and Vegas in one unforgettable experience!",
    "NoMad Las Vegas": "Sophisticated, design-conscious, and looking for a unique experience - NoMad is your perfect match! This boutique hotel within Park MGM offers an intimate, luxurious atmosphere with world-class dining and service. You'll love the exclusive pool access, celebrity chef restaurants, and the perfect blend of privacy and excitement!",
    "Park MGM Las Vegas": "Cultured, design-conscious, and appreciative of boutique experiences - Park MGM is your perfect Vegas match! You'll love the sophisticated yet approachable atmosphere, curated art collection, and intimate venues. The stunning pool, Eataly food hall, and proximity to T-Mobile Arena make this the ideal home base for your Vegas adventure!",
    "W Las Vegas": "Trendy, stylish, and looking for a unique Vegas experience - W Las Vegas is your perfect match! This boutique hotel offers a more personal, sophisticated take on Vegas. You'll love the stylish rooms, celebrity chef restaurants, and the perfect location for exploring the Strip's best attractions!",
    "Excalibur Hotel and Casino": "Family-oriented, budget-conscious, and looking for classic Vegas fun - the Excalibur is your ideal match! You'll enjoy the medieval castle theme, family-friendly atmosphere, and affordable dining options. The Excalibur offers that quintessential Vegas experience with comfortable accommodations and entertainment options that won't break the bank!",
    "Fontainebleau Las Vegas": "Sophisticated, design-conscious, and looking for the newest luxury experience - Fontainebleau is your perfect match! This brand-new resort offers cutting-edge design, world-class dining, and exclusive nightlife venues. You'll love the stunning architecture, luxurious accommodations, and the perfect location for exploring the Strip!",
    "Four Seasons Hotel Las Vegas": "Refined, sophisticated, and appreciative of understated luxury - the Four Seasons is your perfect match! This non-gaming hotel offers an elegant escape from the typical Vegas experience. You'll love the impeccable service, sophisticated dining options, and the serene atmosphere that lets you enjoy Vegas on your own terms!",
    "Resorts World Las Vegas": "Cutting-edge, trendsetting, and drawn to the newest experiences - Resorts World is your ideal Vegas match! As the newest resort on the Strip, it offers state-of-the-art technology, modern design, and fresh entertainment concepts. You'll love discovering the diverse dining collection, multiple pool experiences, and next-generation casino gaming!",
    "Luxor Las Vegas": "Value-conscious, drawn to unique architecture, and looking for a classic Vegas experience - the Luxor is your perfect match! You'll be impressed by the iconic pyramid design, massive atrium, and diverse entertainment options. The Luxor offers that quintessential Vegas experience with comfortable accommodations at a price point that keeps your budget happy!",
    "Mandalay Bay Resort and Casino": "Beach-loving, relaxation-focused, and drawn to tropical vibes - Mandalay Bay is your ideal Vegas match! You'll be amazed by the 11-acre beach complex with real sand, wave pool, and lazy river. The aquarium, diverse dining options, and spacious rooms with spectacular views perfectly complement your laid-back yet luxurious vacation style!",
    "Nirvana Hotel": "Budget-conscious, location-focused, and looking for a comfortable stay - Nirvana Hotel is your perfect match! You'll appreciate the value-priced rooms and the perfect center-Strip location. This hotel offers a comfortable, no-frills experience that lets you save money for Vegas adventures!",
    "Circus Circus Las Vegas": "Family-oriented, budget-conscious, and looking for classic Vegas fun - Circus Circus is your ideal match! You'll enjoy the circus acts, family-friendly atmosphere, and affordable dining options. The Adventuredome theme park, comfortable accommodations, and entertainment options make this the perfect choice for family vacations!",
    "SAHARA Las Vegas": "Style-conscious, appreciative of reinvention, and looking for a boutique experience - SAHARA Las Vegas is your ideal match! Recently reimagined with a sleek, modern design, this historic property offers an intimate yet luxurious atmosphere. You'll love the sophisticated rooms, curated dining options, and the more relaxed north Strip location!",
    "The STRAT Hotel, Casino & Tower": "Thrill-seeking, view-loving, and looking for unique experiences - The STRAT is your perfect Vegas match! You'll be amazed by the iconic tower with its observation deck and heart-pounding thrill rides. The STRAT offers comfortable accommodations at a great value, plus that one-of-a-kind Vegas skyline experience you won't find anywhere else!"
}

# Share image path pattern
SHARE_IMAGE_PATTERN = "share_images/share_{}.jpg"
# Result page URL pattern (GitHub Pages style)
RESULT_PAGE_URL_PATTERN = "https://jefftc92.github.io/vacation-quizes/{}"
SHARE_IMAGE_ABS_URL_PATTERN = "https://jefftc92.github.io/vacation-quizes/{}"

hotel_links = {
    "Bellagio Resort & Casino": "https://expedia.com/affiliates/las-vegas-hotels-bellagio.3x57zyG",
    "Wynn Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-wynn-las-vegas",
    "The Cosmopolitan of Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-the-cosmopolitan-of-las-vegas.Auc1Nr0",
    "ARIA Resort and Casino": "https://expedia.com/affiliates/las-vegas-hotels-aria-resort-casino.Uokiz9Q",
    "Caesars Palace": "https://expedia.com/affiliates/las-vegas-hotels-caesars-palace-resort-casino.TSg28OE",
    "Flamingo Las Vegas Hotel & Casino": "https://expedia.com/affiliates/las-vegas-hotels-flamingo-las-vegas-hotel-casino.ItYrKT6",
    "Nobu Hotel at Caesars Palace": "https://expedia.com/affiliates/las-vegas-hotels-nobu-hotel-at-caesars-palace.pCymfNS",
    "Paris Las Vegas Hotel & Casino": "https://expedia.com/affiliates/las-vegas-hotels-paris-las-vegas-resort-casino.01j1EF3",
    "Planet Hollywood Resort & Casino": "https://expedia.com/affiliates/las-vegas-hotels-planet-hollywood-resort-casino.1I43suF",
    "Waldorf Astoria Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-waldorf-astoria-las-vegas.KtBGh9h",
    "The Cromwell Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-the-cromwell.eIF9i3z",
    "Harrah's Las Vegas Hotel & Casino": "https://expedia.com/affiliates/las-vegas-hotels-harrahs-hotel-and-casino-las-vegas.pyn3WyV",
    "Flamingo, a Hilton Grand Vacations Club": "https://expedia.com/affiliates/las-vegas-hotels-hilton-grand-vacations-at-the-flamingo.q56tJH0",
    "Horseshoe Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-horseshoe-las-vegas.X6VGNld",
    "The LINQ Hotel + Experience": "https://expedia.com/affiliates/las-vegas-hotels-the-linq-hotel-experience.ONDqGs1",
    "The Palazzo at The Venetian Resort Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-the-palazzo-at-the-venetian.H2cxO6M",
    "Treasure Island Hotel and Casino": "https://expedia.com/affiliates/las-vegas-hotels-ti-treasure-island-hotel-and-casino.2OuNVCg",
    "The Venetian Resort Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-the-venetian-resort-las-vegas.NK9yuzb",
    "Best Western Plus Casino Royale - Center Strip": "https://expedia.com/affiliates/las-vegas-hotels-best-western-plus-casino-royale-center-strip.7OVjc4U",
    "Encore at Wynn Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-encore-at-wynn-las-vegas.P350Tha",
    "Hilton Grand Vacations Club Paradise Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-hilton-grand-vacations-on-paradise.13Z5yW1",
    "Hilton Vacation Club Polo Towers Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-polo-towers.rKodcUQ",
    "MGM Grand Hotel & Casino": "https://expedia.com/affiliates/las-vegas-hotels-mgm-grand-hotel-casino.Nq7doFx",
    "New York-New York Hotel and Casino": "https://expedia.com/affiliates/las-vegas-hotels-new-york-new-york-hotel-casino.2nWbiVn",
    "NoMad Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-nomad-las-vegas.AICGyYI",
    "Park MGM Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-park-mgm-las-vegas.UKcRlqb",
    "W Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-delano-las-vegas-at-mandalay-bay.rqdedQU",
    "Excalibur Hotel and Casino": "https://expedia.com/affiliates/las-vegas-hotels-excalibur-hotel-casino.PwrARmh",
    "Fontainebleau Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-fontainebleau-las-vegas.3P4kVL4",
    "Four Seasons Hotel Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-four-seasons-hotel-las-vegas.pH28KRm",
    "Resorts World Las Vegas": "https://www.rwlasvegas.com/",
    "Luxor Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-luxor-hotel-and-casino.zUzJxI2",
    "Mandalay Bay Resort and Casino": "https://expedia.com/affiliates/las-vegas-hotels-mandalay-bay-resort-and-casino.pAZqzIe",
    "Nirvana Hotel": "https://expedia.com/affiliates/las-vegas-hotels-nirvana-hotel.CG25A5n",
    "Circus Circus Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-circus-circus-hotel.khABrrs",
    "SAHARA Las Vegas": "https://expedia.com/affiliates/las-vegas-hotels-sahara-las-vegas.cXegFrm",
    "The STRAT Hotel, Casino & Tower": "https://expedia.com/affiliates/las-vegas-hotels-the-strat-hotel.gIsoxPI"
}

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)

# Load template
with open('result_template.html', 'r') as f:
    template = f.read()

for hotel, desc in hotels.items():
    safe_name = sanitize_filename(hotel)
    share_img = SHARE_IMAGE_PATTERN.format(safe_name)
    share_img_abs = SHARE_IMAGE_ABS_URL_PATTERN.format(share_img)
    result_page = f"result_{safe_name}.html"
    result_url = RESULT_PAGE_URL_PATTERN.format(result_page)
    hotel_link = hotel_links.get(hotel, "#")
    html = template.replace("{{HOTEL_NAME}}", hotel)
    html = html.replace("{{HOTEL_DESC}}", desc)
    html = html.replace("{{SHARE_IMAGE_URL}}", share_img)
    html = html.replace("{{SHARE_IMAGE_ABS_URL}}", share_img_abs)
    html = html.replace("{{RESULT_PAGE_URL}}", result_url)
    html = html.replace("{{HOTEL_LINK}}", hotel_link)
    with open(result_page, 'w') as outf:
        outf.write(html)
    print(f"Generated: {result_page}") 