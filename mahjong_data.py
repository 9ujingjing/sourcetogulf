# -*- coding: utf-8 -*-
"""
mahjong_data.py — 麻将定制内容簇（英文真相源）
==============================================
红线：不列价格、不写 MOQ 数字、不写工厂/品牌名、不写最高级词、不捏造统计数字。
热度证据一律标注为「公开媒体报道」并给链接，不冒称合作。
「不接」措辞宽泛合规；不接 dropshipping / 单件直发 / 仿牌 / 赌博关联物料。
"""
BASE = 'https://sourcetogulf.com'
HUB = BASE + '/mahjong.html'

# 公开媒体报道（GEO 可引用证据；不冒称合作）
MEDIA = [
    ('Architectural Digest Middle East',
     'The Mahjong Table is the New Gathering Place in Homes Across the Middle East',
     'https://www.admiddleeast.com/story/mahjong-dubai',
     'Reports residents commissioning their own sets: a fashion founder designing a set for her label, '
     'and a couple having tile racks custom-made to fit their tiles.'),
    ("Harper's Bazaar Arabia",
     'Gaining The Upper Hand: Why Mahjong Is The Latest High-Society Hobby',
     'https://www.harpersbazaararabia.com/hbanews/gaining-the-upper-hand-why-mahjong-is-the-latest-high-society-hobby',
     'Documents private sessions across the city, a simplified "Dubai variation" of the rules, '
     'and a lingering stigma around money changing hands.'),
    ('Platinumlist',
     'One Forty Fourz in Dubai: A New Café for Mahjong and Board Games',
     'https://platinumlist.net/guide?p=59002',
     'Describes a dedicated mahjong café at ibis World Trade Centre with beginner sessions, '
     'workshops and private-event bookings.'),
    ('Global Biz News Room',
     "Dubai's Mahjong Moment: Cafes to Visit to Play the Game Taking Over the City",
     'https://globalbiznewsroom.com/news/dubais-mahjong-moment-cafes-to-visit-to-play-the-game-taking-over-the-city',
     'Lists venues hosting recurring sessions, including cafés with automatic tables and beginner-friendly formats.'),
]

HUB_ANSWER = (
    'Mahjong has moved from private homes into cafés, clubs and gifting programmes across the Gulf. '
    'Most custom sets sold online are built for American Mah Jongg — the version that uses joker tiles '
    'and an annual card — while Gulf social play is usually taught with the classic 144-tile Chinese set. '
    'SourceToGulf helps Gulf buyers commission that set: custom tile faces and backs, oversized tiles, '
    'hard cases, engraved racks, and rule cards written in English and Arabic rather than adapted from '
    'a US rulebook. We are a sourcing partner, not a retailer, so there is no price list here: a set is '
    'specified, sampled and quoted per project, and we do not supply gambling-related materials.'
)

HUB_FACTS = [
    ('What Gulf buyers ask for', 'Custom tile artwork, oversized tiles, hard cases, bilingual rule cards'),
    ('Classic set', '144 tiles: three suits, winds, dragons, plus flower and season tiles'),
    ('Buyers we serve', 'Cafés, clubs, hosts, lifestyle brands, corporate and seasonal gifting'),
    ('Positioning', 'Social strategy game and gift item — no gambling-related materials'),
]

# 用户提供的定制样品参考图。只描述画面可见内容，不声称拍摄地点、工厂或客户归属。
SAMPLE_PHOTOS = {
    'leopard_backs': (
        'images/mahjong/custom-leopard-backs.jpg',
        'Custom mahjong tiles with leopard-print backs and layered gold, black and white edges',
        'A custom sample showing printed backs, face artwork and layered edges. Back artwork, '
        'face graphics and colour layers are separate specification choices.'),
    'leopard_faces': (
        'images/mahjong/custom-leopard-faces.jpg',
        'Custom mahjong tile faces with leopard artwork, wind characters and layered edges',
        'Face artwork and edge layers visible together. A physical sample is used to confirm '
        'artwork alignment, colour density and finish before accessories are sized.'),
    'american_layout': (
        'images/mahjong/american-custom-tile-layout.jpg',
        'American mahjong tile layout with jokers, custom suit artwork and CRAK and BAM labels',
        'An American-style sample with jokers and custom suit graphics. Jokers and the annual-card '
        'format are not interchangeable with a classic Chinese 144-tile specification.'),
    'green_layers': (
        'images/mahjong/custom-layered-green-backs.jpg',
        'Custom mahjong tiles with green backs and multicolour layered edges',
        'Layered edges and a coloured back change the set\'s appearance without changing the '
        'underlying game. Confirm the version and tile count separately from the colour scheme.'),
    'pink_marble': (
        'images/mahjong/custom-pink-marble-set.jpg',
        'Pink marble-effect mahjong set with floral faces and joker tiles',
        'A gift-oriented custom sample with marble-effect backs and floral face artwork. Case, '
        'insert and rule card are specified separately from the tiles.'),
    'chinese_suits': (
        'images/mahjong/chinese-suits-and-honours.jpg',
        'Chinese mahjong tiles showing character, bamboo and circle suits with honour tiles',
        'Character, bamboo and circle suits are visible alongside honour tiles. This shows the '
        'tile families used in a classic Chinese specification; it is not a complete tile-count checklist.'),
    'blush_pearl': (
        'images/mahjong/custom-blush-pearl-set.jpg',
        'Blush pink mahjong tiles with pearlescent backs and custom floral faces',
        'A blush-coloured custom sample with pearlescent backs and coordinated face artwork. '
        'Colour and finish are approved on a physical sample rather than from a screen image.'),
}

HUB_SHOTS = [SAMPLE_PHOTOS[k] for k in ('leopard_backs', 'american_layout', 'chinese_suits')]

HUB_FAQ = [
    ('Why is everyone in Dubai talking about mahjong?',
     'Regional coverage from Architectural Digest Middle East and Harper\'s Bazaar Arabia documents the game '
     'moving into cafés, clubs and private hosting. A dedicated mahjong café has opened in Dubai, and '
     'several venues now run recurring beginner sessions. That visibility is why buyers are asking about sets.'),
    ('What is the difference between a Chinese and an American mahjong set?',
     'The classic Chinese set has 144 tiles: three numbered suits, wind and dragon honours, and flower or '
     'season bonus tiles. American Mah Jongg adds joker tiles and uses an annually printed card of specific '
     'winning hands. They are different games with different equipment, so a set designed for one is not '
     'automatically right for the other.'),
    ('Can you make a set with my logo or my own artwork?',
     'Yes. Tile faces, tile backs, colours, sizes, racks, mats, cases and rule cards can all be customised. '
     'Work starts from your reference or sketch, moves to a physical sample, and only then to a production run.'),
    ('Do you supply rule cards in Arabic?',
     'Yes. Cards are written and typeset in English and Arabic, with Arabic terminology chosen for the '
     'buyer\'s audience rather than transliterated from a US rulebook. A printed proof is approved before printing.'),
    ('Is mahjong gambling?',
     'Social play without stakes is a strategy game. UAE law addresses games where parties agree that the '
     'loser pays the winner money or another benefit. We supply social and gifting sets only and do not '
     'provide gambling-related materials such as betting chips or cash-value scoring systems.'),
    ('Do you sell single sets to individuals?',
     'No. We are a sourcing partner for production runs, not a retailer. Single-parcel direct-to-consumer '
     'shipping from China across the GCC is outside the work we take on.'),
    ('Can a café or club order in bulk?',
     'Yes. Café, club, hotel and event orders are planned around a bill of quantities, with table-ready '
     'sets, spare tiles and teaching materials consolidated into one shipment.'),
    ('What should I send to start?',
     'A reference photo or sketch, the tile style you want, the destination country, and any private-label '
     'or packaging intent. We come back with a sampling route and a written specification.'),
]

# ---------------------------------------------------------------------------
# 子页
# ---------------------------------------------------------------------------
PAGES = [
    {
        'slug': 'custom-mahjong-sets',
        'title': 'Custom Mahjong Sets for Gulf Buyers: Tiles, Cases, Racks & Private Label | SourceToGulf',
        'h1': 'Custom Mahjong Sets: What You Can Actually Change',
        'desc': 'Which parts of a mahjong set can be customised for the Gulf — tile faces, backs, sizes, '
                'racks, mats, hard cases and private-label packaging — and how sampling works before production.',
        'answer': 'Almost every visible part of a mahjong set can be customised: tile face artwork and '
                  'engraving, tile back colour and finish, tile dimensions, rack engraving, mat printing, '
                  'case structure and private-label packaging. For Gulf buyers the two changes that matter '
                  'most are oversized tiles for a majlis table and bilingual English/Arabic rule cards. '
                  'A physical sample is approved before any production run, and each custom element '
                  'carries its own factory minimum.',
        'facts': [
            ('Tile options', 'Melamine, acrylic, resin; matte or polished finishes'),
            ('Custom areas', 'Face artwork, back colour, size, engraving, racks, mats, case'),
            ('Sampling', 'Digital proof → physical sample → sealed reference before production'),
            ('Positioning', 'Social and gifting sets only; no gambling-related materials'),
        ],
        'flow': ['Reference / sketch', 'Artwork & proof', 'Physical sample', 'Seal & spec', 'Production', 'QC & packing', 'Ship to GCC'],
        'sections': [
            ('Tile faces and backs',
             ['Face artwork can be engraved or printed, including a brand mark, a pattern, or a full thematic set. '
              'Arabic calligraphy can be used as a design element, but it should be reviewed by a native reader '
              'before tooling, since a decorative glyph that reads badly is hard to fix after production.',
              'Back colour and finish change how a set reads on camera, which matters for social sellers. '
              'Acrylic suits translucent and colour-layered looks; melamine suits a matte, lower-glare finish for daily use.']),
            ('Tile size and weight',
             ['Oversized tiles read better across a large table and photograph more clearly, which is why they are '
              'often requested for majlis hosting and café use.',
              'Size changes affect more than appearance: rack length, case internal dimensions and insert tooling '
              'all have to be recalculated. Confirm the tile dimensions first, then size everything else to them.']),
            ('Cases, racks and mats',
             ['Cases can be built as folding cartons, rigid gift boxes, drawer boxes or hard presentation cases, '
              'with inserts cut to the final tile dimensions.',
              'Racks and mats can carry a logo or a custom print. If a buyer supplies tiles from elsewhere, '
              'rack length must be matched to those tiles rather than assumed from a standard size.']),
            ('Private-label packaging',
             ['Private-label work includes the box, the insert, the hangtag, the care or instruction leaflet, '
              'and any Arabic text on the outer carton.',
              'Each element has its own minimum. Box, insert, leaflet and tag are separate production items, '
              'so a launch date should only be promised after all of them are confirmed.']),
        ],
        'pitfalls': [
            ('Sizing everything before the tile is fixed', 'Racks, cases and inserts are dimensioned from the tile. '
             'Freeze tile size first, or the accessories will not fit.'),
            ('Approving artwork on screen only', 'Engraving depth, colour density and foil behave differently in '
             'production. Approve a physical sample, not just a PDF.'),
            ('Arabic used as decoration without review', 'Calligraphic elements need a native review for reading '
             'direction, joining forms and meaning before tooling.'),
            ('Treating private label as one minimum', 'Box, insert, leaflet and tag each carry their own factory '
             'minimum. Confirm them separately.'),
            ('Forgetting the rules card', 'A custom set without a matching rule card leaves the recipient unable '
             'to play. Develop the card alongside the tiles, in English and Arabic.'),
        ],
        'faq': [
            ('Can I put my brand logo on the tiles?', 'Yes, on tile faces, backs, racks, mats, cases and cards. '
             'Written trademark authorisation is confirmed before any logo is produced.'),
            ('Can you match a set I saw online?', 'Send the reference photo or link. We come back with what can '
             'be reproduced, what should change for your market, and a sampling route.'),
            ('Do oversized tiles cost more to ship?', 'Larger and heavier tiles change carton volume and weight, '
             'so they affect freight. That is calculated after the tile specification is fixed.'),
            ('Can you make acrylic and melamine versions of the same design?', 'Yes, where the material allows '
             'the same artwork. Finish and translucency differ, so the proof is reviewed for each material.'),
            ('Do you make one custom set as a gift?', 'No. One-off customisation is outside the work we take on; '
             'custom elements each carry a factory minimum.'),
        ],
        'related': ['en-arabic-rule-cards', 'corporate-gifting', 'buying-guide'],
    },
    {
        'slug': 'en-arabic-rule-cards',
        'title': 'Mahjong Rule Cards in English & Arabic for Gulf Tables | SourceToGulf',
        'h1': 'Teaching Mahjong in English and Arabic',
        'desc': 'Why bilingual rule cards matter for Gulf buyers, how 144-tile Chinese mahjong is structured, '
                'and the terminology choices that make an Arabic teaching card usable.',
        'answer': 'Most mahjong teaching material online is written for American Mah Jongg and assumes joker '
                  'tiles and an annual card. Gulf tables usually learn the classic 144-tile Chinese game, so a '
                  'card built for that set is more useful than a translated US rulebook. We produce English and '
                  'Arabic cards that cover the tile families, the turn sequence, the basic melds and how a hand '
                  'is completed, with Arabic terminology reviewed by a native reader before printing.',
        'facts': [
            ('Tile families', 'Three numbered suits, four winds, three dragons, flowers and seasons'),
            ('Card contents', 'Tile map, turn flow, melds, completing a hand, table etiquette'),
            ('Languages', 'English and Arabic, typeset for right-to-left reading'),
            ('Review', 'Arabic terminology checked by a native reader on a printed proof'),
        ],
        'flow': ['Tile map', 'Suits & honours', 'Turn sequence', 'Melds', 'Complete a hand', 'Arabic review', 'Print & pack'],
        'sections': [
            ('Why the card is part of the product',
             ['A set that arrives without a usable teaching card often stays in its box. Gulf hosting mixes '
              'first-time players with experienced ones, and a card that works in both English and Arabic lets '
              'the whole table learn together rather than relying on one person to translate.',
              'For cafés and clubs, the card is also the cheapest way to standardise teaching across sessions, '
              'which is why we treat it as a designed item rather than an afterthought leaflet.']),
            ('What the card must get right',
             ['Tile names need to be consistent between the card and any Arabic used on the tiles or packaging. '
              'Mixing transliterations for the same tile confuses beginners.',
              'Right-to-left layout changes the reading order of diagrams. A turn-sequence arrow that reads '
              'left-to-right in English has to be mirrored for the Arabic version, not simply pasted over.']),
            ('Choosing terminology for an Arab audience',
             ['We keep the tile family names concrete and visual — suits, winds, dragons, flowers and seasons — '
              'and explain each meld with a short example rather than a scoring table.',
              'Scoring is deliberately kept out of beginner cards. The goal is to get four people playing '
              'a social game, not to teach a points system that reads like wagering.']),
        ],
        'pitfalls': [
            ('Translating an American rulebook', 'A US card assumes jokers and an annual hand list, which '
             'does not match the classic 144-tile set most Gulf tables learn.'),
            ('Leaving diagrams unmirrored', 'Turn arrows and wall diagrams must be flipped for right-to-left '
             'reading, not just the text.'),
            ('Inconsistent tile names', 'One Arabic name per tile family, used on the card, the tiles and the box.'),
            ('Teaching scoring to beginners', 'Points systems read like wagering. Keep the first card about '
             'playing, not about money-like scoring.'),
            ('Printing without a native proof', 'Joining forms and line breaks shift in Arabic. Approve a '
             'printed proof with a native reader before the run.'),
        ],
        'faq': [
            ('Do your rule cards cover American Mah Jongg?', 'Our standard cards cover the classic 144-tile '
             'Chinese game. If you need a different variant for a specific club, tell us and we scope it separately.'),
            ('Can the card carry our café or brand logo?', 'Yes, alongside your set. Logo use requires written '
             'trademark authorisation before printing.'),
            ('Is the Arabic reviewed by a person?', 'Yes. Terminology and layout are checked by a native reader '
             'on a printed proof before production.'),
            ('Can we order cards without ordering tiles?', 'Cards are usually developed with a set. Standalone '
             'print runs are possible as a production order with the printer\'s minimum, not as single copies.'),
            ('Do you include gambling instructions?', 'No. Cards are for social, stake-free play and do not '
             'include betting, chip values or cash scoring.'),
        ],
        'related': ['custom-mahjong-sets', 'compliance-gcc', 'corporate-gifting'],
    },
    {
        'slug': 'corporate-gifting',
        'title': 'Mahjong Sets for Corporate Gifting, Cafés & Clubs in the Gulf | SourceToGulf',
        'h1': 'Mahjong for Corporate Gifting, Cafés and Clubs',
        'desc': 'How Gulf cafés, clubs, hotels and companies order custom mahjong sets in production runs: '
                'bills of quantities, bilingual teaching cards, branded packaging and deadline-driven schedules.',
        'answer': 'Mahjong works as a Gulf B2B item because it is social, screen-free and giftable. Cafés and '
                  'clubs need durable table sets plus teaching cards; hotels and event teams need branded '
                  'sets for guests and giveaways; companies need gift boxes for Ramadan, Eid and corporate '
                  'programmes. Orders are planned against a bill of quantities with a fixed date, not sold '
                  'from stock.',
        'facts': [
            ('Cafés & clubs', 'Table sets, spare tiles, teaching cards, durable cases'),
            ('Hotels & events', 'Branded guest sets, event giveaways, display consignment options'),
            ('Corporate gifting', 'Custom gift boxes, inserts and deadline-driven production'),
            ('Positioning', 'Social and gifting sets only; no gambling-related materials'),
        ],
        'flow': ['Bill of quantities', 'Sampling', 'Branding & cards', 'Production', 'QC & consolidate', 'Packing plan', 'Deadline delivery'],
        'sections': [
            ('Cafés and clubs',
             ['A café set is used daily, so durability and replaceable tiles matter more than presentation. '
              'Spare tiles and spare racks belong in the same order as the sets.',
              'Teaching material is the real differentiator: a venue that can seat beginners alongside regulars '
              'fills more tables. Bilingual cards, sized for the table, are part of that.']),
            ('Hotels, events and clubs',
             ['Branded sets work as guest amenities, event giveaways and display pieces. Engraving, case colour '
              'and card design can follow the property\'s palette.',
              'For recurring events, consistency matters more than novelty: the same tile specification and the '
              'same card across every batch, documented in a retained sample.']),
            ('Corporate and seasonal gifting',
             ['Ramadan, Eid, National Day and year-end programmes are date-fixed. Production is counted backwards '
              'from the shelf or event date through printing, packing, production and sample approval.',
              'The box carries much of the perceived value. A rigid box with a fitted insert and a bilingual '
              'card reads as a considered gift rather than a game in a bag.']),
        ],
        'pitfalls': [
            ('Ordering sets without spares', 'High-turnover venues lose tiles. Spare tiles and racks should be '
             'in the original bill of quantities.'),
            ('Branding approved as a screen logo', 'Engraving and foil look different in production. Approve a '
             'physical sample before the run.'),
            ('Leaving the card to the end', 'Teaching cards need their own artwork, Arabic review and print slot. '
             'Schedule them with the tiles.'),
            ('Counting the deadline from shipping', 'Transit and customs come after shipping. Count backwards '
             'from the event date, not from the booking date.'),
            ('Mixing specifications across batches', 'For recurring events, keep one sealed reference set and '
             'one card file so every batch matches.'),
        ],
        'faq': [
            ('Can you supply a café or club in Dubai?', 'Yes, as a production order against a bill of '
             'quantities, including table sets, spares and teaching materials.'),
            ('Do you do display consignment for venues?', 'Display and consignment arrangements are discussed '
             'per venue. Tell us the venue, the tables and the dates and we will scope it.'),
            ('Can sets be branded for a hotel or event?', 'Yes. Tile backs, cases, racks and cards can follow '
             'a brand palette, with authorisation confirmed before production.'),
            ('Can you deliver before Ramadan?', 'Schedules are built backwards from the fixed date. The earlier '
             'the specification is locked, the more room there is for sampling and review.'),
            ('Do you handle small one-off gifts?', 'No. Production runs follow factory minimums; single-piece '
             'custom gifts are outside the work we take on.'),
        ],
        'related': ['custom-mahjong-sets', 'en-arabic-rule-cards', 'compliance-gcc'],
    },
    {
        'slug': 'buying-guide',
        'title': 'Mahjong Set Buying Guide for the Gulf: Tiles, Sizes & What to Specify | SourceToGulf',
        'h1': 'A Gulf Buyer\'s Guide to Choosing a Mahjong Set',
        'desc': 'How to choose a mahjong set for Gulf use: Chinese 144 tiles vs American sets, melamine vs '
                'acrylic, tile size, racks, mats, cases and what to write into a specification.',
        'answer': 'Start with the version being played, not the picture. Classic Chinese mahjong uses 144 '
                  'tiles; American Mah Jongg uses jokers and an annual card, so the equipment differs. Then '
                  'choose material for how the set will be used — melamine for a matte everyday feel, acrylic '
                  'for colour and translucency — and size for the table. Finally decide whether you need a '
                  'standard set or a custom one with your own artwork, case and bilingual rule card.',
        'facts': [
            ('Step 1', 'Confirm the version: classic 144-tile Chinese vs American with jokers'),
            ('Step 2', 'Material: melamine, acrylic or resin, by use and finish'),
            ('Step 3', 'Size and weight: tile dimensions drive racks, cases and freight'),
            ('Step 4', 'Standard or custom: artwork, case, card and private label'),
        ],
        'flow': ['Version', 'Material', 'Tile size', 'Accessories', 'Rule card', 'Specification', 'Sample & order'],
        'sections': [
            ('Version first',
             ['A classic Chinese set has 144 tiles: three numbered suits, four winds, three dragons, and flower '
              'or season bonus tiles. American Mah Jongg adds jokers and relies on a printed card of specific '
              'winning hands that changes each year.',
              'If the people at your table learned the Chinese game, an American set is not a drop-in '
              'replacement. Confirm the version before comparing anything else.']),
            ('Material and finish',
             ['Melamine gives a matte, lower-glare surface and a familiar weight, which suits daily café and '
              'club use. Acrylic allows translucency, layered colour and a brighter look that reads well on camera.',
              'Resin and specialty finishes sit between them and are usually chosen for gift presentation. '
              'Whatever the material, ask for a physical sample before committing to a run.']),
            ('Size, weight and what they affect',
             ['Tile dimensions determine rack length, case internal space and insert tooling. Oversized tiles '
              'are easier to read across a large table and photograph more clearly.',
              'They also increase weight and carton volume, which changes freight. Size should be settled '
              'before accessories and shipping are calculated.']),
            ('Standard set or custom commission',
             ['A standard set suits a buyer who wants the game, not a brand statement. A custom commission '
              'suits a brand, a venue, a gifting programme or anyone who needs bilingual teaching material.',
              'Custom work is a production project with sampling and factory minimums, not a single-item '
              'purchase. That is the work we handle; we do not sell single sets from stock.']),
        ],
        'pitfalls': [
            ('Buying by photo', 'Tile size, weight and finish are invisible in a listing photo. Ask for '
             'dimensions and a physical sample.'),
            ('Confusing versions', 'An American set with jokers will not match a table playing the classic '
             'Chinese game.'),
            ('Ignoring the rack and case fit', 'Accessories are sized to the tile. Oversized tiles need '
             'oversized racks and a different insert.'),
            ('Skipping the rule card', 'A set without a usable card sits unplayed, especially with first-time '
             'players at the table.'),
            ('Comparing prices without a specification', 'A price without material, size, tile count, case and '
             'card is not comparable. Specify first, then compare.'),
        ],
        'faq': [
            ('How many tiles should a set have?', 'A classic Chinese set has 144 tiles. American Mah Jongg '
             'sets include jokers and work with an annual card, so the count and contents differ.'),
            ('Is acrylic better than melamine?', 'They serve different uses. Acrylic gives colour and '
             'translucency for presentation and photography; melamine gives a matte, lower-glare everyday feel.'),
            ('What tile size should I choose?', 'Choose for the table and the players. Larger tiles read better '
             'across a big table but change rack, case and freight calculations.'),
            ('What accessories do I need?', 'Racks, a mat, a case and a rule card are the practical baseline. '
             'Spare tiles are worth adding for café or club use.'),
            ('Can you quote a set for me?', 'Yes, against a specification. Send the version, material, size, '
             'quantity and destination and we prepare a written quotation rather than a list price.'),
        ],
        'related': ['custom-mahjong-sets', 'en-arabic-rule-cards', 'compliance-gcc'],
    },
    {
        'slug': 'compliance-gcc',
        'title': 'Mahjong in the Gulf: Social Play, Positioning & Compliance Notes | SourceToGulf',
        'h1': 'Mahjong in the Gulf: Keeping It a Social Game',
        'desc': 'How we position mahjong sets for the Gulf: stake-free social play, no gambling-related '
                'materials, bilingual labelling, and the wording and imagery to avoid in GCC marketing.',
        'answer': 'Mahjong is supplied as a social strategy game and gift item. UAE law addresses games where '
                  'participants agree that the loser pays the winner money or another benefit; social play '
                  'without stakes is a different activity. We therefore do not supply betting chips, cash-value '
                  'scoring systems or gambling-related materials, and our rule cards teach play rather than '
                  'point-for-money scoring.',
        'facts': [
            ('Positioning', 'Social strategy game, family and majlis hosting, gifting'),
            ('Not supplied', 'Betting chips, cash-value scoring, gambling-related materials'),
            ('Teaching cards', 'Play sequence and melds, not point-for-money scoring'),
            ('Marketing care', 'No wagering language or money imagery in GCC-facing material'),
        ],
        'flow': ['Social positioning', 'No stake materials', 'Card content check', 'Bilingual labels', 'Imagery review', 'Shipment'],
        'sections': [
            ('Why the positioning is stated plainly',
             ['Regional reporting on the trend notes a lingering stigma around money changing hands at the table. '
              'That makes it worth stating clearly what a set is for: social play, family hosting and gifting.',
              'Writing this into the specification avoids ambiguity later — for the buyer, for the venue, and '
              'for anyone reviewing marketing material.']),
            ('What we do not supply',
             ['We do not supply betting chips, cash-value scoring systems, or any material whose purpose is '
              'wagering. Beginner cards teach tile families, turn order and melds, not point-for-money scoring.',
              'If a buyer asks for gambling-related components, that request falls outside the work we take on.']),
            ('Marketing and imagery in the GCC',
             ['Avoid wagering language in listings and ads: words that imply betting, jackpots or winning money '
              'change how a product reads to a reviewer.',
              'Avoid imagery that centres cash, betting chips or money-like counters. Present the set as a '
              'social and design object: tiles, case, card, and people around a table.']),
            ('Labelling and languages',
             ['Product and packaging information should be clear about what the item is, with English and Arabic '
              'text where the destination requires it.',
              'Arabic is reviewed on a printed proof, because a labelling error discovered after printing is '
              'far more expensive than a review before it.']),
        ],
        'pitfalls': [
            ('Assuming any game is automatically gambling', 'The issue is stakes and payouts, not the tiles '
             'themselves. Keep the product and its materials stake-free.'),
            ('Including chips out of habit', 'Chip sets copied from casino-style kits read as wagering '
             'equipment. Leave them out of social and gifting sets.'),
            ('Teaching money-based scoring', 'Beginner material should teach play, not point-for-money scoring.'),
            ('Using wagering words in marketing', 'Betting, jackpot and win-money phrasing is both a positioning '
             'and a review problem in the GCC.'),
            ('Treating Arabic labels as an afterthought', 'Arabic text is approved on a printed proof before '
             'production, not added afterwards.'),
        ],
        'faq': [
            ('Is mahjong gambling?', 'Social play without stakes is a strategy game. Gambling concerns agreed '
             'stakes and payouts, which is why we do not supply wagering materials.'),
            ('Do your sets include betting chips?', 'No. Sets are supplied for social play and gifting, without '
             'betting chips or cash-value scoring systems.'),
            ('Do your rule cards teach scoring?', 'They teach tile families, turn order and melds so a table '
             'can play. They do not teach point-for-money scoring.'),
            ('Can I market these as a casino product?', 'That is outside our scope. We position sets as social '
             'and gifting items and do not support gambling-related positioning.'),
            ('Do you provide Arabic labelling?', 'Yes, English and Arabic product and packaging text is prepared '
             'and approved on a printed proof before production.'),
        ],
        'related': ['en-arabic-rule-cards', 'corporate-gifting', 'buying-guide'],
    },
]

PAGE_SHOTS = {
    'custom-mahjong-sets': [SAMPLE_PHOTOS[k] for k in
                            ('leopard_backs', 'leopard_faces', 'green_layers', 'pink_marble')],
    'en-arabic-rule-cards': [SAMPLE_PHOTOS[k] for k in ('chinese_suits', 'american_layout')],
    'corporate-gifting': [SAMPLE_PHOTOS[k] for k in ('blush_pearl', 'pink_marble', 'leopard_backs')],
    'buying-guide': [SAMPLE_PHOTOS[k] for k in ('american_layout', 'chinese_suits', 'green_layers')],
    'compliance-gcc': [SAMPLE_PHOTOS[k] for k in ('chinese_suits', 'green_layers')],
}

PHOTO_SECTIONS = {
    'custom-mahjong-sets': ('Custom tile samples', 'Face artwork, back prints and colour layers'),
    'en-arabic-rule-cards': ('What the teaching card must explain', 'Chinese-style suits and honours versus American-style jokers'),
    'corporate-gifting': ('Gift presentation references', 'Coordinated artwork, pearlescent finishes and custom backs'),
    'buying-guide': ('Compare the version before the finish', 'American-style jokers, Chinese-style suits and decorative layers are different decisions'),
    'compliance-gcc': ('Product imagery without wagering cues', 'Tiles, colour and artwork — no cash, betting chips or money-value counters'),
}
