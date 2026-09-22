#!/usr/bin/env bash
# Build build/repo-with-history: the buggy app on main, the fix on branch "upstream-fix".
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
rm -rf build/repo-with-history
mkdir -p build
cp -R app build/repo-with-history
cd build/repo-with-history
git init -q -b main
git -c user.name=maintainer -c user.email=m@example.com add -A
git -c user.name=maintainer -c user.email=m@example.com commit -q -m "wordfreq: initial import"
git checkout -q -b upstream-fix
python3 - <<'PY'
import re
src = open("wordfreq.py", encoding="utf-8").read()
src = src.replace("import sys\n", "import re\nimport sys\n")
src = re.sub(r"    # BUG:.*\n    return Counter\(text\.split\(\)\)\n",
             "    return Counter(re.findall(r\"[a-z]+(?:'[a-z]+)*\", text.lower()))\n", src)
open("wordfreq.py", "w", encoding="utf-8").write(src)
PY
git -c user.name=maintainer -c user.email=m@example.com commit -q -am "count words case-insensitively, ignore punctuation (fixes #12)"
git checkout -q main
