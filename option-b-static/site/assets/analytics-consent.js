/* 4Globetrotters — GDPR-friendly analytics consent + GA4 loader
 * GA4 only loads AFTER the visitor clicks "Accept".
 * Choice is remembered in localStorage ("4gt-consent" = "granted" | "denied").
 */
(function () {
  "use strict";

  var GA_ID = "G-2JR7DEFXX6";
  var STORAGE_KEY = "4gt-consent";

  function loadGA() {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;

    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", GA_ID, { anonymize_ip: true });
  }

  function setConsent(value) {
    try { localStorage.setItem(STORAGE_KEY, value); } catch (e) {}
    if (value === "granted") loadGA();
  }

  function getConsent() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { return null; }
  }

  function buildBanner() {
    var bar = document.createElement("div");
    bar.id = "consent-banner";
    bar.setAttribute("role", "dialog");
    bar.setAttribute("aria-label", "Cookie consent");
    bar.innerHTML =
      '<div class="consent-inner">' +
        '<p class="consent-text">We use cookies for anonymous visitor analytics to understand which travel stories you enjoy. ' +
        'See our <a href="/privacy-policy/">privacy policy</a>.</p>' +
        '<div class="consent-actions">' +
          '<button type="button" class="consent-btn consent-decline" id="consent-decline">Decline</button>' +
          '<button type="button" class="consent-btn consent-accept" id="consent-accept">Accept</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(bar);

    document.getElementById("consent-accept").addEventListener("click", function () {
      setConsent("granted");
      bar.remove();
    });
    document.getElementById("consent-decline").addEventListener("click", function () {
      setConsent("denied");
      bar.remove();
    });
  }

  function init() {
    var choice = getConsent();
    if (choice === "granted") { loadGA(); return; }
    if (choice === "denied") { return; }
    buildBanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
