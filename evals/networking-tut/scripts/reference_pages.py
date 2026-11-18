from course_content import SOURCES, h, p, table, box, code, check
import json
from pathlib import Path
from html import escape

REFERENCES=[]
def ref(path,title,kicker,lede,body,n,kw):
    REFERENCES.append(dict(path=path,title=title,kicker=kicker,lede=lede,body=body,n=n,kw=kw))

glossary=json.loads((Path(__file__).resolve().parents[1]/'research/glossary.json').read_text())
letters={}
for slug,entry in sorted(glossary.items(),key=lambda item:item[1]['name'].lower()):
    letters.setdefault(entry['name'][0].upper(),[]).append((slug,entry))
glossary_body='<div data-glossary><div class="gloss-index">'+''.join(f'<a href="#letter-{letter}">{letter}</a>' for letter in letters)+'</div>'
for letter,entries in letters.items():
    glossary_body+=f'<div class="gloss-letter" id="letter-{letter}">{letter}</div>'
    for slug,entry in entries:
        glossary_body+=f'<div class="gloss-entry" id="{slug}"><h3>{escape(entry["name"])}</h3><p>{escape(entry["def"])}</p></div>'
glossary_body+='</div>'

ref('glossary.html','Glossary','Reference · Vocabulary',
    'Plain-language definitions for the course. Dashed-underlined terms in lessons show a short definition and link here.',
    glossary_body, 'G','terms definitions vocabulary glossary')

ref('appendices/a-calculators.html','Network calculators','Appendix A · Work the numbers',
    'Small, local calculators for checking intuition. These are simplified teaching models, not measurements of your network.',
    h('subnet','Read an IPv4 prefix')+
    p('Enter an IPv4 address and prefix length. The calculator normalizes the network prefix and shows the inclusive range. Address count is not usable-host count: operating systems, cloud providers, and subnet types reserve or interpret addresses differently.')+
    '<div class="explorer" data-subnet><label for="cidr">Address and prefix</label><input id="cidr" value="10.20.1.42/24" inputmode="text" spellcheck="false"><output aria-live="polite" data-result></output></div>'+
    check('Which contains more addresses: /16 or /24?', '/16 leaves 16 variable bits and describes 65,536 addresses. /24 leaves eight variable bits and describes 256. The shorter fixed prefix covers the larger range. A /32 describes one IPv4 address; /0 covers the entire IPv4 address space.')+
    h('transfer','Compute a serialization lower bound')+
    '<div class="explorer" data-transfer><label for="size">Transfer size (decimal MB)</label><input id="size" type="number" min="0" max="1000000" step="any" value="100"><label for="bandwidth">Bottleneck rate (Mb/s)</label><input id="bandwidth" type="number" min="0.001" max="1000000" step="any" value="100"><output aria-live="polite" data-result></output></div>'+
    p('Formula: <code>seconds = MB × 8 / Mb per second</code>. This ignores propagation, queueing, handshakes, protocol overhead, other traffic, and server computation. Do not add overlapping stages twice. MiB and GiB are binary units; these inputs deliberately use decimal MB and Mb.')+
    h('inflight','Estimate average in-flight work')+
    '<div class="explorer" data-capacity><label for="rate">Target completed attempts per second</label><input id="rate" type="number" min="0" max="100000" step="any" value="20"><label for="duration">Mean attempt lifetime (seconds)</label><input id="duration" type="number" min="0.001" max="100000" step="any" value="3"><output aria-live="polite" data-result></output></div>'+
    p('Formula: <code>average in-flight work = throughput × mean time in system</code>. It applies to a stable system with matching measurement boundaries. The result is neither a safe production setting nor a guarantee of throughput. Count queue time if the population includes queued work; exclude it consistently if measuring only active requests.'),
    'A','CIDR calculator bandwidth throughput latency concurrency subnet math')

ref('appendices/b-commands.html','Command reference','Appendix B · Evidence at the terminal',
    'Commands are useful when you can state what their output establishes. Examples use loopback, public example.com, or clearly marked placeholders.',
    h('before','Before collecting evidence')+
    p('Record where the command runs: laptop, container, Pod, or CI worker. Check tool availability and version. Use credential-free endpoints for routine probes and redact any sensitive headers or URLs before sharing output. Placeholder commands below need the real authorized names; do not paste them unchanged.')+
    table(['Command','Establishes','Limit'],[
      ['<code>dig example.com A</code>','A DNS response from the selected resolver.','Not TCP, TLS, HTTP, or necessarily the application’s exact resolver path.'],
      ['<code>curl -i URL</code>','HTTP response headers and body.','HTTP errors do not normally make curl’s process exit fail.'],
      ['<code>curl -v URL</code>','Connection, TLS, and request details.','Verbose output can expose secrets; proxying changes the path.'],
      ['<code>curl -N URL</code>','Output without curl’s ordinary buffering.','Does not disable upstream proxy or server buffering.'],
      ['<code>ping HOST</code>','An ICMP round-trip response, if allowed.','No proof of HTTP reachability; failure can be filtering.'],
      ['<code>traceroute HOST</code>','Responses from some hops to its probes.','Missing replies do not by themselves prove packet loss for your app.'],
      ['<code>lsof -nP -iTCP:8765 -sTCP:LISTEN</code>','A visible local TCP listener (common on macOS).','Not remote reachability; visibility depends on permissions.'],
      ['<code>ss -ltn</code>','Listening TCP sockets on Linux.','Run in the relevant network namespace.'],
      ['<code>ip route get ADDRESS</code>','Linux route selection for an address.','No proof that packets or replies complete the path.'],
      ['<code>route -n get ADDRESS</code>','macOS route selection for an address.','The same limitation; ADDRESS is a placeholder.']])+
    h('timing','Measure a simple HTTPS transfer')+
    code("curl -sS -o /dev/null --connect-timeout 5 --max-time 20 \\\n  -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} first_byte=%{time_starttransfer} total=%{time_total} status=%{http_code}\\n' \\\n  https://example.com/")+
    p('Times are seconds measured cumulatively from transfer start. Differences can approximate phases for a simple fresh connection, but redirects, proxies, reuse, and protocol differences need care. First byte is not first token. A status of 000 indicates that curl did not obtain an HTTP response status; inspect its error and exit code.')+
    h('override','Isolate DNS without changing TLS identity')+
    code('curl --resolve api.example.test:443:192.0.2.10 \\\n  --connect-timeout 5 --max-time 15 https://api.example.test/health')+
    p('This is schematic: example.test and 192.0.2.10 are documentation placeholders. Replace them with an approved hostname, port, and verified address for your service. The URL hostname remains the TLS/HTTP identity. The result tests the chosen address, not ordinary DNS behavior; remove the override after the experiment.')+
    h('exit','Common curl exit codes in this course')+
    table(['Exit','Meaning to investigate'],[['6','Could not resolve the host.'],['7','Failed to connect.'],['22','HTTP error when a fail option is enabled.'],['28','Operation timeout.'],['35','TLS/SSL connection error.'],['60','Peer certificate verification failed.']])+
    p('The exact error text and environment matter. Consult the installed tool’s documentation when flags are unavailable; the <a href="https://curl.se/docs/manpage.html">official curl manual</a> is the source for these options and timing definitions.'),
    'B','commands curl dig ping traceroute lsof ss route timing exit codes')

ref('appendices/c-reading-map.html','A focused route through the book','Appendix C · Reading map',
    'Use the book for deeper explanations of the principles behind the course. You do not need to read every chapter before beginning practical eval work.',
    p('The supplied link starts <a href="https://7e.systemsapproach.org/part_one.html">Part I: Foundation</a> of <em>Computer Networks: A Systems Approach</em>, by Larry Peterson and Bruce Davie. The online edition identifies itself as Version 7.0-dev and is updated over time. Chapter links here were checked on September 20, 2026.')+
    table(['Priority','Book chapters','Read with this question'],[
      ['Core first pass','<a href="https://7e.systemsapproach.org/introduction.html">1: Introduction</a>','What do layers promise, and how do bandwidth and latency differ?'],
      ['Core first pass','<a href="https://7e.systemsapproach.org/applications.html">2: Network Applications</a>','How does a web request use the network, and what changed across HTTP versions?'],
      ['Core first pass','<a href="https://7e.systemsapproach.org/naming.html">11: Naming</a>','How do names resolve, and where does caching change observations?'],
      ['Core first pass','<a href="https://7e.systemsapproach.org/reliable.html">12: Reliable Byte Stream</a>','What does TCP guarantee, and what does an application still need to do?'],
      ['Core first pass','<a href="https://7e.systemsapproach.org/secure.html">14: Secure Channels</a>','How do encryption, authentication, and certificates fit together?'],
      ['Core first pass','<a href="https://7e.systemsapproach.org/message.html">15: Message Transactions</a>','Why are duplicate requests and uncertain outcomes application problems?'],
      ['Selected depth','<a href="https://7e.systemsapproach.org/federation.html">6: Federating Networks</a>','How do IP prefixes, forwarding, and NAT affect a worker’s path?'],
      ['Selected depth','<a href="https://7e.systemsapproach.org/virtual.html">9: Virtualizing Networks</a> and <a href="https://7e.systemsapproach.org/operations.html">10: Operating Networks</a>','What is logical versus physical, and how do operators gather evidence?'],
      ['Recognize, then revisit','<a href="https://7e.systemsapproach.org/technology.html">3: Network Technology</a>, <a href="https://7e.systemsapproach.org/routing.html">4: Routing</a>, <a href="https://7e.systemsapproach.org/congestion.html">13: Congestion Control</a>','What do links, routing algorithms, and congestion mechanisms contribute below the application?']])+
    box('A reading method','Before a section, write the question you want answered. After it, explain one implication for the eval worker and one thing the protocol does not guarantee. Follow unfamiliar words into the glossary; return to packet-level details when a concrete problem calls for them.')+
    p('The book provides a systems foundation. Product-specific routes, Kubernetes objects, curl flags, and GPU libraries require the official documentation linked in the course. The original exercises apply those principles to eval work; they are not claims that the textbook prescribes a particular eval architecture.'),
    'C','Systems Approach book textbook reading map chapters deeper study')

ref('bibliography.html','Annotated bibliography','Reference · Sources and attribution',
    'Primary materials behind the explanations, with the job each source does in this course. Examples and assessment rubrics are original teaching material.',
    box('Textbook attribution','<em>Computer Networks: A Systems Approach</em>, Larry Peterson and Bruce Davie. Copyright Larry L. Peterson and Bruce S. Davie, 2026. <a href="https://github.com/SystemsApproach/7E">Source repository</a>; <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. The book also attributes earlier-edition content to Elsevier, 2012, from <a href="https://github.com/SystemsApproach/book">SystemsApproach/book</a> under CC BY 4.0. This independent companion reorganizes and explains concepts for LLM evals and adds original scenarios, calculations, diagrams, and exercises. It is not endorsed by the book’s authors.','callout')+
    p('Sources were accessed on September 20, 2026. The book is a living development edition, and operational documentation can change. Numeric performance examples are invented and explicitly labeled; they are not benchmark measurements. The source-check notes record topics checked rather than asserting that every sentence is a quotation or directly specified by a source.')+
    ''.join(h(key,title)+p(desc+' <a href="'+url+'">Read the source →</a>') for key,(title,url,desc) in SOURCES.items())+
    h('scope','How to read the evidence')+
    p('Protocol facts are grounded in the textbook and specifications. Provider behavior is described with its provider name and official source. Eval architecture choices, retry budgets, incident scenarios, and the readiness rubric are reasoned teaching recommendations, not universal provider defaults or hiring criteria. The local lab verifies only the behavior of its own included server.'),
    'R','sources bibliography citations reference provenance attribution license')
