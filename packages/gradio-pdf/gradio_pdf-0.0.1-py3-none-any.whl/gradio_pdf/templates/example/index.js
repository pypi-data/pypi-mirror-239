const {
  SvelteComponent: g,
  append: y,
  attr: c,
  detach: o,
  element: u,
  init: v,
  insert: b,
  noop: d,
  safe_not_equal: w,
  set_style: f,
  src_url_equal: m,
  toggle_class: _
} = window.__gradio__svelte__internal;
function E(a) {
  let e, l, i;
  return {
    c() {
      e = u("div"), l = u("iframe"), c(l, "title", "Example pdf"), m(l.src, i = /*samples_dir*/
      a[1] + /*value*/
      a[0]) || c(l, "src", i), f(e, "justify-content", "center"), f(e, "align-items", "center"), f(e, "display", "flex"), f(e, "flex-direction", "column"), c(e, "class", "svelte-1gecy8w"), _(
        e,
        "table",
        /*type*/
        a[2] === "table"
      ), _(
        e,
        "gallery",
        /*type*/
        a[2] === "gallery"
      ), _(
        e,
        "selected",
        /*selected*/
        a[3]
      );
    },
    m(t, s) {
      b(t, e, s), y(e, l);
    },
    p(t, [s]) {
      s & /*samples_dir, value*/
      3 && !m(l.src, i = /*samples_dir*/
      t[1] + /*value*/
      t[0]) && c(l, "src", i), s & /*type*/
      4 && _(
        e,
        "table",
        /*type*/
        t[2] === "table"
      ), s & /*type*/
      4 && _(
        e,
        "gallery",
        /*type*/
        t[2] === "gallery"
      ), s & /*selected*/
      8 && _(
        e,
        "selected",
        /*selected*/
        t[3]
      );
    },
    i: d,
    o: d,
    d(t) {
      t && o(e);
    }
  };
}
function h(a, e, l) {
  let { value: i } = e, { samples_dir: t } = e, { type: s } = e, { selected: r = !1 } = e;
  return a.$$set = (n) => {
    "value" in n && l(0, i = n.value), "samples_dir" in n && l(1, t = n.samples_dir), "type" in n && l(2, s = n.type), "selected" in n && l(3, r = n.selected);
  }, [i, t, s, r];
}
class q extends g {
  constructor(e) {
    super(), v(this, e, h, E, w, {
      value: 0,
      samples_dir: 1,
      type: 2,
      selected: 3
    });
  }
}
export {
  q as default
};
