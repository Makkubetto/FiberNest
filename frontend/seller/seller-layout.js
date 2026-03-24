// ============================================================
//  FiberNest – Seller Shared Layout
//  Include AFTER api.js on every seller page.
//  Exposes: SellerLayout component
// ============================================================

// Tailwind config (shared) – applied by individual pages
const SELLER_NAV = [
  { label:"Dashboard",   href:"seller-dashboard.html",  icon:"📊" },
  { label:"Storefront",  href:"seller-storefront.html",  icon:"🏪" },
  { label:"Inventory",   href:"seller-inventory.html",   icon:"📦" },
  { label:"Reports",     href:"seller-reports.html",     icon:"📈" },
];

function SellerLayout({ children, active }) {
  const [sideOpen, setSideOpen] = React.useState(false);
  const user = Api.getUser();

  React.useEffect(() => {
    if (!Api.isLoggedIn() || !Api.isSeller()) {
      window.location.href = "seller-login.html";
    }
  }, []);

  const logout = () => { Api.clearToken(); Api.clearUser(); window.location.href = "seller-login.html"; };

  return (
    <div className="flex min-h-screen bg-stone-50 font-sans">
      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-40 w-60 bg-gray-900 flex flex-col transition-transform duration-300 ${sideOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}`}>
        <div className="p-5 border-b border-white/10">
          <a href="seller-dashboard.html" className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-white/10 backdrop-blur-md rounded-xl flex items-center justify-center border border-white/20 shadow-sm">
              <img src="../assets/img/logo.png" className="w-7 h-7 object-contain" />
            </div>
            <div>
              <p className="font-display font-bold text-white text-base leading-none">FiberNest</p>
              <p className="text-[10px] text-gray-400 uppercase tracking-wider mt-0.5">Seller Dashboard</p>
            </div>
          </a>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {SELLER_NAV.map(item => (
            <a key={item.href} href={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                active === item.label
                  ? "bg-sage text-white"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}>
              <span className="text-base">{item.icon}</span>{item.label}
            </a>
          ))}
        </nav>
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center gap-3 mb-3 px-2">
            <div className="w-8 h-8 bg-sage/30 rounded-full flex items-center justify-center text-sage text-sm font-bold">
              {(user?.full_name || user?.name || "S")[0].toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-white text-sm font-medium truncate">{user?.full_name || user?.name || "Seller"}</p>
              <p className="text-gray-400 text-xs truncate">{user?.email || ""}</p>
            </div>
          </div>
          <button onClick={logout} className="w-full py-2.5 text-gray-400 hover:text-red-400 text-sm font-medium rounded-lg hover:bg-white/5 transition-all flex items-center justify-center gap-2">
            <span>🚪</span> Log Out
          </button>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sideOpen && <div className="fixed inset-0 z-30 bg-black/50 md:hidden" onClick={() => setSideOpen(false)}></div>}

      {/* Main content */}
      <div className="flex-1 md:ml-60 flex flex-col min-h-screen">
        {/* Top bar */}
        <header className="bg-white border-b border-stone-200 h-14 flex items-center px-6 sticky top-0 z-20">
          <button onClick={() => setSideOpen(s=>!s)} className="md:hidden mr-4 text-gray-500 hover:text-gray-900">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16"/></svg>
          </button>
          <p className="font-semibold text-gray-700 text-sm">{active}</p>
          <div className="ml-auto flex items-center gap-3">
            <a href="../buyer/index.html" className="text-xs text-gray-400 hover:text-gray-600 font-medium">View Store →</a>
          </div>
        </header>
        <main className="flex-1 p-6">{children}</main>
        <footer className="border-t border-stone-200 py-3 px-6 bg-white">
          <p className="text-xs text-gray-400">© 2025 FiberNest. For educational purposes only, and no copyright infringement is intended.</p>
        </footer>
      </div>
    </div>
  );
}
