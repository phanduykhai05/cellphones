# Frame card (khối bao chung của mọi card trong template)
- outer: `display:flex; flex-direction:column; border:1px solid var(--border) (oklch .922); border-radius:14px (radius-xl = .625rem*1.4); background: oklab(.97 0 0 / .5) (muted/50)`
- header: `padding: 8px 16px; display:flex; justify-content:space-between; gap:12px` — title 14px/20px 600; subtitle 14px/20px muted-foreground (oklch .556)
- panel (bên trong): `background:#fff; border:1px solid var(--border); border-radius:14px; margin:0 -1px -1px; padding:16px; box-shadow: 0 1px 2px rgba(0,0,0,.05) (shadow-xs)` — panel chứa bảng thì padding 0
- KPI: value 24px/32px 600 tracking -0.6px tabular-nums; badge ↑ cạnh value gap 10px; dòng phân cách border-top dashed? (thực tế: hr 1px border) rồi "Vs previous period: **$14K**" 12px muted
- grid KPI: 4 cột gap 24px
