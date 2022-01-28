/**
 * chroma.js - JavaScript library for color conversions
 *
 * Copyright (c) 2011-2019, Gregor Aisch
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. The name Gregor Aisch may not be used to endorse or promote products
 * derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL GREGOR AISCH OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * -------------------------------------------------------
 *
 * chroma.js includes colors from colorbrewer2.org, which are released under
 * the following license:
 *
 * Copyright (c) 2002 Cynthia Brewer, Mark Harrower,
 * and The Pennsylvania State University.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific
 * language governing permissions and limitations under the License.
 *
 * ------------------------------------------------------
 *
 * Named colors are taken from X11 Color Names.
 * http://www.w3.org/TR/css3-color/#svg-color
 *
 * @preserve
 */

! function(r, e) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define(e) : r.chroma = e()
}(this, function() {
    "use strict";
    for (var n = function(r, e, n) {
            return void 0 === e && (e = 0), void 0 === n && (n = 1), r < e ? e : n < r ? n : r
        }, e = {}, r = 0, t = ["Boolean", "Number", "String", "Function", "Array", "Date", "RegExp", "Undefined", "Null"]; r < t.length; r += 1) {
        var a = t[r];
        e["[object " + a + "]"] = a.toLowerCase()
    }
    var Y = function(r) {
            return e[Object.prototype.toString.call(r)] || "object"
        },
        f = Math.PI,
        o = {
            clip_rgb: function(r) {
                r._clipped = !1, r._unclipped = r.slice(0);
                for (var e = 0; e <= 3; e++) e < 3 ? ((r[e] < 0 || 255 < r[e]) && (r._clipped = !0), r[e] = n(r[e], 0, 255)) : 3 === e && (r[e] = n(r[e], 0, 1));
                return r
            },
            limit: n,
            type: Y,
            unpack: function(e, r) {
                return void 0 === r && (r = null), 3 <= e.length ? Array.prototype.slice.call(e) : "object" == Y(e[0]) && r ? r.split("").filter(function(r) {
                    return void 0 !== e[0][r]
                }).map(function(r) {
                    return e[0][r]
                }) : e[0]
            },
            last: function(r) {
                if (r.length < 2) return null;
                var e = r.length - 1;
                return "string" == Y(r[e]) ? r[e].toLowerCase() : null
            },
            PI: f,
            TWOPI: 2 * f,
            PITHIRD: f / 3,
            DEG2RAD: f / 180,
            RAD2DEG: 180 / f
        },
        b = {
            format: {},
            autodetect: []
        },
        c = o.last,
        i = o.clip_rgb,
        l = o.type,
        u = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if ("object" === l(r[0]) && r[0].constructor && r[0].constructor === this.constructor) return r[0];
            var n = c(r),
                t = !1;
            if (!n) {
                t = !0, b.sorted || (b.autodetect = b.autodetect.sort(function(r, e) {
                    return e.p - r.p
                }), b.sorted = !0);
                for (var a = 0, f = b.autodetect; a < f.length; a += 1) {
                    var o = f[a];
                    if (n = o.test.apply(o, r)) break
                }
            }
            if (!b.format[n]) throw new Error("unknown format: " + r);
            var u = b.format[n].apply(null, t ? r : r.slice(0, -1));
            this._rgb = i(u), 3 === this._rgb.length && this._rgb.push(1)
        };
    u.prototype.toString = function() {
        return "function" == l(this.hex) ? this.hex() : "[" + this._rgb.join(",") + "]"
    };
    var A = u,
        h = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            return new(Function.prototype.bind.apply(h.Color, [null].concat(r)))
        };
    h.Color = A, h.version = "2.1.0";
    var _ = h,
        d = o.unpack,
        s = Math.max,
        p = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = d(r, "rgb"),
                t = n[0],
                a = n[1],
                f = n[2],
                o = 1 - s(t /= 255, s(a /= 255, f /= 255)),
                u = o < 1 ? 1 / (1 - o) : 0;
            return [(1 - t - o) * u, (1 - a - o) * u, (1 - f - o) * u, o]
        },
        g = o.unpack,
        v = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = (r = g(r, "cmyk"))[0],
                t = r[1],
                a = r[2],
                f = r[3],
                o = 4 < r.length ? r[4] : 1;
            return 1 === f ? [0, 0, 0, o] : [1 <= n ? 0 : 255 * (1 - n) * (1 - f), 1 <= t ? 0 : 255 * (1 - t) * (1 - f), 1 <= a ? 0 : 255 * (1 - a) * (1 - f), o]
        },
        m = o.unpack,
        y = o.type;
    A.prototype.cmyk = function() {
        return p(this._rgb)
    }, _.cmyk = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["cmyk"])))
    }, b.format.cmyk = v, b.autodetect.push({
        p: 2,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = m(r, "cmyk"), "array" === y(r) && 4 === r.length) return "cmyk"
        }
    });
    var w = o.unpack,
        k = o.last,
        M = function(r) {
            return Math.round(100 * r) / 100
        },
        N = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = w(r, "hsla"),
                t = k(r) || "lsa";
            return n[0] = M(n[0] || 0), n[1] = M(100 * n[1]) + "%", n[2] = M(100 * n[2]) + "%", "hsla" === t || 3 < n.length && n[3] < 1 ? (n[3] = 3 < n.length ? n[3] : 1, t = "hsla") : n.length = 3, t + "(" + n.join(",") + ")"
        },
        x = o.unpack,
        E = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = (r = x(r, "rgba"))[0],
                t = r[1],
                a = r[2];
            n /= 255, t /= 255, a /= 255;
            var f, o, u = Math.min(n, t, a),
                c = Math.max(n, t, a),
                i = (c + u) / 2;
            return c === u ? (f = 0, o = Number.NaN) : f = i < .5 ? (c - u) / (c + u) : (c - u) / (2 - c - u), n == c ? o = (t - a) / (c - u) : t == c ? o = 2 + (a - n) / (c - u) : a == c && (o = 4 + (n - t) / (c - u)), (o *= 60) < 0 && (o += 360), 3 < r.length && void 0 !== r[3] ? [o, f, i, r[3]] : [o, f, i]
        },
        P = o.unpack,
        F = o.last,
        O = Math.round,
        j = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = P(r, "rgba"),
                t = F(r) || "rgb";
            return "hsl" == t.substr(0, 3) ? N(E(n), t) : (n[0] = O(n[0]), n[1] = O(n[1]), n[2] = O(n[2]), ("rgba" === t || 3 < n.length && n[3] < 1) && (n[3] = 3 < n.length ? n[3] : 1, t = "rgba"), t + "(" + n.slice(0, "rgb" === t ? 3 : 4).join(",") + ")")
        },
        G = o.unpack,
        q = Math.round,
        L = function() {
            for (var r, e = [], n = arguments.length; n--;) e[n] = arguments[n];
            var t, a, f, o = (e = G(e, "hsl"))[0],
                u = e[1],
                c = e[2];
            if (0 === u) t = a = f = 255 * c;
            else {
                var i = [0, 0, 0],
                    l = [0, 0, 0],
                    h = c < .5 ? c * (1 + u) : c + u - c * u,
                    d = 2 * c - h,
                    s = o / 360;
                i[0] = s + 1 / 3, i[1] = s, i[2] = s - 1 / 3;
                for (var b = 0; b < 3; b++) i[b] < 0 && (i[b] += 1), 1 < i[b] && (i[b] -= 1), 6 * i[b] < 1 ? l[b] = d + 6 * (h - d) * i[b] : 2 * i[b] < 1 ? l[b] = h : 3 * i[b] < 2 ? l[b] = d + (h - d) * (2 / 3 - i[b]) * 6 : l[b] = d;
                t = (r = [q(255 * l[0]), q(255 * l[1]), q(255 * l[2])])[0], a = r[1], f = r[2]
            }
            return 3 < e.length ? [t, a, f, e[3]] : [t, a, f, 1]
        },
        R = /^rgb\(\s*(-?\d+),\s*(-?\d+)\s*,\s*(-?\d+)\s*\)$/,
        I = /^rgba\(\s*(-?\d+),\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*([01]|[01]?\.\d+)\)$/,
        B = /^rgb\(\s*(-?\d+(?:\.\d+)?)%,\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*\)$/,
        C = /^rgba\(\s*(-?\d+(?:\.\d+)?)%,\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*,\s*([01]|[01]?\.\d+)\)$/,
        D = /^hsl\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*\)$/,
        S = /^hsla\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*,\s*([01]|[01]?\.\d+)\)$/,
        $ = Math.round,
        z = function(r) {
            var e;
            if (r = r.toLowerCase().trim(), b.format.named) try {
                return b.format.named(r)
            } catch (r) {}
            if (e = r.match(R)) {
                for (var n = e.slice(1, 4), t = 0; t < 3; t++) n[t] = +n[t];
                return n[3] = 1, n
            }
            if (e = r.match(I)) {
                for (var a = e.slice(1, 5), f = 0; f < 4; f++) a[f] = +a[f];
                return a
            }
            if (e = r.match(B)) {
                for (var o = e.slice(1, 4), u = 0; u < 3; u++) o[u] = $(2.55 * o[u]);
                return o[3] = 1, o
            }
            if (e = r.match(C)) {
                for (var c = e.slice(1, 5), i = 0; i < 3; i++) c[i] = $(2.55 * c[i]);
                return c[3] = +c[3], c
            }
            if (e = r.match(D)) {
                var l = e.slice(1, 4);
                l[1] *= .01, l[2] *= .01;
                var h = L(l);
                return h[3] = 1, h
            }
            if (e = r.match(S)) {
                var d = e.slice(1, 4);
                d[1] *= .01, d[2] *= .01;
                var s = L(d);
                return s[3] = +e[4], s
            }
        };
    z.test = function(r) {
        return R.test(r) || I.test(r) || B.test(r) || C.test(r) || D.test(r) || S.test(r)
    };
    var T = z,
        U = o.type;
    A.prototype.css = function(r) {
        return j(this._rgb, r)
    }, _.css = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["css"])))
    }, b.format.css = T, b.autodetect.push({
        p: 5,
        test: function(r) {
            for (var e = [], n = arguments.length - 1; 0 < n--;) e[n] = arguments[n + 1];
            if (!e.length && "string" === U(r) && T.test(r)) return "css"
        }
    });
    var V = o.unpack;
    b.format.gl = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        var n = V(r, "rgba");
        return n[0] *= 255, n[1] *= 255, n[2] *= 255, n
    }, _.gl = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["gl"])))
    }, A.prototype.gl = function() {
        var r = this._rgb;
        return [r[0] / 255, r[1] / 255, r[2] / 255, r[3]]
    };
    var W = o.unpack,
        X = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n, t = W(r, "rgb"),
                a = t[0],
                f = t[1],
                o = t[2],
                u = Math.min(a, f, o),
                c = Math.max(a, f, o),
                i = c - u,
                l = 100 * i / 255,
                h = u / (255 - i) * 100;
            return 0 === i ? n = Number.NaN : (a === c && (n = (f - o) / i), f === c && (n = 2 + (o - a) / i), o === c && (n = 4 + (a - f) / i), (n *= 60) < 0 && (n += 360)), [n, l, h]
        },
        H = o.unpack,
        J = Math.floor,
        K = function() {
            for (var r, e, n, t, a, f, o = [], u = arguments.length; u--;) o[u] = arguments[u];
            var c, i, l, h = (o = H(o, "hcg"))[0],
                d = o[1],
                s = o[2];
            s *= 255;
            var b = 255 * d;
            if (0 === d) c = i = l = s;
            else {
                360 === h && (h = 0), 360 < h && (h -= 360), h < 0 && (h += 360);
                var p = J(h /= 60),
                    g = h - p,
                    v = s * (1 - d),
                    m = v + b * (1 - g),
                    y = v + b * g,
                    w = v + b;
                switch (p) {
                    case 0:
                        c = (r = [w, y, v])[0], i = r[1], l = r[2];
                        break;
                    case 1:
                        c = (e = [m, w, v])[0], i = e[1], l = e[2];
                        break;
                    case 2:
                        c = (n = [v, w, y])[0], i = n[1], l = n[2];
                        break;
                    case 3:
                        c = (t = [v, m, w])[0], i = t[1], l = t[2];
                        break;
                    case 4:
                        c = (a = [y, v, w])[0], i = a[1], l = a[2];
                        break;
                    case 5:
                        c = (f = [w, v, m])[0], i = f[1], l = f[2]
                }
            }
            return [c, i, l, 3 < o.length ? o[3] : 1]
        },
        Q = o.unpack,
        Z = o.type;
    A.prototype.hcg = function() {
        return X(this._rgb)
    }, _.hcg = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hcg"])))
    }, b.format.hcg = K, b.autodetect.push({
        p: 1,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = Q(r, "hcg"), "array" === Z(r) && 3 === r.length) return "hcg"
        }
    });
    var rr = o.unpack,
        er = o.last,
        nr = Math.round,
        tr = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = rr(r, "rgba"),
                t = n[0],
                a = n[1],
                f = n[2],
                o = n[3],
                u = er(r) || "auto";
            void 0 === o && (o = 1), "auto" === u && (u = o < 1 ? "rgba" : "rgb");
            var c = "000000" + ((t = nr(t)) << 16 | (a = nr(a)) << 8 | (f = nr(f))).toString(16);
            c = c.substr(c.length - 6);
            var i = "0" + nr(255 * o).toString(16);
            switch (i = i.substr(i.length - 2), u.toLowerCase()) {
                case "rgba":
                    return "#" + c + i;
                case "argb":
                    return "#" + i + c;
                default:
                    return "#" + c
            }
        },
        ar = /^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/,
        fr = /^#?([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$/,
        or = function(r) {
            if (r.match(ar)) {
                4 !== r.length && 7 !== r.length || (r = r.substr(1)), 3 === r.length && (r = (r = r.split(""))[0] + r[0] + r[1] + r[1] + r[2] + r[2]);
                var e = parseInt(r, 16);
                return [e >> 16, e >> 8 & 255, 255 & e, 1]
            }
            if (r.match(fr)) {
                5 !== r.length && 9 !== r.length || (r = r.substr(1)), 4 === r.length && (r = (r = r.split(""))[0] + r[0] + r[1] + r[1] + r[2] + r[2] + r[3] + r[3]);
                var n = parseInt(r, 16);
                return [n >> 24 & 255, n >> 16 & 255, n >> 8 & 255, Math.round((255 & n) / 255 * 100) / 100]
            }
            throw new Error("unknown hex color: " + r)
        },
        ur = o.type;
    A.prototype.hex = function(r) {
        return tr(this._rgb, r)
    }, _.hex = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hex"])))
    }, b.format.hex = or, b.autodetect.push({
        p: 4,
        test: function(r) {
            for (var e = [], n = arguments.length - 1; 0 < n--;) e[n] = arguments[n + 1];
            if (!e.length && "string" === ur(r) && 0 <= [3, 4, 5, 6, 7, 8, 9].indexOf(r.length)) return "hex"
        }
    });
    var cr = o.unpack,
        ir = o.TWOPI,
        lr = Math.min,
        hr = Math.sqrt,
        dr = Math.acos,
        sr = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n, t = cr(r, "rgb"),
                a = t[0],
                f = t[1],
                o = t[2],
                u = lr(a /= 255, f /= 255, o /= 255),
                c = (a + f + o) / 3,
                i = 0 < c ? 1 - u / c : 0;
            return 0 === i ? n = NaN : (n = (a - f + (a - o)) / 2, n /= hr((a - f) * (a - f) + (a - o) * (f - o)), n = dr(n), f < o && (n = ir - n), n /= ir), [360 * n, i, c]
        },
        br = o.unpack,
        pr = o.limit,
        gr = o.TWOPI,
        vr = o.PITHIRD,
        mr = Math.cos,
        yr = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n, t, a, f = (r = br(r, "hsi"))[0],
                o = r[1],
                u = r[2];
            return isNaN(f) && (f = 0), isNaN(o) && (o = 0), 360 < f && (f -= 360), f < 0 && (f += 360), (f /= 360) < 1 / 3 ? t = 1 - ((a = (1 - o) / 3) + (n = (1 + o * mr(gr * f) / mr(vr - gr * f)) / 3)) : f < 2 / 3 ? a = 1 - ((n = (1 - o) / 3) + (t = (1 + o * mr(gr * (f -= 1 / 3)) / mr(vr - gr * f)) / 3)) : n = 1 - ((t = (1 - o) / 3) + (a = (1 + o * mr(gr * (f -= 2 / 3)) / mr(vr - gr * f)) / 3)), [255 * (n = pr(u * n * 3)), 255 * (t = pr(u * t * 3)), 255 * (a = pr(u * a * 3)), 3 < r.length ? r[3] : 1]
        },
        wr = o.unpack,
        kr = o.type;
    A.prototype.hsi = function() {
        return sr(this._rgb)
    }, _.hsi = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hsi"])))
    }, b.format.hsi = yr, b.autodetect.push({
        p: 2,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = wr(r, "hsi"), "array" === kr(r) && 3 === r.length) return "hsi"
        }
    });
    var Mr = o.unpack,
        Nr = o.type;
    A.prototype.hsl = function() {
        return E(this._rgb)
    }, _.hsl = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hsl"])))
    }, b.format.hsl = L, b.autodetect.push({
        p: 2,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = Mr(r, "hsl"), "array" === Nr(r) && 3 === r.length) return "hsl"
        }
    });
    var _r = o.unpack,
        xr = Math.min,
        Ar = Math.max,
        Er = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n, t, a, f = (r = _r(r, "rgb"))[0],
                o = r[1],
                u = r[2],
                c = xr(f, o, u),
                i = Ar(f, o, u),
                l = i - c;
            return a = i / 255, 0 === i ? (n = Number.NaN, t = 0) : (t = l / i, f === i && (n = (o - u) / l), o === i && (n = 2 + (u - f) / l), u === i && (n = 4 + (f - o) / l), (n *= 60) < 0 && (n += 360)), [n, t, a]
        },
        Pr = o.unpack,
        Fr = Math.floor,
        Or = function() {
            for (var r, e, n, t, a, f, o = [], u = arguments.length; u--;) o[u] = arguments[u];
            var c, i, l, h = (o = Pr(o, "hsv"))[0],
                d = o[1],
                s = o[2];
            if (s *= 255, 0 === d) c = i = l = s;
            else {
                360 === h && (h = 0), 360 < h && (h -= 360), h < 0 && (h += 360);
                var b = Fr(h /= 60),
                    p = h - b,
                    g = s * (1 - d),
                    v = s * (1 - d * p),
                    m = s * (1 - d * (1 - p));
                switch (b) {
                    case 0:
                        c = (r = [s, m, g])[0], i = r[1], l = r[2];
                        break;
                    case 1:
                        c = (e = [v, s, g])[0], i = e[1], l = e[2];
                        break;
                    case 2:
                        c = (n = [g, s, m])[0], i = n[1], l = n[2];
                        break;
                    case 3:
                        c = (t = [g, v, s])[0], i = t[1], l = t[2];
                        break;
                    case 4:
                        c = (a = [m, g, s])[0], i = a[1], l = a[2];
                        break;
                    case 5:
                        c = (f = [s, g, v])[0], i = f[1], l = f[2]
                }
            }
            return [c, i, l, 3 < o.length ? o[3] : 1]
        },
        jr = o.unpack,
        Gr = o.type;
    A.prototype.hsv = function() {
        return Er(this._rgb)
    }, _.hsv = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hsv"])))
    }, b.format.hsv = Or, b.autodetect.push({
        p: 2,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = jr(r, "hsv"), "array" === Gr(r) && 3 === r.length) return "hsv"
        }
    });
    var qr = 18,
        Lr = .95047,
        Rr = 1,
        Ir = 1.08883,
        Br = .137931034,
        Cr = .206896552,
        Dr = .12841855,
        Sr = .008856452,
        $r = o.unpack,
        Yr = Math.pow,
        zr = function(r) {
            return (r /= 255) <= .04045 ? r / 12.92 : Yr((r + .055) / 1.055, 2.4)
        },
        Tr = function(r) {
            return Sr < r ? Yr(r, 1 / 3) : r / Dr + Br
        },
        Ur = function(r, e, n) {
            return r = zr(r), e = zr(e), n = zr(n), [Tr((.4124564 * r + .3575761 * e + .1804375 * n) / Lr), Tr((.2126729 * r + .7151522 * e + .072175 * n) / Rr), Tr((.0193339 * r + .119192 * e + .9503041 * n) / Ir)]
        },
        Vr = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = $r(r, "rgb"),
                t = n[0],
                a = n[1],
                f = n[2],
                o = Ur(t, a, f),
                u = o[0],
                c = o[1],
                i = 116 * c - 16;
            return [i < 0 ? 0 : i, 500 * (u - c), 200 * (c - o[2])]
        },
        Wr = o.unpack,
        Xr = Math.pow,
        Hr = function(r) {
            return 255 * (r <= .00304 ? 12.92 * r : 1.055 * Xr(r, 1 / 2.4) - .055)
        },
        Jr = function(r) {
            return Cr < r ? r * r * r : Dr * (r - Br)
        },
        Kr = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n, t, a, f = (r = Wr(r, "lab"))[0],
                o = r[1],
                u = r[2];
            return t = (f + 16) / 116, n = isNaN(o) ? t : t + o / 500, a = isNaN(u) ? t : t - u / 200, t = Rr * Jr(t), n = Lr * Jr(n), a = Ir * Jr(a), [Hr(3.2404542 * n - 1.5371385 * t - .4985314 * a), Hr(-.969266 * n + 1.8760108 * t + .041556 * a), Hr(.0556434 * n - .2040259 * t + 1.0572252 * a), 3 < r.length ? r[3] : 1]
        },
        Qr = o.unpack,
        Zr = o.type;
    A.prototype.lab = function() {
        return Vr(this._rgb)
    }, _.lab = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["lab"])))
    }, b.format.lab = Kr, b.autodetect.push({
        p: 2,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = Qr(r, "lab"), "array" === Zr(r) && 3 === r.length) return "lab"
        }
    });
    var re = o.unpack,
        ee = o.RAD2DEG,
        ne = Math.sqrt,
        te = Math.atan2,
        ae = Math.round,
        fe = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = re(r, "lab"),
                t = n[0],
                a = n[1],
                f = n[2],
                o = ne(a * a + f * f),
                u = (te(f, a) * ee + 360) % 360;
            return 0 === ae(1e4 * o) && (u = Number.NaN), [t, o, u]
        },
        oe = o.unpack,
        ue = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = oe(r, "rgb"),
                t = n[0],
                a = n[1],
                f = n[2],
                o = Vr(t, a, f),
                u = o[0],
                c = o[1],
                i = o[2];
            return fe(u, c, i)
        },
        ce = o.unpack,
        ie = o.DEG2RAD,
        le = Math.sin,
        he = Math.cos,
        de = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = ce(r, "lch"),
                t = n[0],
                a = n[1],
                f = n[2];
            return isNaN(f) && (f = 0), [t, he(f *= ie) * a, le(f) * a]
        },
        se = o.unpack,
        be = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = (r = se(r, "lch"))[0],
                t = r[1],
                a = r[2],
                f = de(n, t, a),
                o = f[0],
                u = f[1],
                c = f[2],
                i = Kr(o, u, c);
            return [i[0], i[1], i[2], 3 < r.length ? r[3] : 1]
        },
        pe = o.unpack,
        ge = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = pe(r, "hcl").reverse();
            return be.apply(void 0, n)
        },
        ve = o.unpack,
        me = o.type;
    A.prototype.lch = function() {
        return ue(this._rgb)
    }, A.prototype.hcl = function() {
        return ue(this._rgb).reverse()
    }, _.lch = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["lch"])))
    }, _.hcl = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["hcl"])))
    }, b.format.lch = be, b.format.hcl = ge, ["lch", "hcl"].forEach(function(n) {
        return b.autodetect.push({
            p: 2,
            test: function() {
                for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
                if (r = ve(r, n), "array" === me(r) && 3 === r.length) return n
            }
        })
    });
    var ye = {
            aliceblue: "#f0f8ff",
            antiquewhite: "#faebd7",
            aqua: "#00ffff",
            aquamarine: "#7fffd4",
            azure: "#f0ffff",
            beige: "#f5f5dc",
            bisque: "#ffe4c4",
            black: "#000000",
            blanchedalmond: "#ffebcd",
            blue: "#0000ff",
            blueviolet: "#8a2be2",
            brown: "#a52a2a",
            burlywood: "#deb887",
            cadetblue: "#5f9ea0",
            chartreuse: "#7fff00",
            chocolate: "#d2691e",
            coral: "#ff7f50",
            cornflower: "#6495ed",
            cornflowerblue: "#6495ed",
            cornsilk: "#fff8dc",
            crimson: "#dc143c",
            cyan: "#00ffff",
            darkblue: "#00008b",
            darkcyan: "#008b8b",
            darkgoldenrod: "#b8860b",
            darkgray: "#a9a9a9",
            darkgreen: "#006400",
            darkgrey: "#a9a9a9",
            darkkhaki: "#bdb76b",
            darkmagenta: "#8b008b",
            darkolivegreen: "#556b2f",
            darkorange: "#ff8c00",
            darkorchid: "#9932cc",
            darkred: "#8b0000",
            darksalmon: "#e9967a",
            darkseagreen: "#8fbc8f",
            darkslateblue: "#483d8b",
            darkslategray: "#2f4f4f",
            darkslategrey: "#2f4f4f",
            darkturquoise: "#00ced1",
            darkviolet: "#9400d3",
            deeppink: "#ff1493",
            deepskyblue: "#00bfff",
            dimgray: "#696969",
            dimgrey: "#696969",
            dodgerblue: "#1e90ff",
            firebrick: "#b22222",
            floralwhite: "#fffaf0",
            forestgreen: "#228b22",
            fuchsia: "#ff00ff",
            gainsboro: "#dcdcdc",
            ghostwhite: "#f8f8ff",
            gold: "#ffd700",
            goldenrod: "#daa520",
            gray: "#808080",
            green: "#008000",
            greenyellow: "#adff2f",
            grey: "#808080",
            honeydew: "#f0fff0",
            hotpink: "#ff69b4",
            indianred: "#cd5c5c",
            indigo: "#4b0082",
            ivory: "#fffff0",
            khaki: "#f0e68c",
            laserlemon: "#ffff54",
            lavender: "#e6e6fa",
            lavenderblush: "#fff0f5",
            lawngreen: "#7cfc00",
            lemonchiffon: "#fffacd",
            lightblue: "#add8e6",
            lightcoral: "#f08080",
            lightcyan: "#e0ffff",
            lightgoldenrod: "#fafad2",
            lightgoldenrodyellow: "#fafad2",
            lightgray: "#d3d3d3",
            lightgreen: "#90ee90",
            lightgrey: "#d3d3d3",
            lightpink: "#ffb6c1",
            lightsalmon: "#ffa07a",
            lightseagreen: "#20b2aa",
            lightskyblue: "#87cefa",
            lightslategray: "#778899",
            lightslategrey: "#778899",
            lightsteelblue: "#b0c4de",
            lightyellow: "#ffffe0",
            lime: "#00ff00",
            limegreen: "#32cd32",
            linen: "#faf0e6",
            magenta: "#ff00ff",
            maroon: "#800000",
            maroon2: "#7f0000",
            maroon3: "#b03060",
            mediumaquamarine: "#66cdaa",
            mediumblue: "#0000cd",
            mediumorchid: "#ba55d3",
            mediumpurple: "#9370db",
            mediumseagreen: "#3cb371",
            mediumslateblue: "#7b68ee",
            mediumspringgreen: "#00fa9a",
            mediumturquoise: "#48d1cc",
            mediumvioletred: "#c71585",
            midnightblue: "#191970",
            mintcream: "#f5fffa",
            mistyrose: "#ffe4e1",
            moccasin: "#ffe4b5",
            navajowhite: "#ffdead",
            navy: "#000080",
            oldlace: "#fdf5e6",
            olive: "#808000",
            olivedrab: "#6b8e23",
            orange: "#ffa500",
            orangered: "#ff4500",
            orchid: "#da70d6",
            palegoldenrod: "#eee8aa",
            palegreen: "#98fb98",
            paleturquoise: "#afeeee",
            palevioletred: "#db7093",
            papayawhip: "#ffefd5",
            peachpuff: "#ffdab9",
            peru: "#cd853f",
            pink: "#ffc0cb",
            plum: "#dda0dd",
            powderblue: "#b0e0e6",
            purple: "#800080",
            purple2: "#7f007f",
            purple3: "#a020f0",
            rebeccapurple: "#663399",
            red: "#ff0000",
            rosybrown: "#bc8f8f",
            royalblue: "#4169e1",
            saddlebrown: "#8b4513",
            salmon: "#fa8072",
            sandybrown: "#f4a460",
            seagreen: "#2e8b57",
            seashell: "#fff5ee",
            sienna: "#a0522d",
            silver: "#c0c0c0",
            skyblue: "#87ceeb",
            slateblue: "#6a5acd",
            slategray: "#708090",
            slategrey: "#708090",
            snow: "#fffafa",
            springgreen: "#00ff7f",
            steelblue: "#4682b4",
            tan: "#d2b48c",
            teal: "#008080",
            thistle: "#d8bfd8",
            tomato: "#ff6347",
            turquoise: "#40e0d0",
            violet: "#ee82ee",
            wheat: "#f5deb3",
            white: "#ffffff",
            whitesmoke: "#f5f5f5",
            yellow: "#ffff00",
            yellowgreen: "#9acd32"
        },
        we = o.type;
    A.prototype.name = function() {
        for (var r = tr(this._rgb, "rgb"), e = 0, n = Object.keys(ye); e < n.length; e += 1) {
            var t = n[e];
            if (ye[t] === r) return t.toLowerCase()
        }
        return r
    }, b.format.named = function(r) {
        if (r = r.toLowerCase(), ye[r]) return or(ye[r]);
        throw new Error("unknown color name: " + r)
    }, b.autodetect.push({
        p: 5,
        test: function(r) {
            for (var e = [], n = arguments.length - 1; 0 < n--;) e[n] = arguments[n + 1];
            if (!e.length && "string" === we(r) && ye[r.toLowerCase()]) return "named"
        }
    });
    var ke = o.unpack,
        Me = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            var n = ke(r, "rgb");
            return (n[0] << 16) + (n[1] << 8) + n[2]
        },
        Ne = o.type,
        _e = function(r) {
            if ("number" == Ne(r) && 0 <= r && r <= 16777215) return [r >> 16, r >> 8 & 255, 255 & r, 1];
            throw new Error("unknown num color: " + r)
        },
        xe = o.type;
    A.prototype.num = function() {
        return Me(this._rgb)
    }, _.num = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["num"])))
    }, b.format.num = _e, b.autodetect.push({
        p: 5,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (1 === r.length && "number" === xe(r[0]) && 0 <= r[0] && r[0] <= 16777215) return "num"
        }
    });
    var Ae = o.unpack,
        Ee = o.type,
        Pe = Math.round;
    A.prototype.rgb = function(r) {
        return void 0 === r && (r = !0), !1 === r ? this._rgb.slice(0, 3) : this._rgb.slice(0, 3).map(Pe)
    }, A.prototype.rgba = function(n) {
        return void 0 === n && (n = !0), this._rgb.slice(0, 4).map(function(r, e) {
            return e < 3 ? !1 === n ? r : Pe(r) : r
        })
    }, _.rgb = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["rgb"])))
    }, b.format.rgb = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        var n = Ae(r, "rgba");
        return void 0 === n[3] && (n[3] = 1), n
    }, b.autodetect.push({
        p: 3,
        test: function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            if (r = Ae(r, "rgba"), "array" === Ee(r) && (3 === r.length || 4 === r.length && "number" == Ee(r[3]) && 0 <= r[3] && r[3] <= 1)) return "rgb"
        }
    });
    var Fe = Math.log,
        Oe = function(r) {
            var e, n, t, a = r / 100;
            return t = a < 66 ? (e = 255, n = -155.25485562709179 - .44596950469579133 * (n = a - 2) + 104.49216199393888 * Fe(n), a < 20 ? 0 : .8274096064007395 * (t = a - 10) - 254.76935184120902 + 115.67994401066147 * Fe(t)) : (e = 351.97690566805693 + .114206453784165 * (e = a - 55) - 40.25366309332127 * Fe(e), n = 325.4494125711974 + .07943456536662342 * (n = a - 50) - 28.0852963507957 * Fe(n), 255), [e, n, t, 1]
        },
        je = o.unpack,
        Ge = Math.round,
        qe = function() {
            for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
            for (var n, t = je(r, "rgb"), a = t[0], f = t[2], o = 1e3, u = 4e4; .4 < u - o;) {
                var c = Oe(n = .5 * (u + o));
                c[2] / c[0] >= f / a ? u = n : o = n
            }
            return Ge(n)
        };
    A.prototype.temp = A.prototype.kelvin = A.prototype.temperature = function() {
        return qe(this._rgb)
    }, _.temp = _.kelvin = _.temperature = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        return new(Function.prototype.bind.apply(A, [null].concat(r, ["temp"])))
    }, b.format.temp = b.format.kelvin = b.format.temperature = Oe;
    var Le = o.type;
    A.prototype.alpha = function(r, e) {
        return void 0 === e && (e = !1), void 0 !== r && "number" === Le(r) ? e ? (this._rgb[3] = r, this) : new A([this._rgb[0], this._rgb[1], this._rgb[2], r], "rgb") : this._rgb[3]
    }, A.prototype.clipped = function() {
        return this._rgb._clipped || !1
    }, A.prototype.darken = function(r) {
        void 0 === r && (r = 1);
        var e = this.lab();
        return e[0] -= qr * r, new A(e, "lab").alpha(this.alpha(), !0)
    }, A.prototype.brighten = function(r) {
        return void 0 === r && (r = 1), this.darken(-r)
    }, A.prototype.darker = A.prototype.darken, A.prototype.brighter = A.prototype.brighten, A.prototype.get = function(r) {
        var e = r.split("."),
            n = e[0],
            t = e[1],
            a = this[n]();
        if (t) {
            var f = n.indexOf(t);
            if (-1 < f) return a[f];
            throw new Error("unknown channel " + t + " in mode " + n)
        }
        return a
    };
    var Re = o.type,
        Ie = Math.pow;
    A.prototype.luminance = function(a) {
        if (void 0 === a || "number" !== Re(a)) return Be.apply(void 0, this._rgb.slice(0, 3));
        if (0 === a) return new A([0, 0, 0, this._rgb[3]], "rgb");
        if (1 === a) return new A([255, 255, 255, this._rgb[3]], "rgb");
        var r = this.luminance(),
            f = 20,
            o = function(r, e) {
                var n = r.interpolate(e, .5, "rgb"),
                    t = n.luminance();
                return Math.abs(a - t) < 1e-7 || !f-- ? n : a < t ? o(r, n) : o(n, e)
            },
            e = (a < r ? o(new A([0, 0, 0]), this) : o(this, new A([255, 255, 255]))).rgb();
        return new A(e.concat([this._rgb[3]]))
    };
    var Be = function(r, e, n) {
            return .2126 * (r = Ce(r)) + .7152 * (e = Ce(e)) + .0722 * (n = Ce(n))
        },
        Ce = function(r) {
            return (r /= 255) <= .03928 ? r / 12.92 : Ie((r + .055) / 1.055, 2.4)
        },
        De = {},
        Se = o.type,
        $e = function(r, e, n) {
            void 0 === n && (n = .5);
            for (var t = [], a = arguments.length - 3; 0 < a--;) t[a] = arguments[a + 3];
            var f = t[0] || "lrgb";
            if (De[f] || t.length || (f = Object.keys(De)[0]), !De[f]) throw new Error("interpolation mode " + f + " is not defined");
            return "object" !== Se(r) && (r = new A(r)), "object" !== Se(e) && (e = new A(e)), De[f](r, e, n).alpha(r.alpha() + n * (e.alpha() - r.alpha()))
        };
    A.prototype.mix = A.prototype.interpolate = function(r, e) {
        void 0 === e && (e = .5);
        for (var n = [], t = arguments.length - 2; 0 < t--;) n[t] = arguments[t + 2];
        return $e.apply(void 0, [this, r, e].concat(n))
    }, A.prototype.premultiply = function(r) {
        void 0 === r && (r = !1);
        var e = this._rgb,
            n = e[3];
        return r ? (this._rgb = [e[0] * n, e[1] * n, e[2] * n, n], this) : new A([e[0] * n, e[1] * n, e[2] * n, n], "rgb")
    }, A.prototype.saturate = function(r) {
        void 0 === r && (r = 1);
        var e = this.lch();
        return e[1] += qr * r, e[1] < 0 && (e[1] = 0), new A(e, "lch").alpha(this.alpha(), !0)
    }, A.prototype.desaturate = function(r) {
        return void 0 === r && (r = 1), this.saturate(-r)
    };
    var Ye = o.type;
    A.prototype.set = function(r, e, n) {
        void 0 === n && (n = !1);
        var t = r.split("."),
            a = t[0],
            f = t[1],
            o = this[a]();
        if (f) {
            var u = a.indexOf(f);
            if (-1 < u) {
                if ("string" == Ye(e)) switch (e.charAt(0)) {
                    case "+":
                    case "-":
                        o[u] += +e;
                        break;
                    case "*":
                        o[u] *= +e.substr(1);
                        break;
                    case "/":
                        o[u] /= +e.substr(1);
                        break;
                    default:
                        o[u] = +e
                } else {
                    if ("number" !== Ye(e)) throw new Error("unsupported value for Color.set");
                    o[u] = e
                }
                var c = new A(o, a);
                return n ? (this._rgb = c._rgb, this) : c
            }
            throw new Error("unknown channel " + f + " in mode " + a)
        }
        return o
    };
    De.rgb = function(r, e, n) {
        var t = r._rgb,
            a = e._rgb;
        return new A(t[0] + n * (a[0] - t[0]), t[1] + n * (a[1] - t[1]), t[2] + n * (a[2] - t[2]), "rgb")
    };
    var ze = Math.sqrt,
        Te = Math.pow;
    De.lrgb = function(r, e, n) {
        var t = r._rgb,
            a = t[0],
            f = t[1],
            o = t[2],
            u = e._rgb,
            c = u[0],
            i = u[1],
            l = u[2];
        return new A(ze(Te(a, 2) * (1 - n) + Te(c, 2) * n), ze(Te(f, 2) * (1 - n) + Te(i, 2) * n), ze(Te(o, 2) * (1 - n) + Te(l, 2) * n), "rgb")
    };
    De.lab = function(r, e, n) {
        var t = r.lab(),
            a = e.lab();
        return new A(t[0] + n * (a[0] - t[0]), t[1] + n * (a[1] - t[1]), t[2] + n * (a[2] - t[2]), "lab")
    };
    var Ue = function(r, e, n, t) {
            var a, f, o, u, c, i, l, h, d, s, b, p;
            return "hsl" === t ? (o = r.hsl(), u = e.hsl()) : "hsv" === t ? (o = r.hsv(), u = e.hsv()) : "hcg" === t ? (o = r.hcg(), u = e.hcg()) : "hsi" === t ? (o = r.hsi(), u = e.hsi()) : "lch" !== t && "hcl" !== t || (t = "hcl", o = r.hcl(), u = e.hcl()), "h" === t.substr(0, 1) && (c = (a = o)[0], l = a[1], d = a[2], i = (f = u)[0], h = f[1], s = f[2]), isNaN(c) || isNaN(i) ? isNaN(c) ? isNaN(i) ? p = Number.NaN : (p = i, 1 != d && 0 != d || "hsv" == t || (b = h)) : (p = c, 1 != s && 0 != s || "hsv" == t || (b = l)) : p = c + n * (c < i && 180 < i - c ? i - (c + 360) : i < c && 180 < c - i ? i + 360 - c : i - c), void 0 === b && (b = l + n * (h - l)), new A([p, b, d + n * (s - d)], t)
        },
        Ve = function(r, e, n) {
            return Ue(r, e, n, "lch")
        };
    De.lch = Ve, De.hcl = Ve;
    De.num = function(r, e, n) {
        var t = r.num(),
            a = e.num();
        return new A(t + n * (a - t), "num")
    };
    De.hcg = function(r, e, n) {
        return Ue(r, e, n, "hcg")
    };
    De.hsi = function(r, e, n) {
        return Ue(r, e, n, "hsi")
    };
    De.hsl = function(r, e, n) {
        return Ue(r, e, n, "hsl")
    };
    De.hsv = function(r, e, n) {
        return Ue(r, e, n, "hsv")
    };
    var We = o.clip_rgb,
        Xe = Math.pow,
        He = Math.sqrt,
        Je = Math.PI,
        Ke = Math.cos,
        Qe = Math.sin,
        Ze = Math.atan2,
        rn = function(r, e) {
            for (var n = r.length, t = [0, 0, 0, 0], a = 0; a < r.length; a++) {
                var f = r[a],
                    o = e[a] / n,
                    u = f._rgb;
                t[0] += Xe(u[0], 2) * o, t[1] += Xe(u[1], 2) * o, t[2] += Xe(u[2], 2) * o, t[3] += u[3] * o
            }
            return t[0] = He(t[0]), t[1] = He(t[1]), t[2] = He(t[2]), .9999999 < t[3] && (t[3] = 1), new A(We(t))
        },
        en = o.type,
        nn = Math.pow,
        tn = function(i) {
            var u = "rgb",
                c = _("#ccc"),
                e = 0,
                l = [0, 1],
                h = [],
                d = [0, 0],
                s = !1,
                b = [],
                n = !1,
                p = 0,
                g = 1,
                t = !1,
                v = {},
                m = !0,
                y = 1,
                a = function(r) {
                    if ((r = r || ["#fff", "#000"]) && "string" === en(r) && _.brewer && _.brewer[r.toLowerCase()] && (r = _.brewer[r.toLowerCase()]), "array" === en(r)) {
                        1 === r.length && (r = [r[0], r[0]]), r = r.slice(0);
                        for (var e = 0; e < r.length; e++) r[e] = _(r[e]);
                        for (var n = h.length = 0; n < r.length; n++) h.push(n / (r.length - 1))
                    }
                    return f(), b = r
                },
                w = function(r) {
                    return r
                },
                k = function(r) {
                    return r
                },
                M = function(r, e) {
                    var n, t;
                    if (null == e && (e = !1), isNaN(r) || null === r) return c;
                    e ? t = r : t = s && 2 < s.length ? function(r) {
                        if (null == s) return 0;
                        for (var e = s.length - 1, n = 0; n < e && r >= s[n];) n++;
                        return n - 1
                    }(r) / (s.length - 2) : g !== p ? (r - p) / (g - p) : 1;
                    t = k(t), e || (t = w(t)), 1 !== y && (t = nn(t, y)), t = d[0] + t * (1 - d[0] - d[1]), t = Math.min(1, Math.max(0, t));
                    var a = Math.floor(1e4 * t);
                    if (m && v[a]) n = v[a];
                    else {
                        if ("array" === en(b))
                            for (var f = 0; f < h.length; f++) {
                                var o = h[f];
                                if (t <= o) {
                                    n = b[f];
                                    break
                                }
                                if (o <= t && f === h.length - 1) {
                                    n = b[f];
                                    break
                                }
                                if (o < t && t < h[f + 1]) {
                                    t = (t - o) / (h[f + 1] - o), n = _.interpolate(b[f], b[f + 1], t, u);
                                    break
                                }
                            } else "function" === en(b) && (n = b(t));
                        m && (v[a] = n)
                    }
                    return n
                },
                f = function() {
                    return v = {}
                };
            a(i);
            var N = function(r) {
                var e = _(M(r));
                return n && e[n] ? e[n]() : e
            };
            return N.classes = function(r) {
                if (null == r) return s;
                if ("array" === en(r)) l = [(s = r)[0], r[r.length - 1]];
                else {
                    var e = _.analyze(l);
                    s = 0 === r ? [e.min, e.max] : _.limits(e, "e", r)
                }
                return N
            }, N.domain = function(n) {
                if (!arguments.length) return l;
                p = n[0], g = n[n.length - 1], h = [];
                var r = b.length;
                if (n.length === r && p !== g)
                    for (var e = 0, t = Array.from(n); e < t.length; e += 1) {
                        var a = t[e];
                        h.push((a - p) / (g - p))
                    } else {
                        for (var f = 0; f < r; f++) h.push(f / (r - 1));
                        if (2 < n.length) {
                            var o = n.map(function(r, e) {
                                    return e / (n.length - 1)
                                }),
                                u = n.map(function(r) {
                                    return (r - p) / (g - p)
                                });
                            u.every(function(r, e) {
                                return o[e] === r
                            }) || (k = function(r) {
                                if (r <= 0 || 1 <= r) return r;
                                for (var e = 0; r >= u[e + 1];) e++;
                                var n = (r - u[e]) / (u[e + 1] - u[e]);
                                return o[e] + n * (o[e + 1] - o[e])
                            })
                        }
                    }
                return l = [p, g], N
            }, N.mode = function(r) {
                return arguments.length ? (u = r, f(), N) : u
            }, N.range = function(r, e) {
                return a(r), N
            }, N.out = function(r) {
                return n = r, N
            }, N.spread = function(r) {
                return arguments.length ? (e = r, N) : e
            }, N.correctLightness = function(r) {
                return null == r && (r = !0), t = r, f(), w = t ? function(r) {
                    for (var e = M(0, !0).lab()[0], n = M(1, !0).lab()[0], t = n < e, a = M(r, !0).lab()[0], f = e + (n - e) * r, o = a - f, u = 0, c = 1, i = 20; .01 < Math.abs(o) && 0 < i--;) t && (o *= -1), r += o < 0 ? .5 * (c - (u = r)) : .5 * (u - (c = r)), a = M(r, !0).lab()[0], o = a - f;
                    return r
                } : function(r) {
                    return r
                }, N
            }, N.padding = function(r) {
                return null != r ? ("number" === en(r) && (r = [r, r]), d = r, N) : d
            }, N.colors = function(e, n) {
                arguments.length < 2 && (n = "hex");
                var r = [];
                if (0 === arguments.length) r = b.slice(0);
                else if (1 === e) r = [N(.5)];
                else if (1 < e) {
                    var t = l[0],
                        a = l[1] - t;
                    r = function(r, e, n) {
                        for (var t = [], a = r < e, f = n ? a ? e + 1 : e - 1 : e, o = r; a ? o < f : f < o; a ? o++ : o--) t.push(o);
                        return t
                    }(0, e, !1).map(function(r) {
                        return N(t + r / (e - 1) * a)
                    })
                } else {
                    i = [];
                    var f = [];
                    if (s && 2 < s.length)
                        for (var o = 1, u = s.length, c = 1 <= u; c ? o < u : u < o; c ? o++ : o--) f.push(.5 * (s[o - 1] + s[o]));
                    else f = l;
                    r = f.map(function(r) {
                        return N(r)
                    })
                }
                return _[n] && (r = r.map(function(r) {
                    return r[n]()
                })), r
            }, N.cache = function(r) {
                return null != r ? (m = r, N) : m
            }, N.gamma = function(r) {
                return null != r ? (y = r, N) : y
            }, N.nodata = function(r) {
                return null != r ? (c = _(r), N) : c
            }, N
        };
    var an = function(r) {
            var e, n, t, a, f, o, u;
            if (2 === (r = r.map(function(r) {
                    return new A(r)
                })).length) e = r.map(function(r) {
                return r.lab()
            }), f = e[0], o = e[1], a = function(e) {
                var r = [0, 1, 2].map(function(r) {
                    return f[r] + e * (o[r] - f[r])
                });
                return new A(r, "lab")
            };
            else if (3 === r.length) n = r.map(function(r) {
                return r.lab()
            }), f = n[0], o = n[1], u = n[2], a = function(e) {
                var r = [0, 1, 2].map(function(r) {
                    return (1 - e) * (1 - e) * f[r] + 2 * (1 - e) * e * o[r] + e * e * u[r]
                });
                return new A(r, "lab")
            };
            else if (4 === r.length) {
                var c;
                t = r.map(function(r) {
                    return r.lab()
                }), f = t[0], o = t[1], u = t[2], c = t[3], a = function(e) {
                    var r = [0, 1, 2].map(function(r) {
                        return (1 - e) * (1 - e) * (1 - e) * f[r] + 3 * (1 - e) * (1 - e) * e * o[r] + 3 * (1 - e) * e * e * u[r] + e * e * e * c[r]
                    });
                    return new A(r, "lab")
                }
            } else if (5 === r.length) {
                var i = an(r.slice(0, 3)),
                    l = an(r.slice(2, 5));
                a = function(r) {
                    return r < .5 ? i(2 * r) : l(2 * (r - .5))
                }
            }
            return a
        },
        fn = function(r, e, n) {
            if (!fn[n]) throw new Error("unknown blend mode " + n);
            return fn[n](r, e)
        },
        on = function(a) {
            return function(r, e) {
                var n = _(e).rgb(),
                    t = _(r).rgb();
                return _.rgb(a(n, t))
            }
        },
        un = function(t) {
            return function(r, e) {
                var n = [];
                return n[0] = t(r[0], e[0]), n[1] = t(r[1], e[1]), n[2] = t(r[2], e[2]), n
            }
        };
    fn.normal = on(un(function(r) {
        return r
    })), fn.multiply = on(un(function(r, e) {
        return r * e / 255
    })), fn.screen = on(un(function(r, e) {
        return 255 * (1 - (1 - r / 255) * (1 - e / 255))
    })), fn.overlay = on(un(function(r, e) {
        return e < 128 ? 2 * r * e / 255 : 255 * (1 - 2 * (1 - r / 255) * (1 - e / 255))
    })), fn.darken = on(un(function(r, e) {
        return e < r ? e : r
    })), fn.lighten = on(un(function(r, e) {
        return e < r ? r : e
    })), fn.dodge = on(un(function(r, e) {
        return 255 === r ? 255 : 255 < (r = e / 255 * 255 / (1 - r / 255)) ? 255 : r
    })), fn.burn = on(un(function(r, e) {
        return 255 * (1 - (1 - e / 255) / (r / 255))
    }));
    for (var cn = fn, ln = o.type, hn = o.clip_rgb, dn = o.TWOPI, sn = Math.pow, bn = Math.sin, pn = Math.cos, gn = Math.floor, vn = Math.random, mn = Math.log, yn = Math.pow, wn = Math.floor, kn = Math.abs, Mn = function(r, e) {
            void 0 === e && (e = null);
            var n = {
                min: Number.MAX_VALUE,
                max: -1 * Number.MAX_VALUE,
                sum: 0,
                values: [],
                count: 0
            };
            return "object" === Y(r) && (r = Object.values(r)), r.forEach(function(r) {
                e && "object" === Y(r) && (r = r[e]), null == r || isNaN(r) || (n.values.push(r), n.sum += r, r < n.min && (n.min = r), r > n.max && (n.max = r), n.count += 1)
            }), n.domain = [n.min, n.max], n.limits = function(r, e) {
                return Nn(n, r, e)
            }, n
        }, Nn = function(r, e, n) {
            void 0 === e && (e = "equal"), void 0 === n && (n = 7), "array" == Y(r) && (r = Mn(r));
            var t = r.min,
                a = r.max,
                f = r.values.sort(function(r, e) {
                    return r - e
                });
            if (1 === n) return [t, a];
            var o = [];
            if ("c" === e.substr(0, 1) && (o.push(t), o.push(a)), "e" === e.substr(0, 1)) {
                o.push(t);
                for (var u = 1; u < n; u++) o.push(t + u / n * (a - t));
                o.push(a)
            } else if ("l" === e.substr(0, 1)) {
                if (t <= 0) throw new Error("Logarithmic scales are only possible for values > 0");
                var c = Math.LOG10E * mn(t),
                    i = Math.LOG10E * mn(a);
                o.push(t);
                for (var l = 1; l < n; l++) o.push(yn(10, c + l / n * (i - c)));
                o.push(a)
            } else if ("q" === e.substr(0, 1)) {
                o.push(t);
                for (var h = 1; h < n; h++) {
                    var d = (f.length - 1) * h / n,
                        s = wn(d);
                    if (s === d) o.push(f[s]);
                    else {
                        var b = d - s;
                        o.push(f[s] * (1 - b) + f[s + 1] * b)
                    }
                }
                o.push(a)
            } else if ("k" === e.substr(0, 1)) {
                var p, g = f.length,
                    v = new Array(g),
                    m = new Array(n),
                    y = !0,
                    w = 0,
                    k = null;
                (k = []).push(t);
                for (var M = 1; M < n; M++) k.push(t + M / n * (a - t));
                for (k.push(a); y;) {
                    for (var N = 0; N < n; N++) m[N] = 0;
                    for (var _ = 0; _ < g; _++)
                        for (var x = f[_], A = Number.MAX_VALUE, E = void 0, P = 0; P < n; P++) {
                            var F = kn(k[P] - x);
                            F < A && (A = F, E = P), m[E]++, v[_] = E
                        }
                    for (var O = new Array(n), j = 0; j < n; j++) O[j] = null;
                    for (var G = 0; G < g; G++) null === O[p = v[G]] ? O[p] = f[G] : O[p] += f[G];
                    for (var q = 0; q < n; q++) O[q] *= 1 / m[q];
                    y = !1;
                    for (var L = 0; L < n; L++)
                        if (O[L] !== k[L]) {
                            y = !0;
                            break
                        } k = O, 200 < ++w && (y = !1)
                }
                for (var R = {}, I = 0; I < n; I++) R[I] = [];
                for (var B = 0; B < g; B++) R[p = v[B]].push(f[B]);
                for (var C = [], D = 0; D < n; D++) C.push(R[D][0]), C.push(R[D][R[D].length - 1]);
                C = C.sort(function(r, e) {
                    return r - e
                }), o.push(C[0]);
                for (var S = 1; S < C.length; S += 2) {
                    var $ = C[S];
                    isNaN($) || -1 !== o.indexOf($) || o.push($)
                }
            }
            return o
        }, _n = {
            analyze: Mn,
            limits: Nn
        }, xn = Math.sqrt, An = Math.atan2, En = Math.abs, Pn = Math.cos, Fn = Math.PI, On = {
            cool: function() {
                return tn([_.hsl(180, 1, .9), _.hsl(250, .7, .4)])
            },
            hot: function() {
                return tn(["#000", "#f00", "#ff0", "#fff"]).mode("rgb")
            }
        }, jn = {
            OrRd: ["#fff7ec", "#fee8c8", "#fdd49e", "#fdbb84", "#fc8d59", "#ef6548", "#d7301f", "#b30000", "#7f0000"],
            PuBu: ["#fff7fb", "#ece7f2", "#d0d1e6", "#a6bddb", "#74a9cf", "#3690c0", "#0570b0", "#045a8d", "#023858"],
            BuPu: ["#f7fcfd", "#e0ecf4", "#bfd3e6", "#9ebcda", "#8c96c6", "#8c6bb1", "#88419d", "#810f7c", "#4d004b"],
            Oranges: ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"],
            BuGn: ["#f7fcfd", "#e5f5f9", "#ccece6", "#99d8c9", "#66c2a4", "#41ae76", "#238b45", "#006d2c", "#00441b"],
            YlOrBr: ["#ffffe5", "#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02", "#993404", "#662506"],
            YlGn: ["#ffffe5", "#f7fcb9", "#d9f0a3", "#addd8e", "#78c679", "#41ab5d", "#238443", "#006837", "#004529"],
            Reds: ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],
            RdPu: ["#fff7f3", "#fde0dd", "#fcc5c0", "#fa9fb5", "#f768a1", "#dd3497", "#ae017e", "#7a0177", "#49006a"],
            Greens: ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"],
            YlGnBu: ["#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494", "#081d58"],
            Purples: ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#54278f", "#3f007d"],
            GnBu: ["#f7fcf0", "#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081"],
            Greys: ["#ffffff", "#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373", "#525252", "#252525", "#000000"],
            YlOrRd: ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c", "#fc4e2a", "#e31a1c", "#bd0026", "#800026"],
            PuRd: ["#f7f4f9", "#e7e1ef", "#d4b9da", "#c994c7", "#df65b0", "#e7298a", "#ce1256", "#980043", "#67001f"],
            Blues: ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"],
            PuBuGn: ["#fff7fb", "#ece2f0", "#d0d1e6", "#a6bddb", "#67a9cf", "#3690c0", "#02818a", "#016c59", "#014636"],
            Viridis: ["#440154", "#482777", "#3f4a8a", "#31678e", "#26838f", "#1f9d8a", "#6cce5a", "#b6de2b", "#fee825"],
            Spectral: ["#9e0142", "#d53e4f", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#e6f598", "#abdda4", "#66c2a5", "#3288bd", "#5e4fa2"],
            RdYlGn: ["#a50026", "#d73027", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#d9ef8b", "#a6d96a", "#66bd63", "#1a9850", "#006837"],
            RdBu: ["#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#f7f7f7", "#d1e5f0", "#92c5de", "#4393c3", "#2166ac", "#053061"],
            PiYG: ["#8e0152", "#c51b7d", "#de77ae", "#f1b6da", "#fde0ef", "#f7f7f7", "#e6f5d0", "#b8e186", "#7fbc41", "#4d9221", "#276419"],
            PRGn: ["#40004b", "#762a83", "#9970ab", "#c2a5cf", "#e7d4e8", "#f7f7f7", "#d9f0d3", "#a6dba0", "#5aae61", "#1b7837", "#00441b"],
            RdYlBu: ["#a50026", "#d73027", "#f46d43", "#fdae61", "#fee090", "#ffffbf", "#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#313695"],
            BrBG: ["#543005", "#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#f5f5f5", "#c7eae5", "#80cdc1", "#35978f", "#01665e", "#003c30"],
            RdGy: ["#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#ffffff", "#e0e0e0", "#bababa", "#878787", "#4d4d4d", "#1a1a1a"],
            PuOr: ["#7f3b08", "#b35806", "#e08214", "#fdb863", "#fee0b6", "#f7f7f7", "#d8daeb", "#b2abd2", "#8073ac", "#542788", "#2d004b"],
            Set2: ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"],
            Accent: ["#7fc97f", "#beaed4", "#fdc086", "#ffff99", "#386cb0", "#f0027f", "#bf5b17", "#666666"],
            Set1: ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"],
            Set3: ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"],
            Dark2: ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666"],
            Paired: ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"],
            Pastel2: ["#b3e2cd", "#fdcdac", "#cbd5e8", "#f4cae4", "#e6f5c9", "#fff2ae", "#f1e2cc", "#cccccc"],
            Pastel1: ["#fbb4ae", "#b3cde3", "#ccebc5", "#decbe4", "#fed9a6", "#ffffcc", "#e5d8bd", "#fddaec", "#f2f2f2"]
        }, Gn = 0, qn = Object.keys(jn); Gn < qn.length; Gn += 1) {
        var Ln = qn[Gn];
        jn[Ln.toLowerCase()] = jn[Ln]
    }
    var Rn = jn;
    return _.average = function(r, f, o) {
        void 0 === f && (f = "lrgb"), void 0 === o && (o = null);
        var e = r.length;
        o || (o = Array.from(new Array(e)).map(function() {
            return 1
        }));
        var n = e / o.reduce(function(r, e) {
            return r + e
        });
        if (o.forEach(function(r, e) {
                o[e] *= n
            }), r = r.map(function(r) {
                return new A(r)
            }), "lrgb" === f) return rn(r, o);
        for (var t = r.shift(), u = t.get(f), c = [], i = 0, l = 0, a = 0; a < u.length; a++)
            if (u[a] = (u[a] || 0) * o[0], c.push(isNaN(u[a]) ? 0 : o[0]), "h" === f.charAt(a) && !isNaN(u[a])) {
                var h = u[a] / 180 * Je;
                i += Ke(h) * o[0], l += Qe(h) * o[0]
            } var d = t.alpha() * o[0];
        r.forEach(function(r, e) {
            var n = r.get(f);
            d += r.alpha() * o[e + 1];
            for (var t = 0; t < u.length; t++)
                if (!isNaN(n[t]))
                    if (c[t] += o[e + 1], "h" === f.charAt(t)) {
                        var a = n[t] / 180 * Je;
                        i += Ke(a) * o[e + 1], l += Qe(a) * o[e + 1]
                    } else u[t] += n[t] * o[e + 1]
        });
        for (var s = 0; s < u.length; s++)
            if ("h" === f.charAt(s)) {
                for (var b = Ze(l / c[s], i / c[s]) / Je * 180; b < 0;) b += 360;
                for (; 360 <= b;) b -= 360;
                u[s] = b
            } else u[s] = u[s] / c[s];
        return d /= e, new A(u, f).alpha(.99999 < d ? 1 : d, !0)
    }, _.bezier = function(r) {
        var e = an(r);
        return e.scale = function() {
            return tn(e)
        }, e
    }, _.blend = cn, _.cubehelix = function(o, u, c, i, l) {
        void 0 === o && (o = 300), void 0 === u && (u = -1.5), void 0 === c && (c = 1), void 0 === i && (i = 1), void 0 === l && (l = [0, 1]);
        var h, d = 0;
        "array" === ln(l) ? h = l[1] - l[0] : (h = 0, l = [l, l]);
        var e = function(r) {
            var e = dn * ((o + 120) / 360 + u * r),
                n = sn(l[0] + h * r, i),
                t = (0 !== d ? c[0] + r * d : c) * n * (1 - n) / 2,
                a = pn(e),
                f = bn(e);
            return _(hn([255 * (n + t * (-.14861 * a + 1.78277 * f)), 255 * (n + t * (-.29227 * a - .90649 * f)), 255 * (n + t * (1.97294 * a)), 1]))
        };
        return e.start = function(r) {
            return null == r ? o : (o = r, e)
        }, e.rotations = function(r) {
            return null == r ? u : (u = r, e)
        }, e.gamma = function(r) {
            return null == r ? i : (i = r, e)
        }, e.hue = function(r) {
            return null == r ? c : ("array" === ln(c = r) ? 0 == (d = c[1] - c[0]) && (c = c[1]) : d = 0, e)
        }, e.lightness = function(r) {
            return null == r ? l : (h = "array" === ln(r) ? (l = r)[1] - r[0] : (l = [r, r], 0), e)
        }, e.scale = function() {
            return _.scale(e)
        }, e.hue(c), e
    }, _.mix = _.interpolate = $e, _.random = function() {
        for (var r = "#", e = 0; e < 6; e++) r += "0123456789abcdef".charAt(gn(16 * vn()));
        return new A(r, "hex")
    }, _.scale = tn, _.analyze = _n.analyze, _.contrast = function(r, e) {
        r = new A(r), e = new A(e);
        var n = r.luminance(),
            t = e.luminance();
        return t < n ? (n + .05) / (t + .05) : (t + .05) / (n + .05)
    }, _.deltaE = function(r, e, n, t) {
        void 0 === n && (n = 1), void 0 === t && (t = 1), r = new A(r), e = new A(e);
        for (var a = Array.from(r.lab()), f = a[0], o = a[1], u = a[2], c = Array.from(e.lab()), i = c[0], l = c[1], h = c[2], d = xn(o * o + u * u), s = xn(l * l + h * h), b = f < 16 ? .511 : .040975 * f / (1 + .01765 * f), p = .0638 * d / (1 + .0131 * d) + .638, g = d < 1e-6 ? 0 : 180 * An(u, o) / Fn; g < 0;) g += 360;
        for (; 360 <= g;) g -= 360;
        var v = 164 <= g && g <= 345 ? .56 + En(.2 * Pn(Fn * (g + 168) / 180)) : .36 + En(.4 * Pn(Fn * (g + 35) / 180)),
            m = d * d * d * d,
            y = xn(m / (m + 1900)),
            w = p * (y * v + 1 - y),
            k = d - s,
            M = o - l,
            N = u - h,
            _ = (f - i) / (n * b),
            x = k / (t * p);
        return xn(_ * _ + x * x + (M * M + N * N - k * k) / (w * w))
    }, _.distance = function(r, e, n) {
        void 0 === n && (n = "lab"), r = new A(r), e = new A(e);
        var t = r.get(n),
            a = e.get(n),
            f = 0;
        for (var o in t) {
            var u = (t[o] || 0) - (a[o] || 0);
            f += u * u
        }
        return Math.sqrt(f)
    }, _.limits = _n.limits, _.valid = function() {
        for (var r = [], e = arguments.length; e--;) r[e] = arguments[e];
        try {
            return new(Function.prototype.bind.apply(A, [null].concat(r))), !0
        } catch (r) {
            return !1
        }
    }, _.scales = On, _.colors = ye, _.brewer = Rn, _
});
