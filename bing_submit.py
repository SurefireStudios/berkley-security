import sys
import json
import urllib.request
import xml.etree.ElementTree as ET

def submit_to_bing(api_key):
    site_url = "https://berkleysecurity.com"
    sitemap_path = "sitemap.xml"
    
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return

    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in root.findall('.//sm:loc', ns)]
    
    if not urls:
        print("No URLs found in sitemap.xml!")
        return

    print(f"Found {len(urls)} URLs in sitemap.xml. Submitting to Bing...")

    # Bing URL Submission API accepts up to 500 URLs per batch
    batch_size = 500
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        payload = {
            "siteUrl": site_url,
            "urlList": batch
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={api_key}",
            data=data,
            headers={'Content-Type': 'application/json'}
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                batch_num = (i // batch_size) + 1
                print(f"Batch {batch_num}: Success! Bing Response: {result}")
        except Exception as e:
            print(f"Batch {(i // batch_size) + 1}: Error - {e}")

if __name__ == "__main__":
    api_key = "a5bf25e7f8b24b699668c7d58a7ab227"
    submit_to_bing(api_key)
