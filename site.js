/* Starlit Camp site runtime: applies games.js status and remembers the chosen language. */
(function () {
  var G = window.STARLIT_GAMES || {};

  function url(game, kind) {
    var g = G[game];
    if (!g) return null;
    if (kind === "group") return "https://groups.google.com/g/" + g.group;
    if (kind === "optin") return "https://play.google.com/apps/testing/" + g.package;
    if (kind === "store") return "https://play.google.com/store/apps/details?id=" + g.package;
    if (kind === "appstore") return g.appStore || null;
    return null;
  }

  function apply() {
    var i, el, g, list;
    // Blocks that depend on one game's status: data-game="x" data-when="testing released"
    list = document.querySelectorAll("[data-game][data-when]");
    for (i = 0; i < list.length; i++) {
      el = list[i];
      g = G[el.getAttribute("data-game")];
      if (!g) continue;
      el.hidden = (" " + el.getAttribute("data-when") + " ").indexOf(" " + g.status + " ") < 0;
    }
    // Links: data-game="x" data-href="group|optin|store|appstore"
    list = document.querySelectorAll("[data-game][data-href]");
    for (i = 0; i < list.length; i++) {
      el = list[i];
      var u = url(el.getAttribute("data-game"), el.getAttribute("data-href"));
      if (u) { el.href = u; if (!el.hasAttribute("data-when")) el.hidden = false; }
      else if (el.getAttribute("data-href") === "appstore") el.hidden = true;
    }
    // Sections shown only if at least one game is in one of the statuses: data-any="recruiting testing"
    list = document.querySelectorAll("[data-any]");
    for (i = 0; i < list.length; i++) {
      el = list[i];
      var want = " " + el.getAttribute("data-any") + " ", any = false;
      for (var k in G) if (want.indexOf(" " + G[k].status + " ") >= 0) any = true;
      el.hidden = !any;
    }
  }

  // Remember the language the visitor picks in the switcher.
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[data-setlang]") : null;
    if (a) { try { localStorage.setItem("sc_lang", a.getAttribute("data-setlang")); } catch (_) {} }
  });

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", apply);
  else apply();
})();
