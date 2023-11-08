const {
  SvelteComponent: Ei,
  append: kt,
  attr: oe,
  detach: Si,
  init: Ti,
  insert: Bi,
  noop: Mt,
  safe_not_equal: Ai,
  set_style: de,
  svg_element: pt
} = window.__gradio__svelte__internal;
function Hi(e) {
  let t, n, r, i;
  return {
    c() {
      t = pt("svg"), n = pt("g"), r = pt("path"), i = pt("path"), oe(r, "d", "M18,6L6.087,17.913"), de(r, "fill", "none"), de(r, "fill-rule", "nonzero"), de(r, "stroke-width", "2px"), oe(n, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), oe(i, "d", "M4.364,4.364L19.636,19.636"), de(i, "fill", "none"), de(i, "fill-rule", "nonzero"), de(i, "stroke-width", "2px"), oe(t, "width", "100%"), oe(t, "height", "100%"), oe(t, "viewBox", "0 0 24 24"), oe(t, "version", "1.1"), oe(t, "xmlns", "http://www.w3.org/2000/svg"), oe(t, "xmlns:xlink", "http://www.w3.org/1999/xlink"), oe(t, "xml:space", "preserve"), oe(t, "stroke", "currentColor"), de(t, "fill-rule", "evenodd"), de(t, "clip-rule", "evenodd"), de(t, "stroke-linecap", "round"), de(t, "stroke-linejoin", "round");
    },
    m(s, o) {
      Bi(s, t, o), kt(t, n), kt(n, r), kt(t, i);
    },
    p: Mt,
    i: Mt,
    o: Mt,
    d(s) {
      s && Si(t);
    }
  };
}
class Ni extends Ei {
  constructor(t) {
    super(), Ti(this, t, null, Hi, Ai, {});
  }
}
const {
  SvelteComponent: Pi,
  append: xi,
  attr: ae,
  detach: Ci,
  init: Ii,
  insert: Oi,
  noop: Rt,
  safe_not_equal: Li,
  svg_element: Pn
} = window.__gradio__svelte__internal;
function ki(e) {
  let t, n;
  return {
    c() {
      t = Pn("svg"), n = Pn("path"), ae(n, "d", "M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"), ae(t, "xmlns", "http://www.w3.org/2000/svg"), ae(t, "width", "100%"), ae(t, "height", "100%"), ae(t, "viewBox", "0 0 24 24"), ae(t, "fill", "none"), ae(t, "stroke", "currentColor"), ae(t, "stroke-width", "1.5"), ae(t, "stroke-linecap", "round"), ae(t, "stroke-linejoin", "round"), ae(t, "class", "feather feather-edit-2");
    },
    m(r, i) {
      Oi(r, t, i), xi(t, n);
    },
    p: Rt,
    i: Rt,
    o: Rt,
    d(r) {
      r && Ci(t);
    }
  };
}
class Mi extends Pi {
  constructor(t) {
    super(), Ii(this, t, null, ki, Li, {});
  }
}
const {
  SvelteComponent: Ri,
  append: xn,
  attr: $,
  detach: Di,
  init: Ui,
  insert: Fi,
  noop: Dt,
  safe_not_equal: Gi,
  svg_element: Ut
} = window.__gradio__svelte__internal;
function ji(e) {
  let t, n, r;
  return {
    c() {
      t = Ut("svg"), n = Ut("path"), r = Ut("polyline"), $(n, "d", "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"), $(r, "points", "13 2 13 9 20 9"), $(t, "xmlns", "http://www.w3.org/2000/svg"), $(t, "width", "100%"), $(t, "height", "100%"), $(t, "viewBox", "0 0 24 24"), $(t, "fill", "none"), $(t, "stroke", "currentColor"), $(t, "stroke-width", "1.5"), $(t, "stroke-linecap", "round"), $(t, "stroke-linejoin", "round"), $(t, "class", "feather feather-file");
    },
    m(i, s) {
      Fi(i, t, s), xn(t, n), xn(t, r);
    },
    p: Dt,
    i: Dt,
    o: Dt,
    d(i) {
      i && Di(t);
    }
  };
}
let qi = class extends Ri {
  constructor(t) {
    super(), Ui(this, t, null, ji, Gi, {});
  }
};
const {
  SvelteComponent: Vi,
  append: Cn,
  attr: ee,
  detach: zi,
  init: Xi,
  insert: Wi,
  noop: Ft,
  safe_not_equal: Zi,
  svg_element: Gt
} = window.__gradio__svelte__internal;
function Ji(e) {
  let t, n, r;
  return {
    c() {
      t = Gt("svg"), n = Gt("polyline"), r = Gt("path"), ee(n, "points", "1 4 1 10 7 10"), ee(r, "d", "M3.51 15a9 9 0 1 0 2.13-9.36L1 10"), ee(t, "xmlns", "http://www.w3.org/2000/svg"), ee(t, "width", "100%"), ee(t, "height", "100%"), ee(t, "viewBox", "0 0 24 24"), ee(t, "fill", "none"), ee(t, "stroke", "currentColor"), ee(t, "stroke-width", "2"), ee(t, "stroke-linecap", "round"), ee(t, "stroke-linejoin", "round"), ee(t, "class", "feather feather-rotate-ccw");
    },
    m(i, s) {
      Wi(i, t, s), Cn(t, n), Cn(t, r);
    },
    p: Ft,
    i: Ft,
    o: Ft,
    d(i) {
      i && zi(t);
    }
  };
}
class Qi extends Vi {
  constructor(t) {
    super(), Xi(this, t, null, Ji, Zi, {});
  }
}
const {
  SvelteComponent: Yi,
  append: jt,
  attr: V,
  detach: Ki,
  init: $i,
  insert: es,
  noop: qt,
  safe_not_equal: ts,
  svg_element: gt
} = window.__gradio__svelte__internal;
function ns(e) {
  let t, n, r, i;
  return {
    c() {
      t = gt("svg"), n = gt("path"), r = gt("polyline"), i = gt("line"), V(n, "d", "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"), V(r, "points", "17 8 12 3 7 8"), V(i, "x1", "12"), V(i, "y1", "3"), V(i, "x2", "12"), V(i, "y2", "15"), V(t, "xmlns", "http://www.w3.org/2000/svg"), V(t, "width", "90%"), V(t, "height", "90%"), V(t, "viewBox", "0 0 24 24"), V(t, "fill", "none"), V(t, "stroke", "currentColor"), V(t, "stroke-width", "2"), V(t, "stroke-linecap", "round"), V(t, "stroke-linejoin", "round"), V(t, "class", "feather feather-upload");
    },
    m(s, o) {
      es(s, t, o), jt(t, n), jt(t, r), jt(t, i);
    },
    p: qt,
    i: qt,
    o: qt,
    d(s) {
      s && Ki(t);
    }
  };
}
let rs = class extends Yi {
  constructor(t) {
    super(), $i(this, t, null, ns, ts, {});
  }
};
const {
  SvelteComponent: is,
  append: bt,
  attr: Vt,
  create_component: ss,
  destroy_component: os,
  detach: as,
  element: zt,
  init: ls,
  insert: us,
  mount_component: fs,
  safe_not_equal: cs,
  text: In,
  toggle_class: On,
  transition_in: hs,
  transition_out: ds
} = window.__gradio__svelte__internal;
function _s(e) {
  let t, n, r, i, s, o, a;
  return r = new rs({}), {
    c() {
      t = zt("div"), n = zt("span"), ss(r.$$.fragment), i = In(`
    Drop PDF
    `), s = zt("span"), s.textContent = "- or -", o = In(`
    Click to Upload`), Vt(n, "class", "icon-wrap svelte-kzcjhc"), On(
        n,
        "hovered",
        /*hovered*/
        e[0]
      ), Vt(s, "class", "or svelte-kzcjhc"), Vt(t, "class", "wrap svelte-kzcjhc");
    },
    m(l, u) {
      us(l, t, u), bt(t, n), fs(r, n, null), bt(t, i), bt(t, s), bt(t, o), a = !0;
    },
    p(l, [u]) {
      (!a || u & /*hovered*/
      1) && On(
        n,
        "hovered",
        /*hovered*/
        l[0]
      );
    },
    i(l) {
      a || (hs(r.$$.fragment, l), a = !0);
    },
    o(l) {
      ds(r.$$.fragment, l), a = !1;
    },
    d(l) {
      l && as(t), os(r);
    }
  };
}
function ms(e, t, n) {
  let { hovered: r = !1 } = t;
  return e.$$set = (i) => {
    "hovered" in i && n(0, r = i.hovered);
  }, [r];
}
class ps extends is {
  constructor(t) {
    super(), ls(this, t, ms, _s, cs, { hovered: 0 });
  }
}
const {
  SvelteComponent: gs,
  assign: bs,
  create_slot: vs,
  detach: ys,
  element: ws,
  get_all_dirty_from_scope: Es,
  get_slot_changes: Ss,
  get_spread_update: Ts,
  init: Bs,
  insert: As,
  safe_not_equal: Hs,
  set_dynamic_element_data: Ln,
  set_style: J,
  toggle_class: Te,
  transition_in: Fr,
  transition_out: Gr,
  update_slot_base: Ns
} = window.__gradio__svelte__internal;
function Ps(e) {
  let t, n, r;
  const i = (
    /*#slots*/
    e[17].default
  ), s = vs(
    i,
    e,
    /*$$scope*/
    e[16],
    null
  );
  let o = [
    { "data-testid": (
      /*test_id*/
      e[7]
    ) },
    { id: (
      /*elem_id*/
      e[2]
    ) },
    {
      class: n = "block " + /*elem_classes*/
      e[3].join(" ") + " svelte-1t38q2d"
    }
  ], a = {};
  for (let l = 0; l < o.length; l += 1)
    a = bs(a, o[l]);
  return {
    c() {
      t = ws(
        /*tag*/
        e[14]
      ), s && s.c(), Ln(
        /*tag*/
        e[14]
      )(t, a), Te(
        t,
        "hidden",
        /*visible*/
        e[10] === !1
      ), Te(
        t,
        "padded",
        /*padding*/
        e[6]
      ), Te(
        t,
        "border_focus",
        /*border_mode*/
        e[5] === "focus"
      ), Te(t, "hide-container", !/*explicit_call*/
      e[8] && !/*container*/
      e[9]), J(t, "height", typeof /*height*/
      e[0] == "number" ? (
        /*height*/
        e[0] + "px"
      ) : void 0), J(t, "width", typeof /*width*/
      e[1] == "number" ? `calc(min(${/*width*/
      e[1]}px, 100%))` : void 0), J(
        t,
        "border-style",
        /*variant*/
        e[4]
      ), J(
        t,
        "overflow",
        /*allow_overflow*/
        e[11] ? "visible" : "hidden"
      ), J(
        t,
        "flex-grow",
        /*scale*/
        e[12]
      ), J(t, "min-width", `calc(min(${/*min_width*/
      e[13]}px, 100%))`), J(t, "border-width", "var(--block-border-width)");
    },
    m(l, u) {
      As(l, t, u), s && s.m(t, null), r = !0;
    },
    p(l, u) {
      s && s.p && (!r || u & /*$$scope*/
      65536) && Ns(
        s,
        i,
        l,
        /*$$scope*/
        l[16],
        r ? Ss(
          i,
          /*$$scope*/
          l[16],
          u,
          null
        ) : Es(
          /*$$scope*/
          l[16]
        ),
        null
      ), Ln(
        /*tag*/
        l[14]
      )(t, a = Ts(o, [
        (!r || u & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          l[7]
        ) },
        (!r || u & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          l[2]
        ) },
        (!r || u & /*elem_classes*/
        8 && n !== (n = "block " + /*elem_classes*/
        l[3].join(" ") + " svelte-1t38q2d")) && { class: n }
      ])), Te(
        t,
        "hidden",
        /*visible*/
        l[10] === !1
      ), Te(
        t,
        "padded",
        /*padding*/
        l[6]
      ), Te(
        t,
        "border_focus",
        /*border_mode*/
        l[5] === "focus"
      ), Te(t, "hide-container", !/*explicit_call*/
      l[8] && !/*container*/
      l[9]), u & /*height*/
      1 && J(t, "height", typeof /*height*/
      l[0] == "number" ? (
        /*height*/
        l[0] + "px"
      ) : void 0), u & /*width*/
      2 && J(t, "width", typeof /*width*/
      l[1] == "number" ? `calc(min(${/*width*/
      l[1]}px, 100%))` : void 0), u & /*variant*/
      16 && J(
        t,
        "border-style",
        /*variant*/
        l[4]
      ), u & /*allow_overflow*/
      2048 && J(
        t,
        "overflow",
        /*allow_overflow*/
        l[11] ? "visible" : "hidden"
      ), u & /*scale*/
      4096 && J(
        t,
        "flex-grow",
        /*scale*/
        l[12]
      ), u & /*min_width*/
      8192 && J(t, "min-width", `calc(min(${/*min_width*/
      l[13]}px, 100%))`);
    },
    i(l) {
      r || (Fr(s, l), r = !0);
    },
    o(l) {
      Gr(s, l), r = !1;
    },
    d(l) {
      l && ys(t), s && s.d(l);
    }
  };
}
function xs(e) {
  let t, n = (
    /*tag*/
    e[14] && Ps(e)
  );
  return {
    c() {
      n && n.c();
    },
    m(r, i) {
      n && n.m(r, i), t = !0;
    },
    p(r, [i]) {
      /*tag*/
      r[14] && n.p(r, i);
    },
    i(r) {
      t || (Fr(n, r), t = !0);
    },
    o(r) {
      Gr(n, r), t = !1;
    },
    d(r) {
      n && n.d(r);
    }
  };
}
function Cs(e, t, n) {
  let { $$slots: r = {}, $$scope: i } = t, { height: s = void 0 } = t, { width: o = void 0 } = t, { elem_id: a = "" } = t, { elem_classes: l = [] } = t, { variant: u = "solid" } = t, { border_mode: f = "base" } = t, { padding: h = !0 } = t, { type: c = "normal" } = t, { test_id: d = void 0 } = t, { explicit_call: g = !1 } = t, { container: b = !0 } = t, { visible: w = !0 } = t, { allow_overflow: H = !0 } = t, { scale: S = null } = t, { min_width: m = 0 } = t, _ = c === "fieldset" ? "fieldset" : "div";
  return e.$$set = (E) => {
    "height" in E && n(0, s = E.height), "width" in E && n(1, o = E.width), "elem_id" in E && n(2, a = E.elem_id), "elem_classes" in E && n(3, l = E.elem_classes), "variant" in E && n(4, u = E.variant), "border_mode" in E && n(5, f = E.border_mode), "padding" in E && n(6, h = E.padding), "type" in E && n(15, c = E.type), "test_id" in E && n(7, d = E.test_id), "explicit_call" in E && n(8, g = E.explicit_call), "container" in E && n(9, b = E.container), "visible" in E && n(10, w = E.visible), "allow_overflow" in E && n(11, H = E.allow_overflow), "scale" in E && n(12, S = E.scale), "min_width" in E && n(13, m = E.min_width), "$$scope" in E && n(16, i = E.$$scope);
  }, [
    s,
    o,
    a,
    l,
    u,
    f,
    h,
    d,
    g,
    b,
    w,
    H,
    S,
    m,
    _,
    c,
    i,
    r
  ];
}
class Is extends gs {
  constructor(t) {
    super(), Bs(this, t, Cs, xs, Hs, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 15,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: Os,
  append: Xt,
  attr: vt,
  create_component: Ls,
  destroy_component: ks,
  detach: Ms,
  element: kn,
  init: Rs,
  insert: Ds,
  mount_component: Us,
  safe_not_equal: Fs,
  set_data: Gs,
  space: js,
  text: qs,
  toggle_class: Be,
  transition_in: Vs,
  transition_out: zs
} = window.__gradio__svelte__internal;
function Xs(e) {
  let t, n, r, i, s, o;
  return r = new /*Icon*/
  e[1]({}), {
    c() {
      t = kn("label"), n = kn("span"), Ls(r.$$.fragment), i = js(), s = qs(
        /*label*/
        e[0]
      ), vt(n, "class", "svelte-9gxdi0"), vt(t, "for", ""), vt(t, "data-testid", "block-label"), vt(t, "class", "svelte-9gxdi0"), Be(t, "hide", !/*show_label*/
      e[2]), Be(t, "sr-only", !/*show_label*/
      e[2]), Be(
        t,
        "float",
        /*float*/
        e[4]
      ), Be(
        t,
        "hide-label",
        /*disable*/
        e[3]
      );
    },
    m(a, l) {
      Ds(a, t, l), Xt(t, n), Us(r, n, null), Xt(t, i), Xt(t, s), o = !0;
    },
    p(a, [l]) {
      (!o || l & /*label*/
      1) && Gs(
        s,
        /*label*/
        a[0]
      ), (!o || l & /*show_label*/
      4) && Be(t, "hide", !/*show_label*/
      a[2]), (!o || l & /*show_label*/
      4) && Be(t, "sr-only", !/*show_label*/
      a[2]), (!o || l & /*float*/
      16) && Be(
        t,
        "float",
        /*float*/
        a[4]
      ), (!o || l & /*disable*/
      8) && Be(
        t,
        "hide-label",
        /*disable*/
        a[3]
      );
    },
    i(a) {
      o || (Vs(r.$$.fragment, a), o = !0);
    },
    o(a) {
      zs(r.$$.fragment, a), o = !1;
    },
    d(a) {
      a && Ms(t), ks(r);
    }
  };
}
function Ws(e, t, n) {
  let { label: r = null } = t, { Icon: i } = t, { show_label: s = !0 } = t, { disable: o = !1 } = t, { float: a = !0 } = t;
  return e.$$set = (l) => {
    "label" in l && n(0, r = l.label), "Icon" in l && n(1, i = l.Icon), "show_label" in l && n(2, s = l.show_label), "disable" in l && n(3, o = l.disable), "float" in l && n(4, a = l.float);
  }, [r, i, s, o, a];
}
class Zs extends Os {
  constructor(t) {
    super(), Rs(this, t, Ws, Xs, Fs, {
      label: 0,
      Icon: 1,
      show_label: 2,
      disable: 3,
      float: 4
    });
  }
}
const {
  SvelteComponent: Js,
  append: sn,
  attr: ke,
  bubble: Qs,
  create_component: Ys,
  destroy_component: Ks,
  detach: jr,
  element: on,
  init: $s,
  insert: qr,
  listen: eo,
  mount_component: to,
  safe_not_equal: no,
  set_data: ro,
  space: io,
  text: so,
  toggle_class: Ae,
  transition_in: oo,
  transition_out: ao
} = window.__gradio__svelte__internal;
function Mn(e) {
  let t, n;
  return {
    c() {
      t = on("span"), n = so(
        /*label*/
        e[1]
      ), ke(t, "class", "svelte-xtz2g8");
    },
    m(r, i) {
      qr(r, t, i), sn(t, n);
    },
    p(r, i) {
      i & /*label*/
      2 && ro(
        n,
        /*label*/
        r[1]
      );
    },
    d(r) {
      r && jr(t);
    }
  };
}
function lo(e) {
  let t, n, r, i, s, o, a, l = (
    /*show_label*/
    e[2] && Mn(e)
  );
  return i = new /*Icon*/
  e[0]({}), {
    c() {
      t = on("button"), l && l.c(), n = io(), r = on("div"), Ys(i.$$.fragment), ke(r, "class", "svelte-xtz2g8"), Ae(
        r,
        "small",
        /*size*/
        e[4] === "small"
      ), Ae(
        r,
        "large",
        /*size*/
        e[4] === "large"
      ), ke(
        t,
        "aria-label",
        /*label*/
        e[1]
      ), ke(
        t,
        "title",
        /*label*/
        e[1]
      ), ke(t, "class", "svelte-xtz2g8"), Ae(
        t,
        "pending",
        /*pending*/
        e[3]
      ), Ae(
        t,
        "padded",
        /*padded*/
        e[5]
      );
    },
    m(u, f) {
      qr(u, t, f), l && l.m(t, null), sn(t, n), sn(t, r), to(i, r, null), s = !0, o || (a = eo(
        t,
        "click",
        /*click_handler*/
        e[6]
      ), o = !0);
    },
    p(u, [f]) {
      /*show_label*/
      u[2] ? l ? l.p(u, f) : (l = Mn(u), l.c(), l.m(t, n)) : l && (l.d(1), l = null), (!s || f & /*size*/
      16) && Ae(
        r,
        "small",
        /*size*/
        u[4] === "small"
      ), (!s || f & /*size*/
      16) && Ae(
        r,
        "large",
        /*size*/
        u[4] === "large"
      ), (!s || f & /*label*/
      2) && ke(
        t,
        "aria-label",
        /*label*/
        u[1]
      ), (!s || f & /*label*/
      2) && ke(
        t,
        "title",
        /*label*/
        u[1]
      ), (!s || f & /*pending*/
      8) && Ae(
        t,
        "pending",
        /*pending*/
        u[3]
      ), (!s || f & /*padded*/
      32) && Ae(
        t,
        "padded",
        /*padded*/
        u[5]
      );
    },
    i(u) {
      s || (oo(i.$$.fragment, u), s = !0);
    },
    o(u) {
      ao(i.$$.fragment, u), s = !1;
    },
    d(u) {
      u && jr(t), l && l.d(), Ks(i), o = !1, a();
    }
  };
}
function uo(e, t, n) {
  let { Icon: r } = t, { label: i = "" } = t, { show_label: s = !1 } = t, { pending: o = !1 } = t, { size: a = "small" } = t, { padded: l = !0 } = t;
  function u(f) {
    Qs.call(this, e, f);
  }
  return e.$$set = (f) => {
    "Icon" in f && n(0, r = f.Icon), "label" in f && n(1, i = f.label), "show_label" in f && n(2, s = f.show_label), "pending" in f && n(3, o = f.pending), "size" in f && n(4, a = f.size), "padded" in f && n(5, l = f.padded);
  }, [r, i, s, o, a, l, u];
}
class wn extends Js {
  constructor(t) {
    super(), $s(this, t, uo, lo, no, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5
    });
  }
}
const fo = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Rn = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
fo.reduce(
  (e, { color: t, primary: n, secondary: r }) => ({
    ...e,
    [t]: {
      primary: Rn[t][n],
      secondary: Rn[t][r]
    }
  }),
  {}
);
function qe(e) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], n = 0;
  for (; e > 1e3 && n < t.length - 1; )
    e /= 1e3, n++;
  let r = t[n];
  return (Number.isInteger(e) ? e : e.toFixed(1)) + r;
}
function Ue() {
}
function co(e) {
  return e();
}
function ho(e) {
  e.forEach(co);
}
function _o(e) {
  return typeof e == "function";
}
function mo(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function po(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return Ue;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
const Vr = typeof window < "u";
let Dn = Vr ? () => window.performance.now() : () => Date.now(), zr = Vr ? (e) => requestAnimationFrame(e) : Ue;
const Ve = /* @__PURE__ */ new Set();
function Xr(e) {
  Ve.forEach((t) => {
    t.c(e) || (Ve.delete(t), t.f());
  }), Ve.size !== 0 && zr(Xr);
}
function go(e) {
  let t;
  return Ve.size === 0 && zr(Xr), {
    promise: new Promise((n) => {
      Ve.add(t = { c: e, f: n });
    }),
    abort() {
      Ve.delete(t);
    }
  };
}
const je = [];
function bo(e, t) {
  return {
    subscribe: ht(e, t).subscribe
  };
}
function ht(e, t = Ue) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(a) {
    if (mo(e, a) && (e = a, n)) {
      const l = !je.length;
      for (const u of r)
        u[1](), je.push(u, e);
      if (l) {
        for (let u = 0; u < je.length; u += 2)
          je[u][0](je[u + 1]);
        je.length = 0;
      }
    }
  }
  function s(a) {
    i(a(e));
  }
  function o(a, l = Ue) {
    const u = [a, l];
    return r.add(u), r.size === 1 && (n = t(i, s) || Ue), a(e), () => {
      r.delete(u), r.size === 0 && n && (n(), n = null);
    };
  }
  return { set: i, update: s, subscribe: o };
}
function Ke(e, t, n) {
  const r = !Array.isArray(e), i = r ? [e] : e;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = t.length < 2;
  return bo(n, (o, a) => {
    let l = !1;
    const u = [];
    let f = 0, h = Ue;
    const c = () => {
      if (f)
        return;
      h();
      const g = t(r ? u[0] : u, o, a);
      s ? o(g) : h = _o(g) ? g : Ue;
    }, d = i.map(
      (g, b) => po(
        g,
        (w) => {
          u[b] = w, f &= ~(1 << b), l && c();
        },
        () => {
          f |= 1 << b;
        }
      )
    );
    return l = !0, c(), function() {
      ho(d), h(), l = !1;
    };
  });
}
function Un(e) {
  return Object.prototype.toString.call(e) === "[object Date]";
}
function an(e, t, n, r) {
  if (typeof n == "number" || Un(n)) {
    const i = r - n, s = (n - t) / (e.dt || 1 / 60), o = e.opts.stiffness * i, a = e.opts.damping * s, l = (o - a) * e.inv_mass, u = (s + l) * e.dt;
    return Math.abs(u) < e.opts.precision && Math.abs(i) < e.opts.precision ? r : (e.settled = !1, Un(n) ? new Date(n.getTime() + u) : n + u);
  } else {
    if (Array.isArray(n))
      return n.map(
        (i, s) => an(e, t[s], n[s], r[s])
      );
    if (typeof n == "object") {
      const i = {};
      for (const s in n)
        i[s] = an(e, t[s], n[s], r[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof n} values`);
  }
}
function Fn(e, t = {}) {
  const n = ht(e), { stiffness: r = 0.15, damping: i = 0.8, precision: s = 0.01 } = t;
  let o, a, l, u = e, f = e, h = 1, c = 0, d = !1;
  function g(w, H = {}) {
    f = w;
    const S = l = {};
    return e == null || H.hard || b.stiffness >= 1 && b.damping >= 1 ? (d = !0, o = Dn(), u = w, n.set(e = f), Promise.resolve()) : (H.soft && (c = 1 / ((H.soft === !0 ? 0.5 : +H.soft) * 60), h = 0), a || (o = Dn(), d = !1, a = go((m) => {
      if (d)
        return d = !1, a = null, !1;
      h = Math.min(h + c, 1);
      const _ = {
        inv_mass: h,
        opts: b,
        settled: !0,
        dt: (m - o) * 60 / 1e3
      }, E = an(_, u, e, f);
      return o = m, u = e, n.set(e = E), _.settled && (a = null), !_.settled;
    })), new Promise((m) => {
      a.promise.then(() => {
        S === l && m();
      });
    }));
  }
  const b = {
    set: g,
    update: (w, H) => g(w(f, e), H),
    subscribe: n.subscribe,
    stiffness: r,
    damping: i,
    precision: s
  };
  return b;
}
const {
  SvelteComponent: vo,
  append: le,
  attr: x,
  component_subscribe: Gn,
  detach: yo,
  element: wo,
  init: Eo,
  insert: So,
  noop: jn,
  safe_not_equal: To,
  set_style: yt,
  svg_element: ue,
  toggle_class: qn
} = window.__gradio__svelte__internal, { onMount: Bo } = window.__gradio__svelte__internal;
function Ao(e) {
  let t, n, r, i, s, o, a, l, u, f, h, c;
  return {
    c() {
      t = wo("div"), n = ue("svg"), r = ue("g"), i = ue("path"), s = ue("path"), o = ue("path"), a = ue("path"), l = ue("g"), u = ue("path"), f = ue("path"), h = ue("path"), c = ue("path"), x(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), x(i, "fill", "#FF7C00"), x(i, "fill-opacity", "0.4"), x(i, "class", "svelte-43sxxs"), x(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), x(s, "fill", "#FF7C00"), x(s, "class", "svelte-43sxxs"), x(o, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), x(o, "fill", "#FF7C00"), x(o, "fill-opacity", "0.4"), x(o, "class", "svelte-43sxxs"), x(a, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), x(a, "fill", "#FF7C00"), x(a, "class", "svelte-43sxxs"), yt(r, "transform", "translate(" + /*$top*/
      e[1][0] + "px, " + /*$top*/
      e[1][1] + "px)"), x(u, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), x(u, "fill", "#FF7C00"), x(u, "fill-opacity", "0.4"), x(u, "class", "svelte-43sxxs"), x(f, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), x(f, "fill", "#FF7C00"), x(f, "class", "svelte-43sxxs"), x(h, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), x(h, "fill", "#FF7C00"), x(h, "fill-opacity", "0.4"), x(h, "class", "svelte-43sxxs"), x(c, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), x(c, "fill", "#FF7C00"), x(c, "class", "svelte-43sxxs"), yt(l, "transform", "translate(" + /*$bottom*/
      e[2][0] + "px, " + /*$bottom*/
      e[2][1] + "px)"), x(n, "viewBox", "-1200 -1200 3000 3000"), x(n, "fill", "none"), x(n, "xmlns", "http://www.w3.org/2000/svg"), x(n, "class", "svelte-43sxxs"), x(t, "class", "svelte-43sxxs"), qn(
        t,
        "margin",
        /*margin*/
        e[0]
      );
    },
    m(d, g) {
      So(d, t, g), le(t, n), le(n, r), le(r, i), le(r, s), le(r, o), le(r, a), le(n, l), le(l, u), le(l, f), le(l, h), le(l, c);
    },
    p(d, [g]) {
      g & /*$top*/
      2 && yt(r, "transform", "translate(" + /*$top*/
      d[1][0] + "px, " + /*$top*/
      d[1][1] + "px)"), g & /*$bottom*/
      4 && yt(l, "transform", "translate(" + /*$bottom*/
      d[2][0] + "px, " + /*$bottom*/
      d[2][1] + "px)"), g & /*margin*/
      1 && qn(
        t,
        "margin",
        /*margin*/
        d[0]
      );
    },
    i: jn,
    o: jn,
    d(d) {
      d && yo(t);
    }
  };
}
function Ho(e, t, n) {
  let r, i, { margin: s = !0 } = t;
  const o = Fn([0, 0]);
  Gn(e, o, (c) => n(1, r = c));
  const a = Fn([0, 0]);
  Gn(e, a, (c) => n(2, i = c));
  let l;
  async function u() {
    await Promise.all([o.set([125, 140]), a.set([-125, -140])]), await Promise.all([o.set([-125, 140]), a.set([125, -140])]), await Promise.all([o.set([-125, 0]), a.set([125, -0])]), await Promise.all([o.set([125, 0]), a.set([-125, 0])]);
  }
  async function f() {
    await u(), l || f();
  }
  async function h() {
    await Promise.all([o.set([125, 0]), a.set([-125, 0])]), f();
  }
  return Bo(() => (h(), () => l = !0)), e.$$set = (c) => {
    "margin" in c && n(0, s = c.margin);
  }, [s, r, i, o, a];
}
class No extends vo {
  constructor(t) {
    super(), Eo(this, t, Ho, Ao, To, { margin: 0 });
  }
}
const {
  SvelteComponent: Po,
  append: Re,
  attr: me,
  binding_callbacks: Vn,
  check_outros: Wr,
  create_component: xo,
  create_slot: Co,
  destroy_component: Io,
  destroy_each: Zr,
  detach: T,
  element: ye,
  empty: $e,
  ensure_array_like: Bt,
  get_all_dirty_from_scope: Oo,
  get_slot_changes: Lo,
  group_outros: Jr,
  init: ko,
  insert: B,
  mount_component: Mo,
  noop: ln,
  safe_not_equal: Ro,
  set_data: re,
  set_style: Pe,
  space: pe,
  text: R,
  toggle_class: ne,
  transition_in: Xe,
  transition_out: We,
  update_slot_base: Do
} = window.__gradio__svelte__internal, { tick: Uo } = window.__gradio__svelte__internal, { onDestroy: Fo } = window.__gradio__svelte__internal, Go = (e) => ({}), zn = (e) => ({});
function Xn(e, t, n) {
  const r = e.slice();
  return r[38] = t[n], r[40] = n, r;
}
function Wn(e, t, n) {
  const r = e.slice();
  return r[38] = t[n], r;
}
function jo(e) {
  let t, n = (
    /*i18n*/
    e[1]("common.error") + ""
  ), r, i, s;
  const o = (
    /*#slots*/
    e[29].error
  ), a = Co(
    o,
    e,
    /*$$scope*/
    e[28],
    zn
  );
  return {
    c() {
      t = ye("span"), r = R(n), i = pe(), a && a.c(), me(t, "class", "error svelte-14miwb5");
    },
    m(l, u) {
      B(l, t, u), Re(t, r), B(l, i, u), a && a.m(l, u), s = !0;
    },
    p(l, u) {
      (!s || u[0] & /*i18n*/
      2) && n !== (n = /*i18n*/
      l[1]("common.error") + "") && re(r, n), a && a.p && (!s || u[0] & /*$$scope*/
      268435456) && Do(
        a,
        o,
        l,
        /*$$scope*/
        l[28],
        s ? Lo(
          o,
          /*$$scope*/
          l[28],
          u,
          Go
        ) : Oo(
          /*$$scope*/
          l[28]
        ),
        zn
      );
    },
    i(l) {
      s || (Xe(a, l), s = !0);
    },
    o(l) {
      We(a, l), s = !1;
    },
    d(l) {
      l && (T(t), T(i)), a && a.d(l);
    }
  };
}
function qo(e) {
  let t, n, r, i, s, o, a, l, u, f = (
    /*variant*/
    e[8] === "default" && /*show_eta_bar*/
    e[18] && /*show_progress*/
    e[6] === "full" && Zn(e)
  );
  function h(m, _) {
    if (
      /*progress*/
      m[7]
    )
      return Xo;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    )
      return zo;
    if (
      /*queue_position*/
      m[2] === 0
    )
      return Vo;
  }
  let c = h(e), d = c && c(e), g = (
    /*timer*/
    e[5] && Yn(e)
  );
  const b = [Qo, Jo], w = [];
  function H(m, _) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = H(e)) && (o = w[s] = b[s](e));
  let S = !/*timer*/
  e[5] && ir(e);
  return {
    c() {
      f && f.c(), t = pe(), n = ye("div"), d && d.c(), r = pe(), g && g.c(), i = pe(), o && o.c(), a = pe(), S && S.c(), l = $e(), me(n, "class", "progress-text svelte-14miwb5"), ne(
        n,
        "meta-text-center",
        /*variant*/
        e[8] === "center"
      ), ne(
        n,
        "meta-text",
        /*variant*/
        e[8] === "default"
      );
    },
    m(m, _) {
      f && f.m(m, _), B(m, t, _), B(m, n, _), d && d.m(n, null), Re(n, r), g && g.m(n, null), B(m, i, _), ~s && w[s].m(m, _), B(m, a, _), S && S.m(m, _), B(m, l, _), u = !0;
    },
    p(m, _) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? f ? f.p(m, _) : (f = Zn(m), f.c(), f.m(t.parentNode, t)) : f && (f.d(1), f = null), c === (c = h(m)) && d ? d.p(m, _) : (d && d.d(1), d = c && c(m), d && (d.c(), d.m(n, r))), /*timer*/
      m[5] ? g ? g.p(m, _) : (g = Yn(m), g.c(), g.m(n, null)) : g && (g.d(1), g = null), (!u || _[0] & /*variant*/
      256) && ne(
        n,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!u || _[0] & /*variant*/
      256) && ne(
        n,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let E = s;
      s = H(m), s === E ? ~s && w[s].p(m, _) : (o && (Jr(), We(w[E], 1, 1, () => {
        w[E] = null;
      }), Wr()), ~s ? (o = w[s], o ? o.p(m, _) : (o = w[s] = b[s](m), o.c()), Xe(o, 1), o.m(a.parentNode, a)) : o = null), /*timer*/
      m[5] ? S && (S.d(1), S = null) : S ? S.p(m, _) : (S = ir(m), S.c(), S.m(l.parentNode, l));
    },
    i(m) {
      u || (Xe(o), u = !0);
    },
    o(m) {
      We(o), u = !1;
    },
    d(m) {
      m && (T(t), T(n), T(i), T(a), T(l)), f && f.d(m), d && d.d(), g && g.d(), ~s && w[s].d(m), S && S.d(m);
    }
  };
}
function Zn(e) {
  let t, n = `translateX(${/*eta_level*/
  (e[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = ye("div"), me(t, "class", "eta-bar svelte-14miwb5"), Pe(t, "transform", n);
    },
    m(r, i) {
      B(r, t, i);
    },
    p(r, i) {
      i[0] & /*eta_level*/
      131072 && n !== (n = `translateX(${/*eta_level*/
      (r[17] || 0) * 100 - 100}%)`) && Pe(t, "transform", n);
    },
    d(r) {
      r && T(t);
    }
  };
}
function Vo(e) {
  let t;
  return {
    c() {
      t = R("processing |");
    },
    m(n, r) {
      B(n, t, r);
    },
    p: ln,
    d(n) {
      n && T(t);
    }
  };
}
function zo(e) {
  let t, n = (
    /*queue_position*/
    e[2] + 1 + ""
  ), r, i, s, o;
  return {
    c() {
      t = R("queue: "), r = R(n), i = R("/"), s = R(
        /*queue_size*/
        e[3]
      ), o = R(" |");
    },
    m(a, l) {
      B(a, t, l), B(a, r, l), B(a, i, l), B(a, s, l), B(a, o, l);
    },
    p(a, l) {
      l[0] & /*queue_position*/
      4 && n !== (n = /*queue_position*/
      a[2] + 1 + "") && re(r, n), l[0] & /*queue_size*/
      8 && re(
        s,
        /*queue_size*/
        a[3]
      );
    },
    d(a) {
      a && (T(t), T(r), T(i), T(s), T(o));
    }
  };
}
function Xo(e) {
  let t, n = Bt(
    /*progress*/
    e[7]
  ), r = [];
  for (let i = 0; i < n.length; i += 1)
    r[i] = Qn(Wn(e, n, i));
  return {
    c() {
      for (let i = 0; i < r.length; i += 1)
        r[i].c();
      t = $e();
    },
    m(i, s) {
      for (let o = 0; o < r.length; o += 1)
        r[o] && r[o].m(i, s);
      B(i, t, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        n = Bt(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < n.length; o += 1) {
          const a = Wn(i, n, o);
          r[o] ? r[o].p(a, s) : (r[o] = Qn(a), r[o].c(), r[o].m(t.parentNode, t));
        }
        for (; o < r.length; o += 1)
          r[o].d(1);
        r.length = n.length;
      }
    },
    d(i) {
      i && T(t), Zr(r, i);
    }
  };
}
function Jn(e) {
  let t, n = (
    /*p*/
    e[38].unit + ""
  ), r, i, s = " ", o;
  function a(f, h) {
    return (
      /*p*/
      f[38].length != null ? Zo : Wo
    );
  }
  let l = a(e), u = l(e);
  return {
    c() {
      u.c(), t = pe(), r = R(n), i = R(" | "), o = R(s);
    },
    m(f, h) {
      u.m(f, h), B(f, t, h), B(f, r, h), B(f, i, h), B(f, o, h);
    },
    p(f, h) {
      l === (l = a(f)) && u ? u.p(f, h) : (u.d(1), u = l(f), u && (u.c(), u.m(t.parentNode, t))), h[0] & /*progress*/
      128 && n !== (n = /*p*/
      f[38].unit + "") && re(r, n);
    },
    d(f) {
      f && (T(t), T(r), T(i), T(o)), u.d(f);
    }
  };
}
function Wo(e) {
  let t = qe(
    /*p*/
    e[38].index || 0
  ) + "", n;
  return {
    c() {
      n = R(t);
    },
    m(r, i) {
      B(r, n, i);
    },
    p(r, i) {
      i[0] & /*progress*/
      128 && t !== (t = qe(
        /*p*/
        r[38].index || 0
      ) + "") && re(n, t);
    },
    d(r) {
      r && T(n);
    }
  };
}
function Zo(e) {
  let t = qe(
    /*p*/
    e[38].index || 0
  ) + "", n, r, i = qe(
    /*p*/
    e[38].length
  ) + "", s;
  return {
    c() {
      n = R(t), r = R("/"), s = R(i);
    },
    m(o, a) {
      B(o, n, a), B(o, r, a), B(o, s, a);
    },
    p(o, a) {
      a[0] & /*progress*/
      128 && t !== (t = qe(
        /*p*/
        o[38].index || 0
      ) + "") && re(n, t), a[0] & /*progress*/
      128 && i !== (i = qe(
        /*p*/
        o[38].length
      ) + "") && re(s, i);
    },
    d(o) {
      o && (T(n), T(r), T(s));
    }
  };
}
function Qn(e) {
  let t, n = (
    /*p*/
    e[38].index != null && Jn(e)
  );
  return {
    c() {
      n && n.c(), t = $e();
    },
    m(r, i) {
      n && n.m(r, i), B(r, t, i);
    },
    p(r, i) {
      /*p*/
      r[38].index != null ? n ? n.p(r, i) : (n = Jn(r), n.c(), n.m(t.parentNode, t)) : n && (n.d(1), n = null);
    },
    d(r) {
      r && T(t), n && n.d(r);
    }
  };
}
function Yn(e) {
  let t, n = (
    /*eta*/
    e[0] ? `/${/*formatted_eta*/
    e[19]}` : ""
  ), r, i;
  return {
    c() {
      t = R(
        /*formatted_timer*/
        e[20]
      ), r = R(n), i = R("s");
    },
    m(s, o) {
      B(s, t, o), B(s, r, o), B(s, i, o);
    },
    p(s, o) {
      o[0] & /*formatted_timer*/
      1048576 && re(
        t,
        /*formatted_timer*/
        s[20]
      ), o[0] & /*eta, formatted_eta*/
      524289 && n !== (n = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && re(r, n);
    },
    d(s) {
      s && (T(t), T(r), T(i));
    }
  };
}
function Jo(e) {
  let t, n;
  return t = new No({
    props: { margin: (
      /*variant*/
      e[8] === "default"
    ) }
  }), {
    c() {
      xo(t.$$.fragment);
    },
    m(r, i) {
      Mo(t, r, i), n = !0;
    },
    p(r, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      r[8] === "default"), t.$set(s);
    },
    i(r) {
      n || (Xe(t.$$.fragment, r), n = !0);
    },
    o(r) {
      We(t.$$.fragment, r), n = !1;
    },
    d(r) {
      Io(t, r);
    }
  };
}
function Qo(e) {
  let t, n, r, i, s, o = `${/*last_progress_level*/
  e[15] * 100}%`, a = (
    /*progress*/
    e[7] != null && Kn(e)
  );
  return {
    c() {
      t = ye("div"), n = ye("div"), a && a.c(), r = pe(), i = ye("div"), s = ye("div"), me(n, "class", "progress-level-inner svelte-14miwb5"), me(s, "class", "progress-bar svelte-14miwb5"), Pe(s, "width", o), me(i, "class", "progress-bar-wrap svelte-14miwb5"), me(t, "class", "progress-level svelte-14miwb5");
    },
    m(l, u) {
      B(l, t, u), Re(t, n), a && a.m(n, null), Re(t, r), Re(t, i), Re(i, s), e[30](s);
    },
    p(l, u) {
      /*progress*/
      l[7] != null ? a ? a.p(l, u) : (a = Kn(l), a.c(), a.m(n, null)) : a && (a.d(1), a = null), u[0] & /*last_progress_level*/
      32768 && o !== (o = `${/*last_progress_level*/
      l[15] * 100}%`) && Pe(s, "width", o);
    },
    i: ln,
    o: ln,
    d(l) {
      l && T(t), a && a.d(), e[30](null);
    }
  };
}
function Kn(e) {
  let t, n = Bt(
    /*progress*/
    e[7]
  ), r = [];
  for (let i = 0; i < n.length; i += 1)
    r[i] = rr(Xn(e, n, i));
  return {
    c() {
      for (let i = 0; i < r.length; i += 1)
        r[i].c();
      t = $e();
    },
    m(i, s) {
      for (let o = 0; o < r.length; o += 1)
        r[o] && r[o].m(i, s);
      B(i, t, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        n = Bt(
          /*progress*/
          i[7]
        );
        let o;
        for (o = 0; o < n.length; o += 1) {
          const a = Xn(i, n, o);
          r[o] ? r[o].p(a, s) : (r[o] = rr(a), r[o].c(), r[o].m(t.parentNode, t));
        }
        for (; o < r.length; o += 1)
          r[o].d(1);
        r.length = n.length;
      }
    },
    d(i) {
      i && T(t), Zr(r, i);
    }
  };
}
function $n(e) {
  let t, n, r, i, s = (
    /*i*/
    e[40] !== 0 && Yo()
  ), o = (
    /*p*/
    e[38].desc != null && er(e)
  ), a = (
    /*p*/
    e[38].desc != null && /*progress_level*/
    e[14] && /*progress_level*/
    e[14][
      /*i*/
      e[40]
    ] != null && tr()
  ), l = (
    /*progress_level*/
    e[14] != null && nr(e)
  );
  return {
    c() {
      s && s.c(), t = pe(), o && o.c(), n = pe(), a && a.c(), r = pe(), l && l.c(), i = $e();
    },
    m(u, f) {
      s && s.m(u, f), B(u, t, f), o && o.m(u, f), B(u, n, f), a && a.m(u, f), B(u, r, f), l && l.m(u, f), B(u, i, f);
    },
    p(u, f) {
      /*p*/
      u[38].desc != null ? o ? o.p(u, f) : (o = er(u), o.c(), o.m(n.parentNode, n)) : o && (o.d(1), o = null), /*p*/
      u[38].desc != null && /*progress_level*/
      u[14] && /*progress_level*/
      u[14][
        /*i*/
        u[40]
      ] != null ? a || (a = tr(), a.c(), a.m(r.parentNode, r)) : a && (a.d(1), a = null), /*progress_level*/
      u[14] != null ? l ? l.p(u, f) : (l = nr(u), l.c(), l.m(i.parentNode, i)) : l && (l.d(1), l = null);
    },
    d(u) {
      u && (T(t), T(n), T(r), T(i)), s && s.d(u), o && o.d(u), a && a.d(u), l && l.d(u);
    }
  };
}
function Yo(e) {
  let t;
  return {
    c() {
      t = R(" /");
    },
    m(n, r) {
      B(n, t, r);
    },
    d(n) {
      n && T(t);
    }
  };
}
function er(e) {
  let t = (
    /*p*/
    e[38].desc + ""
  ), n;
  return {
    c() {
      n = R(t);
    },
    m(r, i) {
      B(r, n, i);
    },
    p(r, i) {
      i[0] & /*progress*/
      128 && t !== (t = /*p*/
      r[38].desc + "") && re(n, t);
    },
    d(r) {
      r && T(n);
    }
  };
}
function tr(e) {
  let t;
  return {
    c() {
      t = R("-");
    },
    m(n, r) {
      B(n, t, r);
    },
    d(n) {
      n && T(t);
    }
  };
}
function nr(e) {
  let t = (100 * /*progress_level*/
  (e[14][
    /*i*/
    e[40]
  ] || 0)).toFixed(1) + "", n, r;
  return {
    c() {
      n = R(t), r = R("%");
    },
    m(i, s) {
      B(i, n, s), B(i, r, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && re(n, t);
    },
    d(i) {
      i && (T(n), T(r));
    }
  };
}
function rr(e) {
  let t, n = (
    /*p*/
    (e[38].desc != null || /*progress_level*/
    e[14] && /*progress_level*/
    e[14][
      /*i*/
      e[40]
    ] != null) && $n(e)
  );
  return {
    c() {
      n && n.c(), t = $e();
    },
    m(r, i) {
      n && n.m(r, i), B(r, t, i);
    },
    p(r, i) {
      /*p*/
      r[38].desc != null || /*progress_level*/
      r[14] && /*progress_level*/
      r[14][
        /*i*/
        r[40]
      ] != null ? n ? n.p(r, i) : (n = $n(r), n.c(), n.m(t.parentNode, t)) : n && (n.d(1), n = null);
    },
    d(r) {
      r && T(t), n && n.d(r);
    }
  };
}
function ir(e) {
  let t, n;
  return {
    c() {
      t = ye("p"), n = R(
        /*loading_text*/
        e[9]
      ), me(t, "class", "loading svelte-14miwb5");
    },
    m(r, i) {
      B(r, t, i), Re(t, n);
    },
    p(r, i) {
      i[0] & /*loading_text*/
      512 && re(
        n,
        /*loading_text*/
        r[9]
      );
    },
    d(r) {
      r && T(t);
    }
  };
}
function Ko(e) {
  let t, n, r, i, s;
  const o = [qo, jo], a = [];
  function l(u, f) {
    return (
      /*status*/
      u[4] === "pending" ? 0 : (
        /*status*/
        u[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(n = l(e)) && (r = a[n] = o[n](e)), {
    c() {
      t = ye("div"), r && r.c(), me(t, "class", i = "wrap " + /*variant*/
      e[8] + " " + /*show_progress*/
      e[6] + " svelte-14miwb5"), ne(t, "hide", !/*status*/
      e[4] || /*status*/
      e[4] === "complete" || /*show_progress*/
      e[6] === "hidden"), ne(
        t,
        "translucent",
        /*variant*/
        e[8] === "center" && /*status*/
        (e[4] === "pending" || /*status*/
        e[4] === "error") || /*translucent*/
        e[11] || /*show_progress*/
        e[6] === "minimal"
      ), ne(
        t,
        "generating",
        /*status*/
        e[4] === "generating"
      ), ne(
        t,
        "border",
        /*border*/
        e[12]
      ), Pe(
        t,
        "position",
        /*absolute*/
        e[10] ? "absolute" : "static"
      ), Pe(
        t,
        "padding",
        /*absolute*/
        e[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(u, f) {
      B(u, t, f), ~n && a[n].m(t, null), e[31](t), s = !0;
    },
    p(u, f) {
      let h = n;
      n = l(u), n === h ? ~n && a[n].p(u, f) : (r && (Jr(), We(a[h], 1, 1, () => {
        a[h] = null;
      }), Wr()), ~n ? (r = a[n], r ? r.p(u, f) : (r = a[n] = o[n](u), r.c()), Xe(r, 1), r.m(t, null)) : r = null), (!s || f[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      u[8] + " " + /*show_progress*/
      u[6] + " svelte-14miwb5")) && me(t, "class", i), (!s || f[0] & /*variant, show_progress, status, show_progress*/
      336) && ne(t, "hide", !/*status*/
      u[4] || /*status*/
      u[4] === "complete" || /*show_progress*/
      u[6] === "hidden"), (!s || f[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && ne(
        t,
        "translucent",
        /*variant*/
        u[8] === "center" && /*status*/
        (u[4] === "pending" || /*status*/
        u[4] === "error") || /*translucent*/
        u[11] || /*show_progress*/
        u[6] === "minimal"
      ), (!s || f[0] & /*variant, show_progress, status*/
      336) && ne(
        t,
        "generating",
        /*status*/
        u[4] === "generating"
      ), (!s || f[0] & /*variant, show_progress, border*/
      4416) && ne(
        t,
        "border",
        /*border*/
        u[12]
      ), f[0] & /*absolute*/
      1024 && Pe(
        t,
        "position",
        /*absolute*/
        u[10] ? "absolute" : "static"
      ), f[0] & /*absolute*/
      1024 && Pe(
        t,
        "padding",
        /*absolute*/
        u[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(u) {
      s || (Xe(r), s = !0);
    },
    o(u) {
      We(r), s = !1;
    },
    d(u) {
      u && T(t), ~n && a[n].d(), e[31](null);
    }
  };
}
let wt = [], Wt = !1;
async function $o(e, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (wt.push(e), !Wt)
      Wt = !0;
    else
      return;
    await Uo(), requestAnimationFrame(() => {
      let n = [0, 0];
      for (let r = 0; r < wt.length; r++) {
        const s = wt[r].getBoundingClientRect();
        (r === 0 || s.top + window.scrollY <= n[0]) && (n[0] = s.top + window.scrollY, n[1] = r);
      }
      window.scrollTo({ top: n[0] - 20, behavior: "smooth" }), Wt = !1, wt = [];
    });
  }
}
function ea(e, t, n) {
  let r, { $$slots: i = {}, $$scope: s } = t, { i18n: o } = t, { eta: a = null } = t, { queue: l = !1 } = t, { queue_position: u } = t, { queue_size: f } = t, { status: h } = t, { scroll_to_output: c = !1 } = t, { timer: d = !0 } = t, { show_progress: g = "full" } = t, { message: b = null } = t, { progress: w = null } = t, { variant: H = "default" } = t, { loading_text: S = "Loading..." } = t, { absolute: m = !0 } = t, { translucent: _ = !1 } = t, { border: E = !1 } = t, { autoscroll: X } = t, W, Z = !1, we = 0, ie = 0, Ee = null, Ge = 0, Q = null, A, p = null, k = !0;
  const y = () => {
    n(25, we = performance.now()), n(26, ie = 0), Z = !0, O();
  };
  function O() {
    requestAnimationFrame(() => {
      n(26, ie = (performance.now() - we) / 1e3), Z && O();
    });
  }
  function L() {
    n(26, ie = 0), Z && (Z = !1);
  }
  Fo(() => {
    Z && L();
  });
  let G = null;
  function ce(v) {
    Vn[v ? "unshift" : "push"](() => {
      p = v, n(16, p), n(7, w), n(14, Q), n(15, A);
    });
  }
  function C(v) {
    Vn[v ? "unshift" : "push"](() => {
      W = v, n(13, W);
    });
  }
  return e.$$set = (v) => {
    "i18n" in v && n(1, o = v.i18n), "eta" in v && n(0, a = v.eta), "queue" in v && n(21, l = v.queue), "queue_position" in v && n(2, u = v.queue_position), "queue_size" in v && n(3, f = v.queue_size), "status" in v && n(4, h = v.status), "scroll_to_output" in v && n(22, c = v.scroll_to_output), "timer" in v && n(5, d = v.timer), "show_progress" in v && n(6, g = v.show_progress), "message" in v && n(23, b = v.message), "progress" in v && n(7, w = v.progress), "variant" in v && n(8, H = v.variant), "loading_text" in v && n(9, S = v.loading_text), "absolute" in v && n(10, m = v.absolute), "translucent" in v && n(11, _ = v.translucent), "border" in v && n(12, E = v.border), "autoscroll" in v && n(24, X = v.autoscroll), "$$scope" in v && n(28, s = v.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty[0] & /*eta, old_eta, queue, timer_start*/
    169869313 && (a === null ? n(0, a = Ee) : l && n(0, a = (performance.now() - we) / 1e3 + a), a != null && (n(19, G = a.toFixed(1)), n(27, Ee = a))), e.$$.dirty[0] & /*eta, timer_diff*/
    67108865 && n(17, Ge = a === null || a <= 0 || !ie ? null : Math.min(ie / a, 1)), e.$$.dirty[0] & /*progress*/
    128 && w != null && n(18, k = !1), e.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (w != null ? n(14, Q = w.map((v) => {
      if (v.index != null && v.length != null)
        return v.index / v.length;
      if (v.progress != null)
        return v.progress;
    })) : n(14, Q = null), Q ? (n(15, A = Q[Q.length - 1]), p && (A === 0 ? n(16, p.style.transition = "0", p) : n(16, p.style.transition = "150ms", p))) : n(15, A = void 0)), e.$$.dirty[0] & /*status*/
    16 && (h === "pending" ? y() : L()), e.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && W && c && (h === "pending" || h === "complete") && $o(W, X), e.$$.dirty[0] & /*status, message*/
    8388624, e.$$.dirty[0] & /*timer_diff*/
    67108864 && n(20, r = ie.toFixed(1));
  }, [
    a,
    o,
    u,
    f,
    h,
    d,
    g,
    w,
    H,
    S,
    m,
    _,
    E,
    W,
    Q,
    A,
    p,
    Ge,
    k,
    G,
    r,
    l,
    c,
    b,
    X,
    we,
    ie,
    Ee,
    s,
    i,
    ce,
    C
  ];
}
class ta extends Po {
  constructor(t) {
    super(), ko(
      this,
      t,
      ea,
      Ko,
      Ro,
      {
        i18n: 1,
        eta: 0,
        queue: 21,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
var Zt = new Intl.Collator(0, { numeric: 1 }).compare;
function sr(e, t, n) {
  return e = e.split("."), t = t.split("."), Zt(e[0], t[0]) || Zt(e[1], t[1]) || (t[2] = t.slice(2).join("."), n = /[.-]/.test(e[2] = e.slice(2).join(".")), n == /[.-]/.test(t[2]) ? Zt(e[2], t[2]) : n ? -1 : 1);
}
function Ne(e, t, n) {
  return t.startsWith("http://") || t.startsWith("https://") ? n ? e : t : e + t;
}
function Jt(e) {
  if (e.startsWith("http")) {
    const { protocol: t, host: n } = new URL(e);
    return n.endsWith("hf.space") ? {
      ws_protocol: "wss",
      host: n,
      http_protocol: t
    } : {
      ws_protocol: t === "https:" ? "wss" : "ws",
      http_protocol: t,
      host: n
    };
  } else if (e.startsWith("file:"))
    return {
      ws_protocol: "ws",
      http_protocol: "http:",
      host: "lite.local"
      // Special fake hostname only used for this case. This matches the hostname allowed in `is_self_host()` in `js/wasm/network/host.ts`.
    };
  return {
    ws_protocol: "wss",
    http_protocol: "https:",
    host: e
  };
}
const Qr = /^[^\/]*\/[^\/]*$/, na = /.*hf\.space\/{0,1}$/;
async function ra(e, t) {
  const n = {};
  t && (n.Authorization = `Bearer ${t}`);
  const r = e.trim();
  if (Qr.test(r))
    try {
      const i = await fetch(
        `https://huggingface.co/api/spaces/${r}/host`,
        { headers: n }
      );
      if (i.status !== 200)
        throw new Error("Space metadata could not be loaded.");
      const s = (await i.json()).host;
      return {
        space_id: e,
        ...Jt(s)
      };
    } catch (i) {
      throw new Error("Space metadata could not be loaded." + i.message);
    }
  if (na.test(r)) {
    const { ws_protocol: i, http_protocol: s, host: o } = Jt(r);
    return {
      space_id: o.replace(".hf.space", ""),
      ws_protocol: i,
      http_protocol: s,
      host: o
    };
  }
  return {
    space_id: !1,
    ...Jt(r)
  };
}
function ia(e) {
  let t = {};
  return e.forEach(({ api_name: n }, r) => {
    n && (t[n] = r);
  }), t;
}
const sa = /^(?=[^]*\b[dD]iscussions{0,1}\b)(?=[^]*\b[dD]isabled\b)[^]*$/;
async function or(e) {
  try {
    const n = (await fetch(
      `https://huggingface.co/api/spaces/${e}/discussions`,
      {
        method: "HEAD"
      }
    )).headers.get("x-error-message");
    return !(n && sa.test(n));
  } catch {
    return !1;
  }
}
function De(e, t, n) {
  if (e == null)
    return null;
  if (Array.isArray(e)) {
    const r = [];
    for (const i of e)
      i == null ? r.push(null) : r.push(De(i, t, n));
    return r;
  }
  return e.is_stream ? n == null ? new ze({
    ...e,
    url: t + "/stream/" + e.path
  }) : new ze({
    ...e,
    url: "/proxy=" + n + "stream/" + e.path
  }) : new ze({
    ...e,
    url: aa(e.path, t, n)
  });
}
function oa(e) {
  try {
    const t = new URL(e);
    return t.protocol === "http:" || t.protocol === "https:";
  } catch {
    return !1;
  }
}
function aa(e, t, n) {
  return e == null ? n ? `/proxy=${n}file=` : `${t}/file=` : oa(e) ? e : n ? `/proxy=${n}file=${e}` : `${t}/file=${e}`;
}
async function la(e, t, n = ha) {
  let r = (Array.isArray(e) ? e : [e]).map(
    (i) => i.blob
  );
  return await Promise.all(
    await n(t, r).then(
      async (i) => {
        if (i.error)
          throw new Error(i.error);
        return i.files ? i.files.map((s, o) => {
          const a = new ze({ ...e[o], path: s });
          return De(a, t, null);
        }) : [];
      }
    )
  );
}
async function ua(e, t) {
  return e.map(
    (n, r) => new ze({
      path: n.name,
      orig_name: n.name,
      blob: n,
      size: n.size,
      mime_type: n.type,
      is_stream: t
    })
  );
}
class ze {
  constructor({
    path: t,
    url: n,
    orig_name: r,
    size: i,
    blob: s,
    is_stream: o,
    mime_type: a,
    alt_text: l
  }) {
    this.path = t, this.url = n, this.orig_name = r, this.size = i, this.blob = n ? void 0 : s, this.is_stream = o, this.mime_type = a, this.alt_text = l;
  }
}
const fa = "This application is too busy. Keep trying!", ot = "Connection errored out.";
let Yr;
function ca(e, t) {
  return { post_data: n, upload_files: r, client: i, handle_blob: s };
  async function n(o, a, l) {
    const u = { "Content-Type": "application/json" };
    l && (u.Authorization = `Bearer ${l}`);
    try {
      var f = await e(o, {
        method: "POST",
        body: JSON.stringify(a),
        headers: u
      });
    } catch {
      return [{ error: ot }, 500];
    }
    return [await f.json(), f.status];
  }
  async function r(o, a, l) {
    const u = {};
    l && (u.Authorization = `Bearer ${l}`);
    const f = 1e3, h = [];
    for (let d = 0; d < a.length; d += f) {
      const g = a.slice(d, d + f), b = new FormData();
      g.forEach((H) => {
        b.append("files", H);
      });
      try {
        var c = await e(`${o}/upload`, {
          method: "POST",
          body: b,
          headers: u
        });
      } catch {
        return { error: ot };
      }
      const w = await c.json();
      h.push(...w);
    }
    return { files: h };
  }
  async function i(o, a = { normalise_files: !0 }) {
    return new Promise(async (l) => {
      const { status_callback: u, hf_token: f, normalise_files: h } = a, c = {
        predict: ie,
        submit: Ee,
        view_api: Q,
        component_server: Ge
      }, d = h ?? !0;
      if ((typeof window > "u" || !("WebSocket" in window)) && !global.Websocket) {
        const A = await import("./wrapper-98f94c21-f7f71f53.js");
        Yr = (await import("./__vite-browser-external-2447137e.js")).Blob, global.WebSocket = A.WebSocket;
      }
      const { ws_protocol: g, http_protocol: b, host: w, space_id: H } = await ra(o, f), S = Math.random().toString(36).substring(2), m = {};
      let _, E = {}, X = !1;
      f && H && (X = await _a(H, f));
      async function W(A) {
        if (_ = A, E = ia((A == null ? void 0 : A.dependencies) || []), _.auth_required)
          return {
            config: _,
            ...c
          };
        try {
          Z = await Q(_);
        } catch (p) {
          console.error(`Could not get api details: ${p.message}`);
        }
        return {
          config: _,
          ...c
        };
      }
      let Z;
      async function we(A) {
        if (u && u(A), A.status === "running")
          try {
            _ = await fr(
              e,
              `${b}//${w}`,
              f
            );
            const p = await W(_);
            l(p);
          } catch (p) {
            console.error(p), u && u({
              status: "error",
              message: "Could not load this space.",
              load_status: "error",
              detail: "NOT_FOUND"
            });
          }
      }
      try {
        _ = await fr(
          e,
          `${b}//${w}`,
          f
        );
        const A = await W(_);
        l(A);
      } catch (A) {
        console.error(A), H ? fn(
          H,
          Qr.test(H) ? "space_name" : "subdomain",
          we
        ) : u && u({
          status: "error",
          message: "Could not load this space.",
          load_status: "error",
          detail: "NOT_FOUND"
        });
      }
      function ie(A, p, k) {
        let y = !1, O = !1, L;
        if (typeof A == "number")
          L = _.dependencies[A];
        else {
          const G = A.replace(/^\//, "");
          L = _.dependencies[E[G]];
        }
        if (L.types.continuous)
          throw new Error(
            "Cannot call predict on this function as it may run forever. Use submit instead"
          );
        return new Promise((G, ce) => {
          const C = Ee(A, p, k);
          let v;
          C.on("data", (he) => {
            O && (C.destroy(), G(he)), y = !0, v = he;
          }).on("status", (he) => {
            he.stage === "error" && ce(he), he.stage === "complete" && (O = !0, y && (C.destroy(), G(v)));
          });
        });
      }
      function Ee(A, p, k) {
        let y, O;
        if (typeof A == "number")
          y = A, O = Z.unnamed_endpoints[y];
        else {
          const j = A.replace(/^\//, "");
          y = E[j], O = Z.named_endpoints[A.trim()];
        }
        if (typeof y != "number")
          throw new Error(
            "There is no endpoint matching that name of fn_index matching that number."
          );
        let L, G, ce = _.protocol ?? "sse";
        const C = typeof A == "number" ? "/predict" : A;
        let v, he = null, ge = !1;
        const it = {};
        let st = "";
        typeof window < "u" && (st = new URLSearchParams(window.location.search).toString()), s(
          `${b}//${Ne(w, _.path, !0)}`,
          p,
          O,
          f
        ).then((j) => {
          if (v = { data: j || [], event_data: k, fn_index: y }, ma(y, _))
            U({
              type: "status",
              endpoint: C,
              stage: "pending",
              queue: !1,
              fn_index: y,
              time: /* @__PURE__ */ new Date()
            }), n(
              `${b}//${Ne(w, _.path, !0)}/run${C.startsWith("/") ? C : `/${C}`}${st ? "?" + st : ""}`,
              {
                ...v,
                session_hash: S
              },
              f
            ).then(([D, q]) => {
              const Se = d ? Qt(
                D.data,
                O,
                _.root,
                _.root_url
              ) : D.data;
              q == 200 ? (U({
                type: "data",
                endpoint: C,
                fn_index: y,
                data: Se,
                time: /* @__PURE__ */ new Date()
              }), U({
                type: "status",
                endpoint: C,
                fn_index: y,
                stage: "complete",
                eta: D.average_duration,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              })) : U({
                type: "status",
                stage: "error",
                endpoint: C,
                fn_index: y,
                message: D.error,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              });
            }).catch((D) => {
              U({
                type: "status",
                stage: "error",
                message: D.message,
                endpoint: C,
                fn_index: y,
                queue: !1,
                time: /* @__PURE__ */ new Date()
              });
            });
          else if (ce == "ws") {
            U({
              type: "status",
              stage: "pending",
              queue: !0,
              endpoint: C,
              fn_index: y,
              time: /* @__PURE__ */ new Date()
            });
            let D = new URL(`${g}://${Ne(
              w,
              _.path,
              !0
            )}
							/queue/join${st ? "?" + st : ""}`);
            X && D.searchParams.set("__sign", X), L = t(D), L.onclose = (q) => {
              q.wasClean || U({
                type: "status",
                stage: "error",
                broken: !0,
                message: ot,
                queue: !0,
                endpoint: C,
                fn_index: y,
                time: /* @__PURE__ */ new Date()
              });
            }, L.onmessage = function(q) {
              const Se = JSON.parse(q.data), { type: K, status: F, data: se } = cr(
                Se,
                m[y]
              );
              if (K === "update" && F && !ge)
                U({
                  type: "status",
                  endpoint: C,
                  fn_index: y,
                  time: /* @__PURE__ */ new Date(),
                  ...F
                }), F.stage === "error" && L.close();
              else if (K === "hash") {
                L.send(JSON.stringify({ fn_index: y, session_hash: S }));
                return;
              } else
                K === "data" ? L.send(JSON.stringify({ ...v, session_hash: S })) : K === "complete" ? ge = F : K === "log" ? U({
                  type: "log",
                  log: se.log,
                  level: se.level,
                  endpoint: C,
                  fn_index: y
                }) : K === "generating" && U({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...F,
                  stage: F == null ? void 0 : F.stage,
                  queue: !0,
                  endpoint: C,
                  fn_index: y
                });
              se && (U({
                type: "data",
                time: /* @__PURE__ */ new Date(),
                data: d ? Qt(
                  se.data,
                  O,
                  _.root,
                  _.root_url
                ) : se.data,
                endpoint: C,
                fn_index: y
              }), ge && (U({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...ge,
                stage: F == null ? void 0 : F.stage,
                queue: !0,
                endpoint: C,
                fn_index: y
              }), L.close()));
            }, sr(_.version || "2.0.0", "3.6") < 0 && addEventListener(
              "open",
              () => L.send(JSON.stringify({ hash: S }))
            );
          } else {
            U({
              type: "status",
              stage: "pending",
              queue: !0,
              endpoint: C,
              fn_index: y,
              time: /* @__PURE__ */ new Date()
            });
            var Y = new URLSearchParams({
              fn_index: y.toString(),
              session_hash: S
            }).toString();
            let D = new URL(
              `${b}//${Ne(
                w,
                _.path,
                !0
              )}/queue/join?${Y}`
            );
            G = new EventSource(D), G.onmessage = async function(q) {
              const Se = JSON.parse(q.data), { type: K, status: F, data: se } = cr(
                Se,
                m[y]
              );
              if (K === "update" && F && !ge)
                U({
                  type: "status",
                  endpoint: C,
                  fn_index: y,
                  time: /* @__PURE__ */ new Date(),
                  ...F
                }), F.stage === "error" && G.close();
              else if (K === "data") {
                he = Se.event_id;
                let [Wu, wi] = await n(
                  `${b}//${Ne(
                    w,
                    _.path,
                    !0
                  )}/queue/data`,
                  {
                    ...v,
                    session_hash: S,
                    event_id: he
                  },
                  f
                );
                wi !== 200 && (U({
                  type: "status",
                  stage: "error",
                  message: ot,
                  queue: !0,
                  endpoint: C,
                  fn_index: y,
                  time: /* @__PURE__ */ new Date()
                }), G.close());
              } else
                K === "complete" ? ge = F : K === "log" ? U({
                  type: "log",
                  log: se.log,
                  level: se.level,
                  endpoint: C,
                  fn_index: y
                }) : K === "generating" && U({
                  type: "status",
                  time: /* @__PURE__ */ new Date(),
                  ...F,
                  stage: F == null ? void 0 : F.stage,
                  queue: !0,
                  endpoint: C,
                  fn_index: y
                });
              se && (U({
                type: "data",
                time: /* @__PURE__ */ new Date(),
                data: d ? Qt(
                  se.data,
                  O,
                  _.root,
                  _.root_url
                ) : se.data,
                endpoint: C,
                fn_index: y
              }), ge && (U({
                type: "status",
                time: /* @__PURE__ */ new Date(),
                ...ge,
                stage: F == null ? void 0 : F.stage,
                queue: !0,
                endpoint: C,
                fn_index: y
              }), G.close()));
            };
          }
        });
        function U(j) {
          const D = it[j.type] || [];
          D == null || D.forEach((q) => q(j));
        }
        function It(j, Y) {
          const D = it, q = D[j] || [];
          return D[j] = q, q == null || q.push(Y), { on: It, off: mt, cancel: Ot, destroy: Lt };
        }
        function mt(j, Y) {
          const D = it;
          let q = D[j] || [];
          return q = q == null ? void 0 : q.filter((Se) => Se !== Y), D[j] = q, { on: It, off: mt, cancel: Ot, destroy: Lt };
        }
        async function Ot() {
          const j = {
            stage: "complete",
            queue: !1,
            time: /* @__PURE__ */ new Date()
          };
          ge = j, U({
            ...j,
            type: "status",
            endpoint: C,
            fn_index: y
          });
          let Y = {};
          ce === "ws" ? (L && L.readyState === 0 ? L.addEventListener("open", () => {
            L.close();
          }) : L.close(), Y = { fn_index: y, session_hash: S }) : (G.close(), Y = { event_id: he });
          try {
            await e(
              `${b}//${Ne(
                w,
                _.path,
                !0
              )}/reset`,
              {
                headers: { "Content-Type": "application/json" },
                method: "POST",
                body: JSON.stringify(Y)
              }
            );
          } catch {
            console.warn(
              "The `/reset` endpoint could not be called. Subsequent endpoint results may be unreliable."
            );
          }
        }
        function Lt() {
          for (const j in it)
            it[j].forEach((Y) => {
              mt(j, Y);
            });
        }
        return {
          on: It,
          off: mt,
          cancel: Ot,
          destroy: Lt
        };
      }
      async function Ge(A, p, k) {
        var y;
        const O = { "Content-Type": "application/json" };
        f && (O.Authorization = `Bearer ${f}`);
        let L, G = _.components.find(
          (v) => v.id === A
        );
        (y = G == null ? void 0 : G.props) != null && y.root_url ? L = G.props.root_url : L = `${b}//${Ne(
          w,
          _.path,
          !0
        )}/`;
        const ce = await e(
          `${L}component_server/`,
          {
            method: "POST",
            body: JSON.stringify({
              data: k,
              component_id: A,
              fn_name: p,
              session_hash: S
            }),
            headers: O
          }
        );
        if (!ce.ok)
          throw new Error(
            "Could not connect to component server: " + ce.statusText
          );
        return await ce.json();
      }
      async function Q(A) {
        if (Z)
          return Z;
        const p = { "Content-Type": "application/json" };
        f && (p.Authorization = `Bearer ${f}`);
        let k;
        if (sr(A.version || "2.0.0", "3.30") < 0 ? k = await e(
          "https://gradio-space-api-fetcher-v2.hf.space/api",
          {
            method: "POST",
            body: JSON.stringify({
              serialize: !1,
              config: JSON.stringify(A)
            }),
            headers: p
          }
        ) : k = await e(`${A.root}/info`, {
          headers: p
        }), !k.ok)
          throw new Error(ot);
        let y = await k.json();
        return "api" in y && (y = y.api), y.named_endpoints["/predict"] && !y.unnamed_endpoints[0] && (y.unnamed_endpoints[0] = y.named_endpoints["/predict"]), da(y, A, E);
      }
    });
  }
  async function s(o, a, l, u) {
    const f = await un(
      a,
      void 0,
      [],
      !0,
      l
    );
    return Promise.all(
      f.map(async ({ path: h, blob: c, type: d }) => {
        if (c) {
          const g = (await r(o, [c], u)).files[0];
          return { path: h, file_url: g, type: d, name: c == null ? void 0 : c.name };
        }
        return { path: h, type: d };
      })
    ).then((h) => (h.forEach(({ path: c, file_url: d, type: g, name: b }) => {
      if (g === "Gallery")
        ur(a, d, c);
      else if (d) {
        const w = new ze({ path: d, orig_name: b });
        ur(a, w, c);
      }
    }), a));
  }
}
const { post_data: Qu, upload_files: ha, client: Yu, handle_blob: Ku } = ca(
  fetch,
  (...e) => new WebSocket(...e)
);
function Qt(e, t, n, r) {
  return e.map((i, s) => {
    var o, a, l, u;
    return ((a = (o = t == null ? void 0 : t.returns) == null ? void 0 : o[s]) == null ? void 0 : a.component) === "File" ? De(i, n, r) : ((u = (l = t == null ? void 0 : t.returns) == null ? void 0 : l[s]) == null ? void 0 : u.component) === "Gallery" ? i.map((f) => Array.isArray(f) ? [De(f[0], n, r), f[1]] : [De(f, n, r), null]) : typeof i == "object" && i.path ? De(i, n, r) : i;
  });
}
function ar(e, t, n, r) {
  switch (e.type) {
    case "string":
      return "string";
    case "boolean":
      return "boolean";
    case "number":
      return "number";
  }
  if (n === "JSONSerializable" || n === "StringSerializable")
    return "any";
  if (n === "ListStringSerializable")
    return "string[]";
  if (t === "Image")
    return r === "parameter" ? "Blob | File | Buffer" : "string";
  if (n === "FileSerializable")
    return (e == null ? void 0 : e.type) === "array" ? r === "parameter" ? "(Blob | File | Buffer)[]" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}[]" : r === "parameter" ? "Blob | File | Buffer" : "{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}";
  if (n === "GallerySerializable")
    return r === "parameter" ? "[(Blob | File | Buffer), (string | null)][]" : "[{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}, (string | null))][]";
}
function lr(e, t) {
  return t === "GallerySerializable" ? "array of [file, label] tuples" : t === "ListStringSerializable" ? "array of strings" : t === "FileSerializable" ? "array of files or single file" : e.description;
}
function da(e, t, n) {
  const r = {
    named_endpoints: {},
    unnamed_endpoints: {}
  };
  for (const i in e) {
    const s = e[i];
    for (const o in s) {
      const a = t.dependencies[o] ? o : n[o.replace("/", "")], l = s[o];
      r[i][o] = {}, r[i][o].parameters = {}, r[i][o].returns = {}, r[i][o].type = t.dependencies[a].types, r[i][o].parameters = l.parameters.map(
        ({ label: u, component: f, type: h, serializer: c }) => ({
          label: u,
          component: f,
          type: ar(h, f, c, "parameter"),
          description: lr(h, c)
        })
      ), r[i][o].returns = l.returns.map(
        ({ label: u, component: f, type: h, serializer: c }) => ({
          label: u,
          component: f,
          type: ar(h, f, c, "return"),
          description: lr(h, c)
        })
      );
    }
  }
  return r;
}
async function _a(e, t) {
  try {
    return (await (await fetch(`https://huggingface.co/api/spaces/${e}/jwt`, {
      headers: {
        Authorization: `Bearer ${t}`
      }
    })).json()).token || !1;
  } catch (n) {
    return console.error(n), !1;
  }
}
function ur(e, t, n) {
  for (; n.length > 1; )
    e = e[n.shift()];
  e[n.shift()] = t;
}
async function un(e, t = void 0, n = [], r = !1, i = void 0) {
  if (Array.isArray(e)) {
    let s = [];
    return await Promise.all(
      e.map(async (o, a) => {
        var l;
        let u = n.slice();
        u.push(a);
        const f = await un(
          e[a],
          r ? ((l = i == null ? void 0 : i.parameters[a]) == null ? void 0 : l.component) || void 0 : t,
          u,
          !1,
          i
        );
        s = s.concat(f);
      })
    ), s;
  } else {
    if (globalThis.Buffer && e instanceof globalThis.Buffer)
      return [
        {
          path: n,
          blob: t === "Image" ? !1 : new Yr([e]),
          type: t
        }
      ];
    if (typeof e == "object") {
      let s = [];
      for (let o in e)
        if (e.hasOwnProperty(o)) {
          let a = n.slice();
          a.push(o), s = s.concat(
            await un(
              e[o],
              void 0,
              a,
              !1,
              i
            )
          );
        }
      return s;
    }
  }
  return [];
}
function ma(e, t) {
  var n, r, i, s;
  return !(((r = (n = t == null ? void 0 : t.dependencies) == null ? void 0 : n[e]) == null ? void 0 : r.queue) === null ? t.enable_queue : (s = (i = t == null ? void 0 : t.dependencies) == null ? void 0 : i[e]) != null && s.queue) || !1;
}
async function fr(e, t, n) {
  const r = {};
  if (n && (r.Authorization = `Bearer ${n}`), typeof window < "u" && window.gradio_config && location.origin !== "http://localhost:9876" && !window.gradio_config.dev_mode) {
    const i = window.gradio_config.root, s = window.gradio_config;
    return s.root = Ne(t, s.root, !1), { ...s, path: i };
  } else if (t) {
    let i = await e(`${t}/config`, {
      headers: r
    });
    if (i.status === 200) {
      const s = await i.json();
      return s.path = s.path ?? "", s.root = t, s;
    }
    throw new Error("Could not get config.");
  }
  throw new Error("No config or app endpoint found");
}
async function fn(e, t, n) {
  let r = t === "subdomain" ? `https://huggingface.co/api/spaces/by-subdomain/${e}` : `https://huggingface.co/api/spaces/${e}`, i, s;
  try {
    if (i = await fetch(r), s = i.status, s !== 200)
      throw new Error();
    i = await i.json();
  } catch {
    n({
      status: "error",
      load_status: "error",
      message: "Could not get space status",
      detail: "NOT_FOUND"
    });
    return;
  }
  if (!i || s !== 200)
    return;
  const {
    runtime: { stage: o },
    id: a
  } = i;
  switch (o) {
    case "STOPPED":
    case "SLEEPING":
      n({
        status: "sleeping",
        load_status: "pending",
        message: "Space is asleep. Waking it up...",
        detail: o
      }), setTimeout(() => {
        fn(e, t, n);
      }, 1e3);
      break;
    case "PAUSED":
      n({
        status: "paused",
        load_status: "error",
        message: "This space has been paused by the author. If you would like to try this demo, consider duplicating the space.",
        detail: o,
        discussions_enabled: await or(a)
      });
      break;
    case "RUNNING":
    case "RUNNING_BUILDING":
      n({
        status: "running",
        load_status: "complete",
        message: "",
        detail: o
      });
      break;
    case "BUILDING":
      n({
        status: "building",
        load_status: "pending",
        message: "Space is building...",
        detail: o
      }), setTimeout(() => {
        fn(e, t, n);
      }, 1e3);
      break;
    default:
      n({
        status: "space_error",
        load_status: "error",
        message: "This space is experiencing an issue.",
        detail: o,
        discussions_enabled: await or(a)
      });
      break;
  }
}
function cr(e, t) {
  switch (e.msg) {
    case "send_data":
      return { type: "data" };
    case "send_hash":
      return { type: "hash" };
    case "queue_full":
      return {
        type: "update",
        status: {
          queue: !0,
          message: fa,
          stage: "error",
          code: e.code,
          success: e.success
        }
      };
    case "estimation":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: t || "pending",
          code: e.code,
          size: e.queue_size,
          position: e.rank,
          eta: e.rank_eta,
          success: e.success
        }
      };
    case "progress":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: e.code,
          progress_data: e.progress_data,
          success: e.success
        }
      };
    case "log":
      return { type: "log", data: e };
    case "process_generating":
      return {
        type: "generating",
        status: {
          queue: !0,
          message: e.success ? null : e.output.error,
          stage: e.success ? "generating" : "error",
          code: e.code,
          progress_data: e.progress_data,
          eta: e.average_duration
        },
        data: e.success ? e.output : null
      };
    case "process_completed":
      return "error" in e.output ? {
        type: "update",
        status: {
          queue: !0,
          message: e.output.error,
          stage: "error",
          code: e.code,
          success: e.success
        }
      } : {
        type: "complete",
        status: {
          queue: !0,
          message: e.success ? void 0 : e.output.error,
          stage: e.success ? "complete" : "error",
          code: e.code,
          progress_data: e.progress_data,
          eta: e.output.average_duration
        },
        data: e.success ? e.output : null
      };
    case "process_starts":
      return {
        type: "update",
        status: {
          queue: !0,
          stage: "pending",
          code: e.code,
          size: e.rank,
          position: 0,
          success: e.success
        }
      };
  }
  return { type: "none", status: { stage: "error", queue: !0 } };
}
function pa(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var ga = function(t) {
  return ba(t) && !va(t);
};
function ba(e) {
  return !!e && typeof e == "object";
}
function va(e) {
  var t = Object.prototype.toString.call(e);
  return t === "[object RegExp]" || t === "[object Date]" || Ea(e);
}
var ya = typeof Symbol == "function" && Symbol.for, wa = ya ? Symbol.for("react.element") : 60103;
function Ea(e) {
  return e.$$typeof === wa;
}
function Sa(e) {
  return Array.isArray(e) ? [] : {};
}
function ft(e, t) {
  return t.clone !== !1 && t.isMergeableObject(e) ? Ze(Sa(e), e, t) : e;
}
function Ta(e, t, n) {
  return e.concat(t).map(function(r) {
    return ft(r, n);
  });
}
function Ba(e, t) {
  if (!t.customMerge)
    return Ze;
  var n = t.customMerge(e);
  return typeof n == "function" ? n : Ze;
}
function Aa(e) {
  return Object.getOwnPropertySymbols ? Object.getOwnPropertySymbols(e).filter(function(t) {
    return Object.propertyIsEnumerable.call(e, t);
  }) : [];
}
function hr(e) {
  return Object.keys(e).concat(Aa(e));
}
function Kr(e, t) {
  try {
    return t in e;
  } catch {
    return !1;
  }
}
function Ha(e, t) {
  return Kr(e, t) && !(Object.hasOwnProperty.call(e, t) && Object.propertyIsEnumerable.call(e, t));
}
function Na(e, t, n) {
  var r = {};
  return n.isMergeableObject(e) && hr(e).forEach(function(i) {
    r[i] = ft(e[i], n);
  }), hr(t).forEach(function(i) {
    Ha(e, i) || (Kr(e, i) && n.isMergeableObject(t[i]) ? r[i] = Ba(i, n)(e[i], t[i], n) : r[i] = ft(t[i], n));
  }), r;
}
function Ze(e, t, n) {
  n = n || {}, n.arrayMerge = n.arrayMerge || Ta, n.isMergeableObject = n.isMergeableObject || ga, n.cloneUnlessOtherwiseSpecified = ft;
  var r = Array.isArray(t), i = Array.isArray(e), s = r === i;
  return s ? r ? n.arrayMerge(e, t, n) : Na(e, t, n) : ft(t, n);
}
Ze.all = function(t, n) {
  if (!Array.isArray(t))
    throw new Error("first argument should be an array");
  return t.reduce(function(r, i) {
    return Ze(r, i, n);
  }, {});
};
var Pa = Ze, xa = Pa;
const Ca = /* @__PURE__ */ pa(xa);
var cn = function(e, t) {
  return cn = Object.setPrototypeOf || { __proto__: [] } instanceof Array && function(n, r) {
    n.__proto__ = r;
  } || function(n, r) {
    for (var i in r)
      Object.prototype.hasOwnProperty.call(r, i) && (n[i] = r[i]);
  }, cn(e, t);
};
function Nt(e, t) {
  if (typeof t != "function" && t !== null)
    throw new TypeError("Class extends value " + String(t) + " is not a constructor or null");
  cn(e, t);
  function n() {
    this.constructor = e;
  }
  e.prototype = t === null ? Object.create(t) : (n.prototype = t.prototype, new n());
}
var I = function() {
  return I = Object.assign || function(t) {
    for (var n, r = 1, i = arguments.length; r < i; r++) {
      n = arguments[r];
      for (var s in n)
        Object.prototype.hasOwnProperty.call(n, s) && (t[s] = n[s]);
    }
    return t;
  }, I.apply(this, arguments);
};
function Yt(e, t, n) {
  if (n || arguments.length === 2)
    for (var r = 0, i = t.length, s; r < i; r++)
      (s || !(r in t)) && (s || (s = Array.prototype.slice.call(t, 0, r)), s[r] = t[r]);
  return e.concat(s || Array.prototype.slice.call(t));
}
var N;
(function(e) {
  e[e.EXPECT_ARGUMENT_CLOSING_BRACE = 1] = "EXPECT_ARGUMENT_CLOSING_BRACE", e[e.EMPTY_ARGUMENT = 2] = "EMPTY_ARGUMENT", e[e.MALFORMED_ARGUMENT = 3] = "MALFORMED_ARGUMENT", e[e.EXPECT_ARGUMENT_TYPE = 4] = "EXPECT_ARGUMENT_TYPE", e[e.INVALID_ARGUMENT_TYPE = 5] = "INVALID_ARGUMENT_TYPE", e[e.EXPECT_ARGUMENT_STYLE = 6] = "EXPECT_ARGUMENT_STYLE", e[e.INVALID_NUMBER_SKELETON = 7] = "INVALID_NUMBER_SKELETON", e[e.INVALID_DATE_TIME_SKELETON = 8] = "INVALID_DATE_TIME_SKELETON", e[e.EXPECT_NUMBER_SKELETON = 9] = "EXPECT_NUMBER_SKELETON", e[e.EXPECT_DATE_TIME_SKELETON = 10] = "EXPECT_DATE_TIME_SKELETON", e[e.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE = 11] = "UNCLOSED_QUOTE_IN_ARGUMENT_STYLE", e[e.EXPECT_SELECT_ARGUMENT_OPTIONS = 12] = "EXPECT_SELECT_ARGUMENT_OPTIONS", e[e.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE = 13] = "EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE = 14] = "INVALID_PLURAL_ARGUMENT_OFFSET_VALUE", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR = 15] = "EXPECT_SELECT_ARGUMENT_SELECTOR", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR = 16] = "EXPECT_PLURAL_ARGUMENT_SELECTOR", e[e.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT = 17] = "EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT", e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT = 18] = "EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT", e[e.INVALID_PLURAL_ARGUMENT_SELECTOR = 19] = "INVALID_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_PLURAL_ARGUMENT_SELECTOR = 20] = "DUPLICATE_PLURAL_ARGUMENT_SELECTOR", e[e.DUPLICATE_SELECT_ARGUMENT_SELECTOR = 21] = "DUPLICATE_SELECT_ARGUMENT_SELECTOR", e[e.MISSING_OTHER_CLAUSE = 22] = "MISSING_OTHER_CLAUSE", e[e.INVALID_TAG = 23] = "INVALID_TAG", e[e.INVALID_TAG_NAME = 25] = "INVALID_TAG_NAME", e[e.UNMATCHED_CLOSING_TAG = 26] = "UNMATCHED_CLOSING_TAG", e[e.UNCLOSED_TAG = 27] = "UNCLOSED_TAG";
})(N || (N = {}));
var M;
(function(e) {
  e[e.literal = 0] = "literal", e[e.argument = 1] = "argument", e[e.number = 2] = "number", e[e.date = 3] = "date", e[e.time = 4] = "time", e[e.select = 5] = "select", e[e.plural = 6] = "plural", e[e.pound = 7] = "pound", e[e.tag = 8] = "tag";
})(M || (M = {}));
var Je;
(function(e) {
  e[e.number = 0] = "number", e[e.dateTime = 1] = "dateTime";
})(Je || (Je = {}));
function dr(e) {
  return e.type === M.literal;
}
function Ia(e) {
  return e.type === M.argument;
}
function $r(e) {
  return e.type === M.number;
}
function ei(e) {
  return e.type === M.date;
}
function ti(e) {
  return e.type === M.time;
}
function ni(e) {
  return e.type === M.select;
}
function ri(e) {
  return e.type === M.plural;
}
function Oa(e) {
  return e.type === M.pound;
}
function ii(e) {
  return e.type === M.tag;
}
function si(e) {
  return !!(e && typeof e == "object" && e.type === Je.number);
}
function hn(e) {
  return !!(e && typeof e == "object" && e.type === Je.dateTime);
}
var oi = /[ \xA0\u1680\u2000-\u200A\u202F\u205F\u3000]/, La = /(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;
function ka(e) {
  var t = {};
  return e.replace(La, function(n) {
    var r = n.length;
    switch (n[0]) {
      case "G":
        t.era = r === 4 ? "long" : r === 5 ? "narrow" : "short";
        break;
      case "y":
        t.year = r === 2 ? "2-digit" : "numeric";
        break;
      case "Y":
      case "u":
      case "U":
      case "r":
        throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");
      case "q":
      case "Q":
        throw new RangeError("`q/Q` (quarter) patterns are not supported");
      case "M":
      case "L":
        t.month = ["numeric", "2-digit", "short", "long", "narrow"][r - 1];
        break;
      case "w":
      case "W":
        throw new RangeError("`w/W` (week) patterns are not supported");
      case "d":
        t.day = ["numeric", "2-digit"][r - 1];
        break;
      case "D":
      case "F":
      case "g":
        throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");
      case "E":
        t.weekday = r === 4 ? "short" : r === 5 ? "narrow" : "short";
        break;
      case "e":
        if (r < 4)
          throw new RangeError("`e..eee` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][r - 4];
        break;
      case "c":
        if (r < 4)
          throw new RangeError("`c..ccc` (weekday) patterns are not supported");
        t.weekday = ["short", "long", "narrow", "short"][r - 4];
        break;
      case "a":
        t.hour12 = !0;
        break;
      case "b":
      case "B":
        throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");
      case "h":
        t.hourCycle = "h12", t.hour = ["numeric", "2-digit"][r - 1];
        break;
      case "H":
        t.hourCycle = "h23", t.hour = ["numeric", "2-digit"][r - 1];
        break;
      case "K":
        t.hourCycle = "h11", t.hour = ["numeric", "2-digit"][r - 1];
        break;
      case "k":
        t.hourCycle = "h24", t.hour = ["numeric", "2-digit"][r - 1];
        break;
      case "j":
      case "J":
      case "C":
        throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");
      case "m":
        t.minute = ["numeric", "2-digit"][r - 1];
        break;
      case "s":
        t.second = ["numeric", "2-digit"][r - 1];
        break;
      case "S":
      case "A":
        throw new RangeError("`S/A` (second) patterns are not supported, use `s` instead");
      case "z":
        t.timeZoneName = r < 4 ? "short" : "long";
        break;
      case "Z":
      case "O":
      case "v":
      case "V":
      case "X":
      case "x":
        throw new RangeError("`Z/O/v/V/X/x` (timeZone) patterns are not supported, use `z` instead");
    }
    return "";
  }), t;
}
var Ma = /[\t-\r \x85\u200E\u200F\u2028\u2029]/i;
function Ra(e) {
  if (e.length === 0)
    throw new Error("Number skeleton cannot be empty");
  for (var t = e.split(Ma).filter(function(c) {
    return c.length > 0;
  }), n = [], r = 0, i = t; r < i.length; r++) {
    var s = i[r], o = s.split("/");
    if (o.length === 0)
      throw new Error("Invalid number skeleton");
    for (var a = o[0], l = o.slice(1), u = 0, f = l; u < f.length; u++) {
      var h = f[u];
      if (h.length === 0)
        throw new Error("Invalid number skeleton");
    }
    n.push({ stem: a, options: l });
  }
  return n;
}
function Da(e) {
  return e.replace(/^(.*?)-/, "");
}
var _r = /^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g, ai = /^(@+)?(\+|#+)?[rs]?$/g, Ua = /(\*)(0+)|(#+)(0+)|(0+)/g, li = /^(0+)$/;
function mr(e) {
  var t = {};
  return e[e.length - 1] === "r" ? t.roundingPriority = "morePrecision" : e[e.length - 1] === "s" && (t.roundingPriority = "lessPrecision"), e.replace(ai, function(n, r, i) {
    return typeof i != "string" ? (t.minimumSignificantDigits = r.length, t.maximumSignificantDigits = r.length) : i === "+" ? t.minimumSignificantDigits = r.length : r[0] === "#" ? t.maximumSignificantDigits = r.length : (t.minimumSignificantDigits = r.length, t.maximumSignificantDigits = r.length + (typeof i == "string" ? i.length : 0)), "";
  }), t;
}
function ui(e) {
  switch (e) {
    case "sign-auto":
      return {
        signDisplay: "auto"
      };
    case "sign-accounting":
    case "()":
      return {
        currencySign: "accounting"
      };
    case "sign-always":
    case "+!":
      return {
        signDisplay: "always"
      };
    case "sign-accounting-always":
    case "()!":
      return {
        signDisplay: "always",
        currencySign: "accounting"
      };
    case "sign-except-zero":
    case "+?":
      return {
        signDisplay: "exceptZero"
      };
    case "sign-accounting-except-zero":
    case "()?":
      return {
        signDisplay: "exceptZero",
        currencySign: "accounting"
      };
    case "sign-never":
    case "+_":
      return {
        signDisplay: "never"
      };
  }
}
function Fa(e) {
  var t;
  if (e[0] === "E" && e[1] === "E" ? (t = {
    notation: "engineering"
  }, e = e.slice(2)) : e[0] === "E" && (t = {
    notation: "scientific"
  }, e = e.slice(1)), t) {
    var n = e.slice(0, 2);
    if (n === "+!" ? (t.signDisplay = "always", e = e.slice(2)) : n === "+?" && (t.signDisplay = "exceptZero", e = e.slice(2)), !li.test(e))
      throw new Error("Malformed concise eng/scientific notation");
    t.minimumIntegerDigits = e.length;
  }
  return t;
}
function pr(e) {
  var t = {}, n = ui(e);
  return n || t;
}
function Ga(e) {
  for (var t = {}, n = 0, r = e; n < r.length; n++) {
    var i = r[n];
    switch (i.stem) {
      case "percent":
      case "%":
        t.style = "percent";
        continue;
      case "%x100":
        t.style = "percent", t.scale = 100;
        continue;
      case "currency":
        t.style = "currency", t.currency = i.options[0];
        continue;
      case "group-off":
      case ",_":
        t.useGrouping = !1;
        continue;
      case "precision-integer":
      case ".":
        t.maximumFractionDigits = 0;
        continue;
      case "measure-unit":
      case "unit":
        t.style = "unit", t.unit = Da(i.options[0]);
        continue;
      case "compact-short":
      case "K":
        t.notation = "compact", t.compactDisplay = "short";
        continue;
      case "compact-long":
      case "KK":
        t.notation = "compact", t.compactDisplay = "long";
        continue;
      case "scientific":
        t = I(I(I({}, t), { notation: "scientific" }), i.options.reduce(function(l, u) {
          return I(I({}, l), pr(u));
        }, {}));
        continue;
      case "engineering":
        t = I(I(I({}, t), { notation: "engineering" }), i.options.reduce(function(l, u) {
          return I(I({}, l), pr(u));
        }, {}));
        continue;
      case "notation-simple":
        t.notation = "standard";
        continue;
      case "unit-width-narrow":
        t.currencyDisplay = "narrowSymbol", t.unitDisplay = "narrow";
        continue;
      case "unit-width-short":
        t.currencyDisplay = "code", t.unitDisplay = "short";
        continue;
      case "unit-width-full-name":
        t.currencyDisplay = "name", t.unitDisplay = "long";
        continue;
      case "unit-width-iso-code":
        t.currencyDisplay = "symbol";
        continue;
      case "scale":
        t.scale = parseFloat(i.options[0]);
        continue;
      case "integer-width":
        if (i.options.length > 1)
          throw new RangeError("integer-width stems only accept a single optional option");
        i.options[0].replace(Ua, function(l, u, f, h, c, d) {
          if (u)
            t.minimumIntegerDigits = f.length;
          else {
            if (h && c)
              throw new Error("We currently do not support maximum integer digits");
            if (d)
              throw new Error("We currently do not support exact integer digits");
          }
          return "";
        });
        continue;
    }
    if (li.test(i.stem)) {
      t.minimumIntegerDigits = i.stem.length;
      continue;
    }
    if (_r.test(i.stem)) {
      if (i.options.length > 1)
        throw new RangeError("Fraction-precision stems only accept a single optional option");
      i.stem.replace(_r, function(l, u, f, h, c, d) {
        return f === "*" ? t.minimumFractionDigits = u.length : h && h[0] === "#" ? t.maximumFractionDigits = h.length : c && d ? (t.minimumFractionDigits = c.length, t.maximumFractionDigits = c.length + d.length) : (t.minimumFractionDigits = u.length, t.maximumFractionDigits = u.length), "";
      });
      var s = i.options[0];
      s === "w" ? t = I(I({}, t), { trailingZeroDisplay: "stripIfInteger" }) : s && (t = I(I({}, t), mr(s)));
      continue;
    }
    if (ai.test(i.stem)) {
      t = I(I({}, t), mr(i.stem));
      continue;
    }
    var o = ui(i.stem);
    o && (t = I(I({}, t), o));
    var a = Fa(i.stem);
    a && (t = I(I({}, t), a));
  }
  return t;
}
var Et = {
  AX: [
    "H"
  ],
  BQ: [
    "H"
  ],
  CP: [
    "H"
  ],
  CZ: [
    "H"
  ],
  DK: [
    "H"
  ],
  FI: [
    "H"
  ],
  ID: [
    "H"
  ],
  IS: [
    "H"
  ],
  ML: [
    "H"
  ],
  NE: [
    "H"
  ],
  RU: [
    "H"
  ],
  SE: [
    "H"
  ],
  SJ: [
    "H"
  ],
  SK: [
    "H"
  ],
  AS: [
    "h",
    "H"
  ],
  BT: [
    "h",
    "H"
  ],
  DJ: [
    "h",
    "H"
  ],
  ER: [
    "h",
    "H"
  ],
  GH: [
    "h",
    "H"
  ],
  IN: [
    "h",
    "H"
  ],
  LS: [
    "h",
    "H"
  ],
  PG: [
    "h",
    "H"
  ],
  PW: [
    "h",
    "H"
  ],
  SO: [
    "h",
    "H"
  ],
  TO: [
    "h",
    "H"
  ],
  VU: [
    "h",
    "H"
  ],
  WS: [
    "h",
    "H"
  ],
  "001": [
    "H",
    "h"
  ],
  AL: [
    "h",
    "H",
    "hB"
  ],
  TD: [
    "h",
    "H",
    "hB"
  ],
  "ca-ES": [
    "H",
    "h",
    "hB"
  ],
  CF: [
    "H",
    "h",
    "hB"
  ],
  CM: [
    "H",
    "h",
    "hB"
  ],
  "fr-CA": [
    "H",
    "h",
    "hB"
  ],
  "gl-ES": [
    "H",
    "h",
    "hB"
  ],
  "it-CH": [
    "H",
    "h",
    "hB"
  ],
  "it-IT": [
    "H",
    "h",
    "hB"
  ],
  LU: [
    "H",
    "h",
    "hB"
  ],
  NP: [
    "H",
    "h",
    "hB"
  ],
  PF: [
    "H",
    "h",
    "hB"
  ],
  SC: [
    "H",
    "h",
    "hB"
  ],
  SM: [
    "H",
    "h",
    "hB"
  ],
  SN: [
    "H",
    "h",
    "hB"
  ],
  TF: [
    "H",
    "h",
    "hB"
  ],
  VA: [
    "H",
    "h",
    "hB"
  ],
  CY: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  GR: [
    "h",
    "H",
    "hb",
    "hB"
  ],
  CO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  DO: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KP: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  KR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  NA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PA: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  PR: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  VE: [
    "h",
    "H",
    "hB",
    "hb"
  ],
  AC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  AI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  BW: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  BZ: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CC: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  CX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  DG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  FK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GB: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  GI: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IM: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  IO: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  JE: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  LT: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MK: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  MS: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NF: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NG: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NR: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  NU: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  PN: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SH: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  SX: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  TA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  ZA: [
    "H",
    "h",
    "hb",
    "hB"
  ],
  "af-ZA": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  AR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CL: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CR: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  CU: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  EA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-BO": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-BR": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-EC": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-ES": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-GQ": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  "es-PE": [
    "H",
    "h",
    "hB",
    "hb"
  ],
  GT: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  HN: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  IC: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KG: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  KM: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  LK: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MA: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  MX: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  NI: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  PY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  SV: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  UY: [
    "H",
    "h",
    "hB",
    "hb"
  ],
  JP: [
    "H",
    "h",
    "K"
  ],
  AD: [
    "H",
    "hB"
  ],
  AM: [
    "H",
    "hB"
  ],
  AO: [
    "H",
    "hB"
  ],
  AT: [
    "H",
    "hB"
  ],
  AW: [
    "H",
    "hB"
  ],
  BE: [
    "H",
    "hB"
  ],
  BF: [
    "H",
    "hB"
  ],
  BJ: [
    "H",
    "hB"
  ],
  BL: [
    "H",
    "hB"
  ],
  BR: [
    "H",
    "hB"
  ],
  CG: [
    "H",
    "hB"
  ],
  CI: [
    "H",
    "hB"
  ],
  CV: [
    "H",
    "hB"
  ],
  DE: [
    "H",
    "hB"
  ],
  EE: [
    "H",
    "hB"
  ],
  FR: [
    "H",
    "hB"
  ],
  GA: [
    "H",
    "hB"
  ],
  GF: [
    "H",
    "hB"
  ],
  GN: [
    "H",
    "hB"
  ],
  GP: [
    "H",
    "hB"
  ],
  GW: [
    "H",
    "hB"
  ],
  HR: [
    "H",
    "hB"
  ],
  IL: [
    "H",
    "hB"
  ],
  IT: [
    "H",
    "hB"
  ],
  KZ: [
    "H",
    "hB"
  ],
  MC: [
    "H",
    "hB"
  ],
  MD: [
    "H",
    "hB"
  ],
  MF: [
    "H",
    "hB"
  ],
  MQ: [
    "H",
    "hB"
  ],
  MZ: [
    "H",
    "hB"
  ],
  NC: [
    "H",
    "hB"
  ],
  NL: [
    "H",
    "hB"
  ],
  PM: [
    "H",
    "hB"
  ],
  PT: [
    "H",
    "hB"
  ],
  RE: [
    "H",
    "hB"
  ],
  RO: [
    "H",
    "hB"
  ],
  SI: [
    "H",
    "hB"
  ],
  SR: [
    "H",
    "hB"
  ],
  ST: [
    "H",
    "hB"
  ],
  TG: [
    "H",
    "hB"
  ],
  TR: [
    "H",
    "hB"
  ],
  WF: [
    "H",
    "hB"
  ],
  YT: [
    "H",
    "hB"
  ],
  BD: [
    "h",
    "hB",
    "H"
  ],
  PK: [
    "h",
    "hB",
    "H"
  ],
  AZ: [
    "H",
    "hB",
    "h"
  ],
  BA: [
    "H",
    "hB",
    "h"
  ],
  BG: [
    "H",
    "hB",
    "h"
  ],
  CH: [
    "H",
    "hB",
    "h"
  ],
  GE: [
    "H",
    "hB",
    "h"
  ],
  LI: [
    "H",
    "hB",
    "h"
  ],
  ME: [
    "H",
    "hB",
    "h"
  ],
  RS: [
    "H",
    "hB",
    "h"
  ],
  UA: [
    "H",
    "hB",
    "h"
  ],
  UZ: [
    "H",
    "hB",
    "h"
  ],
  XK: [
    "H",
    "hB",
    "h"
  ],
  AG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  AU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  CA: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  DM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  "en-001": [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FJ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  FM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GD: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GU: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  GY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  JM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KN: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  KY: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  LR: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MH: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MP: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  MW: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  NZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SB: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SL: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SS: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  SZ: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  TT: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  UM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  US: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VC: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VG: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  VI: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  ZM: [
    "h",
    "hb",
    "H",
    "hB"
  ],
  BO: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  EC: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  ES: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  GQ: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  PE: [
    "H",
    "hB",
    "h",
    "hb"
  ],
  AE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  "ar-001": [
    "h",
    "hB",
    "hb",
    "H"
  ],
  BH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  DZ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EG: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  EH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  HK: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  IQ: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  JO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  KW: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  LB: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  LY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MO: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  MR: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  OM: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PH: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  PS: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  QA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SA: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SD: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  SY: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  TN: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  YE: [
    "h",
    "hB",
    "hb",
    "H"
  ],
  AF: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  LA: [
    "H",
    "hb",
    "hB",
    "h"
  ],
  CN: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  LV: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  TL: [
    "H",
    "hB",
    "hb",
    "h"
  ],
  "zu-ZA": [
    "H",
    "hB",
    "hb",
    "h"
  ],
  CD: [
    "hB",
    "H"
  ],
  IR: [
    "hB",
    "H"
  ],
  "hi-IN": [
    "hB",
    "h",
    "H"
  ],
  "kn-IN": [
    "hB",
    "h",
    "H"
  ],
  "ml-IN": [
    "hB",
    "h",
    "H"
  ],
  "te-IN": [
    "hB",
    "h",
    "H"
  ],
  KH: [
    "hB",
    "h",
    "H",
    "hb"
  ],
  "ta-IN": [
    "hB",
    "h",
    "hb",
    "H"
  ],
  BN: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  MY: [
    "hb",
    "hB",
    "h",
    "H"
  ],
  ET: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "gu-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "mr-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  "pa-IN": [
    "hB",
    "hb",
    "h",
    "H"
  ],
  TW: [
    "hB",
    "hb",
    "h",
    "H"
  ],
  KE: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  MM: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  TZ: [
    "hB",
    "hb",
    "H",
    "h"
  ],
  UG: [
    "hB",
    "hb",
    "H",
    "h"
  ]
};
function ja(e, t) {
  for (var n = "", r = 0; r < e.length; r++) {
    var i = e.charAt(r);
    if (i === "j") {
      for (var s = 0; r + 1 < e.length && e.charAt(r + 1) === i; )
        s++, r++;
      var o = 1 + (s & 1), a = s < 2 ? 1 : 3 + (s >> 1), l = "a", u = qa(t);
      for ((u == "H" || u == "k") && (a = 0); a-- > 0; )
        n += l;
      for (; o-- > 0; )
        n = u + n;
    } else
      i === "J" ? n += "H" : n += i;
  }
  return n;
}
function qa(e) {
  var t = e.hourCycle;
  if (t === void 0 && // @ts-ignore hourCycle(s) is not identified yet
  e.hourCycles && // @ts-ignore
  e.hourCycles.length && (t = e.hourCycles[0]), t)
    switch (t) {
      case "h24":
        return "k";
      case "h23":
        return "H";
      case "h12":
        return "h";
      case "h11":
        return "K";
      default:
        throw new Error("Invalid hourCycle");
    }
  var n = e.language, r;
  n !== "root" && (r = e.maximize().region);
  var i = Et[r || ""] || Et[n || ""] || Et["".concat(n, "-001")] || Et["001"];
  return i[0];
}
var Kt, Va = new RegExp("^".concat(oi.source, "*")), za = new RegExp("".concat(oi.source, "*$"));
function P(e, t) {
  return { start: e, end: t };
}
var Xa = !!String.prototype.startsWith, Wa = !!String.fromCodePoint, Za = !!Object.fromEntries, Ja = !!String.prototype.codePointAt, Qa = !!String.prototype.trimStart, Ya = !!String.prototype.trimEnd, Ka = !!Number.isSafeInteger, $a = Ka ? Number.isSafeInteger : function(e) {
  return typeof e == "number" && isFinite(e) && Math.floor(e) === e && Math.abs(e) <= 9007199254740991;
}, dn = !0;
try {
  var el = ci("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  dn = ((Kt = el.exec("a")) === null || Kt === void 0 ? void 0 : Kt[0]) === "a";
} catch {
  dn = !1;
}
var gr = Xa ? (
  // Native
  function(t, n, r) {
    return t.startsWith(n, r);
  }
) : (
  // For IE11
  function(t, n, r) {
    return t.slice(r, r + n.length) === n;
  }
), _n = Wa ? String.fromCodePoint : (
  // IE11
  function() {
    for (var t = [], n = 0; n < arguments.length; n++)
      t[n] = arguments[n];
    for (var r = "", i = t.length, s = 0, o; i > s; ) {
      if (o = t[s++], o > 1114111)
        throw RangeError(o + " is not a valid code point");
      r += o < 65536 ? String.fromCharCode(o) : String.fromCharCode(((o -= 65536) >> 10) + 55296, o % 1024 + 56320);
    }
    return r;
  }
), br = (
  // native
  Za ? Object.fromEntries : (
    // Ponyfill
    function(t) {
      for (var n = {}, r = 0, i = t; r < i.length; r++) {
        var s = i[r], o = s[0], a = s[1];
        n[o] = a;
      }
      return n;
    }
  )
), fi = Ja ? (
  // Native
  function(t, n) {
    return t.codePointAt(n);
  }
) : (
  // IE 11
  function(t, n) {
    var r = t.length;
    if (!(n < 0 || n >= r)) {
      var i = t.charCodeAt(n), s;
      return i < 55296 || i > 56319 || n + 1 === r || (s = t.charCodeAt(n + 1)) < 56320 || s > 57343 ? i : (i - 55296 << 10) + (s - 56320) + 65536;
    }
  }
), tl = Qa ? (
  // Native
  function(t) {
    return t.trimStart();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(Va, "");
  }
), nl = Ya ? (
  // Native
  function(t) {
    return t.trimEnd();
  }
) : (
  // Ponyfill
  function(t) {
    return t.replace(za, "");
  }
);
function ci(e, t) {
  return new RegExp(e, t);
}
var mn;
if (dn) {
  var vr = ci("([^\\p{White_Space}\\p{Pattern_Syntax}]*)", "yu");
  mn = function(t, n) {
    var r;
    vr.lastIndex = n;
    var i = vr.exec(t);
    return (r = i[1]) !== null && r !== void 0 ? r : "";
  };
} else
  mn = function(t, n) {
    for (var r = []; ; ) {
      var i = fi(t, n);
      if (i === void 0 || hi(i) || ol(i))
        break;
      r.push(i), n += i >= 65536 ? 2 : 1;
    }
    return _n.apply(void 0, r);
  };
var rl = (
  /** @class */
  function() {
    function e(t, n) {
      n === void 0 && (n = {}), this.message = t, this.position = { offset: 0, line: 1, column: 1 }, this.ignoreTag = !!n.ignoreTag, this.locale = n.locale, this.requiresOtherClause = !!n.requiresOtherClause, this.shouldParseSkeletons = !!n.shouldParseSkeletons;
    }
    return e.prototype.parse = function() {
      if (this.offset() !== 0)
        throw Error("parser can only be used once");
      return this.parseMessage(0, "", !1);
    }, e.prototype.parseMessage = function(t, n, r) {
      for (var i = []; !this.isEOF(); ) {
        var s = this.char();
        if (s === 123) {
          var o = this.parseArgument(t, r);
          if (o.err)
            return o;
          i.push(o.val);
        } else {
          if (s === 125 && t > 0)
            break;
          if (s === 35 && (n === "plural" || n === "selectordinal")) {
            var a = this.clonePosition();
            this.bump(), i.push({
              type: M.pound,
              location: P(a, this.clonePosition())
            });
          } else if (s === 60 && !this.ignoreTag && this.peek() === 47) {
            if (r)
              break;
            return this.error(N.UNMATCHED_CLOSING_TAG, P(this.clonePosition(), this.clonePosition()));
          } else if (s === 60 && !this.ignoreTag && pn(this.peek() || 0)) {
            var o = this.parseTag(t, n);
            if (o.err)
              return o;
            i.push(o.val);
          } else {
            var o = this.parseLiteral(t, n);
            if (o.err)
              return o;
            i.push(o.val);
          }
        }
      }
      return { val: i, err: null };
    }, e.prototype.parseTag = function(t, n) {
      var r = this.clonePosition();
      this.bump();
      var i = this.parseTagName();
      if (this.bumpSpace(), this.bumpIf("/>"))
        return {
          val: {
            type: M.literal,
            value: "<".concat(i, "/>"),
            location: P(r, this.clonePosition())
          },
          err: null
        };
      if (this.bumpIf(">")) {
        var s = this.parseMessage(t + 1, n, !0);
        if (s.err)
          return s;
        var o = s.val, a = this.clonePosition();
        if (this.bumpIf("</")) {
          if (this.isEOF() || !pn(this.char()))
            return this.error(N.INVALID_TAG, P(a, this.clonePosition()));
          var l = this.clonePosition(), u = this.parseTagName();
          return i !== u ? this.error(N.UNMATCHED_CLOSING_TAG, P(l, this.clonePosition())) : (this.bumpSpace(), this.bumpIf(">") ? {
            val: {
              type: M.tag,
              value: i,
              children: o,
              location: P(r, this.clonePosition())
            },
            err: null
          } : this.error(N.INVALID_TAG, P(a, this.clonePosition())));
        } else
          return this.error(N.UNCLOSED_TAG, P(r, this.clonePosition()));
      } else
        return this.error(N.INVALID_TAG, P(r, this.clonePosition()));
    }, e.prototype.parseTagName = function() {
      var t = this.offset();
      for (this.bump(); !this.isEOF() && sl(this.char()); )
        this.bump();
      return this.message.slice(t, this.offset());
    }, e.prototype.parseLiteral = function(t, n) {
      for (var r = this.clonePosition(), i = ""; ; ) {
        var s = this.tryParseQuote(n);
        if (s) {
          i += s;
          continue;
        }
        var o = this.tryParseUnquoted(t, n);
        if (o) {
          i += o;
          continue;
        }
        var a = this.tryParseLeftAngleBracket();
        if (a) {
          i += a;
          continue;
        }
        break;
      }
      var l = P(r, this.clonePosition());
      return {
        val: { type: M.literal, value: i, location: l },
        err: null
      };
    }, e.prototype.tryParseLeftAngleBracket = function() {
      return !this.isEOF() && this.char() === 60 && (this.ignoreTag || // If at the opening tag or closing tag position, bail.
      !il(this.peek() || 0)) ? (this.bump(), "<") : null;
    }, e.prototype.tryParseQuote = function(t) {
      if (this.isEOF() || this.char() !== 39)
        return null;
      switch (this.peek()) {
        case 39:
          return this.bump(), this.bump(), "'";
        case 123:
        case 60:
        case 62:
        case 125:
          break;
        case 35:
          if (t === "plural" || t === "selectordinal")
            break;
          return null;
        default:
          return null;
      }
      this.bump();
      var n = [this.char()];
      for (this.bump(); !this.isEOF(); ) {
        var r = this.char();
        if (r === 39)
          if (this.peek() === 39)
            n.push(39), this.bump();
          else {
            this.bump();
            break;
          }
        else
          n.push(r);
        this.bump();
      }
      return _n.apply(void 0, n);
    }, e.prototype.tryParseUnquoted = function(t, n) {
      if (this.isEOF())
        return null;
      var r = this.char();
      return r === 60 || r === 123 || r === 35 && (n === "plural" || n === "selectordinal") || r === 125 && t > 0 ? null : (this.bump(), _n(r));
    }, e.prototype.parseArgument = function(t, n) {
      var r = this.clonePosition();
      if (this.bump(), this.bumpSpace(), this.isEOF())
        return this.error(N.EXPECT_ARGUMENT_CLOSING_BRACE, P(r, this.clonePosition()));
      if (this.char() === 125)
        return this.bump(), this.error(N.EMPTY_ARGUMENT, P(r, this.clonePosition()));
      var i = this.parseIdentifierIfPossible().value;
      if (!i)
        return this.error(N.MALFORMED_ARGUMENT, P(r, this.clonePosition()));
      if (this.bumpSpace(), this.isEOF())
        return this.error(N.EXPECT_ARGUMENT_CLOSING_BRACE, P(r, this.clonePosition()));
      switch (this.char()) {
        case 125:
          return this.bump(), {
            val: {
              type: M.argument,
              // value does not include the opening and closing braces.
              value: i,
              location: P(r, this.clonePosition())
            },
            err: null
          };
        case 44:
          return this.bump(), this.bumpSpace(), this.isEOF() ? this.error(N.EXPECT_ARGUMENT_CLOSING_BRACE, P(r, this.clonePosition())) : this.parseArgumentOptions(t, n, i, r);
        default:
          return this.error(N.MALFORMED_ARGUMENT, P(r, this.clonePosition()));
      }
    }, e.prototype.parseIdentifierIfPossible = function() {
      var t = this.clonePosition(), n = this.offset(), r = mn(this.message, n), i = n + r.length;
      this.bumpTo(i);
      var s = this.clonePosition(), o = P(t, s);
      return { value: r, location: o };
    }, e.prototype.parseArgumentOptions = function(t, n, r, i) {
      var s, o = this.clonePosition(), a = this.parseIdentifierIfPossible().value, l = this.clonePosition();
      switch (a) {
        case "":
          return this.error(N.EXPECT_ARGUMENT_TYPE, P(o, l));
        case "number":
        case "date":
        case "time": {
          this.bumpSpace();
          var u = null;
          if (this.bumpIf(",")) {
            this.bumpSpace();
            var f = this.clonePosition(), h = this.parseSimpleArgStyleIfPossible();
            if (h.err)
              return h;
            var c = nl(h.val);
            if (c.length === 0)
              return this.error(N.EXPECT_ARGUMENT_STYLE, P(this.clonePosition(), this.clonePosition()));
            var d = P(f, this.clonePosition());
            u = { style: c, styleLocation: d };
          }
          var g = this.tryParseArgumentClose(i);
          if (g.err)
            return g;
          var b = P(i, this.clonePosition());
          if (u && gr(u == null ? void 0 : u.style, "::", 0)) {
            var w = tl(u.style.slice(2));
            if (a === "number") {
              var h = this.parseNumberSkeletonFromString(w, u.styleLocation);
              return h.err ? h : {
                val: { type: M.number, value: r, location: b, style: h.val },
                err: null
              };
            } else {
              if (w.length === 0)
                return this.error(N.EXPECT_DATE_TIME_SKELETON, b);
              var H = w;
              this.locale && (H = ja(w, this.locale));
              var c = {
                type: Je.dateTime,
                pattern: H,
                location: u.styleLocation,
                parsedOptions: this.shouldParseSkeletons ? ka(H) : {}
              }, S = a === "date" ? M.date : M.time;
              return {
                val: { type: S, value: r, location: b, style: c },
                err: null
              };
            }
          }
          return {
            val: {
              type: a === "number" ? M.number : a === "date" ? M.date : M.time,
              value: r,
              location: b,
              style: (s = u == null ? void 0 : u.style) !== null && s !== void 0 ? s : null
            },
            err: null
          };
        }
        case "plural":
        case "selectordinal":
        case "select": {
          var m = this.clonePosition();
          if (this.bumpSpace(), !this.bumpIf(","))
            return this.error(N.EXPECT_SELECT_ARGUMENT_OPTIONS, P(m, I({}, m)));
          this.bumpSpace();
          var _ = this.parseIdentifierIfPossible(), E = 0;
          if (a !== "select" && _.value === "offset") {
            if (!this.bumpIf(":"))
              return this.error(N.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, P(this.clonePosition(), this.clonePosition()));
            this.bumpSpace();
            var h = this.tryParseDecimalInteger(N.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE, N.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE);
            if (h.err)
              return h;
            this.bumpSpace(), _ = this.parseIdentifierIfPossible(), E = h.val;
          }
          var X = this.tryParsePluralOrSelectOptions(t, a, n, _);
          if (X.err)
            return X;
          var g = this.tryParseArgumentClose(i);
          if (g.err)
            return g;
          var W = P(i, this.clonePosition());
          return a === "select" ? {
            val: {
              type: M.select,
              value: r,
              options: br(X.val),
              location: W
            },
            err: null
          } : {
            val: {
              type: M.plural,
              value: r,
              options: br(X.val),
              offset: E,
              pluralType: a === "plural" ? "cardinal" : "ordinal",
              location: W
            },
            err: null
          };
        }
        default:
          return this.error(N.INVALID_ARGUMENT_TYPE, P(o, l));
      }
    }, e.prototype.tryParseArgumentClose = function(t) {
      return this.isEOF() || this.char() !== 125 ? this.error(N.EXPECT_ARGUMENT_CLOSING_BRACE, P(t, this.clonePosition())) : (this.bump(), { val: !0, err: null });
    }, e.prototype.parseSimpleArgStyleIfPossible = function() {
      for (var t = 0, n = this.clonePosition(); !this.isEOF(); ) {
        var r = this.char();
        switch (r) {
          case 39: {
            this.bump();
            var i = this.clonePosition();
            if (!this.bumpUntil("'"))
              return this.error(N.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE, P(i, this.clonePosition()));
            this.bump();
            break;
          }
          case 123: {
            t += 1, this.bump();
            break;
          }
          case 125: {
            if (t > 0)
              t -= 1;
            else
              return {
                val: this.message.slice(n.offset, this.offset()),
                err: null
              };
            break;
          }
          default:
            this.bump();
            break;
        }
      }
      return {
        val: this.message.slice(n.offset, this.offset()),
        err: null
      };
    }, e.prototype.parseNumberSkeletonFromString = function(t, n) {
      var r = [];
      try {
        r = Ra(t);
      } catch {
        return this.error(N.INVALID_NUMBER_SKELETON, n);
      }
      return {
        val: {
          type: Je.number,
          tokens: r,
          location: n,
          parsedOptions: this.shouldParseSkeletons ? Ga(r) : {}
        },
        err: null
      };
    }, e.prototype.tryParsePluralOrSelectOptions = function(t, n, r, i) {
      for (var s, o = !1, a = [], l = /* @__PURE__ */ new Set(), u = i.value, f = i.location; ; ) {
        if (u.length === 0) {
          var h = this.clonePosition();
          if (n !== "select" && this.bumpIf("=")) {
            var c = this.tryParseDecimalInteger(N.EXPECT_PLURAL_ARGUMENT_SELECTOR, N.INVALID_PLURAL_ARGUMENT_SELECTOR);
            if (c.err)
              return c;
            f = P(h, this.clonePosition()), u = this.message.slice(h.offset, this.offset());
          } else
            break;
        }
        if (l.has(u))
          return this.error(n === "select" ? N.DUPLICATE_SELECT_ARGUMENT_SELECTOR : N.DUPLICATE_PLURAL_ARGUMENT_SELECTOR, f);
        u === "other" && (o = !0), this.bumpSpace();
        var d = this.clonePosition();
        if (!this.bumpIf("{"))
          return this.error(n === "select" ? N.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT : N.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT, P(this.clonePosition(), this.clonePosition()));
        var g = this.parseMessage(t + 1, n, r);
        if (g.err)
          return g;
        var b = this.tryParseArgumentClose(d);
        if (b.err)
          return b;
        a.push([
          u,
          {
            value: g.val,
            location: P(d, this.clonePosition())
          }
        ]), l.add(u), this.bumpSpace(), s = this.parseIdentifierIfPossible(), u = s.value, f = s.location;
      }
      return a.length === 0 ? this.error(n === "select" ? N.EXPECT_SELECT_ARGUMENT_SELECTOR : N.EXPECT_PLURAL_ARGUMENT_SELECTOR, P(this.clonePosition(), this.clonePosition())) : this.requiresOtherClause && !o ? this.error(N.MISSING_OTHER_CLAUSE, P(this.clonePosition(), this.clonePosition())) : { val: a, err: null };
    }, e.prototype.tryParseDecimalInteger = function(t, n) {
      var r = 1, i = this.clonePosition();
      this.bumpIf("+") || this.bumpIf("-") && (r = -1);
      for (var s = !1, o = 0; !this.isEOF(); ) {
        var a = this.char();
        if (a >= 48 && a <= 57)
          s = !0, o = o * 10 + (a - 48), this.bump();
        else
          break;
      }
      var l = P(i, this.clonePosition());
      return s ? (o *= r, $a(o) ? { val: o, err: null } : this.error(n, l)) : this.error(t, l);
    }, e.prototype.offset = function() {
      return this.position.offset;
    }, e.prototype.isEOF = function() {
      return this.offset() === this.message.length;
    }, e.prototype.clonePosition = function() {
      return {
        offset: this.position.offset,
        line: this.position.line,
        column: this.position.column
      };
    }, e.prototype.char = function() {
      var t = this.position.offset;
      if (t >= this.message.length)
        throw Error("out of bound");
      var n = fi(this.message, t);
      if (n === void 0)
        throw Error("Offset ".concat(t, " is at invalid UTF-16 code unit boundary"));
      return n;
    }, e.prototype.error = function(t, n) {
      return {
        val: null,
        err: {
          kind: t,
          message: this.message,
          location: n
        }
      };
    }, e.prototype.bump = function() {
      if (!this.isEOF()) {
        var t = this.char();
        t === 10 ? (this.position.line += 1, this.position.column = 1, this.position.offset += 1) : (this.position.column += 1, this.position.offset += t < 65536 ? 1 : 2);
      }
    }, e.prototype.bumpIf = function(t) {
      if (gr(this.message, t, this.offset())) {
        for (var n = 0; n < t.length; n++)
          this.bump();
        return !0;
      }
      return !1;
    }, e.prototype.bumpUntil = function(t) {
      var n = this.offset(), r = this.message.indexOf(t, n);
      return r >= 0 ? (this.bumpTo(r), !0) : (this.bumpTo(this.message.length), !1);
    }, e.prototype.bumpTo = function(t) {
      if (this.offset() > t)
        throw Error("targetOffset ".concat(t, " must be greater than or equal to the current offset ").concat(this.offset()));
      for (t = Math.min(t, this.message.length); ; ) {
        var n = this.offset();
        if (n === t)
          break;
        if (n > t)
          throw Error("targetOffset ".concat(t, " is at invalid UTF-16 code unit boundary"));
        if (this.bump(), this.isEOF())
          break;
      }
    }, e.prototype.bumpSpace = function() {
      for (; !this.isEOF() && hi(this.char()); )
        this.bump();
    }, e.prototype.peek = function() {
      if (this.isEOF())
        return null;
      var t = this.char(), n = this.offset(), r = this.message.charCodeAt(n + (t >= 65536 ? 2 : 1));
      return r ?? null;
    }, e;
  }()
);
function pn(e) {
  return e >= 97 && e <= 122 || e >= 65 && e <= 90;
}
function il(e) {
  return pn(e) || e === 47;
}
function sl(e) {
  return e === 45 || e === 46 || e >= 48 && e <= 57 || e === 95 || e >= 97 && e <= 122 || e >= 65 && e <= 90 || e == 183 || e >= 192 && e <= 214 || e >= 216 && e <= 246 || e >= 248 && e <= 893 || e >= 895 && e <= 8191 || e >= 8204 && e <= 8205 || e >= 8255 && e <= 8256 || e >= 8304 && e <= 8591 || e >= 11264 && e <= 12271 || e >= 12289 && e <= 55295 || e >= 63744 && e <= 64975 || e >= 65008 && e <= 65533 || e >= 65536 && e <= 983039;
}
function hi(e) {
  return e >= 9 && e <= 13 || e === 32 || e === 133 || e >= 8206 && e <= 8207 || e === 8232 || e === 8233;
}
function ol(e) {
  return e >= 33 && e <= 35 || e === 36 || e >= 37 && e <= 39 || e === 40 || e === 41 || e === 42 || e === 43 || e === 44 || e === 45 || e >= 46 && e <= 47 || e >= 58 && e <= 59 || e >= 60 && e <= 62 || e >= 63 && e <= 64 || e === 91 || e === 92 || e === 93 || e === 94 || e === 96 || e === 123 || e === 124 || e === 125 || e === 126 || e === 161 || e >= 162 && e <= 165 || e === 166 || e === 167 || e === 169 || e === 171 || e === 172 || e === 174 || e === 176 || e === 177 || e === 182 || e === 187 || e === 191 || e === 215 || e === 247 || e >= 8208 && e <= 8213 || e >= 8214 && e <= 8215 || e === 8216 || e === 8217 || e === 8218 || e >= 8219 && e <= 8220 || e === 8221 || e === 8222 || e === 8223 || e >= 8224 && e <= 8231 || e >= 8240 && e <= 8248 || e === 8249 || e === 8250 || e >= 8251 && e <= 8254 || e >= 8257 && e <= 8259 || e === 8260 || e === 8261 || e === 8262 || e >= 8263 && e <= 8273 || e === 8274 || e === 8275 || e >= 8277 && e <= 8286 || e >= 8592 && e <= 8596 || e >= 8597 && e <= 8601 || e >= 8602 && e <= 8603 || e >= 8604 && e <= 8607 || e === 8608 || e >= 8609 && e <= 8610 || e === 8611 || e >= 8612 && e <= 8613 || e === 8614 || e >= 8615 && e <= 8621 || e === 8622 || e >= 8623 && e <= 8653 || e >= 8654 && e <= 8655 || e >= 8656 && e <= 8657 || e === 8658 || e === 8659 || e === 8660 || e >= 8661 && e <= 8691 || e >= 8692 && e <= 8959 || e >= 8960 && e <= 8967 || e === 8968 || e === 8969 || e === 8970 || e === 8971 || e >= 8972 && e <= 8991 || e >= 8992 && e <= 8993 || e >= 8994 && e <= 9e3 || e === 9001 || e === 9002 || e >= 9003 && e <= 9083 || e === 9084 || e >= 9085 && e <= 9114 || e >= 9115 && e <= 9139 || e >= 9140 && e <= 9179 || e >= 9180 && e <= 9185 || e >= 9186 && e <= 9254 || e >= 9255 && e <= 9279 || e >= 9280 && e <= 9290 || e >= 9291 && e <= 9311 || e >= 9472 && e <= 9654 || e === 9655 || e >= 9656 && e <= 9664 || e === 9665 || e >= 9666 && e <= 9719 || e >= 9720 && e <= 9727 || e >= 9728 && e <= 9838 || e === 9839 || e >= 9840 && e <= 10087 || e === 10088 || e === 10089 || e === 10090 || e === 10091 || e === 10092 || e === 10093 || e === 10094 || e === 10095 || e === 10096 || e === 10097 || e === 10098 || e === 10099 || e === 10100 || e === 10101 || e >= 10132 && e <= 10175 || e >= 10176 && e <= 10180 || e === 10181 || e === 10182 || e >= 10183 && e <= 10213 || e === 10214 || e === 10215 || e === 10216 || e === 10217 || e === 10218 || e === 10219 || e === 10220 || e === 10221 || e === 10222 || e === 10223 || e >= 10224 && e <= 10239 || e >= 10240 && e <= 10495 || e >= 10496 && e <= 10626 || e === 10627 || e === 10628 || e === 10629 || e === 10630 || e === 10631 || e === 10632 || e === 10633 || e === 10634 || e === 10635 || e === 10636 || e === 10637 || e === 10638 || e === 10639 || e === 10640 || e === 10641 || e === 10642 || e === 10643 || e === 10644 || e === 10645 || e === 10646 || e === 10647 || e === 10648 || e >= 10649 && e <= 10711 || e === 10712 || e === 10713 || e === 10714 || e === 10715 || e >= 10716 && e <= 10747 || e === 10748 || e === 10749 || e >= 10750 && e <= 11007 || e >= 11008 && e <= 11055 || e >= 11056 && e <= 11076 || e >= 11077 && e <= 11078 || e >= 11079 && e <= 11084 || e >= 11085 && e <= 11123 || e >= 11124 && e <= 11125 || e >= 11126 && e <= 11157 || e === 11158 || e >= 11159 && e <= 11263 || e >= 11776 && e <= 11777 || e === 11778 || e === 11779 || e === 11780 || e === 11781 || e >= 11782 && e <= 11784 || e === 11785 || e === 11786 || e === 11787 || e === 11788 || e === 11789 || e >= 11790 && e <= 11798 || e === 11799 || e >= 11800 && e <= 11801 || e === 11802 || e === 11803 || e === 11804 || e === 11805 || e >= 11806 && e <= 11807 || e === 11808 || e === 11809 || e === 11810 || e === 11811 || e === 11812 || e === 11813 || e === 11814 || e === 11815 || e === 11816 || e === 11817 || e >= 11818 && e <= 11822 || e === 11823 || e >= 11824 && e <= 11833 || e >= 11834 && e <= 11835 || e >= 11836 && e <= 11839 || e === 11840 || e === 11841 || e === 11842 || e >= 11843 && e <= 11855 || e >= 11856 && e <= 11857 || e === 11858 || e >= 11859 && e <= 11903 || e >= 12289 && e <= 12291 || e === 12296 || e === 12297 || e === 12298 || e === 12299 || e === 12300 || e === 12301 || e === 12302 || e === 12303 || e === 12304 || e === 12305 || e >= 12306 && e <= 12307 || e === 12308 || e === 12309 || e === 12310 || e === 12311 || e === 12312 || e === 12313 || e === 12314 || e === 12315 || e === 12316 || e === 12317 || e >= 12318 && e <= 12319 || e === 12320 || e === 12336 || e === 64830 || e === 64831 || e >= 65093 && e <= 65094;
}
function gn(e) {
  e.forEach(function(t) {
    if (delete t.location, ni(t) || ri(t))
      for (var n in t.options)
        delete t.options[n].location, gn(t.options[n].value);
    else
      $r(t) && si(t.style) || (ei(t) || ti(t)) && hn(t.style) ? delete t.style.location : ii(t) && gn(t.children);
  });
}
function al(e, t) {
  t === void 0 && (t = {}), t = I({ shouldParseSkeletons: !0, requiresOtherClause: !0 }, t);
  var n = new rl(e, t).parse();
  if (n.err) {
    var r = SyntaxError(N[n.err.kind]);
    throw r.location = n.err.location, r.originalMessage = n.err.message, r;
  }
  return t != null && t.captureLocation || gn(n.val), n.val;
}
function $t(e, t) {
  var n = t && t.cache ? t.cache : dl, r = t && t.serializer ? t.serializer : hl, i = t && t.strategy ? t.strategy : ul;
  return i(e, {
    cache: n,
    serializer: r
  });
}
function ll(e) {
  return e == null || typeof e == "number" || typeof e == "boolean";
}
function di(e, t, n, r) {
  var i = ll(r) ? r : n(r), s = t.get(i);
  return typeof s > "u" && (s = e.call(this, r), t.set(i, s)), s;
}
function _i(e, t, n) {
  var r = Array.prototype.slice.call(arguments, 3), i = n(r), s = t.get(i);
  return typeof s > "u" && (s = e.apply(this, r), t.set(i, s)), s;
}
function En(e, t, n, r, i) {
  return n.bind(t, e, r, i);
}
function ul(e, t) {
  var n = e.length === 1 ? di : _i;
  return En(e, this, n, t.cache.create(), t.serializer);
}
function fl(e, t) {
  return En(e, this, _i, t.cache.create(), t.serializer);
}
function cl(e, t) {
  return En(e, this, di, t.cache.create(), t.serializer);
}
var hl = function() {
  return JSON.stringify(arguments);
};
function Sn() {
  this.cache = /* @__PURE__ */ Object.create(null);
}
Sn.prototype.get = function(e) {
  return this.cache[e];
};
Sn.prototype.set = function(e, t) {
  this.cache[e] = t;
};
var dl = {
  create: function() {
    return new Sn();
  }
}, en = {
  variadic: fl,
  monadic: cl
}, Qe;
(function(e) {
  e.MISSING_VALUE = "MISSING_VALUE", e.INVALID_VALUE = "INVALID_VALUE", e.MISSING_INTL_API = "MISSING_INTL_API";
})(Qe || (Qe = {}));
var Pt = (
  /** @class */
  function(e) {
    Nt(t, e);
    function t(n, r, i) {
      var s = e.call(this, n) || this;
      return s.code = r, s.originalMessage = i, s;
    }
    return t.prototype.toString = function() {
      return "[formatjs Error: ".concat(this.code, "] ").concat(this.message);
    }, t;
  }(Error)
), yr = (
  /** @class */
  function(e) {
    Nt(t, e);
    function t(n, r, i, s) {
      return e.call(this, 'Invalid values for "'.concat(n, '": "').concat(r, '". Options are "').concat(Object.keys(i).join('", "'), '"'), Qe.INVALID_VALUE, s) || this;
    }
    return t;
  }(Pt)
), _l = (
  /** @class */
  function(e) {
    Nt(t, e);
    function t(n, r, i) {
      return e.call(this, 'Value for "'.concat(n, '" must be of type ').concat(r), Qe.INVALID_VALUE, i) || this;
    }
    return t;
  }(Pt)
), ml = (
  /** @class */
  function(e) {
    Nt(t, e);
    function t(n, r) {
      return e.call(this, 'The intl string context variable "'.concat(n, '" was not provided to the string "').concat(r, '"'), Qe.MISSING_VALUE, r) || this;
    }
    return t;
  }(Pt)
), z;
(function(e) {
  e[e.literal = 0] = "literal", e[e.object = 1] = "object";
})(z || (z = {}));
function pl(e) {
  return e.length < 2 ? e : e.reduce(function(t, n) {
    var r = t[t.length - 1];
    return !r || r.type !== z.literal || n.type !== z.literal ? t.push(n) : r.value += n.value, t;
  }, []);
}
function gl(e) {
  return typeof e == "function";
}
function St(e, t, n, r, i, s, o) {
  if (e.length === 1 && dr(e[0]))
    return [
      {
        type: z.literal,
        value: e[0].value
      }
    ];
  for (var a = [], l = 0, u = e; l < u.length; l++) {
    var f = u[l];
    if (dr(f)) {
      a.push({
        type: z.literal,
        value: f.value
      });
      continue;
    }
    if (Oa(f)) {
      typeof s == "number" && a.push({
        type: z.literal,
        value: n.getNumberFormat(t).format(s)
      });
      continue;
    }
    var h = f.value;
    if (!(i && h in i))
      throw new ml(h, o);
    var c = i[h];
    if (Ia(f)) {
      (!c || typeof c == "string" || typeof c == "number") && (c = typeof c == "string" || typeof c == "number" ? String(c) : ""), a.push({
        type: typeof c == "string" ? z.literal : z.object,
        value: c
      });
      continue;
    }
    if (ei(f)) {
      var d = typeof f.style == "string" ? r.date[f.style] : hn(f.style) ? f.style.parsedOptions : void 0;
      a.push({
        type: z.literal,
        value: n.getDateTimeFormat(t, d).format(c)
      });
      continue;
    }
    if (ti(f)) {
      var d = typeof f.style == "string" ? r.time[f.style] : hn(f.style) ? f.style.parsedOptions : r.time.medium;
      a.push({
        type: z.literal,
        value: n.getDateTimeFormat(t, d).format(c)
      });
      continue;
    }
    if ($r(f)) {
      var d = typeof f.style == "string" ? r.number[f.style] : si(f.style) ? f.style.parsedOptions : void 0;
      d && d.scale && (c = c * (d.scale || 1)), a.push({
        type: z.literal,
        value: n.getNumberFormat(t, d).format(c)
      });
      continue;
    }
    if (ii(f)) {
      var g = f.children, b = f.value, w = i[b];
      if (!gl(w))
        throw new _l(b, "function", o);
      var H = St(g, t, n, r, i, s), S = w(H.map(function(E) {
        return E.value;
      }));
      Array.isArray(S) || (S = [S]), a.push.apply(a, S.map(function(E) {
        return {
          type: typeof E == "string" ? z.literal : z.object,
          value: E
        };
      }));
    }
    if (ni(f)) {
      var m = f.options[c] || f.options.other;
      if (!m)
        throw new yr(f.value, c, Object.keys(f.options), o);
      a.push.apply(a, St(m.value, t, n, r, i));
      continue;
    }
    if (ri(f)) {
      var m = f.options["=".concat(c)];
      if (!m) {
        if (!Intl.PluralRules)
          throw new Pt(`Intl.PluralRules is not available in this environment.
Try polyfilling it using "@formatjs/intl-pluralrules"
`, Qe.MISSING_INTL_API, o);
        var _ = n.getPluralRules(t, { type: f.pluralType }).select(c - (f.offset || 0));
        m = f.options[_] || f.options.other;
      }
      if (!m)
        throw new yr(f.value, c, Object.keys(f.options), o);
      a.push.apply(a, St(m.value, t, n, r, i, c - (f.offset || 0)));
      continue;
    }
  }
  return pl(a);
}
function bl(e, t) {
  return t ? I(I(I({}, e || {}), t || {}), Object.keys(e).reduce(function(n, r) {
    return n[r] = I(I({}, e[r]), t[r] || {}), n;
  }, {})) : e;
}
function vl(e, t) {
  return t ? Object.keys(e).reduce(function(n, r) {
    return n[r] = bl(e[r], t[r]), n;
  }, I({}, e)) : e;
}
function tn(e) {
  return {
    create: function() {
      return {
        get: function(t) {
          return e[t];
        },
        set: function(t, n) {
          e[t] = n;
        }
      };
    }
  };
}
function yl(e) {
  return e === void 0 && (e = {
    number: {},
    dateTime: {},
    pluralRules: {}
  }), {
    getNumberFormat: $t(function() {
      for (var t, n = [], r = 0; r < arguments.length; r++)
        n[r] = arguments[r];
      return new ((t = Intl.NumberFormat).bind.apply(t, Yt([void 0], n, !1)))();
    }, {
      cache: tn(e.number),
      strategy: en.variadic
    }),
    getDateTimeFormat: $t(function() {
      for (var t, n = [], r = 0; r < arguments.length; r++)
        n[r] = arguments[r];
      return new ((t = Intl.DateTimeFormat).bind.apply(t, Yt([void 0], n, !1)))();
    }, {
      cache: tn(e.dateTime),
      strategy: en.variadic
    }),
    getPluralRules: $t(function() {
      for (var t, n = [], r = 0; r < arguments.length; r++)
        n[r] = arguments[r];
      return new ((t = Intl.PluralRules).bind.apply(t, Yt([void 0], n, !1)))();
    }, {
      cache: tn(e.pluralRules),
      strategy: en.variadic
    })
  };
}
var wl = (
  /** @class */
  function() {
    function e(t, n, r, i) {
      var s = this;
      if (n === void 0 && (n = e.defaultLocale), this.formatterCache = {
        number: {},
        dateTime: {},
        pluralRules: {}
      }, this.format = function(o) {
        var a = s.formatToParts(o);
        if (a.length === 1)
          return a[0].value;
        var l = a.reduce(function(u, f) {
          return !u.length || f.type !== z.literal || typeof u[u.length - 1] != "string" ? u.push(f.value) : u[u.length - 1] += f.value, u;
        }, []);
        return l.length <= 1 ? l[0] || "" : l;
      }, this.formatToParts = function(o) {
        return St(s.ast, s.locales, s.formatters, s.formats, o, void 0, s.message);
      }, this.resolvedOptions = function() {
        return {
          locale: s.resolvedLocale.toString()
        };
      }, this.getAst = function() {
        return s.ast;
      }, this.locales = n, this.resolvedLocale = e.resolveLocale(n), typeof t == "string") {
        if (this.message = t, !e.__parse)
          throw new TypeError("IntlMessageFormat.__parse must be set to process `message` of type `string`");
        this.ast = e.__parse(t, {
          ignoreTag: i == null ? void 0 : i.ignoreTag,
          locale: this.resolvedLocale
        });
      } else
        this.ast = t;
      if (!Array.isArray(this.ast))
        throw new TypeError("A message must be provided as a String or AST.");
      this.formats = vl(e.formats, r), this.formatters = i && i.formatters || yl(this.formatterCache);
    }
    return Object.defineProperty(e, "defaultLocale", {
      get: function() {
        return e.memoizedDefaultLocale || (e.memoizedDefaultLocale = new Intl.NumberFormat().resolvedOptions().locale), e.memoizedDefaultLocale;
      },
      enumerable: !1,
      configurable: !0
    }), e.memoizedDefaultLocale = null, e.resolveLocale = function(t) {
      var n = Intl.NumberFormat.supportedLocalesOf(t);
      return n.length > 0 ? new Intl.Locale(n[0]) : new Intl.Locale(typeof t == "string" ? t : t[0]);
    }, e.__parse = al, e.formats = {
      number: {
        integer: {
          maximumFractionDigits: 0
        },
        currency: {
          style: "currency"
        },
        percent: {
          style: "percent"
        }
      },
      date: {
        short: {
          month: "numeric",
          day: "numeric",
          year: "2-digit"
        },
        medium: {
          month: "short",
          day: "numeric",
          year: "numeric"
        },
        long: {
          month: "long",
          day: "numeric",
          year: "numeric"
        },
        full: {
          weekday: "long",
          month: "long",
          day: "numeric",
          year: "numeric"
        }
      },
      time: {
        short: {
          hour: "numeric",
          minute: "numeric"
        },
        medium: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric"
        },
        long: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        },
        full: {
          hour: "numeric",
          minute: "numeric",
          second: "numeric",
          timeZoneName: "short"
        }
      }
    }, e;
  }()
);
function El(e, t) {
  if (t == null)
    return;
  if (t in e)
    return e[t];
  const n = t.split(".");
  let r = e;
  for (let i = 0; i < n.length; i++)
    if (typeof r == "object") {
      if (i > 0) {
        const s = n.slice(i, n.length).join(".");
        if (s in r) {
          r = r[s];
          break;
        }
      }
      r = r[n[i]];
    } else
      r = void 0;
  return r;
}
const xe = {}, Sl = (e, t, n) => n && (t in xe || (xe[t] = {}), e in xe[t] || (xe[t][e] = n), n), mi = (e, t) => {
  if (t == null)
    return;
  if (t in xe && e in xe[t])
    return xe[t][e];
  const n = xt(t);
  for (let r = 0; r < n.length; r++) {
    const i = n[r], s = Bl(i, e);
    if (s)
      return Sl(e, t, s);
  }
};
let Tn;
const dt = ht({});
function Tl(e) {
  return Tn[e] || null;
}
function pi(e) {
  return e in Tn;
}
function Bl(e, t) {
  if (!pi(e))
    return null;
  const n = Tl(e);
  return El(n, t);
}
function Al(e) {
  if (e == null)
    return;
  const t = xt(e);
  for (let n = 0; n < t.length; n++) {
    const r = t[n];
    if (pi(r))
      return r;
  }
}
function Hl(e, ...t) {
  delete xe[e], dt.update((n) => (n[e] = Ca.all([n[e] || {}, ...t]), n));
}
Ke(
  [dt],
  ([e]) => Object.keys(e)
);
dt.subscribe((e) => Tn = e);
const Tt = {};
function Nl(e, t) {
  Tt[e].delete(t), Tt[e].size === 0 && delete Tt[e];
}
function gi(e) {
  return Tt[e];
}
function Pl(e) {
  return xt(e).map((t) => {
    const n = gi(t);
    return [t, n ? [...n] : []];
  }).filter(([, t]) => t.length > 0);
}
function bn(e) {
  return e == null ? !1 : xt(e).some(
    (t) => {
      var n;
      return (n = gi(t)) == null ? void 0 : n.size;
    }
  );
}
function xl(e, t) {
  return Promise.all(
    t.map((r) => (Nl(e, r), r().then((i) => i.default || i)))
  ).then((r) => Hl(e, ...r));
}
const at = {};
function bi(e) {
  if (!bn(e))
    return e in at ? at[e] : Promise.resolve();
  const t = Pl(e);
  return at[e] = Promise.all(
    t.map(
      ([n, r]) => xl(n, r)
    )
  ).then(() => {
    if (bn(e))
      return bi(e);
    delete at[e];
  }), at[e];
}
const Cl = {
  number: {
    scientific: { notation: "scientific" },
    engineering: { notation: "engineering" },
    compactLong: { notation: "compact", compactDisplay: "long" },
    compactShort: { notation: "compact", compactDisplay: "short" }
  },
  date: {
    short: { month: "numeric", day: "numeric", year: "2-digit" },
    medium: { month: "short", day: "numeric", year: "numeric" },
    long: { month: "long", day: "numeric", year: "numeric" },
    full: { weekday: "long", month: "long", day: "numeric", year: "numeric" }
  },
  time: {
    short: { hour: "numeric", minute: "numeric" },
    medium: { hour: "numeric", minute: "numeric", second: "numeric" },
    long: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    },
    full: {
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
      timeZoneName: "short"
    }
  }
}, Il = {
  fallbackLocale: null,
  loadingDelay: 200,
  formats: Cl,
  warnOnMissingMessages: !0,
  handleMissingMessage: void 0,
  ignoreTag: !0
}, Ol = Il;
function Ye() {
  return Ol;
}
const nn = ht(!1);
var Ll = Object.defineProperty, kl = Object.defineProperties, Ml = Object.getOwnPropertyDescriptors, wr = Object.getOwnPropertySymbols, Rl = Object.prototype.hasOwnProperty, Dl = Object.prototype.propertyIsEnumerable, Er = (e, t, n) => t in e ? Ll(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n, Ul = (e, t) => {
  for (var n in t || (t = {}))
    Rl.call(t, n) && Er(e, n, t[n]);
  if (wr)
    for (var n of wr(t))
      Dl.call(t, n) && Er(e, n, t[n]);
  return e;
}, Fl = (e, t) => kl(e, Ml(t));
let vn;
const At = ht(null);
function Sr(e) {
  return e.split("-").map((t, n, r) => r.slice(0, n + 1).join("-")).reverse();
}
function xt(e, t = Ye().fallbackLocale) {
  const n = Sr(e);
  return t ? [.../* @__PURE__ */ new Set([...n, ...Sr(t)])] : n;
}
function Fe() {
  return vn ?? void 0;
}
At.subscribe((e) => {
  vn = e ?? void 0, typeof window < "u" && e != null && document.documentElement.setAttribute("lang", e);
});
const Gl = (e) => {
  if (e && Al(e) && bn(e)) {
    const { loadingDelay: t } = Ye();
    let n;
    return typeof window < "u" && Fe() != null && t ? n = window.setTimeout(
      () => nn.set(!0),
      t
    ) : nn.set(!0), bi(e).then(() => {
      At.set(e);
    }).finally(() => {
      clearTimeout(n), nn.set(!1);
    });
  }
  return At.set(e);
}, _t = Fl(Ul({}, At), {
  set: Gl
}), Ct = (e) => {
  const t = /* @__PURE__ */ Object.create(null);
  return (r) => {
    const i = JSON.stringify(r);
    return i in t ? t[i] : t[i] = e(r);
  };
};
var jl = Object.defineProperty, Ht = Object.getOwnPropertySymbols, vi = Object.prototype.hasOwnProperty, yi = Object.prototype.propertyIsEnumerable, Tr = (e, t, n) => t in e ? jl(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n, Bn = (e, t) => {
  for (var n in t || (t = {}))
    vi.call(t, n) && Tr(e, n, t[n]);
  if (Ht)
    for (var n of Ht(t))
      yi.call(t, n) && Tr(e, n, t[n]);
  return e;
}, et = (e, t) => {
  var n = {};
  for (var r in e)
    vi.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && Ht)
    for (var r of Ht(e))
      t.indexOf(r) < 0 && yi.call(e, r) && (n[r] = e[r]);
  return n;
};
const ct = (e, t) => {
  const { formats: n } = Ye();
  if (e in n && t in n[e])
    return n[e][t];
  throw new Error(`[svelte-i18n] Unknown "${t}" ${e} format.`);
}, ql = Ct(
  (e) => {
    var t = e, { locale: n, format: r } = t, i = et(t, ["locale", "format"]);
    if (n == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format numbers');
    return r && (i = ct("number", r)), new Intl.NumberFormat(n, i);
  }
), Vl = Ct(
  (e) => {
    var t = e, { locale: n, format: r } = t, i = et(t, ["locale", "format"]);
    if (n == null)
      throw new Error('[svelte-i18n] A "locale" must be set to format dates');
    return r ? i = ct("date", r) : Object.keys(i).length === 0 && (i = ct("date", "short")), new Intl.DateTimeFormat(n, i);
  }
), zl = Ct(
  (e) => {
    var t = e, { locale: n, format: r } = t, i = et(t, ["locale", "format"]);
    if (n == null)
      throw new Error(
        '[svelte-i18n] A "locale" must be set to format time values'
      );
    return r ? i = ct("time", r) : Object.keys(i).length === 0 && (i = ct("time", "short")), new Intl.DateTimeFormat(n, i);
  }
), Xl = (e = {}) => {
  var t = e, {
    locale: n = Fe()
  } = t, r = et(t, [
    "locale"
  ]);
  return ql(Bn({ locale: n }, r));
}, Wl = (e = {}) => {
  var t = e, {
    locale: n = Fe()
  } = t, r = et(t, [
    "locale"
  ]);
  return Vl(Bn({ locale: n }, r));
}, Zl = (e = {}) => {
  var t = e, {
    locale: n = Fe()
  } = t, r = et(t, [
    "locale"
  ]);
  return zl(Bn({ locale: n }, r));
}, Jl = Ct(
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  (e, t = Fe()) => new wl(e, t, Ye().formats, {
    ignoreTag: Ye().ignoreTag
  })
), Ql = (e, t = {}) => {
  var n, r, i, s;
  let o = t;
  typeof e == "object" && (o = e, e = o.id);
  const {
    values: a,
    locale: l = Fe(),
    default: u
  } = o;
  if (l == null)
    throw new Error(
      "[svelte-i18n] Cannot format a message without first setting the initial locale."
    );
  let f = mi(e, l);
  if (!f)
    f = (s = (i = (r = (n = Ye()).handleMissingMessage) == null ? void 0 : r.call(n, { locale: l, id: e, defaultValue: u })) != null ? i : u) != null ? s : e;
  else if (typeof f != "string")
    return console.warn(
      `[svelte-i18n] Message with id "${e}" must be of type "string", found: "${typeof f}". Gettin its value through the "$format" method is deprecated; use the "json" method instead.`
    ), f;
  if (!a)
    return f;
  let h = f;
  try {
    h = Jl(f, l).format(a);
  } catch (c) {
    c instanceof Error && console.warn(
      `[svelte-i18n] Message "${e}" has syntax error:`,
      c.message
    );
  }
  return h;
}, Yl = (e, t) => Zl(t).format(e), Kl = (e, t) => Wl(t).format(e), $l = (e, t) => Xl(t).format(e), eu = (e, t = Fe()) => mi(e, t);
Ke([_t, dt], () => Ql);
Ke([_t], () => Yl);
Ke([_t], () => Kl);
Ke([_t], () => $l);
Ke([_t, dt], () => eu);
const {
  SvelteComponent: tu,
  append: Br,
  attr: be,
  binding_callbacks: nu,
  bubble: Ce,
  create_slot: ru,
  detach: iu,
  element: Ar,
  get_all_dirty_from_scope: su,
  get_slot_changes: ou,
  init: au,
  insert: lu,
  listen: te,
  prevent_default: Ie,
  run_all: uu,
  safe_not_equal: fu,
  space: cu,
  stop_propagation: Oe,
  toggle_class: He,
  transition_in: hu,
  transition_out: du,
  update_slot_base: _u
} = window.__gradio__svelte__internal, { createEventDispatcher: mu, tick: pu, getContext: gu } = window.__gradio__svelte__internal;
function bu(e) {
  let t, n, r, i, s, o, a, l, u;
  const f = (
    /*#slots*/
    e[16].default
  ), h = ru(
    f,
    e,
    /*$$scope*/
    e[15],
    null
  );
  return {
    c() {
      t = Ar("button"), h && h.c(), n = cu(), r = Ar("input"), be(r, "type", "file"), be(
        r,
        "accept",
        /*filetype*/
        e[0]
      ), r.multiple = i = /*file_count*/
      e[4] === "multiple" || void 0, be(r, "webkitdirectory", s = /*file_count*/
      e[4] === "directory" || void 0), be(r, "mozdirectory", o = /*file_count*/
      e[4] === "directory" || void 0), be(r, "class", "svelte-18dlsnh"), be(t, "class", "svelte-18dlsnh"), He(
        t,
        "hidden",
        /*hidden*/
        e[5]
      ), He(
        t,
        "center",
        /*center*/
        e[2]
      ), He(
        t,
        "boundedheight",
        /*boundedheight*/
        e[1]
      ), He(
        t,
        "flex",
        /*flex*/
        e[3]
      );
    },
    m(c, d) {
      lu(c, t, d), h && h.m(t, null), Br(t, n), Br(t, r), e[24](r), a = !0, l || (u = [
        te(
          r,
          "change",
          /*load_files_from_upload*/
          e[9]
        ),
        te(t, "drag", Oe(Ie(
          /*drag_handler*/
          e[17]
        ))),
        te(t, "dragstart", Oe(Ie(
          /*dragstart_handler*/
          e[18]
        ))),
        te(t, "dragend", Oe(Ie(
          /*dragend_handler*/
          e[19]
        ))),
        te(t, "dragover", Oe(Ie(
          /*dragover_handler*/
          e[20]
        ))),
        te(t, "dragenter", Oe(Ie(
          /*dragenter_handler*/
          e[21]
        ))),
        te(t, "dragleave", Oe(Ie(
          /*dragleave_handler*/
          e[22]
        ))),
        te(t, "drop", Oe(Ie(
          /*drop_handler*/
          e[23]
        ))),
        te(
          t,
          "click",
          /*open_file_upload*/
          e[6]
        ),
        te(
          t,
          "drop",
          /*loadFilesFromDrop*/
          e[10]
        ),
        te(
          t,
          "dragenter",
          /*updateDragging*/
          e[8]
        ),
        te(
          t,
          "dragleave",
          /*updateDragging*/
          e[8]
        )
      ], l = !0);
    },
    p(c, [d]) {
      h && h.p && (!a || d & /*$$scope*/
      32768) && _u(
        h,
        f,
        c,
        /*$$scope*/
        c[15],
        a ? ou(
          f,
          /*$$scope*/
          c[15],
          d,
          null
        ) : su(
          /*$$scope*/
          c[15]
        ),
        null
      ), (!a || d & /*filetype*/
      1) && be(
        r,
        "accept",
        /*filetype*/
        c[0]
      ), (!a || d & /*file_count*/
      16 && i !== (i = /*file_count*/
      c[4] === "multiple" || void 0)) && (r.multiple = i), (!a || d & /*file_count*/
      16 && s !== (s = /*file_count*/
      c[4] === "directory" || void 0)) && be(r, "webkitdirectory", s), (!a || d & /*file_count*/
      16 && o !== (o = /*file_count*/
      c[4] === "directory" || void 0)) && be(r, "mozdirectory", o), (!a || d & /*hidden*/
      32) && He(
        t,
        "hidden",
        /*hidden*/
        c[5]
      ), (!a || d & /*center*/
      4) && He(
        t,
        "center",
        /*center*/
        c[2]
      ), (!a || d & /*boundedheight*/
      2) && He(
        t,
        "boundedheight",
        /*boundedheight*/
        c[1]
      ), (!a || d & /*flex*/
      8) && He(
        t,
        "flex",
        /*flex*/
        c[3]
      );
    },
    i(c) {
      a || (hu(h, c), a = !0);
    },
    o(c) {
      du(h, c), a = !1;
    },
    d(c) {
      c && iu(t), h && h.d(c), e[24](null), l = !1, uu(u);
    }
  };
}
function rn(e) {
  let t, n = e[0], r = 1;
  for (; r < e.length; ) {
    const i = e[r], s = e[r + 1];
    if (r += 2, (i === "optionalAccess" || i === "optionalCall") && n == null)
      return;
    i === "access" || i === "optionalAccess" ? (t = n, n = s(n)) : (i === "call" || i === "optionalCall") && (n = s((...o) => n.call(t, ...o)), t = void 0);
  }
  return n;
}
function vu(e, t) {
  return !e || e === "*" ? !0 : e.endsWith("/*") ? t.startsWith(e.slice(0, -1)) : e === t;
}
function yu(e, t, n) {
  let { $$slots: r = {}, $$scope: i } = t, { filetype: s = null } = t, { dragging: o = !1 } = t, { boundedheight: a = !0 } = t, { center: l = !0 } = t, { flex: u = !0 } = t, { file_count: f = "single" } = t, { disable_click: h = !1 } = t, { root: c } = t, { hidden: d = !1 } = t;
  const g = gu("upload_files");
  let b;
  const w = mu();
  function H() {
    n(11, o = !o);
  }
  function S() {
    h || (n(7, b.value = "", b), b.click());
  }
  async function m(p) {
    await pu();
    const k = await la(p, c, g);
    return w("load", f === "single" ? rn([k, "optionalAccess", (y) => y[0]]) : k), k || [];
  }
  async function _(p) {
    if (!p.length)
      return;
    let k = p.map((O) => new File([O], O.name)), y = await ua(k);
    return await m(y);
  }
  async function E(p) {
    const k = p.target;
    k.files && await _(Array.from(k.files));
  }
  async function X(p) {
    if (n(11, o = !1), !rn([p, "access", (y) => y.dataTransfer, "optionalAccess", (y) => y.files]))
      return;
    const k = Array.from(p.dataTransfer.files).filter((y) => rn([
      s,
      "optionalAccess",
      (O) => O.split,
      "call",
      (O) => O(","),
      "access",
      (O) => O.some,
      "call",
      (O) => O((L) => vu(L, y.type))
    ]) ? !0 : (w("error", `Invalid file type only ${s} allowed.`), !1));
    await _(k);
  }
  function W(p) {
    Ce.call(this, e, p);
  }
  function Z(p) {
    Ce.call(this, e, p);
  }
  function we(p) {
    Ce.call(this, e, p);
  }
  function ie(p) {
    Ce.call(this, e, p);
  }
  function Ee(p) {
    Ce.call(this, e, p);
  }
  function Ge(p) {
    Ce.call(this, e, p);
  }
  function Q(p) {
    Ce.call(this, e, p);
  }
  function A(p) {
    nu[p ? "unshift" : "push"](() => {
      b = p, n(7, b);
    });
  }
  return e.$$set = (p) => {
    "filetype" in p && n(0, s = p.filetype), "dragging" in p && n(11, o = p.dragging), "boundedheight" in p && n(1, a = p.boundedheight), "center" in p && n(2, l = p.center), "flex" in p && n(3, u = p.flex), "file_count" in p && n(4, f = p.file_count), "disable_click" in p && n(12, h = p.disable_click), "root" in p && n(13, c = p.root), "hidden" in p && n(5, d = p.hidden), "$$scope" in p && n(15, i = p.$$scope);
  }, [
    s,
    a,
    l,
    u,
    f,
    d,
    S,
    b,
    H,
    E,
    X,
    o,
    h,
    c,
    _,
    i,
    r,
    W,
    Z,
    we,
    ie,
    Ee,
    Ge,
    Q,
    A
  ];
}
class wu extends tu {
  constructor(t) {
    super(), au(this, t, yu, bu, fu, {
      filetype: 0,
      dragging: 11,
      boundedheight: 1,
      center: 2,
      flex: 3,
      file_count: 4,
      disable_click: 12,
      root: 13,
      hidden: 5,
      open_file_upload: 6,
      load_files: 14
    });
  }
  get open_file_upload() {
    return this.$$.ctx[6];
  }
  get load_files() {
    return this.$$.ctx[14];
  }
}
const {
  SvelteComponent: Eu,
  append: Hr,
  attr: Su,
  check_outros: Nr,
  create_component: An,
  destroy_component: Hn,
  detach: Tu,
  element: Bu,
  group_outros: Pr,
  init: Au,
  insert: Hu,
  mount_component: Nn,
  safe_not_equal: Nu,
  set_style: xr,
  space: Cr,
  toggle_class: Ir,
  transition_in: ve,
  transition_out: Me
} = window.__gradio__svelte__internal, { createEventDispatcher: Pu } = window.__gradio__svelte__internal;
function Or(e) {
  let t, n;
  return t = new wn({
    props: {
      Icon: Mi,
      label: (
        /*i18n*/
        e[3]("common.edit")
      )
    }
  }), t.$on(
    "click",
    /*click_handler*/
    e[5]
  ), {
    c() {
      An(t.$$.fragment);
    },
    m(r, i) {
      Nn(t, r, i), n = !0;
    },
    p(r, i) {
      const s = {};
      i & /*i18n*/
      8 && (s.label = /*i18n*/
      r[3]("common.edit")), t.$set(s);
    },
    i(r) {
      n || (ve(t.$$.fragment, r), n = !0);
    },
    o(r) {
      Me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      Hn(t, r);
    }
  };
}
function Lr(e) {
  let t, n;
  return t = new wn({
    props: {
      Icon: Qi,
      label: (
        /*i18n*/
        e[3]("common.undo")
      )
    }
  }), t.$on(
    "click",
    /*click_handler_1*/
    e[6]
  ), {
    c() {
      An(t.$$.fragment);
    },
    m(r, i) {
      Nn(t, r, i), n = !0;
    },
    p(r, i) {
      const s = {};
      i & /*i18n*/
      8 && (s.label = /*i18n*/
      r[3]("common.undo")), t.$set(s);
    },
    i(r) {
      n || (ve(t.$$.fragment, r), n = !0);
    },
    o(r) {
      Me(t.$$.fragment, r), n = !1;
    },
    d(r) {
      Hn(t, r);
    }
  };
}
function xu(e) {
  let t, n, r, i, s, o = (
    /*editable*/
    e[0] && Or(e)
  ), a = (
    /*undoable*/
    e[1] && Lr(e)
  );
  return i = new wn({
    props: {
      Icon: Ni,
      label: (
        /*i18n*/
        e[3]("common.clear")
      )
    }
  }), i.$on(
    "click",
    /*click_handler_2*/
    e[7]
  ), {
    c() {
      t = Bu("div"), o && o.c(), n = Cr(), a && a.c(), r = Cr(), An(i.$$.fragment), Su(t, "class", "svelte-1wj0ocy"), Ir(t, "not-absolute", !/*absolute*/
      e[2]), xr(
        t,
        "position",
        /*absolute*/
        e[2] ? "absolute" : "static"
      );
    },
    m(l, u) {
      Hu(l, t, u), o && o.m(t, null), Hr(t, n), a && a.m(t, null), Hr(t, r), Nn(i, t, null), s = !0;
    },
    p(l, [u]) {
      /*editable*/
      l[0] ? o ? (o.p(l, u), u & /*editable*/
      1 && ve(o, 1)) : (o = Or(l), o.c(), ve(o, 1), o.m(t, n)) : o && (Pr(), Me(o, 1, 1, () => {
        o = null;
      }), Nr()), /*undoable*/
      l[1] ? a ? (a.p(l, u), u & /*undoable*/
      2 && ve(a, 1)) : (a = Lr(l), a.c(), ve(a, 1), a.m(t, r)) : a && (Pr(), Me(a, 1, 1, () => {
        a = null;
      }), Nr());
      const f = {};
      u & /*i18n*/
      8 && (f.label = /*i18n*/
      l[3]("common.clear")), i.$set(f), (!s || u & /*absolute*/
      4) && Ir(t, "not-absolute", !/*absolute*/
      l[2]), u & /*absolute*/
      4 && xr(
        t,
        "position",
        /*absolute*/
        l[2] ? "absolute" : "static"
      );
    },
    i(l) {
      s || (ve(o), ve(a), ve(i.$$.fragment, l), s = !0);
    },
    o(l) {
      Me(o), Me(a), Me(i.$$.fragment, l), s = !1;
    },
    d(l) {
      l && Tu(t), o && o.d(), a && a.d(), Hn(i);
    }
  };
}
function Cu(e, t, n) {
  let { editable: r = !1 } = t, { undoable: i = !1 } = t, { absolute: s = !0 } = t, { i18n: o } = t;
  const a = Pu(), l = () => a("edit"), u = () => a("undo"), f = (h) => {
    a("clear"), h.stopPropagation();
  };
  return e.$$set = (h) => {
    "editable" in h && n(0, r = h.editable), "undoable" in h && n(1, i = h.undoable), "absolute" in h && n(2, s = h.absolute), "i18n" in h && n(3, o = h.i18n);
  }, [
    r,
    i,
    s,
    o,
    a,
    l,
    u,
    f
  ];
}
class Iu extends Eu {
  constructor(t) {
    super(), Au(this, t, Cu, xu, Nu, {
      editable: 0,
      undoable: 1,
      absolute: 2,
      i18n: 3
    });
  }
}
const {
  SvelteComponent: Ou,
  assign: Lu,
  attr: Le,
  check_outros: kr,
  create_component: tt,
  destroy_component: nt,
  detach: lt,
  element: ku,
  empty: Mu,
  get_spread_object: Ru,
  get_spread_update: Du,
  group_outros: Mr,
  init: Uu,
  insert: ut,
  mount_component: rt,
  safe_not_equal: Fu,
  space: yn,
  src_url_equal: Rr,
  transition_in: fe,
  transition_out: _e
} = window.__gradio__svelte__internal, { tick: Dr } = window.__gradio__svelte__internal;
function Ur(e) {
  let t, n;
  const r = [
    {
      autoscroll: (
        /*gradio*/
        e[11].autoscroll
      )
    },
    { i18n: (
      /*gradio*/
      e[11].i18n
    ) },
    /*loading_status*/
    e[10]
  ];
  let i = {};
  for (let s = 0; s < r.length; s += 1)
    i = Lu(i, r[s]);
  return t = new ta({ props: i }), {
    c() {
      tt(t.$$.fragment);
    },
    m(s, o) {
      rt(t, s, o), n = !0;
    },
    p(s, o) {
      const a = o & /*gradio, loading_status*/
      3072 ? Du(r, [
        o & /*gradio*/
        2048 && {
          autoscroll: (
            /*gradio*/
            s[11].autoscroll
          )
        },
        o & /*gradio*/
        2048 && { i18n: (
          /*gradio*/
          s[11].i18n
        ) },
        o & /*loading_status*/
        1024 && Ru(
          /*loading_status*/
          s[10]
        )
      ]) : {};
      t.$set(a);
    },
    i(s) {
      n || (fe(t.$$.fragment, s), n = !0);
    },
    o(s) {
      _e(t.$$.fragment, s), n = !1;
    },
    d(s) {
      nt(t, s);
    }
  };
}
function Gu(e) {
  let t, n;
  return t = new wu({
    props: {
      filetype: "application/pdf",
      file_count: "single",
      root: (
        /*root*/
        e[6]
      ),
      $$slots: { default: [qu] },
      $$scope: { ctx: e }
    }
  }), t.$on(
    "load",
    /*handle_upload*/
    e[14]
  ), {
    c() {
      tt(t.$$.fragment);
    },
    m(r, i) {
      rt(t, r, i), n = !0;
    },
    p(r, i) {
      const s = {};
      i & /*root*/
      64 && (s.root = /*root*/
      r[6]), i & /*$$scope*/
      131072 && (s.$$scope = { dirty: i, ctx: r }), t.$set(s);
    },
    i(r) {
      n || (fe(t.$$.fragment, r), n = !0);
    },
    o(r) {
      _e(t.$$.fragment, r), n = !1;
    },
    d(r) {
      nt(t, r);
    }
  };
}
function ju(e) {
  let t, n, r, i, s;
  return t = new Iu({
    props: {
      i18n: (
        /*gradio*/
        e[11].i18n
      ),
      absolute: !0
    }
  }), t.$on(
    "clear",
    /*handle_clear*/
    e[13]
  ), {
    c() {
      tt(t.$$.fragment), n = yn(), r = ku("iframe"), Le(
        r,
        "title",
        /*label*/
        e[8]
      ), Rr(r.src, i = /*_value*/
      e[12].url) || Le(r, "src", i), Le(r, "width", "100%"), Le(
        r,
        "height",
        /*height*/
        e[7]
      );
    },
    m(o, a) {
      rt(t, o, a), ut(o, n, a), ut(o, r, a), s = !0;
    },
    p(o, a) {
      const l = {};
      a & /*gradio*/
      2048 && (l.i18n = /*gradio*/
      o[11].i18n), t.$set(l), (!s || a & /*label*/
      256) && Le(
        r,
        "title",
        /*label*/
        o[8]
      ), (!s || a & /*_value*/
      4096 && !Rr(r.src, i = /*_value*/
      o[12].url)) && Le(r, "src", i), (!s || a & /*height*/
      128) && Le(
        r,
        "height",
        /*height*/
        o[7]
      );
    },
    i(o) {
      s || (fe(t.$$.fragment, o), s = !0);
    },
    o(o) {
      _e(t.$$.fragment, o), s = !1;
    },
    d(o) {
      o && (lt(n), lt(r)), nt(t, o);
    }
  };
}
function qu(e) {
  let t, n;
  return t = new ps({}), {
    c() {
      tt(t.$$.fragment);
    },
    m(r, i) {
      rt(t, r, i), n = !0;
    },
    i(r) {
      n || (fe(t.$$.fragment, r), n = !0);
    },
    o(r) {
      _e(t.$$.fragment, r), n = !1;
    },
    d(r) {
      nt(t, r);
    }
  };
}
function Vu(e) {
  let t, n, r, i, s, o, a, l = (
    /*loading_status*/
    e[10] && Ur(e)
  );
  n = new Zs({
    props: {
      show_label: (
        /*label*/
        e[8] !== null
      ),
      Icon: qi,
      float: (
        /*value*/
        e[0] === null
      ),
      label: (
        /*label*/
        e[8] || "File"
      )
    }
  });
  const u = [ju, Gu], f = [];
  function h(c, d) {
    return (
      /*_value*/
      c[12] ? 0 : 1
    );
  }
  return i = h(e), s = f[i] = u[i](e), {
    c() {
      l && l.c(), t = yn(), tt(n.$$.fragment), r = yn(), s.c(), o = Mu();
    },
    m(c, d) {
      l && l.m(c, d), ut(c, t, d), rt(n, c, d), ut(c, r, d), f[i].m(c, d), ut(c, o, d), a = !0;
    },
    p(c, d) {
      /*loading_status*/
      c[10] ? l ? (l.p(c, d), d & /*loading_status*/
      1024 && fe(l, 1)) : (l = Ur(c), l.c(), fe(l, 1), l.m(t.parentNode, t)) : l && (Mr(), _e(l, 1, 1, () => {
        l = null;
      }), kr());
      const g = {};
      d & /*label*/
      256 && (g.show_label = /*label*/
      c[8] !== null), d & /*value*/
      1 && (g.float = /*value*/
      c[0] === null), d & /*label*/
      256 && (g.label = /*label*/
      c[8] || "File"), n.$set(g);
      let b = i;
      i = h(c), i === b ? f[i].p(c, d) : (Mr(), _e(f[b], 1, 1, () => {
        f[b] = null;
      }), kr(), s = f[i], s ? s.p(c, d) : (s = f[i] = u[i](c), s.c()), fe(s, 1), s.m(o.parentNode, o));
    },
    i(c) {
      a || (fe(l), fe(n.$$.fragment, c), fe(s), a = !0);
    },
    o(c) {
      _e(l), _e(n.$$.fragment, c), _e(s), a = !1;
    },
    d(c) {
      c && (lt(t), lt(r), lt(o)), l && l.d(c), nt(n, c), f[i].d(c);
    }
  };
}
function zu(e) {
  let t, n;
  return t = new Is({
    props: {
      visible: (
        /*visible*/
        e[3]
      ),
      elem_id: (
        /*elem_id*/
        e[1]
      ),
      elem_classes: (
        /*elem_classes*/
        e[2]
      ),
      container: (
        /*container*/
        e[4]
      ),
      scale: (
        /*scale*/
        e[5]
      ),
      min_width: (
        /*min_width*/
        e[9]
      ),
      $$slots: { default: [Vu] },
      $$scope: { ctx: e }
    }
  }), {
    c() {
      tt(t.$$.fragment);
    },
    m(r, i) {
      rt(t, r, i), n = !0;
    },
    p(r, [i]) {
      const s = {};
      i & /*visible*/
      8 && (s.visible = /*visible*/
      r[3]), i & /*elem_id*/
      2 && (s.elem_id = /*elem_id*/
      r[1]), i & /*elem_classes*/
      4 && (s.elem_classes = /*elem_classes*/
      r[2]), i & /*container*/
      16 && (s.container = /*container*/
      r[4]), i & /*scale*/
      32 && (s.scale = /*scale*/
      r[5]), i & /*min_width*/
      512 && (s.min_width = /*min_width*/
      r[9]), i & /*$$scope, label, _value, height, gradio, root, value, loading_status*/
      138689 && (s.$$scope = { dirty: i, ctx: r }), t.$set(s);
    },
    i(r) {
      n || (fe(t.$$.fragment, r), n = !0);
    },
    o(r) {
      _e(t.$$.fragment, r), n = !1;
    },
    d(r) {
      nt(t, r);
    }
  };
}
function Xu(e, t, n) {
  let { elem_id: r = "" } = t, { elem_classes: i = [] } = t, { visible: s = !0 } = t, { value: o = null } = t, { container: a = !0 } = t, { scale: l = null } = t, { root: u } = t, { height: f = 500 } = t, { label: h } = t, { proxy_url: c } = t, { min_width: d = void 0 } = t, { loading_status: g } = t, { gradio: b } = t, w = o, H = w;
  async function S() {
    n(12, w = null), await Dr(), b.dispatch("change");
  }
  async function m({ detail: _ }) {
    n(0, o = _), await Dr(), b.dispatch("change"), b.dispatch("upload");
  }
  return e.$$set = (_) => {
    "elem_id" in _ && n(1, r = _.elem_id), "elem_classes" in _ && n(2, i = _.elem_classes), "visible" in _ && n(3, s = _.visible), "value" in _ && n(0, o = _.value), "container" in _ && n(4, a = _.container), "scale" in _ && n(5, l = _.scale), "root" in _ && n(6, u = _.root), "height" in _ && n(7, f = _.height), "label" in _ && n(8, h = _.label), "proxy_url" in _ && n(15, c = _.proxy_url), "min_width" in _ && n(9, d = _.min_width), "loading_status" in _ && n(10, g = _.loading_status), "gradio" in _ && n(11, b = _.gradio);
  }, e.$$.update = () => {
    e.$$.dirty & /*value, root, proxy_url*/
    32833 && n(12, w = De(o, u, c)), e.$$.dirty & /*old_value, _value, gradio*/
    71680 && JSON.stringify(H) != JSON.stringify(w) && (n(16, H = w), b.dispatch("change"));
  }, [
    o,
    r,
    i,
    s,
    a,
    l,
    u,
    f,
    h,
    d,
    g,
    b,
    w,
    S,
    m,
    c,
    H
  ];
}
class $u extends Ou {
  constructor(t) {
    super(), Uu(this, t, Xu, zu, Fu, {
      elem_id: 1,
      elem_classes: 2,
      visible: 3,
      value: 0,
      container: 4,
      scale: 5,
      root: 6,
      height: 7,
      label: 8,
      proxy_url: 15,
      min_width: 9,
      loading_status: 10,
      gradio: 11
    });
  }
}
export {
  $u as default
};
