// Hành vi giao diện — đối chiếu docs/research/BEHAVIORS.md. Mỗi khối gắn qua data-* nên trang nào thiếu phần tử thì bỏ qua.

// 1. Header thu gọn khi cuộn + nút "Lên đầu"
const header = document.querySelector("[data-header]");
const toTop = document.querySelector("[data-to-top]");
const onScroll = () => {
  header?.classList.toggle("is-scrolled", scrollY > 50);
  if (toTop) toTop.hidden = scrollY < 400;
};
addEventListener("scroll", onScroll, { passive: true });
onScroll();
toTop?.addEventListener("click", () => scrollTo({ top: 0, behavior: "smooth" }));

// 2. Slider banner: tự chuyển 4.5s, click tab/mũi tên, dừng khi hover
document.querySelectorAll("[data-slider]").forEach((slider) => {
  const slides = [...slider.querySelectorAll("[data-slide]")];
  const tabs = [...slider.querySelectorAll("[data-slide-to]")];
  const tabBar = slider.querySelector("[data-slider-tabs]");
  let current = 0;
  let timer;
  const show = (i) => {
    current = (i + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle("is-active", k === current));
    tabs.forEach((t, k) => t.classList.toggle("is-active", k === current));
    const tab = tabs[current];
    if (tab && tabBar) tabBar.scrollTo({ left: tab.offsetLeft - (tabBar.clientWidth - tab.offsetWidth) / 2, behavior: "smooth" });
  };
  const play = () => { clearInterval(timer); timer = setInterval(() => show(current + 1), 4500); };
  tabs.forEach((t, k) => t.addEventListener("click", () => { show(k); play(); }));
  // Mũi tên thanh tab: cuộn ~nửa thanh, ẩn khi tới mép
  const tabPrev = slider.querySelector("[data-tabs-prev]");
  const tabNext = slider.querySelector("[data-tabs-next]");
  const syncTabNav = () => {
    if (!tabBar || !tabPrev) return;
    tabPrev.disabled = tabBar.scrollLeft < 4;
    tabNext.disabled = tabBar.scrollLeft + tabBar.clientWidth >= tabBar.scrollWidth - 4;
  };
  tabPrev?.addEventListener("click", () => tabBar.scrollBy({ left: -tabBar.clientWidth / 2 }));
  tabNext?.addEventListener("click", () => tabBar.scrollBy({ left: tabBar.clientWidth / 2 }));
  tabBar?.addEventListener("scroll", syncTabNav, { passive: true });
  syncTabNav();
  slider.querySelector("[data-slide-prev]")?.addEventListener("click", () => { show(current - 1); play(); });
  slider.querySelector("[data-slide-next]")?.addEventListener("click", () => { show(current + 1); play(); });
  slider.addEventListener("mouseenter", () => clearInterval(timer));
  slider.addEventListener("mouseleave", play);
  if (slides.length > 1) play();
});

// 3. Tab đổi panel (khối Deal, block danh mục)
document.querySelectorAll("[data-tabs]").forEach((box) => {
  const tabs = [...box.querySelectorAll("[data-tab]")];
  const panels = [...box.querySelectorAll("[data-panel]")];
  tabs.forEach((tab) => tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.toggle("is-active", t === tab));
    panels.forEach((p) => { p.hidden = p.dataset.panel !== tab.dataset.tab; });
    panels.forEach((p) => !p.hidden && p.querySelectorAll("[data-carousel]").forEach(updateCarousel));
  }));
});

// 4. Carousel cuộn ngang: mũi tên cuộn 1 trang, ẩn khi tới mép
function updateCarousel(c) {
  const track = c.querySelector("[data-track]");
  c.querySelector("[data-prev]").disabled = track.scrollLeft < 4;
  c.querySelector("[data-next]").disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
}
document.querySelectorAll("[data-carousel]").forEach((c) => {
  const track = c.querySelector("[data-track]");
  c.querySelector("[data-prev]").addEventListener("click", () => track.scrollBy({ left: -track.clientWidth, behavior: "smooth" }));
  c.querySelector("[data-next]").addEventListener("click", () => track.scrollBy({ left: track.clientWidth, behavior: "smooth" }));
  track.addEventListener("scroll", () => updateCarousel(c), { passive: true });
  updateCarousel(c);
});

// 5. Nút tim (chỉ đổi trạng thái phía client)
document.addEventListener("click", (e) => {
  const fav = e.target.closest("[data-fav]");
  if (fav) fav.setAttribute("aria-pressed", fav.getAttribute("aria-pressed") !== "true");
});

// 6. Gallery trang chi tiết: thumbnail, mũi tên, chọn màu đổi ảnh
document.querySelectorAll("[data-gallery]").forEach((g) => {
  const main = g.querySelector("[data-gallery-main]");
  const thumbs = [...g.querySelectorAll("[data-thumb]")];
  let current = 0;
  const show = (i) => {
    current = (i + thumbs.length) % thumbs.length;
    main.src = thumbs[current].dataset.thumb;
    thumbs.forEach((t, k) => t.classList.toggle("is-active", k === current));
    thumbs[current].scrollIntoView({ block: "nearest", inline: "nearest" });
  };
  thumbs.forEach((t, k) => t.addEventListener("click", () => show(k)));
  g.querySelector("[data-gallery-prev]")?.addEventListener("click", () => show(current - 1));
  g.querySelector("[data-gallery-next]")?.addEventListener("click", () => show(current + 1));
  document.querySelectorAll("[data-color-img]").forEach((input) =>
    input.addEventListener("change", () => { main.src = input.dataset.colorImg; thumbs.forEach((t) => t.classList.remove("is-active")); }));
});

// 7. Đóng menu/dropdown <details> khi click ra ngoài hoặc nhấn Esc
const closeDetails = (except) =>
  document.querySelectorAll(".hd-menu[open], .hd-account[open], .filter-dd[open]").forEach((d) => d !== except && d.removeAttribute("open"));
document.addEventListener("click", (e) => closeDetails(e.target.closest("details")));
document.addEventListener("keydown", (e) => e.key === "Escape" && closeDetails());
