/* REBASH Academy – Custom JavaScript */

document.addEventListener("DOMContentLoaded", function () {
  initLearningPathPicker();
});

function initLearningPathPicker() {
  const picker = document.querySelector(".rebash-path-picker");
  const stepsContainer = document.getElementById("rebash-path-steps");
  if (!picker || !stepsContainer) return;

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
    selectPath(hash, false);
  }
}
