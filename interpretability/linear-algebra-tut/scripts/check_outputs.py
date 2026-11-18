"""Every quoted output block in the lessons must appear verbatim in the saved transcript."""
import re
from html import unescape
from pathlib import Path
from build import ROOT

transcript = (ROOT / 'research/verify/lab-transcript.txt').read_text()
blocks = 0; missing = []
for page in sorted((ROOT / 'pages').glob('*.html')):
    for m in re.finditer(r'<pre class="term out"><code>(.*?)</code></pre>', page.read_text(), re.S):
        blocks += 1
        text = unescape(m.group(1))
        if text not in transcript:
            first_bad = next((line for line in text.splitlines() if line not in transcript), text[:80])
            missing.append(f'{page.name}: block {blocks} not in transcript; first missing line: {first_bad!r}')
if missing:
    print('\n'.join(missing)); raise SystemExit(1)
print(f'PASS: {blocks} quoted output blocks match the transcript verbatim.')
