---
name: berkley-seo-standards
description: SEO, schema, and content standards for berkleysecurity.com. Use when creating or modifying any page, blog post, or city landing page on the Berkley Security website.
---

# Berkley Security - SEO & AI-Citation Standards

This skill defines the mandatory SEO, schema, and content patterns for all pages on berkleysecurity.com. Follow these standards when creating or modifying any page.

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

## Head Section Standards

### 1. Title Tags
- **Format:** `[Keyword-Rich Page Title] | Berkley Security`
- **Length:** 50-60 characters
- **Include:** Primary keyword near the beginning

### 2. Meta Description
- **Length:** 140-160 characters
- **Include:** Primary keyword, geographic target, CTA or value proposition

### 3. Canonical URL
- **Always set** to the full production URL of the page
- **Format:** `<link rel="canonical" href="https://berkleysecurity.com/[path]">`

### 4. Open Graph & Twitter Cards
```html
<meta property="og:title" content="[Keyword title]">
<meta property="og:description" content="[Shorter, compelling description]">
<meta property="og:type" content="article">
<meta property="og:url" content="https://berkleysecurity.com/[path]">
<meta property="og:image" content="https://berkleysecurity.com/src/img/Berkley-Security-Logo.png">
<meta property="og:site_name" content="Berkley Security Inc.">
```

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
- Minimum 5 questions per page
- Target "People Also Ask" and voice search queries
- Include service-specific and location-specific questions

### LocalBusiness Schema (City Landing Pages)
- Unique per city with correct geo-coordinates
- Include `areaServed` with nearby communities
- Include `hasOfferCatalog` with service types

## Content Structure Standards

### Blog Post Template
1. **Quick Answer Box** - Blue-highlighted box with the direct answer and 1-2 internal links
2. **Expanded Content** - 1,500+ words with H2/H3 headings, bullet lists, data tables
3. **Mid-Article CTA** - Centered blue box with service pitch
4. **FAQ Section** - 5 accordion items using `<details>/<summary>` matching FAQPage JSON-LD
5. **Bottom CTA** - Navy background with phone and contact buttons
6. **Related Articles** - 3-column grid linking to related blog posts
7. **Related Services** - Horizontal pill links to service pages

### City Landing Page Template
1. Unique H1 title (no two city pages share the same title)
2. Locally relevant hero paragraph with specific geographic and industry references
3. 6 service cards linking to service pages
4. 7 unique FAQ questions with FAQPage JSON-LD schema
5. "Areas We Serve" section with 4 nearby city links
6. LocalBusiness JSON-LD with correct coordinates

## Technical Standards

### CSS Framework
- Tailwind CSS via CDN
- Custom colors: navy (#1a2744), accent (#3182ce), accent-light (#63b3ed)
- Font: Inter from Google Fonts

### Navigation
- Desktop: Home | About | Services | Blog | Contact | Pay Online
- Mobile: Same links in slide-out menu with toll-free number
- Top contact bar with toll-free and office numbers

## Content Writing Rules

1. **No em dashes.** Use commas, periods, or "and" instead.
2. **Use specific numbers.** Not "significant savings" but "$200-$400 annually."
3. **Write for AI citation.** Structure answers so AI can extract clean, factual statements.
4. **Geographic anchoring.** Mention Mississippi, Louisiana, and specific cities naturally.
5. **Authority signals.** Reference "since 1978", "licensed in MS & LA", "background-checked technicians."
6. **Service cross-selling.** Every page should naturally reference related services.
