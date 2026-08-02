/* Justified-rows gallery layout.
   For each .wp-block-gallery, read every figure's aspect ratio (from its
   inline --ar, else from the loaded image) and lay them out in rows that each
   fill the container width at a shared height — so every photo is shown in
   full, no crop and no letterbox. Re-runs on resize. */
(function () {
  var GAP = 12;          // must match the CSS gap
  var TARGET_H = 320;    // desired row height (used only for row packing)
  var MAX_ROW_H = 680;   // cap so a row of tall portraits can't balloon

  function arOf(fig) {
    var v = parseFloat(fig.style.getPropertyValue('--ar'));
    if (v && isFinite(v) && v > 0) return v;
    var img = fig.querySelector('img');
    if (img && img.naturalWidth && img.naturalHeight) {
      return img.naturalWidth / img.naturalHeight;
    }
    return 1.3333;
  }

  function layout(gallery) {
    var figs = Array.prototype.filter.call(
      gallery.children,
      function (c) { return c.classList && c.classList.contains('wp-block-image'); }
    );
    if (!figs.length) return;

    var containerW = gallery.clientWidth;
    if (!containerW) return;

    var items = figs.map(function (f) { return { el: f, ar: arOf(f) }; });

    // Greedy row packing: add images until the row (at TARGET_H) overflows.
    var rows = [];
    var row = [];
    var rowArSum = 0;
    items.forEach(function (it) {
      row.push(it);
      rowArSum += it.ar;
      // width at target height = rowArSum*TARGET_H + gaps
      var w = rowArSum * TARGET_H + GAP * (row.length - 1);
      if (w >= containerW) {
        rows.push(row);
        row = [];
        rowArSum = 0;
      }
    });
    if (row.length) rows.push(row);

    rows.forEach(function (cells) {
      var arSum = cells.reduce(function (s, it) { return s + it.ar; }, 0);
      var avail = containerW - GAP * (cells.length - 1);
      // justify the row to the full content width
      var h = avail / arSum;
      // guard against a row of tall portraits becoming absurdly big: cap the
      // height (the row then no longer fills full width, so centre it)
      if (h > MAX_ROW_H) h = MAX_ROW_H;
      cells.forEach(function (it) {
        var w = Math.round(h * it.ar);
        it.el.style.width = w + 'px';
        it.el.style.height = Math.round(h) + 'px';
        it.el.style.flex = '0 0 auto';
      });
    });

    gallery.classList.add('jg-ready');
  }

  function layoutAll() {
    var galleries = document.querySelectorAll('.page-content .wp-block-gallery');
    Array.prototype.forEach.call(galleries, layout);
  }

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    layoutAll();
    // Re-run once images have loaded (natural sizes may refine ratios)
    window.addEventListener('load', layoutAll);
    var t;
    window.addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(layoutAll, 120);
    });
  });
})();
