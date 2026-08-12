/* REBASH Academy — interactive tools (client-side only) */
(function () {
  "use strict";

  function toolSlug() {
    var parts = (window.location.pathname || "").replace(/\/+$/, "").split("/");
    var i = parts.indexOf("tools");
    if (i < 0 || !parts[i + 1] || parts[i + 1] === "index.html") return null;
    return parts[i + 1];
  }

  function articleRoot() {
    return (
      document.querySelector("article.md-content__inner") ||
      document.querySelector(".md-content__inner")
    );
  }

  /* -------------------------------------------------------------------------- */
  /* IPv4 helpers                                                                */
  /* -------------------------------------------------------------------------- */

  function parseIPv4(str) {
    if (!str || typeof str !== "string") return null;
    var s = str.trim();
    var m = s.match(/^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$/);
    if (!m) return null;
    var oct = [];
    for (var i = 1; i <= 4; i++) {
      var n = Number(m[i]);
      if (!Number.isInteger(n) || n < 0 || n > 255) return null;
      if (String(n) !== m[i] && m[i].length > 1 && m[i][0] === "0") return null;
      oct.push(n);
    }
    return ((oct[0] << 24) >>> 0) + (oct[1] << 16) + (oct[2] << 8) + oct[3];
  }

  function ipToString(num) {
    return [
      (num >>> 24) & 255,
      (num >>> 16) & 255,
      (num >>> 8) & 255,
      num & 255,
    ].join(".");
  }

  function maskFromCidr(cidr) {
    if (cidr <= 0) return 0;
    if (cidr >= 32) return 0xffffffff >>> 0;
    return (0xffffffff << (32 - cidr)) >>> 0;
  }

  function cidrFromMask(mask) {
    var bits = 0;
    var m = mask >>> 0;
    var seenZero = false;
    for (var i = 31; i >= 0; i--) {
      var bit = (m >>> i) & 1;
      if (bit === 1) {
        if (seenZero) return null;
        bits++;
      } else {
        seenZero = true;
      }
    }
    return bits;
  }

  function octetBinary(n) {
    return n.toString(2).padStart(8, "0");
  }

  function ipBinaryOctets(num) {
    return [
      octetBinary((num >>> 24) & 255),
      octetBinary((num >>> 16) & 255),
      octetBinary((num >>> 8) & 255),
      octetBinary(num & 255),
    ];
  }

  function addressClass(ip) {
    var first = (ip >>> 24) & 255;
    if (first <= 127) return "Class A";
    if (first <= 191) return "Class B";
    if (first <= 223) return "Class C";
    if (first <= 239) return "Class D (multicast)";
    return "Class E (reserved)";
  }

  function addressScope(ip) {
    var a = (ip >>> 24) & 255;
    var b = (ip >>> 16) & 255;
    if (a === 10) return "Private";
    if (a === 172 && b >= 16 && b <= 31) return "Private";
    if (a === 192 && b === 168) return "Private";
    if (a === 127) return "Loopback";
    if (a === 169 && b === 254) return "Link-local";
    if (a >= 224 && a <= 239) return "Multicast";
    if (a >= 240) return "Reserved";
    if (ip === 0) return "This network";
    return "Public";
  }

  function networkContext(ip) {
    var a = (ip >>> 24) & 255;
    var b = (ip >>> 16) & 255;
    if (a === 10) {
      return {
        label: "Typical AWS / GCP / Azure VPC",
        detail: "10.0.0.0/8 is the most common private range for cloud VPCs and large enterprises.",
      };
    }
    if (a === 172 && b >= 16 && b <= 31) {
      return {
        label: "Common enterprise network",
        detail: "172.16.0.0/12 is widely used for corporate LANs and data-centre overlays.",
      };
    }
    if (a === 192 && b === 168) {
      return {
        label: "Typical home / lab router",
        detail: "192.168.0.0/16 is the default on most home routers and small office networks.",
      };
    }
    if (a === 127) {
      return {
        label: "Loopback",
        detail: "127.0.0.0/8 always refers to this host — not a routable network.",
      };
    }
    if (a === 169 && b === 254) {
      return {
        label: "Link-local (APIPA)",
        detail: "169.254.0.0/16 is used for automatic addressing when DHCP fails.",
      };
    }
    if (addressScope(ip) === "Public") {
      return {
        label: "Public address space",
        detail: "This address is in publicly routable space — treat it as internet-facing.",
      };
    }
    return null;
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function copyPlain(text, btn) {
    if (!text || !navigator.clipboard) return;
    navigator.clipboard.writeText(text).then(function () {
      if (!btn) return;
      btn.classList.add("ra-tool__copy--done");
      if (btn.querySelector("svg")) {
        var prevLabel = btn.getAttribute("aria-label") || "Copy";
        btn.setAttribute("aria-label", "Copied");
        window.setTimeout(function () {
          btn.setAttribute("aria-label", prevLabel);
          btn.classList.remove("ra-tool__copy--done");
        }, 1200);
        return;
      }
      var prev = btn.textContent;
      btn.textContent = "Copied";
      window.setTimeout(function () {
        btn.textContent = prev;
        btn.classList.remove("ra-tool__copy--done");
      }, 1200);
    });
  }

  function blockSizeForCidr(cidr) {
    if (cidr >= 32) return 1;
    if (cidr >= 24) return Math.pow(2, 32 - cidr);
    if (cidr >= 16) return Math.pow(2, 24 - cidr);
    if (cidr >= 8) return Math.pow(2, 16 - cidr);
    return Math.pow(2, 8 - cidr);
  }

  /* Live chrome bottom — avoids overlapping sticky breadcrumbs when scrolling. */
  function stickyTopOffset() {
    var path = document.querySelector(".md-path.ra-path");
    if (path && !path.hasAttribute("hidden")) {
      var bottom = path.getBoundingClientRect().bottom;
      if (bottom > 0) return Math.ceil(bottom) + 6;
    }
    var header = document.querySelector(".md-header");
    if (header) {
      return Math.ceil(header.getBoundingClientRect().bottom) + 6;
    }
    return 72;
  }

  /* Keep the input tile pinned while reading results / cheat sheet below. */
  function pinComposer(composer) {
    if (!composer || composer.dataset.raPinned === "1") return;
    composer.dataset.raPinned = "1";

    var placeholder = document.createElement("div");
    placeholder.className = "ra-tool__composer-ph";
    placeholder.setAttribute("aria-hidden", "true");
    composer.parentNode.insertBefore(placeholder, composer);

    var stuck = false;

    function applyFixed() {
      var top = stickyTopOffset();
      var rect = placeholder.getBoundingClientRect();
      composer.classList.add("ra-tool__composer--fixed");
      composer.style.top = top + "px";
      composer.style.left = Math.round(rect.left) + "px";
      composer.style.width = Math.round(rect.width) + "px";
      placeholder.style.height = composer.offsetHeight + "px";
    }

    function clearFixed() {
      composer.classList.remove("ra-tool__composer--fixed");
      composer.style.top = "";
      composer.style.left = "";
      composer.style.width = "";
      placeholder.style.height = "0px";
    }

    function sync() {
      var top = stickyTopOffset();
      if (!stuck) {
        var y = composer.getBoundingClientRect().top;
        if (y <= top) {
          stuck = true;
          placeholder.style.height = composer.offsetHeight + "px";
          applyFixed();
        }
      } else {
        /* Hysteresis: unpin only once the natural spot is clearly below chrome */
        var phTop = placeholder.getBoundingClientRect().top;
        if (phTop > top + 2) {
          stuck = false;
          clearFixed();
        } else {
          applyFixed();
        }
      }
    }

    window.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    if (typeof ResizeObserver !== "undefined") {
      var ro = new ResizeObserver(function () {
        if (stuck) applyFixed();
      });
      ro.observe(composer);
    }
    window.requestAnimationFrame(sync);
  }

  function calculateSubnet(ipNum, cidr) {
    var mask = maskFromCidr(cidr);
    var wildcard = ~mask >>> 0;
    var network = (ipNum & mask) >>> 0;
    var broadcast = (network | wildcard) >>> 0;
    var total = Math.pow(2, 32 - cidr);
    var usableHosts;
    var firstHost = null;
    var lastHost = null;
    var hostNote = "";

    if (cidr === 32) {
      usableHosts = 1;
      firstHost = network;
      lastHost = network;
      hostNote = "/32 is a single-host route — network and host are the same address.";
    } else if (cidr === 31) {
      usableHosts = 2;
      firstHost = network;
      lastHost = broadcast;
      hostNote =
        "/31 (RFC 3021) uses both addresses for point-to-point links — no classic network/broadcast reservation.";
    } else {
      usableHosts = Math.max(total - 2, 0);
      if (usableHosts > 0) {
        firstHost = (network + 1) >>> 0;
        lastHost = (broadcast - 1) >>> 0;
      }
    }

    return {
      ip: ipNum,
      cidr: cidr,
      mask: mask,
      wildcard: wildcard,
      network: network,
      broadcast: broadcast,
      total: total,
      usableHosts: usableHosts,
      firstHost: firstHost,
      lastHost: lastHost,
      hostNote: hostNote,
      addressClass: addressClass(ipNum),
      scope: addressScope(ipNum),
      networkBits: cidr,
      hostBits: 32 - cidr,
      blockSize: blockSizeForCidr(cidr),
    };
  }

  var COMMON_MASKS = (function () {
    var list = [];
    for (var c = 32; c >= 8; c--) {
      list.push({ cidr: c, mask: ipToString(maskFromCidr(c)) });
    }
    return list;
  })();

  /* -------------------------------------------------------------------------- */
  /* Subnet Calculator UI                                                        */
  /* -------------------------------------------------------------------------- */

  function initSubnetCalculator() {
    var mount = document.getElementById("ra-tool-subnet");
    if (!mount || mount.dataset.raReady === "1") return;
    mount.dataset.raReady = "1";
    mount.classList.add("ra-tool", "ra-tool--subnet");


    var EXAMPLES = [
      { id: "home", label: "Home Network", ip: "192.168.1.10", cidr: 24, primary: true },
      { id: "aws", label: "AWS VPC", ip: "10.0.1.25", cidr: 16, primary: true },
      { id: "k8s", label: "Kubernetes", ip: "10.244.1.12", cidr: 16, primary: true },
      { id: "wan", label: "WAN /30", ip: "203.0.113.1", cidr: 30, primary: true },
      { id: "enterprise", label: "Enterprise", ip: "172.16.40.55", cidr: 20, primary: false },
      { id: "lab", label: "Lab /29", ip: "192.168.10.1", cidr: 29, primary: false },
      { id: "host", label: "Single host /32", ip: "198.51.100.10", cidr: 32, primary: false },
    ];

    var maskOptions = COMMON_MASKS.map(function (m) {
      return (
        '<option value="' +
        m.cidr +
        '"' +
        (m.cidr === 16 ? " selected" : "") +
        ">" +
        m.mask +
        " (/" +
        m.cidr +
        ")</option>"
      );
    }).join("");

    var cidrOptions = "";
    for (var c = 32; c >= 0; c--) {
      cidrOptions +=
        '<option value="' +
        c +
        '"' +
        (c === 16 ? " selected" : "") +
        ">/" +
        c +
        "</option>";
    }

    var primaryChips = EXAMPLES.filter(function (ex) {
      return ex.primary;
    })
      .map(function (ex) {
        return (
          '<button type="button" class="ra-tool__chip" data-ra-example="' +
          ex.id +
          '">' +
          escapeHtml(ex.label) +
          "</button>"
        );
      })
      .join("");

    var moreOptions = EXAMPLES.filter(function (ex) {
      return !ex.primary;
    })
      .map(function (ex) {
        return (
          '<option value="' +
          ex.id +
          '">' +
          escapeHtml(ex.label) +
          "</option>"
        );
      })
      .join("");

    mount.innerHTML =
      '<header class="ra-tool__masthead">' +
      '<div class="ra-tool__masthead-top">' +
      '<div class="ra-tool__title-row">' +
      '<h2 class="ra-tool__title">Subnet Calculator</h2>' +
      '<span class="ra-tool__badge">IPv4</span>' +
      "</div>" +
      '<ul class="ra-tool__trust">' +
      "<li>Client-side</li>" +
      "<li>No data uploaded</li>" +
      "<li>RFC 3021 /31 &amp; /32</li>" +
      "<li>Instant results</li>" +
      "</ul>" +
      "</div>" +
      '<p class="ra-tool__subtitle">Calculate network address, broadcast address, host range, subnet mask, and more.</p>' +
      "</header>" +
      '<div class="ra-tool__composer" role="region" aria-label="Subnet calculator inputs">' +
      '<form class="ra-tool__form" novalidate>' +
      '<div class="ra-tool__fields">' +
      '<label class="ra-tool__field ra-tool__field--ip">' +
      '<span class="ra-tool__field-label">IP Address</span>' +
      '<span class="ra-tool__input">' +
      '<svg class="ra-tool__ico ra-tool__ico--field" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M15 20a1 1 0 0 0 1-1v-2h2a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2V5a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v2H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2v2a1 1 0 0 0 1 1h6M10 6h4v2h-4V6m-4 5h12v4H6v-4m4 6h4v2h-4v-2Z"/></svg>' +
      '<input type="text" name="ip" inputmode="decimal" autocomplete="off" spellcheck="false" placeholder="192.168.1.0" value="192.168.1.0" aria-label="IP address" aria-describedby="ra-subnet-error">' +
      "</span>" +
      "</label>" +
      '<label class="ra-tool__field ra-tool__field--cidr">' +
      '<span class="ra-tool__field-label">CIDR</span>' +
      '<span class="ra-tool__select">' +
      '<select name="cidr" aria-label="CIDR prefix length">' +
      cidrOptions +
      "</select>" +
      "</span>" +
      "</label>" +
      '<span class="ra-tool__or" aria-hidden="true">or</span>' +
      '<label class="ra-tool__field ra-tool__field--mask">' +
      '<span class="ra-tool__field-label">Subnet Mask</span>' +
      '<span class="ra-tool__select">' +
      '<select name="mask" aria-label="Subnet mask">' +
      maskOptions +
      "</select>" +
      "</span>" +
      "</label>" +
      "</div>" +
      '<div class="ra-tool__footer-row">' +
      '<div class="ra-tool__actions">' +
      '<button type="submit" class="ra-tool__btn ra-tool__btn--primary">' +
      '<svg class="ra-tool__ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 2h10a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2m0 2v4h10V4H7m0 6v2h2v-2H7m4 0v2h2v-2h-2m4 0v2h2v-2h-2m-8 4v2h2v-2H7m4 0v2h2v-2h-2m4 0v2h2v-2h-2m-8 4v2h2v-2H7m4 0v2h2v-2h-2m4 0v2h2v-2h-2Z"/></svg>' +
      "<span>Calculate</span></button>" +
      '<button type="button" class="ra-tool__btn ra-tool__btn--ghost" data-ra-reset>' +
      '<svg class="ra-tool__ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 5V1L7 6l5 5V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8Z"/></svg>' +
      "<span>Reset</span></button>" +
      '<button type="button" class="ra-tool__btn ra-tool__btn--ghost" data-ra-random>' +
      '<svg class="ra-tool__ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14.83 13.41 13.42 14.82 16.55 17.95 14 20.5V22h8v-8h-1.5l2.54 2.55-3.54 3.54-1.41-1.41 2.55-2.54-3.13-3.14m2.72-8.96L14 2v1.5l2.55 2.54L13.41 9.17l1.41 1.41 3.14-3.13L20.5 10H22V2h-8v1.5l2.55-2.05M10.59 9.17 5.05 3.63 3.63 5.05l5.54 5.54 1.42-1.42M9.17 13.41 3.63 18.95l1.42 1.42 5.54-5.54-1.42-1.42Z"/></svg>' +
      "<span>Random Example</span></button>" +
      "</div>" +
      '<div class="ra-tool__examples">' +
      '<span class="ra-tool__examples-label">Examples:</span>' +
      '<div class="ra-tool__chips">' +
      primaryChips +
      '<label class="ra-tool__more">' +
      '<span class="ra-tool__more-label">More</span>' +
      '<select data-ra-more aria-label="More examples">' +
      '<option value="">More</option>' +
      moreOptions +
      "</select></label>" +
      "</div></div></div>" +
      '<p class="ra-tool__error" id="ra-subnet-error" hidden></p>' +
      "</form>" +
      "</div>" +
      '<div class="ra-tool__strip" data-ra-strip hidden></div>' +
      '<div class="ra-tool__results" data-ra-results hidden></div>';

    var form = mount.querySelector("form");
    var ipInput = form.querySelector('[name="ip"]');
    var cidrSelect = form.querySelector('[name="cidr"]');
    var maskSelect = form.querySelector('[name="mask"]');
    var errorEl = mount.querySelector("#ra-subnet-error");
    var stripEl = mount.querySelector("[data-ra-strip]");
    var resultsEl = mount.querySelector("[data-ra-results]");
    var syncing = false;
    var lastText = "";
    var activeTab = "summary";

    function findExample(id) {
      for (var i = 0; i < EXAMPLES.length; i++) {
        if (EXAMPLES[i].id === id) return EXAMPLES[i];
      }
      return null;
    }

    function scrollToToolView() {
      window.requestAnimationFrame(function () {
        var top = stickyTopOffset();
        var y =
          mount.getBoundingClientRect().top + window.pageYOffset - top - 8;
        window.scrollTo({
          top: Math.max(0, Math.round(y)),
          behavior: "smooth",
        });
      });
    }

    function revealSummaryView() {
      activeTab = "summary";
      run();
      scrollToToolView();
    }

    function applyExample(ex) {
      if (!ex) return;
      ipInput.value = ex.ip;
      cidrSelect.value = String(ex.cidr);
      syncCidrToMask();
      revealSummaryView();
    }

    function showError(msg) {
      errorEl.hidden = !msg;
      errorEl.textContent = msg || "";
      if (msg) {
        stripEl.hidden = true;
        resultsEl.hidden = true;
      }
    }

    function syncCidrToMask() {
      syncing = true;
      maskSelect.value = String(cidrSelect.value);
      syncing = false;
    }

    function syncMaskToCidr() {
      syncing = true;
      cidrSelect.value = String(maskSelect.value);
      syncing = false;
    }

    cidrSelect.addEventListener("change", function () {
      if (!syncing) syncCidrToMask();
    });
    maskSelect.addEventListener("change", function () {
      if (!syncing) syncMaskToCidr();
    });

    function readQuery() {
      try {
        var q = new URLSearchParams(window.location.search);
        var ip = q.get("ip");
        var cidr = q.get("cidr");
        var mask = q.get("mask");
        if (ip) ipInput.value = ip;
        if (cidr !== null && cidr !== "" && !Number.isNaN(Number(cidr))) {
          cidrSelect.value = String(Math.max(0, Math.min(32, Number(cidr))));
          syncCidrToMask();
        } else if (mask) {
          var mn = parseIPv4(mask);
          var bits = mn === null ? null : cidrFromMask(mn);
          if (bits !== null) {
            cidrSelect.value = String(bits);
            syncCidrToMask();
          }
        }
      } catch (e) {
        /* ignore */
      }
    }

    function writeQuery(ip, cidr) {
      try {
        var url = new URL(window.location.href);
        url.searchParams.set("ip", ip);
        url.searchParams.set("cidr", String(cidr));
        url.searchParams.delete("mask");
        if (history.replaceState) {
          history.replaceState(null, "", url.pathname + url.search + url.hash);
        }
      } catch (e) {
        /* ignore */
      }
    }

    function timelineStops(r) {
      var stops = [];
      var seen = {};

      function add(stop) {
        if (stop.ip === null || stop.ip === undefined) return;
        var key = String(stop.ip >>> 0);
        if (seen[key] && !stop.yours) return;
        if (seen[key] && stop.yours) {
          for (var i = 0; i < stops.length; i++) {
            if ((stops[i].ip >>> 0) === (stop.ip >>> 0)) {
              stops[i] = stop;
              return;
            }
          }
        }
        seen[key] = true;
        stops.push(stop);
      }

      if (r.cidr >= 31) {
        if (r.cidr === 32) {
          add({
            role: "yours",
            label: "Your IP",
            ip: r.ip,
            yours: true,
            marker: "star",
          });
          return stops;
        }
        add({
          role: "network",
          label: "Point-to-point",
          ip: r.network,
          yours: r.ip === r.network,
          marker: r.ip === r.network ? "star" : "net",
        });
        if (r.broadcast !== r.network) {
          add({
            role: r.ip === r.broadcast ? "yours" : "host",
            label: r.ip === r.broadcast ? "Your IP" : "Peer",
            ip: r.broadcast,
            yours: r.ip === r.broadcast,
            marker: r.ip === r.broadcast ? "star" : "host",
          });
        }
        return stops;
      }

      add({
        role: "network",
        label: "Network",
        ip: r.network,
        yours: false,
        marker: "net",
      });

      var gateway = r.firstHost;
      if (gateway !== null) {
        if (r.ip === gateway) {
          add({
            role: "yours",
            label: "Your IP (gateway)",
            ip: gateway,
            yours: true,
            marker: "star",
          });
        } else {
          add({
            role: "gateway",
            label: "Gateway (typical)",
            ip: gateway,
            yours: false,
            marker: "gateway",
          });
        }
      }

      if (
        r.ip !== r.network &&
        r.ip !== r.broadcast &&
        r.ip !== gateway
      ) {
        add({
          role: "yours",
          label: "Your IP",
          ip: r.ip,
          yours: true,
          marker: "star",
        });
      } else if (r.ip === r.network) {
        stops[0] = {
          role: "yours",
          label: "Your IP (network)",
          ip: r.network,
          yours: true,
          marker: "star",
        };
        seen[String(r.network >>> 0)] = true;
      }

      var mid = null;
      if (r.usableHosts >= 4 && r.lastHost !== null) {
        mid = (r.network + Math.floor(r.total / 2) + 10) >>> 0;
        if (mid > r.lastHost) mid = r.lastHost;
        if (
          mid !== r.ip &&
          mid !== gateway &&
          mid !== r.broadcast &&
          mid !== r.network &&
          mid >= (r.firstHost || 0) &&
          mid <= r.lastHost
        ) {
          add({
            role: "example",
            label: "Example Host",
            ip: mid,
            yours: false,
            marker: "host",
          });
        }
      }

      if (
        r.lastHost !== null &&
        r.lastHost !== r.ip &&
        r.lastHost !== gateway &&
        r.lastHost !== mid
      ) {
        add({
          role: "last",
          label: "Last Usable Host",
          ip: r.lastHost,
          yours: false,
          marker: "host",
        });
      }

      add({
        role: "broadcast",
        label: "Broadcast",
        ip: r.broadcast,
        yours: r.ip === r.broadcast,
        marker: r.ip === r.broadcast ? "star" : "broadcast",
      });

      return stops;
    }

    function binaryRow(label, num, cidr) {
      var octets = ipBinaryOctets(num);
      var html =
        '<div class="ra-tool__bin-row">' +
        '<div class="ra-tool__bin-label">' +
        "<span>" +
        escapeHtml(label) +
        "</span>" +
        '<span class="ra-tool__bin-ip">' +
        ipToString(num) +
        "</span></div>" +
        '<div class="ra-tool__bin-octets" aria-label="Binary octets">';
      for (var o = 0; o < 4; o++) {
        var start = o * 8;
        var end = start + 8;
        var netBits = 0;
        for (var b = start; b < end; b++) {
          if (b < cidr) netBits++;
        }
        var tone =
          netBits === 8 ? "net" : netBits === 0 ? "host" : "mixed";
        var mixedStyle =
          tone === "mixed"
            ? ' style="--ra-bin-split:' + (netBits / 8) * 100 + '%"'
            : "";
        html +=
          '<div class="ra-tool__bin-octet ra-tool__bin-octet--' +
          tone +
          '"' +
          mixedStyle +
          ">";
        for (var i = 0; i < 8; i++) {
          var bitIndex = start + i;
          var isNet = bitIndex < cidr;
          html +=
            '<span class="ra-tool__bit' +
            (isNet ? " ra-tool__bit--net" : " ra-tool__bit--host") +
            '">' +
            octets[o][i] +
            "</span>";
        }
        html += "</div>";
      }
      html += "</div></div>";
      return html;
    }

    function calcStep(line, sub) {
      return (
        '<div class="ra-tool__calc-step" role="listitem">' +
        '<span class="ra-tool__calc-line">' +
        line +
        "</span>" +
        (sub
          ? '<span class="ra-tool__calc-sub">' + sub + "</span>"
          : "") +
        "</div>"
      );
    }

    function explainSubnet(r) {
      var totalStr = r.total.toLocaleString("en-GB");
      var usableStr = r.usableHosts.toLocaleString("en-GB");
      var steps = [];

      steps.push(calcStep("CIDR = <strong>/" + r.cidr + "</strong>"));
      steps.push(
        calcStep(
          "Network bits = <strong>" +
            r.networkBits +
            "</strong> · Host bits = <strong>" +
            r.hostBits +
            "</strong>"
        )
      );
      steps.push(
        calcStep(
          "Total addresses = 2<sup>" +
            r.hostBits +
            "</sup> = <strong>" +
            totalStr +
            "</strong>"
        )
      );

      if (r.cidr <= 30) {
        steps.push(
          calcStep(
            "Usable hosts = " +
              totalStr +
              " − 2 = <strong>" +
              usableStr +
              "</strong>"
          )
        );
      } else if (r.cidr === 31) {
        steps.push(
          calcStep(
            "Usable hosts = <strong>" +
              totalStr +
              "</strong> (RFC 3021 point-to-point — no network/broadcast reserve)"
          )
        );
      } else {
        steps.push(
          calcStep("Usable hosts = <strong>1</strong> (single-host /32 route)")
        );
      }

      steps.push(
        calcStep(
          "Network = IP AND Mask",
          ipToString(r.ip) +
            " AND " +
            ipToString(r.mask) +
            " = <strong>" +
            ipToString(r.network) +
            "</strong>"
        )
      );

      if (r.cidr < 31) {
        steps.push(
          calcStep(
            "Broadcast = Network OR Wildcard",
            ipToString(r.network) +
              " OR " +
              ipToString(r.wildcard) +
              " = <strong>" +
              ipToString(r.broadcast) +
              "</strong>"
          )
        );
      } else if (r.cidr === 31) {
        steps.push(
          calcStep(
            "Addresses = <strong>" +
              ipToString(r.network) +
              "</strong> and <strong>" +
              ipToString(r.broadcast) +
              "</strong>",
            "/31 has no classic broadcast address"
          )
        );
      }

      return (
        '<div class="ra-tool__tile ra-tool__explain-panel">' +
        '<h3 class="ra-tool__explain-title">Calculation Steps</h3>' +
        '<div class="ra-tool__calc-steps" role="list">' +
        steps.join("") +
        "</div></div>"
      );
    }

    function vizMarker(marker) {
      if (marker === "net") {
        return (
          '<span class="ra-tool__timeline-badge ra-tool__timeline-badge--net" aria-hidden="true">N</span>'
        );
      }
      if (marker === "broadcast") {
        return (
          '<span class="ra-tool__timeline-badge ra-tool__timeline-badge--broadcast" aria-hidden="true">B</span>'
        );
      }
      if (marker === "star") {
        return (
          '<span class="ra-tool__timeline-badge ra-tool__timeline-badge--star" aria-hidden="true">' +
          '<svg viewBox="0 0 24 24" width="14" height="14" focusable="false">' +
          '<path fill="currentColor" d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>' +
          "</svg></span>"
        );
      }
      return (
        '<span class="ra-tool__timeline-dot ra-tool__timeline-dot--' +
        escapeHtml(marker) +
        '" aria-hidden="true"></span>'
      );
    }

    function renderViz(r) {
      var stops = timelineStops(r);
      var html =
        '<div class="ra-tool__tile ra-tool__viz-panel">' +
        '<h3 class="ra-tool__viz-title">Network Visualisation</h3>' +
        '<div class="ra-tool__timeline" role="list" aria-label="Addresses in this subnet">';
      stops.forEach(function (s) {
        html +=
          '<div class="ra-tool__timeline-item ra-tool__timeline-item--' +
          escapeHtml(s.role) +
          (s.yours ? " ra-tool__timeline-item--yours" : "") +
          '" role="listitem">' +
          '<div class="ra-tool__timeline-rail">' +
          vizMarker(s.marker) +
          "</div>" +
          '<div class="ra-tool__timeline-body">' +
          '<span class="ra-tool__timeline-label">' +
          escapeHtml(s.label) +
          "</span>" +
          '<span class="ra-tool__timeline-ip">' +
          ipToString(s.ip) +
          "</span>" +
          "</div></div>";
      });
      html += "</div></div>";
      return html;
    }

    function bindResultsUi() {
      resultsEl.querySelectorAll("[data-ra-copy-val]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          copyPlain(btn.getAttribute("data-ra-copy-val") || "", btn);
        });
      });
      var summaryCopy = resultsEl.querySelector("[data-ra-copy-summary]");
      if (summaryCopy) {
        summaryCopy.addEventListener("click", function () {
          copyPlain(lastText, summaryCopy);
        });
      }
      resultsEl.querySelectorAll("[data-ra-tab]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          activeTab = btn.getAttribute("data-ra-tab") || "summary";
          resultsEl.querySelectorAll("[data-ra-tab]").forEach(function (b) {
            var on = b === btn;
            b.classList.toggle("ra-tool__tab--active", on);
            b.setAttribute("aria-selected", on ? "true" : "false");
          });
          resultsEl.querySelectorAll("[data-ra-panel]").forEach(function (p) {
            p.hidden = p.getAttribute("data-ra-panel") !== activeTab;
          });
        });
      });
    }

    function render(r) {
      var rangePlain =
        r.firstHost === null
          ? "—"
          : r.firstHost === r.lastHost
            ? ipToString(r.firstHost)
            : ipToString(r.firstHost) + " – " + ipToString(r.lastHost);
      var rangeHtml =
        r.firstHost === null
          ? "—"
          : r.firstHost === r.lastHost
            ? escapeHtml(ipToString(r.firstHost))
            : '<span class="ra-tool__range ra-tool__range--stack">' +
              "<span>" +
              escapeHtml(ipToString(r.firstHost)) +
              "</span>" +
              '<span class="ra-tool__range-arrow" aria-hidden="true">↓</span>' +
              "<span>" +
              escapeHtml(ipToString(r.lastHost)) +
              "</span></span>";
      var ctx = networkContext(r.ip);
      var cidrStr = ipToString(r.network) + "/" + r.cidr;
      var scopeSub =
        r.scope === "Private" ? "RFC 1918" : r.scope === "Public" ? "Routable" : "";

      var ICO = {
        network:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.9 17.39A7.93 7.93 0 0 0 20 12c0-1.54-.44-2.98-1.2-4.2l-2.12 2.12A5 5 0 0 1 17 12c0 1.1-.36 2.12-.97 2.95l1.87 2.44M12 19a7 7 0 0 1-5.66-2.95l-2.12 2.12A8.96 8.96 0 0 0 12 21c1.86 0 3.58-.56 5.01-1.52l-2.12-2.12c-.86.41-1.84.64-2.89.64m0-14c1.05 0 2.03.23 2.89.64l2.12-2.12A8.96 8.96 0 0 0 12 3a8.96 8.96 0 0 0-7.78 4.17l2.12 2.12A7 7 0 0 1 12 5m-5.9.61L4.22 3.17A8.96 8.96 0 0 0 3 12c0 1.95.62 3.75 1.68 5.22l2.12-2.12A7 7 0 0 1 5 12c0-1.54.5-2.96 1.34-4.1l-.24-.29Z"/></svg>',
        broadcast:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a3 3 0 0 1 3 3c0 1.3-.84 2.4-2 2.82V9h5a1 1 0 0 1 1 1v2.18c1.16.41 2 1.51 2 2.82a3 3 0 1 1-5.82-1H12v2.18A2.99 2.99 0 0 1 15 19a3 3 0 1 1-3-3v-2H8.82A2.99 2.99 0 0 1 6 16a3 3 0 1 1 1.18-5.82V9H12V7.82A2.99 2.99 0 0 1 9 5a3 3 0 0 1 3-3Z"/></svg>',
        hosts:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4m0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4Z"/></svg>',
        mask:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6m4 18H6V4h7v5h5v11Z"/></svg>',
        wildcard:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M10.76 8.69 9.53 7.5 12 5.03 14.47 7.5l-1.23 1.19L12 7.42l-1.24 1.27m7.71 2.07L16.24 13l2.23 2.24-1.23 1.19L13.78 13l3.46-3.46 1.23 1.22m-13 0 1.23-1.22L10.22 13l-3.46 3.43-1.23-1.19L7.76 13l-2.29-2.24M12 16.58l1.24-1.27 1.23 1.19L12 18.97l-2.47-2.47 1.23-1.19L12 16.58Z"/></svg>',
        cidr:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M10.6 9.6 8.5 7.5 7 9l2.1 2.1L7 13.2 8.5 14.7l2.1-2.1 2.1 2.1 1.5-1.5-2.1-2.1L14.2 9 12.7 7.5 10.6 9.6M5 3h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2Z"/></svg>',
        total:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.41 11.58 12.41 2.58A2 2 0 0 0 11 2H4a2 2 0 0 0-2 2v7c0 .53.21 1.04.59 1.41l9 9a2 2 0 0 0 2.82 0l7-7a2 2 0 0 0 0-2.83M5.5 7A1.5 1.5 0 1 1 7 5.5 1.5 1.5 0 0 1 5.5 7Z"/></svg>',
        usable:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3m-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3m0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5C15 14.17 10.33 13 8 13m8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5Z"/></svg>',
        klass:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 7V3H2v18h20V7H12M6 19H4v-2h2v2m0-4H4v-2h2v2m0-4H4V9h2v2m0-4H4V5h2v2m4 12H8v-2h2v2m0-4H8v-2h2v2m0-4H8V9h2v2m0-4H8V5h2v2m10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10Z"/></svg>',
        scope:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 1 3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4m0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8Z"/></svg>',
        block:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13 9h-2V7h2m0 10h-2v-6h2m-1-9A10 10 0 0 0 2 12a10 10 0 0 0 10 10 10 10 0 0 0 10-10A10 10 0 0 0 12 2Z"/></svg>',
        copy:
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16 1H4a2 2 0 0 0-2 2v14h2V3h12V1m3 4H8a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2m0 16H8V7h11v14Z"/></svg>',
      };

      function metricCard(opts) {
        return (
          '<div class="ra-tool__metric ra-tool__metric--' +
          opts.tone +
          (opts.tall ? " ra-tool__metric--tall" : "") +
          '">' +
          '<button type="button" class="ra-tool__metric-copy" data-ra-copy-val="' +
          escapeHtml(opts.copy) +
          '" aria-label="Copy ' +
          escapeHtml(opts.label) +
          '">' +
          ICO.copy +
          "</button>" +
          '<div class="ra-tool__metric-main">' +
          '<span class="ra-tool__metric-icon" aria-hidden="true">' +
          opts.icon +
          "</span>" +
          '<div class="ra-tool__metric-body">' +
          '<p class="ra-tool__metric-label">' +
          escapeHtml(opts.label) +
          "</p>" +
          '<p class="ra-tool__metric-value">' +
          opts.valueHtml +
          "</p>" +
          (opts.sub
            ? '<p class="ra-tool__metric-sub">' + escapeHtml(opts.sub) + "</p>"
            : "") +
          "</div></div></div>"
        );
      }

      var summary =
        '<div class="ra-tool__metric-grid">' +
        metricCard({
          tone: "network",
          label: "Network Address",
          icon: ICO.network,
          valueHtml: escapeHtml(ipToString(r.network)),
          copy: ipToString(r.network),
        }) +
        metricCard({
          tone: "broadcast",
          label: "Broadcast Address",
          icon: ICO.broadcast,
          valueHtml: escapeHtml(ipToString(r.broadcast)),
          copy: ipToString(r.broadcast),
        }) +
        metricCard({
          tone: "hosts",
          label: "Usable Host Range",
          icon: ICO.hosts,
          valueHtml: rangeHtml,
          copy: rangePlain,
          tall: true,
        }) +
        metricCard({
          tone: "mask",
          label: "Subnet Mask",
          icon: ICO.mask,
          valueHtml: escapeHtml(ipToString(r.mask)),
          copy: ipToString(r.mask),
        }) +
        metricCard({
          tone: "wildcard",
          label: "Wildcard Mask",
          icon: ICO.wildcard,
          valueHtml: escapeHtml(ipToString(r.wildcard)),
          copy: ipToString(r.wildcard),
        }) +
        metricCard({
          tone: "total",
          label: "Total Addresses",
          icon: ICO.total,
          valueHtml: escapeHtml(r.total.toLocaleString("en-GB")),
          copy: String(r.total),
        }) +
        metricCard({
          tone: "usable",
          label: "Usable Hosts",
          icon: ICO.usable,
          valueHtml: escapeHtml(r.usableHosts.toLocaleString("en-GB")),
          copy: String(r.usableHosts),
        }) +
        metricCard({
          tone: "cidr",
          label: "CIDR",
          icon: ICO.cidr,
          valueHtml: escapeHtml("/" + r.cidr),
          copy: "/" + r.cidr,
        }) +
        metricCard({
          tone: "scope",
          label: "Private / Public",
          icon: ICO.scope,
          valueHtml: escapeHtml(r.scope),
          copy: r.scope,
          sub: scopeSub,
        }) +
        metricCard({
          tone: "block",
          label: "Block Size (Increment)",
          icon: ICO.block,
          valueHtml: escapeHtml(String(r.blockSize)),
          copy: String(r.blockSize),
        }) +
        metricCard({
          tone: "klass",
          label: "Address Class",
          icon: ICO.klass,
          valueHtml: escapeHtml(r.addressClass),
          copy: r.addressClass,
        }) +
        "</div>";

      var binary =
        '<div class="ra-tool__tile ra-tool__binary-panel">' +
        '<h3 class="ra-tool__binary-title">Binary Representation</h3>' +
        '<p class="ra-tool__bin-legend">' +
        '<span class="ra-tool__legend-item">' +
        '<span class="ra-tool__legend-swatch ra-tool__legend-swatch--net" aria-hidden="true"></span>' +
        "Network bits</span>" +
        '<span class="ra-tool__legend-item">' +
        '<span class="ra-tool__legend-swatch ra-tool__legend-swatch--host" aria-hidden="true"></span>' +
        "Host bits</span>" +
        "</p>" +
        '<div class="ra-tool__binary">' +
        binaryRow("IP Address", r.ip, r.cidr) +
        binaryRow("Subnet Mask", r.mask, r.cidr) +
        binaryRow("Network Address", r.network, r.cidr) +
        "</div></div>";

      var steps = explainSubnet(r);

      var tabs = [
        { id: "summary", label: "Summary" },
        { id: "binary", label: "Binary" },
        { id: "viz", label: "Visualisation" },
        { id: "explain", label: "Explanation" },
      ];
      var tabBar =
        '<div class="ra-tool__tabs-row">' +
        '<div class="ra-tool__tabs" role="tablist" aria-label="Result views">' +
        tabs
          .map(function (t) {
            var on = t.id === activeTab;
            return (
              '<button type="button" class="ra-tool__tab' +
              (on ? " ra-tool__tab--active" : "") +
              '" role="tab" aria-selected="' +
              (on ? "true" : "false") +
              '" data-ra-tab="' +
              t.id +
              '">' +
              t.label +
              "</button>"
            );
          })
          .join("") +
        "</div>" +
        '<button type="button" class="ra-tool__copy ra-tool__copy--all" data-ra-copy-summary>Copy all</button>' +
        "</div>";

      function stripCell(icon, label, value) {
        return (
          '<div class="ra-tool__strip-cell">' +
          '<span class="ra-tool__strip-icon" aria-hidden="true">' +
          icon +
          "</span>" +
          '<div class="ra-tool__strip-text">' +
          '<span class="ra-tool__strip-label">' +
          escapeHtml(label) +
          "</span>" +
          '<span class="ra-tool__strip-value">' +
          escapeHtml(value) +
          "</span></div></div>"
        );
      }

      var icoNet =
        '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M21 16V4H3v12h9v2H8v2h8v-2h-4v-2h9M5 14V6h14v8H5Z"/></svg>';
      var icoHosts =
        '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3m-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3m0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5C15 14.17 10.33 13 8 13m8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5Z"/></svg>';
      var icoClass =
        '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M21.41 11.58 12.41 2.58A2 2 0 0 0 11 2H4a2 2 0 0 0-2 2v7a2 2 0 0 0 .59 1.42l9 9a2 2 0 0 0 2.82 0l7-7a2 2 0 0 0 0-2.84M5.5 7A1.5 1.5 0 1 1 7 5.5 1.5 1.5 0 0 1 5.5 7Z"/></svg>';
      var icoLock =
        '<svg viewBox="0 0 24 24"><path fill="currentColor" d="M12 17a2 2 0 1 0 0-4 2 2 0 0 0 0 4m6-9h-1V6a5 5 0 0 0-10 0v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2m-3 0H9V6a3 3 0 0 1 6 0v2Z"/></svg>';

      stripEl.innerHTML =
        stripCell(icoNet, "Network Summary", cidrStr) +
        stripCell(
          icoHosts,
          "Usable Hosts",
          r.usableHosts.toLocaleString("en-GB")
        ) +
        stripCell(icoClass, "Address Class", r.addressClass) +
        stripCell(icoLock, "Private / Public", r.scope);
      stripEl.hidden = false;

      resultsEl.innerHTML =
        tabBar +
        '<div class="ra-tool__panels">' +
        '<div data-ra-panel="summary"' +
        (activeTab === "summary" ? "" : " hidden") +
        ">" +
        summary +
        "</div>" +
        '<div data-ra-panel="binary"' +
        (activeTab === "binary" ? "" : " hidden") +
        ">" +
        binary +
        "</div>" +
        '<div data-ra-panel="viz"' +
        (activeTab === "viz" ? "" : " hidden") +
        ">" +
        renderViz(r) +
        "</div>" +
        '<div data-ra-panel="explain"' +
        (activeTab === "explain" ? "" : " hidden") +
        ">" +
        steps +
        "</div>" +
        "</div>";

      lastText = [
        "Network address: " + ipToString(r.network),
        "Broadcast address: " + ipToString(r.broadcast),
        "Usable host range: " + rangePlain,
        "Subnet mask: " + ipToString(r.mask),
        "Wildcard mask: " + ipToString(r.wildcard),
        "CIDR: /" + r.cidr,
        "Total addresses: " + r.total.toLocaleString("en-GB"),
        "Usable hosts: " + r.usableHosts.toLocaleString("en-GB"),
        "Network: " + cidrStr,
        "IP: " + ipToString(r.ip),
        "Class: " + r.addressClass,
        "Scope: " + r.scope,
        ctx ? "Context: " + ctx.label : "",
      ]
        .filter(Boolean)
        .join("\n");

      resultsEl.hidden = false;
      bindResultsUi();
    }

    function run() {
      var ipStr = (ipInput.value || "").trim();
      var cidr = Number(cidrSelect.value);
      var ipNum = parseIPv4(ipStr);
      if (ipNum === null) {
        showError("Enter a valid IPv4 address (for example 192.168.1.10).");
        ipInput.focus();
        return;
      }
      if (!Number.isInteger(cidr) || cidr < 0 || cidr > 32) {
        showError("CIDR must be between /0 and /32.");
        return;
      }
      showError("");
      var r = calculateSubnet(ipNum, cidr);
      render(r);
      writeQuery(ipStr, cidr);
    }

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      revealSummaryView();
    });

    mount.querySelector("[data-ra-reset]").addEventListener("click", function () {
      ipInput.value = "192.168.1.0";
      cidrSelect.value = "16";
      syncCidrToMask();
      showError("");
      try {
        var url = new URL(window.location.href);
        url.search = "";
        if (history.replaceState) {
          history.replaceState(null, "", url.pathname + url.hash);
        }
      } catch (e) {
        /* ignore */
      }
      revealSummaryView();
    });

    mount.querySelector("[data-ra-random]").addEventListener("click", function () {
      var ex = EXAMPLES[Math.floor(Math.random() * EXAMPLES.length)];
      applyExample(ex);
    });

    var moreSelect = mount.querySelector("[data-ra-more]");
    if (moreSelect) {
      moreSelect.addEventListener("change", function () {
        var ex = findExample(moreSelect.value);
        if (ex) applyExample(ex);
        moreSelect.value = "";
      });
    }

    mount.querySelectorAll("[data-ra-example]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyExample(findExample(btn.getAttribute("data-ra-example")));
      });
    });

    /* Cheat sheet rows + private network presets in page body */
    var article = articleRoot();
    if (article) {
      article.querySelectorAll(".ra-tool-cheatsheet").forEach(function (table) {
        table.querySelectorAll("tbody tr").forEach(function (tr) {
          tr.tabIndex = 0;
          tr.setAttribute("role", "button");
          function applyRow() {
            var cell = tr.querySelector("td");
            if (!cell) return;
            var m = (cell.textContent || "").match(/\/(\d{1,2})/);
            if (!m) return;
            cidrSelect.value = String(Number(m[1]));
            syncCidrToMask();
            revealSummaryView();
          }
          tr.addEventListener("click", applyRow);
          tr.addEventListener("keydown", function (ev) {
            if (ev.key === "Enter" || ev.key === " ") {
              ev.preventDefault();
              applyRow();
            }
          });
        });
      });

      var sheet = article.querySelector("#ra-cidr-sheet");
      var fullToggle = article.querySelector("[data-ra-full-table]");
      if (sheet && fullToggle) {
        var extraRows = sheet.querySelectorAll(".ra-tool-cheatsheet__extra");
        fullToggle.addEventListener("click", function () {
          var open = fullToggle.getAttribute("aria-expanded") === "true";
          var next = !open;
          fullToggle.setAttribute("aria-expanded", next ? "true" : "false");
          fullToggle.textContent = next
            ? "Show less ↑"
            : "View full table →";
          extraRows.forEach(function (row) {
            if (next) row.removeAttribute("hidden");
            else row.setAttribute("hidden", "");
          });
        });
      }

      function applyPreset(el) {
        var preset = el.getAttribute("data-ra-preset") || "";
        var parts = preset.split("/");
        if (parts[0]) ipInput.value = parts[0];
        if (parts[1]) {
          cidrSelect.value = String(parts[1]);
          syncCidrToMask();
        }
        revealSummaryView();
      }

      article.querySelectorAll("[data-ra-preset]").forEach(function (el) {
        el.addEventListener("click", function (ev) {
          ev.preventDefault();
          applyPreset(el);
        });
        el.addEventListener("keydown", function (ev) {
          if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            applyPreset(el);
          }
        });
      });
    }

    readQuery();
    syncCidrToMask();
    run();
    pinComposer(mount.querySelector(".ra-tool__composer"));
  }

  function boot() {
    var slug = toolSlug();
    if (slug === "subnet-calculator") initSubnetCalculator();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(boot);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
