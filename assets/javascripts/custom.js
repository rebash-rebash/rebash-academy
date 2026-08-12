/* REBASH Academy – Custom JavaScript */

function buildRoadmapPath(points) {
  if (points.length < 2) return "";
  var d = "M " + points[0].x + " " + points[0].y;
  for (var i = 1; i < points.length; i++) {
    var prev = points[i - 1];
    var curr = points[i];
    var midY = (prev.y + curr.y) / 2;
    d +=
      " C " +
      prev.x +
      " " +
      midY +
      ", " +
      curr.x +
      " " +
      midY +
      ", " +
      curr.x +
      " " +
      curr.y;
  }
  return d;
}

function redrawRoadmapCanvas(canvas) {
  if (!canvas) return;
  var svg = canvas.querySelector(".rebash-roadmap__path");
  var stroke = canvas.querySelector(".rebash-roadmap__stroke");
  var dash = canvas.querySelector(".rebash-roadmap__dash");
  var stops = canvas.querySelectorAll(".rebash-roadmap__stops > li");
  if (!stroke || !dash || !stops.length) return;

  var rect = canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;

  if (svg) {
    svg.setAttribute("width", String(Math.round(rect.width)));
    svg.setAttribute("height", String(Math.round(rect.height)));
  }

  var points = [];
  stops.forEach(function (stop) {
    var card = stop.querySelector(".rebash-roadmap__card") || stop;
    var cardRect = card.getBoundingClientRect();
    points.push({
      x: ((cardRect.left + cardRect.width / 2 - rect.left) / rect.width) * 100,
      y: ((cardRect.top + cardRect.height / 2 - rect.top) / rect.height) * 100
    });
  });

  var d = buildRoadmapPath(points);
  stroke.setAttribute("d", d);
  dash.setAttribute("d", d);
}

function redrawVisibleRoadmaps() {
  document.querySelectorAll(".rebash-roadmap__canvas").forEach(function (canvas) {
    if (canvas.offsetParent === null) return;
    redrawRoadmapCanvas(canvas);
  });
}

function bindRoadmapCanvas(canvas) {
  if (!canvas || canvas.dataset.rebashRoadmapBound) return;
  canvas.dataset.rebashRoadmapBound = "1";

  function scheduleRedraw() {
    window.requestAnimationFrame(function () {
      redrawRoadmapCanvas(canvas);
    });
  }

  scheduleRedraw();
  window.addEventListener("resize", scheduleRedraw);

  if (typeof ResizeObserver !== "undefined") {
    new ResizeObserver(scheduleRedraw).observe(canvas);
    var stops = canvas.querySelector(".rebash-roadmap__stops");
    if (stops) {
      new ResizeObserver(scheduleRedraw).observe(stops);
    }
  }

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(scheduleRedraw);
  }
}

function initRecommendedRoadmap() {
  document.querySelectorAll(".rebash-roadmap__canvas").forEach(bindRoadmapCanvas);
  redrawVisibleRoadmaps();
}

function initLearningPathPicker() {
  const picker = document.querySelector(".rebash-path-picker");
  const stepsContainer = document.getElementById("rebash-path-steps");
  if (!picker || !stepsContainer) return;
  if (picker.dataset.rebashPickerBound) return;
  picker.dataset.rebashPickerBound = "1";

  const tiles = picker.querySelectorAll(".rebash-path-tile");
  const panels = stepsContainer.querySelectorAll(".rebash-path-steps__panel");
  let activeId = null;

  function selectPath(pathId, scrollIntoView) {
    if (activeId === pathId) {
      closePath();
      return;
    }

    activeId = pathId;

    tiles.forEach(function (tile) {
      const isActive = tile.dataset.pathId === pathId;
      tile.classList.toggle("is-active", isActive);
      tile.setAttribute("aria-selected", isActive ? "true" : "false");
    });

    panels.forEach(function (panel) {
      const isActive = panel.id === "panel-" + pathId;
      panel.hidden = !isActive;
    });

    stepsContainer.hidden = false;
    initRecommendedRoadmap();
    window.requestAnimationFrame(function () {
      window.requestAnimationFrame(redrawVisibleRoadmaps);
    });

    if (scrollIntoView) {
      stepsContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    if (pathId && history.replaceState) {
      history.replaceState(null, "", "#" + pathId);
    }
  }

  function closePath() {
    activeId = null;
    tiles.forEach(function (tile) {
      tile.classList.remove("is-active");
      tile.setAttribute("aria-selected", "false");
    });
    panels.forEach(function (panel) {
      panel.hidden = true;
    });
    stepsContainer.hidden = true;

    if (history.replaceState) {
      history.replaceState(null, "", window.location.pathname);
    }
  }

  tiles.forEach(function (tile) {
    tile.addEventListener("click", function () {
      selectPath(tile.dataset.pathId, true);
    });
  });

  const hash = window.location.hash.replace("#", "");
  if (hash && picker.querySelector('[data-path-id="' + hash + '"]')) {
    selectPath(hash, true);
  }
}

function markCustomTemplateLinks() {
  document.querySelectorAll("a[href]").forEach(function (link) {
    try {
      var path = link.pathname || "";
      if (/\/(career-paths|learning-paths|technologies|labs|quizzes|tools|projects|capstones|cheatsheets|interview|certifications|blog|about|books)\/?$/.test(path)) {
        link.setAttribute("data-md-no-instant", "");
      }
    } catch (e) {
      /* ignore invalid hrefs */
    }
  });
}

/** Mark lab fences: title="Terminal" → terminal chrome; other titles → file chrome */
function markLabCodeBlocks() {
  document.querySelectorAll(".highlight > .filename, .highlighttable .filename").forEach(function (el) {
    var label = (el.textContent || "").trim().toLowerCase();
    var block =
      el.closest(".highlighttable") ||
      el.closest(".highlight") ||
      el.parentElement;
    if (!block) return;
    block.classList.remove("ra-terminal", "ra-file-code");
    if (label === "terminal" || label === "shell" || label === "console") {
      block.classList.add("ra-terminal");
      el.setAttribute("data-ra-chrome", "terminal");
    } else if (label) {
      block.classList.add("ra-file-code");
      el.setAttribute("data-ra-chrome", "file");
    }
  });
}

function normalizeHeaderPath(pathname) {
  if (!pathname) return "/";
  var path = pathname.replace(/\/+$/, "");
  return path || "/";
}

function closeHeaderDropdowns() {
  document.querySelectorAll(".rebash-header-dd").forEach(function (dd) {
    dd.classList.remove("rebash-header-dd--open");
    dd.classList.add("rebash-header-dd--closed");
  });
  var active = document.activeElement;
  if (
    active &&
    active.closest &&
    active.closest(".rebash-header-dd") &&
    typeof active.blur === "function"
  ) {
    active.blur();
  }
}

/** Highlight the dropdown item that best matches the current URL */
function markHeaderDropdownActive() {
  var path = normalizeHeaderPath(window.location.pathname);
  var items = document.querySelectorAll(".rebash-header-dd__item");
  var best = null;
  var bestLen = -1;

  items.forEach(function (item) {
    item.classList.remove("rebash-header-dd__item--active");
    var href = item.getAttribute("href");
    if (!href || href.charAt(0) === "#") return;
    try {
      var itemPath = normalizeHeaderPath(new URL(href, window.location.href).pathname);
      if (itemPath === path || (itemPath !== "/" && path.indexOf(itemPath + "/") === 0)) {
        if (itemPath.length > bestLen) {
          best = item;
          bestLen = itemPath.length;
        }
      }
    } catch (e) {
      /* ignore bad hrefs */
    }
  });

  if (best) best.classList.add("rebash-header-dd__item--active");
}

/** Header dropdowns: one open at a time; close after picking a link (instant nav) */
function initHeaderDropdowns() {
  var menus = document.querySelectorAll(".rebash-header-dd");
  if (!menus.length) return;

  if (!document.documentElement.dataset.rebashDdEscBound) {
    document.documentElement.dataset.rebashDdEscBound = "1";
    document.addEventListener("keydown", function (event) {
      if (event.key !== "Escape") return;
      closeHeaderDropdowns();
    });
  }

  menus.forEach(function (dd) {
    if (dd.dataset.rebashDdBound) return;
    dd.dataset.rebashDdBound = "1";
    var leaveTimer = null;

    function armOpen() {
      if (leaveTimer) {
        window.clearTimeout(leaveTimer);
        leaveTimer = null;
      }
      dd.classList.remove("rebash-header-dd--closed");
      menus.forEach(function (other) {
        if (other === dd) return;
        other.classList.add("rebash-header-dd--closed");
        var active = document.activeElement;
        if (active && other.contains(active) && typeof active.blur === "function") {
          active.blur();
        }
      });
    }

    function scheduleClose() {
      if (leaveTimer) window.clearTimeout(leaveTimer);
      /* Delay so the pointer can cross trigger → panel without killing the menu */
      leaveTimer = window.setTimeout(function () {
        leaveTimer = null;
        if (dd.matches(":hover") || dd.contains(document.activeElement)) return;
        dd.classList.add("rebash-header-dd--closed");
        var active = document.activeElement;
        if (active && dd.contains(active) && typeof active.blur === "function") {
          active.blur();
        }
      }, 180);
    }

    dd.addEventListener("pointerenter", armOpen);
    dd.addEventListener("focusin", armOpen);
    dd.addEventListener("pointerleave", scheduleClose);

    dd.addEventListener("click", function (event) {
      var link = event.target.closest("a");
      if (!link) return;
      /* Close after choose — Material instant nav keeps focus on the item */
      window.setTimeout(closeHeaderDropdowns, 0);
    });

    dd.addEventListener("focusout", function () {
      window.setTimeout(function () {
        if (!dd.contains(document.activeElement) && !dd.matches(":hover")) {
          dd.classList.add("rebash-header-dd--closed");
        }
      }, 0);
    });
  });
}

/** Home + #ra-nav-technologies: scroll left hub nav to Technologies */
function scrollHubNavToTechnologies() {
  if (window.location.hash !== "#ra-nav-technologies") return;
  var target = document.getElementById("ra-nav-technologies");
  if (!target) return;
  var wrap = target.closest(".md-sidebar__scrollwrap");
  if (wrap) {
    var wrapRect = wrap.getBoundingClientRect();
    var elRect = target.getBoundingClientRect();
    wrap.scrollTop += elRect.top - wrapRect.top - 8;
  } else {
    target.scrollIntoView({ block: "start", inline: "nearest" });
  }
}

/** Keep the active course tutorial visible in the left sidebar */
function scrollActiveCourseNav() {
  var active =
    document.querySelector(".ra-sidebar--course .ra-sidebar__sublink--active") ||
    document.querySelector(".ra-sidebar--course .ra-sidebar__course-title--active");
  if (!active) return;

  var wrap = active.closest(".md-sidebar__scrollwrap");
  if (!wrap) {
    active.scrollIntoView({ block: "center", inline: "nearest" });
    return;
  }

  var wrapRect = wrap.getBoundingClientRect();
  var elRect = active.getBoundingClientRect();
  var delta =
    elRect.top - wrapRect.top - wrapRect.height / 2 + elRect.height / 2;
  /* Only move when the active item is outside the comfortable middle band */
  var edge = Math.min(96, wrapRect.height * 0.2);
  var fullyVisible =
    elRect.top >= wrapRect.top + edge &&
    elRect.bottom <= wrapRect.bottom - edge;
  if (!fullyVisible) {
    wrap.scrollTop += delta;
  }
}

/**
 * Bottom edge of sticky page chrome in the viewport (header + breadcrumbs +
 * quiz bar). Summing heights under-counts when Material rewrites header size.
 */
function stickyChromeBottom() {
  var bottom = 0;
  var nodes = [
    document.querySelector(".md-header"),
    document.querySelector(".md-tabs"),
    document.querySelector(".md-path.ra-path"),
    document.querySelector(".ra-quiz-toolbar"),
  ];
  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    if (!el || el.hasAttribute("hidden")) continue;
    var r = el.getBoundingClientRect();
    /* Ignore off-screen / collapsed chrome */
    if (r.height < 1 || r.bottom <= 0) continue;
    if (r.top > 220) continue;
    bottom = Math.max(bottom, r.bottom);
  }
  return Math.ceil(bottom);
}

/** Keep sticky breadcrumbs / quiz bar under the real header height. */
function syncStickyOffsets() {
  var root = document.documentElement;
  var header = document.querySelector(".md-header");
  var path = document.querySelector(".md-path.ra-path");
  var headerH = 0;
  var pathH = 0;
  var toolbarH = 0;
  if (header) {
    headerH = Math.ceil(header.getBoundingClientRect().height);
    if (headerH > 0) {
      root.style.setProperty("--ra-header-offset", headerH + "px");
      root.style.setProperty("--md-header-height", headerH + "px");
    }
  }
  if (path && !path.hasAttribute("hidden")) {
    pathH = Math.ceil(path.getBoundingClientRect().height);
    if (pathH > 0) root.style.setProperty("--ra-path-height", pathH + "px");
  } else {
    root.style.setProperty("--ra-path-height", "0px");
    pathH = 0;
  }
  var toolbar = document.querySelector(".ra-quiz-toolbar");
  if (toolbar) {
    toolbarH = Math.ceil(toolbar.getBoundingClientRect().height);
    root.style.setProperty(
      "--ra-quiz-toolbar-height",
      toolbarH > 0 ? toolbarH + "px" : "0px"
    );
  } else {
    root.style.setProperty("--ra-quiz-toolbar-height", "0px");
  }
  /* Prefer live chrome bottom so headings never sit under the top nav */
  var gap = 20;
  var fromChrome = stickyChromeBottom() + gap;
  var fromParts = Math.max(headerH, 48) + pathH + toolbarH + gap;
  var clear = Math.max(fromChrome, fromParts);
  root.style.setProperty("--ra-sticky-scroll-clearance", clear + "px");
}

function initStickyOffsets() {
  syncStickyOffsets();
  if (!initStickyOffsets._resizeBound) {
    initStickyOffsets._resizeBound = true;
    window.addEventListener("resize", syncStickyOffsets);
  }
  if (typeof ResizeObserver === "undefined") return;

  if (!initStickyOffsets._ro) {
    initStickyOffsets._ro = new ResizeObserver(syncStickyOffsets);
  }
  var ro = initStickyOffsets._ro;
  var header = document.querySelector(".md-header");
  var path = document.querySelector(".md-path.ra-path");
  var toolbar = document.querySelector(".ra-quiz-toolbar");
  /* Re-observe after Instant Navigation replaces content nodes */
  ro.disconnect();
  if (header) ro.observe(header);
  if (path) ro.observe(path);
  if (toolbar) ro.observe(toolbar);
}

function stickyScrollClearance() {
  syncStickyOffsets();
  var cs = getComputedStyle(document.documentElement);
  var clear = parseFloat(cs.getPropertyValue("--ra-sticky-scroll-clearance"));
  if (clear > 0) return clear;
  var header = parseFloat(cs.getPropertyValue("--ra-header-offset")) || 60;
  var path = parseFloat(cs.getPropertyValue("--ra-path-height")) || 30;
  var toolbar = parseFloat(cs.getPropertyValue("--ra-quiz-toolbar-height")) || 0;
  return header + path + toolbar + 24;
}

/** Scroll a heading into view below sticky header + breadcrumbs (+ quiz bar). */
function scrollToAnchorEl(el, behavior) {
  if (!el) return;
  var clear = stickyScrollClearance();
  var y = el.getBoundingClientRect().top + window.scrollY - clear;
  window.scrollTo({
    top: Math.max(0, y),
    behavior: behavior === "smooth" ? "smooth" : "auto",
  });
  /* Second pass after layout / Instant Navigation settles */
  window.requestAnimationFrame(function () {
    var clear2 = stickyScrollClearance();
    var top = el.getBoundingClientRect().top;
    if (Math.abs(top - clear2) > 2) {
      var y2 = top + window.scrollY - clear2;
      window.scrollTo({ top: Math.max(0, y2), behavior: "auto" });
    }
  });
}

function scrollToLocationHash(behavior) {
  var id = decodeURIComponent((window.location.hash || "").replace(/^#/, ""));
  if (!id) return;
  var el = document.getElementById(id);
  if (!el) return;
  scrollToAnchorEl(el, behavior || "auto");
}

/** Hash id from a TOC link — Material may rewrite href to a full URL + #id. */
function tocAnchorId(a) {
  if (!a) return "";
  try {
    var url = new URL(a.getAttribute("href") || a.href || "", window.location.href);
    return decodeURIComponent((url.hash || "").replace(/^#/, ""));
  } catch (e) {
    var href = a.getAttribute("href") || "";
    var i = href.lastIndexOf("#");
    return i >= 0 ? decodeURIComponent(href.slice(i + 1)) : "";
  }
}

function collectTocItems(nav) {
  var items = [];
  if (!nav) return items;
  var links = nav.querySelectorAll("a.md-nav__link");
  for (var i = 0; i < links.length; i++) {
    var a = links[i];
    var id = tocAnchorId(a);
    if (!id) continue;
    var el = document.getElementById(id);
    if (el) items.push({ a: a, el: el, id: id });
  }
  return items;
}

function findTocLinkById(id) {
  if (!id) return null;
  var nav = document.querySelector(".ra-onthispage");
  if (!nav) return null;
  var links = nav.querySelectorAll("a.md-nav__link");
  for (var i = 0; i < links.length; i++) {
    if (tocAnchorId(links[i]) === id) return links[i];
  }
  return null;
}

function setActiveTocLink(link) {
  if (!link) return;
  var nav = document.querySelector(".ra-onthispage");
  if (!nav) return;
  /* Prefer the live node for this hash (TOC can be rewritten after click) */
  var id = tocAnchorId(link);
  var live = id ? findTocLinkById(id) : link;
  if (live) link = live;
  nav.querySelectorAll(".md-nav__link.ra-toc-active").forEach(function (el) {
    el.classList.remove("ra-toc-active");
  });
  link.classList.add("ra-toc-active");
  var list = document.querySelector(".ra-onthispage__list");
  if (list && typeof link.scrollIntoView === "function") {
    var lr = list.getBoundingClientRect();
    var ar = link.getBoundingClientRect();
    if (ar.top < lr.top + 8 || ar.bottom > lr.bottom - 8) {
      link.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
  }
}

/**
 * Sticky-aware "On this page" spy.
 * Uses .ra-toc-active only — Material's --active/--passed are ignored visually.
 */
function initOnThisPageSpy() {
  var nav = document.querySelector(".ra-onthispage");
  if (!nav) return;
  if (!collectTocItems(nav).length) return;

  function pickActive() {
    var items = collectTocItems(nav);
    if (!items.length) return null;
    var clearance = stickyScrollClearance();
    var active = items[0];
    for (var i = 0; i < items.length; i++) {
      if (items[i].el.getBoundingClientRect().top <= clearance + 4) {
        active = items[i];
      }
    }
    return active;
  }

  function update() {
    if (
      initOnThisPageSpy._lockedUntil &&
      Date.now() < initOnThisPageSpy._lockedUntil &&
      initOnThisPageSpy._lockedId
    ) {
      setActiveTocLink(
        findTocLinkById(initOnThisPageSpy._lockedId) ||
          initOnThisPageSpy._lockedLink
      );
      return;
    }

    var active = pickActive();
    if (!active) return;
    if (active.a.classList.contains("ra-toc-active")) return;
    setActiveTocLink(active.a);
  }

  function onScroll() {
    if (
      !initOnThisPageSpy._ignoreScrollUnlock &&
      initOnThisPageSpy._lockedLink &&
      typeof initOnThisPageSpy._lockScrollY === "number" &&
      Math.abs(window.scrollY - initOnThisPageSpy._lockScrollY) > 48
    ) {
      initOnThisPageSpy._lockedUntil = 0;
      initOnThisPageSpy._lockedLink = null;
    }
    if (initOnThisPageSpy._tick) return;
    initOnThisPageSpy._tick = true;
    window.requestAnimationFrame(function () {
      initOnThisPageSpy._tick = false;
      update();
    });
  }

  if (initOnThisPageSpy._onScroll) {
    window.removeEventListener("scroll", initOnThisPageSpy._onScroll);
    window.removeEventListener("resize", initOnThisPageSpy._onScroll);
  }
  initOnThisPageSpy._onScroll = onScroll;
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  update();
}

function lockOnThisPageSpy(ms, link) {
  initOnThisPageSpy._lockedUntil = Date.now() + (ms || 500);
  initOnThisPageSpy._lockedId = tocAnchorId(link);
  initOnThisPageSpy._lockedLink =
    findTocLinkById(initOnThisPageSpy._lockedId) || link || null;
  initOnThisPageSpy._lockScrollY = window.scrollY;
  if (initOnThisPageSpy._unlockTimer) {
    window.clearTimeout(initOnThisPageSpy._unlockTimer);
  }
  initOnThisPageSpy._unlockTimer = window.setTimeout(function () {
    initOnThisPageSpy._lockedLink = null;
    initOnThisPageSpy._lockedId = null;
    initOnThisPageSpy._lockedUntil = 0;
    if (typeof initOnThisPageSpy._onScroll === "function") {
      initOnThisPageSpy._onScroll();
    }
  }, ms || 500);
}

/**
 * TOC / in-page links: scroll with sticky clearance; TOC clicks own the highlight.
 */
function initStickyAnchorScroll() {
  if (initStickyAnchorScroll._bound) return;
  initStickyAnchorScroll._bound = true;

  document.addEventListener(
    "click",
    function (ev) {
      var a =
        ev.target && ev.target.closest ? ev.target.closest("a[href*='#']") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      var hash = "";
      try {
        var url = new URL(href, window.location.href);
        if (
          url.pathname.replace(/\/+$/, "") !==
          window.location.pathname.replace(/\/+$/, "")
        ) {
          return;
        }
        hash = decodeURIComponent(url.hash.replace(/^#/, ""));
      } catch (e) {
        return;
      }
      if (!hash) return;
      var el = document.getElementById(hash);
      if (!el) return;

      var fromToc = !!a.closest(".ra-onthispage");
      if (fromToc) {
        ev.preventDefault();
        ev.stopPropagation();
        if (history.replaceState) {
          history.replaceState(null, "", "#" + hash);
        } else {
          window.location.hash = hash;
        }
        lockOnThisPageSpy(600, a);
        setActiveTocLink(a);
        initOnThisPageSpy._ignoreScrollUnlock = true;
        scrollToAnchorEl(el, "auto");
        window.setTimeout(function () {
          scrollToAnchorEl(el, "auto");
          setActiveTocLink(a);
          initOnThisPageSpy._lockScrollY = window.scrollY;
          initOnThisPageSpy._ignoreScrollUnlock = false;
        }, 80);
        return;
      }

      window.setTimeout(function () {
        scrollToAnchorEl(el, "smooth");
      }, 0);
    },
    true
  );

  window.addEventListener("hashchange", function () {
    scrollToLocationHash("smooth");
    var id = decodeURIComponent((window.location.hash || "").replace(/^#/, ""));
    if (!id) return;
    var link = findTocLinkById(id);
    if (link) {
      lockOnThisPageSpy(600, link);
      setActiveTocLink(link);
    }
  });
}

function onPageReady() {
  closeHeaderDropdowns();
  markHeaderDropdownActive();
  initLearningPathPicker();
  markCustomTemplateLinks();
  initRecommendedRoadmap();
  markLabCodeBlocks();
  initHeaderDropdowns();
  initStickyOffsets();
  initStickyAnchorScroll();
  initOnThisPageSpy();
  window.requestAnimationFrame(function () {
    window.requestAnimationFrame(function () {
      syncStickyOffsets();
      scrollActiveCourseNav();
      scrollHubNavToTechnologies();
      initOnThisPageSpy();
      if (window.location.hash) scrollToLocationHash("auto");
    });
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(onPageReady);
} else {
  document.addEventListener("DOMContentLoaded", onPageReady);
}
