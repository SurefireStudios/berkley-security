const fs = require('fs');
const path = 'blog.html';
let html = fs.readFileSync(path, 'utf8');

// 1. Replace the search UI specifically by slicing it out
const startTarget = '<div class="max-w-3xl mb-12">';
const endTarget = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="blog-grid">';

let startIdx = html.indexOf(startTarget);
let endIdx = html.indexOf(endTarget, startIdx);

if (startIdx !== -1 && endIdx !== -1) {
    const newUI = `      <div class="max-w-4xl mb-12">
        <label for="blog-search" class="sr-only">Search Articles</label>
        <div class="relative mb-6">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          <input type="text" id="blog-search" class="block w-full pl-10 pr-3 py-4 border border-gray-200 rounded-xl leading-5 bg-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-base transition-shadow shadow-sm hover:shadow" placeholder="Search blog posts by keyword, topic, or location...">
        </div>
        
        <div class="flex flex-wrap items-center gap-3" id="blog-filters">
          <span class="text-sm font-semibold text-gray-500 uppercase tracking-wider mr-2 hidden sm:inline-block">Filters:</span>
          <button data-filter="all" class="filter-btn active px-4 py-2 rounded-full text-sm font-medium transition-colors bg-navy text-white border border-navy hover:bg-blue-800">All Posts</button>
          <button data-filter="local" class="filter-btn px-4 py-2 rounded-full text-sm font-medium transition-colors bg-white text-gray-600 border border-gray-200 hover:bg-blue-50 hover:text-accent hover:border-blue-200">Local Area Guides</button>
          <button data-filter="residential" class="filter-btn px-4 py-2 rounded-full text-sm font-medium transition-colors bg-white text-gray-600 border border-gray-200 hover:bg-blue-50 hover:text-accent hover:border-blue-200">Residential</button>
          <button data-filter="commercial" class="filter-btn px-4 py-2 rounded-full text-sm font-medium transition-colors bg-white text-gray-600 border border-gray-200 hover:bg-blue-50 hover:text-accent hover:border-blue-200">Commercial</button>
          <button data-filter="guides" class="filter-btn px-4 py-2 rounded-full text-sm font-medium transition-colors bg-white text-gray-600 border border-gray-200 hover:bg-blue-50 hover:text-accent hover:border-blue-200">Tips & Guides</button>
        </div>
      </div>\n`;

    html = html.slice(0, startIdx) + newUI + html.slice(endIdx);
}

// 2. Replace the script blocks at the bottom of the body
const scriptStartStr = '</div>\n  </section>\n\n  <script>';
const scriptStartStrAlt = '</div>\r\n  </section>\r\n\r\n  <script>';

let scriptIdx = html.indexOf(scriptStartStr);
if (scriptIdx === -1) {
    scriptIdx = html.indexOf(scriptStartStrAlt);
}

if (scriptIdx !== -1) {
    const newScriptSection = `</div>
  </section>

  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const searchInput = document.getElementById('blog-search');
      const grid = document.getElementById('blog-grid');
      const filterBtns = document.querySelectorAll('.filter-btn');
      
      let currentFilter = 'all';
      let currentSearch = '';

      if(searchInput && grid) {
        const articles = Array.from(grid.querySelectorAll('article'));

        articles.forEach(article => {
          const text = article.textContent.toLowerCase();
          const title = (article.querySelector('h2') ? article.querySelector('h2').textContent.toLowerCase() : "");
          
          if (title.includes('security systems in')) {
            article.dataset.category = 'local';
          } else if (text.match(/home|residential|driveway|estate|family|pool|yard|house|theater/)) {
            article.dataset.category = 'residential';
          } else if (text.match(/commercial|business|warehouse|office|store|facility|pharmacy|law/)) {
            article.dataset.category = 'commercial';
          } else {
            article.dataset.category = 'guides';
          }
        });

        function filterArticles() {
          articles.forEach(article => {
            const text = article.textContent.toLowerCase();
            const matchesSearch = text.includes(currentSearch);
            const matchesCategory = currentFilter === 'all' || article.dataset.category === currentFilter;

            if (matchesSearch && matchesCategory) {
              article.style.display = 'flex';
            } else {
              article.style.display = 'none';
            }
          });
        }

        searchInput.addEventListener('input', (e) => {
          currentSearch = e.target.value.toLowerCase().trim();
          filterArticles();
        });

        if (filterBtns) {
          filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
              filterBtns.forEach(b => {
                b.classList.remove('bg-navy', 'text-white', 'border-navy');
                b.classList.add('bg-white', 'text-gray-600', 'border-gray-200');
              });
              e.target.classList.remove('bg-white', 'text-gray-600', 'border-gray-200');
              e.target.classList.add('bg-navy', 'text-white', 'border-navy');
              
              currentFilter = e.target.dataset.filter;
              filterArticles();
            });
          });
        }
      }
    });
  </script>
</body>
</html>`;

    // We slice from the start to scriptIdx, then append new
    html = html.slice(0, scriptIdx) + newScriptSection;
}

fs.writeFileSync(path, html, 'utf8');
console.log('Fixed blog.html correctly.');
