# LAVIGO website

The finished website is in **`site/`**. Open `site/index.html`, or serve it:

```
python -m http.server 8000 --directory site
```

## Change content

Everything is generated from **`lavigo-content/`**. Edit there, then rebuild:

```
python build_lavigo.py
```

| What | Where |
|---|---|
| All texts (destinations, places, blog posts, headings) | `lavigo-content/content.py` |
| Phone, email, address, opening hours, legal details (placeholders in `[brackets]`) | `CONTACT` at the top of `content.py` |
| Photos | `lavigo-content/images/<name>.jpg` |
| Photo credits | `lavigo-content/images/credits.json` |
| Logo, favicon | `lavigo-content/brand/` |
| Travel map and India mini-map | `lavigo-content/map/` |

### Trips and WhatsApp bookings
- Trips live in `TRIPS` in `content.py`: name, dates, days/nights, prices, overview, highlights,
  places, day-by-day itinerary, included / not included. Add a trip by copying one block.
- `price_adult` is per adult (above 10 years), `price_child` per child (3-10 years); under 3 is free.
  **The prices and dates there now are samples - replace them.**
- Set your WhatsApp number in `CONTACT["whatsapp"]` (country code + number, digits only, e.g. `919876543210`).
  The "Book on WhatsApp" button sends the trip, date, travellers and estimated total in a pre-filled message;
  the green bubble on every page opens a chat.
- The About us page text is in `ABOUT` (replace the `[bracketed]` story).
- Layout of the new sections: `lavigo-content/extras/lavigo.css`; calculator: `lavigo-content/extras/lavigo-trip.js`.

### Reviews
`REVIEWS` in `content.py` holds **placeholders**. Replace them with real reviews from your travellers
(ask their permission). Add `"photo": "file-name"` for a customer photo, or leave it empty to show initials.
`"trip"` also shows the review on that trip's page.

### Custom trip requests
The "Plan a custom trip" form is on the Trips page (`CUSTOM_TRIP` in `content.py`). It sends the answers to your WhatsApp.

### Google (do this once the site is online)
1. In `content.py` set `SITE["url"]` to your real address (e.g. `https://www.lavigo.in`) and rebuild.
   This fills `site/sitemap.xml`, `site/robots.txt`, and the page addresses Google reads.
2. **Google Search Console** (search.google.com/search-console): Add property > URL prefix > your address >
   choose "HTML tag", copy only the `content="..."` value into `SITE["google_site_verification"]`, rebuild, upload,
   then click Verify. Then open Sitemaps and submit `sitemap.xml`.
3. **Google Business Profile** (business.google.com): create the profile as a "Travel agency" with your
   address/phone, verify it (postcard, phone or video), add photos and your website link.
   Then use "Ask for reviews" and paste that link into `SITE["google_reviews"]` - a
   "See all our reviews on Google" button appears under the reviews.

### Replacing photos
Save your photo over an existing file using the same name (for example `nepal-everest.jpg`), then rebuild.
To add a new photo, put it in `lavigo-content/images/`, use its name (without `.jpg`) in `content.py`,
and add an entry to `credits.json`. Wide photos about 1920 px across work best.

The current photos come from Wikimedia Commons under free licences. If you keep any of them,
keep their credits: the site shows them on each photo (©) and on the Legal notice page.

## Other folders
- `original-scrape/` - the downloaded original site (English pages + assets), used as the design template
- `build_site.py`, `translations/` - turn the scrape into clean English pages (run automatically by `build_lavigo.py`)
- `logo/` - your original logo file
