const fs = require('fs');
const path = require('path');
const http = require('http');

const cityDir = path.join(__dirname, '..', 'city');

function fetchZipCodes(state, city) {
    return new Promise((resolve, reject) => {
        // Clean up city name for API (e.g., st-joseph -> st joseph)
        const apiCity = city.replace(/-/g, '%20');
        const url = `http://api.zippopotam.us/us/${state}/${apiCity}`;
        
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const json = JSON.parse(data);
                        const zips = json.places.map(p => p['post code']);
                        // Deduplicate
                        const uniqueZips = [...new Set(zips)];
                        resolve(uniqueZips);
                    } catch (e) {
                        resolve([]);
                    }
                } else {
                    resolve([]);
                }
            });
        }).on('error', (err) => {
            resolve([]);
        });
    });
}

async function processFiles() {
    const files = fs.readdirSync(cityDir).filter(f => f.endsWith('.html'));
    
    for (const file of files) {
        const filePath = path.join(cityDir, file);
        let html = fs.readFileSync(filePath, 'utf8');
        
        // Skip if already modified
        if (html.includes('- Zip Code')) {
            console.log(`Skipping ${file} - already has zip code.`);
            continue;
        }

        const match = file.match(/^(.+)-([a-z]{2})\.html$/);
        if (!match) continue;
        
        const citySlug = match[1];
        const state = match[2];
        
        // Fetch zip codes
        let zips = await fetchZipCodes(state, citySlug);
        
        if (zips.length === 0) {
            console.log(`No zip codes found for ${citySlug}, ${state}. Skipping.`);
            continue;
        }
        
        let zipString = '';
        if (zips.length === 1) {
            zipString = ` - Zip Code ${zips[0]}`;
        } else if (zips.length === 2) {
            zipString = ` - Zip Codes ${zips[0]} and ${zips[1]}`;
        } else if (zips.length > 2) {
             // For 3 or more, format like "39157, 39158, and 39159"
             // But actually let's just use up to 3 to keep it small, or all if there are only a few.
             if(zips.length > 5) {
                 zips = zips.slice(0, 5); // Limit to 5 max
                 zipString = ` - Zip Codes ${zips.slice(0, -1).join(', ')}, and ${zips[zips.length-1]}`;
             } else {
                 zipString = ` - Zip Codes ${zips.slice(0, -1).join(', ')} and ${zips[zips.length-1]}`;
             }
        }

        // Regex to find the hero <p> tag
        // <p class="text-accent-light font-semibold mb-3 tracking-wide uppercase text-sm">Alexandria, Louisiana - Heart of Central Louisiana</p>
        const pRegex = /(<p class="text-accent-light[^>]*>)(.*?)(<\/p>)/;
        
        if (pRegex.test(html)) {
            html = html.replace(pRegex, `$1$2${zipString}$3`);
            fs.writeFileSync(filePath, html, 'utf8');
            console.log(`Updated ${file} with ${zipString}`);
        } else {
            console.log(`Could not find target <p> tag in ${file}`);
        }
    }
}

processFiles().then(() => console.log('Done!'));
