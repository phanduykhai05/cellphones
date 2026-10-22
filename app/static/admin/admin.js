// Hành vi admin — đối chiếu docs/research/admin/BEHAVIORS.md
const adm = document.querySelector("[data-adm]");
const mobile = () => matchMedia("(max-width: 1023px)").matches;

// Thu/mở sidebar (desktop: thu gọn và nhớ trạng thái; mobile: trượt ra như drawer)
try { if (localStorage.getItem("adm-collapsed") === "1" && !mobile()) adm?.classList.add("is-collapsed"); } catch {}
document.querySelector("[data-sidebar-toggle]")?.addEventListener("click", () => {
  if (mobile()) return adm.classList.toggle("is-open");
  const collapsed = adm.classList.toggle("is-collapsed");
  try { localStorage.setItem("adm-collapsed", collapsed ? "1" : "0"); } catch {}
});

// ⌘K / Ctrl+K: focus ô tìm kiếm
document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
    const input = document.querySelector("[data-search-input]");
    if (input) { e.preventDefault(); if (mobile()) adm.classList.add("is-open"); input.focus(); }
  }
  if (e.key === "Escape") document.querySelectorAll(".amenu[open]").forEach((d) => d.removeAttribute("open"));
});

// Click cả hàng bảng để mở chi tiết (trừ khi click vào link/nút/menu bên trong)
document.addEventListener("click", (e) => {
  document.querySelectorAll(".amenu[open]").forEach((d) => !d.contains(e.target) && d.removeAttribute("open"));
  const row = e.target.closest("tr[data-href]");
  if (row && !e.target.closest("a, button, summary, details, input, select")) location.href = row.dataset.href;
});

// Chọn số dòng -> submit
document.querySelectorAll("form[data-autosubmit] select").forEach((s) => s.addEventListener("change", () => s.form.submit()));

// Hiện/ẩn mật khẩu
document.querySelector("[data-toggle-password]")?.addEventListener("click", () => {
  const input = document.querySelector("[data-password]");
  input.type = input.type === "password" ? "text" : "password";
});

// Xem trước ảnh upload
const imageInput = document.querySelector("[data-image-input]");
imageInput?.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;
  const preview = document.querySelector("[data-image-preview]");
  preview.src = URL.createObjectURL(file);
  preview.hidden = false;
  document.querySelector("[data-image-name]").textContent = file.name;
});

// Xác nhận trước khi xoá / huỷ đơn
document.addEventListener("submit", (e) => {
  const btn = e.submitter;
  if (btn?.dataset.confirm && !confirm(btn.dataset.confirm)) e.preventDefault();
  const status = e.target.querySelector("select[name=status]");
  if (status?.value === "cancelled" && !confirm("Huỷ đơn này? Sản phẩm sẽ được trả về kho.")) e.preventDefault();
});

// ===== Motion =====
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;

// Đóng drawer khi bấm lớp nền mờ
document.querySelector("[data-sidebar-close]")?.addEventListener("click", () => adm.classList.remove("is-open"));

// Thứ tự dòng bảng cho hiệu ứng hiện lần lượt
document.querySelectorAll(".dt tbody").forEach((tbody) =>
  [...tbody.rows].forEach((tr, i) => tr.style.setProperty("--row", Math.min(i, 12))));

// Số KPI chạy từ 0 lên giá trị thật (ease-out cubic, 0.9s)
if (!reduceMotion) {
  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = Number(el.dataset.count);
    if (!target) return;
    const suffix = el.hasAttribute("data-money") ? "đ" : "";
    const fmt = (n) => n.toLocaleString("vi-VN") + suffix;
    const start = performance.now() + 150;
    const tick = (now) => {
      const t = Math.min(Math.max((now - start) / 900, 0), 1);
      el.textContent = fmt(Math.round(target * (1 - (1 - t) ** 3)));
      if (t < 1) requestAnimationFrame(tick);
    };
    el.textContent = fmt(0);
    requestAnimationFrame(tick);
  });
}

// Thông báo tự ẩn sau 4 giây
document.querySelectorAll(".aflash").forEach((el) => {
  setTimeout(() => {
    el.classList.add("is-leaving");
    setTimeout(() => el.remove(), reduceMotion ? 0 : 300);
  }, 4000);
});
