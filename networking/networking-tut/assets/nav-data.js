window.NAV = [
  {
    "module": "Start here",
    "pages": [
      {
        "path": "index.html",
        "title": "Course home",
        "n": "",
        "kw": "overview"
      }
    ]
  },
  {
    "module": "0 \u00b7 The professional baseline",
    "pages": [
      {
        "n": "00",
        "path": "pages/00-orientation.html",
        "title": "What networking competence looks like",
        "kw": "beginner employable professional readiness learning path"
      }
    ]
  },
  {
    "module": "1 \u00b7 Follow one request",
    "pages": [
      {
        "n": "01",
        "path": "pages/01-request-journey.html",
        "title": "Follow an eval request",
        "kw": "layers packets host client server protocol request journey OSI"
      },
      {
        "n": "02",
        "path": "pages/02-addresses-and-ports.html",
        "title": "Addresses, ports, and localhost",
        "kw": "localhost loopback IPv4 IPv6 socket bind listener port URL five tuple"
      },
      {
        "n": "03",
        "path": "pages/03-ip-and-routing.html",
        "title": "IP, subnets, and routes",
        "kw": "CIDR subnet mask routing private public gateway NAT IPv6 ARP switch MTU"
      }
    ]
  },
  {
    "module": "2 \u00b7 The application stack",
    "pages": [
      {
        "n": "04",
        "path": "pages/04-dns.html",
        "title": "DNS: names, answers, and context",
        "kw": "DNS resolver cache TTL A AAAA CNAME NXDOMAIN SERVFAIL VPN split horizon"
      },
      {
        "n": "05",
        "path": "pages/05-transport.html",
        "title": "TCP, UDP, and QUIC",
        "kw": "TCP UDP QUIC sockets handshake pool connection reset refusal retransmission flow congestion"
      },
      {
        "n": "06",
        "path": "pages/06-tls.html",
        "title": "TLS: encryption and identity",
        "kw": "TLS HTTPS SSL certificates SNI mTLS trust CA encryption authentication authorization"
      },
      {
        "n": "07",
        "path": "pages/07-http.html",
        "title": "HTTP: read the actual exchange",
        "kw": "HTTP REST API status headers JSON 401 403 429 502 504 gRPC CORS"
      },
      {
        "n": "08",
        "path": "pages/08-streaming.html",
        "title": "Streaming and partial responses",
        "kw": "SSE streaming TTFT first token partial response buffering WebSocket cancellation"
      }
    ]
  },
  {
    "module": "3 \u00b7 Make runs reliable",
    "pages": [
      {
        "n": "09",
        "path": "pages/09-latency-and-throughput.html",
        "title": "Latency, throughput, and bottlenecks",
        "kw": "latency throughput bandwidth RTT p50 p95 p99 percentiles Little law bottleneck BDP"
      },
      {
        "n": "10",
        "path": "pages/10-concurrency-and-limits.html",
        "title": "Concurrency, queues, and rate limits",
        "kw": "concurrency rate limit quota 429 semaphore async queues backpressure token budget"
      },
      {
        "n": "11",
        "path": "pages/11-timeouts-and-retries.html",
        "title": "Timeouts, retries, and uncertain outcomes",
        "kw": "timeout deadline retries exponential backoff jitter idempotency ambiguous result cancellation"
      }
    ]
  },
  {
    "module": "4 \u00b7 Navigate infrastructure",
    "pages": [
      {
        "n": "12",
        "path": "pages/12-proxies-and-load-balancers.html",
        "title": "Proxies, gateways, and load balancers",
        "kw": "reverse proxy forward proxy API gateway load balancer ingress health checks 502 504 413"
      },
      {
        "n": "13",
        "path": "pages/13-cloud-networks.html",
        "title": "Cloud networks without the mystery",
        "kw": "VPC subnet cloud AWS security group NACL private public egress NAT VPN endpoint region availability zone"
      },
      {
        "n": "14",
        "path": "pages/14-containers.html",
        "title": "Containers: whose network is this?",
        "kw": "Docker container bridge namespace localhost publish EXPOSE port mapping host"
      },
      {
        "n": "15",
        "path": "pages/15-kubernetes.html",
        "title": "Read a Kubernetes network diagram",
        "kw": "Kubernetes k8s Pod Service ClusterIP EndpointSlice ingress Gateway namespace NetworkPolicy kubectl"
      },
      {
        "n": "16",
        "path": "pages/16-inference-and-locality.html",
        "title": "Where the model runs changes the network",
        "kw": "GPU inference serving data parallel tensor parallel pipeline NCCL RDMA InfiniBand locality region"
      }
    ]
  },
  {
    "module": "5 \u00b7 Investigate failures",
    "pages": [
      {
        "n": "17",
        "path": "pages/17-diagnostic-method.html",
        "title": "A diagnostic method you can repeat",
        "kw": "debug troubleshoot curl ping traceroute MTU connection timeout diagnosis runbook incident"
      },
      {
        "n": "18",
        "path": "pages/18-observability.html",
        "title": "Collect evidence that explains an eval",
        "kw": "observability logs metrics traces spans trace ID request ID telemetry cardinality outcomes denominators"
      }
    ]
  },
  {
    "module": "6 \u00b7 Practice on a real service",
    "pages": [
      {
        "n": "19",
        "path": "pages/19-local-lab.html",
        "title": "Lab: observe a real HTTP service",
        "kw": "hands on lab local curl Python HTTP timeout stream 429 503 experiment"
      },
      {
        "n": "20",
        "path": "pages/20-incident-practice.html",
        "title": "Practice: four infrastructure incidents",
        "kw": "incidents practice debugging interview case study outage selection bias"
      }
    ]
  },
  {
    "module": "7 \u00b7 Design and defend",
    "pages": [
      {
        "n": "21",
        "path": "pages/21-design-an-eval-system.html",
        "title": "Design an eval system you can explain",
        "kw": "architecture design queue worker fleet scheduler storage reliability retries circuit breaker"
      },
      {
        "n": "22",
        "path": "pages/22-boundaries-and-validity.html",
        "title": "Trust boundaries and eval validity",
        "kw": "agent sandbox egress security trust boundaries leakage SSRF validity network permissions score denominator"
      },
      {
        "n": "23",
        "path": "pages/23-readiness-review.html",
        "title": "Capstone: explain, diagnose, and defend",
        "kw": "capstone readiness interview professional assessment design review employable"
      }
    ]
  },
  {
    "module": "Reference & practice",
    "pages": [
      {
        "path": "glossary.html",
        "title": "Glossary",
        "n": "G",
        "kw": "terms definitions vocabulary glossary"
      },
      {
        "path": "appendices/a-calculators.html",
        "title": "Network calculators",
        "n": "A",
        "kw": "CIDR calculator bandwidth throughput latency concurrency subnet math"
      },
      {
        "path": "appendices/b-commands.html",
        "title": "Command reference",
        "n": "B",
        "kw": "commands curl dig ping traceroute lsof ss route timing exit codes"
      },
      {
        "path": "appendices/c-reading-map.html",
        "title": "A focused route through the book",
        "n": "C",
        "kw": "Systems Approach book textbook reading map chapters deeper study"
      },
      {
        "path": "bibliography.html",
        "title": "Annotated bibliography",
        "n": "R",
        "kw": "sources bibliography citations reference provenance attribution license"
      }
    ]
  }
];
