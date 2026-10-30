# Nhà Gió Homestay – Design spec & danh sách thay đổi cho `css/app.css`

Phạm vi: chỉ CSS (và vài gợi ý class nhỏ trong JS ở mục ghi rõ). Không đổi thương hiệu: giữ tông cam đất / cát / xanh biển hiện có, chỉ chỉnh độ đậm để đạt WCAG.
Nguồn số liệu hiện tại: `css/app.css` (trích nguyên giá trị) và ảnh `screenshots/` (ghi **đo từ ảnh**). Ảnh desktop rộng 1440px; ảnh mobile rộng 780px = viewport 390px @2x (đo từ ảnh).
Cách viết: `hiện tại → đề xuất`.

---

## 0. Ưu tiên (làm theo thứ tự)
1. **Nút chính không đạt tương phản**: chữ trắng trên `--acc #e76f51` = **3.09:1** (cần 4.5:1, chữ 16px/600 không tính là "large text"). Đổi nền nút sang `#b5472c` (5.38:1).
2. **Link `.link` / eyebrow** `#c95a3e` trên nền `#fffaf5` = **4.04:1** → `#b5472c` (5.19:1).
3. **Viền ô nhập** dùng `--line #eee2d6` trên trắng = **1.27:1** (WCAG 1.4.11 cần ≥3:1 cho ranh giới control) → token `--border-strong #a8917c` (3.00:1) cho input/select/textarea/checkbox.
4. **Toast không tự tắt và đè nội dung**: "Đã lưu vào yêu thích" / "NGRABLBZ: Đã xác nhận" còn hiện ở mọi màn chụp, có lúc nằm trên footer cùng màu `#2b2622` nên chỉ còn chữ trôi nổi (desktop-04, 05, 08 – đo từ ảnh). Thêm viền/khác màu nền và tự ẩn (xem §9).
5. **Trạng thái rỗng vỡ layout** (desktop-02b): nút "Xóa bộ lọc & xem tất cả" nằm ngang cạnh `<ul>` do `.empty ul{display:inline-block}` → nút xuống dòng riêng (§5).
6. **Lịch đặt phòng**: ngày đã kín (`.d.bk` sọc `#f3e9e0`) và ngày quá khứ (`.d:disabled` chữ `#c8bdb3`, 1.84:1) gần như không phân biệt được ở ảnh desktop-03 → định nghĩa lại 5 trạng thái (§6.2).
7. **Trang đặt phòng desktop**: khối tóm tắt `.sum` bắt đầu thấp hơn form ~110px (đo từ ảnh desktop-04: form top ≈193px, sum top ≈306px trên ảnh 1024px thu nhỏ) → `align-self:start` + `top` khớp (§6.4).
8. Gom số "lẻ" (gap 10/14/22, radius 10/12/16/20, padding 18) về thang 4/8.

---

## 1. Màu – tokens

Thay khối `:root` hiện tại:
```
--bg:#fffaf5;--card:#fff;--ink:#2b2622;--mut:#6f645b;--line:#eee2d6;--acc:#e76f51;--acc2:#c95a3e;--teal:#1f5f63;--sand:#fbeee2;--r:16px;--sh:0 6px 24px rgba(80,50,30,.08)
```
bằng:
```css
:root{
  /* nền & bề mặt */
  --color-bg:#fffaf5;            /* giữ (--bg) */
  --color-surface:#ffffff;       /* giữ (--card) */
  --color-surface-alt:#fbeee2;   /* giữ (--sand) – chip, tiện nghi, ngày trong khoảng */
  /* chữ */
  --color-text:#2b2622;          /* giữ (--ink) */
  --color-text-muted:#6f645b;    /* giữ (--mut) */
  --color-text-disabled:#a8917c; /* MỚI, thay #c8bdb3 */
  --color-text-inverse:#ffffff;
  /* viền */
  --color-border:#eee2d6;        /* giữ (--line) – chỉ dùng cho divider/thẻ */
  --color-border-strong:#a8917c; /* MỚI – input, select, checkbox, nút ghost */
  /* thương hiệu */
  --color-primary:#b5472c;       /* (--acc2 #c95a3e / nút dùng --acc #e76f51) → #b5472c */
  --color-primary-hover:#9a3a22; /* MỚI */
  --color-accent:#e76f51;        /* giữ (--acc) – chỉ trang trí: sao, logo, cột biểu đồ, viền thumb đang chọn */
  --color-secondary:#1f5f63;     /* giữ (--teal) */
  /* trạng thái */
  --color-success:#1f7a6e;       /* .ok-ic #2a9d8f → #1f7a6e */
  --color-success-text:#11623f;  /* giữ (.up, .s2) */
  --color-danger:#b42318;        /* giữ (.err, .down, .bad) */
  --color-danger-bg:#fff5f5;     /* giữ (.bad) */
  --color-warning-bg:#fff4e5;    /* giữ (.demo-note) */
  --color-warning-border:#f5d0a9;/* giữ */
  --color-fav:#e63946;           /* giữ (.fav.on) */
  --focus-ring:0 0 0 3px rgba(181,71,44,.35); /* MỚI – hiện chưa có style :focus-visible */
}
```
Giữ alias cũ trong giai đoạn chuyển (`--acc:var(--color-accent)` …) để không vỡ selector đang dùng; sau đó đổi dần.

**Áp dụng:** `.btn.primary{background:var(--color-primary);border-color:var(--color-primary)}`, `:hover → --color-primary-hover`; `.link,.eyebrow → color:var(--color-primary)`; `select,input,textarea,.chk input → border-color:var(--color-border-strong)`; thêm `:focus-visible{outline:none;box-shadow:var(--focus-ring)}` cho `.btn,a,input,select,textarea,.d,.fav,.cv,.ic`.

### Tương phản đã tính (công thức WCAG 2.x, luminance sRGB)
| Cặp | Hiện tại | Kết quả | Đề xuất | Kết quả |
|---|---|---|---|---|
| Chữ trắng / nút chính | #fff / #e76f51 | **3.09** ✗ | #fff / #b5472c | 5.38 ✓ AA |
| Nút chính hover | #fff / #c95a3e | 4.19 ✗ | #fff / #9a3a22 | 6.99 ✓ |
| Link/eyebrow / nền | #c95a3e / #fffaf5 | **4.04** ✗ | #b5472c / #fffaf5 | 5.19 ✓ |
| Chữ chính / nền | #2b2622 / #fffaf5 | 14.43 ✓ | giữ | |
| Muted / nền | #6f645b / #fffaf5 | 5.55 ✓ | giữ | |
| Muted / trắng | #6f645b / #fff | 5.75 ✓ | giữ | |
| Chữ / --sand | #2b2622 / #fbeee2 | 13.14 ✓ | giữ | |
| Ngày disabled / trắng | #c8bdb3 / #fff | 1.84 (miễn trừ, nhưng khó đọc) | #a8917c | 3.00 |
| Viền input / trắng | #eee2d6 / #fff | **1.27** ✗ (1.4.11) | #a8917c | 3.00 ✓ |
| Demo bar | #fff / #1f5f63 | 7.30 ✓ | giữ | |
| Link demo bar | #ffd8a8 / #1f5f63 | 5.44 ✓ | giữ | |
| Icon thành công | #fff / #2a9d8f | 3.32 (đủ cho đồ họa, sát ngưỡng) | #fff / #1f7a6e | 5.16 ✓ |
| Lỗi | #b42318 / #fff | 6.57 ✓ | giữ | |
| Lỗi trên ô lỗi | #b42318 / #fff5f5 | 6.15 ✓ | giữ | |
| Badge s0 chờ xác nhận | #7a5200 / #fff1c2 | 6.13 ✓ | giữ | |
| s1 đã xác nhận | #0b4a8b / #d7ecff | 7.32 ✓ | giữ | |
| s2 đã nhận phòng | #11623f / #d8f3e6 | 6.29 ✓ | giữ | |
| s3 hoàn tất | #4b3b8f / #e9e4f7 | 7.28 ✓ | giữ | |
| s4 hủy | #666 / #f1f1f1 | 5.08 ✓ | giữ | |
| Footer chữ phụ | #c9bcb0 / #2b2622 | 8.06 ✓ | giữ | |
| Badge xám `.badge.gray` | #fff / #555 | 7.46 ✓ | giữ | |

Lưu ý: `--color-accent #e76f51` **không** được dùng làm nền cho chữ thường (nút, `.cnt` badge số, `.gantt th.td`). `.cnt` (chữ trắng .75rem trên #e76f51 = 3.09) → nền `--color-primary`.

---

## 2. Typography
Hiện tại: `font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif`; h1 `clamp(1.5rem,4vw,2.2rem)`, hero h1 `clamp(2rem,6vw,3.4rem)`, h2 `1.3rem`, card h3 `1.05rem`; các cỡ lẻ: .7, .75, .78, .82, .85, .88, .9, .92, 1.05, 1.08, 1.1, 1.15rem.

Đề xuất: **giữ system-ui** (README yêu cầu không CDN, không thư viện ngoài; system-ui có dấu tiếng Việt tốt). Gom về 8 bậc:

| Token | rem / px | line-height | weight | Dùng cho | Thay cho |
|---|---|---|---|---|---|
| `--fs-xs` | 0.75 / 12 | 1.4 | 600–700 | nhãn picked, thứ trong tuần, header bảng | .7, .75, .78, .82rem |
| `--fs-sm` | 0.875 / 14 | 1.45 | 400–600 | meta, muted, badge, legend, lỗi | .85, .88, .9, .92rem |
| `--fs-base` | 1 / 16 | 1.55 | 400 | body (giữ) | 16px |
| `--fs-md` | 1.125 / 18 | 1.4 | 700 | tiêu đề card, giá card, lead | 1.05, 1.08, 1.1, 1.15rem |
| `--fs-lg` | 1.375 / 22 | 1.3 | 700 | h2 section | 1.3rem |
| `--fs-xl` | 1.75 / 28 | 1.25 | 700 | h1 trang trong, số KPI | 1.5rem, 1.7rem |
| `--fs-2xl` | clamp(1.75rem,4vw,2.25rem) / 28–36 | 1.2 | 800 | h1 trang chi tiết/đặt phòng | clamp(1.5rem,4vw,2.2rem) |
| `--fs-display` | clamp(2.25rem,6vw,3.5rem) / 36–56 | 1.1 | 800 | hero | clamp(2rem,6vw,3.4rem) |

Weights: chỉ dùng 400 / 600 / 700 / 800 (hiện đã dùng đủ 4; `font-weight:500` ở `.logo small`, `.cat small`, `.big small` → 400).
Số tiền: thêm `font-variant-numeric:tabular-nums` cho `.price,.calc,.tbl td,.kpi b` để cột giá thẳng hàng (desktop-04/06 cột tiền đang canh phải nhưng chữ số tỉ lệ).
`.eyebrow` letter-spacing `.12em` → giữ; `.code` `.12em` giữ.

---

## 3. Spacing (thang 4/8)
```css
--sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-5:20px; --sp-6:24px; --sp-8:32px; --sp-10:40px; --sp-12:48px; --sp-16:64px;
```
Chuyển đổi giá trị lẻ hiện có:
| Vị trí | Hiện tại → Đề xuất |
|---|---|
| `.grid` gap | 22px → 24px |
| `.about` gap | 22px → 24px |
| `.search` gap / padding | 10px / 12px → 8px / 12px |
| `.kpis`, `.adm-grid` gap | 14px → 16px |
| `.panel` margin-bottom | 14px → 16px |
| `.cb` padding | 12px 14px 16px → 16px |
| `.book-box` padding | 18px → 24px |
| `.dt-main section` padding | 18px 0 → 24px 0 |
| `.fg` margin-bottom | 14px → 16px |
| `.btn` padding | 0 18px → 0 20px |
| `section.wrap` margin-top | 44px → 48px |
| `.list-body` gap | 24px → giữ |
| `.dt-body` gap | 32px → giữ |
| `.book-grid` gap | 28px → 32px |
| `.cats` gap | 12px → giữ |

---

## 4. Radius & shadow
Hiện tại: `--r:16px`, cộng giá trị cứng 8, 10, 12, 20, 999px; `--sh:0 6px 24px rgba(80,50,30,.08)`; `.m-bar` `0 -4px 16px rgba(0,0,0,.06)`.
```css
--radius-sm:8px;    /* .mini, gantt booking, thumbs (10px → 8px) */
--radius-md:12px;   /* .btn, input/select (10px → 12px), .picked, .map, .code */
--radius-lg:16px;   /* card, panel, filters, kpi (giữ --r) */
--radius-xl:24px;   /* .book-box, #bookForm, .sum, .carousel, .search (20px → 24px) */
--radius-full:999px;
--shadow-sm:0 1px 2px rgba(80,50,30,.06);                  /* thẻ tĩnh – MỚI */
--shadow-md:0 6px 24px rgba(80,50,30,.08);                 /* giữ --sh: hover card, search, book-box */
--shadow-lg:0 12px 32px rgba(80,50,30,.14);                /* toast, menu mobile – MỚI */
--shadow-up:0 -4px 16px rgba(80,50,30,.08);                /* .m-bar (rgba(0,0,0,.06) → đồng tông nâu) */
```
Input: `border-radius:10px → var(--radius-md)` để khớp `.btn` 12px (hiện lệch 2px, thấy ở desktop-09 ô giá vs nút "Lưu").

---

## 5. Room card (`.card`, `.cb`) & danh sách
Hiện tại: ảnh `.ph aspect-ratio:4/3`; `.cb padding:12px 14px 16px`; h3 `1.05rem`; `.rt .9rem` nowrap; `.price b 1.1rem`; hover `translateY(-2px)` + shadow; `.fav 42×42`, nền `rgba(255,255,255,.92)`; grid `minmax(260px,1fr)` gap 22px.
Quan sát (đo từ ảnh desktop-02): tên dài "Phòng Gia Đình Hoa Giấy" xuống 2 dòng làm giá của card đó thấp hơn card bên cạnh ~14px; meta ("Phòng đôi · 2 khách · 1 giường đôi") cũng wrap 2 dòng → chiều cao card không đều.

Đề xuất:
- Ảnh: giữ `4/3` (hợp ảnh minh họa SVG ngang); `border-radius` ảnh = `--radius-lg` trên, card vẫn `overflow:hidden`.
- Card bỏ viền nền trắng nặng: `border:1px solid var(--color-border)` giữ, `box-shadow:var(--shadow-sm)`.
- `.cb{padding:16px;display:flex;flex-direction:column;gap:4px}`; card dùng `display:flex;flex-direction:column;height:100%` và `.price{margin-top:auto}` → giá luôn thẳng đáy.
- Hàng 1: `h3` `--fs-md`/700, `-webkit-line-clamp:1` + ellipsis; rating `.rt` `--fs-sm`, sao `--color-accent`, số đánh giá muted.
- Hàng 2: meta `--fs-sm` muted, `line-clamp:2`, `min-height:2lh`.
- Hàng 3: `.price b` `--fs-md` 700 + " / đêm" `--fs-sm` muted.
- Hover (chỉ `@media (hover:hover)`): `transform:translateY(-2px)` giữ, `box-shadow:var(--shadow-md)`; thêm `.ph svg{transition:transform .3s}` + `.card:hover .ph svg{transform:scale(1.03)}`. Thêm `:focus-within` dùng cùng style để bàn phím thấy.
- `.badge` "Được yêu thích": giữ trắng, thêm `box-shadow:var(--shadow-sm)`, padding 3px 10px → 4px 12px.
- `.fav`: 42px → 40px (vẫn ≥ 24px tối thiểu; mobile giữ 44px), thêm `box-shadow:var(--shadow-sm)`.
- Grid: gap 22 → 24px; `minmax(260px,1fr)` → `minmax(280px,1fr)` desktop (desktop-02 với sidebar 260px đang ra 3 cột ~178px ảnh thu nhỏ, chấp nhận được; 280 vẫn ra 3 cột ở container 1200 − 260 − 24).
- **Empty state (`.empty`)**: `.empty ul{display:inline-block}` → `display:block;max-width:360px;margin:8px auto 16px`; nút đặt trong block riêng `display:flex;justify-content:center`. Viền `dashed` giữ.
- **Mobile list header** (mobile-02): nhãn "Sắp xếp" bị gãy 2 dòng cạnh select → `.sort{white-space:nowrap}` hoặc ẩn label bằng `.sr-only` dưới 640px.

---

## 6. Trang chi tiết

### 6.1 Gallery
Hiện tại: `.track figure aspect-ratio:16/7` (mobile 4/3), `.carousel border-radius:20px`, `.cv 44×44`, thumbs `aspect-ratio:4/3;max-width:120px;border:3px solid transparent`, active `--acc`.
Đề xuất:
- Desktop: `16/7 → 16/9` cho ảnh chính và đặt chiều cao tối đa `max-height:520px` (ở 16/7 ảnh rộng ~1168px chỉ cao ~510px trong desktop-03, nhưng gallery chiếm toàn bộ màn đầu; 16/9 + max-height giữ cùng chiều cao nhưng crop ít hơn khi container hẹp). Nếu muốn kiểu Airbnb: ≥1100px dùng lưới 1 ảnh lớn + 4 ảnh nhỏ `grid-template-columns:2fr 1fr 1fr; grid-template-rows:1fr 1fr; gap:8px`, ẩn `.thumbs`.
- Radius 20 → `--radius-xl` 24px.
- Thumbs: viền 3px → 2px + `outline-offset:2px` cho `.on` (`outline:2px solid var(--color-text)`), `opacity:.7` cho thumb chưa chọn; radius 10 → 8px.
- `.cv` nút: thêm `box-shadow:var(--shadow-md)`; ẩn ở mobile <640px (vuốt đã có scroll-snap) hoặc giữ 40px.
- `figcaption` nền `rgba(0,0,0,.55)` giữ.

### 6.2 Lịch – trạng thái ngày (`.d`)
Hiện tại: `.d` tròn `aspect-ratio:1;min-height:36px`; hover `outline:2px solid var(--ink)`; disabled chữ `#c8bdb3`; đã kín `.bk` gạch ngang + sọc `#f3e9e0/#fff`; trong khoảng `.in` nền `--sand` vuông; chọn `.sel` nền `--ink` chữ trắng; hôm nay `.td` weight 800.

| Trạng thái | Đề xuất |
|---|---|
| Trống (available) | chữ `--color-text` 600, nền trong suốt, `min-height:40px` (≥ mục tiêu chạm), radius full |
| Hover/focus | `box-shadow:inset 0 0 0 2px var(--color-text)` (thay `outline` để không bị cắt bởi grid gap 2px) |
| Hôm nay | chữ 800 + gạch chân 2px `--color-accent` (hiện chỉ đậm, đo từ ảnh khó thấy) |
| Chọn (check-in/out) | nền `--color-text #2b2622`, chữ trắng (14.97:1) – giữ |
| Trong khoảng (range) | nền `--color-surface-alt #fbeee2`, radius 0; đầu khoảng: `border-radius:999px 0 0 999px` nền nối (dùng pseudo `::before` nửa ô) để dải liền mạch |
| Quá khứ (disabled) | chữ `--color-text-disabled #a8917c`, không nền, `cursor:not-allowed` |
| Đã kín (booked) | chữ `#a8917c` + `text-decoration:line-through`, nền sọc **đậm hơn**: `#ead8c8` thay `#f3e9e0`, và legend `.lg.bk` dùng cùng màu (hiện legend `#e6d6c8` ≠ ô `#f3e9e0`) |
| Chỉ được check-out (đêm trước là kín) | (tùy) nửa sọc – để sau |

Lưới: `.wd,.days gap:2px → 0` (dải range liền), cột tuần `--fs-xs`.
`.mos` 2 tháng ở ≥1100px giữ.

### 6.3 Booking box sticky
Hiện tại: `.book-box` sticky `top:84px`, padding 18px, radius 20px, cột `400px`, ≥1100px `520px`.
Đề xuất:
- Cột: 400 → **380px** dưới 1100px; ≥1100px 520 → **440px** (520 chiếm ~45% của 1168 làm phần mô tả bị hẹp – desktop-03 đo từ ảnh: cột trái ~232px/536 ảnh thu nhỏ ≈ 43%). Lịch 2 tháng ở 440px: mỗi tháng ~190px, ô ~27px – quá nhỏ ⇒ **trong book-box chỉ hiện 1 tháng** + nút ‹ ›; muốn 2 tháng thì đặt lịch vào cột trái (section "Chọn ngày") như Airbnb. Chọn một: khuyến nghị lịch 2 tháng ở cột trái, book-box chỉ hiện ô Nhận/Trả phòng mở popover.
- `top:84px` → `calc(64px + 24px)` (header `.top-in min-height:64px`) – thêm `--header-h:64px`.
- Thứ tự: giá/đêm (`--fs-xl` 700 + "/ đêm" muted) → `.picked` 2 ô (radius 12, viền `--color-border-strong`) → số khách → nút "Đặt phòng" full width 48px → dòng "chưa bị trừ tiền" `--fs-sm` muted canh giữa → breakdown.
- `max-height:calc(100vh - 112px);overflow:auto` để box không vượt màn hình thấp.

### 6.4 Price breakdown (`.calc`)
Hiện tại: `.calc p` flex space-between, margin `.4em`; `.tot` viền trên, 800, 1.05rem.
Đề xuất: dòng `--fs-base`, nhãn phí dọn/phí dịch vụ dùng `text-decoration:underline dotted` (gợi ý giải thích), số `tabular-nums`; `.tot` `--fs-md` 800, `padding-top:12px;margin-top:12px`. Trang đặt phòng `.sum`: thêm `align-self:start` và cùng `top` với book-box; thẻ `.sum` hiện đang bắt đầu thấp hơn form (đo từ ảnh desktop-04) – kiểm tra margin-top của `.sum` / phần tử đầu trong `.book-grid`.

---

## 7. Trang quản lý
Hiện tại: tab ngang `.adm-tabs` (padding 12px 16px, gạch dưới 3px `--acc`), KPI 4 cột, bảng `.tbl` padding 10px, th `.82rem` uppercase muted, badge `.s0–.s4` pill. **Không có sidebar** (desktop-06…09).

- **Sidebar** (đề xuất mới, ≥1100px): `.admin{display:grid;grid-template-columns:232px 1fr;gap:32px}`; tab chuyển thành list dọc: item `min-height:40px;padding:8px 12px;border-radius:12px;font-weight:600`, active nền `--color-surface-alt` + chữ `--color-text` + thanh trái 3px `--color-primary`. Dưới 1100px giữ tab ngang hiện có. (Cần đổi wrapper trong admin.js – nếu không muốn đụng JS thì giữ tab, chỉ áp phần dưới.)
- **Tab mobile** (mobile-06/07): tab thứ 3 bị cắt "Lịc…" không có dấu hiệu cuộn → thêm `mask-image:linear-gradient(90deg,#000 85%,transparent)` hoặc giảm padding 12px 16px → 10px 12px ở <640px.
- **Mật độ bảng**: padding 10px → `12px 16px` (comfortable) mặc định; thêm `.tbl.dense td{padding:8px 12px}`. th `.82rem` → `--fs-xs` 700, letter-spacing .04em, nền `--color-surface-alt`, `position:sticky;top:0`. Hàng hover `background:#fffaf5`. Cột tiền `text-align:right` (hiện canh trái – desktop-07).
- **Badge trạng thái**: giữ 5 cặp màu (đều ≥5:1, xem §1). Thêm chấm tròn 6px `currentColor` trước chữ để không chỉ dựa vào màu. Badge (`.chip`) padding 3px 10px → 4px 10px, `--fs-xs` 700. `.st-sel` (select dạng badge) min-height 36 → giữ, thêm caret rõ và viền `1px solid currentColor` 30% khi focus.
- **KPI**: số `1.7rem` → `--fs-xl` 28px 800 tabular; label `--fs-sm` muted 600; delta `.up/.down` thêm mũi tên đã có.
- **Gantt** (desktop-08): ô 44px cao, min-width 34px – giữ; cột cuối tuần `#f6e0cf` giữ; hôm nay `th.td` nền `--acc` chữ trắng (3.09) → nền `--color-primary` (5.38). Thanh booking dùng đúng class `.s0–.s3`; legend dùng chip màu đã có.
- **Form** (desktop-09 "Thêm phòng mới"): label 600 `--fs-sm`, gap label–input 4 → 6px, hàng gap 12 → 16px; input cao 42px → 44px; nút "+ Thêm phòng" hiện rộng nửa form (đo từ ảnh) → `justify-self:start;min-width:200px` hoặc full width ở mobile. Bảng phòng: ô số `.num` 130px giữ, nút "Lưu" chuyển thành `.btn` secondary (viền) và chỉ đổi primary khi hàng có thay đổi (giảm 7 nút cam liên tiếp).
- Hàng bảng ở mobile (card hóa): `border-bottom:8px solid var(--bg)` → dùng `margin-bottom:12px;border:1px solid var(--color-border);border-radius:var(--radius-lg)` để mỗi đặt phòng thành thẻ rõ (mobile-07 hiện các hàng dính nhau, đo từ ảnh).

---

## 8. Breakpoints & mobile
Hiện tại: `max-width:900px`, `max-width:640px`, `min-width:1100px`. Container `max-width:1200px;padding:0 16px`.
Đề xuất (mobile-first, giữ 3 mốc hiện có để ít sửa):
| Token | Giá trị | Ghi chú |
|---|---|---|
| `sm` | ≥640px | 2 cột search, 2 cột card |
| `md` | ≥900px | hiện nav desktop, sidebar lọc, 2 cột chi tiết |
| `lg` | ≥1100px | lịch 2 tháng, sidebar admin |
| container padding | 16px (<640) → 24px (≥640) → 32px (≥1100) | hiện cố định 16px |

Mobile (viewport 390px, đo từ ảnh):
- **Demo bar** chiếm 2 dòng (~38px) – rút gọn chữ dưới 640px hoặc `font-size:--fs-xs`.
- **Search hero** đè lên tranh: giữ gradient 180deg hiện tại.
- **Thanh đặt phòng dưới (`.m-bar`)**: padding 10px 16px → `12px 16px calc(12px + env(safe-area-inset-bottom))`.
- **Toast** `bottom:80px` trên mobile đè nội dung form (mobile-04 đo từ ảnh) → xem §9.
- **Menu mobile** (mobile-10): ảnh chụp chỉ thấy trang chủ, menu chưa mở ⇒ không đánh giá được; đề xuất `.nav.open` thêm `box-shadow:var(--shadow-lg)`, item 48px.
- **Trang thành công mobile** (mobile-05): dòng "Ngày 02/11/2026 → 05/11/2026 (3 đêm)" chật – đổi `.calc.left p` sang `flex-wrap:wrap`.
- Lịch quản lý mobile: tên phòng wrap 2–3 dòng ở cột 112px – giữ, nhưng giảm cỡ còn `--fs-xs`.
- Mọi vùng chạm ≥44px: `.chk` 34px → 44px; `.d` 36 → 40px; `.fchip` 40 → 44px.

---

## 9. Toast
Hiện tại: `#toasts` fixed right 16 bottom 16; `.toast` nền `--ink #2b2622`, không có viền; trùng màu footer `#2b2622`.
Đề xuất: `.toast{border:1px solid rgba(255,255,255,.12);box-shadow:var(--shadow-lg);max-width:min(360px,calc(100vw - 32px))}`; JS (nhỏ) tự ẩn sau 3s với `animation: toast-in .2s, toast-out .2s 2.8s forwards`; tôn trọng `prefers-reduced-motion`. Mobile: căn giữa `left:16px;right:16px`, `bottom:calc(80px + env(safe-area-inset-bottom))` chỉ khi có `.m-bar`.

---

## 10. Bảng token: hiện tại → đề xuất
| Token | Hiện tại | Đề xuất |
|---|---|---|
| bg | `--bg #fffaf5` | `--color-bg #fffaf5` (giữ) |
| surface | `--card #fff` | `--color-surface #fff` (giữ) |
| surface-alt | `--sand #fbeee2` | `--color-surface-alt #fbeee2` (giữ) |
| text | `--ink #2b2622` | `--color-text #2b2622` (giữ) |
| muted | `--mut #6f645b` | `--color-text-muted #6f645b` (giữ) |
| disabled text | `#c8bdb3` (cứng) | `--color-text-disabled #a8917c` |
| border | `--line #eee2d6` | `--color-border #eee2d6` (divider) |
| border control | (dùng `--line`) | `--color-border-strong #a8917c` |
| primary (nút) | `--acc #e76f51` | `--color-primary #b5472c` |
| primary hover | `--acc2 #c95a3e` | `--color-primary-hover #9a3a22` |
| accent (trang trí) | `--acc #e76f51` | `--color-accent #e76f51` |
| secondary | `--teal #1f5f63` | `--color-secondary #1f5f63` (giữ) |
| success | `#2a9d8f` / `#11623f` | `--color-success #1f7a6e` / `--color-success-text #11623f` |
| danger | `#b42318` | `--color-danger #b42318` (giữ) |
| radius | `--r 16px` + 8/10/12/20 cứng | `--radius-sm 8 / md 12 / lg 16 / xl 24 / full 999` |
| shadow | `--sh 0 6px 24px rgba(80,50,30,.08)` | `--shadow-sm / md(=cũ) / lg / up` |
| font | system-ui 16px/1.55 | giữ; 12 cỡ lẻ → 8 bậc `--fs-xs…display` |
| spacing | 10/14/18/22/44 lẻ | thang 4/8: 4,8,12,16,20,24,32,40,48,64 |
| focus | không có | `--focus-ring 0 0 0 3px rgba(181,71,44,.35)` |
| header height | 64px (cứng) | `--header-h 64px` |

---
*Ghi chú: mọi màu đề xuất giữ cùng hue với bảng màu hiện tại (cam đất, cát, xanh biển), chỉ tối hơn để qua AA. Không thêm font, logo hay màu thương hiệu mới.*
