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
    var stopRect = stop.getBoundingClientRect();
    var card = stop.querySelector(".rebash-roadmap__card") || stop;
    var cardRect = card.getBoundingClientRect();
    points.push({
      x: ((cardRect.left + cardRect.width / 2 - rect.left) / rect.width) * 100,
      y: ((stopRect.top + stopRect.height / 2 - rect.top) / rect.height) * 100
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
      if (/\/(career-paths|learning-paths|technologies|labs|quizzes|projects|capstones|cheatsheets|interview|certifications|blog|about)\/?$/.test(path)) {
        link.setAttribute("data-md-no-instant", "");
      }
    } catch (e) {
      /* ignore invalid hrefs */
    }
  });
}

function onPageReady() {
  initLearningPathPicker();
  markCustomTemplateLinks();
  initRecommendedRoadmap();
}

if (typeof document$ !== "undefined") {
  document$.subscribe(onPageReady);
} else {
  document.addEventListener("DOMContentLoaded", onPageReady);
}
