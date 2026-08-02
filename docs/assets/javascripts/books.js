/* REBASH Academy – free book registration gate */

(function () {
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function $(sel, root) {
    return (root || document).querySelector(sel);
  }

  function readRegistration(key) {
    try {
      var raw = localStorage.getItem(key);
      if (!raw) return null;
      var data = JSON.parse(raw);
      if (!data || !data.email || !data.ts) return null;
      // Re-prompt after 365 days
      if (Date.now() - data.ts > 365 * 24 * 60 * 60 * 1000) return null;
      return data;
    } catch (e) {
      return null;
    }
  }

  function writeRegistration(key, payload) {
    localStorage.setItem(
      key,
      JSON.stringify({
        name: payload.name || "",
        email: payload.email,
        book_interest: payload.book_interest || "",
        ts: Date.now()
      })
    );
  }

  function setStatus(el, message, kind) {
    if (!el) return;
    el.hidden = !message;
    el.textContent = message || "";
    el.classList.remove("is-error", "is-ok", "is-pending");
    if (kind) el.classList.add("is-" + kind);
  }

  function showDownloads(root, gate, downloads) {
    if (gate) gate.hidden = true;
    if (downloads) {
      downloads.hidden = false;
      downloads.setAttribute("data-unlocked", "true");
    }
    root.classList.add("is-unlocked");
  }

  function showGate(root, gate, downloads) {
    if (gate) gate.hidden = false;
    if (downloads) {
      downloads.hidden = true;
      downloads.removeAttribute("data-unlocked");
    }
    root.classList.remove("is-unlocked");
  }

  function submitLead(root, fields) {
    var formspreeId = (root.getAttribute("data-formspree-id") || "").trim();
    var web3Key = (root.getAttribute("data-web3forms-key") || "").trim();

    if (web3Key) {
      return fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        },
        body: JSON.stringify({
          access_key: web3Key,
          subject: "REBASH Academy — free book registration",
          from_name: "REBASH Academy Books",
          name: fields.name,
          email: fields.email,
          book_interest: fields.book_interest,
          message:
            fields.name +
            " (" +
            fields.email +
            ") registered for free book downloads. Interest: " +
            fields.book_interest +
            "."
        })
      }).then(function (res) {
        if (!res.ok) throw new Error("Registration service returned " + res.status);
        return res.json();
      });
    }

    if (formspreeId) {
      return fetch("https://formspree.io/f/" + formspreeId, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json"
        },
        body: JSON.stringify({
          name: fields.name,
          email: fields.email,
          book_interest: fields.book_interest,
          _subject: "REBASH Academy — free book registration"
        })
      }).then(function (res) {
        if (!res.ok) throw new Error("Registration service returned " + res.status);
        return res.json().catch(function () {
          return {};
        });
      });
    }

    return Promise.reject(
      new Error(
        "Book registration is not configured yet. Add formspree_form_id or web3forms_access_key under extra.books in mkdocs.yml."
      )
    );
  }

  function initBooksGate() {
    var root = $("#rebash-books");
    if (!root || root.dataset.bound === "1") return;
    root.dataset.bound = "1";

    var key = root.getAttribute("data-storage-key") || "rebash-books-registered";
    var gate = $("#rebash-books-gate", root);
    var downloads = $("#rebash-books-downloads", root);
    var form = $("#rebash-books-form", root);
    var status = $("#rebash-books-status", root);

    // Soft-hide direct download URLs until unlocked (still not true DRM)
    if (downloads) {
      downloads.querySelectorAll("a[href]").forEach(function (link) {
        link.addEventListener("click", function (ev) {
          if (!readRegistration(key)) {
            ev.preventDefault();
            showGate(root, gate, downloads);
            setStatus(status, "Please register free to unlock downloads.", "error");
            if (gate) gate.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        });
      });
    }

    if (readRegistration(key)) {
      showDownloads(root, gate, downloads);
      return;
    }

    showGate(root, gate, downloads);

    if (!form) return;

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var fd = new FormData(form);
      if ((fd.get("_gotcha") || "").toString().trim()) {
        return; // honeypot
      }

      var name = (fd.get("name") || "").toString().trim();
      var email = (fd.get("email") || "").toString().trim().toLowerCase();
      var bookInterest = (fd.get("book_interest") || "").toString().trim();
      var consent = fd.get("consent");

      if (!name || name.length < 2) {
        setStatus(status, "Please enter your name.", "error");
        return;
      }
      if (!EMAIL_RE.test(email)) {
        setStatus(status, "Please enter a valid email address.", "error");
        return;
      }
      if (!bookInterest) {
        bookInterest = "linux";
      }
      if (!consent) {
        setStatus(status, "Please accept the privacy notice to continue.", "error");
        return;
      }

      var submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;
      setStatus(status, "Registering…", "pending");

      var payload = {
        name: name,
        email: email,
        book_interest: bookInterest
      };

      submitLead(root, payload)
        .then(function () {
          writeRegistration(key, payload);
          setStatus(status, "Registration complete — downloads unlocked.", "ok");
          showDownloads(root, gate, downloads);
          if (downloads) {
            downloads.scrollIntoView({ behavior: "smooth", block: "start" });
          }
        })
        .catch(function (err) {
          setStatus(
            status,
            (err && err.message) || "Registration failed. Please try again in a moment.",
            "error"
          );
        })
        .finally(function () {
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  }

  function onReady() {
    initBooksGate();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(onReady);
  } else {
    document.addEventListener("DOMContentLoaded", onReady);
  }
})();
