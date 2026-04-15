# Berkley Security Inc. — Website Specification

## Concept & Vision
A modern, conversion-focused static website for a trusted security company established in 1978. The site conveys reliability, local expertise, and professional security solutions for residential and commercial clients across Mississippi and Louisiana. Clean, authoritative design that prioritizes phone calls and consultation requests.

## Design Language

### Aesthetic Direction
Premium service business aesthetic — think enterprise security meets local trusted contractor. Dark, professional base with clean white space and subtle accent colors. Not flashy; dignified and reassuring.

### Color Palette
- Primary (Navy): `#1a2744`
- Secondary (Charcoal): `#2d3748`
- Accent (Blue): `#3182ce`
- Accent Light: `#63b3ed`
- Background Light: `#f7fafc`
- Background White: `#ffffff`
- Text Primary: `#1a202c`
- Text Secondary: `#4a5568`
- Text Muted: `#718096`
- Border: `#e2e8f0`
- Success: `#38a169`

### Typography
- Headings: Inter (700, 600) — clean, professional
- Body: Inter (400, 500) — excellent readability
- Fallback: system-ui, -apple-system, sans-serif

### Spatial System
- Base unit: 4px
- Section padding: 80px-120px vertical (desktop), 48px-64px (mobile)
- Card padding: 24px-32px
- Container max-width: 1280px
- Grid gaps: 24px (cards), 32px (sections)

### Motion Philosophy
- Subtle, purposeful transitions (200-300ms ease)
- Fade-up on scroll for sections (IntersectionObserver)
- Hover states on cards (slight lift + shadow)
- No jarring or flashy animations

### Visual Assets
- Hero: solid color with gradient overlay or abstract pattern
- Icons: Lucide icons via CDN (clean, consistent line icons)
- No stock photos needed — clean geometric patterns

## Layout & Structure

### Contact Bar (Top)
- Dark navy background
- Toll free + all local numbers + email
- Mobile: stacked, Desktop: inline

### Navigation
- White/light background with shadow on scroll
- Logo left, nav links center-right
- Mobile: hamburger menu
- CTA button: "Pay Online" (accent color)

### Page Structure
Each page follows: Hero section → Content sections → CTA → Footer

### Footer
- 3-column layout: About, Quick Links, Contact
- Bottom bar with copyright
- All office addresses + phone numbers

## Features & Interactions

### Navigation
- Sticky header with subtle shadow on scroll
- Mobile hamburger menu with slide-in drawer
- Active page highlighting
- Smooth scroll for anchor links

### Contact Form
- Fields: name, email, phone, service area (dropdown), service type (dropdown), residential/commercial toggle, message textarea, consent checkbox
- Client-side validation with inline error states
- Success state with confirmation message
- Fallback: mailto link if JS disabled

### Service Cards
- Icon + title + brief description
- Hover: subtle lift and shadow increase
- Link to detail page

### Testimonials
- Auto-rotating carousel (no JS: show static first)
- Dots indicator for manual navigation
- Pause on hover

### City Pages
- Unique H1, title, meta per page
- Service area overview
- Core services list
- Why Choose Us section
- Nearby cities grid
- Contact CTA

## Component Inventory

### Button
- Primary: accent blue bg, white text, hover darken
- Secondary: navy bg, white text
- Outline: transparent bg, navy border, hover fill
- States: default, hover, active, disabled

### Card
- White bg, subtle shadow, rounded-lg
- Hover: increased shadow, slight translateY(-2px)
- Padding: 24px

### Form Input
- Full width, border-gray-300
- Focus: ring-2 ring-accent
- Error: border-red-500, error message below

### Badge
- Small pill for labels
- Variants: accent, muted

## Technical Approach

### Stack
- HTML5 semantic markup
- Tailwind CSS via CDN with custom config
- Minimal vanilla JavaScript (ES6+)
- No build step required

### File Structure
```
project/
├── index.html
├── about.html
├── services.html
├── security-systems.html
├── video-surveillance.html
├── fire-alarms.html
├── medical-alerts.html
├── home-automation.html
├── contact.html
├── css/
│   └── styles.css (custom Tailwind additions)
├── js/
│   └── main.js (all interactive components)
└── city/
    ├── clinton-ms.html
    ├── natchez-ms.html
    └── ... (16 city pages)
```

### SEO
- Unique title: "Page Name | Berkley Security Inc."
- Unique meta description per page
- Semantic HTML (h1, h2, nav, main, section, article)
- Schema.org LocalBusiness markup on homepage

### Performance
- Tailwind via CDN (production: build with purge)
- Lazy load below-fold images (if any)
- Minimal JS, no heavy libraries
- Target: <2s load time

## Business Information

### Core Data
- Company: Berkley Security Inc.
- Founded: 1978
- Licensed: Mississippi & Louisiana
- Hours: Mon-Fri 8am-5pm, 24/7 Emergency Availability

### Contact Numbers
- Toll Free: 1-800-778-3173
- Vicksburg: (601) 636-6955
- Natchez: (601) 442-2293
- Vidalia: (318) 336-6196
- Email: staff@berkleysecurity.com

### Office Locations
- Vicksburg, MS (Main Office)
- Natchez, MS
- Vidalia, LA

### Services
1. Security Alarms — intrusion detection, 24/7 monitoring
2. Video Surveillance — cameras, recorders, remote access
3. Fire Alarms — detection, notification, monitoring
4. Medical Alerts — emergency response for seniors
5. Home Automation — smart locks, lights, thermostat, scenes
6. Home Theater (Optional upsell)

## City Pages

16 cities with unique content:
1. Clinton, MS
2. Natchez, MS
3. Jackson, MS
4. Byram, MS
5. Madison, MS
6. Canton, MS
7. Ridgeland, MS
8. Flowood, MS
9. Richland, MS
10. Brandon, MS
11. Hattiesburg, MS
12. Vidalia, LA
13. Rayville, LA
14. Brookhaven, MS
15. McComb, MS

Each page URL: `/security-systems-[city]-[state].html`
