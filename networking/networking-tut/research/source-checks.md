# Source checks and authoring scope

Access date: September 20, 2026.

The user-supplied textbook page was accessible through a direct HTTPS fetch. The web reader initially could not access that domain. The full text of the relevant chapters was fetched to a temporary research cache; the following topic passages were inspected. The delivered course links to the primary sources rather than bundling the book.

| Source | Topics checked |
| --- | --- |
| Systems Approach, chapter 1 | Encapsulation, end-to-end responsibility, bandwidth/latency and units. |
| Chapter 2 | HTTP request/response operation and multiplexing across protocol versions. |
| Chapters 3–4 and 6 | Link/packet roles, routing, prefix matching, private address translation. |
| Chapters 9–10 | Virtual networks and network operation context. |
| Chapter 11 | DNS resource records, resolver role, aliases, record TTL and caching. |
| Chapter 12 | Byte-stream abstraction, connection handshake, flow control. |
| Chapter 13 | Congestion window versus receiver window and shared capacity. |
| Chapter 14 | Certificates, trust, authentication, and TLS handshake protection. |
| Chapter 15 | Duplicate message effects, idempotence, RPC, and gRPC over HTTP. |
| Book About page | Authors, 2026 attribution, CC BY 4.0, prior-edition attribution, living main branch. |
| RFC 9110 | Idempotent methods, Retry-After syntax, HTTP semantics and gateway statuses. |
| RFC 9114 | HTTP over QUIC; independent streams and UDP transport. |
| RFC 6585 §4 | 429 meaning; optional Retry-After and implementation-specific counting scope. |
| RFC 3596 §2 | AAAA records store IPv6 addresses; record type is independent of query transport. |
| WHATWG HTML / Fetch | Event-stream framing and browser cross-origin access rules. |
| curl manual | Cumulative timing definitions, connection/total limits, output buffering, resolve overrides, failure options. |
| AWS VPC, security groups, NAT gateway docs | Route targets, subnet context, stateful security groups, outbound translation and response mapping. |
| Docker networking and port-publishing docs | Container network context, user-defined network names, host versus container ports. |
| Kubernetes Service, DNS, NetworkPolicy docs | Stable service access, endpoints, namespace DNS search, direction-specific isolation and enforcement dependency. |
| OpenTelemetry traces | Span relationships, trace IDs, and context propagation. |
| Python http.server | Standard-library request handlers and threaded teaching server. |
| NVIDIA NCCL overview | Collective communication and supported GPU/node interconnect technologies. |

`sources.json` records the course’s source inventory and `retrieval-manifest.json` records direct-fetch metadata. HTTP success was not treated as proof of useful content: an AWS retry article redirected to a JavaScript shell with no readable article text, so it was excluded from the source inventory and is not cited. The retry-policy discussion is original design guidance grounded in the textbook’s remote-transaction discussion and the HTTP idempotence specification.

## Boundaries of the claims

- The course is independently written and selects a practical curriculum for the user’s stated goal. It does not claim that the textbook prescribes this curriculum.
- All incident scenarios, quotas used as examples, latency figures, architectures, and readiness criteria are original teaching examples. No actual employer requirement or provider quota is asserted.
- No live model service was called. The local lab demonstrates only its own documented behavior.
- Source-level checks cover terminology and important protocol distinctions. They do not certify each recommendation as universally appropriate to every cloud, SDK, or provider.
- Browser visual verification was unavailable. Static structure/link checks, JavaScript checks, calculator cases, and actual loopback protocol experiments are recorded separately in the completion report.

## Rebuilding

Original prose: `scripts/course_content.py` and `scripts/reference_pages.py`. Glossary: `scripts/make_glossary.py`. The builder adds first-mention glossary links to lesson prose without modifying code examples or existing hyperlinks. Generated pages contain full lesson prose, so no runtime content fetch is needed.
