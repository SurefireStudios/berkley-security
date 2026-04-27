const fs = require('fs');
const path = require('path');

const rootDir = path.join(__dirname, '..');
const cityDir = path.join(rootDir, 'city');

// 1. Get all cities and group by state
const cityFiles = fs.readdirSync(cityDir).filter(f => f.endsWith('.html'));
const cities = { ms: [], la: [] };

cityFiles.forEach(file => {
    const match = file.match(/^(.+)-([a-z]{2})\.html$/);
    if (match) {
        let name = match[1].replace(/-/g, ' ');
        // capitalize
        name = name.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
        
        const state = match[2];
        if (cities[state]) {
            cities[state].push({ name, file: `city/${file}` });
        }
    }
});

// Sort alphabetically
cities.ms.sort((a, b) => a.name.localeCompare(b.name));
cities.la.sort((a, b) => a.name.localeCompare(b.name));

function generatePills(cityList, isSubdir=false) {
    const prefix = isSubdir ? '../' : '';
    return cityList.map(c => `<a href="${prefix}${c.file}" class="inline-block bg-white/10 hover:bg-accent/80 border border-white/20 rounded-full px-4 py-2 text-sm transition-colors text-white">${c.name}</a>`).join('\n              ');
}

// 2. Generate locations.html (based on index.html template)
const indexHtml = fs.readFileSync(path.join(rootDir, 'index.html'), 'utf8');

// Extract header and footer from index.html to reuse
const headerMatch = indexHtml.match(/(<!DOCTYPE html>[\s\S]+?<main>)/);
const footerMatch = indexHtml.match(/(<\/main>[\s\S]+?<\/html>)/);

if (headerMatch && footerMatch) {
    let header = headerMatch[1];
    let footer = footerMatch[1];
    
    // Fix paths and active states if necessary, change title
    header = header.replace(/<title>.*?<\/title>/, '<title>Service Areas | Berkley Security Locations in MS & LA</title>');
    header = header.replace(/<meta name="description" content=".*?">/, '<meta name="description" content="Berkley Security provides top-tier security systems, cameras, and fire alarms across Mississippi and Louisiana. Find your local service area.">');
    header = header.replace(/<link rel="canonical" href=".*?">/, '<link rel="canonical" href="https://berkleysecurity.com/locations.html">');

    const mainContent = `
    <section class="hero-pattern text-white py-16 md:py-24 lg:py-32 relative">
      <div class="absolute inset-0 bg-navy/80"></div>
      <div class="max-w-7xl mx-auto px-4 relative z-10 text-center">
        <p class="text-accent-light font-semibold mb-3 tracking-wide uppercase text-sm">Service Coverage</p>
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6">Serving Mississippi & Louisiana</h1>
        <p class="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto">All of our security services are available throughout Mississippi and Louisiana, with main offices in Vicksburg, Natchez, and Vidalia.</p>
      </div>
    </section>

    <section class="py-16 lg:py-20 bg-navy text-white">
      <div class="max-w-7xl mx-auto px-4">
        <div class="grid lg:grid-cols-2 gap-12">
          <!-- Mississippi -->
          <div>
            <h2 class="text-2xl font-bold text-accent-light mb-6 flex items-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              Mississippi
            </h2>
            <div class="flex flex-wrap gap-3">
              ${generatePills(cities.ms)}
            </div>
          </div>
          <!-- Louisiana -->
          <div>
            <h2 class="text-2xl font-bold text-accent-light mb-6 flex items-center gap-2">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
              Louisiana
            </h2>
            <div class="flex flex-wrap gap-3">
              ${generatePills(cities.la)}
            </div>
            
            <div class="mt-12 p-8 bg-white/5 rounded-2xl border border-white/10">
              <h3 class="text-xl font-bold text-white mb-3">Don't see your city?</h3>
              <p class="text-gray-300 mb-6">We serve communities throughout the entire region. If your specific town or county is not listed above, it is very likely we still cover it.</p>
              <a href="contact.html" class="inline-flex items-center gap-2 bg-accent hover:bg-blue-600 px-6 py-3 rounded-lg text-white font-semibold transition-colors">
                Contact us to check coverage
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
    `;

    fs.writeFileSync(path.join(rootDir, 'locations.html'), header + mainContent + footer, 'utf8');
    console.log('Created locations.html');
}

// 3. Update all footers across top-level HTML files and blog files
const allFiles = [];

// Get top level HTML
fs.readdirSync(rootDir).forEach(f => {
    if (f.endsWith('.html')) allFiles.push({ path: path.join(rootDir, f), isSubdir: false });
});

// Get blog HTML
const blogDir = path.join(rootDir, 'blog');
if (fs.existsSync(blogDir)) {
    fs.readdirSync(blogDir).forEach(f => {
        if (f.endsWith('.html')) allFiles.push({ path: path.join(blogDir, f), isSubdir: true });
    });
}

// Get city HTML
if (fs.existsSync(cityDir)) {
    fs.readdirSync(cityDir).forEach(f => {
        if (f.endsWith('.html')) allFiles.push({ path: path.join(cityDir, f), isSubdir: true });
    });
}

let updatedCount = 0;
for (const fileObj of allFiles) {
    let content = fs.readFileSync(fileObj.path, 'utf8');
    
    // Check if Service Areas link already exists
    if (content.includes('>Service Areas<')) continue;

    const linkPath = fileObj.isSubdir ? '../locations.html' : 'locations.html';
    
    // We want to add it to the Quick Links column in the footer
    // Look for: <li><a href="contact.html" class="text-sm text-gray-400 hover:text-white transition-colors">Contact</a></li>
    const contactLinkRegex = /(<a href="[^"]*contact\.html"[^>]*>Contact<\/a><\/li>)/;
    
    if (contactLinkRegex.test(content)) {
        content = content.replace(contactLinkRegex, `$1\n            <li><a href="${linkPath}" class="text-sm text-gray-400 hover:text-white transition-colors">Service Areas</a></li>`);
        fs.writeFileSync(fileObj.path, content, 'utf8');
        updatedCount++;
    }
}

console.log(`Updated footers in ${updatedCount} files.`);
