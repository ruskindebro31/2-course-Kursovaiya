const toggle = document.getElementById("menu-toggle");
const nav = document.getElementById("main-nav");

function setOpen(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
}

if (toggle && nav) {
    toggle.addEventListener("click", () => {
        setOpen(!nav.classList.contains("open"));
    });

    document.addEventListener("click", (e) => {
        if (!nav.classList.contains("open")) return;
        const t = e.target;
        if (t instanceof Node && !nav.contains(t) && !toggle.contains(t)) {
            setOpen(false);
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") setOpen(false);
    });

    nav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            if (window.matchMedia("(max-width: 768px)").matches) setOpen(false);
        });
    });
}
