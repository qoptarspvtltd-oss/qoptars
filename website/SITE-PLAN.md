# Qoptars website: plan

## What the source pages tell us

| Source | What it is | How it is used |
|---|---|---|
| Homepage.html, About-Us.html, All_Products.html (new) | Defence-led positioning. Conservative, verifiable claims (founded 2019, 6+ platforms, 10+ institutional relationships, GeM OEM, i-TIC IIT Hyderabad). States plainly that DGCA type certification is not held. | **Source of truth for all copy, specs and claims.** |
| Previous WordPress site (screenshots) | Colourful consumer-style design. Agri drone sales page with price and countdown offer, testimonials, team photos, product pages with FAQs and order forms. | Used for structure ideas only (product detail pages, team section). Content not carried over where it conflicts with the new pages (see below). |

## Not carried over from the old site (needs the owner's confirmation)

- "+75 enterprise & government clients", "+15000 flight hours", "+500 production capacity", "3 countries deployed". The new pages claim "10+ institutional relationships" instead. These numbers contradict each other, so none are shown.
- Prices (agri drone Rs 3,45,000 and "Starting at Rs ... Lakhs" on other products), countdown timer and discount offer. Procurement buyers quote through GeM, so the new site asks for a briefing instead.
- Customer testimonials (not legible in the screenshots, source unknown).
- Product photos that are not Qoptars' own: the Tethered Drone image on the current site is a third-party product photo (Aeryon SkyRanger) and is **not used**. The Kamikaze and Agriculture images look like stock photography; they are used with an "Illustrative image" label until real photos exist.

## Audience

1. Defence, paramilitary and police procurement officers
2. Government and PSU buyers (GeM)
3. Industrial and institutional agriculture programmes
4. International and OEM enquiries

## Information architecture

```
Home
Solutions            (all 7 platforms, filter by category)
  Surveillance & reconnaissance: Vayu, Day Surveillance, Day/Night Surveillance
  Tactical operations:           Kamikaze, Payload Dropping, Tethered
  Agriculture & industrial:      Agriculture Spray 10L
Company              (story, what we do, certifications, team)
Contact              (technical briefing request)
```

One primary action across the whole site: **Request briefing**.

## Home page flow

1. Hero: one claim, one proof line, two actions. Real field photography.
2. Who we serve: four entry points (defence, government/PSU, GeM, international).
3. Who is Qoptars: story and credentials.
4. Why Qoptars: five reasons.
5. AI autonomy: the shared onboard stack (the stated USP).
6. Solutions: filterable platform cards.
7. Institutional relationships: logos only.
8. Closing call to action.

## Design direction

Dark, instrument-panel feel to match the product category and the dark field photography. One accent (signal gold) on near-black. Manrope for text, IBM Plex Mono for specs and figures. Cards 16px radius, buttons pill. Motion is limited to image crossfade, scroll reveal and hover feedback, and is disabled under `prefers-reduced-motion`.

## Build

`python3 build.py` regenerates every page from the data in `build.py`. Output is plain static HTML, CSS and JS with self-hosted fonts and no external requests.

## Open items

- Real product photography for Kamikaze, Tethered and Agriculture.
- Team photos (monogram placeholders for now) and LinkedIn links.
- Connect the contact form to a real endpoint (it opens the visitor's email app for now).
- Detailed specification sheets per platform (only verified headline specs are shown).
- Privacy policy and terms pages.
