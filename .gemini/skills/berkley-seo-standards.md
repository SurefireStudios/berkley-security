# Berkley Security - SEO & AI-Citation Standards

This skill defines the mandatory SEO, schema, and content patterns for all pages on berkleysecurity.com. Follow these standards when creating or modifying any page.

---

## Business Information (Always Use These Exact Values)

- **Company:** Berkley Security Inc.
- **Founded:** 1978
- **Licensed in:** MS & LA
- **Toll Free:** 1-800-778-3173
- **Email:** staff@berkleysecurity.com
- **Pay Online:** http://www.invoicecloud.com/vicksburgms
- **Facebook:** https://www.facebook.com/Burglaralarmandvideocameras/
- **Logo URL:** https://berkleysecurity.com/src/img/Berkley-Security-Logo.png
- **Hours:** Mon-Fri 8am-5pm | 24/7 Emergency Availability

### Office Locations (for LocalBusiness schema & footer)
1. **Vicksburg (Main Office):** 3512B Manor Dr., Vicksburg, MS 39180 | (601) 636-6955
2. **Natchez:** 415 Main St., Natchez, MS 39120 | (601) 442-2293
3. **Vidalia:** 506 Carter St. Suite C, Vidalia, LA 71373 | (318) 336-6196

### Services (for internal linking)
- Security Alarms: `security-systems.html`
- Video Surveillance: `video-surveillance.html`
- Fire Systems: `fire-alarms.html`
- Medical Alerts: `medical-alerts.html`
- Home Automation: `home-automation.html`
- Home Theater: `home-theater.html`

---

## Head Section Standards

### 1. Title Tags
- **Format:** `[Keyword-Rich Page Title] | Berkley Security`
- **Length:** 50-60 characters
- **Include:** Primary keyword near the beginning
- **Example:** `4K vs 1080p Security Cameras: Which Do You Need? | Berkley Security`

### 2. Meta Description
- **Length:** 140-160 characters
- **Include:** Primary keyword, geographic target, CTA or value proposition
- **Example:** `Compare 4K and 1080p security cameras side by side. Storage costs, bandwidth, and when the upgrade is worth it. Free assessment in Mississippi.`

### 3. Canonical URL
- **Always set** to the full production URL of the page
- **Format:** `<link rel="canonical" href="https://berkleysecurity.com/[path]">`
- **Blog example:** `https://berkleysecurity.com/blog/blog-[slug].html`
- **Main page example:** `https://berkleysecurity.com/[page].html`

### 4. Open Graph & Twitter Cards
```html
<meta property="og:title" content="[Keyword title, can differ from page title]">
<meta property="og:description" content="[Shorter, compelling description]">
<meta property="og:type" content="article"> <!-- or "website" for main pages -->
<meta property="og:url" content="https://berkleysecurity.com/[path]">
<meta property="og:image" content="https://berkleysecurity.com/src/img/Berkley-Security-Logo.png">
<meta property="og:site_name" content="Berkley Security Inc.">
```

### 5. Geo-Targeting Meta Tags (Main Pages Only)
```html
<meta name="geo.region" content="US-MS">
<meta name="geo.placename" content="Vicksburg, Mississippi">
<meta name="ICBM" content="32.3526, -90.8779">
```

---

## JSON-LD Schema Standards

### Article Schema (All Blog Posts)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[Full article title]",
  "description": "[2-3 sentence summary]",
  "author": {
    "@type": "Organization",
    "name": "Berkley Security Inc.",
    "url": "https://berkleysecurity.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Berkley Security Inc.",
    "logo": {
      "@type": "ImageObject",
      "url": "https://berkleysecurity.com/src/img/Berkley-Security-Logo.png"
    }
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntityOfPage": "https://berkleysecurity.com/blog/[slug].html"
}
```

### FAQPage Schema (All Blog Posts + Service Pages)
- **Minimum 5 questions** per page
- Questions should target "People Also Ask" and voice search queries
- Answers should be direct, factual, and cite specific numbers when possible
- Include service-specific and location-specific questions
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Natural language question]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Direct, comprehensive answer with specific data points]"
      }
    }
  ]
}
```

### LocalBusiness Schema (All Main Pages)
- Include all 3 office locations
- Include areaServed with all service cities
- Include service types offered
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Berkley Security Inc.",
  "url": "https://berkleysecurity.com",
  "telephone": "1-800-778-3173",
  "email": "staff@berkleysecurity.com",
  "foundingDate": "1978",
  "logo": "https://berkleysecurity.com/src/img/Berkley-Security-Logo.png",
  "image": "https://berkleysecurity.com/src/img/Berkley-Security-Logo.png",
  "description": "[Service-specific description]",
  "areaServed": ["Vicksburg", "Jackson", "Natchez", "Brandon", "Madison", "Ridgeland", "Flowood", "Clinton", "Byram", "Canton", "Richland", "Brookhaven", "Hattiesburg", "McComb", "Vidalia", "Rayville"],
  "address": [
    {
      "@type": "PostalAddress",
      "streetAddress": "3512B Manor Dr.",
      "addressLocality": "Vicksburg",
      "addressRegion": "MS",
      "postalCode": "39180"
    }
  ]
}
```

---

## Content Structure Standards

### Blog Post Template
Every blog post must include these sections in order:

1. **Quick Answer Box** - Blue-highlighted box at the top with the direct answer. Should be AI-citation optimized (clear, factual, standalone). Include 1-2 internal links to service pages.

2. **Expanded Content** - 1,500+ words covering the topic thoroughly with:
   - H2 headings for major sections
   - H3 headings for subsections
   - Bullet lists with bold lead-ins
   - Data tables where comparison data exists
   - Specific numbers, costs, and measurements (not vague claims)

3. **Mid-Article CTA** - Centered blue box with service pitch and contact link

4. **FAQ Section** - 5 accordion-style FAQ items using `<details>/<summary>` elements
   - Must match the FAQPage JSON-LD schema exactly
   - Target "People Also Ask" queries
   - Include cost, comparison, and "how does X work" questions

5. **Bottom CTA** - Navy background with phone number button + contact form button

6. **Related Articles** - 3-column grid linking to topically related blog posts

7. **Related Services** - Horizontal pill links to relevant service pages

### Main Page Template
Every main page must include:

1. **SEO Meta Block** - Title, description, keywords, canonical, OG tags, geo tags
2. **LocalBusiness + FAQPage JSON-LD** - Both schemas in the head
3. **FAQ Accordion Section** - Visual FAQ matching schema
4. **Areas We Serve Section** - Full city grid (see below)
5. **CTA Sections** - Multiple throughout the page

---

## Areas We Serve Section (Main Pages)

Use `bg-blue-900` background. Include the full city list in a 2-column grid (Mississippi | Louisiana):

### Mississippi (Linked Cities - have landing pages)
Vicksburg, Jackson, Natchez, Brandon, Madison, Ridgeland, Flowood, Clinton, Byram, Canton, Richland, Brookhaven, Hattiesburg, McComb

### Mississippi (Unlinked - span pills)
Pearl, Yazoo City, Port Gibson, Raymond, Edwards, Bolton, Crystal Springs, Hazlehurst, Mendenhall, Laurel, Petal, Columbia, Woodville, Fayette, Rolling Fork, Greenville, Grenada, Indianola

### Louisiana (Linked Cities)
Vidalia, Rayville

### Louisiana (Unlinked - span pills)
Ferriday, Jonesville, Tallulah, Monroe, West Monroe, Delhi, Winnsboro, Bastrop, Newellton, St. Joseph, Waterproof, Mangham

### City Landing Page Link Format
```html
<a href="city/[city]-[state].html" class="inline-block bg-white/10 hover:bg-accent/80 border border-white/20 rounded-full px-3 py-1 text-sm transition-colors">[City Name]</a>
```

---

## Navigation Standards

### Desktop Nav (all pages)
Home | About | Services | Blog | Contact | Facebook icon | Pay Online button

### Mobile Nav
Same links in slide-out menu with toll-free number at bottom

### Top Contact Bar
Toll free number | Vicksburg number | Natchez number | Vidalia number | Email

---

## Internal Linking Strategy

### Blog Posts Should Link To:
- 1-2 service pages in the Quick Answer box
- City landing pages when mentioning specific cities (e.g., `<a href="../city/canton-ms.html">Canton, MS</a>`)
- 3 related blog posts in the Related Articles section
- 3-4 service pages in the Related Services pills

### Main Pages Should Link To:
- All city landing pages in the Areas We Serve grid
- Related service pages in content
- Blog posts where relevant

---

## Technical Standards

### CSS Framework
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Custom colors: navy (#1a2744), charcoal (#1A2744), accent (#3182ce), accent-light (#63b3ed)
- Font: Inter from Google Fonts

### FAQ Accordion CSS
```css
details summary::-webkit-details-marker { display: none }
details summary { list-style: none }
details[open] summary .faq-chevron { transform: rotate(180deg) }
.faq-chevron { transition: transform .3s ease }
```

### Footer
- Consistent across all pages
- 4-column grid: Company info | Quick Links | Services | Contact
- Includes all 3 office locations with phone numbers
- Copyright with dynamic year via JS
- Links to Privacy Policy and Terms & Conditions

---

## Content Writing Rules

1. **No em dashes (—).** Use commas, periods, or "and" instead.
2. **Use specific numbers.** Not "significant savings" but "$200-$400 annually."
3. **Write for AI citation.** Structure answers so AI can extract clean, factual statements.
4. **Geographic anchoring.** Mention Mississippi, Louisiana, and specific cities naturally.
5. **Date content.** Use "Updated [Month] [Year]" format, not specific dates.
6. **Service cross-selling.** Every page should naturally reference related services.
7. **Authority signals.** Reference "since 1978", "licensed in MS & LA", "background-checked technicians."
