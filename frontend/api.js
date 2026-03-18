// ============================================================
//  FiberNest – Shared API Config & Utilities
//  All pages load this script before their own React code.
// ============================================================

const API_BASE = "http://127.0.0.1:8000"; // ← change to your FastAPI URL

const Api = {
  // ── Auth helpers ────────────────────────────────────────
  getToken: () => localStorage.getItem("fn_token"),
  setToken: (t) => localStorage.setItem("fn_token", t),
  clearToken: () => localStorage.removeItem("fn_token"),
  getUser: () => {
    try { return JSON.parse(localStorage.getItem("fn_user") || "null"); }
    catch { return null; }
  },
  setUser: (u) => localStorage.setItem("fn_user", JSON.stringify(u)),
  clearUser: () => localStorage.removeItem("fn_user"),
  isLoggedIn: () => !!localStorage.getItem("fn_token"),
  isSeller: () => {
    const u = Api.getUser();
    return u && u.role === "seller";
  },

  // ── Base fetch ───────────────────────────────────────────
  async request(path, options = {}) {
    const token = Api.getToken();
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (token) headers["Authorization"] = `Bearer ${token}`;
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (res.status === 401) { Api.clearToken(); Api.clearUser(); window.location.href = "../buyer/login.html"; }
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Request failed");
    return data;
  },

  get:    (path)         => Api.request(path, { method: "GET" }),
  post:   (path, body)   => Api.request(path, { method: "POST",   body: JSON.stringify(body) }),
  put:    (path, body)   => Api.request(path, { method: "PUT",    body: JSON.stringify(body) }),
  delete: (path)         => Api.request(path, { method: "DELETE" }),
  patch:  (path, body)   => Api.request(path, { method: "PATCH",  body: JSON.stringify(body) }),

  // ── Cart (local cache) ───────────────────────────────────
  cart: {
    get: () => { try { return JSON.parse(localStorage.getItem("fn_cart") || "[]"); } catch { return []; } },
    save: (items) => localStorage.setItem("fn_cart", JSON.stringify(items)),
    add: (product, qty = 1) => {
      const cart = Api.cart.get();
      const idx = cart.findIndex(i => i.product_id === product.id);
      if (idx > -1) cart[idx].quantity += qty;
      else cart.push({ product_id: product.id, name: product.name, price: product.price, image: product.image, quantity: qty });
      Api.cart.save(cart); return cart;
    },
    remove: (productId) => { const c = Api.cart.get().filter(i => i.product_id !== productId); Api.cart.save(c); return c; },
    clear: () => localStorage.removeItem("fn_cart"),
    count: () => Api.cart.get().reduce((s, i) => s + i.quantity, 0),
    total: () => Api.cart.get().reduce((s, i) => s + i.price * i.quantity, 0),
  },

  // ── Nav redirect helpers ─────────────────────────────────
  requireAuth: () => { if (!Api.isLoggedIn()) { window.location.href = "../buyer/login.html"; return false; } return true; },
  requireSeller: () => { if (!Api.isSeller()) { window.location.href = "../seller/seller-login.html"; return false; } return true; },
};
