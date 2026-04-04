(function () {
  function createShareUrl(platform, url, title) {
    if (platform === "facebook") return "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url);
    if (platform === "linkedin") return "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url);
    if (platform === "x") return "https://twitter.com/intent/tweet?url=" + encodeURIComponent(url) + "&text=" + encodeURIComponent(title);
    if (platform === "pinterest") return "https://pinterest.com/pin/create/button/?url=" + encodeURIComponent(url) + "&description=" + encodeURIComponent(title);
    return "#";
  }

  function mountShareBar() {
    var main = document.querySelector("main.page-content");
    if (!main || document.querySelector(".share-post")) return;

    var pageUrl = window.location.href.split("#")[0];
    var pageTitle = document.title.replace(" | 4Globetrotters", "");

    var wrap = document.createElement("section");
    wrap.className = "share-post";
    wrap.style.margin = "28px 0";
    wrap.style.padding = "18px 20px";
    wrap.style.border = "1px solid #e8e8e8";
    wrap.style.borderRadius = "10px";
    wrap.style.background = "#fafafa";

    var title = document.createElement("h3");
    title.textContent = "Share This Story";
    title.style.margin = "0 0 10px 0";
    title.style.fontSize = "1.15rem";
    title.style.fontFamily = "Playfair Display, Georgia, serif";

    var p = document.createElement("p");
    p.textContent = "Enjoyed this post? Share it with friends planning family travel.";
    p.style.margin = "0 0 12px 0";
    p.style.color = "#666";

    var row = document.createElement("div");
    row.style.display = "flex";
    row.style.gap = "10px";
    row.style.flexWrap = "wrap";

    var items = [
      ["Facebook", "facebook"],
      ["LinkedIn", "linkedin"],
      ["X", "x"],
      ["Pinterest", "pinterest"]
    ];

    items.forEach(function (item) {
      var a = document.createElement("a");
      a.href = createShareUrl(item[1], pageUrl, pageTitle);
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.textContent = item[0];
      a.style.display = "inline-block";
      a.style.padding = "8px 12px";
      a.style.border = "1px solid #d9d9d9";
      a.style.borderRadius = "999px";
      a.style.fontSize = ".85rem";
      a.style.color = "#444";
      a.style.textDecoration = "none";
      row.appendChild(a);
    });

    wrap.appendChild(title);
    wrap.appendChild(p);
    wrap.appendChild(row);

    var comments = document.querySelector(".comments-section");
    if (comments && comments.parentNode === main) {
      main.insertBefore(wrap, comments);
    } else {
      main.appendChild(wrap);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountShareBar);
  } else {
    mountShareBar();
  }
})();
