/**
 * REBASH Academy — interactive quizzes
 * Enhances existing Markdown quiz pages: select answers, track progress,
 * submit for scored results, persist completion, print summary.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "rebash.quiz.v1";
  var OPTION_RE = /^\s*([A-D])\.\s*(.*)$/i;
  var CORRECT_RE = /Correct answer:\s*([A-D])/i;

  function quizSlug() {
    var parts = (window.location.pathname || "").replace(/\/+$/, "").split("/");
    var i = parts.indexOf("quizzes");
    if (i < 0 || !parts[i + 1] || parts[i + 1] === "index.html") return null;
    return parts[i + 1];
  }

  function isQuizHub() {
    var path = (window.location.pathname || "").replace(/\/+$/, "");
    return /\/quizzes$/.test(path) || /\/quizzes\/index\.html$/.test(path);
  }

  function isQuizPage() {
    return !!quizSlug();
  }

  function loadStore() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}") || {};
    } catch (e) {
      return {};
    }
  }

  function saveStore(store) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(store));
    } catch (e) {
      /* private mode / quota */
    }
  }

  function parsePassPercent(root) {
    var text = root.textContent || "";
    var m = text.match(/Passing score\s*[|:]\s*.*?(\d+)\s*%/i);
    if (m) return parseInt(m[1], 10);
    m = text.match(/(\d+)\s*%\s*\(/);
    if (m) return parseInt(m[1], 10);
    return 70;
  }

  function optionLetter(li) {
    var strong = li.querySelector("strong");
    var raw = (strong ? strong.textContent : li.textContent) || "";
    var m = raw.match(OPTION_RE) || raw.match(/^\s*([A-D])\b/);
    return m ? m[1].toUpperCase() : null;
  }

  function optionLabel(li) {
    var clone = li.cloneNode(true);
    var strong = clone.querySelector("strong");
    if (strong) strong.remove();
    var t = (clone.textContent || "").replace(/^\s*[.:]\s*/, "").trim();
    if (t) return t;
    var raw = (li.textContent || "").trim();
    var m = raw.match(OPTION_RE);
    return m ? m[2].trim() : raw;
  }

  function findCorrect(details) {
    if (!details) return null;
    var m = (details.textContent || "").match(CORRECT_RE);
    return m ? m[1].toUpperCase() : null;
  }

  function collectQuestions(article) {
    var headings = Array.prototype.slice.call(
      article.querySelectorAll("h3")
    ).filter(function (h) {
      return /^Question\s+\d+/i.test((h.textContent || "").trim());
    });

    var questions = [];
    headings.forEach(function (h3, idx) {
      var nodes = [];
      var el = h3.nextElementSibling;
      while (el && el.tagName !== "H2" && el.tagName !== "H3") {
        nodes.push(el);
        el = el.nextElementSibling;
      }

      var optionsUl = null;
      var details = null;
      nodes.forEach(function (node) {
        if (!optionsUl && node.tagName === "UL") {
          var items = node.querySelectorAll(":scope > li");
          if (items.length >= 2 && optionLetter(items[0])) optionsUl = node;
        }
        if (
          !details &&
          (node.tagName === "DETAILS" ||
            (node.classList && node.classList.contains("admonition")))
        ) {
          if (CORRECT_RE.test(node.textContent || "")) details = node;
        }
        if (!details && node.querySelector) {
          var d = node.querySelector("details");
          if (d && CORRECT_RE.test(d.textContent || "")) details = d;
        }
      });

      var correct = findCorrect(details);
      if (!optionsUl || !correct) return;

      var options = [];
      Array.prototype.forEach.call(optionsUl.querySelectorAll(":scope > li"), function (li) {
        var letter = optionLetter(li);
        if (!letter) return;
        options.push({ letter: letter, label: optionLabel(li), li: li });
      });
      if (options.length < 2) return;

      var numMatch = (h3.textContent || "").match(/Question\s+(\d+)/i);
      questions.push({
        id: "q" + (numMatch ? numMatch[1] : idx + 1),
        index: questions.length,
        heading: h3,
        optionsUl: optionsUl,
        details: details,
        correct: correct,
        options: options,
        prompt: "",
      });
    });

    questions.forEach(function (q) {
      var parts = [];
      var n = q.heading.nextElementSibling;
      while (n && n !== q.optionsUl) {
        if (n.tagName === "P") {
          var t = (n.textContent || "").trim();
          if (
            t &&
            !/^Difficulty:/i.test(t) &&
            !/^Options:/i.test(t) &&
            !/^Related concepts/i.test(t)
          ) {
            parts.push(t);
          }
        }
        n = n.nextElementSibling;
      }
      q.prompt = parts.join(" ");
    });

    return questions;
  }

  function buildToolbar(total, answered) {
    var bar = document.createElement("div");
    bar.className = "ra-quiz-toolbar";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Quiz progress");
    bar.innerHTML =
      '<div class="ra-quiz-toolbar__inner">' +
      '<div class="ra-quiz-toolbar__meta">' +
      '<span class="ra-quiz-toolbar__title">Quiz progress</span>' +
      '<span class="ra-quiz-toolbar__count" data-ra-quiz-count></span>' +
      "</div>" +
      '<div class="ra-quiz-toolbar__track" aria-hidden="true">' +
      '<div class="ra-quiz-toolbar__fill" data-ra-quiz-fill></div>' +
      "</div>" +
      '<div class="ra-quiz-toolbar__actions">' +
      '<button type="button" class="ra-quiz-btn ra-quiz-btn--ghost" data-ra-quiz-reset>Reset</button>' +
      '<button type="button" class="ra-quiz-btn ra-quiz-btn--primary" data-ra-quiz-submit>Submit quiz</button>' +
      "</div>" +
      "</div>";
    return bar;
  }

  function updateProgress(toolbar, answered, total) {
    var count = toolbar.querySelector("[data-ra-quiz-count]");
    var fill = toolbar.querySelector("[data-ra-quiz-fill]");
    if (count) count.textContent = answered + " / " + total + " answered";
    if (fill) fill.style.width = total ? Math.round((answered / total) * 100) + "%" : "0%";
  }

  function enhanceQuestion(q, groupName, savedAnswer) {
    var fieldset = document.createElement("fieldset");
    fieldset.className = "ra-quiz-options";
    fieldset.dataset.raQuizId = q.id;
    fieldset.dataset.raCorrect = q.correct;

    var legend = document.createElement("legend");
    legend.className = "ra-quiz-options__legend";
    legend.textContent = "Choose one answer";
    fieldset.appendChild(legend);

    q.options.forEach(function (opt) {
      var label = document.createElement("label");
      label.className = "ra-quiz-option";
      var input = document.createElement("input");
      input.type = "radio";
      input.name = groupName + "-" + q.id;
      input.value = opt.letter;
      input.className = "ra-quiz-option__input";
      if (savedAnswer && savedAnswer === opt.letter) input.checked = true;
      var mark = document.createElement("span");
      mark.className = "ra-quiz-option__mark";
      mark.textContent = opt.letter;
      var text = document.createElement("span");
      text.className = "ra-quiz-option__text";
      text.textContent = opt.label;
      label.appendChild(input);
      label.appendChild(mark);
      label.appendChild(text);
      fieldset.appendChild(label);
    });

    q.optionsUl.replaceWith(fieldset);
    q.fieldset = fieldset;

    if (q.details) {
      q.details.classList.add("ra-quiz-reveal");
      q.details.hidden = true;
    }

    var status = document.createElement("div");
    status.className = "ra-quiz-qstatus";
    status.hidden = true;
    fieldset.insertAdjacentElement("afterend", status);
    q.statusEl = status;
  }

  function gatherAnswers(questions) {
    var answers = {};
    questions.forEach(function (q) {
      var checked = q.fieldset.querySelector("input:checked");
      if (checked) answers[q.id] = checked.value;
    });
    return answers;
  }

  function answeredCount(answers) {
    return Object.keys(answers).length;
  }

  function grade(questions, answers) {
    var correct = 0;
    var rows = questions.map(function (q) {
      var picked = answers[q.id] || "";
      var ok = picked === q.correct;
      if (ok) correct += 1;
      return {
        id: q.id,
        prompt: q.prompt || q.heading.textContent,
        picked: picked,
        correct: q.correct,
        ok: ok,
      };
    });
    return { correct: correct, total: questions.length, rows: rows };
  }

  function renderResults(container, result, passPercent, title) {
    var pct = result.total ? Math.round((result.correct / result.total) * 100) : 0;
    var passed = pct >= passPercent;
    container.hidden = false;
    container.innerHTML =
      '<div class="ra-quiz-results__card' +
      (passed ? " ra-quiz-results__card--pass" : " ra-quiz-results__card--fail") +
      '">' +
      "<h2>Your results</h2>" +
      '<p class="ra-quiz-results__score">' +
      result.correct +
      " / " +
      result.total +
      " correct (" +
      pct +
      "%)</p>" +
      '<p class="ra-quiz-results__verdict">' +
      (passed
        ? "Pass — you met the " + passPercent + "% mark."
        : "Not yet — pass mark is " + passPercent + "%. Review the misses below.") +
      "</p>" +
      '<div class="ra-quiz-results__actions">' +
      '<button type="button" class="ra-quiz-btn ra-quiz-btn--primary" data-ra-quiz-print>Print results</button>' +
      '<button type="button" class="ra-quiz-btn ra-quiz-btn--ghost" data-ra-quiz-retry>Try again</button>' +
      "</div>" +
      '<div class="ra-quiz-results__printhead" hidden>' +
      "<h1>" +
      (title || "Quiz results") +
      "</h1>" +
      "<p>REBASH Academy · " +
      new Date().toLocaleString("en-GB") +
      "</p>" +
      "</div>" +
      '<ol class="ra-quiz-results__list"></ol>' +
      "</div>";

    var list = container.querySelector(".ra-quiz-results__list");
    result.rows.forEach(function (row, i) {
      var li = document.createElement("li");
      li.className =
        "ra-quiz-results__item " +
        (row.ok ? "ra-quiz-results__item--ok" : "ra-quiz-results__item--bad");
      li.innerHTML =
        "<strong>Q" +
        (i + 1) +
        "</strong> " +
        '<span class="ra-quiz-results__prompt"></span>' +
        '<div class="ra-quiz-results__meta">' +
        (row.ok
          ? "Correct (" + row.correct + ")"
          : "Your answer: " +
            (row.picked || "—") +
            " · Correct: " +
            row.correct) +
        "</div>";
      li.querySelector(".ra-quiz-results__prompt").textContent = row.prompt;
      list.appendChild(li);
    });
  }

  function applyGradeUI(questions, answers, graded) {
    questions.forEach(function (q) {
      var picked = answers[q.id];
      q.fieldset.querySelectorAll(".ra-quiz-option").forEach(function (label) {
        var input = label.querySelector("input");
        label.classList.remove(
          "ra-quiz-option--correct",
          "ra-quiz-option--wrong",
          "ra-quiz-option--missed"
        );
        if (!input) return;
        if (input.value === q.correct) label.classList.add("ra-quiz-option--correct");
        if (picked && input.value === picked && picked !== q.correct) {
          label.classList.add("ra-quiz-option--wrong");
        }
        if (!picked && input.value === q.correct) {
          label.classList.add("ra-quiz-option--missed");
        }
        input.disabled = true;
      });
      if (q.details) {
        q.details.hidden = false;
        try {
          q.details.open = !graded || answers[q.id] !== q.correct;
        } catch (e) {
          /* ignore */
        }
      }
      if (q.statusEl) {
        q.statusEl.hidden = false;
        var ok = answers[q.id] === q.correct;
        q.statusEl.textContent = ok
          ? "Correct"
          : answers[q.id]
            ? "Incorrect — correct answer is " + q.correct
            : "Unanswered — correct answer is " + q.correct;
        q.statusEl.className =
          "ra-quiz-qstatus " + (ok ? "ra-quiz-qstatus--ok" : "ra-quiz-qstatus--bad");
      }
    });
  }

  function clearGradeUI(questions) {
    questions.forEach(function (q) {
      q.fieldset.querySelectorAll(".ra-quiz-option").forEach(function (label) {
        label.classList.remove(
          "ra-quiz-option--correct",
          "ra-quiz-option--wrong",
          "ra-quiz-option--missed"
        );
        var input = label.querySelector("input");
        if (input) {
          input.disabled = false;
          input.checked = false;
        }
      });
      if (q.details) {
        q.details.hidden = true;
        try {
          q.details.open = false;
        } catch (e) {
          /* ignore */
        }
      }
      if (q.statusEl) {
        q.statusEl.hidden = true;
        q.statusEl.textContent = "";
      }
    });
  }

  function initQuizPage() {
    var slug = quizSlug();
    if (!slug) return;

    var article =
      document.querySelector("article.md-content__inner") ||
      document.querySelector(".md-content__inner");
    if (!article) return;

    var questions = collectQuestions(article);
    if (questions.length < 2) return;

    article.classList.add("ra-quiz-page");
    var passPercent = parsePassPercent(article);
    var titleEl = article.querySelector("h1");
    var title = titleEl ? titleEl.textContent.trim() : "Quiz";

    var store = loadStore();
    var saved = store[slug] || {};
    var savedAnswers = saved.answers || {};

    var groupName = "ra-quiz-" + slug;
    questions.forEach(function (q) {
      enhanceQuestion(q, groupName, savedAnswers[q.id]);
    });

    /* Soften old tip */
    article.querySelectorAll(".admonition.tip, details.tip").forEach(function (tip) {
      var body = tip.textContent || "";
      if (/Reveal answer|Score yourself/i.test(body)) {
        tip.classList.add("ra-quiz-legacy-tip");
      }
    });

    var banner = document.createElement("div");
    banner.className = "ra-quiz-banner";
    banner.innerHTML =
      "<strong>Interactive mode</strong> — select an answer for each question, watch your progress, then submit for a scored result. Progress is saved in this browser.";
    var h1 = article.querySelector("h1");
    if (h1 && h1.nextSibling) h1.parentNode.insertBefore(banner, h1.nextSibling);
    else article.insertBefore(banner, article.firstChild);

    var toolbar = buildToolbar(questions.length, answeredCount(savedAnswers));
    article.insertBefore(toolbar, banner.nextSibling);
    updateProgress(toolbar, answeredCount(savedAnswers), questions.length);
    /* Toolbar is sticky — remeasure clearance so TOC jumps clear it */
    if (typeof initStickyOffsets === "function") initStickyOffsets();
    else if (typeof syncStickyOffsets === "function") syncStickyOffsets();
    if (typeof initOnThisPageSpy === "function") initOnThisPageSpy();

    var results = document.createElement("div");
    results.className = "ra-quiz-results";
    results.id = "ra-quiz-results";
    results.hidden = true;
    article.appendChild(results);

    function persist(partial) {
      var storeNow = loadStore();
      storeNow[slug] = Object.assign({}, storeNow[slug] || {}, partial, {
        updatedAt: new Date().toISOString(),
      });
      saveStore(storeNow);
    }

    function onAnswerChange() {
      if (article.classList.contains("ra-quiz-page--submitted")) return;
      var answers = gatherAnswers(questions);
      updateProgress(toolbar, answeredCount(answers), questions.length);
      persist({
        answers: answers,
        status: "in_progress",
        total: questions.length,
      });
    }

    questions.forEach(function (q) {
      q.fieldset.addEventListener("change", onAnswerChange);
    });

    function submit() {
      var answers = gatherAnswers(questions);
      var result = grade(questions, answers);
      var pct = result.total
        ? Math.round((result.correct / result.total) * 100)
        : 0;
      var passed = pct >= passPercent;

      article.classList.add("ra-quiz-page--submitted");
      applyGradeUI(questions, answers, true);
      renderResults(results, result, passPercent, title);
      updateProgress(toolbar, answeredCount(answers), questions.length);

      persist({
        answers: answers,
        status: "completed",
        score: result.correct,
        total: result.total,
        percent: pct,
        passed: passed,
        completedAt: new Date().toISOString(),
      });

      /* Offset for sticky header + breadcrumbs + progress bar */
      window.requestAnimationFrame(function () {
        if (typeof syncStickyOffsets === "function") syncStickyOffsets();
        var root = document.documentElement;
        var cs = getComputedStyle(root);
        var offset =
          (parseFloat(cs.getPropertyValue("--ra-header-offset")) || 60) +
          (parseFloat(cs.getPropertyValue("--ra-path-height")) || 30) +
          (parseFloat(cs.getPropertyValue("--ra-quiz-toolbar-height")) || 72) +
          12;
        var top =
          results.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({
          top: Math.max(0, top),
          behavior: "smooth",
        });
      });

      var printBtn = results.querySelector("[data-ra-quiz-print]");
      var retryBtn = results.querySelector("[data-ra-quiz-retry]");
      if (printBtn) {
        printBtn.addEventListener("click", function () {
          var head = results.querySelector(".ra-quiz-results__printhead");
          if (head) head.hidden = false;
          document.body.classList.add("ra-quiz-printing");
          window.print();
          window.setTimeout(function () {
            document.body.classList.remove("ra-quiz-printing");
            if (head) head.hidden = true;
          }, 300);
        });
      }
      if (retryBtn) retryBtn.addEventListener("click", resetQuiz);
    }

    function resetQuiz() {
      article.classList.remove("ra-quiz-page--submitted");
      clearGradeUI(questions);
      results.hidden = true;
      results.innerHTML = "";
      updateProgress(toolbar, 0, questions.length);
      var storeNow = loadStore();
      delete storeNow[slug];
      saveStore(storeNow);
      banner.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    toolbar.querySelectorAll("[data-ra-quiz-submit]").forEach(function (btn) {
      btn.addEventListener("click", submit);
    });
    toolbar.querySelector("[data-ra-quiz-reset]").addEventListener("click", function () {
      if (window.confirm("Clear your answers for this quiz?")) resetQuiz();
    });

    if (saved.status === "completed" && saved.answers) {
      article.classList.add("ra-quiz-page--submitted");
      var restored = grade(questions, saved.answers);
      applyGradeUI(questions, saved.answers, true);
      renderResults(results, restored, passPercent, title);
      var printBtn = results.querySelector("[data-ra-quiz-print]");
      var retryBtn = results.querySelector("[data-ra-quiz-retry]");
      if (printBtn) {
        printBtn.addEventListener("click", function () {
          document.body.classList.add("ra-quiz-printing");
          window.print();
          window.setTimeout(function () {
            document.body.classList.remove("ra-quiz-printing");
          }, 300);
        });
      }
      if (retryBtn) retryBtn.addEventListener("click", resetQuiz);
    }
  }

  function initHub() {
    if (!isQuizHub()) return;
    var store = loadStore();
    var table = document.querySelector("article table");
    if (!table) return;

    var headRow = table.querySelector("thead tr") || table.querySelector("tr");
    if (!headRow) return;

    var th = document.createElement("th");
    th.textContent = "Your progress";
    headRow.appendChild(th);

    var rows = table.querySelectorAll("tbody tr");
    if (!rows.length) rows = Array.prototype.slice.call(table.querySelectorAll("tr")).slice(1);

    Array.prototype.forEach.call(rows, function (tr) {
      var link = tr.querySelector("a[href]");
      var td = document.createElement("td");
      td.className = "ra-quiz-hub-progress";
      if (!link) {
        td.textContent = "—";
        tr.appendChild(td);
        return;
      }
      var href = link.getAttribute("href") || "";
      var slug = href
        .replace(/\/$/, "")
        .split("/")
        .filter(Boolean)
        .pop();
      if (slug) slug = slug.replace(/\.md$/i, "");
      var rec = store[slug];
      if (rec && rec.status === "completed") {
        td.innerHTML =
          '<span class="ra-quiz-hub-badge ra-quiz-hub-badge--' +
          (rec.passed ? "pass" : "fail") +
          '">' +
          (rec.passed ? "Passed" : "Attempted") +
          " · " +
          (rec.percent != null ? rec.percent + "%" : rec.score + "/" + rec.total) +
          "</span>";
      } else if (rec && rec.status === "in_progress") {
        var n = rec.answers ? Object.keys(rec.answers).length : 0;
        td.innerHTML =
          '<span class="ra-quiz-hub-badge ra-quiz-hub-badge--progress">In progress · ' +
          n +
          (rec.total ? "/" + rec.total : "") +
          "</span>";
      } else {
        td.innerHTML = '<span class="ra-quiz-hub-badge">Not started</span>';
      }
      tr.appendChild(td);
    });

    var note = document.createElement("p");
    note.className = "ra-quiz-hub-note";
    note.textContent =
      "Progress is stored in this browser only. Submit a quiz to record your score.";
    table.parentNode.insertBefore(note, table.nextSibling);
  }

  function boot() {
    if (isQuizPage()) initQuizPage();
    if (isQuizHub()) initHub();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(boot);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
