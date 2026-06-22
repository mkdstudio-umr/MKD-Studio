#!/usr/bin/env python3
"""
Metadata refinement: fix title tags and meta descriptions.
Removes photography-as-category patterns from descriptions.
Fixes AURA title format.
"""
import re, os

BASE = os.path.expanduser('~/Desktop/GitHub/MKD-Studio/studies')

# slug -> {title, desc, og_title, og_desc, tw_title, tw_desc}
# None = leave unchanged
UPDATES = {
    'aime-leon-dore': {
        'title':    'Aimé Leon Dore, London / mkd STUDIO',
        'desc':     'An editorial study of Aimé Leon Dore in London. Sport, material and the ritual of a retail space that operates entirely on its own terms.',
        'og_title': 'Aimé Leon Dore, London / mkd STUDIO',
        'og_desc':  'An editorial study of Aimé Leon Dore, London. Sport, material and the ritual of a space that operates on its own terms.',
        'tw_title': 'Aimé Leon Dore, London / mkd STUDIO',
        'tw_desc':  'An editorial study of Aimé Leon Dore, London. Sport, material and the ritual of a space that operates on its own terms.',
    },
    'al-mourjan': {
        'title':    None,
        'desc':     'An editorial study of the Al Mourjan Business Lounge at Hamad International Airport, Doha. A departure lounge designed for stillness in one of the world\'s busiest terminals.',
        'og_title': None,
        'og_desc':  'An editorial study of Al Mourjan Business Lounge, Doha. A departure lounge designed for stillness.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Al Mourjan Business Lounge, Doha. A departure lounge designed for stillness.',
    },
    'alila-ubud': {
        'title':    None,
        'desc':     'An editorial study of Alila Ubud, Bali. Stone, timber and thatched architecture built among the trees of the Ayung River valley. Hospitality shaped by landscape, stillness and material.',
        'og_title': None,
        'og_desc':  'An editorial study of Alila Ubud, Bali. Stone, timber and thatched architecture shaped by landscape and stillness.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Alila Ubud, Bali. Stone, timber and thatched architecture shaped by landscape and stillness.',
    },
    'antalya': {
        'title':    None,
        'desc':     'An editorial study of Antalya, Türkiye. The Taurus mountains descending into the Mediterranean, limestone ridges and a coastline that holds its own character.',
        'og_title': None,
        'og_desc':  'An editorial study of Antalya, Türkiye. The Taurus mountains, limestone ridges and the Mediterranean coastline.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Antalya, Türkiye. The Taurus mountains, limestone ridges and the Mediterranean coastline.',
    },
    'apotek-57': {
        'title':    None,
        'desc':     'An editorial study of Apotek 57 in Copenhagen. A converted pharmacy that moves between café, gallery and design without belonging entirely to any one of them.',
        'og_title': None,
        'og_desc':  'An editorial study of Apotek 57, Copenhagen. A converted pharmacy that moves between café, gallery and design.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Apotek 57, Copenhagen. A converted pharmacy that moves between café, gallery and design.',
    },
    'aura': {
        'title':    'AURA, Dubai / mkd STUDIO',
        'desc':     'An editorial study of AURA, Dubai. The infinity pool above Palm Jumeirah, where water, sky and the city\'s skyline meet at elevation.',
        'og_title': 'AURA, Dubai / mkd STUDIO',
        'og_desc':  'An editorial study of AURA, Dubai. The infinity pool above Palm Jumeirah, where water, sky and skyline meet at elevation.',
        'tw_title': 'AURA, Dubai / mkd STUDIO',
        'tw_desc':  'An editorial study of AURA, Dubai. The infinity pool above Palm Jumeirah, where water, sky and skyline meet at elevation.',
    },
    'buttery-bakery': {
        'title':    None,
        'desc':     'An editorial study of The Buttery Bakery in Msheireb, Doha. A bakery built from timber, brass and stone with a single coherent visual language across every surface.',
        'og_title': None,
        'og_desc':  'An editorial study of The Buttery Bakery, Doha. A bakery built from timber, brass and stone with a single visual language.',
        'tw_title': None,
        'tw_desc':  'An editorial study of The Buttery Bakery, Doha. A bakery built from timber, brass and stone with a single visual language.',
    },
    'byredo-leeds': {
        'title':    None,
        'desc':     'An editorial study of the BYREDO boutique in Leeds. Fragrance, restraint and considered luxury in a city not typically associated with either.',
        'og_title': None,
        'og_desc':  'An editorial study of BYREDO, Leeds. Fragrance, restraint and considered luxury in Yorkshire.',
        'tw_title': None,
        'tw_desc':  'An editorial study of BYREDO, Leeds. Fragrance, restraint and considered luxury in Yorkshire.',
    },
    'copenhagen': {
        'title':    None,
        'desc':     'An editorial study of Copenhagen, Denmark. The city\'s ordinary rhythm: Nyhavn, quiet streets, café culture and waterfront light on an unhurried day.',
        'og_title': None,
        'og_desc':  'An editorial study of Copenhagen, Denmark. Nyhavn, quiet streets, café culture and waterfront light.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Copenhagen, Denmark. Nyhavn, quiet streets, café culture and waterfront light.',
    },
    'corfu-after-arrival': {
        'title':    None,
        'desc':     'An editorial study of Corfu Town, Greece. Venetian facades, arched courtyards, old town passages and evening light in the hours after arrival.',
        'og_title': None,
        'og_desc':  'An editorial study of Corfu Town, Greece. Venetian facades, arched courtyards and evening light.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Corfu Town, Greece. Venetian facades, arched courtyards and evening light.',
    },
    'dar-el-bacha': {
        'title':    None,
        'desc':     'An editorial study of Dar El Bacha in Marrakech, Morocco. Moroccan craft, courtyard geometry and a building that carries its age without ceremony.',
        'og_title': None,
        'og_desc':  'An editorial study of Dar El Bacha, Marrakech. Moroccan craft, courtyard geometry and a building that carries its age quietly.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Dar El Bacha, Marrakech. Moroccan craft, courtyard geometry and a building that carries its age quietly.',
    },
    'earth-doha': {
        'title':    None,
        'desc':     'An editorial study of EARTH restaurant in Msheireb Downtown Doha. Texture, material and atmosphere in a dining space shaped by the landscape around it.',
        'og_title': None,
        'og_desc':  'An editorial study of EARTH, Msheireb Doha. Texture, material and atmosphere in a dining space shaped by landscape.',
        'tw_title': None,
        'tw_desc':  'An editorial study of EARTH, Msheireb Doha. Texture, material and atmosphere in a dining space shaped by landscape.',
    },
    'fueguia-milan': {
        'title':    None,
        'desc':     'An editorial study of FUEGUIA 1833 in Milan. An Argentine fragrance house and a collection assembled slowly, held within a space that reflects the same unhurried logic.',
        'og_title': None,
        'og_desc':  'An editorial study of FUEGUIA 1833, Milan. An Argentine fragrance house and a collection assembled slowly.',
        'tw_title': None,
        'tw_desc':  'An editorial study of FUEGUIA 1833, Milan. An Argentine fragrance house and a collection assembled slowly.',
    },
    'gewan-island': {
        'title':    None,
        'desc':     'An editorial study of Palms at Gewan Island, Doha. Morning light, water and unhurried service on Qatar\'s man-made island.',
        'og_title': None,
        'og_desc':  'An editorial study of Gewan Island, Doha. Morning light, water and unhurried service in Qatar.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Gewan Island, Doha. Morning light, water and unhurried service in Qatar.',
    },
    'giorgio-armani-tennis-classic': {
        'title':    None,
        'desc':     'An editorial study of the Giorgio Armani Tennis Classic at the Hurlingham Club, London. Brand partnership, atmosphere and temporary occupation within an established institution.',
        'og_title': None,
        'og_desc':  'An editorial study of the Giorgio Armani Tennis Classic, Hurlingham Club. Atmosphere and temporary occupation within an established institution.',
        'tw_title': None,
        'tw_desc':  'An editorial study of the Giorgio Armani Tennis Classic, Hurlingham Club. Atmosphere and temporary occupation within an established institution.',
    },
    'guerlain-katara': {
        'title':    None,
        'desc':     'An editorial study of the Guerlain boutique at Katara Cultural Village, Doha. Perfume presented with the attention and restraint of hospitality rather than retail.',
        'og_title': None,
        'og_desc':  'An editorial study of Guerlain at Katara, Doha. Perfume presented with the restraint of hospitality.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Guerlain at Katara, Doha. Perfume presented with the restraint of hospitality.',
    },
    'host-qatar-2022': {
        'title':    None,
        'desc':     'An editorial study of Qatar hosting the 2022 FIFA World Cup. Hospitality infrastructure, temporary architecture and a country receiving the world for the first time.',
        'og_title': None,
        'og_desc':  'An editorial study of Qatar at the 2022 FIFA World Cup. Hospitality, temporary architecture and a country receiving the world.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Qatar at the 2022 FIFA World Cup. Hospitality, temporary architecture and a country receiving the world.',
    },
    'ilkley-open': {
        'title':    None,
        'desc':     'An editorial study of the Lexus Ilkley Open in Ilkley, Yorkshire. A professional grass court tennis tournament, its partnerships and atmosphere, set against the moorland above the town.',
        'og_title': None,
        'og_desc':  'An editorial study of the Lexus Ilkley Open, Yorkshire. Tennis, partnership and atmosphere on the grass courts above Ilkley.',
        'tw_title': None,
        'tw_desc':  'An editorial study of the Lexus Ilkley Open, Yorkshire. Tennis, partnership and atmosphere on the grass courts above Ilkley.',
    },
    'italia-after-the-heat': {
        'title':    None,
        'desc':     'An editorial study of Italy in the late season. Florence, Venice and the surfaces held by Italian light: warm facades, ceremonial shadows, stone, water and evening distance.',
        'og_title': None,
        'og_desc':  'An editorial study of Italy in the late season. Florence, Venice and the surfaces held by Italian light.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Italy in the late season. Florence, Venice and the surfaces held by Italian light.',
    },
    'jihae-hwang': {
        'title':    None,
        'desc':     'An editorial study of Jihae Hwang\'s garden A Letter From A Million Years Past at RHS Chelsea Flower Show 2023. A Korean mountain landscape reconstructed in the grounds of the Royal Hospital Chelsea.',
        'og_title': None,
        'og_desc':  'An editorial study of Jihae Hwang\'s garden at Chelsea 2023. A Korean mountain landscape reconstructed in London.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Jihae Hwang\'s garden at Chelsea 2023. A Korean mountain landscape reconstructed in London.',
    },
    'kaawa-manchester': {
        'title':    None,
        'desc':     'An editorial study of KAAWA in Manchester. Light after dark and the particular atmosphere of a space that finds its register in the evening hours.',
        'og_title': None,
        'og_desc':  'An editorial study of KAAWA, Manchester. Light after dark and the atmosphere of an evening space.',
        'tw_title': None,
        'tw_desc':  'An editorial study of KAAWA, Manchester. Light after dark and the atmosphere of an evening space.',
    },
    'kew-under-glass': {
        'title':    None,
        'desc':     'An editorial study of Kew Gardens in London. Victorian glasshouses, planted rooms, water and the cultivated stillness of a great garden in public life.',
        'og_title': None,
        'og_desc':  'An editorial study of Kew Gardens, London. Victorian glasshouses, planted rooms and cultivated stillness.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Kew Gardens, London. Victorian glasshouses, planted rooms and cultivated stillness.',
    },
    'kuala-lumpur': {
        'title':    None,
        'desc':     'An editorial study of Kuala Lumpur, Malaysia. A city between worlds: its architecture, streets and the contrasts held within a rapidly grown capital.',
        'og_title': None,
        'og_desc':  'An editorial study of Kuala Lumpur, Malaysia. Architecture, streets and the contrasts of a rapidly grown capital.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Kuala Lumpur, Malaysia. Architecture, streets and the contrasts of a rapidly grown capital.',
    },
    'leeds': {
        'title':    None,
        'desc':     'An editorial study of coffee culture in Leeds. A city developing a distinctive taste for itself, one interior at a time.',
        'og_title': None,
        'og_desc':  'An editorial study of coffee culture in Leeds. A city developing a distinctive taste for itself.',
        'tw_title': None,
        'tw_desc':  'An editorial study of coffee culture in Leeds. A city developing a distinctive taste for itself.',
    },
    'lisbon': {
        'title':    None,
        'desc':     'An editorial study of Lisbon, Portugal. Old material, tiled facades, thresholds and the quality of light at the edge of day.',
        'og_title': None,
        'og_desc':  'An editorial study of Lisbon, Portugal. Old material, tiled facades and the quality of light at the edge of day.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Lisbon, Portugal. Old material, tiled facades and the quality of light at the edge of day.',
    },
    'loro-piana-milan': {
        'title':    None,
        'desc':     'An editorial study of Loro Piana in Milan. Afternoon light, Italian material and the quiet confidence of a luxury house that has nothing left to prove.',
        'og_title': None,
        'og_desc':  'An editorial study of Loro Piana, Milan. Afternoon light, Italian material and quiet confidence.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Loro Piana, Milan. Afternoon light, Italian material and quiet confidence.',
    },
    'madrid-held-in-light': {
        'title':    None,
        'desc':     'An editorial study of Madrid, Spain. Civic architecture, the Palacio de Cristal, interior thresholds and the rooftops of old Madrid in afternoon light.',
        'og_title': None,
        'og_desc':  'An editorial study of Madrid, Spain. Civic architecture, the Palacio de Cristal and old rooftops in afternoon light.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Madrid, Spain. Civic architecture, the Palacio de Cristal and old rooftops in afternoon light.',
    },
    'paddock': {
        'title':    None,
        'desc':     'An editorial study from inside the Formula One paddock at Silverstone. Access, infrastructure and the temporary city assembled behind the race each season.',
        'og_title': None,
        'og_desc':  'An editorial study from the Formula One paddock at Silverstone. Access, infrastructure and the temporary city behind the race.',
        'tw_title': None,
        'tw_desc':  'An editorial study from the Formula One paddock at Silverstone. Access, infrastructure and the temporary city behind the race.',
    },
    'paris': {
        'title':    None,
        'desc':     'An editorial study of Paris, France. The Louvre, its courtyards and galleries, and the streets that hold the city together.',
        'og_title': None,
        'og_desc':  'An editorial study of Paris, France. The Louvre, its courtyards and galleries, and the streets that hold the city together.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Paris, France. The Louvre, its courtyards and galleries, and the streets that hold the city together.',
    },
    'penny-bun': {
        'title':    None,
        'desc':     'An editorial study of The Penny Bun in Askwith, Yorkshire. A restored inn near Ilkley that holds the pace of a Yorkshire morning without effort.',
        'og_title': None,
        'og_desc':  'An editorial study of The Penny Bun, Askwith. A restored inn near Ilkley and the pace of a Yorkshire morning.',
        'tw_title': None,
        'tw_desc':  'An editorial study of The Penny Bun, Askwith. A restored inn near Ilkley and the pace of a Yorkshire morning.',
    },
    'place-vendome': {
        'title':    None,
        'desc':     'An editorial study of Place Vendôme in Lusail, Doha. A landmark luxury retail and hospitality development and the theatre it creates around commerce in Qatar.',
        'og_title': None,
        'og_desc':  'An editorial study of Place Vendôme, Doha. A landmark development and the theatre it creates around luxury in Qatar.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Place Vendôme, Doha. A landmark development and the theatre it creates around luxury in Qatar.',
    },
    'porto-after-the-river': {
        'title':    None,
        'desc':     'An editorial study of Porto, Portugal. The Douro river, tram lines, stained glass interiors and café life in a city that holds its character carefully.',
        'og_title': None,
        'og_desc':  'An editorial study of Porto, Portugal. The Douro river, tram lines, stained glass and café life.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Porto, Portugal. The Douro river, tram lines, stained glass and café life.',
    },
    'qatar-at-night': {
        'title':    None,
        'desc':     'An editorial study of Doha after midnight. The city\'s skyline, waterfront architecture and the particular quiet that settles over Qatar in the late hours.',
        'og_title': None,
        'og_desc':  'An editorial study of Doha after midnight. Skyline, waterfront architecture and the quiet of late-night Qatar.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Doha after midnight. Skyline, waterfront architecture and the quiet of late-night Qatar.',
    },
    'qatar-gp': {
        'title':    None,
        'desc':     'An editorial study of the Qatar Grand Prix at Lusail International Circuit. Formula One under floodlights, paddock operations and the scale of a race weekend in the desert.',
        'og_title': None,
        'og_desc':  'An editorial study of the Qatar Grand Prix, Lusail. Formula One under floodlights and the scale of a desert race weekend.',
        'tw_title': None,
        'tw_desc':  'An editorial study of the Qatar Grand Prix, Lusail. Formula One under floodlights and the scale of a desert race weekend.',
    },
    'qinwan-msheireb': {
        'title':    None,
        'desc':     'An editorial study of QINWAN in Msheireb Downtown Doha. Welcome, interior craft and the particular language of Qatari hospitality at the table.',
        'og_title': None,
        'og_desc':  'An editorial study of QINWAN, Msheireb Doha. Welcome, interior craft and Qatari hospitality at the table.',
        'tw_title': None,
        'tw_desc':  'An editorial study of QINWAN, Msheireb Doha. Welcome, interior craft and Qatari hospitality at the table.',
    },
    'raffles-doha': {
        'title':    None,
        'desc':     'An editorial study of Raffles Doha. Arched architecture, considered hospitality and the particular weight that the name carries in Qatar.',
        'og_title': None,
        'og_desc':  'An editorial study of Raffles Doha. Arched architecture and considered hospitality in Qatar.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Raffles Doha. Arched architecture and considered hospitality in Qatar.',
    },
    'raffles-singapore': {
        'title':    None,
        'desc':     'An editorial study of Raffles Singapore. A colonial institution, its gardens, long corridors and the permanence of a hotel that has outlasted everything around it.',
        'og_title': None,
        'og_desc':  'An editorial study of Raffles Singapore. A colonial institution, its gardens and the permanence of a hospitality legacy.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Raffles Singapore. A colonial institution, its gardens and the permanence of a hospitality legacy.',
    },
    'ralphs-london': {
        'title':    None,
        'desc':     'An editorial study of Ralph\'s Coffee in London. Seasonal structures, brand signage and an atmosphere built into the city for a few weeks each winter.',
        'og_title': None,
        'og_desc':  'An editorial study of Ralph\'s Coffee, London. Seasonal structures and an atmosphere built into the city each winter.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Ralph\'s Coffee, London. Seasonal structures and an atmosphere built into the city each winter.',
    },
    'rhs-chelsea': {
        'title':    None,
        'desc':     'An editorial study of the RHS Chelsea Flower Show 2022. Temporary gardens built from stone, water, timber and planting at the world\'s most closely watched horticultural show.',
        'og_title': None,
        'og_desc':  'An editorial study of RHS Chelsea 2022. Temporary gardens built from stone, water, timber and planting.',
        'tw_title': None,
        'tw_desc':  'An editorial study of RHS Chelsea 2022. Temporary gardens built from stone, water, timber and planting.',
    },
    'singapore': {
        'title':    None,
        'desc':     'An editorial study of Singapore. Marina Bay, Gardens by the Bay, Kampong Glam and the waterfront at night. Glass, gardens and a city built at extraordinary scale.',
        'og_title': None,
        'og_desc':  'An editorial study of Singapore. Marina Bay, Gardens by the Bay and a city built at extraordinary scale.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Singapore. Marina Bay, Gardens by the Bay and a city built at extraordinary scale.',
    },
    'tangier-ii': {
        'title':    None,
        'desc':     'A second editorial study of Tangier, Morocco. Interior surfaces: tadelakt, terrazzo, terracotta and the architecture of a city that keeps its character on the inside.',
        'og_title': None,
        'og_desc':  'A second editorial study of Tangier, Morocco. Interior surfaces: tadelakt, terrazzo, terracotta and inward character.',
        'tw_title': None,
        'tw_desc':  'A second editorial study of Tangier, Morocco. Interior surfaces: tadelakt, terrazzo, terracotta and inward character.',
    },
    'tangier': {
        'title':    None,
        'desc':     'An editorial study of Tangier, Morocco. A city at the edge of continents: streets, light and a Mediterranean character that moves at its own pace.',
        'og_title': None,
        'og_desc':  'An editorial study of Tangier, Morocco. Streets, light and a Mediterranean character at its own pace.',
        'tw_title': None,
        'tw_desc':  'An editorial study of Tangier, Morocco. Streets, light and a Mediterranean character at its own pace.',
    },
    'the-mosque': {
        'title':    None,
        'desc':     'An editorial study of the Education City Mosque in Doha, Qatar. Geometry, calligraphy, light and the quiet occupation of a contemporary Islamic landmark.',
        'og_title': None,
        'og_desc':  'An editorial study of the Education City Mosque, Doha. Geometry, calligraphy and light in a contemporary Islamic landmark.',
        'tw_title': None,
        'tw_desc':  'An editorial study of the Education City Mosque, Doha. Geometry, calligraphy and light in a contemporary Islamic landmark.',
    },
    'the-ned-doha': {
        'title':    None,
        'desc':     'An editorial study of The Ned Doha. Scale held quietly, considered hospitality and the atmosphere of a hotel that understands its own weight.',
        'og_title': None,
        'og_desc':  'An editorial study of The Ned Doha. Scale held quietly and considered hospitality in Qatar.',
        'tw_title': None,
        'tw_desc':  'An editorial study of The Ned Doha. Scale held quietly and considered hospitality in Qatar.',
    },
    'the-ritz-carlton-bali': {
        'title':    None,
        'desc':     'An editorial study of The Ritz-Carlton, Bali. Arrival, dusk and atmosphere after dark. Stone, palm, water and the light that remains after sunset in Nusa Dua.',
        'og_title': None,
        'og_desc':  'An editorial study of The Ritz-Carlton, Bali. Arrival, dusk and the light that remains after sunset in Nusa Dua.',
        'tw_title': None,
        'tw_desc':  'An editorial study of The Ritz-Carlton, Bali. Arrival, dusk and the light that remains after sunset in Nusa Dua.',
    },
    'the-spaces-between': {
        'title':    None,
        'desc':     'An editorial study series on Formula One away from the racing line. The spaces, people and systems at Silverstone and Lusail that hold the sport in place.',
        'og_title': None,
        'og_desc':  'An editorial study series on Formula One at Silverstone and Lusail. The spaces and systems away from the racing line.',
        'tw_title': None,
        'tw_desc':  'An editorial study series on Formula One at Silverstone and Lusail. The spaces and systems away from the racing line.',
    },
    'waiting-for-dusk': {
        'title':    None,
        'desc':     'An editorial study of the Commercial Bank Qatar Masters at Doha Golf Club. Time, atmosphere and the light of a tournament day measured in increments towards evening.',
        'og_title': None,
        'og_desc':  'An editorial study of the Qatar Masters, Doha Golf Club. Time, atmosphere and light moving slowly towards evening.',
        'tw_title': None,
        'tw_desc':  'An editorial study of the Qatar Masters, Doha Golf Club. Time, atmosphere and light moving slowly towards evening.',
    },
}

def replace_attr(content, attr_name, new_value):
    """Replace a meta tag's content attribute."""
    # For <title> tag
    if attr_name == 'title':
        return re.sub(r'<title>[^<]*</title>', f'<title>{new_value}</title>', content)
    # For meta name="description"
    if attr_name == 'desc':
        return re.sub(
            r'(<meta name="description" content=")[^"]*(")',
            lambda m: m.group(1) + new_value + m.group(2),
            content
        )
    # For og:title
    if attr_name == 'og_title':
        return re.sub(
            r'(<meta property="og:title" content=")[^"]*(")',
            lambda m: m.group(1) + new_value + m.group(2),
            content
        )
    # For og:description
    if attr_name == 'og_desc':
        return re.sub(
            r'(<meta property="og:description" content=")[^"]*(")',
            lambda m: m.group(1) + new_value + m.group(2),
            content
        )
    # For twitter:title
    if attr_name == 'tw_title':
        return re.sub(
            r'(<meta name="twitter:title" content=")[^"]*(")',
            lambda m: m.group(1) + new_value + m.group(2),
            content
        )
    # For twitter:description
    if attr_name == 'tw_desc':
        return re.sub(
            r'(<meta name="twitter:description" content=")[^"]*(")',
            lambda m: m.group(1) + new_value + m.group(2),
            content
        )
    return content

changed = []
for slug, updates in UPDATES.items():
    filepath = os.path.join(BASE, slug, 'index.html')
    if not os.path.exists(filepath):
        print(f'MISSING: {slug}')
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    field_map = {
        'title': 'title',
        'desc': 'desc',
        'og_title': 'og_title',
        'og_desc': 'og_desc',
        'tw_title': 'tw_title',
        'tw_desc': 'tw_desc',
    }
    for key, attr in field_map.items():
        val = updates.get(key)
        if val is not None:
            content = replace_attr(content, attr, val)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changed.append(slug)
        print(f'Updated: {slug}')
    else:
        print(f'No change: {slug}')

print(f'\nTotal changed: {len(changed)}')
