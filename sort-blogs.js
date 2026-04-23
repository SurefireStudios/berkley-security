const fs = require('fs');

const path = 'blog.html';
let html = fs.readFileSync(path, 'utf8');

const gridStartStrAlt = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">';

let gridStartMatches = html.split(gridStartStrAlt);

if (gridStartMatches.length < 2) {
    console.log("Could not find grid container.");
    process.exit(1);
}

const preGrid = gridStartMatches[0];
const gridAndPost = gridStartMatches[1];

let sections = gridAndPost.split('</div>\n    </div>\n  </section>');
if (sections.length < 2) sections = gridAndPost.split('</div>\r\n    </div>\r\n  </section>');
if (sections.length < 2) {
    console.error("Could not find the end of the grid");
    process.exit(1);
}

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

    articles.push({
        html: rawStr,
        dateStr: dateStr,
        timestamp: parsedDate.getTime()
    });
}

console.log('Found ' + articles.length + ' articles inside blog.html.');

// SORT articles
articles.sort((a, b) => b.timestamp - a.timestamp);

let newArticlesHtml = articles.map(a => a.html).join('\n');

const searchUI = `
      <div class="max-w-3xl mb-12">
        <label for="blog-search" class="sr-only">Search Articles</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input type="text" id="blog-search" class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-accent focus:border-accent sm:text-sm transition-colors" placeholder="Search blog posts by keyword, topic, or location...">
        </div>
      </div>
`;

const filterScript = `
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const searchInput = document.getElementById('blog-search');
      const grid = document.getElementById('blog-grid');
      
      if(searchInput && grid) {
        const articles = grid.querySelectorAll('article');

        searchInput.addEventListener('input', (e) => {
          const term = e.target.value.toLowerCase().trim();
          articles.forEach(article => {
            const text = article.textContent.toLowerCase();
            if (text.includes(term)) {
              article.style.display = 'flex';
            } else {
              article.style.display = 'none';
            }
          });
        });
      }
    });
  </script>
`;

let rebuiltHtml = preGrid + searchUI + '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="blog-grid">\n' + newArticlesHtml + '\n</div>\n    </div>\n  </section>' + postGrid;

rebuiltHtml = rebuiltHtml.replace('</body>', filterScript + '\n</body>');

fs.writeFileSync(path, rebuiltHtml, 'utf8');
console.log('Done.');
