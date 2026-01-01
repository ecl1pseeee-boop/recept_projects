function toggleFilters() {
    const panel = document.getElementById("filters-panel");
    const btn = document.getElementById("filters-toggle");
    const chevron = document.getElementById("filters-chevron");

    const isOpen = panel.classList.contains("max-h-[2000px]");

    if (isOpen) {
      panel.classList.remove("max-h-[2000px]", "opacity-100");
      panel.classList.add("max-h-0", "opacity-0");
      chevron.classList.remove("rotate-180");
      btn.setAttribute("aria-expanded", "false");
    } else {
      panel.classList.remove("max-h-0", "opacity-0");
      panel.classList.add("max-h-[2000px]", "opacity-100");
      chevron.classList.add("rotate-180");
      btn.setAttribute("aria-expanded", "true");
    }
}