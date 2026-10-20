"""Original course prose. Run build.py to regenerate the static reading pages."""
from html import escape

MODULES = [
 ('The professional baseline', 'What you need to explain, investigate, and design in an LLM evals role.'),
 ('Follow one request', 'Hosts, packets, addresses, ports, routes, and the journey from a worker to a model.'),
 ('The application stack', 'DNS, TCP, TLS, HTTP, and streaming: what an API call actually depends on.'),
 ('Make runs reliable', 'Latency, concurrency, rate limits, timeouts, retries, and honest measurements.'),
 ('Navigate infrastructure', 'Proxies, cloud networks, containers, Kubernetes, and where inference runs.'),
 ('Investigate failures', 'A repeatable diagnostic method and the evidence to bring to an incident.'),
 ('Practice on a real service', 'Local experiments and realistic incidents with explanations you can check.'),
 ('Design and defend', 'An eval architecture, its trust boundaries, and a final readiness review.'),
]
SOURCES = {}
SOURCES.update({
 'foundation':('Systems Approach, Chapter 1: Introduction','https://7e.systemsapproach.org/introduction.html','Layering, encapsulation, resource sharing, bandwidth, and latency.'),
 'apps':('Systems Approach, Chapter 2: Network Applications','https://7e.systemsapproach.org/applications.html','HTTP and the application view of a network.'),
 'links':('Systems Approach, Chapter 3: Network Technology','https://7e.systemsapproach.org/technology.html','Links, switches, and Ethernet.'),
 'routing':('Systems Approach, Chapter 4: Routing','https://7e.systemsapproach.org/routing.html','Forwarding and the calculation of routes.'),
 'ip':('Systems Approach, Chapter 6: Federating Networks','https://7e.systemsapproach.org/federation.html','IP, prefixes, fragmentation, and address translation.'),
 'virtual':('Systems Approach, Chapter 9: Virtualizing Networks','https://7e.systemsapproach.org/virtual.html','Virtual networks and overlays.'),
 'ops':('Systems Approach, Chapter 10: Operating Networks','https://7e.systemsapproach.org/operations.html','Network management and observation.'),
 'dns':('Systems Approach, Chapter 11: Naming','https://7e.systemsapproach.org/naming.html','Name resolution, DNS records, and caching.'),
 'tcp':('Systems Approach, Chapter 12: Reliable Byte Stream','https://7e.systemsapproach.org/reliable.html','TCP connections, acknowledgment, retransmission, and flow control.'),
 'congestion':('Systems Approach, Chapter 13: Congestion Control','https://7e.systemsapproach.org/congestion.html','How senders respond to shared network capacity.'),
 'tls':('Systems Approach, Chapter 14: Secure Channels','https://7e.systemsapproach.org/secure.html','Encryption, authentication, certificates, and TLS.'),
 'rpc':('Systems Approach, Chapter 15: Message Transactions','https://7e.systemsapproach.org/message.html','RPC, duplicate requests, and gRPC.'),
 'http':('RFC 9110: HTTP Semantics','https://www.rfc-editor.org/rfc/rfc9110.html','Methods, status codes, intermediaries, and idempotence; see §§9, 10.2.3, and 15.'),
 'http3':('RFC 9114: HTTP/3','https://www.rfc-editor.org/rfc/rfc9114.html','HTTP over QUIC and independent streams.'),
 'dns6':('RFC 3596: DNS extensions for IPv6','https://www.rfc-editor.org/rfc/rfc3596.html','AAAA records and the independence of record type from query transport.'),
 'limits':('RFC 6585: Additional HTTP status codes','https://www.rfc-editor.org/rfc/rfc6585.html','The meaning and scope of HTTP 429; see §4.'),
 'cors':('WHATWG Fetch: CORS protocol','https://fetch.spec.whatwg.org/#http-cors-protocol','Browser cross-origin access to responses.'),
 'sse':('WHATWG HTML: Server-sent events','https://html.spec.whatwg.org/multipage/server-sent-events.html','Event-stream framing; endpoint completion semantics remain application-specific.'),
 'curl':('curl manual','https://curl.se/docs/manpage.html','Command options, timeout behavior, exit codes, and timing fields.'),
 'vpc':('Amazon VPC: How it works','https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html','Subnets, route tables, gateways, and network access.'),
 'sg':('Amazon VPC: Security groups','https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html','Stateful allow rules for resources.'),
 'nat':('Amazon VPC: NAT gateways','https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html','Outbound address translation and return traffic.'),
 'docker':('Docker Engine: Networking','https://docs.docker.com/engine/network/','Network namespaces, container names, and user-defined networks.'),
 'ports':('Docker Engine: Port publishing','https://docs.docker.com/engine/network/port-publishing/','Host-to-container port mappings and binding addresses.'),
 'k8s':('Kubernetes: Services','https://kubernetes.io/docs/concepts/services-networking/service/','Service discovery, stable frontends, and backend endpoints.'),
 'k8sdns':('Kubernetes: DNS for Services and Pods','https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/','Namespace-sensitive names and cluster DNS.'),
 'policy':('Kubernetes: Network Policies','https://kubernetes.io/docs/concepts/services-networking/network-policies/','Ingress/egress isolation and the need for an enforcing network plugin.'),
 'otel':('OpenTelemetry: Traces','https://opentelemetry.io/docs/concepts/signals/traces/','Spans and propagated trace context.'),
 'python':('Python: http.server','https://docs.python.org/3/library/http.server.html','The standard-library server used by the local teaching lab.'),
 'nccl':('NVIDIA: NCCL overview','https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html','Collective communication within and between GPU nodes.'),
})
LESSONS = []
def add(n, slug, module, title, lede, body, sources, keywords=''):
    LESSONS.append(dict(n=f'{n:02}',slug=slug,path=f'pages/{n:02}-{slug}.html',module=module,title=title,lede=lede,body=body,sources=sources,kw=keywords))
def h(id,title): return f'<h2 id="{id}">{title}</h2>'
def p(text): return f'<p>{text}</p>'
def box(label,text,kind='keyidea'): return f'<div class="{kind}"><span class="label">{label}</span><p>{text}</p></div>'
def code(text): return '<pre><code>'+escape(text)+'</code></pre>'
def diagram(text,caption=''): return '<figure><div class="diagram">'+escape(text)+'</div><figcaption>'+caption+'</figcaption></figure>'
def table(headers,rows): return '<div class="table-scroll"><table><thead><tr>'+''.join('<th scope="col">'+v+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def check(q,a): return '<div class="exercise"><span class="label">Check your understanding</span><p>'+q+'</p><details><summary>Reveal the reasoning</summary><p>'+a+'</p></details></div>'
def term(slug,text=None): return f'<a class="term" data-g="{slug}" href="../glossary.html#{slug}">{text or slug}</a>'
def cite(key): return f'<a class="cite" href="{SOURCES[key][1]}">[{key}]</a>'

add(0,'orientation',0,'What networking competence looks like',
    'You are learning to reason about the infrastructure around an evaluation: where a request goes, what can fail, what to measure, and how to explain a design. No networking background is assumed.',
    h('the-job','The job this course prepares you for')+
    p('An evaluation can involve a laptop, a fleet of workers, a model provider, a grading service, a database, and a sandbox that lets an agent use tools. Each connection introduces time, cost, permissions, and ways to fail. Your score depends on that infrastructure behaving as intended. A dropped request is an observation about the run; it is not automatically evidence that a model lacks a capability.')+
    p('The useful professional standard is concrete: draw the request path, explain the role of each component, distinguish evidence from a hypothesis, and propose a bounded experiment. You do not need to configure an Internet backbone to do these things. You do need to know what a route, a port, a timeout, and a proxy mean.')+
    box('The recurring example','We are evaluating 10,000 prompts against a model API. Workers read a dataset, send requests, preserve the responses and timing, and hand completed attempts to a grader. Some attempts will fail. Our job is to make those failures explainable.')+
    h('three-skills','Three abilities to build')+
    table(['Ability','A useful demonstration'],[
      ['Discuss','Explain why “DNS works” does not establish that a model endpoint is reachable.'],
      ['Navigate','Investigate a request from inside the worker’s environment, identify the last successful stage, and bring relevant logs.'],
      ['Design','Choose where workers run, how they reach dependencies, how concurrency is bounded, and how interrupted attempts are recorded.']])+
    h('how-to-study','How to use the course')+
    p('Read the lessons in order the first time. Each introduces a small set of terms, uses them in an eval scenario, and ends with a question whose answer you can reveal. Say your answer out loud before opening it. Follow the glossary links whenever a noun is unfamiliar; needing a definition is part of learning.')+
    p('Work the local service lab after the diagnostic lessons. It requires Python 3 and curl, but no cloud account, model API key, Docker installation, or paid service. The course pages themselves open directly from disk. External reading links need an Internet connection; all of the explanations and local experiments are included here.')+
    h('depth','Where to go deep, and where to recognize the idea')+
    table(['Learn to use','Learn to recognize','Save for a specialized role'],[
      ['DNS, HTTP status and headers, TLS identity, ports, curl, deadlines, retries, concurrency, trace IDs','CIDR, NAT, routing, load balancing, Kubernetes Services, IPv6, QUIC, GPU interconnects','BGP policy configuration, Ethernet switching internals, congestion-control proofs, RDMA tuning']])+
    p('The book you supplied, <em>Computer Networks: A Systems Approach</em>, is the foundation for the underlying concepts. This course follows a request through the system rather than following every book chapter. Official protocol and infrastructure documentation supplies the implementation details. The annotated bibliography separates those sources from the course’s own design exercises.')+
    box('A realistic finish line','This is a networking component of professional preparation, not a promise of employment. The final review asks you to explain and defend an eval design, reproduce a failure, and keep infrastructure outcomes separate from model outcomes. Those are observable skills you can demonstrate.', 'callout')+
    check('A benchmark score falls after moving workers from your laptop into a cloud network. What would you establish before blaming the model?', 'Check whether the same examples produced complete responses under the same request settings. Compare infrastructure failures, deadlines, retries, region, concurrency, and scoring policy. A deployment change can alter which examples finish and therefore which examples reach the grader.'),
    ['foundation'],'beginner employable professional readiness learning path')

add(1,'request-journey',1,'Follow an eval request',
 'A method call in your program can set a chain of machines in motion. Start by making that hidden chain visible.',
 h('actors','Programs, machines, and messages')+
 p('A <strong>host</strong> is a computer participating in a network, such as your laptop or a cloud virtual machine. A <strong>process</strong> is a running instance of a program on that host. For this example, imagine a Python program on a cloud virtual machine that reads a test prompt, sends it to a model API, and saves the answer. That running program is our <strong>eval worker</strong>; the virtual machine is its host.')+
 table(['Term','Meaning in this course'],[
 ['Eval harness','The software that organizes an evaluation: loading test cases, configuring runs, assigning work, collecting results, and arranging scoring. It can be a single program or a system with many workers.'],
 ['Eval worker','The part of the eval harness that executes assigned test cases. In this example it is one Python process that sends prompts and records responses, timing, and failures.'],
 ['Agent','A model-driven system that can choose actions, use tools, and use their results to continue a task. In an agent evaluation, this is the system being tested; the worker starts or drives a test task and records what happens. A simple prompt-and-answer eval needs no agent loop.'],
 ['Model gateway','An intermediary service that accepts model API requests and forwards them to a suitable model-serving service. It may check API keys, enforce rate limits, or select a backend. Here it is an API gateway for model calls; it does not itself run the model.'],
 ['Inference backend','The service behind the gateway that runs the trained model to generate output. “Inference service” and “model server” refer to this same role in our example.']])+
 p('The word <em>harness</em> needs context. An <strong>agent harness</strong> is the code around a model that manages the action loop, tool execution, and task state. An <strong>eval harness</strong> runs and measures tests of a model or agent. A worker may run an agent harness in its own process or control one running elsewhere. These responsibilities do not require one process or machine each.')+
 h('client-server','Client and server describe each exchange')+
 p('For the HTTP API calls in this example, a <strong>client</strong> sends a request for work and receives the response. A <strong>server</strong> accepts the request and sends a response. <strong>Both sides send and receive data.</strong> A server returning an answer, including streaming it in pieces, is still acting as the server. The roles describe who requests the work and who serves that request, not a one-way flow of data. The same program can serve requests on one connection while making requests on another.'+cite('http'))+
 diagram('Requests:   eval worker → model gateway → inference backend\nResponses:  eval worker ← model gateway ← inference backend','One possible deployment, with two separate request/response exchanges. The gateway is optional; a worker can also call a model server directly.')+
 table(['Exchange','Client','Server'],[
 ['Worker asks the gateway to generate an answer','Eval worker','Model gateway'],
 ['Gateway asks the backend to perform generation','Model gateway','Inference backend']])+
 p('The worker and backend therefore communicate <em>through the gateway</em> in this example. The worker receives the gateway’s response, which carries output obtained from the backend. If the worker calls the backend directly instead, the worker is the client and the backend is the server. If a backend makes a separate request to a worker’s callback endpoint, the backend is a client and the worker is a server for that separate exchange. Simply returning the model’s answer does not reverse their roles.')+
 check('The backend streams generated text to the gateway, which streams it to the worker. Has the worker become a server?', 'No. Those messages are responses to requests already made. The worker remains the client of the gateway, and the gateway remains the client of the backend. To identify the roles, ask who requests work on each connection, not who is currently sending bytes.')+
 h('packets','Messages travel in packets')+
 p('A network moves data between hosts over links. It breaks large transfers into manageable pieces called <strong>packets</strong>. Devices forward those pieces toward their destinations. Sending a million-byte prompt does not create one giant indivisible Internet message. Your software sees a higher-level abstraction built over many transfers.'+cite('foundation'))+
 h('stages','The request has stages')+
 table(['Stage','What it contributes','A distinct failure'],[
 ['Resolve a name','DNS helps find an address for the API hostname.','The worker cannot resolve the name.'],
 ['Reach an endpoint','IP routing and a transport connection get traffic to a listening service.','The connection is refused or times out.'],
 ['Establish a secure channel','TLS checks the server identity and protects the connection.','Certificate validation fails.'],
 ['Exchange an API message','HTTP carries a method, path, headers, and body.','The gateway returns 401 or 429.'],
 ['Complete application work','The service generates and returns an answer.','The stream ends before the documented completion signal.'],
 ['Record the outcome','The worker persists an attempt and its result.','The answer arrives but storing it fails.']])+
 p('This order is a teaching model for a new HTTPS connection using TCP. DNS answers and connections can be reused; proxies add stages; HTTP/3 uses QUIC. You will learn these variations after the basic path is familiar. The essential habit survives every variation: identify which component was responsible for the next step.')+
 h('layers','Why engineers talk about layers')+
 p('A <strong>protocol</strong> is an agreement about messages and behavior. HTTP describes requests and responses. TCP supplies an ordered byte stream. IP addresses and forwards packets. Ethernet or Wi-Fi carries traffic over a local link. Each protocol can add its own header around data from the layer above; that wrapping is <strong>encapsulation</strong>. The receiver interprets and removes the wrappers in reverse order.'+cite('foundation'))+
 diagram('Application       HTTP request / response\nSecure channel    TLS records\nTransport         TCP segments\nInternet          IP packets\nLocal link        Ethernet or Wi-Fi frames','A common HTTPS stack, simplified. Packet and application-message boundaries need not align.')+
 p('The seven-layer OSI vocabulary appears in infrastructure discussions. “Layer 3” usually concerns IP routing; “Layer 4” concerns transport addresses and ports; “Layer 7” concerns application messages such as HTTP. Treat these as clues to what a device inspects. Memorizing a seven-word list does not tell you why a request failed.')+
 box('For an eval review','For every arrow in a design, ask: who initiates it, what name and port are used, what identity is checked, what deadline applies, and where the outcome is recorded? These questions turn an attractive diagram into an operational description.')+
 check('Your worker receives HTTP 401. Which early stages probably succeeded, and what is still uncertain?', 'It reached an HTTP-speaking component. If HTTPS certificate verification was enabled and succeeded, it also established TLS to that component. The model backend may never have seen the request: a gateway could have rejected authentication. Investigate credentials, endpoint, and response provenance before blaming routing.'),
 ['foundation','apps','http'],'layers packets host client server protocol request journey OSI eval worker harness agent model gateway inference backend')

add(2,'addresses-and-ports',1,'Addresses, ports, and localhost',
 'An address tells the system where to send traffic; a port helps it deliver traffic to the right service. The meaning of “here” is just as important.',
 h('url','Read an endpoint carefully')+
 code('https://models.example.test:8443/v1/evaluate?stream=true\n└scheme └──── hostname ────┘└port┘└── path ─┘└─ query ─┘')+
 p('This is a fictional endpoint, not a working service. The hostname is a name to resolve. An IP address identifies a network interface or a logical destination in some routing context. A <strong>port</strong> is a transport-level number used to distinguish communication endpoints. TCP port 443 is conventionally used for HTTPS; the URL above explicitly selects 8443. A path such as <code>/v1/evaluate</code> is interpreted by the HTTP service after the connection reaches it.')+
 p('Your operating system gives a client connection a source port, typically from an ephemeral range. A TCP connection is distinguished by source address, source port, destination address, and destination port. Add the transport protocol and you have the common <strong>five-tuple</strong>. Thousands of clients can connect to one destination port because their complete tuples differ.'+cite('tcp'))+
 h('listen','A server must listen')+
 p('A running process does not automatically accept network connections. It must bind an address and port and listen. Binding to <code>127.0.0.1:8000</code> limits this listener to IPv4 loopback in its network environment. Binding to <code>0.0.0.0:8000</code> means listening on all local IPv4 interfaces. It does not, by itself, create a route, publish a container port, or grant firewall access.')+
 table(['Notation','Meaning','What to avoid assuming'],[
 ['127.0.0.1','IPv4 loopback: this network environment.','It is not the host of whichever service you had in mind.'],
 ['::1','IPv6 loopback.','An IPv4-only listener need not accept it.'],
 ['0.0.0.0 (bind address)','All local IPv4 interfaces for a listener.','It is not a remote server address to distribute to clients.'],
 ['10.20.1.8','An example private IPv4 address.','Your laptop needs a route into that private network.'],
 ['443/tcp','A TCP port, conventionally HTTPS.','A port number does not prove which protocol is actually running.']])+
 h('context','Localhost is a point of view')+
 p('On your laptop, <code>localhost</code> normally resolves to loopback addresses. Inside a container, it ordinarily means that container’s network namespace. Inside a Kubernetes Pod, containers share the Pod’s network namespace, so localhost can reach another container in the same Pod. It does not mean another Pod or your laptop. Network namespaces create separate views of interfaces, routes, and sockets; you will revisit them in the container lesson.')+
 box('A common deployment failure','A worker runs in one container, but its model URL is <code>http://localhost:8000</code>. The model server runs in a different container. The URL points back at the worker’s own environment. Use the appropriate service name and port on a shared network. Increasing the timeout does not fix the destination.', 'pitfall')+
 h('observe','First local observation')+
 p('Later the lab will start a server bound to <code>127.0.0.1:8765</code>. You will run <code>curl http://127.0.0.1:8765/ok</code> and inspect the response. The address, port, and path each have a separate job. If the service uses plain HTTP, asking curl for HTTPS on that port attempts the wrong protocol even though the address and port are correct.')+
 check('A server listens on 127.0.0.1:8000 inside a container. You publish the container’s port 8000 to a host port. Why might the host still fail to connect?', 'The forwarded connection generally arrives through a container interface, while the process listens only on the container’s loopback interface. The process must listen on an appropriate container interface, often 0.0.0.0, and the host mapping and network policy must also permit the path.'),
 ['tcp','docker','ports'],'localhost loopback IPv4 IPv6 socket bind listener port URL five tuple')

add(3,'ip-and-routing',1,'IP, subnets, and routes',
 'Learn to read an address range and a route table. That is enough to ask useful questions about where a worker can send traffic.',
 h('prefix','A subnet is an address range')+
 p('IPv4 addresses contain 32 bits, commonly written as four decimal numbers. A <strong>CIDR prefix</strong>, such as <code>10.20.1.0/24</code>, says the first 24 bits identify the range. That leaves eight bits, or 256 possible addresses, from <code>10.20.1.0</code> through <code>10.20.1.255</code>. The number available for machines depends on the network and provider’s reservations. Do not automatically promise 256 hosts.')+
 p('A smaller prefix length describes a larger range: <code>10.20.0.0/16</code> contains <code>10.20.1.0/24</code>. The common private IPv4 ranges are <code>10.0.0.0/8</code>, <code>172.16.0.0/12</code>, and <code>192.168.0.0/16</code>. They can be reused in separate networks and are not ordinary globally routable Internet destinations. “Private” describes addressing, not encryption or authorization.'+cite('ip'))+
 h('forwarding','Routes choose a next step')+
 p('A route table maps destination prefixes to next hops or interfaces. The usual IP forwarding rule chooses the matching route with the longest prefix: the most specific match. A default route, <code>0.0.0.0/0</code>, matches every IPv4 address and handles destinations with no more specific match. Routers make forwarding decisions hop by hop; your worker does not need a list of every router on the Internet.')+
 table(['Destination','Next step in this hypothetical network'],[
 ['10.20.1.0/24','Local interface'],['10.20.0.0/16','Internal router'],['0.0.0.0/0','Default gateway']])+
 p('A packet for <code>10.20.1.9</code> matches all three entries; the /24 wins. A packet for <code>10.20.2.9</code> uses the /16. A public model endpoint uses the default route. This table is a simplified teaching example: a real operating system can also use policy routing and multiple tables.')+
 h('links','A route still needs a local delivery mechanism')+
 p('On an Ethernet LAN, devices use link-layer addresses to send frames over the next local segment. ARP helps map a directly reachable IPv4 address to a link-layer address. When a destination is remote, the host generally sends the frame toward its next-hop router, not directly to the remote server’s Ethernet address. Switches move frames within a link-layer network; routers forward IP traffic across networks. Hardware can combine these roles.'+cite('links'))+
 h('link-and-frame','What a local link and a frame actually do')+
 p('A <strong>link</strong> is an immediate connection, such as a cable between devices or a Wi-Fi connection to an access point. Several links joined by a switch or access point can form one <strong>local network</strong>. “Local” means reachable within that link-layer network without an IP router forwarding between address ranges; it does not mean the entire Internet. A radio signal or cable has limited physical reach, so a sender needs a way to address the receiver on the current part of the trip.')+
 p('<strong>Layer 2</strong> is this local delivery job. Ethernet and Wi-Fi send <strong>frames</strong>, which can carry <strong>Layer 3</strong> IP packets inside them. The IP packet identifies its intended destination across networks; the frame identifies the receiver for this local part of the journey. On Ethernet, the frame uses <strong>MAC addresses</strong>—Media Access Control addresses—of network interfaces. MAC has nothing to do with Apple Mac computers; a MacBook, a Windows laptop, and a router can all have MAC addresses. Wi-Fi frames may carry extra access-point address fields beyond this simplified Ethernet view.')+
 p('Frames also include information that lets a receiver detect some transmission errors. If a frame is damaged, the receiver can discard it. That check alone does not promise delivery. Each link has its own framing, so a router can remove one frame, inspect the IP packet, and place the packet in a new frame addressed to the next local receiver. The packet is the continuing delivery request; the frame is the wrapper for one part of its path.')+
 h('two-network-trip','Follow a request and its reply across two networks')+
 diagram('Laptop 192.168.10.20   ← Network A →   Router   ← Network B →   Wiki server 192.168.20.30\n                                       192.168.10.1   192.168.20.1','The router participates in both local networks. A wiki server means a computer running software that serves wiki pages; it need not be a dedicated machine.')+
 p('Assume Network A is <code>192.168.10.0/24</code> and Network B is <code>192.168.20.0/24</code>. The <code>/24</code> matters: in these examples, the first three decimal numbers identify the address range. An IP address alone does not tell the router the range; its interface settings also specify the prefix length. “Directly connected” means the router has an interface on each of these two local networks, not that it has a direct link to every router on Earth.')+
 table(['Destination in this router’s table','Next step'],[
 ['192.168.10.0/24','Use the Network A interface, addressed 192.168.10.1'],
 ['192.168.20.0/24','Use the Network B interface, addressed 192.168.20.1']])+
 p('A <strong>routing table</strong> is this collection of destination-range-to-next-step rules. The router learns these two rules from its configured, directly connected interfaces. Other routes could be configured or learned from other routers. It checks the destination <em>IP address</em> against the table, using the prefix length to find a match. A routing table describes forwarding; it is not a list of every device on Earth.')+
 p('The laptop sees that <code>192.168.20.30</code> is outside its own <code>192.168.10.0/24</code>, so it sends the packet to its <strong>default gateway</strong>, <code>192.168.10.1</code>. The gateway is the nearby router used for destinations outside the laptop’s local network. ARP can find that router interface’s MAC address; the first frame goes toward the router, while the IP packet inside it still names the wiki server. The router matches <code>192.168.20.0/24</code>, learns the server’s local MAC address, and sends a new frame on Network B. On the way back, the wiki server sees that the laptop is outside <code>192.168.20.0/24</code>. It sends its reply through <em>its</em> gateway, <code>192.168.20.1</code>; the router matches <code>192.168.10.0/24</code> and forwards the reply to the laptop.')+
 h('multiple-routers','Three ways to connect multiple routers')+
 table(['Arrangement','How the laptop reaches the wiki'],[
 ['One shared local network','Two access points can connect to one local network. The laptop and wiki could be 192.168.10.20 and 192.168.10.30; local frames reach the server without routing between IP networks.'],
 ['Ordinary routed networks','The laptop and wiki occupy the two /24 networks above. A router uses its routing table to forward between them; additional routers would need routes too.'],
 ['Lightning Mesh','The laptop could be 10.42.1.20 behind Router A and the wiki 10.42.2.30 behind Router B. Each router serves devices from its own /24; the routers learn routes to each other’s ranges and can also share names such as wiki.mesh.']])+
 p('The first arrangement can use ordinary Ethernet access points or a conventional Wi-Fi mesh. Layer 3 routing is ordinary networking too. Lightning Mesh’s particular design gives each router’s clients a separate network and coordinates those networks without requiring one central router to hold every local route. The laptop still uses Router A as its gateway. A router offering a route to the public Internet is an <strong>Internet gateway</strong>, a more specific role; Router B does not need to provide Internet access merely to host the wiki.')+
 p('The shared local network is also one <strong>broadcast domain</strong>: a local broadcast message can reach all its devices. Lightning Mesh keeps each router’s broadcast domain for connected devices separate and routes packets between them. A shared Wi-Fi name can make moving between access points convenient, but it does not alone guarantee that a phone retains its IP address or that an ongoing call survives the move. <strong>LAN</strong> means local area network; <strong>WAN</strong> means wide area network, often the upstream Internet-facing side of a household router.')+
 p('In Lightning Mesh, the boxes run <strong>OpenWrt</strong>, a Linux-based router operating system. Linux’s <strong>kernel</strong> performs the packet forwarding; a <strong>daemon</strong> is a background program. The <code>mjolnir-meshd</code> daemon coordinates the mesh, while <code>babeld</code> runs <strong>Babel</strong>, a routing protocol that updates paths between router-owned networks. Phones join the Wi-Fi <strong>SSID</strong> (network name) intended for them; routers can use a separate <strong>802.11s backhaul</strong> (router-to-router Wi-Fi). <code>dnsmasq</code> helps hand devices addresses through DHCP and answer name-lookup questions; Lightning Mesh’s <code>.mesh</code> service names come from its shared directory.')+
 p('Here <strong>DHCP</strong> means Dynamic Host Configuration Protocol, which gives a joining device an address and gateway setting. <strong><a class="term" data-g="dns" href="../glossary.html#dns">DNS</a></strong> means Domain Name System, which helps turn a name into an address. <strong>SSID</strong> means Service Set Identifier, the advertised Wi-Fi network name. <strong>802.11s</strong> is the Wi-Fi standard for mesh links between the routers. OpenWrt keeps settings in <strong>UCI</strong> (Unified Configuration Interface), and <code>procd</code> starts and supervises daemons. Operators can use <strong>SSH</strong> (Secure Shell) to log into a router; <code>mjolnir-hello</code> serves the <code>hello.mesh</code> front desk. These programs configure the network, while the Linux kernel forwards ordinary packets according to the routes.')+
 p('The routers spread directory and subnet-ownership updates by <strong>gossip</strong>: peers pass updates onward. A <strong>CRDT</strong> is a shared data structure with rules for merging copies after updates arrive in different orders. Babel handles forwarding routes, while the shared records coordinate ownership and discovery. Across distant sites, <strong>Iroh</strong> can carry encrypted connections over existing Internet access. This is an <strong>overlay</strong>, a logical network carried over another network; Linux exposes its packet path to software through a virtual <strong>TUN interface</strong>. Distant sites still need some underlying connectivity. This is a case study of one implementation, described in the <a href="https://github.com/WorldTreeNetwork/lightning-mesh/blob/main/ARCHITECTURE.md">Lightning Mesh architecture</a>.')+
 p('Iroh uses <strong>QUIC</strong>, an encrypted transport built over UDP, to connect router identities. <strong><a class="term" data-g="nat" href="../glossary.html#nat">NAT</a> traversal</strong> means attempting to connect through the address translation commonly used at Internet gateways. If a direct connection is unavailable, a <strong>relay</strong> may pass the encrypted traffic between sites. Local traffic between neighboring routers can use the local backhaul without taking this Internet path.')+
 h('nat','Address translation and IPv6')+
 p('<strong>NAT</strong> rewrites addressing information. A common outbound configuration maps many private connections onto public addresses and ports, then uses that mapping to deliver replies. NAT is not the same as a firewall, although devices often perform both jobs. A successful outbound connection does not imply that arbitrary inbound connections can be initiated from the Internet.')+
 p('IPv6 uses 128-bit addresses and its own routing and neighbor-discovery mechanisms. A hostname may have both IPv4 and IPv6 answers, while only one path works in a particular environment. When troubleshooting, note which address family the client selected. The goal here is to recognize that two addresses for the same hostname can represent two different network paths.')+
 box('In an infrastructure discussion','Ask which subnet the worker occupies, which route covers the destination, how outbound traffic leaves, and whether any connected networks overlap in address space. Overlapping private prefixes can make an intended remote destination look local.')+
 check('Does adding a default route guarantee that a private worker can reach a public HTTPS endpoint?', 'No. The next hop must provide a working outbound path; the return path, source addressing or translation, DNS, security controls, and the destination listener must also work. A route is a forwarding decision, not an end-to-end success guarantee.'),
 ['ip','routing','links'],'CIDR subnet mask routing private public gateway NAT IPv6 ARP switch MTU')

add(4,'dns',2,'DNS: names, answers, and context',
 'DNS helps a program turn a name into information it can use to connect. A correct answer is one step toward a working request.',
 h('resolution','What resolution actually means')+
 p('A client asks a <strong>resolver</strong> for records associated with a name. A recursive resolver can consult other DNS servers and cache results. Authoritative servers publish records for their zones. The client usually does not visit every part of that hierarchy itself. A local cache, an operating-system configuration, a container resolver, or a corporate VPN can all affect the answer.'+cite('dns'))+
 table(['Record or response','What it tells you'],[
 ['A','An IPv4 address associated with a name.'],['AAAA','An IPv6 address associated with a name.'],['CNAME','An alias to another DNS name.'],['TTL','A lifetime used for caching a record; it is not a connection timeout.'],['NXDOMAIN','The queried name does not exist according to this DNS response.'],['SERVFAIL','The DNS server could not successfully answer; the name is not thereby proven nonexistent.']])+
 p('Caching explains why two workers can temporarily use different answers after a change. Also distinguish DNS caching from connection reuse: an existing connection can remain attached to an old backend even after a DNS record changes. Lowering a TTL does not forcibly reconnect clients or evict previously cached records immediately.')+
 h('where','Resolve from the environment that fails')+
 p('Suppose your laptop resolves <code>model.internal</code>, but a CI worker does not. The laptop may be using a VPN resolver with a private zone. A public resolver does not necessarily know that zone. The useful question is which resolver the failing process uses and whether it can reach it. Asking an unrelated public DNS server can test a different system.')+
 code('dig example.com A\ndig example.com AAAA\npython3 -c \'import socket; print(socket.getaddrinfo("example.com", 443))\'')+
 p('These commands make live DNS queries, so outputs vary. <code>dig</code> may need installation on some systems. Python’s lookup follows the operating system’s name-resolution interfaces; it can differ from a direct DNS query because of hosts files and local resolver behavior. Inspect the DNS status and answer section, not just whether the command printed text.')+
 h('separate','Separate name resolution from connectivity')+
 p('If a hostname resolves to an address but HTTPS fails, DNS has supplied a candidate destination; routing, connections, TLS, or HTTP may still fail. Conversely, substituting an IP directly into an HTTPS URL changes the requested identity. A certificate for a hostname need not cover that address.')+
 p('For a controlled diagnostic on a known endpoint, curl’s <code>--resolve hostname:port:address</code> supplies an address while preserving the URL hostname for HTTP and TLS. Obtain the address from an approved source and record the override. It is a way to isolate name resolution, not a permanent hard-coded fix. See the command appendix for an example.'+cite('curl'))+
 box('Common mistake','“DNS propagated” is too vague for an incident report. Say which name, record type, resolver, environment, time, and answer you observed. A private DNS view and a public DNS view can intentionally disagree.', 'pitfall')+
 check('The service moved to a new address ten minutes ago, but one long-running worker keeps hitting the old backend. Must its DNS cache be broken?', 'No. It may be reusing an already-open connection and therefore not performing a new lookup. Check connection lifetime as well as cached DNS records, TTLs, and any intermediate proxy’s resolution behavior.'),
    ['dns','dns6','curl'],'DNS resolver cache TTL A AAAA CNAME NXDOMAIN SERVFAIL VPN split horizon')

add(5,'transport',2,'TCP, UDP, and QUIC',
 'A transport protocol gives programs a way to exchange data. Knowing its promise helps you understand what it cannot guarantee.',
 h('tcp','TCP provides an ordered byte stream')+
 p('TCP tracks sequence numbers, acknowledges received data, and retransmits when necessary. If a connection succeeds, the receiving application reads an ordered stream of bytes rather than a bag of out-of-order packets. TCP does not preserve your application’s write boundaries: a JSON message can arrive across several reads, and one read can contain parts of multiple messages.'+cite('tcp'))+
 diagram('client                                  server\n  SYN  ──────────────────────────────────→\n       ←──────────────────────── SYN + ACK\n  ACK  ──────────────────────────────────→\n       application bytes can flow','A simplified TCP connection handshake. It does not show the later TLS handshake.')+
 p('The initial handshake takes time. Reusing a connection through a client pool can avoid repeating connection establishment and, for HTTPS, much of the security setup. A pool holds reusable connections with finite capacity and lifetimes. Waiting for a free pool slot is client-side waiting, not necessarily slow server processing.')+
 h('limits','Reliable transport has limits')+
 p('A TCP acknowledgment says something about bytes reaching the receiving TCP implementation. It does not certify that your inference finished, that a database committed, or that a response was stored. A broken connection can leave the client uncertain whether the server completed a request. That uncertainty is the reason retry design is an application concern.')+
 p('<strong>Flow control</strong> protects the receiver from receiving more data than it can buffer. <strong>Congestion control</strong> adjusts sending to the network’s shared capacity. Neither is your provider’s requests-per-minute quota. Raising an API concurrency limit is not the same action as changing a TCP window.'+cite('congestion'))+
 h('udp','UDP and QUIC')+
 p('UDP supplies datagrams with relatively little transport machinery. It does not itself guarantee delivery, ordering, or retransmission. Applications can build those functions above it. DNS frequently uses UDP, but also uses TCP and encrypted transports; blocking TCP DNS merely because “DNS uses UDP” is a poor assumption.')+
 p('QUIC runs over UDP and supplies reliable streams, congestion control, and integrated TLS-based security. HTTP/3 uses QUIC. Independent QUIC streams avoid making one stream’s missing data hold up delivery on another stream in the same way that a shared TCP byte stream can. Shared bandwidth and connection-level resources still matter. HTTP/3 is therefore not “unreliable HTTP.”'+cite('http3'))+
 h('symptoms','Read transport symptoms carefully')+
 table(['Symptom','Reasonable interpretation'],[
 ['Connection refused','An active rejection arrived; a missing listener is one possibility. Check the address, port, and rejecting component.'],
 ['Connect timeout','The connection did not become usable within the limit. Packet drops, routing, filtering, or overload are candidates.'],
 ['Connection reset','A connection was abruptly terminated by a peer or intermediary. Look for server/proxy events and request state.'],
 ['Pool timeout','The client could not obtain a usable connection slot in time. Inspect pool limits and unreleased responses.']])+
 check('A TCP connection is reliable, so can you automatically retry any model POST after its connection resets?', 'No. The server may have accepted and performed the request before the response was lost. A retry can duplicate work or charges and can produce a different sample. You need an explicit attempt policy and any documented server-side idempotency support.'),
 ['tcp','congestion','http3'],'TCP UDP QUIC sockets handshake pool connection reset refusal retransmission flow congestion')

add(6,'tls',2,'TLS: encryption and identity',
 'HTTPS protects a connection and helps authenticate the server. It does not replace API authorization or define who can read data after termination.',
 h('promise','What TLS contributes')+
 p('TLS establishes cryptographic keys, protects data against eavesdropping and tampering in transit, and ordinarily lets the client authenticate the server. A certificate binds an identity to a public key under a trust system. A normal HTTPS client checks that the certificate is valid for the URL hostname, within its validity period, and chains to a trusted authority.'+cite('tls'))+
 p('These checks are distinct from sending an API key. TLS can succeed and HTTP authorization can fail. Conversely, a valid API key does not repair a certificate mismatch. In mutual TLS, the server also authenticates a client certificate; that is another identity mechanism, not an automatic feature of every HTTPS connection.')+
 h('name','Why the hostname matters')+
 p('Multiple services can share an IP address. Server Name Indication, or SNI, lets a TLS client indicate the intended hostname during connection setup. The later HTTP request also identifies its target authority. Simply replacing <code>https://api.example.test</code> with an IP address can change both certificate validation and virtual hosting behavior. Preserve the hostname when you are isolating a DNS issue.')+
 table(['Failure','A productive first check'],[
 ['Hostname mismatch','Is the URL correct, and is this the intended gateway or proxy?'],
 ['Unknown certificate authority','Does this environment have the required trust store or approved corporate CA?'],
 ['Expired / not yet valid','Check the certificate dates and the client clock.'],
 ['Handshake fails before HTTP','Check TLS compatibility, the listening protocol, SNI, and any intermediary.']])+
 p('A browser, curl, and a language runtime can use different trust stores and proxy settings. “It works in my browser” does not prove the worker is configured the same way. Identify the actual executable and environment that fails. Verbose diagnostic output can include sensitive headers; use a credential-free endpoint when possible and redact before sharing logs.')+
 h('boundaries','TLS termination defines a boundary')+
 diagram('worker ══ TLS connection 1 ══ gateway ══ TLS connection 2 ══ model\n                                  ↑\n                         plaintext available here','Two encrypted connections are two trust relationships. The gateway can inspect data at termination.')+
 p('A load balancer may terminate client TLS, read HTTP, and create a new connection to a backend. Ask whether that second hop is also encrypted and authenticated. A private subnet alone does not encrypt it. A network diagram labeled “HTTPS” on only the external arrow leaves an important part of the design unspecified.')+
 box('Avoid making the test meaningless','Disabling verification with <code>curl -k</code> removes certificate checks and can conceal a wrong destination or trust problem. Keep verification enabled in the normal path. Diagnose the URL, chain, hostname, and trust configuration instead of copying an insecure workaround into the runner.', 'pitfall')+
 check('Your TLS handshake succeeds, but the gateway returns HTTP 403. Should you change the certificate configuration first?', 'No. Successful verified TLS establishes a secure connection to that endpoint. A 403 concerns refusal to fulfill the HTTP request and can come from application authorization or gateway policy. Inspect the responder, credentials, account/project permissions, and policy evidence.'),
 ['tls','http','curl'],'TLS HTTPS SSL certificates SNI mTLS trust CA encryption authentication authorization')

add(7,'http',2,'HTTP: read the actual exchange',
 'An SDK wraps HTTP messages. When something goes wrong, being able to read the method, URL, headers, status, and body makes the wrapper less mysterious.',
 h('message','A request is structured data')+
 code('POST /v1/evaluate HTTP/1.1\nHost: models.example.test\nContent-Type: application/json\nAuthorization: Bearer <redacted>\n\n{"prompt": "Explain DNS", "stream": false}')+
 p('This is a simplified HTTP/1.1 illustration, not a runnable provider request. The method describes an operation, the target identifies a resource, headers carry metadata, and the body carries content. JSON is one possible content format. HTTP/2 uses binary framing and streams, so its wire representation differs while many of these semantics remain.'+cite('http'))+
 p('An API contract adds rules above HTTP: required fields, model identifiers, quotas, response schemas, and completion conditions. An HTTP success status does not certify that the answer is valid for your evaluation. A JSON decoder can fail on a 200 response, and a valid JSON body can contain a task failure.')+
 h('status','Treat status codes as evidence')+
 table(['Response','First investigation'],[
 ['400 / 422','Validate fields and schema using this API’s documentation.'],
 ['401','Check authentication credentials and the intended account or endpoint.'],
 ['403','Inspect authorization or gateway policy; do not assume a transport failure.'],
 ['404','Check the route, resource, model name, and API version.'],
 ['429','Inspect the provider’s limit category, response body, and retry instructions.'],
 ['500 / 503','Locate the responder and inspect a server failure or unavailability.'],
 ['502 / 504','A gateway reports an upstream response problem or timeout. Identify that gateway and its upstream.']])+
 p('These are diagnostic starting points, not a lookup table of proven root causes. Services can return custom error bodies and sometimes misuse status codes. Save the status, a redacted body, relevant headers, and a request ID together. The body may distinguish a quota exhausted for the day from a temporary request-rate limit.')+
 h('tools','Look at headers as well as the body')+
 code('curl -i --connect-timeout 5 --max-time 15 https://example.com/')+
 p('This sends a live GET to a public example site. <code>-i</code> includes response headers; <code>--connect-timeout</code> bounds connection setup; <code>--max-time</code> bounds this transfer. curl normally treats an HTTP 500 as a completed transfer rather than a process error. Use <code>--fail-with-body</code> when you want supported curl versions to return a failing exit code for HTTP errors while preserving the body. Exit status and HTTP status answer different questions.'+cite('curl'))+
 h('api-shapes','Other API shapes you will encounter')+
 p('A REST-style API commonly exposes resource-oriented HTTP endpoints. An RPC interface looks more like calling a remote function. gRPC usually uses HTTP/2 and Protocol Buffers, and communicates an application status that is not captured by checking the HTTP status alone. The debugging habit is the same: understand the protocol’s actual success condition.'+cite('rpc'))+
 p('Browser-based tools also encounter CORS: browser rules governing whether a page can access a cross-origin response. A successful curl call does not establish that browser JavaScript is allowed to read that response. A CORS error is not proof that the server is unreachable, and adding credentials to an arbitrary proxy is not a sound diagnosis.')+
 check('An HTTP request returned 200, but the grader cannot parse the response. Is the sample a successful model answer?', 'Not yet. You have transport/application-protocol evidence, but must validate the API response schema, completion state, and expected answer field. Preserve the raw redacted evidence and classify the failure separately from a correctly parsed answer that the grader judges wrong.'),
    ['http','limits','cors','apps','rpc','curl'],'HTTP REST API status headers JSON 401 403 429 502 504 gRPC CORS')

add(8,'streaming',2,'Streaming and partial responses',
 'Seeing the first token is useful. Knowing whether the response completed is essential for a trustworthy evaluation.',
 h('stream','A stream is still a protocol')+
 p('A non-streaming API commonly returns one completed response body. A streaming API makes pieces available over time. Server-sent events, or SSE, use a text event stream with fields such as <code>data:</code> and blank lines between events. WebSockets provide a different, bidirectional message channel. Neither is the same thing as a TCP packet.'+cite('sse'))+
 code('event: token\ndata: {"text": "Hello"}\n\nevent: done\ndata: {"complete": true}\n\n')+
 p('This is the local lab’s original event format. A real model provider defines its own event schema and terminal signal. Do not assume that every API uses a particular marker. Also do not assume one socket read contains one event: network reads, HTTP frames, SSE events, and model tokens have different boundaries.')+
 h('timing','Measure the experience at several points')+
 table(['Metric','Meaning'],[
 ['Time to first byte','When any response byte arrives; this may be a header or heartbeat.'],
 ['Time to first token','When the client can identify the first generated token/content event. Define exactly what counts.'],
 ['Inter-event gap','Elapsed time between parsed stream events; buffering can change it.'],
 ['Completion latency','When the documented terminal state is received and the response is usable.']])+
 p('First-token latency can include queueing, connection setup, prompt processing, and initial generation. Later generation can dominate total time. Comparing first-token latency in one run to total response latency in another is not a fair comparison. Record your timing boundaries, connection reuse, and any retries.')+
 h('intermediaries','Intermediaries affect what you observe')+
 p('A reverse proxy may buffer data, hold it until a buffer fills, or impose an idle timeout. Your client may buffer printed output too. If a stream appears all at once, investigate where flushing stops. The lab uses <code>curl -N</code> to disable curl’s output buffering. That option cannot force an upstream server or proxy to flush.')+
 p('A stream that begins with HTTP 200 can still be interrupted. Once headers are sent, a later failure may appear as an error event, an incomplete body, or a connection closure rather than a new HTTP error status. EOF is not necessarily a documented successful finish. Store whether the terminal signal was seen and whether parsing completed.')+
 box('An eval policy to write down','For a capability score, an interrupted answer might require an explicit infrastructure-failure classification and a predefined retry policy. For a product reliability eval, interruption may itself count as product failure. State the target metric first; never silently treat a truncated answer as a completed sample.')+
 h('cancellation','Cancellation is a request, not proof')+
 p('If a client closes a stream after its deadline, the remote service might already have generated or billed more work. Some systems propagate cancellation; others do not stop promptly. Track the local outcome separately from any server-reported usage. A retry can create another generation even if the original one is still running.')+
 check('The first token arrives in 0.8 seconds, but no terminal event arrives before your 30-second deadline. What do you record?', 'Record first-token latency, the partial-response state, elapsed time, the deadline exceeded, and the absence of a terminal event. Do not label 0.8 seconds as completion latency. Whether and how you retry follows the evaluation’s policy, with a separate attempt ID.'),
    ['sse','apps','curl'],'SSE streaming TTFT first token partial response buffering WebSocket cancellation')

add(9,'latency-and-throughput',3,'Latency, throughput, and bottlenecks',
 '“The network is slow” is the beginning of a question. Break elapsed time into parts before deciding what to change.',
 h('units','Start with quantities and units')+
 p('<strong>Latency</strong> is elapsed time for a specified operation. <strong>RTT</strong> is the round-trip time for a network exchange. <strong>Bandwidth</strong> is a capacity, commonly in bits per second. <strong>Throughput</strong> is the achieved rate of useful work, such as bytes per second or completed eval samples per minute. Eight bits make one byte: 100 megabits/s is at most 12.5 megabytes/s before overhead, using decimal units.'+cite('foundation'))+
 p('A hypothetical 100 MB file requires at least 8 seconds to serialize through a 100 Mb/s bottleneck. That calculation excludes setup, propagation, contention, protocol overhead, and server delays. A tiny prompt may spend almost no time being transmitted while waiting seconds for model computation. More network bandwidth does not eliminate that computation.')+
 h('budget','Account for the whole request')+
 diagram('sample elapsed time\n  = local queue + pool wait + connection setup (if needed)\n  + request upload + remote queue/compute\n  + response transfer + local validation/storage','A conceptual budget. Some stages overlap, especially during streaming.')+
 p('curl timing fields are cumulative from the start of a transfer. On a simple fresh HTTPS request without redirects or proxies, <code>time_connect − time_namelookup</code> roughly isolates TCP setup; <code>time_appconnect − time_connect</code> roughly isolates TLS setup. Reused connections, redirects, proxies, and different HTTP versions complicate those interpretations. <code>time_starttransfer</code> includes preceding work and server time; it is not a pure network measurement.'+cite('curl'))+
 h('tail','The slow tail changes a batch')+
 p('The median describes a typical observation. The 95th percentile, p95, is a value at or below which roughly 95% of observations fall under your chosen quantile convention. A mean can hide a small but important set of very slow requests. Report the sample count, errors, and timing definition alongside percentiles. A p99 from a handful of requests is not strong evidence about the tail.')+
 p('For an eval, record latency by relevant conditions: prompt/output length, model, region, concurrency, connection reuse, and attempt number. Compare like with like. A run whose longest prompts time out can appear faster if you compute latency only over successful responses.')+
 h('capacity','A useful capacity relationship')+
 p('In a stable system over a suitable observation interval, average in-flight work is approximately throughput multiplied by average time in the system: <code>L = λ × W</code>. The important part is matching boundaries and populations. If you measure completed attempts per second, use attempt latency and attempt concurrency. Do not mix logical samples with retries.')+
 p('For a hypothetical workload with 20 requests/s and a 3-second mean request lifetime, about 60 requests are in flight on average. This is a sizing estimate under stable conditions, not a promise that setting concurrency to 60 produces 20 requests/s. Provider limits, CPU, connection capacity, queueing, and token budgets can prevent it.')+
 box('Try it','The <a href="../appendices/a-calculators.html">network calculators</a> let you vary transfer size, link rate, mean request time, and target throughput. Each result names the assumptions instead of presenting an unconditional performance prediction.','callout')+
 check('After doubling concurrency, throughput barely changes but p95 latency triples. What does that suggest?', 'A constrained resource may already be saturated, so additional work waits rather than finishing faster. Investigate client pools, provider limits, server queues, CPU/GPU capacity, and network bottlenecks. Measure where waiting increases before choosing a fix.'),
 ['foundation','congestion','curl'],'latency throughput bandwidth RTT p50 p95 p99 percentiles Little law bottleneck BDP')

add(10,'concurrency-and-limits',3,'Concurrency, queues, and rate limits',
 'How many requests you start, how many are in flight, and how much work they contain are three different controls.',
 h('distinctions','Separate the knobs')+
 table(['Control','Question it answers','Example setting'],[
 ['Concurrency limit','How many operations may be active at once?','At most 20 model attempts in flight.'],
 ['Rate limit','How quickly may new work start over time?','At most 120 attempts per minute under an example policy.'],
 ['Token budget','How much model input/output work may be used?','A shared budget based on the provider’s documented accounting.'],
 ['Queue capacity','How much not-yet-started work may accumulate?','Stop accepting new local tasks when 200 are waiting.'],
 ['Connection-pool limit','How many connections may this client manage?','A finite pool; HTTP/2 can carry multiple streams per connection.']])+
 p('These example values are invented for teaching; they are not provider quotas. A concurrency limit of 20 permits a high start rate when requests finish quickly and a low start rate when they are slow. A rate limiter controls starts more directly. A prompt with 50,000 input tokens can consume much more budget than a short prompt even though each is one HTTP request.')+
 h('queues','Queues move waiting rather than remove it')+
 p('Imagine a worker reads 10,000 examples and launches one asynchronous task per example. The code looks concurrent, but waiting is now hidden in the connection pool, the event loop, memory, or the remote gateway. Bounded work admission makes the waiting visible and prevents unbounded accumulation. <strong>Backpressure</strong> is the idea that a downstream constraint should slow upstream production.')+
 p('Use a queue of pending samples and a fixed number of consumers. Before each attempt, obtain the relevant rate/token permission and an in-flight slot. Release resources on success, error, and cancellation. A task that leaks a connection by never consuming or closing a response can starve the pool even when the network is healthy.')+
 h('shared','Limits often span workers')+
 p('If ten workers each enforce “120 requests per minute,” together they can start 1,200. A project-wide budget needs coordination, partitioned allowances, or a shared scheduler. Count retries too. A retry storm is real traffic and consumes the same scarce capacity as first attempts.')+
 p('An HTTP 429 is evidence of a rate-limiting decision, but the relevant dimension can vary: requests, tokens, concurrent requests, organization quota, or a provider-specific policy. Inspect the response body and documentation. If a Retry-After field is present, it can specify a delay or a date; treat it as part of the service contract rather than hard-coding an arbitrary one-second loop.'+cite('http'))+
 h('fairness','Preserve a fair experiment')+
 p('A limiter can change which examples finish first. If you stop after a wall-clock budget, short examples may be overrepresented. Predefine sampling, ordering, retry, and stopping rules. Keep the original logical sample ID even when it produces multiple attempts, and record the scheduler wait separately from remote request time.')+
 box('A useful engineering sentence','“We cap in-flight attempts separately from the shared request and token budgets, count retries against those budgets, and log queue wait so a slower run does not silently change our evaluation population.”')+
 check('You increase an HTTP client pool from 10 to 100 connections and see more 429s. What changed, and what did not?', 'You removed one local constraint on simultaneous traffic. You did not increase the remote service’s quota. Add or adjust a coordinated request/token limiter and choose a measured concurrency level; do not interpret the extra connections as extra provider capacity.'),
    ['foundation','congestion','http','limits'],'concurrency rate limit quota 429 semaphore async queues backpressure token budget')

add(11,'timeouts-and-retries',3,'Timeouts, retries, and uncertain outcomes',
 'A timeout tells you that a caller stopped waiting. It does not tell you that the remote operation never happened.',
 h('clocks','Define which clock is running')+
 table(['Budget','What it bounds'],[
 ['Queue / pool wait','Time before obtaining permission or a connection.'],
 ['Connection setup','Establishing a usable connection; exact DNS/TLS coverage depends on the client.'],
 ['Read / idle timeout','Time without expected incoming data; often resets as data arrives.'],
 ['Total attempt deadline','Elapsed time for one complete attempt.'],
 ['Logical sample deadline','All attempts, waits, and backoff for one sample.'],
 ['Run budget','The whole evaluation, including result persistence.']])+
 p('Client libraries use these terms differently. Read the actual configuration semantics. An idle timeout can allow an endless trickle of data; a total deadline cannot. In curl, <code>--connect-timeout</code> includes DNS and the requested connection handshakes, while <code>--max-time</code> limits the transfer. Retry behavior adds another budget to inspect.'+cite('curl'))+
 h('uncertainty','The lost-response problem')+
 diagram('worker ── request ──→ server\n                      performs work\nworker ←─ X response ─ server\n  timeout: did the work happen?','The client’s uncertainty is about the outcome, not merely packet delivery.')+
 p('Repeating an operation is safe only under a defined contract. An <strong>idempotent</strong> operation has the same intended effect when repeated as when performed once. That does not mean identical response bytes or zero extra work. HTTP does not make arbitrary POSTs idempotent. A provider may support an idempotency key with explicit scope, expiration, and replay behavior; verify those details before relying on it.'+cite('http')+cite('rpc'))+
 p('Generating another answer can incur another charge and produce a different sample. Even without an external side effect, repeatedly retrying until the model gives a satisfactory answer changes the experiment. Retrying a transport failure and retrying a low-quality answer are different policies.')+
 h('policy','Write a bounded retry policy')+
 p('Define which failures are candidates for retry, a maximum attempt count, a remaining logical-sample deadline, and an overall retry budget. Use increasing delays with randomness so many workers do not retry in lockstep. Honor applicable server retry instructions. Authentication or malformed-input errors normally require a configuration or input change, not repetition.')+
 code('example policy, not a provider default:\n  logical sample budget: 90 seconds\n  maximum attempts: 3 total (first attempt + at most 2 retries)\n  retry: documented transient errors / selected transport failures\n  before retry: check remaining time, quota, and outcome ambiguity\n  delay: random between 0 and min(cap, base × 2^retry_index)\n  record every attempt; never keep only the fastest successful one')+
 p('Avoid independent retry loops in every layer. If an SDK makes three total attempts and your wrapper repeats that whole call three times, a sample can cause nine remote attempts. Repeated layers can amplify load exactly when a dependency is struggling. Identify the owner of retries and expose the actual attempt count.')+
 box('Keep the evidence','Record logical sample ID, attempt ID, timeout phase, elapsed time, error/status, request ID, partial-response state, retry decision, and known usage. If the outcome is ambiguous, label it ambiguous. A timeout is not proof of zero cost or zero remote effect.')+
 check('A gateway stops waiting at 30 seconds while your client deadline is 90 seconds. Will raising the client deadline to 180 seconds fix a 504?', 'Not by itself. The gateway’s upstream budget can still expire at 30 seconds. Identify every deadline along the path, decide which component should own the budget, and verify whether the backend continues working after the gateway stops waiting.'),
    ['http','rpc','curl'],'timeout deadline retries exponential backoff jitter idempotency ambiguous result cancellation')

add(12,'proxies-and-load-balancers',4,'Proxies, gateways, and load balancers',
 'The machine answering your connection may be an intermediary. Learn what it owns before attributing its behavior to the model.',
 h('roles','Several roles can share one component')+
 p('A <strong>forward proxy</strong> acts for clients making outbound requests. A <strong>reverse proxy</strong> stands in front of servers. A <strong>load balancer</strong> distributes traffic over backends. An <strong>API gateway</strong> often combines reverse proxying with authentication, quotas, routing, and other HTTP policy. One product can perform several of these jobs.'+cite('http'))+
 diagram('workers → outbound proxy → public API gateway → model replicas\n                              │\n                              └→ quota / authentication checks','An example path. An organization may have only some of these components.')+
 p('A Layer 4 balancer can make decisions using connection information. A Layer 7 proxy can inspect HTTP and route by host, path, or headers. If it decrypts client HTTPS to inspect messages, identify where TLS terminates and how the backend connection is protected. Do not infer the trust boundary from a product name alone.')+
 h('balance','Load balancing does not mean equal work')+
 p('One long-lived connection can carry many requests. Whether those requests reach several backends depends on the protocol and balancing layer. Counting connections may be a poor estimate of model load when request sizes differ substantially. A single long output can occupy capacity far longer than a short answer.')+
 p('Readiness checks help decide which backends should receive new traffic. A port being open is weaker evidence than a successful application-level readiness check. Even an HTTP health endpoint can be green while model weights are unavailable or the real inference path is overloaded. Ask what the health check actually tests and what it costs.')+
 h('policies','Find the intermediary’s limits')+
 table(['Policy','Possible eval symptom'],[
 ['Request body limit','Large prompts fail while small prompts succeed.'],
 ['Upstream timeout','Requests fail after a consistent elapsed time.'],
 ['Response buffering','Streaming appears in bursts or all at once.'],
 ['Idle timeout','Long gaps in a stream trigger disconnection.'],
 ['Header or auth policy','A direct backend call works but the supported gateway route fails.'],
 ['Backend selection','One subset of requests fails on a particular replica.']])+
 p('A 502 or 504 tells you about an intermediary’s problem with an upstream exchange. It does not identify every component in the chain. Correlate gateway logs with a request ID, selected backend, upstream duration, and termination reason. If the platform supplies these fields, they can be more useful than repeatedly trying the same request from a laptop.')+
 h('environment','Invisible proxy configuration')+
 p('Clients may honor <code>HTTP_PROXY</code>, <code>HTTPS_PROXY</code>, and <code>NO_PROXY</code>, with behavior that varies by client. A proxy can change resolution location, certificates, reachable destinations, and timing. Inspect relevant configuration without dumping credential-bearing environment values into a shared log. A direct curl test and an SDK request may take different routes.')+
 check('Small prompts succeed; large prompts receive 413 almost immediately. Should you increase inference timeout?', 'First inspect request-size limits at the responding gateway and the API contract. An immediate rejection of the request body is different from slow inference. Record payload size and response provenance, and establish the supported limit before changing timeouts.'),
 ['http','apps','ops','curl'],'reverse proxy forward proxy API gateway load balancer ingress health checks 502 504 413')

add(13,'cloud-networks',4,'Cloud networks without the mystery',
 'A cloud diagram becomes easier to read when you separate addressing, routing, traffic permission, and application identity.',
 h('pieces','Read the pieces independently')+
 p('A cloud virtual network groups configurable addressing and network connectivity. AWS calls this a VPC. A subnet is a range within that network; in AWS it belongs to one availability zone. Route tables decide where traffic goes. Security groups and other controls decide which traffic is allowed. Application credentials decide what a reached service permits. These mechanisms solve different problems.'+cite('vpc'))+
 table(['Question','Typical component'],[
 ['Which addresses can we allocate?','VPC and subnet CIDR ranges.'],
 ['Where does a packet for this destination go?','Route table and next hop.'],
 ['May this connection pass?','Security group, firewall, network ACL, or policy.'],
 ['How does private IPv4 traffic reach a public service?','An explicit outbound design, often NAT plus an Internet path.'],
 ['Which service can this identity use?','IAM/application authorization, beyond basic reachability.']])+
 h('example','A worker in a private subnet')+
 diagram('private subnet                           outside VPC\n  eval worker → public NAT gateway → Internet gateway → model API\n       │\n       └→ private endpoint / internal route → artifact service','Simplified AWS-style example. Routes and permissions must exist for each arrow.')+
 p('A private subnet does not directly route to an Internet gateway. It can still have outbound Internet access through a configured path such as a public NAT gateway in a public subnet. For ordinary IPv4 Internet access, appropriate source addressing or translation is also needed. A public subnet alone does not make every instance reachable.')+
 p('A managed NAT gateway tracks outgoing connections and translates return traffic. It does not grant remote systems a general ability to initiate inbound connections to private workers. At scale, connection capacity, idle lifetimes, and ports can become relevant. Before diagnosing rare connection errors as “the model is flaky,” inspect the outbound component’s metrics.'+cite('nat'))+
 h('permissions','Network permission is not application permission')+
 p('AWS security groups are stateful allow controls: return traffic for an allowed connection is treated differently from an unrelated new connection. Network ACLs are separate subnet-level controls with different semantics. Do not carry a rule recipe from one product to another without checking its model. Opening an inbound port on a worker is normally unrelated to its need to initiate an outbound HTTPS connection.'+cite('sg'))+
 p('Private service endpoints, VPNs, and peering can provide additional paths. Ask which exact service and region a private endpoint covers, how its DNS behaves, and which identity policy applies. “It is private” does not prove all dependencies use private paths or that every identity is authorized.')+
 h('review','Questions that make a review productive')+
 p('State the worker’s region, subnet, DNS view, outbound route, destination, port, and identity. Trace dataset download, model calls, grading, and result upload separately. A model call can succeed while result storage fails because those are different dependencies. Record whether a path crosses regions or zones when discussing latency and transfer costs; verify current pricing when estimating actual spend.')+
 check('A cloud worker can reach an internal database but cannot call a public model API. Does the database connection prove the network is fine?', 'It proves a particular internal path worked. Public model access can use different DNS, routes, gateways, firewall rules, and identities. Investigate the model path from the worker’s subnet, including its outbound route and any NAT or proxy.'),
 ['vpc','sg','nat','ip'],'VPC subnet cloud AWS security group NACL private public egress NAT VPN endpoint region availability zone')

add(14,'containers',4,'Containers: whose network is this?',
 'Most beginner container-networking failures are destination mistakes. Identify the network environment before changing the application.',
 h('namespace','A container gets a network view')+
 p('With ordinary container isolation, a process sees its own interfaces, loopback, routes, and ports through a network namespace. Two containers can both listen on port 8000 without conflict because those listeners are in different environments. Containers sharing a network namespace are an exception; configuration determines the boundary.'+cite('docker'))+
 diagram('host\n  host port 8080 ── mapping ──→ model container :8000\n                               ↑\n  worker container ── shared network, name “model” ──┘','From the worker, the container service name and container port are usually the relevant endpoint.')+
 p('On a Docker user-defined network, containers can find one another using container names or aliases. A host-port publication is a separate way for traffic from the host or elsewhere to enter the container. It does not change the port the process listens on inside the container.')+
 h('mapping','Read a mapping from outside to inside')+
 code('127.0.0.1:8080:8000\n└ host bind address\n          └ host port\n               └ container port')+
 p('This describes a host-loopback publication of container port 8000 at host port 8080. It is not an application command and does not start a listener. The containerized application must listen on an appropriate interface, often <code>0.0.0.0:8000</code>. The worker on the same container network normally calls <code>http://model:8000</code>, while the host calls <code>http://127.0.0.1:8080</code>.'+cite('ports'))+
 p('A container image’s <code>EXPOSE</code> declaration documents intended ports; it does not by itself publish them to the host. Docker Desktop also introduces a virtual-machine boundary on common desktop platforms, so a Linux-host recipe may not map exactly onto macOS. Recognize the boundary and consult the platform’s supported host-access mechanism.')+
 h('inspect','Observe before editing')+
 code('docker ps\ndocker port MODEL_CONTAINER\ndocker inspect --format \'{{json .NetworkSettings.Networks}}\' MODEL_CONTAINER')+
 p('These are optional read-only Docker commands. Replace <code>MODEL_CONTAINER</code> with the actual container name; the core course lab does not require Docker. The first command identifies running containers and published ports, the second lists port mappings, and the third shows network attachments. Avoid treating a remembered internal IP as a stable service identity.')+
 h('failure','A worked diagnosis')+
 p('The host can call <code>localhost:8080</code>. A worker container cannot call the same URL. First note that localhost now refers to the worker container. Check that both containers share the intended network, that the model name resolves there, and that the model is listening on its container port. Use a diagnostic command inside the worker’s environment if available; host success is only evidence about the host path.')+
 box('For an eval deployment','Document the endpoint separately for host development, container-to-container calls, and cloud execution. A configuration variable called MODEL_URL is useful only if each environment gives it a valid value. Copying a working local URL unchanged is not a deployment strategy.')+
 check('You publish 9000:8000 and the model listens on 8000. Which port should another container on the same user-defined network use to reach the model by name?', 'Normally 8000, the container service port. Port 9000 is the published host port. The exact supported route depends on configuration, but you should choose the intended service-to-service path rather than assuming every caller uses the host mapping.'),
    ['docker','ports','virtual'],'Docker container bridge namespace localhost publish EXPOSE port mapping host')

add(15,'kubernetes',4,'Read a Kubernetes network diagram',
 'You need a working map of the objects and paths before you need to administer a cluster.',
 h('objects','Learn four objects first')+
 table(['Object','Network role'],[
 ['Pod','One or more containers sharing a network namespace and ports. Pod instances can be replaced.'],
 ['Service','A stable access abstraction for a set of backends; a typical ClusterIP Service exposes a cluster-internal address.'],
 ['EndpointSlice','A representation of backend endpoints associated with a Service.'],
 ['Ingress / Gateway','Configuration for traffic entering services, implemented by a controller or supporting infrastructure.']])+
 p('A Service gives clients a stable way to refer to changing backends. A typical selector-based Service tracks matching Pods through endpoint objects. It is not necessarily a proxy process running on a machine with the Service IP. Cluster networking implements the forwarding. A Service existing in the API does not prove it has a ready backend.'+cite('k8s'))+
 h('dns','Names carry context')+
 p('A name like <code>grader</code> can resolve within the caller’s namespace. A longer name such as <code>grader.evals.svc.cluster.local</code> makes the Service and namespace explicit in a cluster using the common <code>cluster.local</code> domain. The cluster domain is configurable. Your laptop’s resolver usually does not know these names or have the internal route.'+cite('k8sdns'))+
 diagram('worker Pod\n  → cluster DNS: grader.evals.svc.cluster.local\n  → Service port 80\n  → ready backend Pod, target port 8000','Service port and backend targetPort can differ, just as host and container ports can differ.')+
 h('policy','Reachability is also a policy question')+
 p('NetworkPolicy can constrain traffic to and from selected Pods, provided the cluster’s network plugin enforces it. With no selecting policy for a direction, Pods are generally non-isolated for that direction. In an isolated setup, both source egress and destination ingress rules can matter. A policy file existing is not proof of enforcement or of the intended permissions.'+cite('policy'))+
 p('A worker may need DNS access, model API access, artifact storage, and a grading service. A rule that permits only HTTPS to one destination can accidentally break name resolution or storage. Conversely, allowing arbitrary egress because one dependency failed hides the original problem and broadens the trust boundary. Identify each required flow.')+
 h('inspect','A minimal read-only investigation')+
 code('kubectl -n evals get pods\nkubectl -n evals get service grader\nkubectl -n evals get endpointslices -l kubernetes.io/service-name=grader\nkubectl -n evals get networkpolicy')+
 p('These optional commands require access to the intended cluster. First confirm your current context using <code>kubectl config current-context</code>; use the correct namespace. You are looking for healthy backends, the Service’s port and selector, and relevant policies. Commands from your laptop inspect cluster state but do not reproduce a worker’s data path.')+
 p('A port-forward can help isolate an application, but it creates a different path. Success through port-forward does not prove Service routing, DNS, ingress, or NetworkPolicy behavior along the normal production path. Report exactly which path you tested.')+
 check('The Service name resolves and kubectl shows the Service exists, but requests fail. What is the next useful distinction?', 'Check whether the Service has ready backend endpoints and whether its target port matches the application listener. Then inspect the source/destination network policy and the worker’s actual path. A DNS answer and a Service object alone do not prove a usable backend.'),
 ['k8s','k8sdns','policy'],'Kubernetes k8s Pod Service ClusterIP EndpointSlice ingress Gateway namespace NetworkPolicy kubectl')

add(16,'inference-and-locality',4,'Where the model runs changes the network',
 'Calling a hosted model and distributing inference across GPU nodes involve different network responsibilities. Learn to distinguish them.',
 h('boundaries','Three deployment patterns')+
 table(['Pattern','Connections you should understand'],[
 ['Hosted model API','Worker → provider endpoint; your dependencies, credentials, quotas, and observed latency.'],
 ['Self-hosted inference on one node','Worker → gateway → model server; queues, model readiness, resource limits, and telemetry.'],
 ['Inference spanning several nodes','The client path plus internal communication among model processes and GPUs.']])+
 p('A GPU is a processor optimized for parallel work; a GPU node is a machine containing one or more GPUs. A single-node service can still serve many network clients. Conversely, one logical inference request may trigger communication across several machines if the model or computation is partitioned.')+
 h('parallelism','Recognize the parallelism terms')+
 p('<strong>Data parallelism</strong> runs replicas on different requests or data. <strong>Tensor parallelism</strong> divides parts of a model’s operations across devices. <strong>Pipeline parallelism</strong> divides model stages. The resulting communication patterns differ: balancing independent requests is unlike exchanging intermediate results repeatedly during one request.')+
 p('NCCL is a library for collective communication among GPUs. Its supported paths include technologies such as PCIe, NVLink, InfiniBand, and IP sockets. These names refer to different interconnects or communication mechanisms; they are not alternate names for a public HTTPS API. If an inference operator reports slow collectives, raising your worker’s HTTP pool size is unlikely to address the same bottleneck.'+cite('nccl'))+
 h('locality','Move the right data the right distance')+
 p('An eval may download a dataset, fetch images or audio for each prompt, send requests, collect output, and upload artifacts. List these transfers separately. Sending a compact text prompt to a remote API and repeatedly downloading a large multimodal dataset have very different bandwidth demands.')+
 p('Co-locating workers with data or inference can reduce some path lengths and cross-region transfer, but the effect depends on the bottleneck. If generation time dominates, shaving milliseconds off RTT may not materially change total throughput. Placement can also affect data handling requirements and availability. Measure the actual path and verify provider-specific prices before making a cost claim.')+
 h('layers-of-control','Control traffic and bulk data')+
 p('A scheduler assigning tasks is control traffic. Dataset transfers, prompts, model outputs, and internal inference tensors are data traffic. These are conceptual categories, not necessarily separate physical networks. A robust design asks whether bulk transfers can starve scheduling or telemetry and whether retries amplify the wrong workload.')+
 box('Depth appropriate to your role','For many eval engineering tasks, you should explain the external request path and recognize when the bottleneck is inside inference serving. Detailed RDMA tuning or collective-algorithm design belongs to a more specialized role. Escalate with evidence about placement, sizes, timings, and affected components.')+
 check('Model-server metrics show GPU communication stalls, while worker-to-gateway connection times remain stable. What should your investigation focus on?', 'The inference backend’s topology, collective communication, resource saturation, and serving configuration are now stronger candidates than client connection setup. Preserve the evidence and involve the serving owner. Stable external timings do not prove every network inside the system is healthy.'),
 ['foundation','nccl','virtual'],'GPU inference serving data parallel tensor parallel pipeline NCCL RDMA InfiniBand locality region')

add(17,'diagnostic-method',5,'A diagnostic method you can repeat',
 'The goal of troubleshooting is to reduce uncertainty with evidence. Start with the exact caller, destination, and last successful stage.',
 h('scope','First, make the report reproducible')+
 p('Write down the timestamp and time zone, worker environment, hostname, port, protocol, endpoint path, example size, timeout settings, concurrency, and error. Redact credentials and sensitive prompt content. Establish the scope: one worker or all workers, one region or all regions, one example type or every request. A recent change is a hypothesis to investigate, not proof of causation.')+
 h('ladder','Climb the evidence ladder')+
 table(['Stage','A useful observation','What it does not prove'],[
 ['Local setup','Expected endpoint, proxy settings, and client configuration.','The path is reachable.'],
 ['Name resolution','Resolver returns the expected address family and destination.','A listener or route works.'],
 ['Connection','TCP setup reaches a listening endpoint.','TLS or the API works.'],
 ['TLS','Verified handshake with the intended identity.','Your API identity is authorized.'],
 ['HTTP','Status, headers, body, and request ID.','The model produced a complete usable answer.'],
 ['Application','Valid schema and completion signal.','The result was durably recorded or correctly graded.']])+
 p('The last successful stage helps you choose the next experiment. If DNS fails, tuning generation parameters is irrelevant to that attempt. If a gateway returns 429, a packet-level investigation is rarely the first useful step. If the answer arrives but persistence fails, the model path may be fine while the artifact path is not.')+
 h('commands','Use commands to test a hypothesis')+
 code('curl -v --connect-timeout 5 --max-time 15 https://example.com/')+
 p('This live, credential-free request can show the selected address, proxy use, TLS verification, and HTTP exchange. It tests the environment where curl runs. To investigate a container or CI worker, use an approved diagnostic method in that environment or record why your test differs. Never paste full authenticated verbose output into an incident channel.')+
 p('<code>ping</code> tests an ICMP exchange, which can be blocked while HTTPS works. A failed ping does not establish an application outage. <code>traceroute</code> can reveal responding hops, but nonresponding hops are not automatically failed hops, and probes can take a different path from the application. Use these tools as evidence with limits, not pass/fail oracles.'+cite('ops'))+
 h('one-change','Change one thing when possible')+
 p('Compare a small and a large request, the failing worker and a known-good worker, IPv4 and IPv6, or the ordinary DNS answer and a controlled address override. Hold other variables steady. A successful test should distinguish hypotheses: changing region, client library, payload, model, and timeout together gives you little causal information.')+
 p('For a reproducible large-transfer stall, MTU can become relevant. The maximum transmission unit limits packet size on a link; encapsulation can reduce the usable size. Path-MTU problems are a possible later investigation when the evidence fits, not a reason to begin every HTTP incident with packet captures.')+
 box('A strong escalation','“At 14:05 UTC, workers in subnet A resolve the endpoint to X but connection setup reaches its 5-second limit. Subnet B completes the same credential-free health request. No HTTP response exists. The failure began after the outbound-route change. Here are the route and gateway observations.”')+
 check('Ping fails, but curl returns the expected HTTPS response. Is that contradictory?', 'No. ICMP and HTTPS are different traffic and can be governed by different rules. The successful curl exchange is direct evidence for that HTTPS path; ping’s failure only describes the tested ICMP behavior.'),
 ['curl','ops','ip'],'debug troubleshoot curl ping traceroute MTU connection timeout diagnosis runbook incident')

add(18,'observability',5,'Collect evidence that explains an eval',
 'A useful result record describes both the model output and the path that produced it. Design that record before a failure forces you to improvise.',
 h('signals','Logs, metrics, and traces')+
 p('A log records an event. A metric aggregates a quantity over observations or time. A trace represents a request’s path as related spans: timed operations such as queue wait, model request, or result upload. Propagated trace context allows participating components to relate their spans. Instrumentation and context propagation must be present; the network does not automatically create a complete trace.'+cite('otel'))+
 diagram('logical sample 0042\n  ├─ attempt A: queue → model request → timeout\n  ├─ retry wait\n  └─ attempt B: queue → model request → parse → persist\n                                           └→ grade','One logical sample can contain multiple attempts and several independently failing operations.')+
 h('record','A minimal attempt record')+
 code('{\n  "run_id": "example-run",\n  "sample_id": "0042",\n  "attempt_id": "0042-b",\n  "worker_region": "example-region",\n  "endpoint_host": "models.example.test",\n  "queue_ms": 240,\n  "attempt_ms": 8200,\n  "http_status": 200,\n  "provider_request_id": "if-supplied",\n  "terminal_event_seen": true,\n  "outcome": "completed",\n  "retry_count_before_attempt": 1\n}')+
 p('This is a hypothetical schema and invented data. Add the model/version, client version, request parameters, input/output lengths, timeout policy, and known token usage where appropriate. Store timestamps with an explicit time zone and use a monotonic clock for local durations so wall-clock adjustments do not corrupt elapsed-time measurements.')+
 h('classification','Classify without erasing ambiguity')+
 table(['Outcome','What to preserve'],[
 ['Completed','Valid response and documented completion. Grade it under the task rubric.'],
 ['Protocol / schema failure','HTTP or parsing evidence and any partial body.'],
 ['Transport / deadline failure','Phase, exception, elapsed time, and known remote request ID.'],
 ['Unknown remote outcome','A timeout/reset after submission without authoritative completion evidence.'],
 ['Persistence failure','Whether a response existed and whether it can be recovered.']])+
 p('The labels should match your evaluation target. A product test may count infrastructure failures in its end-to-end reliability metric. A model-capability analysis might also report a separately labeled completed-sample score. In both cases, retain counts and denominators so readers can see the missingness and retry policy.')+
 h('privacy','Useful telemetry can be selective')+
 p('Prompt bodies, model outputs, authorization headers, signed URLs, and proxy credentials can be sensitive. Prefer identifiers, sizes, status, bounded redacted error excerpts, and timing fields for routine networking diagnostics. If content is required to reproduce a problem, handle it under the dataset’s access and retention rules. More logging is not automatically more useful evidence.')+
 p('Avoid putting sample IDs into every metric label when that creates a separate time series per sample. Aggregate metrics by a small set of useful dimensions; put high-cardinality identifiers into logs or traces. Sampling a trace stream can omit rare failures, so ensure run accounting and durable result records remain complete enough for your analysis.')+
 check('The dashboard shows 95% accuracy but no count of timed-out samples. What is missing?', 'The denominator and failure population. You need total scheduled samples, attempted/completed/failed counts, the retry policy, and whether infrastructure failures were excluded. Without that information, 95% can describe a selectively completed subset rather than the intended evaluation.'),
    ['otel','ops'],'observability logs metrics traces spans trace ID request ID telemetry cardinality outcomes denominators')

add(19,'local-lab',6,'Lab: observe a real HTTP service',
 'Use two terminal windows to run a tiny service and investigate it. Everything stays on your computer; the examples need no API key or Internet connection.',
 h('setup','Start the service')+
 p('You need Python 3 and curl. Check with <code>python3 --version</code> and <code>curl --version</code>. The commands below assume a macOS or Linux shell. A terminal is a text interface for running programs; leave the first terminal open because its server process must keep running while the second terminal makes requests.')+
 code('cd /Users/mark/dev/repos/_do/evals/domains/networking/networking-tut\npython3 labs/server.py')+
 p('If you move the course, change the folder in the first command. The service prints <code>http://127.0.0.1:8765</code> and waits for requests. If that port is occupied, use <code>python3 labs/server.py --port 8766</code> and change the client URLs accordingly. Stop it with Ctrl-C. It binds only to loopback, stores experiment counters in memory, and makes no external requests. This is a teaching server, not a production deployment.'+cite('python'))+
 h('success','1. Read a successful exchange')+
 code('curl -i http://127.0.0.1:8765/ok')+
 p('Expect HTTP 200, a JSON content type, and a body whose <code>outcome</code> is <code>complete</code>. Identify the address, port, path, status, and body. Now request <code>/missing</code>. Expect 404: you reached a working HTTP service, but it does not recognize that route. This contrasts with stopping the server and seeing a connection refusal. Restart it before continuing.')+
 h('status','2. Separate HTTP status from process exit status')+
 code('curl -i http://127.0.0.1:8765/status/429\necho $?')+
 p('Expect an HTTP 429 with <code>Retry-After: 2</code>, but normally shell exit status 0: curl successfully transferred an HTTP error response. The <code>$?</code> expression reports the preceding command’s exit status. Run the next command separately:')+
 code('curl --fail-with-body -i http://127.0.0.1:8765/status/429\necho $?')+
 p('With curl versions supporting this flag, expect exit status 22 while keeping the error body. On older curl, use <code>--fail</code>, which suppresses the response body. This simulated endpoint always returns 429, even if you wait. Its purpose is to expose status and headers, not to model a recovering quota.')+
 h('timeout','3. Watch work outlive a client deadline')+
 code('curl --max-time 1 "http://127.0.0.1:8765/slow?seconds=3&key=late"\necho $?')+
 p('Expect curl to stop after approximately one second with exit status 28. Wait at least three seconds from when you started the request, then inspect the server’s record:')+
 code('curl http://127.0.0.1:8765/stats')+
 p('The <code>slow_completed</code> object should include <code>"late": 1</code> on a fresh server. The client timed out, but the server still finished its simulated work. Repeating the experiment increments the count. This is evidence of an ambiguous outcome at timeout time, later resolved by an authoritative server record.')+
 h('retry','4. Observe separate attempts')+
 code('curl -i "http://127.0.0.1:8765/flaky?key=exercise-one"\ncurl -i "http://127.0.0.1:8765/flaky?key=exercise-one"')+
 p('For a new key, the first request returns 503 and the second 200 with <code>attempt: 2</code>. The lab does not automatically retry. Use a new key or restart the server to reset the scenario. Write two attempt records under one logical sample rather than pretending there was one flawless request.')+
 h('stream','5. Check stream completion')+
 code('curl -N http://127.0.0.1:8765/stream\ncurl -N "http://127.0.0.1:8765/stream?cut=1"')+
 p('The complete stream emits three token events and then an <code>event: done</code>. The cut stream emits one token and closes without done. Both start with HTTP 200, and curl can exit successfully on both because this HTTP body is delimited by connection closure. Your application must enforce its own completion contract. <code>-N</code> disables curl output buffering, making the arriving events easier to see.')+
 check('Write a six-line incident report for the slow endpoint. Include the request, the client deadline, the observed error, the later server evidence, what you learned, and a remaining limitation.', 'A good answer says the local request exceeded a one-second client deadline, curl exited 28, and /stats later recorded completion. This demonstrates that stopping the caller does not necessarily stop server work. The lab does not reproduce provider billing, TLS, DNS, gateway behavior, or a real model; those would require separate evidence.'),
 ['python','curl','sse'],'hands on lab local curl Python HTTP timeout stream 429 503 experiment')

add(20,'incident-practice',6,'Practice: four infrastructure incidents',
 'For each incident, state the last successful stage, at least two plausible causes, and the next observation that would distinguish them. Then reveal the reasoning.',
 h('incident-one','1. Works on the laptop, fails in CI')+
 p('Hypothetical evidence: a private grader works from the developer’s laptop while connected to a VPN. CI reports name-resolution failure for <code>grader.internal</code>. No HTTP status or provider request ID exists. Someone suggests increasing the request deadline from 30 to 120 seconds.')+
 check('Where should you investigate first?', 'Name resolution in CI. The laptop may use a private DNS view unavailable to CI; CI may use the wrong resolver or be unable to reach it. Inspect the failing environment’s configured resolver and required network access. A longer application deadline does not create a missing private DNS zone. After resolution works, routing and service access still need to be established.')+
 h('incident-two','2. The new deployment fails at 60 seconds')+
 p('Hypothetical evidence: short model requests complete. Long requests through a gateway return 504 at approximately 60 seconds. Direct backend tests can complete after 75 seconds. The client’s total deadline is 120 seconds, and there is no evidence yet about what the backend does after the gateway stops waiting.')+
 check('What hypothesis fits, and what evidence would you request?', 'A gateway upstream deadline is a strong hypothesis, but a consistently timed downstream failure is also possible. Inspect the gateway’s configured deadlines and termination reason, then correlate backend logs with the same request ID. The direct test follows a different path. Establish whether work continues after the 504 before adding retries or increasing deadlines.')+
 h('incident-three','3. Faster workers, worse results')+
 p('Hypothetical evidence: concurrency rises from 10 to 100. The run finishes sooner, successful-request mean latency falls, and the reported accuracy rises from 72% to 79%. But completed samples fall from 1,000 to 620, with most missing examples containing large prompts. The report excludes all HTTP errors and timeouts.')+
 check('Can you conclude that the new deployment improved model performance?', 'No. The evaluated population changed and the missingness is related to prompt size. You have a conditional score over a different subset. Report counts, failure types, prompt distributions, deadlines, and retry policy. Investigate limits and queueing, then compare under a predefined population and failure-handling policy. The performance change may be mostly selection bias.')+
 h('incident-four','4. Healthy Service, failed requests')+
 p('Hypothetical evidence: a Kubernetes Service name resolves. Its Service port is 80 and targetPort is 8000. The Pods are running, but the application log says it is listening on 127.0.0.1:8000. Requests from other Pods fail. A port-forward succeeds.')+
 check('How do you explain the discrepancy?', 'A loopback-only listener inside the Pod is a strong candidate: ordinary Service traffic reaches a Pod interface rather than loopback. The port-forward path differs. Check actual listener binding, ready EndpointSlices, selectors, target ports, and policies before treating the hypothesis as proven. “Running” is a process state, not evidence that the intended interface accepts requests.')+
 h('writeup','Turn observations into an escalation')+
 code('Impact: which runs / samples / environments are affected?\nEvidence: timestamps, exact error, last successful stage, request IDs\nScope: what works, what fails, and which comparison was controlled\nHypotheses: two plausible explanations, ranked with reasons\nNext test: the smallest observation that distinguishes them\nMeasurement: how failures and retries appear in the eval report')+
 p('These cases are original exercises, not reports of real outages. The standard is not guessing the hidden answer on the first try. It is choosing a test whose result would change your belief, preserving contradictory evidence, and explaining the limits of what you observed. Revisit the diagnostic lesson if your next step is only “try again.”'),
 ['dns','http','k8s','docker'],'incidents practice debugging interview case study outage selection bias')

add(21,'design-an-eval-system',7,'Design an eval system you can explain',
 'Combine the pieces into a small, reviewable architecture. Start with the required flows and failure accounting, then choose infrastructure to support them.',
 h('requirements','An explicit example brief')+
 p('Design a hypothetical nightly evaluation of 10,000 examples against a hosted model API. Some examples include images. A separate grader processes completed answers. Results must be recoverable after a worker crash, and a report must distinguish model quality from infrastructure outcomes. These are exercise requirements, not a prescription for every team.')+
 diagram('versioned dataset → scheduler / task queue → bounded workers\n                                             │   │\n                              HTTPS model API┘   └→ artifact store\n                                                      │\n                                                grader workers\n                                                      │\n                                                report builder\n\nall stages → attempt records, metrics, correlated logs','Each arrow is a dependency to specify. The queue carries work references; large artifacts can live in storage.')+
 h('flows','Describe every connection')+
 table(['Flow','Details a reviewer needs'],[
 ['Worker → model','Hostname, TLS identity, outbound route, region, API identity, quotas, connection reuse, deadlines.'],
 ['Worker → data/storage','Dataset version, access identity, object sizes, encryption, bandwidth, retries, and durable write behavior.'],
 ['Worker → queue','Delivery semantics, lease/visibility timing, acknowledgment policy, and recovery after failure.'],
 ['Grader → dependencies','The same model/network rules if grading calls another model; do not hide this second workload.'],
 ['Telemetry → collector','Identifiers, redaction, retention, failure buffering, and what can be reconstructed if telemetry is delayed.']])+
 h('state','Give each sample a durable history')+
 p('Assign a run ID, logical sample ID, and distinct attempt IDs. Keep an explicit state such as queued, running, completed, infrastructure-failed, or outcome-unknown. Persist the received answer before marking the logical work complete. The exact queue and storage transaction design depends on the platform, but a worker crash between “remote work completed” and “result stored” must have a documented recovery path.')+
 p('A queue that can redeliver work is useful for recovery, but redelivery can duplicate model calls. Local deduplication of stored results does not undo remote charges or side effects. Use documented idempotency support where available and record uncertain attempts when it is not. Do not claim exactly-once end-to-end processing just because a database row is unique.')+
 h('capacity','Make capacity a measured choice')+
 p('For an invented sizing example, suppose each request takes 5 seconds on average and you want 4 completions/s. About 20 in-flight requests are a starting estimate under stable conditions. Confirm shared request/token limits, workload sizes, and failure rates. A grader that makes another model call adds its own traffic and can be the bottleneck. Sweep concurrency conservatively and record throughput and tail latency together.')+
 h('recovery','Review failure paths before the happy path')+
 p('What if the provider returns 429 for ten minutes? What if a worker loses its response after generation completes? What if storage is down? Bound retries, pause admission when appropriate, and make unfinished work visible. A circuit breaker temporarily stops calls to a failing dependency according to a measured policy; it still needs a recovery check and honest run accounting.')+
 box('A concrete review deliverable','Produce the diagram, a flow table, the timeout/retry policy, a sample attempt record, and a failure matrix. Together these let a teammate understand how the system behaves when a request stops halfway through.')+
 check('Why is “retry the whole sample whenever anything fails” an incomplete recovery policy?', 'Failure may occur after the model already completed, during storage, or during grading. Retrying everything can regenerate a new answer, duplicate cost, and alter the sample. Preserve stage-specific state and retry the failed operation when the contract and stored evidence make that safe.'),
 ['foundation','rpc','http','vpc'],'architecture design queue worker fleet scheduler storage reliability retries circuit breaker')

add(22,'boundaries-and-validity',7,'Trust boundaries and eval validity',
 'Network access is part of the experiment. It determines what an agent can observe or change and which failures enter your score.',
 h('authority','An agent’s tool access changes the design')+
 p('A simple model call sends a prompt to a known endpoint. An agent that runs tools may fetch URLs, execute code, access a database, or browse a site. Its network permissions become part of the task environment. Draw the boundary between the eval controller, the agent sandbox, the model provider, and services the agent can reach.')+
 p('Give the sandbox only the identities and reachable services needed for the task. Treat model output and retrieved pages as untrusted inputs to tool execution. A proxy or allowlist can help constrain egress, but the whole design must account for redirects, DNS behavior, alternate addresses, and service-specific access. A private address is not a reliable label for “safe to contact.”')+
 h('sensitive','Keep powerful services out of the task environment')+
 p('Internal admin endpoints, cloud instance metadata, credentials, and grader internals should not become reachable simply because an agent can request a URL. Keep the controller’s credentials outside the sandbox where possible. The goal is to make task permissions explicit and enforceable, not to rely on the agent remembering an instruction.')+
 p('Network isolation and application authorization complement each other. A network control can block a connection; a reached service must still validate identity and scope. TLS protects a link, while the service at termination can read the request. Decide where sensitive datasets and outputs may travel and what gets retained in logs.')+
 h('construct','Access can change what the eval measures')+
 p('If a benchmark intends to test unaided reasoning, allowing Internet retrieval changes the available information. If it intends to test web-agent ability, blocking all egress destroys the task. Record allowed services, Internet access, cached data, snapshots, DNS/proxy configuration, and relevant versions so the environment can be interpreted later.')+
 p('Changing an external site can change a browsing task between runs. A request failure might come from your infrastructure, an external rate limit, or the task’s expected obstacle. The rubric should distinguish these where the evaluation objective requires it. Preserve enough evidence to classify outcomes without exposing more sensitive content than needed.')+
 h('denominators','Make failure accounting visible')+
 table(['Metric in a hypothetical report','Interpretation'],[
 ['800 correct / 1,000 scheduled = 80%','An end-to-end success definition where all other outcomes are unsuccessful.'],
 ['800 correct / 900 completed ≈ 88.9%','Quality conditional on completion, with 100 incomplete samples disclosed.'],
 ['900 completed / 1,000 scheduled = 90%','Completion rate under the stated deadlines and retry policy.']])+
 p('These figures describe different questions using the same invented run. None should be relabeled as the others. Conditional quality can be biased if difficult or long examples are more likely to fail. Report distributions and failure categories, and choose the primary metric before looking at results.')+
 check('A new runner improves “accuracy” by dropping all samples that time out. What would you ask in review?', 'Ask whether the target metric changed, how many samples were excluded, whether exclusions correlate with task difficulty or size, and whether the policy was predefined. Request both full-run accounting and any explicitly conditional score. Then investigate the failures rather than treating missing samples as irrelevant.'),
 ['tls','policy','rpc'],'agent sandbox egress security trust boundaries leakage SSRF validity network permissions score denominator')

add(23,'readiness-review',7,'Capstone: explain, diagnose, and defend',
 'Your finish line is a set of things you can demonstrate. Use this review to find the next gap, then return to the relevant lesson.',
 h('brief','The design brief')+
 p('A team runs 10,000 nightly evals. Workers run in containers in a private cloud subnet. They call a hosted model API, write responses to object storage, and send completed responses to a grader. Some tasks run agents in sandboxes. Current problems include intermittent 429s, 60-second gateway failures, and an unexplained improvement in accuracy when concurrency increases. Draw and explain a revised design.')+
 h('deliverables','Bring five artifacts to the review')+
 table(['Artifact','What to include'],[
 ['Network diagram','Hosts/processes, DNS, routes, egress, proxies, TLS boundaries, model and storage dependencies.'],
 ['Request budget','Queue wait, connection setup, attempt deadline, logical sample deadline, retry count and backoff.'],
 ['Attempt record','IDs, environment, status/error, partial state, completion evidence, timing, retry decision.'],
 ['Incident report','One reproduced local lab failure, its evidence, a hypothesis, and the next discriminating test.'],
 ['Measurement policy','How retries, incomplete samples, agent network access, and denominators affect the report.']])+
 h('oral','Questions to answer aloud')+
 check('Trace a fresh HTTPS model request from a container, then explain what connection reuse changes.', 'Identify the container network view, resolver, destination address and port, route/egress, TCP setup, TLS identity, HTTP request, gateway/backend, response framing, and persistence. A cached DNS answer or an existing connection can avoid some setup work. An explicit proxy or HTTP/3 changes the path; state your assumptions rather than insisting every request follows one sequence.')+
 check('Why can localhost work in development and fail after deployment?', 'It refers to the caller’s network environment. A separate container or Pod is generally a different destination. Check the intended service name, network attachment, container/Service ports, and listener binding. Do not fix a wrong destination with retries.')+
 check('You see a 504 at 60 seconds with a 120-second client deadline. What do you do?', 'Identify the gateway, its upstream, and their timing and termination logs using a request ID. Confirm which deadline fires and whether work continues. Align budgets to the intended request lifecycle, and account for ambiguous outcomes before adding retries.')+
 check('What is the difference between 30 concurrent requests and 30 requests per minute?', 'Concurrency is the number in flight at an instant. Rate concerns starts or completions over an interval, and you must specify which. Request duration relates them under stable conditions. A shared rate/token limiter and a concurrency bound solve different constraints.')+
 check('A model call times out. Can you claim it cost nothing or that retrying produces the same sample?', 'No. The remote service may have accepted and completed the request. Seek authoritative usage/completion information where available; otherwise record ambiguity. A retry may incur cost and produce another stochastic output. Apply a predefined policy, not an assumption of rollback.')+
 check('Which infrastructure does the grader need, and why does that matter?', 'If grading calls another model or database, it has its own DNS, connections, TLS, quotas, deadlines, and failure states. Measure and budget it separately. A model response can be complete while grading fails; regenerating the answer may be unnecessary and may alter the evaluation.')+
 h('rubric','An observable readiness rubric')+
 table(['Skill','Ready enough to build on','Practice more if…'],[
 ['Explain','You can draw a request path and define each component in ordinary language.','You use “the network” for every stage.'],
 ['Diagnose','You reproduce a failure, name the last successful stage, and choose a test that distinguishes causes.','Your only strategy is longer timeouts or repeated restarts.'],
 ['Design','You specify flows, budgets, identities, capacity controls, and recovery states.','The diagram has arrows without destinations, permission, or failure behavior.'],
 ['Measure','You account for all scheduled samples and separate attempts from logical outcomes.','Errors disappear from the denominator without explanation.'],
 ['Communicate','You state evidence, uncertainty, and the appropriate component owner.','You present a plausible cause as proven.']])+
 p('This rubric is an original self-assessment, not an industry certification or a universal hiring standard. Rehearse with a teammate or explain it into a recording. A useful answer can include “I do not know yet; this observation would distinguish the two possibilities.” Professional fluency includes knowing where your evidence ends.')+
 h('next','Choose the next depth deliberately')+
 p('If your weak point is vocabulary, revisit the request and stack lessons. If commands feel abstract, repeat the local lab and write the output in your own words. If you are moving toward infrastructure or inference-serving roles, follow the book reading map into routing, congestion control, virtual networks, and internal GPU communication. For an eval role, keep practicing the connection between infrastructure outcomes and measurement.'),
 ['foundation','rpc','http','ops'],'capstone readiness interview professional assessment design review employable')
