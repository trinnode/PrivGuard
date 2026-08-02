(function () {
  "use strict";

  /* ============================
     DARK MODE
     ============================ */
  var SK = "privguard_theme";

  function getTheme() {
    return localStorage.getItem(SK) || "light";
  }

  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(SK, theme);
    var btn = document.querySelector(".dark-mode-toggle");
    if (btn) {
      btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }
  }

  setTheme(getTheme());

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest(".dark-mode-toggle");
    if (toggle) {
      e.preventDefault();
      setTheme(getTheme() === "dark" ? "light" : "dark");
    }
  });

  /* ============================
     MOBILE MENU
     ============================ */
  var menuToggle = document.querySelector(".mobile-menu-toggle");
  var nav = document.querySelector(".nav-links");
  if (menuToggle && nav) {
    menuToggle.addEventListener("click", function () {
      nav.classList.toggle("is-open");
      menuToggle.setAttribute("aria-expanded", nav.classList.contains("is-open"));
    });
    document.addEventListener("click", function (e) {
      if (!menuToggle.contains(e.target) && !nav.contains(e.target)) {
        nav.classList.remove("is-open");
        menuToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ============================
     HEADER SCROLL EFFECT
     ============================ */
  var header = document.querySelector(".site-header");
  if (header) {
    var lastScroll = 0;
    window.addEventListener("scroll", function () {
      var st = window.pageYOffset;
      if (st > 10) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
      lastScroll = st;
    }, { passive: true });
  }

  /* ============================
     AUTO-DISMISS ALERTS
     ============================ */
  document.querySelectorAll(".messages-list .alert").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity 0.4s, transform 0.4s";
      el.style.opacity = "0";
      el.style.transform = "translateY(-8px)";
      setTimeout(function () { if (el.parentNode) el.remove(); }, 400);
    }, 5000);
  });

  /* ============================
     MODAL
     ============================ */
  function openModal(html) {
    var overlay = document.createElement("div");
    overlay.className = "modal-overlay";
    overlay.innerHTML = '<div class="modal-dialog">' +
      '<div class="modal-header">' +
        '<h2>Report an Incident</h2>' +
        '<button class="modal-close" aria-label="Close">&times;</button>' +
      '</div>' +
      '<div class="modal-body">' + html + '</div>' +
    '</div>';
    document.body.appendChild(overlay);
    document.body.classList.add("modal-open");

    overlay.querySelector(".modal-close").addEventListener("click", function () {
      closeModal(overlay);
    });
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeModal(overlay);
    });
    document.addEventListener("keydown", function handler(e) {
      if (e.key === "Escape") { closeModal(overlay); document.removeEventListener("keydown", handler); }
    });
    return overlay;
  }

  function closeModal(overlay) {
    overlay.classList.add("closing");
    setTimeout(function () { overlay.remove(); document.body.classList.remove("modal-open"); }, 200);
  }

  /* ============================
     MULTI-STEP FORM WIZARD
     ============================ */
  var form = document.getElementById("incident-form");
  if (form) {
    var stepPanels = form.querySelectorAll(".wizard-step-content");
    var stepIndicators = form.querySelectorAll(".wizard-step");
    var progressFill = form.querySelector(".wizard-progress-fill");
    var progressPct = form.querySelector(".wizard-percentage");
    var currentStep = 0;

    function updateWizard() {
      var total = stepPanels.length;
      var pct = Math.round(((currentStep + 1) / total) * 100);

      stepPanels.forEach(function (p, i) {
        p.style.display = i === currentStep ? "block" : "none";
      });
      stepIndicators.forEach(function (s, i) {
        s.classList.toggle("is-active", i === currentStep);
        s.classList.toggle("is-done", i < currentStep);
      });
      if (progressFill) progressFill.style.width = pct + "%";
      if (progressPct) progressPct.textContent = pct + "% complete";
    }

    function validateStep(idx) {
      var panel = stepPanels[idx];
      var required = panel.querySelectorAll("[required]");
      var valid = true;
      required.forEach(function (f) {
        if (!f.value.trim()) { f.classList.add("is-invalid"); f.style.borderColor = "var(--error)"; valid = false; }
        else { f.classList.remove("is-invalid"); f.style.borderColor = ""; }
      });
      return valid;
    }

    form.addEventListener("click", function (e) {
      var nextBtn = e.target.closest(".wizard-next");
      var backBtn = e.target.closest(".wizard-back");
      if (nextBtn) {
        e.preventDefault();
        if (validateStep(currentStep) && currentStep < stepPanels.length - 1) {
          currentStep++;
          updateWizard();
          var formTop = form.closest(".modal-body") ? form.closest(".modal-dialog") : form;
          formTop.scrollTo ? formTop.scrollTo({ top: 0, behavior: "smooth" }) : window.scrollTo({ top: form.offsetTop - 80, behavior: "smooth" });
        }
      }
      if (backBtn) {
        e.preventDefault();
        if (currentStep > 0) {
          currentStep--;
          updateWizard();
          var formTop = form.closest(".modal-body") ? form.closest(".modal-dialog") : form;
          formTop.scrollTo ? formTop.scrollTo({ top: 0, behavior: "smooth" }) : window.scrollTo({ top: form.offsetTop - 80, behavior: "smooth" });
        }
      }
    });

    updateWizard();

    /* ---- Harm toggle ---- */
    var harmCount = document.getElementById("harm-count");

    function updateHarmCount() {
      if (!harmCount) return;
      var checked = form.querySelectorAll('.harm-option input[type="checkbox"]:checked');
      var n = checked.length;
      harmCount.textContent = n + " harm categor" + (n === 1 ? "y" : "ies") + " selected";
    }

    form.querySelectorAll(".harm-option").forEach(function (opt) {
      var cb = opt.querySelector('input[type="checkbox"]');
      if (!cb) return;

      cb.addEventListener("change", function () {
        opt.classList.toggle("is-selected", this.checked);
        var details = opt.querySelector(".harm-details");
        if (details) details.style.display = this.checked ? "block" : "none";
        updateHarmCount();
      });

      opt.addEventListener("click", function (e) {
        if (e.target.closest("select") || e.target.closest("textarea") || e.target.closest("input")) return;
        cb.checked = !cb.checked;
        cb.dispatchEvent(new Event("change", { bubbles: true }));
      });

      opt.setAttribute("tabindex", "0");
      opt.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          cb.checked = !cb.checked;
          cb.dispatchEvent(new Event("change", { bubbles: true }));
        }
      });
    });

    updateHarmCount();

    /* ---- Form submit ---- */
    form.addEventListener("submit", function () {
      var submitBtn = form.querySelector("[type='submit']");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 0.7s linear infinite;width:16px;height:16px"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg> Submitting...';
      }
    });
  }

  /* ============================
     FILE UPLOAD
     ============================ */
  document.querySelectorAll("input[type='file']").forEach(function (input) {
    input.addEventListener("change", function () {
      var area = this.closest(".upload-area");
      if (!area) return;
      if (this.files && this.files.length > 0) {
        var file = this.files[0];
        if (file.size > 100 * 1024) {
          showToast("File too large. Maximum is 100KB.", "error");
          this.value = "";
          area.classList.remove("has-file");
          return;
        }
        if (!["image/png", "image/jpeg", "application/pdf"].includes(file.type)) {
          showToast("Only PNG, JPEG, and PDF files are allowed.", "error");
          this.value = "";
          area.classList.remove("has-file");
          return;
        }
        area.classList.add("has-file");
        var label = area.querySelector(".upload-label");
        if (label) {
          var size = file.size < 1024 ? file.size + " B" : file.size < 1048576 ? (file.size / 1024).toFixed(1) + " KB" : (file.size / 1048576).toFixed(1) + " MB";
          label.textContent = file.name + " (" + size + ")";
        }
      } else {
        area.classList.remove("has-file");
        var label = area.querySelector(".upload-label");
        if (label) label.textContent = "Drop a file here or click to browse. PNG, JPEG, or PDF. Max 100KB.";
      }
    });
  });

  /* ============================
     TOAST
     ============================ */
  function showToast(message, type) {
    type = type || "info";
    var container = document.querySelector(".toast-container");
    if (!container) {
      container = document.createElement("div");
      container.className = "toast-container";
      document.body.appendChild(container);
    }
    var toast = document.createElement("div");
    toast.className = "toast toast-" + type;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(function () { if (toast.parentNode) toast.remove(); }, 5000);
  }
  window.showToast = showToast;

  /* ============================
     DISTRESS DETECTION
     ============================ */
  var narrativeField = document.querySelector("#id_narrative");
  var supportBanner = document.getElementById("support-banner");
  var keywords = ["suicide", "kill myself", "end my life", "self-harm", "hurt myself", "not safe", "afraid", "scared", "traumatized", "can't cope", "desperate", "panic", "terrified"];
  if (narrativeField && supportBanner) {
    narrativeField.addEventListener("input", function () {
      var text = this.value.toLowerCase();
      supportBanner.style.display = keywords.some(function (k) { return text.includes(k); }) ? "block" : "none";
    });
  }

  /* ============================
     CONFIRM DESTRUCTIVE
     ============================ */
  document.querySelectorAll("[data-confirm]").forEach(function (el) {
    el.addEventListener("click", function (e) {
      if (!confirm(this.getAttribute("data-confirm") || "Are you sure?")) e.preventDefault();
    });
  });

  /* ============================
     PARALLAX
     ============================ */
  if (window.innerWidth >= 1024) {
    var par = document.querySelectorAll("[data-parallax]");
    if (par.length > 0) {
      window.addEventListener("scroll", function () {
        var y = window.pageYOffset;
        par.forEach(function (el) {
          var r = parseFloat(el.getAttribute("data-parallax-rate")) || 0.08;
          el.style.setProperty("--parallax-offset", Math.min(y * r, 60) + "px");
        });
      }, { passive: true });
    }
  }

  /* ============================
     SMOOTH PAGE TRANSITIONS
     ============================ */
  document.querySelectorAll('a[href^="/"]').forEach(function (link) {
    if (link.closest("nav") || link.closest(".modal")) return;
    link.addEventListener("click", function (e) {
      if (e.ctrlKey || e.metaKey || e.shiftKey) return;
      var href = this.getAttribute("href");
      if (href && href !== window.location.pathname) {
        document.body.style.opacity = "0.7";
        document.body.style.transition = "opacity 0.15s";
      }
    });
  });

  /* ============================
     ACCESSIBILITY: FOCUS STYLES
     ============================ */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Tab") {
      document.body.classList.add("using-keyboard");
    }
  });
  document.addEventListener("mousedown", function () {
    document.body.classList.remove("using-keyboard");
  });
})();
