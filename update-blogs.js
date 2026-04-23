const fs = require('fs');
const path = require('path');

const blogHtmlPath = 'blog.html';
const blogDir = 'blog';

let html = fs.readFileSync(blogHtmlPath, 'utf8');

const gridStartStrAlt = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="blog-grid">';
let gridStartMatches = html.split(gridStartStrAlt);

if (gridStartMatches.length < 2) {
    console.log("Could not find grid container.");
    process.exit(1);
}

const preGrid = gridStartMatches[0];
const gridAndPost = gridStartMatches[1];

let sections = gridAndPost.split('</div>\n    </div>\n  </section>');
if (sections.length < 2) sections = gridAndPost.split('</div>\r\n    </div>\r\n  </section>');

let articlesHtml = sections[0];
const postGrid = sections.slice(1).join('</div>\n    </div>\n  </section>');

const articleRegex = /<article[\s\S]*?<\/article>/g;
let match;
let articles = [];

while ((match = articleRegex.exec(articlesHtml)) !== null) {
    let rawStr = match[0];
    let dateMatch = rawStr.match(/<p class="text-sm text-gray-500 mb-2">(.*?)<\/p>/);
    let dateStr = dateMatch ? dateMatch[1] : '';
    let parsedDate = new Date(dateStr);
    if (isNaN(parsedDate)) parsedDate = new Date(0);

    let linkMatch = rawStr.match(/href="([^"]+)"/);
    let link = linkMatch ? linkMatch[1] : '';

    articles.push({
        html: rawStr,
        dateStr: dateStr,
        timestamp: parsedDate.getTime(),
        link: link
    });
}

// Find files in blog folder that are not in articles array
let existingLinks = new Set(articles.map(a => a.link).filter(Boolean));

let files = fs.readdirSync(blogDir);
let addedCount = 0;

for (let file of files) {
    if (!file.endsWith('.html')) continue;
    
    let expectedLink = 'blog/' + file;
    if (!existingLinks.has(expectedLink)) {
        // Read file to get title and description
        let content = fs.readFileSync(path.join(blogDir, file), 'utf8');
        
        // Grab title from standard H1 or Title meta
        let titleMatch = content.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
        let fallbackTitleMatch = content.match(/<title>([\s\S]*?)<\/title>/);
        let title = titleMatch ? titleMatch[1].trim() : (fallbackTitleMatch ? fallbackTitleMatch[1].trim() : file);
        title = title.replace(/<[^>]+>/g, '');
        
        let descMatch = content.match(/<meta name="description" content="([^"]+)"/);
        // Fallback to first p if no desc
        if(!descMatch) descMatch = content.match(/<p>([\s\S]*?)<\/p>/);
        let desc = descMatch ? descMatch[1].trim() : "Protect your property natively intelligently.";
        desc = desc.substring(0, 150) + "...";

        // Grab published date from json-ld
        let datePubMatch = content.match(/"datePublished":"([^"]+)"/);
        let dateStr = "April 23, 2026";
        if (datePubMatch) {
            let pDate = new Date(datePubMatch[1]);
            dateStr = pDate.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
        }
        
        let parsedDate = new Date(dateStr);

        let articleTemplate = `          <article class="bg-white flex flex-col rounded-xl shadow-sm overflow-hidden hover:shadow-lg transition-shadow duration-300">
            <div class="h-48 bg-navy flex items-center justify-center shrink-0">
              <svg class="w-16 h-16 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div class="p-6 flex flex-col flex-grow">
              <p class="text-sm text-gray-500 mb-2">${dateStr}</p>
              <h2 class="text-xl font-bold text-navy mb-3">${title}</h2>
              <p class="text-gray-600 text-sm mb-4 flex-grow">${desc}</p>
              <a href="${expectedLink}" class="text-accent font-semibold text-sm hover:text-blue-600 transition-colors mt-auto inline-block py-2">Read More &rarr;</a>
            </div>
          </article>`;

        articles.push({
            html: articleTemplate,
            dateStr: dateStr,
            timestamp: parsedDate.getTime() + addedCount, // Ensure deterministic sorting for same day
            link: expectedLink
        });
        addedCount++;
    }
}

console.log('Added ' + addedCount + ' missing articles locally into blog.html.');

articles.sort((a, b) => b.timestamp - a.timestamp);

let newArticlesHtml = articles.map(a => a.html).join('\n');

let rebuiltHtml = preGrid + '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="blog-grid">\n' + newArticlesHtml + '\n</div>\n    </div>\n  </section>' + postGrid;

fs.writeFileSync(blogHtmlPath, rebuiltHtml, 'utf8');
console.log('Done.');
