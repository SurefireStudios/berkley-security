const fs = require('fs');
const path = 'C:\\Users\\Haz\\Desktop\\Berkley Security\\blog.html';
let html = fs.readFileSync(path, 'utf8');

// 1. Replace the entire top search/filter block
const uiStartStr = '<div class="max-w-4xl mb-12">';
const uiEndStr = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="blog-grid">';

let startIdx = html.indexOf(uiStartStr);
let endIdx = html.indexOf(uiEndStr, startIdx);

if (startIdx !== -1 && endIdx !== -1) {
    const newUI = `      <div class="max-w-7xl mx-auto mb-10">
        <label for="blog-search" class="sr-only">Search Articles</label>
        <div class="flex flex-col sm:flex-row items-center gap-4">
          <div class="relative flex-grow w-full">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <input type="text" id="blog-search" class="block w-full pl-11 pr-4 py-3 border border-gray-200 rounded-lg leading-5 bg-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent transition-shadow shadow-sm" placeholder="Search blog posts by keyword, topic, or location...">
          </div>
          <button id="search-btn" class="w-full sm:w-auto px-6 py-3 bg-accent text-white font-semibold rounded-lg hover:bg-blue-600 transition-colors shrink-0 shadow-sm">Search</button>
          
          <div class="relative shrink-0 w-full sm:w-48">
            <select id="sort-select" class="block w-full pl-4 pr-10 py-3 text-base border border-gray-200 focus:outline-none focus:ring-2 focus:ring-accent focus:border-accent sm:text-sm rounded-lg bg-white shadow-sm appearance-none cursor-pointer">
              <option value="newest">Sort by: Newest</option>
              <option value="oldest">Sort by: Oldest</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-gray-500">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>
      </div>\n`;

    html = html.slice(0, startIdx) + newUI + html.slice(endIdx);
}

// 2. Replace the script blocks at the bottom of the body
const scriptStartStr = '  <script>\n    document.addEventListener(\'DOMContentLoaded\', () => {';
let scriptIdx = html.indexOf(scriptStartStr);

if (scriptIdx !== -1) {
    const newScriptSection = `  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const searchInput = document.getElementById('blog-search');
      const searchBtn = document.getElementById('search-btn');
      const sortSelect = document.getElementById('sort-select');
      const grid = document.getElementById('blog-grid');
      
      if(searchInput && grid) {
        let articlesArray = Array.from(grid.querySelectorAll('article'));

        // Assign parsed dates to articles for sorting
        articlesArray.forEach(article => {
          const dateElem = article.querySelector('p.text-sm.text-gray-500.mb-2');
          let ts = 0;
          if (dateElem) {
             const parsed = new Date(dateElem.textContent);
             if(!isNaN(parsed)) ts = parsed.getTime();
          }
          article.dataset.timestamp = ts;
        });

        function performSearch() {
          const term = searchInput.value.toLowerCase().trim();
          articlesArray.forEach(article => {
            const text = article.textContent.toLowerCase();
            if (text.includes(term)) {
              article.style.display = 'flex';
            } else {
              article.style.display = 'none';
            }
          });
        }

        // Search Handlers
        searchBtn.addEventListener('click', performSearch);
        searchInput.addEventListener('keyup', (e) => {
          if (e.key === 'Enter') performSearch();
        });
        
        // Optional instant search 
        searchInput.addEventListener('input', performSearch);

        // Sort Handler
        sortSelect.addEventListener('change', (e) => {
          const sortVal = e.target.value;
          articlesArray.sort((a, b) => {
             const tsA = parseInt(a.dataset.timestamp);
             const tsB = parseInt(b.dataset.timestamp);
             if (sortVal === 'oldest') {
                return tsA - tsB;
             } else {
                return tsB - tsA;
             }
          });
          
          // Re-append sorted articles back to grid
          articlesArray.forEach(article => grid.appendChild(article));
        });
      }
    });
  </script>
</body>
</html>`;

    // We slice from the start to scriptIdx, then append new
    html = html.slice(0, scriptIdx) + newScriptSection;
}

fs.writeFileSync(path, html, 'utf8');
console.log('Fixed blog.html layout correctly.');
