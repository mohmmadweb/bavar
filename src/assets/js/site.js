/* صندوق باور — رفتارهای سمت کاربر (بدون وابستگی) */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var FA = "۰۱۲۳۴۵۶۷۸۹";
  function fa(n) { return String(n).replace(/\d/g, function (d) { return FA[d]; }); }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(k, v) {
    try {
      if (v === undefined) return JSON.parse(localStorage.getItem(k) || "null");
      if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, JSON.stringify(v));
    } catch (e) { return null; }
  }

  /* ---------------------------------------------------------- mobile nav */
  var toggle = $(".nav-toggle"), nav = $("#main-nav");
  if (toggle && nav) {
    var setNav = function (open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "بستن منو" : "باز کردن منو");
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
    };
    toggle.addEventListener("click", function () { setNav(toggle.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav.classList.contains("is-open")) { setNav(false); toggle.focus(); } });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });
  }

  /* ---------------------------------------------------------- hero slider */
  var hero = $("[data-slider]");
  if (hero) {
    var slides = $$(".slide", hero), tabs = $$(".hero-tabs [data-slide]", hero), pauseBtn = $("[data-pause]", hero);
    var DUR = 7000, cur = 0, timer = null, userPaused = reduce, hoverPaused = false;
    hero.style.setProperty("--slide-ms", DUR + "ms");

    var show = function (i, focusTab) {
      i = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        var on = k === i;
        s.hidden = !on;
        s.classList.toggle("is-active", on);
      });
      tabs.forEach(function (t, k) {
        t.setAttribute("aria-selected", k === i ? "true" : "false");
        t.tabIndex = k === i ? 0 : -1;
      });
      // restart progress bar animation
      var bar = tabs[i] && $(".bar i", tabs[i]);
      if (bar) { bar.style.animation = "none"; void bar.offsetWidth; bar.style.animation = ""; }
      cur = i;
      if (focusTab) tabs[i].focus();
      schedule();
    };
    var schedule = function () {
      clearTimeout(timer);
      var playing = !userPaused && !hoverPaused;
      hero.toggleAttribute("data-playing", !userPaused);
      hero.toggleAttribute("data-paused", userPaused || hoverPaused);
      if (playing) timer = setTimeout(function () { show(cur + 1); }, DUR);
    };
    tabs.forEach(function (t, k) {
      t.addEventListener("click", function () { show(k); });
      t.addEventListener("keydown", function (e) {
        // RTL: ArrowLeft = next
        if (e.key === "ArrowLeft") { e.preventDefault(); show(cur + 1, true); }
        if (e.key === "ArrowRight") { e.preventDefault(); show(cur - 1, true); }
      });
    });
    if (pauseBtn) pauseBtn.addEventListener("click", function () {
      userPaused = !userPaused;
      pauseBtn.setAttribute("aria-label", userPaused ? "ادامه‌ی نمایش خودکار" : "توقف نمایش خودکار");
      schedule();
    });
    hero.addEventListener("mouseenter", function () { hoverPaused = true; schedule(); });
    hero.addEventListener("mouseleave", function () { hoverPaused = false; schedule(); });
    hero.addEventListener("focusin", function () { hoverPaused = true; schedule(); });
    hero.addEventListener("focusout", function (e) { if (!hero.contains(e.relatedTarget)) { hoverPaused = false; schedule(); } });
    document.addEventListener("visibilitychange", function () { if (document.hidden) clearTimeout(timer); else schedule(); });
    // swipe
    var x0 = null;
    hero.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) show(dx > 0 ? cur + 1 : cur - 1);
    });
    if (userPaused && pauseBtn) pauseBtn.setAttribute("aria-label", "ادامه‌ی نمایش خودکار");
    schedule();
  }

  /* ---------------------------------------------------------- status: dots + counters */
  var status = $("[data-status]");
  if (status) {
    var counters = $$("[data-count]", status);
    var run = function () {
      status.classList.add("is-in");
      if (reduce) return;
      counters.forEach(function (el) {
        var to = +el.getAttribute("data-count"), plus = el.hasAttribute("data-plus") ? "+" : "", t0 = null, D = 1400;
        var step = function (t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / D), v = Math.round(to * (1 - Math.pow(1 - p, 3)));
          el.textContent = fa(v) + (p === 1 ? plus : "");
          if (p < 1) requestAnimationFrame(step);
        };
        el.textContent = fa(0);
        requestAnimationFrame(step);
      });
    };
    if ("IntersectionObserver" in window && !reduce) {
      var io = new IntersectionObserver(function (en) {
        if (en[0].isIntersecting) { run(); io.disconnect(); }
      }, { threshold: 0.35 });
      io.observe(status);
    } else { status.classList.add("is-in"); }
  }

  /* ---------------------------------------------------------- filter tabs (news / portfolio) */
  $$("[data-filter-group]").forEach(function (group) {
    var target = document.getElementById(group.getAttribute("data-filter-group"));
    if (!target) return;
    var attr = group.getAttribute("data-attr") || "type";
    var limit = +(target.getAttribute("data-limit") || 0);
    var items = $$(":scope > [data-" + attr + "]", target);
    var empty = target.nextElementSibling && target.nextElementSibling.classList.contains("empty") ? target.nextElementSibling : null;
    var buttons = $$("[data-filter]", group);
    var apply = function (key) {
      var shown = 0;
      items.forEach(function (it) {
        var ok = key === "all" || it.getAttribute("data-" + attr) === key;
        if (ok && limit && shown >= limit) ok = false;
        it.hidden = !ok;
        if (ok) shown++;
      });
      if (empty) empty.hidden = shown > 0;
      buttons.forEach(function (b) { b.setAttribute("aria-selected", b.getAttribute("data-filter") === key ? "true" : "false"); });
    };
    buttons.forEach(function (b) { b.addEventListener("click", function () { apply(b.getAttribute("data-filter")); }); });
    apply("all");
  });

  /* ---------------------------------------------------------- dialogs */
  var lastOpener = null;
  $$("[data-open]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var d = document.getElementById(btn.getAttribute("data-open"));
      if (!d || typeof d.showModal !== "function") return;
      lastOpener = btn;
      d.showModal();
      document.body.style.overflow = "hidden";
    });
  });
  $$("dialog.modal").forEach(function (d) {
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    $$("[data-close]", d).forEach(function (b) { b.addEventListener("click", function () { d.close(); }); });
    d.addEventListener("close", function () { document.body.style.overflow = ""; if (lastOpener) lastOpener.focus(); });
  });

  /* ---------------------------------------------------------- simple demo forms (club) */
  $$("[data-demo-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = validate($$("input, select, textarea", f));
      if (!ok) return;
      $$(".field, .btn", f).forEach(function (el) { el.hidden = true; });
      var msg = $(".form-ok", f); msg.hidden = false; msg.focus && msg.setAttribute("tabindex", "-1"); msg.focus();
    });
  });

  function fieldOf(el) { return el.closest(".field") || el.closest(".check"); }
  function validate(els) {
    var first = null;
    els.forEach(function (el) {
      if (el.type === "radio") {
        var groupOk = !el.required || $$('input[name="' + el.name + '"]', el.form).some(function (r) { return r.checked; });
        var fw = fieldOf(el); if (fw) fw.classList.toggle("is-invalid", !groupOk);
        if (!groupOk && !first) first = el;
        return;
      }
      var ok = el.checkValidity();
      var w = fieldOf(el); if (w) w.classList.toggle("is-invalid", !ok);
      if (!ok && !first) first = el;
    });
    if (first) { first.focus(); return false; }
    return true;
  }
  document.addEventListener("input", function (e) {
    var w = e.target.closest && (e.target.closest(".field") || e.target.closest(".check"));
    if (w && w.classList.contains("is-invalid") && e.target.checkValidity()) w.classList.remove("is-invalid");
  });
  document.addEventListener("change", function (e) {
    var w = e.target.closest && (e.target.closest(".field") || e.target.closest(".check"));
    if (w && w.classList.contains("is-invalid") && (e.target.type === "radio" || e.target.checkValidity())) w.classList.remove("is-invalid");
  });

  /* ---------------------------------------------------------- apply form (multi-step) */
  var form = $("[data-apply]");
  if (form) {
    var steps = $$(".fstep", form), inds = $$("[data-step-ind]", form);
    var prev = $("[data-prev]", form), next = $("[data-next]", form), submit = $("[data-submit]", form);
    var draftEl = $("[data-draft]", form), review = $("[data-review]", form);
    var KEY = "bavar-apply-draft", at = 0;
    var params = new URLSearchParams(location.search);

    var go = function (i) {
      at = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      inds.forEach(function (li, k) {
        li.classList.toggle("is-current", k === i);
        li.classList.toggle("is-done", k < i);
        if (k === i) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
      });
      prev.hidden = i === 0;
      next.hidden = i === steps.length - 1;
      submit.hidden = i !== steps.length - 1;
      if (i === steps.length - 1) buildReview();
      var lg = $("legend", steps[i]);
      if (lg) { lg.setAttribute("tabindex", "-1"); lg.focus({ preventScroll: true }); }
      form.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    };
    next.addEventListener("click", function () {
      if (!validate($$("input, select, textarea", steps[at]))) return;
      go(at + 1);
    });
    prev.addEventListener("click", function () { go(at - 1); });

    // draft save / restore (text fields only)
    var saveT = null;
    var save = function () {
      clearTimeout(saveT);
      saveT = setTimeout(function () {
        var data = {};
        $$("input, select, textarea", form).forEach(function (el) {
          if (!el.name || el.type === "file") return;
          if (el.type === "radio") { if (el.checked) data[el.name] = el.value; return; }
          if (el.type === "checkbox") return;
          data[el.name] = el.value;
        });
        store(KEY, data);
        if (draftEl) draftEl.textContent = "پیش‌نویس ذخیره شد";
      }, 500);
    };
    var restore = store(KEY);
    if (restore) {
      Object.keys(restore).forEach(function (k) {
        var els = $$('[name="' + k + '"]', form);
        els.forEach(function (el) {
          if (el.type === "radio") el.checked = el.value === restore[k];
          else el.value = restore[k];
        });
      });
      if (draftEl) draftEl.textContent = "پیش‌نویس قبلی بازیابی شد";
    }
    var pre = params.get("sector");
    if (pre && $('#a-sector option[value="' + pre + '"]')) $("#a-sector").value = pre;
    if (params.get("from") === "zarban") {
      var t = $("#a-title"); if (t && !t.value) t.placeholder = "عنوان طرح برای رویداد ملی ضربان";
    }
    form.addEventListener("input", save);
    form.addEventListener("change", save);

    // char counter
    $$("[data-counter]", form).forEach(function (c) {
      var ta = document.getElementById(c.getAttribute("data-counter"));
      var upd = function () { c.textContent = fa(ta.value.length); };
      ta.addEventListener("input", upd); upd();
    });

    // file drop labels
    $$(".drop", form).forEach(function (d) {
      var inp = $("input", d), txt = $(".drop-t", d), orig = txt.textContent;
      inp.addEventListener("change", function () {
        var f = inp.files && inp.files[0];
        d.classList.toggle("has-file", !!f);
        txt.textContent = f ? f.name + " (" + fa((f.size / 1048576).toFixed(1)).replace(".", "٫") + " مگابایت)" : orig;
      });
      ["dragenter", "dragover"].forEach(function (ev) { d.addEventListener(ev, function () { d.classList.add("is-over"); }); });
      ["dragleave", "drop"].forEach(function (ev) { d.addEventListener(ev, function () { d.classList.remove("is-over"); }); });
    });

    var buildReview = function () {
      var get = function (n) { var el = $('[name="' + n + '"]:checked', form) || $('[name="' + n + '"]', form); return el ? el.value : ""; };
      var sectorSel = $("#a-sector"), stage = $('[name="stage"]:checked', form);
      var rows = [
        ["متقاضی", get("name")],
        ["عنوان طرح", get("title")],
        ["محور", sectorSel.value ? sectorSel.options[sectorSel.selectedIndex].text : ""],
        ["مرحله", stage ? $("strong", stage.parentNode).textContent : ""],
        ["تعداد اعضا", get("size") ? fa(get("size")) + " نفر" : ""]
      ];
      review.innerHTML = "<dl>" + rows.map(function (r) {
        return "<dt>" + r[0] + "</dt><dd>" + (r[1] ? escapeHtml(r[1]) : "—") + "</dd>";
      }).join("") + "</dl>";
    };
    function escapeHtml(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate($$("input, select, textarea", steps[at]))) return;
      var code = "BV-1405-" + String(Math.floor(1000 + Math.random() * 9000));
      store(KEY, null);
      form.hidden = true;
      var done = $("[data-done]");
      $("[data-code]", done).textContent = code;
      done.hidden = false;
      done.focus();
      done.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    });
  }
})();
