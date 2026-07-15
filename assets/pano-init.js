/* Lazy-init 360° panoramas on blog posts.
   Markup:  <div class="pano-embed" data-pano="/wp-content/uploads/2026/07/xxx-360.jpg"
                 data-caption="optional caption"></div>
   Pannellum (self-hosted in /assets/pannellum/) is loaded on demand only when a
   post actually contains a .pano-embed, so other pages stay lightweight. */
(function () {
  var nodes = document.querySelectorAll('.pano-embed[data-pano]');
  if (!nodes.length) return;

  function loadOnce(tag, attrs) {
    return new Promise(function (resolve) {
      var el = document.createElement(tag);
      Object.keys(attrs).forEach(function (k) { el[k] = attrs[k]; });
      el.onload = resolve;
      document.head.appendChild(el);
    });
  }

  Promise.all([
    loadOnce('link', { rel: 'stylesheet', href: '/assets/pannellum/pannellum.css' }),
    loadOnce('script', { src: '/assets/pannellum/pannellum.js' })
  ]).then(function () {
    nodes.forEach(function (node, i) {
      var id = 'pano-' + i;
      var holder = document.createElement('div');
      holder.id = id;
      holder.className = 'pano-viewer';
      node.appendChild(holder);
      // Only build the (heavy) sphere when scrolled near, to keep the page snappy.
      var built = false;
      function build() {
        if (built) return; built = true;
        window.pannellum.viewer(id, {
          type: 'equirectangular',
          panorama: node.getAttribute('data-pano'),
          autoLoad: true,
          autoRotate: -2,
          compass: false,
          showZoomCtrl: true,
          hfov: 100
        });
      }
      if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) { if (e.isIntersecting) { build(); io.disconnect(); } });
        }, { rootMargin: '200px' });
        io.observe(node);
      } else {
        build();
      }
      var cap = node.getAttribute('data-caption');
      if (cap) {
        var c = document.createElement('p');
        c.className = 'pano-caption';
        c.textContent = cap;
        node.appendChild(c);
      }
    });
  });
})();
