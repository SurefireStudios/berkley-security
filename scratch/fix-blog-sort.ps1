$file = "c:\Users\Haz\Desktop\Berkley Security\blog.html"
$content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)

$oldBlock1 = @"
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
"@

$newBlock = @"
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const searchInput = document.getElementById('blog-search');
      const sortSelect  = document.getElementById('sort-select');
      const grid        = document.getElementById('blog-grid');

      if (!grid) return;

      function parseArticleDate(article) {
        const dateEl = article.querySelector('p.text-sm.text-gray-500');
        if (!dateEl) return 0;
        const d = new Date(dateEl.textContent.trim());
        return isNaN(d) ? 0 : d.getTime();
      }

      function applySort() {
        const order = sortSelect ? sortSelect.value : 'newest';
        const articles = Array.from(grid.querySelectorAll('article'));
        articles.sort((a, b) => {
          const da = parseArticleDate(a);
          const db = parseArticleDate(b);
          return order === 'oldest' ? da - db : db - da;
        });
        articles.forEach(article => grid.appendChild(article));
        applySearch();
      }

      function applySearch() {
        const term = searchInput ? searchInput.value.toLowerCase().trim() : '';
        const articles = grid.querySelectorAll('article');
        articles.forEach(article => {
          const text = article.textContent.toLowerCase();
          article.style.display = (!term || text.includes(term)) ? 'flex' : 'none';
        });
      }

      if (searchInput) {
        searchInput.addEventListener('input', applySearch);
      }

      if (sortSelect) {
        sortSelect.addEventListener('change', applySort);
        applySort();
      }
    });
  </script>
"@

# Normalize line endings to LF for matching, then replace, then convert back
$contentLF = $content.Replace("`r`n", "`n")
$old1LF = $oldBlock1.Replace("`r`n", "`n")
$newLF = $newBlock.Replace("`r`n", "`n")

if ($contentLF.Contains($old1LF)) {
    $updatedLF = $contentLF.Replace($old1LF, $newLF)
    $updated = $updatedLF.Replace("`n", "`r`n")
    [System.IO.File]::WriteAllText($file, $updated, [System.Text.Encoding]::UTF8)
    Write-Host "SUCCESS: Sort+search script injected."
} else {
    Write-Host "WARNING: Old block not found - trying line-based approach."
    # Fall back: remove lines 2510-2554 (0-indexed: 2509-2553) and insert new block
    $lines = [System.IO.File]::ReadAllLines($file, [System.Text.Encoding]::UTF8)
    Write-Host "Total lines: $($lines.Length)"
    
    # Find the first standalone <script> after line 2508 (0-indexed 2507)
    $startIdx = -1
    $endIdx = -1
    for ($i = 2507; $i -lt $lines.Length; $i++) {
        if ($lines[$i].Trim() -eq '<script>' -and $startIdx -eq -1) {
            $startIdx = $i
        }
        if ($startIdx -ge 0 -and $i -gt $startIdx -and $lines[$i].Trim() -eq '</script>') {
            $endIdx = $i
            # Check if there's another block immediately after (the duplicate)
        }
    }
    Write-Host "First block: $startIdx to $endIdx"
    
    # Find second </script> after endIdx
    $end2Idx = -1
    for ($i = $endIdx + 1; $i -lt $lines.Length; $i++) {
        if ($lines[$i].Trim() -eq '<script>') {
            for ($j = $i + 1; $j -lt $lines.Length; $j++) {
                if ($lines[$j].Trim() -eq '</script>') {
                    $end2Idx = $j
                    break
                }
            }
            break
        }
    }
    Write-Host "Second block ends: $end2Idx"
    
    if ($startIdx -ge 0 -and $end2Idx -ge 0) {
        $before = $lines[0..($startIdx - 1)]
        $after  = $lines[($end2Idx + 1)..($lines.Length - 1)]
        $newLines = $newBlock.Split("`n") | ForEach-Object { $_.TrimEnd("`r") }
        $combined = $before + $newLines + $after
        [System.IO.File]::WriteAllLines($file, $combined, [System.Text.Encoding]::UTF8)
        Write-Host "SUCCESS via line-based approach."
    } else {
        Write-Host "ERROR: Could not locate script blocks."
    }
}
