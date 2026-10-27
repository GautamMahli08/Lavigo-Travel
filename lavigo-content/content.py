"""All LAVIGO website texts. Edit this file, then rebuild with:  python build_lavigo.py

Images are referenced by their file name (without .jpg) in lavigo-content/images/.
To use your own photo: drop it in that folder (e.g. nepal-everest.jpg) and rebuild,
or add a new file and change the name below. Photo credits live in images/credits.json.
"""

COMPANY = "LAVIGO"
YEAR = 2026

# ---------------------------------------------------------------- contact details (placeholders - replace these)
CONTACT = {
    "address_lines": ["[LAVIGO office address]", "[City, PIN code, Country]"],
    "map_link": "#",
    "phone": "[+91 00000 00000]",
    "phone_link": "#",
    "email": "[hello@your-domain.com]",
    "email_link": "#",
    # WhatsApp number used for bookings: country code + number, digits only (e.g. 919876543210)
    "whatsapp": "919031474036",
    "facebook": "#",
    "instagram": "#",
    "hours": [
        ("Monday to Saturday", "[9:30 am - 6:30 pm IST]"),
        ("Sunday", "[Closed - email us any time]"),
    ],
    # legal notice
    "legal_name": "[LAVIGO registered company name]",
    "registration": "[Company registration number / GSTIN]",
    "director": "[Name of the person responsible for publication]",
    "host": "[Website hosting provider, address]",
}

HERO = {
    "image": "hero-parvati-valley",
    "line1": "Let yourself be transported",
    "line2": "to the Himalayas",
    "description": "Tailor-made journeys to Nepal, Everest Base Camp, Sikkim, Darjeeling, Bhutan and Manali.",
}

# ---------------------------------------------------------------- destinations
# map_icon: index of the original map pictogram to reuse (0-7), map_color: pin colour
DESTINATIONS = [
    {
        "slug": "nepal",
        "name": "Nepal",
        "title": ("Nepal", "Roof of the world"),
        "hero": "nepal-everest",
        "card_image": "nepal-boudhanath",
        "card_text": "Eight of the world's ten highest peaks, ancient royal cities and the warm welcome of the Kathmandu Valley.",
        "map_text": "From the stupas of Kathmandu to the lakes of Pokhara and the trails of the Everest region.",
        "map_icon": 7,
        "map_color": "#243179",
        "intro": [
            "Nepal stretches from the jungles of the Terai to the summit of Mount Everest, the highest point on Earth. In a few hundred kilometres you pass from rice terraces and rhododendron forests to glaciers and some of the most famous trekking trails in the world.",
            "In the Kathmandu Valley, centuries-old temples, stupas and palace squares are still at the heart of everyday life. Whether you come to trek, to discover Himalayan culture or simply to slow down by a lake, Nepal leaves a lasting mark.",
        ],
        "places": [
            {
                "label": "Kathmandu Valley",
                "name": "Boudhanath & Swayambhunath",
                "text": [
                    "Boudhanath is one of the largest stupas in the world and the spiritual heart of Tibetan Buddhism in Nepal. Join the pilgrims walking clockwise around its white dome at dusk, as butter lamps are lit and prayer wheels turn.",
                    "On its hilltop above the city, Swayambhunath - the \"monkey temple\" - offers sweeping views over Kathmandu. Both sites are part of the Kathmandu Valley UNESCO World Heritage Site.",
                ],
                "images": ["nepal-boudhanath", "nepal-swayambhunath", "nepal-kathmandu-durbar"],
            },
            {
                "label": "Royal city",
                "name": "Bhaktapur",
                "text": [
                    "Bhaktapur is a living museum of Newar art and architecture. Its Durbar Square, brick lanes and pagoda temples - including the five-storey Nyatapola - are best explored on foot, with a stop for the town's famous juju dhau, the \"king of curds\".",
                ],
                "images": ["nepal-bhaktapur"],
            },
            {
                "label": "Lakeside",
                "name": "Pokhara & Phewa Lake",
                "text": [
                    "Gateway to the Annapurna region, Pokhara sits on the shores of Phewa Lake with the snow peaks reflected in its waters on clear mornings. Paddle out to the island temple of Tal Barahi, paraglide above the valley or watch the sunrise from Sarangkot.",
                ],
                "images": ["nepal-phewa-lake", "nepal-pokhara"],
            },
            {
                "label": "Trekking",
                "name": "Everest region",
                "text": [
                    "At 8,849 metres, Mount Everest towers over the Khumbu valley. A flight to Lukla opens the way to Sherpa villages, monasteries and viewpoints such as Gokyo Ri and Kala Patthar. We organise treks for every level, from short scenic routes to Everest Base Camp.",
                ],
                "images": ["nepal-everest"],
            },
            {
                "label": "Wildlife",
                "name": "Chitwan National Park",
                "text": [
                    "Nepal's first national park and a UNESCO World Heritage Site, Chitwan protects forests and grasslands that are home to the one-horned rhinoceros, the Bengal tiger and hundreds of bird species. Explore it on a jungle walk, by jeep or by dugout canoe.",
                ],
                "images": ["nepal-chitwan"],
            },
        ],
    },
    {
        "slug": "gangtok",
        "name": "Gangtok",
        "title": ("Gangtok", "Capital of Sikkim"),
        "hero": "gangtok-view",
        "card_image": "gangtok-tsomgo",
        "card_text": "A hillside capital facing Kangchenjunga, with monasteries, glacial lakes and high mountain passes close by.",
        "map_text": "Sikkim's lively capital, its monasteries and the road to Tsomgo Lake and Nathu La.",
        "map_icon": 0,
        "map_color": "#243179",
        "intro": [
            "Built along a ridge at around 1,650 metres, Gangtok is the capital of Sikkim and the perfect base for exploring the eastern Himalayas. On clear days the city looks straight out at Kangchenjunga, the third-highest mountain in the world.",
            "Clean, friendly and easy to explore on foot, Gangtok mixes Buddhist monasteries, colourful markets and cafés with quick access to high-altitude lakes and passes.",
        ],
        "places": [
            {
                "label": "Promenade",
                "name": "MG Marg",
                "text": [
                    "Gangtok's pedestrian-only main street is the meeting point of the city. Lined with shops, cafés and flower beds, MG Marg is perfect for an evening stroll, a plate of momos and some people-watching.",
                ],
                "images": ["gangtok-mg-marg", "gangtok-view"],
            },
            {
                "label": "Monasteries",
                "name": "Rumtek & Enchey",
                "text": [
                    "About 24 km from Gangtok, Rumtek Monastery is one of the most important seats of the Karma Kagyu school of Tibetan Buddhism. Closer to the centre, the colourful Enchey Monastery is famous for its masked Cham dances.",
                ],
                "images": ["gangtok-rumtek", "gangtok-enchey"],
            },
            {
                "label": "Glacial lake",
                "name": "Tsomgo Lake",
                "text": [
                    "At around 3,750 metres, Tsomgo (Changu) Lake is surrounded by steep mountain slopes that are snow-covered in winter and dotted with flowers in spring. A permit is required - we arrange it for you.",
                ],
                "images": ["gangtok-tsomgo"],
            },
            {
                "label": "Mountain pass",
                "name": "Nathu La",
                "text": [
                    "At about 4,310 metres on the old Silk Route between India and Tibet, Nathu La is one of the highest motorable passes you can visit. Access is limited to Indian nationals with a permit and depends on the weather.",
                ],
                "images": ["gangtok-nathu-la"],
            },
            {
                "label": "Viewpoint & culture",
                "name": "Hanuman Tok & Tibetology",
                "text": [
                    "Above the city, the Hanuman Tok temple offers one of the finest views of the Kangchenjunga range. Down in town, the Namgyal Institute of Tibetology houses a remarkable collection of thangkas, statues and manuscripts.",
                ],
                "images": ["gangtok-hanuman-tok", "gangtok-tibetology", "gangtok-city"],
            },
        ],
    },
    {
        "slug": "darjeeling",
        "name": "Darjeeling",
        "title": ("Darjeeling", "Queen of the hills"),
        "hero": "darjeeling-kanchenjunga",
        "card_image": "darjeeling-toy-train",
        "card_text": "Tea gardens, the UNESCO-listed toy train and sunrise over Kangchenjunga from Tiger Hill.",
        "map_text": "Tea estates, the historic toy train and legendary Himalayan sunrises.",
        "map_icon": 2,
        "map_color": "#243179",
        "intro": [
            "Perched at about 2,050 metres, Darjeeling is famous the world over for its tea and its views of Kangchenjunga. Colonial-era buildings, Buddhist monasteries and busy bazaars cling to the hillside above endless green tea gardens.",
            "Take the little steam train, taste a first-flush tea where it was grown and get up early for one of the most beautiful sunrises in the Himalayas.",
        ],
        "places": [
            {
                "label": "Sunrise",
                "name": "Tiger Hill",
                "text": [
                    "At 2,567 metres, Tiger Hill is the place to watch the first light of day turn the snows of Kangchenjunga pink and gold. On very clear mornings, Mount Everest can be seen in the distance.",
                ],
                "images": ["darjeeling-tiger-hill", "darjeeling-kanchenjunga"],
            },
            {
                "label": "UNESCO heritage",
                "name": "The toy train",
                "text": [
                    "Opened in 1881, the Darjeeling Himalayan Railway is a UNESCO World Heritage Site. Its tiny two-foot-gauge trains climb through loops and zig-zags, passing right through the bazaars of the hill towns.",
                ],
                "images": ["darjeeling-toy-train", "darjeeling-town"],
            },
            {
                "label": "Memorial gardens",
                "name": "Batasia Loop",
                "text": [
                    "The railway spirals around the Batasia Loop to gain height. Its landscaped gardens, home to the Gorkha war memorial, offer a superb panorama of the town and the Kangchenjunga range.",
                ],
                "images": ["darjeeling-batasia"],
            },
            {
                "label": "Tea country",
                "name": "Happy Valley Tea Estate",
                "text": [
                    "Established in 1854, Happy Valley is one of Darjeeling's oldest tea gardens. Walk among the bushes, discover how the leaves are withered, rolled and dried, and finish with a tasting of the famous \"champagne of teas\".",
                ],
                "images": ["darjeeling-tea", "darjeeling-tea-2"],
            },
            {
                "label": "Peace",
                "name": "Japanese Peace Pagoda",
                "text": [
                    "Set in the forest on the slopes of Jalapahar hill, the white Peace Pagoda is a haven of calm, with golden statues of the Buddha and views over the town and the mountains.",
                ],
                "images": ["darjeeling-peace-pagoda", "darjeeling-zoo"],
            },
        ],
    },
    {
        "slug": "manali",
        "name": "Manali",
        "title": ("Manali", "Valley of the gods"),
        "hero": "manali-town",
        "card_image": "manali-solang",
        "card_text": "Cedar forests, snow-capped passes and adventure sports at the head of the Kullu Valley.",
        "map_text": "The adventure capital of Himachal Pradesh, between cedar forests and high passes.",
        "map_icon": 3,
        "map_color": "#243179",
        "intro": [
            "At the northern end of the Kullu Valley, Manali sits at about 2,050 metres on the banks of the Beas river, surrounded by deodar forests and snowy peaks. It is the starting point for the road to Lahaul, Spiti and Ladakh.",
            "Ancient wooden temples, apple orchards and hot springs sit alongside skiing, paragliding, rafting and trekking - Manali has something for every traveller.",
        ],
        "places": [
            {
                "label": "Sacred forest",
                "name": "Hidimba Devi Temple",
                "text": [
                    "Built in 1553 in a grove of giant cedars, this wooden temple dedicated to the goddess Hidimba is a masterpiece of Himalayan pagoda architecture, with finely carved doors and a four-tiered roof.",
                ],
                "images": ["manali-hidimba"],
            },
            {
                "label": "Adventure",
                "name": "Solang Valley",
                "text": [
                    "Just north of Manali, Solang Valley is the place for paragliding and zorbing in summer, and for skiing and snow play in winter. A ropeway climbs to viewpoints over the glaciers.",
                ],
                "images": ["manali-solang", "manali-kullu"],
            },
            {
                "label": "High pass",
                "name": "Rohtang Pass",
                "text": [
                    "At about 3,980 metres, Rohtang Pass separates the green Kullu Valley from the high-altitude desert of Lahaul. It is usually open from late spring to autumn and requires a permit, which we arrange for you.",
                ],
                "images": ["manali-rohtang"],
            },
            {
                "label": "Engineering marvel",
                "name": "Atal Tunnel",
                "text": [
                    "Opened in 2020, the 9 km Atal Tunnel runs beneath the Rohtang range and links Manali to the Lahaul valley all year round. Cross it for a day trip to Sissu and its waterfalls.",
                ],
                "images": ["manali-atal-tunnel"],
            },
            {
                "label": "Hot springs",
                "name": "Vashisht & the Beas river",
                "text": [
                    "Across the river from Manali, the village of Vashisht is known for its stone temples and natural hot sulphur springs. Below, the Beas river is ideal for rafting and riverside walks.",
                ],
                "images": ["manali-vashisht", "manali-beas"],
            },
        ],
    },
    {
        "slug": "lachen-and-lachung",
        "name": "Lachen & Lachung",
        "title": ("Lachen & Lachung", "North Sikkim"),
        "hero": "lachung-village",
        "card_image": "lachen-gurudongmar",
        "card_text": "Remote mountain villages, a sacred lake at over 5,000 metres and valleys covered in rhododendrons.",
        "map_text": "The wild high valleys of North Sikkim, from Gurudongmar Lake to Yumthang.",
        "map_icon": 6,
        "map_color": "#2d540e",
        "intro": [
            "In the far north of Sikkim, the villages of Lachen and Lachung guard the valleys that lead to the Tibetan plateau. Here the road follows roaring rivers past waterfalls, pine forests and wooden houses, to landscapes of snow, ice and high-altitude lakes.",
            "North Sikkim is a protected area: permits are required and some sites are open to Indian nationals only. LAVIGO handles permits, vehicles and stays so you can simply enjoy the journey.",
        ],
        "places": [
            {
                "label": "Sacred lake",
                "name": "Gurudongmar Lake",
                "text": [
                    "At about 5,430 metres, Gurudongmar is one of the highest lakes in the world and is sacred to Buddhists, Sikhs and Hindus alike. Its turquoise waters, framed by snow peaks, are reached on an early-morning drive from Lachen.",
                ],
                "images": ["lachen-gurudongmar"],
            },
            {
                "label": "Valley of flowers",
                "name": "Yumthang Valley",
                "text": [
                    "Above Lachung, at around 3,560 metres, the Yumthang Valley turns pink and red when the rhododendrons bloom in spring. Hot springs, grazing yaks and a meandering river complete the scene.",
                ],
                "images": ["lachung-yumthang"],
            },
            {
                "label": "End of the road",
                "name": "Zero Point",
                "text": [
                    "Beyond Yumthang, the road climbs to Yumesamdong, known as Zero Point, at about 4,700 metres - a world of snow and rock where the tarmac ends.",
                ],
                "images": ["lachung-zero-point"],
            },
            {
                "label": "High valleys",
                "name": "Thangu & Chopta",
                "text": [
                    "On the way to Gurudongmar, the high meadows of Thangu and the Chopta valley offer breathtaking views of Mount Khangchengyao and are a good place to acclimatise.",
                ],
                "images": ["lachen-thangu", "lachen-khangchengyao"],
            },
            {
                "label": "Mountain villages",
                "name": "Monasteries of Lachen & Lachung",
                "text": [
                    "Both villages are home to Buddhist monasteries overlooking the valleys. Spend the night in a local homestay to share the daily life of the Lachenpa and Lachungpa communities.",
                ],
                "images": ["lachen-monastery", "lachung-monastery", "lachen-teesta"],
            },
        ],
    },
    {
        "slug": "pelling",
        "name": "Pelling",
        "title": ("Pelling", "West Sikkim"),
        "hero": "pelling-kanchenjunga",
        "card_image": "pelling-pemayangtse",
        "card_text": "A ridge-top town facing Kangchenjunga, with ancient monasteries, royal ruins and a sacred lake.",
        "map_text": "Sunrise over Kangchenjunga, Pemayangtse Monastery and the sacred Khecheopalri Lake.",
        "map_icon": 7,
        "map_color": "#2d540e",
        "intro": [
            "Perched at about 2,150 metres in West Sikkim, Pelling looks straight across at the Kangchenjunga range - on a clear morning the snows turn pink and gold at sunrise, right from your hotel window.",
            "Around the town, forest trails lead to some of Sikkim's oldest monasteries, the ruins of its second royal capital and a hidden lake held sacred by Buddhists and Hindus alike.",
        ],
        "places": [
            {
                "label": "Mountain views",
                "name": "Kangchenjunga from Pelling",
                "text": ["Few places in the Himalayas offer such a close and complete view of Kangchenjunga, the third-highest mountain on Earth. Sunrise is the magic moment."],
                "images": ["pelling-kanchenjunga"],
            },
            {
                "label": "Monastery",
                "name": "Pemayangtse",
                "text": ["Founded at the end of the 17th century, Pemayangtse is one of the oldest and most important monasteries of Sikkim, known for its seven-storey wooden model of the celestial palace of Guru Rinpoche."],
                "images": ["pelling-pemayangtse"],
            },
            {
                "label": "Royal history",
                "name": "Rabdentse Ruins",
                "text": ["A short forest walk leads to the ruins of Rabdentse, the capital of the kingdom of Sikkim from the 17th to the early 19th century, with views over the valleys below."],
                "images": ["pelling-rabdentse"],
            },
            {
                "label": "Sacred lake",
                "name": "Khecheopalri Lake",
                "text": ["Surrounded by forest, this calm lake is known as the wish-fulfilling lake. It is said that birds keep its surface free of leaves."],
                "images": ["pelling-khecheopalri"],
            },
            {
                "label": "New landmark",
                "name": "Skywalk & Chenrezig statue",
                "text": ["A glass-floored skywalk leads to the giant statue of Chenrezig, the Buddha of Compassion, overlooking the mountains."],
                "images": ["pelling-skywalk"],
            },
        ],
    },
    {
        "slug": "bhutan",
        "name": "Bhutan",
        "title": ("Bhutan", "Land of the Thunder Dragon"),
        "hero": "bhutan-taktsang",
        "card_image": "bhutan-punakha",
        "card_text": "Fortress-monasteries, prayer-flag passes and the Tiger's Nest in the kingdom of happiness.",
        "map_text": "Thimphu, Punakha and the legendary Tiger's Nest monastery above Paro.",
        "map_icon": 0,
        "map_color": "#2d540e",
        "intro": [
            "Bhutan is a small Himalayan kingdom that has kept its culture and its forests intact - it famously measures progress in Gross National Happiness. Its dzongs (fortress-monasteries), festivals and traditional dress are part of everyday life.",
            "All visitors need a permit and pay a Sustainable Development Fee per night set by the Government of Bhutan. LAVIGO arranges the permits, a licensed guide and everything else for you.",
        ],
        "places": [
            {
                "label": "Icon of Bhutan",
                "name": "Paro Taktsang",
                "text": ["The Tiger's Nest monastery clings to a cliff about 900 metres above the Paro valley. The hike up through pine forest and prayer flags is the highlight of any trip to Bhutan."],
                "images": ["bhutan-taktsang"],
            },
            {
                "label": "Dzong",
                "name": "Punakha Dzong",
                "text": ["Built in the 17th century where the Pho Chhu and Mo Chhu rivers meet, Punakha Dzong is often called the most beautiful fortress in the country, especially when the jacaranda trees bloom in spring."],
                "images": ["bhutan-punakha"],
            },
            {
                "label": "Mountain pass",
                "name": "Dochula Pass",
                "text": ["At about 3,100 metres on the road from Thimphu to Punakha, Dochula is crowned by 108 memorial chortens, with views of the high Himalayas on clear days."],
                "images": ["bhutan-dochula"],
            },
            {
                "label": "Capital",
                "name": "Thimphu & Buddha Dordenma",
                "text": ["Bhutan's capital is a city without traffic lights. Above it, the giant golden Buddha Dordenma statue watches over the valley."],
                "images": ["bhutan-dordenma"],
            },
        ],
    },
    {
        "slug": "everest-base-camp",
        "name": "Everest Base Camp",
        "title": ("Everest Base Camp", "Khumbu region, Nepal"),
        "hero": "ebc-kala-patthar",
        "card_image": "ebc-base-camp",
        "card_text": "Sherpa villages, mountain monasteries and the foot of the highest mountain on Earth.",
        "map_text": "The classic trek through the Khumbu to the foot of Mount Everest.",
        "map_icon": 6,
        "map_color": "#243179",
        "intro": [
            "The Khumbu region in north-eastern Nepal is home to Mount Everest and the Sherpa people. From the tiny airstrip of Lukla, trails lead through forests, suspension bridges and stone villages to the glaciers at the foot of the world's highest peaks.",
            "Reaching Everest Base Camp takes about ten days of walking with acclimatisation stops - an unforgettable adventure for fit walkers, guided every step of the way.",
        ],
        "places": [
            {
                "label": "Sherpa capital",
                "name": "Namche Bazaar",
                "text": ["Built in a horseshoe-shaped bowl at about 3,440 metres, Namche is the trading hub of the Khumbu and the place to acclimatise, with bakeries, gear shops and the first views of Everest."],
                "images": ["ebc-namche"],
            },
            {
                "label": "Monastery",
                "name": "Tengboche",
                "text": ["The most important monastery of the Khumbu stands on a ridge at about 3,860 metres, with Ama Dablam and Everest rising behind it."],
                "images": ["ebc-tengboche"],
            },
            {
                "label": "The goal",
                "name": "Everest Base Camp",
                "text": ["At about 5,360 metres beside the Khumbu Icefall, the base camp used by Everest expeditions is the end point of the trek."],
                "images": ["ebc-base-camp"],
            },
            {
                "label": "Viewpoint",
                "name": "Kala Patthar",
                "text": ["A pre-dawn climb to Kala Patthar (about 5,550 m) gives the classic close-up view of the summit of Mount Everest."],
                "images": ["ebc-kala-patthar", "nepal-everest"],
            },
        ],
    },
]

# order of the destinations on the site (menu, map, cards, carousel)
_ORDER = ["nepal", "everest-base-camp", "gangtok", "lachen-and-lachung", "darjeeling", "pelling", "bhutan", "manali"]
DESTINATIONS.sort(key=lambda d: _ORDER.index(d["slug"]) if d["slug"] in _ORDER else 99)

DESTINATIONS_PAGE = {
    "title": "Discover the destinations",
    "image": "manali-kullu",
    "intro": "From the temples of Kathmandu to the high lakes of North Sikkim, LAVIGO takes you to the most beautiful corners of the Himalayas. Choose your destination - we take care of the rest: stays, transport, permits and local guides.",
    "outro_title": "Journeys tailored to you",
    "outro_text": [
        "Every LAVIGO journey is designed around your dates, your pace and your interests. Combine several destinations - for example Darjeeling, Gangtok and North Sikkim in a single trip - or focus on one region in depth.",
        "Tell us about your plans and we will send you a personalised itinerary.",
    ],
    "outro_image": "gangtok-hanuman-tok",
}

GALLERY = {"line1": "Explore", "line2": "the Himalayas"}
MAP = {"line1": "Travel", "line2": "map"}
BLOG_SECTION = {"line1": "Headlines", "line2": "from the Himalayas"}
OUTRO = {"line1": COMPANY, "line2": "Himalayan journeys", "image": "lachung-yumthang", "region": "Himalayas"}
FOOTER_TAGLINE = "Tailor-made journeys across Nepal, Sikkim, Darjeeling, Bhutan and Himachal Pradesh."
NEWSLETTER = {"title": "Subscribe to our newsletter", "text": "Travel ideas and offers from LAVIGO, straight to your inbox"}

# ---------------------------------------------------------------- blog posts
BLOG = [
    {
        "slug": "best-time-to-visit-sikkim-and-darjeeling",
        "title": "When to visit Sikkim and Darjeeling",
        "image": "darjeeling-tiger-hill",
        "excerpt": "Clear mountain views, blooming rhododendrons or snowy passes? Here is our season-by-season guide to the eastern Himalayas.",
        "lead": "Clear mountain views, blooming rhododendrons or snowy passes? Each season in the eastern Himalayas has its own charm. Here is our guide to choosing the best time for your trip.",
        "sections": [
            ("Spring (March to May)", [
                "Spring is one of the most popular seasons. The days are mild, the tea gardens are bright green and the rhododendrons are in full bloom - especially in the Yumthang Valley in North Sikkim.",
            ], ["lachung-yumthang", "darjeeling-tea", "gangtok-mg-marg"]),
            ("Monsoon (June to September)", [
                "Heavy rain brings lush landscapes and waterfalls, but also landslides that can close mountain roads. It is a quieter time to visit Darjeeling and Gangtok, with flexible plans.",
            ], []),
            ("Autumn (October to November)", [
                "After the monsoon the air is crystal clear: this is the best season for views of Kangchenjunga from Tiger Hill and for trekking. Book early, as it is also festival season.",
            ], ["darjeeling-kanchenjunga", "gangtok-hanuman-tok", "darjeeling-batasia"]),
            ("Winter (December to February)", [
                "Cold, sunny days and snow on the high passes. Tsomgo Lake may freeze and some roads in North Sikkim can close after heavy snowfall, but Darjeeling and Gangtok are calm and beautiful.",
            ], []),
        ],
    },
    {
        "slug": "travelling-to-lachen-and-lachung",
        "title": "Travelling to Lachen and Lachung",
        "image": "lachen-gurudongmar",
        "excerpt": "Permits, altitude and the best route: everything you need to know before setting off for North Sikkim.",
        "lead": "North Sikkim is one of the most spectacular regions of the Himalayas - and one of the most protected. Here is what you need to know before you go.",
        "sections": [
            ("Permits", [
                "North Sikkim is a restricted area. Indian nationals and foreign visitors need permits, which are issued through registered tour operators such as LAVIGO. Some sites, including Gurudongmar Lake and Zero Point, may be open to Indian nationals only - rules change, so we always check the latest regulations for you.",
            ], ["lachung-village", "lachen-monastery", "lachen-teesta"]),
            ("Altitude", [
                "Gurudongmar Lake lies at about 5,430 metres. Spend a night in Lachen (about 2,750 m) or Lachung (about 2,900 m) first, drink plenty of water and avoid rushing. Our itineraries are designed to help you acclimatise.",
            ], []),
            ("A classic itinerary", [
                "Day 1: Gangtok to Lachen. Day 2: Gurudongmar Lake at sunrise, then on to Lachung. Day 3: Yumthang Valley and Zero Point, then back to Gangtok.",
            ], ["lachen-gurudongmar", "lachung-yumthang", "lachung-zero-point"]),
        ],
    },
    {
        "slug": "a-first-trip-to-nepal",
        "title": "A first trip to Nepal",
        "image": "nepal-phewa-lake",
        "excerpt": "Kathmandu, Pokhara, Chitwan or the Everest region? How to plan your first journey to Nepal.",
        "lead": "Temples and stupas, lakes and jungles, and of course the highest mountains on Earth: Nepal has so much to offer that a first trip can be hard to plan. Here is our suggested route.",
        "sections": [
            ("Kathmandu Valley", [
                "Start with two or three days in the valley to discover Boudhanath, Swayambhunath and the royal squares of Kathmandu and Bhaktapur.",
            ], ["nepal-boudhanath", "nepal-swayambhunath", "nepal-bhaktapur"]),
            ("Pokhara and the mountains", [
                "Continue to Pokhara for lakeside walks, sunrise over the Annapurnas and, if you like, a short trek in the foothills.",
            ], ["nepal-phewa-lake", "nepal-pokhara", "nepal-everest"]),
            ("Into the jungle", [
                "End your journey in Chitwan National Park to look for rhinos and birds before flying home from Kathmandu.",
            ], []),
        ],
    },
]

CONTACT_PAGE = {
    "line1": COMPANY,
    "line2": "travel desk",
    "text": "Tell us about your travel plans and we will design a journey that suits you - dates, budget, pace and interests. We usually reply within one working day.",
    "image": "gangtok-city",
    "hours_title": ("Our", "opening hours"),
    "hours_text": "The LAVIGO team is here to help you plan your trip.",
    "hours_image": "darjeeling-tea",
    "consent": "I agree to receive LAVIGO travel ideas by email",
    "countries": ["India", "Nepal", "Bangladesh", "Bhutan", "United Kingdom", "United States", "Australia",
                  "Germany", "France", "Other"],
}


# ---------------------------------------------------------------- trips
# Prices and dates below are SAMPLES - replace them with your real ones.
# price_adult: per adult (above 10 years), price_child: per child (3 to 10 years). Children under 3 travel free.
CURRENCY = "₹"  # rupee sign

TRIPS_PAGE = {
    "title": "Our trips",
    "image": "lachung-yumthang",
    "intro": "Small-group journeys with fixed departure dates, local guides and everything organised for you. Pick a trip, check the price for your group and book in one message on WhatsApp.",
    "outro_title": "Want a private trip?",
    "outro_text": [
        "All our trips can also be arranged privately for your family or friends, on the dates of your choice.",
        "Write to us on WhatsApp or through the contact page and we will tailor the itinerary for you.",
    ],
    "outro_image": "darjeeling-tea",
}

TRIPS = [
    {
        "slug": "gangtok-and-north-sikkim",
        "name": "Gangtok & North Sikkim",
        "tagline": "Monasteries, high lakes and the valleys of Lachen and Lachung",
        "days": 6,
        "nights": 5,
        "start": "Bagdogra / NJP",
        "end": "Bagdogra / NJP",
        "dates": ["2026-11-14", "2026-12-05", "2027-03-20", "2027-04-10", "2027-05-01"],
        "price_adult": 24999,
        "price_child": 17999,
        "hero": "lachen-gurudongmar",
        "card_image": "lachung-yumthang",
        "overview": [
            "From the lively streets of Gangtok to the sacred waters of Gurudongmar Lake at over 5,000 metres, this journey takes you to the heart of Sikkim. You will cross rhododendron forests, visit Buddhist monasteries and spend two nights in the mountain villages of Lachen and Lachung.",
            "Permits, vehicles, drivers and stays are all arranged by LAVIGO, so you can simply enjoy the road.",
        ],
        "highlights": [
            "Sunrise at Gurudongmar Lake, one of the highest lakes in the world",
            "Rhododendrons and hot springs in the Yumthang Valley",
            "The snowfields of Zero Point (Yumesamdong)",
            "Rumtek Monastery and an evening stroll on MG Marg",
            "Tsomgo Lake on the road to Nathu La",
        ],
        "places": [
            {"label": "Day 1-2", "name": "Gangtok", "text": ["Sikkim's friendly capital, with its monasteries, viewpoints over Kangchenjunga and the pedestrian MG Marg."], "images": ["gangtok-view", "gangtok-mg-marg", "gangtok-rumtek"]},
            {"label": "Day 3-4", "name": "Lachen & Gurudongmar", "text": ["A mountain village above the Teesta river, starting point for the drive to Gurudongmar Lake."], "images": ["lachen-gurudongmar", "lachen-thangu", "lachen-monastery"]},
            {"label": "Day 4-5", "name": "Lachung & Yumthang", "text": ["Wooden houses, apple orchards and the flower-filled Yumthang Valley below Zero Point."], "images": ["lachung-yumthang", "lachung-zero-point", "lachung-village"]},
            {"label": "Day 6", "name": "Tsomgo Lake", "text": ["A glacial lake at about 3,750 metres on the high road towards Nathu La (optional, permit required)."], "images": ["gangtok-tsomgo"]},
        ],
        "itinerary": [
            ("Arrival - Gangtok", "Pick-up at Bagdogra airport or NJP station and drive along the Teesta river to Gangtok (about 4-5 hours). Evening free on MG Marg."),
            ("Gangtok sightseeing", "Rumtek Monastery, Enchey Monastery, the Namgyal Institute of Tibetology and the Hanuman Tok viewpoint. Permits for North Sikkim are finalised today."),
            ("Gangtok - Lachen", "Scenic drive north past waterfalls and the town of Mangan to Lachen (about 6 hours). Overnight in a local guesthouse."),
            ("Gurudongmar Lake - Lachung", "Very early start to see Gurudongmar Lake in the morning light, via the Thangu valley. Return to Lachen for lunch and continue to Lachung."),
            ("Yumthang Valley & Zero Point", "Morning in the Yumthang Valley and drive up to Zero Point (optional, extra cost). Afternoon return to Gangtok."),
            ("Departure", "Breakfast and transfer back to Bagdogra or NJP for your onward journey."),
        ],
        "included": [
            "5 nights in hotels and guesthouses (twin sharing)",
            "Daily breakfast, plus dinner in Lachen and Lachung",
            "All transfers and sightseeing in a private vehicle with driver",
            "North Sikkim permits",
            "Services of a LAVIGO trip coordinator",
        ],
        "not_included": [
            "Flights or train tickets to Bagdogra / NJP",
            "Zero Point and Nathu La excursions (optional)",
            "Lunches and drinks",
            "Travel insurance",
            "Tips and personal expenses",
        ],
    },
    {
        "slug": "darjeeling-and-gangtok",
        "name": "Darjeeling & Gangtok",
        "tagline": "Tea gardens, the toy train and sunrise over Kangchenjunga",
        "days": 5,
        "nights": 4,
        "start": "Bagdogra / NJP",
        "end": "Bagdogra / NJP",
        "dates": ["2026-11-21", "2026-12-19", "2027-02-13", "2027-03-27", "2027-04-17"],
        "price_adult": 19999,
        "price_child": 13999,
        "hero": "darjeeling-kanchenjunga",
        "card_image": "darjeeling-toy-train",
        "overview": [
            "Two of the most beloved hill stations of the eastern Himalayas in a single trip. Watch the sun rise over Kangchenjunga from Tiger Hill, ride the UNESCO-listed toy train and taste Darjeeling tea where it is grown, before continuing to Gangtok and its monasteries.",
        ],
        "highlights": [
            "Sunrise over Kangchenjunga from Tiger Hill",
            "A joy ride on the Darjeeling Himalayan Railway",
            "Tea tasting at the Happy Valley Tea Estate",
            "Batasia Loop and the Japanese Peace Pagoda",
            "Rumtek Monastery and MG Marg in Gangtok",
        ],
        "places": [
            {"label": "Day 1-3", "name": "Darjeeling", "text": ["The Queen of the Hills, with its tea gardens, colonial heritage and views of the third-highest mountain on Earth."], "images": ["darjeeling-tiger-hill", "darjeeling-toy-train", "darjeeling-tea"]},
            {"label": "Day 3-5", "name": "Gangtok", "text": ["Sikkim's capital, clean and welcoming, surrounded by monasteries and viewpoints."], "images": ["gangtok-view", "gangtok-rumtek", "gangtok-hanuman-tok"]},
        ],
        "itinerary": [
            ("Arrival - Darjeeling", "Pick-up at Bagdogra or NJP and drive up through the tea gardens to Darjeeling (about 3 hours). Evening on the Mall and Chowrasta."),
            ("Tiger Hill & Darjeeling", "Early drive to Tiger Hill for sunrise, then Batasia Loop and Ghoom Monastery. Afternoon toy train joy ride and visit to a tea estate."),
            ("Darjeeling - Gangtok", "Morning at the Peace Pagoda, then a scenic drive to Gangtok along the Teesta river (about 4 hours)."),
            ("Gangtok sightseeing", "Rumtek and Enchey monasteries, the Namgyal Institute of Tibetology and the Hanuman Tok viewpoint. Evening on MG Marg."),
            ("Departure", "Breakfast and transfer to Bagdogra or NJP."),
        ],
        "included": [
            "4 nights in hotels (twin sharing) with daily breakfast",
            "All transfers and sightseeing in a private vehicle with driver",
            "Toy train joy ride tickets",
            "Services of a LAVIGO trip coordinator",
        ],
        "not_included": [
            "Flights or train tickets to Bagdogra / NJP",
            "Lunches, dinners and drinks",
            "Entry fees to monuments and the zoo",
            "Travel insurance",
            "Tips and personal expenses",
        ],
    },
    {
        "slug": "nepal-highlights",
        "name": "Nepal Highlights",
        "tagline": "Kathmandu, Bhaktapur, Pokhara and Chitwan",
        "days": 7,
        "nights": 6,
        "start": "Kathmandu",
        "end": "Kathmandu",
        "dates": ["2026-11-07", "2026-12-12", "2027-02-20", "2027-03-13", "2027-10-09"],
        "price_adult": 39999,
        "price_child": 27999,
        "hero": "nepal-phewa-lake",
        "card_image": "nepal-boudhanath",
        "overview": [
            "The perfect first trip to Nepal: the temples and stupas of the Kathmandu Valley, the lakes and mountain views of Pokhara and the wildlife of Chitwan National Park, in one week.",
        ],
        "highlights": [
            "The great stupa of Boudhanath at dusk",
            "Bhaktapur's royal squares and pagoda temples",
            "Sunrise over the Annapurnas from Sarangkot",
            "A boat ride on Phewa Lake",
            "Jungle safari in Chitwan National Park",
        ],
        "places": [
            {"label": "Day 1-2", "name": "Kathmandu Valley", "text": ["UNESCO-listed temples, stupas and palace squares in Kathmandu and Bhaktapur."], "images": ["nepal-boudhanath", "nepal-swayambhunath", "nepal-bhaktapur"]},
            {"label": "Day 3-4", "name": "Pokhara", "text": ["Lakeside town at the foot of the Annapurna range."], "images": ["nepal-phewa-lake", "nepal-pokhara"]},
            {"label": "Day 5-6", "name": "Chitwan", "text": ["Forests and grasslands home to rhinos, elephants and hundreds of bird species."], "images": ["nepal-chitwan"]},
        ],
        "itinerary": [
            ("Arrival in Kathmandu", "Welcome at the airport and transfer to your hotel. Evening walk around Thamel."),
            ("Kathmandu & Bhaktapur", "Swayambhunath, Kathmandu Durbar Square and Boudhanath, then the medieval city of Bhaktapur."),
            ("Kathmandu - Pokhara", "Drive or fly to Pokhara. Afternoon boat ride on Phewa Lake to the Tal Barahi temple."),
            ("Pokhara", "Sunrise over the Annapurnas from Sarangkot. Free afternoon - paragliding is optional."),
            ("Pokhara - Chitwan", "Drive to Chitwan National Park. Evening Tharu cultural programme."),
            ("Chitwan National Park", "Jeep safari, canoe ride and jungle walk with a naturalist guide."),
            ("Chitwan - Kathmandu, departure", "Return to Kathmandu for your onward flight."),
        ],
        "included": [
            "6 nights in hotels (twin sharing) with daily breakfast",
            "All meals in Chitwan",
            "Private vehicle with driver for all transfers",
            "English-speaking guide in Kathmandu and naturalist in Chitwan",
            "Park and monument entry fees",
        ],
        "not_included": [
            "International flights and Nepal visa",
            "Pokhara flight (if chosen instead of the drive)",
            "Lunches and dinners outside Chitwan",
            "Paragliding and optional activities",
            "Travel insurance, tips and personal expenses",
        ],
    },
    {
        "slug": "manali-adventure",
        "name": "Manali Adventure",
        "tagline": "Cedar forests, snow points and the Atal Tunnel",
        "days": 5,
        "nights": 4,
        "start": "Manali",
        "end": "Manali",
        "dates": ["2026-12-26", "2027-01-16", "2027-04-24", "2027-05-15", "2027-06-05"],
        "price_adult": 17999,
        "price_child": 12499,
        "hero": "manali-solang",
        "card_image": "manali-town",
        "overview": [
            "Discover Manali and the upper Kullu Valley: ancient wooden temples, the snowfields of Solang Valley, the Atal Tunnel to Lahaul and, when the road is open, the high Rohtang Pass.",
        ],
        "highlights": [
            "The Hidimba Devi Temple in its cedar forest",
            "Snow activities and paragliding in Solang Valley",
            "Through the Atal Tunnel to Sissu in Lahaul",
            "Rohtang Pass (subject to season and permits)",
            "Hot springs of Vashisht and rafting on the Beas",
        ],
        "places": [
            {"label": "Day 1-2", "name": "Manali", "text": ["Temples, cafés and orchards at the head of the Kullu Valley."], "images": ["manali-town", "manali-hidimba", "manali-vashisht"]},
            {"label": "Day 3", "name": "Solang Valley", "text": ["Paragliding, ropeway and snow play."], "images": ["manali-solang"]},
            {"label": "Day 4", "name": "Atal Tunnel & Rohtang", "text": ["The road to Lahaul through the 9 km Atal Tunnel, and the high Rohtang Pass in season."], "images": ["manali-atal-tunnel", "manali-rohtang"]},
        ],
        "itinerary": [
            ("Arrival in Manali", "Check in and evening stroll on the Mall Road."),
            ("Manali sightseeing", "Hidimba Devi Temple, Old Manali, Vashisht hot springs and the Tibetan monastery."),
            ("Solang Valley", "A full day of snow activities, ropeway and optional paragliding."),
            ("Atal Tunnel & Sissu / Rohtang", "Drive through the Atal Tunnel to Sissu in Lahaul, or to Rohtang Pass when open (permit required)."),
            ("Departure", "Optional rafting on the Beas before your departure."),
        ],
        "included": [
            "4 nights in a hotel (twin sharing) with breakfast and dinner",
            "Private vehicle with driver for sightseeing",
            "Rohtang permit (when the pass is open)",
            "Services of a LAVIGO trip coordinator",
        ],
        "not_included": [
            "Travel to and from Manali",
            "Adventure activities (paragliding, rafting, ropeway)",
            "Snow clothing rental",
            "Travel insurance",
            "Tips and personal expenses",
        ],
    },
]

# ---------------------------------------------------------------- about us
ABOUT = {
    "title": ("About", "LAVIGO"),
    "hero": "hero-kangchenjunga",
    "card_text": "A travel company dedicated to the Himalayas.",
    "intro": [
        "LAVIGO is a travel company dedicated to the Himalayas. We design journeys to Nepal, Sikkim, Darjeeling and Himachal Pradesh for travellers who want to discover the mountains in comfort, safely and at their own pace.",
        "From the first message to the day you return home, one team takes care of everything: itineraries, stays, transport, permits and local guides.",
    ],
    "blocks": [
        {"label": "Our story", "name": "Born in the mountains", "text": ["[Tell the story of LAVIGO here: who founded it, when and why.] We started LAVIGO because we love the Himalayas and want to share them the way we know them - with time to look, to meet people and to feel at home."], "images": ["darjeeling-tea", "lachung-village"]},
        {"label": "Why travel with us", "name": "Local and personal", "text": ["We work with local drivers, guides and family-run guesthouses we know personally. Our trips are small, flexible and built around you.", "Need a change of plan? We are one WhatsApp message away, before and during your trip."], "images": ["gangtok-mg-marg", "nepal-bhaktapur"]},
        {"label": "Peace of mind", "name": "Permits & safety", "text": ["The Himalayas have protected areas, high passes and fast-changing weather. We handle permits, plan time to acclimatise and always check road conditions, so you can travel with confidence."], "images": ["lachen-thangu", "gangtok-nathu-la"]},
        {"label": "Responsible travel", "name": "Respect for the mountains", "text": ["We favour local businesses, keep our groups small and ask our travellers to respect sacred sites, wildlife and the fragile mountain environment."], "images": ["nepal-chitwan", "lachen-teesta"]},
    ],
}


# ---------------------------------------------------------------- home page: call to action above the footer
HOME_CTA = {
    "small": "What are you waiting for?",
    "title": "Book your Himalayan journey",
    "text": "Check our trip plans with dates, day-by-day itinerary and prices, calculate the cost for your group and book in one message on WhatsApp.",
    "button_trips": "Check trip plans",
    "button_book": "Book on WhatsApp",
    "button_custom": "Plan a custom trip",
    # trips shown as cards in this section (slugs from TRIPS)
    "trips": ["gangtok-and-north-sikkim", "darjeeling-and-gangtok", "bhutan-happiness-tour", "everest-base-camp-trek"],
}


# ---------------------------------------------------------------- more trips (SAMPLE prices and dates - replace them)
TRIPS += [
    {
        "slug": "pelling-and-west-sikkim",
        "name": "Pelling & West Sikkim",
        "tagline": "Kangchenjunga views, ancient monasteries and a sacred lake",
        "days": 4,
        "nights": 3,
        "start": "Bagdogra / NJP",
        "end": "Bagdogra / NJP",
        "dates": ["2026-11-28", "2026-12-26", "2027-03-06", "2027-04-03", "2027-05-08"],
        "price_adult": 15999,
        "price_child": 10999,
        "hero": "pelling-kanchenjunga",
        "card_image": "pelling-pemayangtse",
        "overview": [
            "Pelling sits on a ridge in West Sikkim facing the full sweep of the Kangchenjunga range. This short trip combines its famous sunrise views with the monasteries, ruins and sacred lake that make the region so special.",
        ],
        "highlights": [
            "Sunrise over Kangchenjunga from Pelling",
            "Pemayangtse Monastery, one of the oldest in Sikkim",
            "The ruins of Rabdentse, Sikkim's second royal capital",
            "The sacred Khecheopalri Lake in the forest",
            "The glass Skywalk and the giant Chenrezig statue",
        ],
        "places": [
            {"label": "Day 1-4", "name": "Pelling", "text": ["A small hill town at about 2,150 metres with some of the best mountain views in Sikkim."], "images": ["pelling-kanchenjunga", "pelling-skywalk"]},
            {"label": "Day 2", "name": "Pemayangtse & Rabdentse", "text": ["A 17th-century monastery and the forested ruins of the former royal capital, a short walk apart."], "images": ["pelling-pemayangtse", "pelling-rabdentse"]},
            {"label": "Day 3", "name": "Khecheopalri Lake", "text": ["A wish-fulfilling lake sacred to Buddhists and Hindus, hidden in the forest above Pelling."], "images": ["pelling-khecheopalri"]},
        ],
        "itinerary": [
            ("Arrival - Pelling", "Pick-up at Bagdogra or NJP and drive to Pelling through tea gardens and the Teesta valley (about 6 hours)."),
            ("Pelling sightseeing", "Sunrise over Kangchenjunga, then Pemayangtse Monastery, Rabdentse ruins and the Skywalk with the Chenrezig statue."),
            ("Khecheopalri Lake & waterfalls", "Morning at Khecheopalri Lake, then Kanchenjunga Falls and Rimbi waterfall. Evening free."),
            ("Departure", "Breakfast and transfer back to Bagdogra or NJP."),
        ],
        "included": [
            "3 nights in a hotel with mountain views (twin sharing)",
            "Daily breakfast and dinner",
            "All transfers and sightseeing in a private vehicle with driver",
            "Services of a LAVIGO trip coordinator",
        ],
        "not_included": [
            "Flights or train tickets to Bagdogra / NJP",
            "Lunches and drinks",
            "Entry fees (Skywalk, monasteries)",
            "Travel insurance",
            "Tips and personal expenses",
        ],
    },
    {
        "slug": "bhutan-happiness-tour",
        "name": "Bhutan Happiness Tour",
        "tagline": "Thimphu, Punakha and the Tiger's Nest",
        "days": 6,
        "nights": 5,
        "start": "Paro",
        "end": "Paro",
        "dates": ["2026-11-15", "2027-03-14", "2027-04-11", "2027-10-10", "2027-11-07"],
        "price_adult": 54999,
        "price_child": 38999,
        "hero": "bhutan-taktsang",
        "card_image": "bhutan-punakha",
        "overview": [
            "The Land of the Thunder Dragon is like nowhere else: fortress-monasteries above green valleys, prayer flags on every pass and a culture that measures success in happiness. This tour covers the highlights of western Bhutan, ending with the hike to the famous Tiger's Nest.",
            "Bhutan charges a Sustainable Development Fee (SDF) per night and requires a permit for every visitor. LAVIGO arranges the permits and tells you the current fee before you book.",
        ],
        "highlights": [
            "The hike to Paro Taktsang, the Tiger's Nest monastery",
            "Punakha Dzong at the meeting of two rivers",
            "The 108 chortens of Dochula Pass",
            "The giant Buddha Dordenma above Thimphu",
            "Local guide and Bhutanese hospitality throughout",
        ],
        "places": [
            {"label": "Day 1-2", "name": "Thimphu", "text": ["Bhutan's capital - a city without traffic lights, with markets, museums and the Buddha Dordenma statue."], "images": ["bhutan-dordenma"]},
            {"label": "Day 3", "name": "Dochula & Punakha", "text": ["Over the Dochula pass and its 108 chortens down to the magnificent Punakha Dzong."], "images": ["bhutan-punakha", "bhutan-dochula"]},
            {"label": "Day 5", "name": "Paro & the Tiger's Nest", "text": ["A monastery clinging to a cliff 900 metres above the Paro valley - the icon of Bhutan."], "images": ["bhutan-taktsang"]},
        ],
        "itinerary": [
            ("Arrival in Paro - Thimphu", "Welcome at Paro airport by your Bhutanese guide and drive to Thimphu (about 1.5 hours)."),
            ("Thimphu", "Buddha Dordenma, the Memorial Chorten, the Folk Heritage Museum and Tashichho Dzong at sunset."),
            ("Thimphu - Punakha", "Drive over Dochula Pass (3,100 m) with its 108 chortens to Punakha. Visit Punakha Dzong and the suspension bridge."),
            ("Punakha - Paro", "Morning walk to Chimi Lhakhang, then drive back to Paro. Visit Rinpung Dzong and Paro town."),
            ("Tiger's Nest hike", "Hike to Paro Taktsang (about 5 hours return). Evening farewell dinner with a hot-stone bath (optional)."),
            ("Departure", "Transfer to Paro airport for your onward flight."),
        ],
        "included": [
            "5 nights in government-approved hotels (twin sharing)",
            "All meals during the tour",
            "Licensed English-speaking Bhutanese guide",
            "Private vehicle with driver",
            "Entry permits and monument fees",
        ],
        "not_included": [
            "Flights to and from Paro",
            "Sustainable Development Fee (SDF), charged per night by the Government of Bhutan",
            "Drinks and the optional hot-stone bath",
            "Travel insurance",
            "Tips and personal expenses",
        ],
    },
    {
        "slug": "everest-base-camp-trek",
        "name": "Everest Base Camp Trek",
        "tagline": "Sherpa villages, monasteries and the foot of the world's highest mountain",
        "days": 14,
        "nights": 13,
        "start": "Kathmandu",
        "end": "Kathmandu",
        "dates": ["2027-03-27", "2027-04-10", "2027-04-24", "2027-10-02", "2027-10-16"],
        "price_adult": 129999,
        "price_child": None,  # adults only
        "min_age": 12,
        "hero": "ebc-kala-patthar",
        "card_image": "ebc-namche",
        "overview": [
            "The classic Himalayan trek: fly to Lukla, follow the Dudh Koshi valley through Sherpa villages and monasteries, and walk to Everest Base Camp at about 5,360 metres. The next morning, climb Kala Patthar for the closest view of Mount Everest you can get without climbing it.",
            "This trek is for fit walkers (minimum age 12). Acclimatisation days are built in, and you walk with an experienced guide and porters.",
        ],
        "highlights": [
            "The flight into Lukla, one of the most spectacular in the world",
            "Namche Bazaar, the Sherpa capital",
            "Tengboche Monastery with Ama Dablam behind it",
            "Everest Base Camp at about 5,360 metres",
            "Sunrise over Everest from Kala Patthar (about 5,550 m)",
        ],
        "places": [
            {"label": "Day 2-4", "name": "Lukla & Namche Bazaar", "text": ["The gateway to the Khumbu and the lively market town of the Sherpa people."], "images": ["ebc-namche", "nepal-everest"]},
            {"label": "Day 5", "name": "Tengboche", "text": ["The most important monastery of the Khumbu, facing Everest and Ama Dablam."], "images": ["ebc-tengboche"]},
            {"label": "Day 9-10", "name": "Base Camp & Kala Patthar", "text": ["The Khumbu glacier, Everest Base Camp and the viewpoint of Kala Patthar."], "images": ["ebc-base-camp", "ebc-kala-patthar"]},
        ],
        "itinerary": [
            ("Arrival in Kathmandu", "Welcome, trek briefing and gear check."),
            ("Fly to Lukla - Phakding", "Early flight to Lukla (2,860 m) and an easy walk to Phakding."),
            ("Phakding - Namche Bazaar", "Cross the suspension bridges of the Dudh Koshi and climb to Namche (3,440 m)."),
            ("Acclimatisation in Namche", "Short hike to the Everest View Hotel and back."),
            ("Namche - Tengboche", "Walk to Tengboche (3,860 m) and visit the monastery."),
            ("Tengboche - Dingboche", "Through rhododendron forests to Dingboche (4,410 m)."),
            ("Acclimatisation in Dingboche", "Hike up Nangkartshang hill for views of Makalu and Lhotse."),
            ("Dingboche - Lobuche", "Past the climbers' memorials to Lobuche (4,940 m)."),
            ("Everest Base Camp", "Walk to Gorak Shep, then on to Everest Base Camp and back."),
            ("Kala Patthar - Pheriche", "Sunrise climb of Kala Patthar, then descend to Pheriche."),
            ("Pheriche - Namche", "Long descent back to Namche Bazaar."),
            ("Namche - Lukla", "Last day of walking, celebration evening in Lukla."),
            ("Fly to Kathmandu", "Morning flight back to Kathmandu. Afternoon free."),
            ("Departure", "Transfer to the airport."),
        ],
        "included": [
            "Hotel in Kathmandu and teahouse lodges on the trek",
            "All meals during the trek",
            "Kathmandu - Lukla - Kathmandu flights",
            "Experienced trekking guide and porters (1 porter for 2 trekkers)",
            "Sagarmatha National Park and local area permits",
        ],
        "not_included": [
            "International flights and Nepal visa",
            "Meals in Kathmandu",
            "Travel insurance with helicopter rescue (required)",
            "Hot showers, charging and Wi-Fi in lodges",
            "Tips for guide and porters",
        ],
    },
]

# ---------------------------------------------------------------- custom trip request (on the Trips page)
CUSTOM_TRIP = {
    "small": "Your journey, your way",
    "title": "Plan a custom trip",
    "text": "Tell us where you would like to go, when and with whom. We will send you a personalised itinerary and price on WhatsApp.",
    "places": ["Nepal", "Gangtok", "Darjeeling", "Manali", "Lachen & Lachung", "Pelling", "Bhutan", "Everest Base Camp"],
    "budgets": ["Not sure yet", "Under ₹15,000 per person", "₹15,000 - ₹30,000 per person",
                "₹30,000 - ₹60,000 per person", "Above ₹60,000 per person"],
    "button": "Send my request on WhatsApp",
}

# ---------------------------------------------------------------- reviews
# Replace these placeholders with REAL reviews from your travellers (with their permission).
# "photo" is optional: put a photo in lavigo-content/images/ and write its name (without .jpg), or leave "".
# "trip" (optional) shows the review on that trip's page too.
REVIEWS = {
    "small": "Our travellers",
    "title": "What they say",
    "google_text": "See all our reviews on Google",
    "items": [
        {"name": "[Customer name]", "place": "[City]", "trip": "gangtok-and-north-sikkim", "rating": 5, "photo": "",
         "text": "[Paste a real review from one of your travellers here - what they loved about the trip, the guide, the hotels...]"},
        {"name": "[Customer name]", "place": "[City]", "trip": "darjeeling-and-gangtok", "rating": 5, "photo": "",
         "text": "[Paste a real review from one of your travellers here.]"},
        {"name": "[Customer name]", "place": "[City]", "trip": "nepal-highlights", "rating": 5, "photo": "",
         "text": "[Paste a real review from one of your travellers here.]"},
    ],
}

# ---------------------------------------------------------------- Google / search engines
SITE = {
    # Your website address once it is online (no slash at the end). Used for the sitemap and Google.
    "url": "https://www.your-domain.com",
    # From Google Search Console > Add property > HTML tag: paste only the content="..." value here.
    "google_site_verification": "",
    # Link to your Google reviews (Google Business Profile > Ask for reviews / Share profile).
    "google_reviews": "#",
}
