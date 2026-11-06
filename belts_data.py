# -*- coding: utf-8 -*-
"""
belts_data.py — 中国产业带 × 海湾客户类型 内容真相源
=====================================================
唯一数据源。改文案改这里，再跑 `python3 build_belts.py`。
红线（改内容前先读）：
  - 不写客户名 / 供应商名 / 工厂名 / 1688 / SHEIN / 具体产品价格 / MOQ 数字 / FOB 公式
  - 不写最高级词（best / leading / largest / #1 / densest / most）
  - 产业带只写城市或区镇 + 公开集群事实，不编造「占全国 X%」
  - 图片 caption 只描述照片里真实可见的内容，不给照片安上它不属于的地点
  - 「不接」措辞宽泛、合规、保护向；不接 dropshipping / 单件直发 / 仿牌 / 危险品 / 无认证路径
"""
from html import escape as _e

HUB_URL = 'https://sourcetogulf.com/sourcing-belts.html'
BASE = 'https://sourcetogulf.com'

# ---------------------------------------------------------------------------
# 一、海湾买家类型（6 类，符合 GCC 市场实际，明确不含 dropshipping）
# ---------------------------------------------------------------------------
BUYER_TYPES = [
    {
        'slug': 'social-sellers',
        'name': 'Social commerce sellers',
        'local': 'Instagram · TikTok · Snapchat · WhatsApp · Salla / Zid',
        'brief': 'Home-based and creator-led sellers who take orders in DMs and sell through Gulf social platforms.',
        'brings': 'Screenshots, a reference link, or a photo of a style that is already selling in their market.',
        'gets': 'Small first runs, on-camera sample photos, and a private label that can grow into a reorder.',
        'belts': ['guangzhou-womenswear', 'shantou-chaoyang-sleepwear', 'shenzhen-jewellery'],
        'icon': 'phone',
    },
    {
        'slug': 'modest-boutiques',
        'name': 'Modest-fashion & abaya boutiques',
        'local': 'Riyadh · Jeddah · Dubai · Doha · Kuwait City',
        'brief': 'Boutique owners buying abayas, kaftans, jalabiyas, hijabs and layered sets for a local shop.',
        'brings': 'A curated style list, fabric preferences and a requirement for consistent sizing across a season.',
        'gets': 'Mixed-style runs, fabric cards, embroidery samples and coordinated gift packaging.',
        'belts': ['guangzhou-womenswear', 'fujian-sportswear', 'dongguan-packaging'],
        'icon': 'hanger',
    },
    {
        'slug': 'souq-traders',
        'name': 'Souq traders, wholesalers & re-exporters',
        'local': 'Deira · Dragon Mart · wholesale districts · re-export to wider region',
        'brief': 'Traders who buy by the carton, restock on a cycle, and often move goods on to other markets.',
        'brings': 'A category list, a destination port and a restock calendar rather than a single-item request.',
        'gets': 'Mixed cartons, consolidation across several clusters, and repeat-order continuity on specifications.',
        'belts': ['shenzhen-electronics', 'zhongshan-lighting', 'shantou-chaoyang-sleepwear', 'foshan-furniture'],
        'icon': 'boxes',
    },
    {
        'slug': 'brand-founders',
        'name': 'Brand founders & private-label owners',
        'local': 'Fragrance · bakhoor · home scent · beauty · lifestyle',
        'brief': 'Gulf founders building a named label who need the product, the box and the paperwork to match.',
        'brings': 'A logo, a product concept and a target launch date — often tied to a seasonal window.',
        'gets': 'Sampling, structure design for packaging, EN/AR labelling and a documented specification.',
        'belts': ['dongguan-packaging', 'shenzhen-jewellery', 'guangzhou-womenswear'],
        'icon': 'tag',
    },
    {
        'slug': 'project-buyers',
        'name': 'Hospitality, retail & project buyers',
        'local': 'Hotels · restaurants · clinics · fit-out · commercial spaces',
        'brief': 'Project teams buying against a bill of quantities rather than a single product.',
        'brings': 'A multi-model equipment or furnishing list, with handover dates and site requirements.',
        'gets': 'Multi-cluster consolidation, conformity documentation, and delivery planned around the project.',
        'belts': ['foshan-furniture', 'zhongshan-lighting', 'shenzhen-electronics', 'dongguan-packaging'],
        'icon': 'plan',
    },
    {
        'slug': 'gifting-buyers',
        'name': 'Corporate & seasonal gifting buyers',
        'local': 'Ramadan · Eid · National Day · White Friday · corporate programmes',
        'brief': 'Buyers working backwards from a fixed date, where the box is as important as what is inside.',
        'brings': 'A budget band, a quantity, a date and a branding guideline.',
        'gets': 'Custom gift boxes, coordinated inserts, and a production schedule counted back from the deadline.',
        'belts': ['dongguan-packaging', 'zhongshan-lighting', 'shenzhen-jewellery'],
        'icon': 'gift',
    },
]

# ---------------------------------------------------------------------------
# 二、明确排除项（筛客用，措辞宽泛合规）
# ---------------------------------------------------------------------------
EXCLUSIONS = [
    ('Single-piece dropshipping',
     'Single-parcel, direct-to-consumer dropshipping from China to end customers across the GCC, '
     'where goods are not already warehoused inside the GCC. We are a sourcing partner, not a parcel network.'),
    ('One-piece customisation',
     'Private-label runs follow the factory MOQ for each element — woven label, care label, hangtag and box '
     'each carry their own minimum. A single printed piece is not a production run.'),
    ('Counterfeit & restricted goods',
     'Counterfeit, replica or IP-infringing branded goods; illegal, prohibited or restricted goods; '
     'and hazardous cargo such as aerosols (UN1950) and other transport-restricted items.'),
    ('No viable compliance path',
     'Categories requiring mandatory certification (for example ECAS or SABER for electrical appliances) '
     'where the paperwork cannot be closed before shipment.'),
    ('Price-only enquiries',
     'We work from a specification — photo, material, quantity and destination — rather than a request '
     'for the lowest price on an unnamed item. There is no public price list to compare against.'),
]

# ---------------------------------------------------------------------------
# 三、8 个产业带
#   photos 里的 caption 只描述照片里真实可见的东西；绝不写「摄于 XX 工厂」
#   flow 是产业链步骤，用于自绘 SVG 信息图（文字可被 AI 抓取）
# ---------------------------------------------------------------------------
BELTS = [
    {
        'slug': 'shantou-chaoyang-sleepwear',
        'city': 'Shantou · Chaoyang',
        'region': 'Guangdong, South China',
        'category': 'Sleepwear & loungewear',
        'h1': 'Sleepwear and Loungewear from Shantou Chaoyang: A Gulf Buyer\'s Guide',
        'title': 'Sleepwear & Loungewear Sourcing from Shantou Chaoyang, China | SourceToGulf',
        'desc': 'What Gulf buyers source from the Chaoyang knitwear cluster in Shantou: fabrics, seasonal windows, '
                'EN/AR labelling, SABER and ECAS watchpoints, and the five mistakes that cost a season.',
        'answer': 'Chaoyang district in Shantou, Guangdong is one of China\'s knitwear and intimate-apparel clusters. '
                  'Gulf buyers source sleepwear, lounge sets and modest homewear here in production runs with private '
                  'labels — combed cotton, modal, ice silk and fleece — with English/Arabic care labelling and the '
                  'textile documentation prepared before shipment. The reason to buy by cluster rather than by '
                  'catalogue is that knitting, dyeing, cut-and-sew, labelling and packing sit within one region, '
                  'so a style change or a repeat order does not have to cross several provinces.',
        'facts': [
            ('Cluster', 'Knitwear, underwear, sleepwear and homewear'),
            ('Typical buyers', 'Boutiques, social sellers, department buyers, gifting programmes'),
            ('Gulf season', 'Light fabrics year-round; fleece in the November–February window'),
            ('Compliance watch', 'Textile labelling, Arabic care instructions, SABER for Saudi, ECAS for children\'s sleepwear in the UAE'),
        ],
        'intro': [
            'Chaoyang is a knitwear district inside Shantou, on the eastern Guangdong coast. Yarn, knitting, '
            'dyeing and finishing, cutting, sewing and packing are concentrated in the same area. For a Gulf buyer '
            'that matters less as a geography fact and more as a scheduling fact: a fabric decision, a sample and '
            'a repeat order can be handled without moving work between distant suppliers.',
            'Sleepwear is also a forgiving first category for a new buyer. Sizing tolerance is wider than in '
            'tailored womenswear, reorders are frequent, and the product is easy to gift-box for Ramadan or Eid. '
            'That is why it appears early in most Gulf sourcing plans.',
        ],
        'buys': [
            ('Year-round: UAE, Qatar, Oman, Bahrain', 'Ice silk, modal and light combed cotton; short sets, robes, slip dresses and modest lounge sets.'),
            ('Longer summer: Saudi inland', 'Breathable knits and lighter constructions; darker colourways for the modest-wear segment.'),
            ('November–February', 'Fleece, polar fleece and quilted knits for the short winter window and for northern Gulf retail.'),
            ('Gifting windows', 'Coordinated two- and three-piece sets packed as gift boxes, produced together with the packaging cluster.'),
        ],
        'compliance': [
            'Saudi Arabia: textile labelling and conformity requirements apply under SABER. Fibre composition, '
            'care instructions and country of origin belong on the label, in Arabic.',
            'UAE: children\'s sleepwear falls under safety and flammability-related requirements via ECAS; '
            'adult sleepwear is handled as a textile category. Confirm the route before sampling.',
            'A practical default is an EN/AR care label plus a composition label, approved as a physical sample '
            'before the bulk run — not added after production.',
            'Keep a signed-off specification sheet with fabric weight, colour card reference and shrinkage '
            'tolerance; it is what a dispute is measured against.',
        ],
        'pitfalls': [
            ('Fabric weight written but not held', 'A specification that says one gram weight and a bulk roll that '
             'is lighter. Ask for a retained sample and keep the swatch card with the order file.'),
            ('Shade variation between dye lots', 'Two cartons of the same colour from different lots look different '
             'under shop lighting. Keep one dye lot per shipment, or archive a colour card for each batch.'),
            ('Shrinkage after the first wash', 'Cotton knits that were not pre-shrunk move out of size. Put '
             'pre-shrinking and a shrinkage tolerance into the specification.'),
            ('Private-label minimums counted as one', 'Woven labels, care labels, hangtags and gift boxes each '
             'carry their own factory minimum. Confirm all four separately before promising a launch date.'),
            ('Lead time counted backwards too late', 'Ramadan and Eid retail dates are fixed. Work backwards from '
             'the shelf date through transit, packing, production and sampling, then add approval time.'),
        ],
        'perfect_for': ['social-sellers', 'modest-boutiques', 'souq-traders'],
        'photos': [
            ('images/apparel/fabric-wall-1.jpg',
             'Wall of fabric colour cards in an apparel sample room',
             'A wall of fabric colour cards in a sample room — the hand feel and shade are chosen from physical '
             'swatches before a sleepwear run is specified.'),
            ('images/apparel/label-carelabel.jpg',
             'Care and composition label sample for a garment',
             'A printed care and composition label. For the Gulf, fibre content and care text are signed off as a '
             'physical sample in English and Arabic before the bulk run.'),
        ],
        'flow': ['Yarn & knitting', 'Dyeing & finishing', 'Cut & sew', 'Labels & QC', 'Packing', 'Compliance file', 'Ship to GCC'],
        'faq': [
            ('What is Chaoyang in Shantou known for?',
             'Knitwear, underwear, sleepwear and homewear production, with knitting, dyeing, cut-and-sew and '
             'packing concentrated in the same district of Shantou, Guangdong.'),
            ('Can I order a small first run?',
             'Yes, provided it meets the factory minimum for that style. We start with samples and a written '
             'specification, then confirm the minimum for each style and each private-label element before production.'),
            ('Do you prepare Arabic care labels?',
             'Yes. English/Arabic care and composition labels are approved as a physical sample before the bulk '
             'run, rather than added after production.'),
            ('Is SABER required for sleepwear going to Saudi Arabia?',
             'Textile labelling and conformity requirements apply to Saudi imports. We prepare the documentation '
             'set before shipment and confirm the applicable route for the specific product.'),
            ('Which fabrics suit Gulf summers?',
             'Ice silk, modal and light combed cotton for the long summer; fleece and quilted knits for the '
             'short November–February window.'),
            ('Can sleepwear be made as Ramadan gift boxes?',
             'Yes. Coordinated sets are packed with boxes produced through the packaging cluster, with the '
             'schedule counted backwards from the retail date.'),
            ('Do you dropship single pieces to end customers?',
             'No. We do not handle single-parcel direct-to-consumer dropshipping from China across the GCC '
             'where goods are not already warehoused inside the GCC.'),
        ],
        'related': ['guangzhou-womenswear', 'dongguan-packaging', 'fujian-sportswear'],
    },
    {
        'slug': 'guangzhou-womenswear',
        'city': 'Guangzhou',
        'region': 'Guangdong, South China',
        'category': 'Womenswear & modest fashion',
        'h1': 'Womenswear and Modest Fashion from Guangzhou: A Gulf Buyer\'s Guide',
        'title': 'Guangzhou Womenswear & Modest Fashion Sourcing for Gulf Buyers | SourceToGulf',
        'desc': 'How Gulf boutiques and social sellers use Guangzhou for small-batch womenswear, abayas, kaftans '
                'and fast reorders: fabric choice, embroidery, sizing, EN/AR labels and the GCC compliance route.',
        'answer': 'Guangzhou is a womenswear wholesale and production hub in Guangdong, with fabric markets, '
                  'sampling rooms, embroidery, cut-and-sew and export packing in one city. Gulf buyers use it for '
                  'small-batch dresses and sets, and for modest-wear pieces such as abayas, kaftans and jalabiyas. '
                  'Its value to a Gulf buyer is short sampling cycles and the ability to reorder a proven style '
                  'without waiting behind a full container of someone else\'s stock.',
        'facts': [
            ('Cluster', 'Womenswear wholesale, sampling, embroidery, modest-wear tailoring'),
            ('Typical buyers', 'Boutiques, social sellers, brand founders, seasonal buyers'),
            ('Gulf season', 'Ramadan / Eid collections, White Friday, year-round restock'),
            ('Compliance watch', 'Textile labelling, Arabic care text, SABER for Saudi, fabric composition declarations'),
        ],
        'intro': [
            'Guangzhou combines wholesale markets with a dense sampling and production network. A buyer can '
            'choose a fabric from a physical card, see a sample on a rail, adjust embroidery, and approve a '
            'care label in the same working week. For Gulf sellers whose demand is driven by social platforms, '
            'that speed matters more than a large minimum quantity.',
            'The city also has a long-established export trade in modest wear for the Gulf. Abayas, kaftans '
            'and jalabiyas are made here alongside mainstream womenswear, with embroidery, beading and foil '
            'work available as separate processes that can be sampled independently.',
        ],
        'buys': [
            ('Ramadan & Eid', 'Abayas, kaftans, jalabiyas and coordinated sets; embroidery and festive trims.'),
            ('Social-commerce restock', 'Dresses, co-ord sets and layered pieces in small runs, reordered once a style proves itself.'),
            ('Boutique seasons', 'Curated mixed-style runs with consistent sizing and a shared fabric story.'),
            ('Brand launches', 'Private-label wovens, care labels, hangtags and boxes developed together with the packaging cluster.'),
        ],
        'compliance': [
            'Saudi Arabia: textile imports are handled under SABER with fibre composition, care instructions '
            'and country of origin on the label, in Arabic.',
            'UAE and other GCC markets: keep a written declaration of fabric composition and a retained '
            'approved sample for each style.',
            'Embroidery, foil and beading change the hand feel and the care instruction. A care label copied '
            'from a plain version of the same dress is often wrong.',
            'For children\'s clothing, confirm the applicable safety route before sampling; requirements '
            'differ from adult womenswear.',
        ],
        'pitfalls': [
            ('Sizing copied from another market', 'A size chart from a different region will not fit the same '
             'customer. Approve a graded size set on a physical sample, including length for modest cuts.'),
            ('Embroidery approved from a photo', 'Thread colour, density and backing change with the fabric. '
             'Approve a stitched sample under the light the garment will be sold in.'),
            ('Colour matched on a screen', 'A screen proof is not a dye lot. Keep a physical colour card and '
             'make one lot per shipment where possible.'),
            ('Reorder without a retained spec', 'Without a signed specification and a retained sample, a reorder '
             'becomes a new product. Archive fabric, trim and label references from the first run.'),
            ('Sampling time left out of the calendar', 'Fabric selection, sample, revision, approval and bulk '
             'production are separate steps. Count them all backwards from a fixed Eid or campaign date.'),
        ],
        'perfect_for': ['social-sellers', 'modest-boutiques', 'brand-founders'],
        'photos': [
            ('images/apparel/apparel-rack-showroom.jpg',
             'Rail of developed garment samples in a showroom',
             'A rail of developed garment samples in a showroom — styles that already exist can be adapted '
             'instead of built from a blank page.'),
            ('images/apparel/apparel-embroidery.jpg',
             'Close-up of embroidery work on a garment',
             'Embroidery work on a garment. Thread colour, density and backing are approved on a stitched '
             'sample, not from a photograph.'),
            ('images/products/abaya-embroidered.jpg',
             'Embroidered black abaya shown on a stand',
             'An embroidered abaya of the kind Gulf boutiques develop for Ramadan and Eid collections.'),
        ],
        'flow': ['Fabric cards', 'Pattern & sample', 'Embroidery / trim', 'Fit approval', 'Labels & QC', 'Packing', 'Ship to GCC'],
        'faq': [
            ('Why do Gulf buyers source womenswear from Guangzhou?',
             'Fabric markets, sampling rooms, embroidery, cut-and-sew and export packing are concentrated in '
             'one city, which shortens sampling and makes small reorders practical.'),
            ('Can abayas and kaftans be made here?',
             'Yes. Guangzhou has an established export trade in modest wear for the Gulf, including abayas, '
             'kaftans, jalabiyas and embroidered pieces.'),
            ('How small can a first run be?',
             'It depends on the style and the fabric. We confirm the factory minimum per style after a sample '
             'and a written specification, and we do not handle one-piece customisation.'),
            ('Can you match a style from a photo?',
             'Yes. Send the photo, the intended fabric and the quantity; we come back with a physical sample '
             'and a specification rather than a price guess.'),
            ('Do you handle Arabic labels and SABER documents?',
             'Yes. English/Arabic care and composition labels are approved as samples, and the Saudi '
             'conformity documentation is prepared before shipment.'),
            ('How do reorders stay consistent?',
             'A retained approved sample, a signed specification and archived fabric and trim references '
             'are kept from the first run and used for the reorder.'),
            ('Do you ship single pieces to end customers?',
             'No. Single-parcel direct-to-consumer dropshipping from China across the GCC is outside the '
             'work we take on where goods are not already warehoused inside the GCC.'),
        ],
        'related': ['shantou-chaoyang-sleepwear', 'fujian-sportswear', 'dongguan-packaging'],
    },
    {
        'slug': 'fujian-sportswear',
        'city': 'Shishi & Jinjiang',
        'region': 'Fujian, Southeast China',
        'category': 'Sportswear & casualwear',
        'h1': 'Sportswear and Casualwear from Fujian: A Gulf Buyer\'s Guide',
        'title': 'Fujian Sportswear & Casualwear Sourcing (Shishi, Jinjiang) for Gulf Buyers | SourceToGulf',
        'desc': 'What Gulf buyers source from the Shishi and Jinjiang clothing clusters in Fujian: activewear, '
                'light layering, team and club orders, fabric performance claims and GCC labelling.',
        'answer': 'Shishi and Jinjiang in Fujian are clothing and sportswear clusters covering casualwear, '
                  'knitted sportswear and footwear supply chains. Gulf buyers use them for activewear, '
                  'lightweight layering pieces, club and team orders, and coordinated sets. Fabric for abaya '
                  'and kaftan production is usually specified separately through textile clusters, then made '
                  'up in the garment clusters — a distinction worth making before a supplier promises both.',
        'facts': [
            ('Cluster', 'Casualwear, knitted sportswear, teamwear; adjacent footwear supply chain'),
            ('Typical buyers', 'Wholesalers, club and team buyers, social sellers, project buyers'),
            ('Gulf season', 'Year-round activewear; peak around fitness campaigns and school terms'),
            ('Compliance watch', 'Fibre composition declarations, Arabic care text, performance claims in writing'),
        ],
        'intro': [
            'Fujian\'s Shishi and Jinjiang clusters grew around casual garments, knitted sportswear and '
            'the footwear supply chain. The practical advantage is a deep bench of knit constructions, '
            'performance fabrics and trim suppliers that a single factory elsewhere may not hold.',
            'For Gulf buyers the useful framing is climate and use: light, breathable constructions for '
            'most of the year, and layered pieces for air-conditioned retail and the short winter. Team and '
            'club orders also come from this cluster, where a consistent size grade across a whole order '
            'matters more than a single sample looking right.',
        ],
        'buys': [
            ('Everyday activewear', 'Knitted sets, training tops, leggings and shorts in breathable constructions.'),
            ('Modest layering', 'Longline tops, light outer layers and coordinated sets that work over other pieces.'),
            ('Club, team & corporate orders', 'Graded size runs with repeated logo application and consistent colour across the batch.'),
            ('Footwear-adjacent programmes', 'Where a buyer is building a full sports range, garment and footwear '
             'supply chains can be coordinated through the same region.'),
        ],
        'compliance': [
            'Record fibre composition as a written declaration; "quick-dry", "UV" or similar performance '
            'claims need a basis in the fabric specification, not a marketing line.',
            'Arabic care and composition labels should be approved for the specific construction — a '
            'performance knit can have different care instructions from a cotton one.',
            'For Saudi shipments, align the textile documentation with SABER requirements before production '
            'rather than at the booking stage.',
            'For team or corporate orders with logos, confirm trademark authorisation in writing before '
            'any logo is applied.',
        ],
        'pitfalls': [
            ('Performance claims with no fabric basis', 'A "quick-dry" label with no corresponding fabric '
             'specification. Ask what the construction is and put it in the sheet.'),
            ('One size grade applied to every style', 'A legging and an outer layer cannot share one grade. '
             'Approve a graded size set per style.'),
            ('Logo application checked only on one piece', 'Print placement and colour can drift across a batch. '
             'Approve a placement sheet and check the first pieces off the line.'),
            ('Fabric substituted after the sample', 'A lighter knit can appear in the bulk run. Keep a retained '
             'swatch from the approved sample and reference it in the order file.'),
            ('Assuming one cluster covers fabric and garment', 'Textile fabrics and made-up garments often come '
             'from different clusters. Map both before accepting a single promise for the whole range.'),
        ],
        'perfect_for': ['souq-traders', 'project-buyers', 'social-sellers'],
        'photos': [
            ('images/apparel/apparel-cutting.jpg',
             'Cutting tables in a garment workshop',
             'A cutting floor in a garment workshop. Cut-and-sew, pressing and packing sit close together in '
             'these clusters, which is what makes a repeat order traceable.'),
            ('images/apparel/apparel-pressing.jpg',
             'Pressing and finishing a garment by hand',
             'Pressing and finishing by hand. Construction and finishing are checked on a physical sample '
             'before a graded size run is approved.'),
        ],
        'flow': ['Fabric spec', 'Knit / cut', 'Logo & trim', 'Graded fit', 'Labels & QC', 'Packing', 'Ship to GCC'],
        'faq': [
            ('What are Shishi and Jinjiang known for?',
             'Casualwear, knitted sportswear and teamwear, with an adjacent footwear supply chain in Fujian.'),
            ('Is abaya fabric made in Fujian?',
             'Made-up garments and sportswear come from these clothing clusters; base textiles such as abaya '
             'fabrics are usually specified through separate textile clusters. We map both before quoting a range.'),
            ('Can you do team or club orders with logos?',
             'Yes, for production runs. We confirm trademark authorisation in writing and approve a logo '
             'placement sheet before application.'),
            ('How do you verify a performance fabric claim?',
             'The construction and composition go into a written specification with a retained swatch from '
             'the approved sample; claims without a fabric basis are not carried onto the label.'),
            ('Do you prepare Arabic care labels for sportswear?',
             'Yes, for the specific construction in the order. A performance knit and a cotton knit can '
             'require different care text.'),
            ('Can this cluster be combined with others in one shipment?',
             'Yes. Consolidation across clusters is a normal part of a Gulf order, with one specification '
             'file and one pre-shipment check.'),
            ('Do you take single-piece orders?',
             'No. One-piece customisation is outside the work we take on; private-label elements each '
             'carry their own factory minimum.'),
        ],
        'related': ['guangzhou-womenswear', 'shantou-chaoyang-sleepwear', 'shenzhen-electronics'],
    },
    {
        'slug': 'shenzhen-jewellery',
        'city': 'Shenzhen · Shuibei',
        'region': 'Guangdong, South China',
        'category': 'Fashion jewellery & silver',
        'h1': 'Fashion Jewellery from Shenzhen Shuibei: A Gulf Buyer\'s Guide',
        'title': 'Shenzhen Shuibei Fashion Jewellery Sourcing for Gulf Buyers | SourceToGulf',
        'desc': 'How Gulf jewellery buyers use Shenzhen\'s Shuibei cluster: 316L steel, PVD plating, silver, '
                'sampling from a sketch, hallmark and composition questions, and gift packaging.',
        'answer': 'Shuibei in Shenzhen is a jewellery design, manufacturing and wholesale district covering '
                  'gold, silver, fashion jewellery and setting work. Gulf buyers source custom pieces here '
                  'from a sketch or a reference photo — commonly 316L stainless steel with PVD gold plating, '
                  'sterling silver, and moissanite or stone setting. A physical sample is approved before a '
                  'production run, and plating thickness, base metal and packaging are written into the spec.',
        'facts': [
            ('Cluster', 'Gold, silver, fashion jewellery, setting and plating'),
            ('Typical buyers', 'Boutiques, brand founders, gifting programmes, social sellers'),
            ('Gulf season', 'Eid, wedding season, White Friday, year-round gifting'),
            ('Compliance watch', 'Metal composition declarations, hallmark questions, nickel release, plating spec'),
        ],
        'intro': [
            'Shuibei is a dense jewellery district in Shenzhen: design, casting, setting, plating and '
            'wholesale counters sit within a small area. For a Gulf buyer with a sketch, that means a '
            'physical sample can be developed and revised without commissioning a full production run first.',
            'Jewellery is also where a gift programme succeeds or fails. The pouch, the box and the tag are '
            'part of the product in Gulf retail, and they are produced through the packaging cluster rather '
            'than at the jewellery counter. Planning both together avoids a box that arrives after the pieces.',
        ],
        'buys': [
            ('Custom from a sketch', 'Rings, bangles, necklaces and earrings developed as a physical sample before a run.'),
            ('Everyday fashion jewellery', '316L stainless steel with PVD gold plating, chosen for tarnish resistance in a humid climate.'),
            ('Occasion & gifting', 'Coordinated sets with matching boxes for Eid, weddings and corporate programmes.'),
            ('Private-label lines', 'Logo on the pouch, box and jewellery tag, with the same finish across a collection.'),
        ],
        'compliance': [
            'Put base metal, plating method and plating thickness into the written specification; "gold colour" '
            'is not a composition.',
            'For any piece described as silver or gold, clarify what is being claimed and what documentation '
            'supports it before the label is printed.',
            'Nickel release and skin-contact questions should be raised at sampling for the target market, '
            'not after the batch is plated.',
            'Keep a sealed approved sample. Plating tone is the most common difference between a first '
            'sample and a bulk run.',
        ],
        'pitfalls': [
            ('Plating tone drifting between lots', 'A sample approved under warm showroom light can look '
             'different in bulk. Keep a sealed sample and check the first pieces off the line.'),
            ('Composition described loosely', '"Gold" that means colour rather than content. Write the base '
             'metal and plating method into the specification.'),
            ('Stone setting checked only in a photo', 'Prong height and stone alignment need a physical sample '
             'under magnification, especially for repeated pieces in a set.'),
            ('Packaging ordered after the jewellery', 'Box inserts are cut to the piece. Develop box and '
             'jewellery together so the insert fits the final dimensions.'),
            ('No trademark authorisation for a logo', 'Brand marks on tags and boxes require written '
             'authorisation before production.'),
        ],
        'perfect_for': ['brand-founders', 'modest-boutiques', 'gifting-buyers'],
        'photos': [
            ('images/gold-rings-bowl.jpg',
             'Gold-toned rings arranged in a display bowl',
             'Gold-toned rings in a display bowl. Base metal and plating method are written into the '
             'specification rather than described as a colour alone.'),
            ('images/jewelry-showroom-table.jpg',
             'Jewellery display stand in a showroom',
             'A jewellery display stand in a showroom, where an existing design can be adapted into a '
             'private-label piece.'),
            ('images/earrings-display.jpg',
             'Assorted earrings laid out on a display board',
             'Assorted earrings on a display board. Coordinated sets are planned together with their '
             'gift box inserts.'),
        ],
        'flow': ['Sketch / reference', 'CAD & casting', 'Setting', 'Plating', 'Sealed sample', 'Box & tag', 'Ship to GCC'],
        'faq': [
            ('What is Shuibei in Shenzhen known for?',
             'Jewellery design, manufacturing and wholesale, including gold, silver, fashion jewellery, '
             'setting and plating, concentrated in one district.'),
            ('Can you make a piece from a sketch or a photo?',
             'Yes. The usual path is a physical sample for approval, then a production run against a '
             'sealed sample and a written specification.'),
            ('What materials do Gulf buyers commonly choose?',
             '316L stainless steel with PVD gold plating for everyday pieces, plus sterling silver and '
             'stone-set designs for occasion ranges.'),
            ('How do you keep plating consistent across a reorder?',
             'A sealed approved sample, a specification that records base metal, plating method and '
             'thickness, and a check on the first pieces off the line.'),
            ('Can the box and pouch carry our logo?',
             'Yes. Pouches, boxes and tags are produced through the packaging cluster and developed '
             'alongside the jewellery so inserts fit the finished piece.'),
            ('Do you handle hallmark or composition claims?',
             'We clarify what is being claimed and what documentation supports it before any label is '
             'printed, rather than using a colour description as a composition.'),
            ('Do you dropship single pieces to buyers?',
             'No. Single-parcel direct-to-consumer dropshipping from China across the GCC is outside '
             'the work we take on.'),
        ],
        'related': ['dongguan-packaging', 'guangzhou-womenswear', 'shantou-chaoyang-sleepwear'],
    },
    {
        'slug': 'dongguan-packaging',
        'city': 'Dongguan & Shenzhen',
        'region': 'Guangdong, South China',
        'category': 'Custom packaging & printing',
        'h1': 'Custom Packaging from Dongguan and Shenzhen: A Gulf Buyer\'s Guide',
        'title': 'Custom Packaging & Printing from Dongguan / Shenzhen for Gulf Buyers | SourceToGulf',
        'desc': 'How Gulf brands develop folding cartons, rigid gift boxes and inserts in Guangdong: dielines, '
                'printing and finishing, Arabic artwork checks, and why box minimums differ from product minimums.',
        'answer': 'Dongguan and Shenzhen in Guangdong hold printing, die-cutting, gluing and box-making '
                  'capacity close to the factories that make the products. Gulf buyers develop folding cartons, '
                  'mailer boxes, rigid gift boxes, drawer boxes and paper bags here, with printing, '
                  'die-cutting, gluing and pulp or foam inserts handled in the same production chain. '
                  'Arabic artwork is checked as a printed proof, and each packaging element carries its own '
                  'factory minimum.',
        'facts': [
            ('Cluster', 'Printing, die-cutting, gluing, rigid boxes, paper bags, inserts'),
            ('Typical buyers', 'Brand founders, gifting programmes, boutiques, project buyers'),
            ('Gulf season', 'Ramadan / Eid, National Day, White Friday, corporate gifting'),
            ('Compliance watch', 'Arabic typesetting proof, origin marking, insert fit, trademark authorisation'),
        ],
        'intro': [
            'Packaging is the part of a Gulf order most often planned too late. The box has to fit the '
            'product, carry Arabic and English artwork correctly, and arrive in the same shipment. In '
            'Guangdong the printing press, the folder-gluer, the rigid-box line and the insert maker are '
            'close enough to develop together.',
            'A structural dieline is the starting point, not a logo file. Once the flat structure is '
            'approved, artwork is placed on it and a printed proof is checked — particularly Arabic text, '
            'where a typesetting error is expensive to discover after a full run.',
        ],
        'buys': [
            ('Private-label retail packaging', 'Folding cartons, mailer boxes, labels, hangtags and paper bags.'),
            ('Gifting programmes', 'Rigid gift boxes, drawer boxes and coordinated inserts for Ramadan, Eid and corporate gifting.'),
            ('Product protection', 'Pulp trays, foam or card inserts sized to the finished product.'),
            ('Finishing', 'Hot foil, embossing, spot UV and lamination — chosen for what the design actually needs.'),
        ],
        'compliance': [
            'Approve Arabic artwork on a printed proof. Text reflow, missing joining forms and reversed '
            'order are common when a file is placed into a dieline without a native review.',
            'Country-of-origin and product information belong on the packaging where the destination '
            'requires it; confirm the required fields before artwork is finalised.',
            'Brand marks require written trademark authorisation before printing.',
            'Inserts are cut to the finished product. Finalise product dimensions before the insert '
            'tooling is made.',
        ],
        'pitfalls': [
            ('Arabic text checked on screen only', 'A screen preview can hide reflow and joining issues. '
             'Approve a printed proof with a native reader.'),
            ('Box minimums assumed to match product minimums', 'Carton, rigid box, insert, label and bag '
             'each have their own minimum. Confirm all of them before committing to a launch date.'),
            ('Insert made before the product is final', 'A small dimension change makes the insert useless. '
             'Freeze product dimensions first.'),
            ('Finish chosen for looks, not for transit', 'Foil and soft-touch lamination mark differently '
             'in heat and handling. Ask for a handled sample, not only a flat proof.'),
            ('Packaging produced in a different window', 'Boxes made weeks before the product sit in a '
             'warehouse or miss the shipment. Plan both against one packing date.'),
        ],
        'perfect_for': ['brand-founders', 'gifting-buyers', 'modest-boutiques'],
        'photos': [
            ('images/packaging/package-printing-press.jpg',
             'Printing press on a packaging production floor',
             'A printing press on a packaging production floor. Arabic artwork is checked on a printed '
             'proof before a full run.'),
            ('images/packaging/package-gluing-machine.jpg',
             'Folder-gluer running folding cartons',
             'A folder-gluer running folding cartons. Printing, die-cutting and gluing are separate '
             'steps, each with its own minimum.'),
            ('images/packaging/package-pulp-tray.jpg',
             'Stack of moulded pulp insert trays',
             'Moulded pulp insert trays. Inserts are cut to the finished product, so dimensions are '
             'frozen before tooling.'),
        ],
        'flow': ['Structure / dieline', 'Artwork & AR proof', 'Printing', 'Die-cut & glue', 'Inserts', 'Fit check', 'Pack with goods'],
        'faq': [
            ('Why source packaging from Dongguan and Shenzhen?',
             'Printing, die-cutting, gluing, rigid-box making and inserts sit in the same Guangdong '
             'production region as many of the product factories, so box and product can be developed together.'),
            ('What kinds of boxes can be made?',
             'Folding cartons, mailer boxes, rigid gift boxes, drawer boxes, paper bags and pulp or '
             'card inserts, with finishing such as foil, embossing and spot UV.'),
            ('Do you check Arabic artwork?',
             'Yes. Arabic text is approved on a printed proof with a native reader before the full run.'),
            ('Why are packaging minimums different from product minimums?',
             'Each element — carton, rigid box, insert, label, bag — is a separate production item with '
             'its own factory minimum. We confirm all of them before a launch date is promised.'),
            ('Can packaging be made for a Ramadan gifting programme?',
             'Yes. The schedule is counted backwards from the fixed retail date through artwork, proof, '
             'production and packing.'),
            ('Do you need authorisation for a logo?',
             'Yes. Written trademark authorisation is confirmed before any brand mark is printed.'),
            ('Do you print one box at a time?',
             'No. One-piece custom printing is outside the work we take on; packaging runs follow '
             'factory minimums.'),
        ],
        'related': ['shenzhen-jewellery', 'guangzhou-womenswear', 'zhongshan-lighting'],
    },
    {
        'slug': 'foshan-furniture',
        'city': 'Foshan · Lecong',
        'region': 'Guangdong, South China',
        'category': 'Furniture & fit-out',
        'h1': 'Furniture and Fit-Out from Foshan Lecong: A Gulf Buyer\'s Guide',
        'title': 'Foshan Lecong Furniture & Hospitality Fit-Out Sourcing for Gulf Buyers | SourceToGulf',
        'desc': 'How Gulf hospitality and project buyers source furniture from Foshan\'s Lecong cluster: '
                'bill-of-quantities orders, finishes, flat-pack volume, samples and project handover dates.',
        'answer': 'Lecong in Foshan, Guangdong is a furniture trade and manufacturing cluster serving '
                  'residential, hospitality and commercial fit-out. Gulf project buyers use it for '
                  'multi-item orders against a bill of quantities — seating, tables, case goods and '
                  'flat-packed pieces — where finishes, dimensions and delivery are tied to a site '
                  'handover date. Samples and a written specification come before a project order.',
        'facts': [
            ('Cluster', 'Furniture showrooms, manufacturing, fit-out and flat-pack supply'),
            ('Typical buyers', 'Hospitality, retail fit-out, project buyers, re-export traders'),
            ('Gulf season', 'Project-driven; hotel and retail opening calendars'),
            ('Compliance watch', 'Material declarations, fire-rating questions for contract use, packing volume'),
        ],
        'intro': [
            'Foshan\'s Lecong furniture district combines large showroom coverage with nearby '
            'manufacturing. For a project buyer the useful unit is not a single chair but a bill of '
            'quantities: a list of items, finishes, quantities and a handover date.',
            'That changes how the order is checked. A finish sample, a dimension sheet and a packing '
            'plan matter more than a catalogue photo, because the goods have to arrive together and fit '
            'a site that is already under construction.',
        ],
        'buys': [
            ('Hospitality fit-out', 'Guest-room and public-area furniture specified against an opening date.'),
            ('Retail & commercial spaces', 'Display, counters, seating and coordinated case goods.'),
            ('Re-export ranges', 'Flat-packed and volume-efficient lines for traders moving goods onward.'),
            ('Model units', 'Furnishing packages for show apartments and sample units.'),
        ],
        'compliance': [
            'For contract and hospitality use, raise fire-rating and material-declaration questions at '
            'sampling; these can differ from residential requirements.',
            'Record dimensions, finish and material in a written sheet per item, not in a single '
            'showroom photograph.',
            'Packing volume drives freight. Confirm whether a line ships assembled or flat-packed before '
            'the shipping plan is fixed.',
            'For branded marks in a fit-out, confirm trademark authorisation in writing.',
        ],
        'pitfalls': [
            ('Showroom sample treated as the specification', 'The finish on the floor may not be the finish '
             'ordered. Keep a signed finish sample and a dimension sheet per item.'),
            ('Volume estimated before packing method', 'Assembled versus flat-packed changes the container '
             'plan. Confirm packing before freight is calculated.'),
            ('Contract requirements raised late', 'Fire-rating and material declarations for hospitality '
             'use should be asked at sampling, not at shipment.'),
            ('Items arriving in different windows', 'A project needs one delivery. Consolidate across '
             'factories against a single packing date.'),
            ('Handover date used as the shipping date', 'Transit, customs and site installation sit after '
             'shipping. Count backwards from the handover date.'),
        ],
        'perfect_for': ['project-buyers', 'souq-traders'],
        'photos': [
            ('images/logistics-warehouse.jpg',
             'Racked warehouse with boxed goods ready for consolidation',
             'A consolidation warehouse with boxed goods on racks — multi-item project orders are '
             'brought together against one packing date.'),
            ('images/packing-consolidation.jpg',
             'Cartons being packed and consolidated for shipment',
             'Cartons being consolidated for shipment. Packing method and volume are confirmed before '
             'the freight plan is fixed.'),
        ],
        'flow': ['Bill of quantities', 'Finish samples', 'Dimension sheets', 'Production', 'Consolidation', 'Packing plan', 'Site handover'],
        'faq': [
            ('What is Lecong in Foshan known for?',
             'A furniture trade and manufacturing cluster covering showrooms, residential furniture '
             'and hospitality or commercial fit-out supply.'),
            ('Do you take single-item furniture orders?',
             'Project work starts from a bill of quantities with a written specification. Single-piece '
             'direct-to-consumer shipping is outside the work we take on.'),
            ('How are hospitality requirements handled?',
             'Fire-rating and material-declaration questions are raised at sampling, because contract '
             'requirements can differ from residential ones.'),
            ('Can items from several factories ship together?',
             'Yes. Consolidation against one packing date is a normal part of a project order.'),
            ('How is freight volume estimated?',
             'After the packing method is confirmed — assembled versus flat-packed changes the plan, '
             'so it is fixed before freight is calculated.'),
            ('Can you work to a hotel opening date?',
             'Yes. The schedule is counted backwards from the handover date through transit, customs, '
             'packing, production and sampling.'),
            ('Do you handle installation at the site?',
             'We plan delivery around the project handover. On-site installation scope is confirmed '
             'with the buyer before the order is placed.'),
        ],
        'related': ['zhongshan-lighting', 'dongguan-packaging', 'shenzhen-electronics'],
    },
    {
        'slug': 'zhongshan-lighting',
        'city': 'Zhongshan · Guzhen',
        'region': 'Guangdong, South China',
        'category': 'Lighting & decorative lighting',
        'h1': 'Lighting from Zhongshan Guzhen: A Gulf Buyer\'s Guide',
        'title': 'Zhongshan Guzhen Lighting Sourcing for Gulf Hospitality & Retail | SourceToGulf',
        'desc': 'What Gulf project and seasonal buyers source from Guzhen in Zhongshan: decorative and '
                'commercial lighting, voltage and plug questions, certification routes and Ramadan displays.',
        'answer': 'Guzhen in Zhongshan, Guangdong is a lighting manufacturing and trade cluster covering '
                  'decorative fittings, commercial lighting and seasonal light strings. Gulf buyers use it '
                  'for hospitality and retail fit-out, and for Ramadan and Eid decorative displays. '
                  'Voltage, plug type, IP rating where relevant, and the destination conformity route are '
                  'confirmed before a production order.',
        'facts': [
            ('Cluster', 'Decorative fittings, commercial lighting, seasonal light strings'),
            ('Typical buyers', 'Project and hospitality buyers, retail fit-out, seasonal gifting'),
            ('Gulf season', 'Project openings; Ramadan and Eid display windows'),
            ('Compliance watch', 'Voltage / plug, ECAS and SABER routes for electrical goods, IP rating'),
        ],
        'intro': [
            'Guzhen concentrates lighting manufacturing, components and showrooms in one town in '
            'Zhongshan. A project buyer can review fittings, finishes and light temperature in person '
            'rather than choosing from isolated catalogue images.',
            'Electrical goods are also the category where the paperwork matters most. Voltage, plug '
            'type and the destination conformity route are decided at specification stage, because a '
            'finished batch cannot be re-certified after the fact.',
        ],
        'buys': [
            ('Hospitality & retail fit-out', 'Decorative fittings, downlights and coordinated lighting plans for a site.'),
            ('Seasonal displays', 'Light strings and decorative pieces for Ramadan, Eid and National Day retail windows.'),
            ('Commercial spaces', 'Repeated fittings across a chain or a project with a consistent finish and colour temperature.'),
            ('Gifting programmes', 'Decorative lighting packed with coordinated gift packaging.'),
        ],
        'compliance': [
            'Electrical appliances can fall under mandatory certification — ECAS in the UAE and SABER '
            'for Saudi Arabia. Confirm the applicable route for the exact model before production.',
            'Confirm voltage and plug type for the destination market in the written specification.',
            'Where fittings are used outdoors or in wet areas, agree the IP rating at sampling.',
            'Keep the model number, the test documentation and the physical sample in the same order '
            'file; they are checked together before shipment.',
        ],
        'pitfalls': [
            ('Certification asked about after production', 'A finished batch cannot be re-certified to a '
             'different model. Confirm the ECAS / SABER route at specification stage.'),
            ('Colour temperature mixed across a project', 'Two batches of "warm white" can differ. '
             'Approve a lit sample and keep it as the reference for the whole order.'),
            ('Plug and voltage assumed', 'A plug that does not match the destination is discovered at '
             'installation. Put both in the specification.'),
            ('Outdoor rating assumed', 'Decorative strings used outside need an agreed IP rating. '
             'Ask at sampling, not after the display is built.'),
            ('Seasonal deadline counted from shipping', 'A Ramadan display date is fixed. Count '
             'backwards through transit, certification, production and sample approval.'),
        ],
        'perfect_for': ['project-buyers', 'gifting-buyers', 'souq-traders'],
        'photos': [
            ('images/islamic-decor-display.jpg',
             'Warm decorative light strings used in a festive display',
             'Warm decorative light strings in a festive display. Seasonal lighting is ordered against '
             'a fixed Ramadan or Eid retail date.'),
            ('images/products/ramadan-lights.jpg',
             'Small decorative lights arranged for a seasonal table setting',
             'Small decorative lights arranged for a seasonal table setting — the kind of display '
             'piece Gulf retailers plan well ahead of the season.'),
        ],
        'flow': ['Specification', 'Lit sample', 'Certification route', 'Production', 'Model / doc check', 'Packing', 'Ship to GCC'],
        'faq': [
            ('What is Guzhen in Zhongshan known for?',
             'Lighting manufacturing and trade, including decorative fittings, commercial lighting and '
             'seasonal light strings.'),
            ('Do lighting products need certification for the Gulf?',
             'Electrical appliances can fall under mandatory routes such as ECAS in the UAE and SABER '
             'for Saudi Arabia. The route is confirmed for the exact model before production.'),
            ('Can you supply a whole hotel or retail lighting plan?',
             'Yes, against a bill of quantities with an approved lit sample and consistent colour '
             'temperature across the order.'),
            ('How do you keep colour temperature consistent?',
             'A lit sample is approved and retained as the reference for the entire batch.'),
            ('Do you handle Ramadan decorative lighting?',
             'Yes. Seasonal orders are scheduled backwards from the fixed display date.'),
            ('What should be in the specification?',
             'Model, voltage, plug type for the destination, IP rating where relevant, finish and '
             'colour temperature.'),
            ('Do you take categories with no compliance path?',
             'No. Categories requiring mandatory certification without a viable route are outside '
             'the work we take on.'),
        ],
        'related': ['foshan-furniture', 'dongguan-packaging', 'shenzhen-electronics'],
    },
    {
        'slug': 'shenzhen-electronics',
        'city': 'Shenzhen & Dongguan',
        'region': 'Guangdong, South China',
        'category': 'Consumer electronics & equipment',
        'h1': 'Consumer Electronics and Equipment from Shenzhen / Dongguan: A Gulf Buyer\'s Guide',
        'title': 'Shenzhen & Dongguan Electronics Sourcing for Gulf Project Buyers | SourceToGulf',
        'desc': 'How Gulf project and wholesale buyers source multi-model electronics from Shenzhen and '
                'Dongguan: model lists, certification routes, documentation sets and consolidation.',
        'answer': 'Shenzhen and Dongguan in Guangdong hold consumer-electronics and equipment supply chains '
                  'covering components, assembly, accessories and security or storage devices. Gulf project '
                  'and wholesale buyers use them for multi-model orders against a list, where the value is '
                  'in matching exact model numbers, accessory sets and documentation rather than in a single '
                  'unit price. Applicable conformity routes are confirmed before an order is placed.',
        'facts': [
            ('Cluster', 'Components, assembly, accessories, security and storage devices'),
            ('Typical buyers', 'Project buyers, wholesalers, re-export traders'),
            ('Gulf season', 'Project-driven; retail replenishment cycles'),
            ('Compliance watch', 'ECAS / SABER for electrical appliances, model numbers, documentation set'),
        ],
        'intro': [
            'A Gulf project buyer rarely orders one device. The order is a list: several models, '
            'matching accessories, a common documentation set and one delivery date. Shenzhen and '
            'Dongguan are useful here because components, assembly and accessory supply sit in the '
            'same region and can be consolidated into one shipment.',
            'This is also the category where an incomplete specification does the most damage. An '
            'exact model number, the accessory list and the applicable conformity route have to be '
            'locked before production, because a substituted model changes the paperwork.',
        ],
        'buys': [
            ('Project equipment lists', 'Multi-model orders with matched accessories and a single handover date.'),
            ('Security & storage devices', 'Devices specified by exact model with the accompanying documentation.'),
            ('Accessories & peripherals', 'Cables, mounts, cases and add-on items consolidated with the main order.'),
            ('Wholesale replenishment', 'Repeat model runs with consistent packaging and labelling.'),
        ],
        'compliance': [
            'Electrical appliances may fall under ECAS (UAE) or SABER (Saudi Arabia). Confirm the route '
            'for each exact model before production.',
            'Record exact model numbers and the accessory list in the specification; a substituted '
            'model invalidates the documentation set.',
            'Agree the documentation pack — declarations, manuals and labelling — before shipment, '
            'and check it against the physical goods.',
            'Confirm plug type, voltage and language requirements for manuals at specification stage.',
        ],
        'pitfalls': [
            ('Model substituted after the quote', 'A different model can look identical and carry '
             'different paperwork. Lock model numbers and check the first cartons.'),
            ('Certification route left to the end', 'ECAS / SABER questions raised at booking can stop '
             'a shipment. Confirm at specification stage.'),
            ('Accessory list assumed', 'Mounts, cables and power supplies are separate line items. '
             'List them explicitly.'),
            ('Documentation not matched to goods', 'A manual or declaration for another model is a '
             'common cause of a held shipment. Check the pack against the physical units.'),
            ('Multi-model order shipped in pieces', 'A project needs one handover. Consolidate against '
             'one packing date.'),
        ],
        'perfect_for': ['project-buyers', 'souq-traders'],
        'photos': [
            ('images/factory-components.jpg',
             'Tray of small electronic components on a production floor',
             'A tray of small electronic components on a production floor. Exact model numbers and '
             'accessory lists are locked in the specification before a multi-model order.'),
            ('images/warehouse-inspection.jpg',
             'Cartons being checked in a warehouse before shipment',
             'Cartons being checked in a warehouse before shipment. Documentation is matched against '
             'the physical goods as part of the pre-shipment check.'),
        ],
        'flow': ['Model list', 'Certification route', 'Specification lock', 'Production', 'Doc pack', 'Consolidation', 'Ship to GCC'],
        'faq': [
            ('What do Shenzhen and Dongguan supply for Gulf buyers?',
             'Consumer electronics and equipment supply chains — components, assembly, accessories, '
             'and security or storage devices — often ordered as multi-model lists.'),
            ('Do electronics need certification for the Gulf?',
             'Electrical appliances may fall under ECAS in the UAE or SABER for Saudi Arabia. The route '
             'is confirmed for each exact model before production.'),
            ('Can you handle an order with many different models?',
             'Yes. Multi-model orders are consolidated against one packing date with a matched '
             'documentation set.'),
            ('What is the most common problem with these orders?',
             'A model substituted after the specification was agreed, which changes the paperwork. '
             'Model numbers are locked and the first cartons are checked.'),
            ('Do you consolidate accessories with the main order?',
             'Yes, provided cables, mounts and power supplies are listed explicitly as line items.'),
            ('Do you take categories without a compliance path?',
             'No. Categories that require mandatory certification but have no viable route are '
             'outside the work we take on.'),
            ('Do you ship single units to end customers?',
             'No. Single-parcel direct-to-consumer dropshipping from China across the GCC is outside '
             'the work we take on.'),
        ],
        'related': ['foshan-furniture', 'zhongshan-lighting', 'dongguan-packaging'],
    },
]

# ---------------------------------------------------------------------------
# 四、hub 页 FAQ（可见 FAQ 与 FAQPage schema 同源逐字一致）
# ---------------------------------------------------------------------------
HUB_FAQ = [
    ('Why organise sourcing by Chinese industrial cluster instead of by product?',
     'Because China\'s manufacturing is concentrated in a limited number of city-level clusters, each with '
     'its own materials, processes and compliance habits. Searching by cluster tells a buyer what can '
     'realistically be sampled, changed and reordered; searching by product photo does not. For a Gulf '
     'buyer it also makes the labelling and certification conversation concrete, since the same product '
     'can carry different requirements depending on where and how it is made.'),
    ('Which Chinese clusters matter most for Gulf buyers?',
     'Eight clusters recur in Gulf sourcing: Shantou Chaoyang for sleepwear and knitwear; Guangzhou for '
     'womenswear and modest fashion; Shishi and Jinjiang in Fujian for sportswear and casualwear; Shenzhen '
     'Shuibei for fashion jewellery; Dongguan and Shenzhen for custom packaging; Foshan Lecong for '
     'furniture and fit-out; Zhongshan Guzhen for lighting; and Shenzhen and Dongguan for consumer '
     'electronics and equipment.'),
    ('Does SourceToGulf publish a product catalogue with prices?',
     'No. SourceToGulf is a sourcing partner, not a retailer. It does not hold inventory or publish a '
     'purchasable price list. The capability samples shown elsewhere on the site illustrate categories '
     'and are not purchasable stock. A buyer starts from a photo, a link or a specification, and a written '
     'quotation is prepared for that specific request.'),
    ('Do you work with dropshipping sellers?',
     'No. Single-parcel, direct-to-consumer dropshipping from China to end customers across the GCC, '
     'where goods are not already warehoused inside the GCC, is outside the work we take on. We also do '
     'not take one-piece customisation, counterfeit or IP-infringing branded goods, illegal or hazardous '
     'cargo, or categories requiring mandatory certification without a viable compliance path.'),
    ('Which Gulf buyer types is this built for?',
     'Six: social commerce sellers; modest-fashion and abaya boutiques; souq traders, wholesalers and '
     're-exporters; brand founders and private-label owners; hospitality, retail and project buyers; '
     'and corporate or seasonal gifting buyers. Each starts from a different document — a screenshot, '
     'a style list, a category plan, a logo, a bill of quantities or a deadline.'),
    ('What do I need to send to start?',
     'A product reference (a photo, a link or a text description), the destination GCC country, and '
     'whatever specification you already have — material, quantity, private-label intent and timeline. '
     'A written quotation follows for that specific request; there is no public price list to browse.'),
    ('Is there a fee to start a sourcing request?',
     'Yes. A USD 125 sourcing intent deposit applies. It is credited in full against the order value, '
     'or billed as a sourcing service fee for the work performed if no order is placed. Quotations are '
     'valid for one week, and a person reviews every request before work starts.'),
    ('Do you handle SABER, ECAS and Arabic labelling?',
     'The applicable route is confirmed for the exact product and destination before production. '
     'English/Arabic care, composition and origin labels are approved as physical samples rather than '
     'added after a batch is made; conformity documentation is prepared before shipment.'),
]

HUB_ANSWER = (
    'China\'s export manufacturing is concentrated in a limited number of city-level clusters rather '
    'than spread evenly across the country. For a Gulf buyer, the useful question is not "can I find '
    'this product" but "which cluster makes it, what can be changed there, and what paperwork does it '
    'need before it reaches Saudi Arabia or the UAE". This page maps eight clusters that recur in GCC '
    'sourcing — from Shantou sleepwear and Guangzhou modest fashion to Guzhen lighting and Foshan '
    'furniture — against six buyer types that actually operate in the Gulf market. SourceToGulf is a '
    'sourcing partner, not a retailer: there is no price list here, and single-piece dropshipping to '
    'end customers across the GCC is not a service we take on.'
)
