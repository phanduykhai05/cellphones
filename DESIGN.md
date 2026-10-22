---
version: alpha
name: Cellphones
description: |
  CellphoneS embodies a bold, energetic e-commerce aesthetic centered on urgent
  action and consumer trust. The design radiates confidence through vibrant
  primary red paired with crisp whites and subtle neutrals, creating a
  high-contrast, product-focused environment. Hero sections employ dynamic
  gradients that shift from cool light blues to warmer tones, evoking both tech
  sophistication and approachability. The visual language prioritizes clarity
  and scannability—large, uppercase typography dominates promotional zones,
  while structured layouts guide users through product discovery with
  efficiency. Rounded pill-shaped buttons and controlled shadows create a
  modern, accessible interface that feels both premium and friendly.
source:
  url: "https://cellphones.com.vn/"
  pagesAnalyzed: 1
  extractedAt: 2026-10-22
  tokensMeasured: true
colors:
  primary: "#D70018"
  accent: "#E45464"
  canvas: "#FFFFFF"
  surface-alt: "#F2F2F3"
  on-primary: "#000000"
  ink: "#000000"
  body: "#1D1D20"
  hairline: "#CFCFD3"
  info: "#3B82F6"
  accent-1: "#2B2B30"
  accent-2: "#2570EB"
  neutral-1: "#71717A"
  neutral-2: "#A1A1AA"
  neutral-3: "#52525B"
typography:
  heading-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: 700
    lineHeight: 2
    letterSpacing: 0px
    textTransform: uppercase
  heading-sm-tight:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: 700
    lineHeight: 0.4
    letterSpacing: 0px
    textTransform: uppercase
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: 0px
  body-md-strong:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0px
  body-sm-strong:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: 0px
  body-sm-2:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.5
    letterSpacing: 0px
  body-xs:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0px
  button-xl:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: 800
    lineHeight: 0.57
    letterSpacing: 0px
    textTransform: uppercase
  button-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: 0px
    textTransform: uppercase
  button-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.43
    letterSpacing: 0px
  button-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0px
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0px
  label-xs:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.5
    letterSpacing: 0px
  caption-xs:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 2
    letterSpacing: 0px
  caption-xs-tight:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.33
    letterSpacing: 0px
  caption-xs-strong:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.33
    letterSpacing: 0px
  caption-xs-2:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.33
    letterSpacing: 0px
  caption-xs-3:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: 0px
  caption-xs-4:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.33
    letterSpacing: 0px
rounded:
  none: 0px
  xs: 6px
  sm: 8px
  md: 12px
  full: 9999px
spacing:
  xxs: 4px
  xs: 8px
  sm: 12px
  md: 16px
  lg: 20px
  xl: 24px
  xxl: 32px
  xxxl: 36px
  section: 120px
borderWidths:
  thin: 1px
  medium: 3px
shadows:
  sm: "rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px"
  md: "rgba(0, 0, 0, 0.05) -1px 0px 10px 0px inset, rgba(0, 0, 0, 0.03) 0px 2px 8px 0px"
  lg: "rgb(82, 82, 91) 0px 0px 0px 0px"
  xl: "rgba(0, 0, 0, 0.11) 0px 4px 20px -8px, rgba(0, 0, 0, 0.06) 0px 0px 10px 0px"
elevationStrategy: layered-micro
themes:
  derived: dark   # the other theme is the site's measured palette
  light:
    bg: "#FFFFFF"
    surface: "#F2F2F3"
    surfaceRaised: "#E8E8E9"
    text: "#000000"
    textMuted: "#1D1D20"
    border: "#CFCFD3"
    accent: "#D70018"
    accentFg: "#FFFFFF"
    focusRing: "#D70018"
    elevation: shadow
  dark:
    bg: "#15090C"
    surface: "#23181B"
    surfaceRaised: "#2F2427"
    text: "#FDF5F6"
    textMuted: "#A59B9D"
    border: "#3A3033"
    accent: "#FF011D"
    accentFg: "#000000"
    focusRing: "#D70018"
    elevation: "border+surface"
gradients:
  - context: hero
    kind: linear
    value: "linear-gradient(188.66deg, rgb(239, 245, 255) 28.75%, rgba(244, 251, 255, 0.4) 87.64%)"
  - context: section
    kind: linear
    value: "linear-gradient(in oklab, rgb(228, 84, 100) 0px, rgb(215, 0, 24) 100%)"
components:
  button-filled:
    textColor: "{colors.ink}"
    border: "3px solid rgb(96, 154, 250)"
    height: 63.9844px
    fontSize: 16px
    fontFamily: Inter
    fontWeight: 400
    lineHeight: 1.5
    rounded: "16px 16px 0px 0px"
    backgroundColor: "rgb(239, 245, 255)"
  button-filled-2:
    textColor: "{colors.ink}"
    height: 63.9844px
    padding: "3px 0px 0px 0px"
    fontSize: 16px
    boxShadow: "rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) -1px 0px 10px 0px inset, rgba(0, 0, 0, 0.03) 0px 2px 8px 0px"
    fontFamily: Inter
    fontWeight: 400
    lineHeight: 1.5
    rounded: "16px 16px 0px 0px"
    backgroundColor: "rgb(247, 247, 248)"
  button-secondary:
    typography: "{typography.body-sm-strong}"
    textColor: "{colors.canvas}"
    border: "1px solid {colors.on-primary}"
    height: 42px
    padding: "8px 16px 8px 16px"
    rounded: "{rounded.md}"
    backgroundColor: "{colors.on-primary}"
  button-primary:
    typography: "{typography.body-sm-strong}"
    textColor: "{colors.canvas}"
    border: "1px solid {colors.primary}"
    height: 42px
    padding: "8px 16px 8px 16px"
    rounded: "{rounded.md}"
    backgroundColor: "{colors.primary}"
  button-primary-sm:
    typography: "{typography.label-sm}"
    textColor: "{colors.canvas}"
    border: "1px solid {colors.primary}"
    height: 40px
    padding: "8px 16px 8px 16px"
    rounded: "{rounded.sm}"
    backgroundColor: "{colors.primary}"
  footer:
    textColor: "{colors.ink}"
    fontSize: 16px
    fontFamily: Inter
    fontWeight: 400
    lineHeight: 1.5
  link:
    textColor: "{colors.ink}"
    fontSize: 16px
    fontFamily: Inter
    fontWeight: 400
    lineHeight: 1
    rounded: "{rounded.md}"
    backgroundColor: "{colors.surface-alt}"
  link-sm:
    textColor: "{colors.ink}"
    fontSize: 16px
    fontFamily: Inter
    fontWeight: 400
    lineHeight: 1
states:
  link-hover:
    target: link
    state: hover
    textDecoration: underline
  other-hover:
    target: other
    state: hover
    opacity: 0.8
  other-focus:
    target: other
    state: focus
    outline: "rgba(0, 0, 0, 0) solid 2px"
    outlineColor: "rgba(0, 0, 0, 0)"
    outlineWidth: 2px
  other-focus-visible:
    target: other
    state: focus-visible
    outlineWidth: 1px
  other-disabled:
    target: other
    state: disabled
    opacity: 0.5
breakpoints:
  - width: 375
    containerWidth: 367
    gridColumns: 5
    navLinksVisible: 0
    menuToggleVisible: true
    headingPx: 16
    bodyPx: 16
    sectionPaddingX: 8
  - width: 768
    containerWidth: 752
    gridColumns: 6
    navLinksVisible: 0
    menuToggleVisible: true
    headingPx: 20
    bodyPx: 16
    sectionPaddingX: 8
  - width: 1024
    containerWidth: 1008
    gridColumns: 6
    navLinksVisible: 0
    menuToggleVisible: true
    headingPx: 20
    bodyPx: 16
    sectionPaddingX: 8
  - width: 1280
    containerWidth: 1232
    gridColumns: 6
    navLinksVisible: 0
    menuToggleVisible: true
    headingPx: 20
    bodyPx: 16
    sectionPaddingX: 16
  - width: 1440
    containerWidth: 1232
    gridColumns: 6
    navLinksVisible: 0
    menuToggleVisible: true
    headingPx: 20
    bodyPx: 16
    sectionPaddingX: 16
coverage:
  statesFound: 61
  gradientsFound: 2
  rolesUnassigned: 5
  archetypesUnnamed: 0
  archetypesDetected: 0
  responsiveMeasured: true
  stylesheetsBlocked: false
  semanticRampDeclared: true
---

# Design System Inspired by CellphoneS

## 1. Visual Theme & Atmosphere

CellphoneS embodies a bold, energetic e-commerce aesthetic centered on urgent action and consumer trust. The design radiates confidence through vibrant primary red paired with crisp whites and subtle neutrals, creating a high-contrast, product-focused environment. Hero sections employ dynamic gradients that shift from cool light blues to warmer tones, evoking both tech sophistication and approachability. The visual language prioritizes clarity and scannability—large, uppercase typography dominates promotional zones, while structured layouts guide users through product discovery with efficiency. Rounded pill-shaped buttons and controlled shadows create a modern, accessible interface that feels both premium and friendly.

**Key Characteristics**
- Bold primary red (`#D70018`) as the dominant brand and CTA color
- High contrast between `#FFFFFF` canvas and `#000000` text for readability
- Gradient hero sections blending light blue and warm red tones
- Pill-shaped buttons (`{rounded.full}`) for softer, inviting interactions
- Uppercase typography on high-impact elements (headings, CTAs, labels)
- Layered micro-shadows for subtle, barely-there depth
- Dense product grids with consistent spacing and alignment
- Neutral surface alternation (`#FFFFFF` and `#F2F2F3`) for visual rhythm

---

## 2. Color Palette & Roles

### Primary
- **Primary / Brand** (`#D70018`): Primary CTA buttons, brand accent on promotional hero bands, active link states, and key navigation elements. The heart of the brand identity—high saturation, commanding attention.
- **On Primary** (`#000000`): Text and labels placed directly on brand surfaces; ensures legibility on red backgrounds.

### Accent Colors
- **Accent** (`#E45464`): Secondary accent used in hero bands and promotional gradients; a lighter variant of the primary for depth layering.
- **Accent Decorative** (`#2B2B30`): Unassigned decorative tone; no measured role on the site.
- **Accent Decorative** (`#2B2B30`): Unassigned decorative tone; no measured role on the site.

### Interactive
- **Info** (`#3B82F6`): Informational states, links, and secondary interactive elements. Used in border highlights and focus states.

### Neutral Scale
- **Canvas** (`#FFFFFF`): Default page background and primary surface.
- **Surface Alt** (`#F2F2F3`): Alternating section backgrounds and container fills; creates subtle visual rhythm.
- **Body** (`#1D1D20`): Primary body copy and headline text; near-black for maximum legibility.
- **Neutral Medium** (`#71717A`): Placeholder text, secondary labels, and de-emphasized content.
- **Neutral Light** (`#A1A1AA`): Tertiary text and very light accents.
- **Neutral Dark** (`#52525B`): Mid-tone neutrals for secondary UI elements.

### Surface & Borders
- **Hairline** (`#CFCFD3`): 1px dividers and subtle borders; the finest stroke weight in the palette.

---

## 3. Typography Rules

### Font Family
**Primary:** Inter (sans-serif)  
**Fallback:** system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif

### Hierarchy

| Role | Font | Size | Weight | Line Height | Letter Spacing | Notes |
|---|---|---|---|---|---|---|
| Display XL | Inter | 28px | 800 | 0.57 | 0px | `{typography.button-xl}` — uppercase promotional text; ultra-tight line height for impact |
| Heading SM | Inter | 20px | 700 | 2 | 0px | `{typography.heading-sm}` — section titles and category headers; uppercase |
| Heading SM Tight | Inter | 20px | 700 | 0.4 | 0px | `{typography.heading-sm-tight}` — compact uppercase headings |
| Body MD Strong | Inter | 16px | 700 | 1.5 | 0px | `{typography.body-md-strong}` — bold body emphasis |
| Body MD | Inter | 16px | 600 | 1.5 | 0px | `{typography.body-md}` — primary body and section intro text |
| Body SM Strong | Inter | 14px | 600 | 1.5 | 0px | `{typography.body-sm-strong}` — bold inline copy |
| Body SM | Inter | 14px | 700 | 1.5 | 0px | `{typography.body-sm-2}` — strong body variant |
| Body SM Standard | Inter | 14px | 500 | 1.5 | 0px | `{typography.body-sm}` — regular body on links |
| Button LG | Inter | 16px | 600 | 1.5 | 0px | `{typography.button-lg}` — large button text; uppercase |
| Button MD | Inter | 14px | 600 | 1.43 | 0px | `{typography.button-md}` — standard button text |
| Button SM | Inter | 12px | 500 | 1 | 0px | `{typography.button-sm}` — small button or compact CTA |
| Label SM | Inter | 14px | 400 | 1.5 | 0px | `{typography.label-sm}` — form input and field labels |
| Label XS | Inter | 12px | 500 | 1.5 | 0px | `{typography.label-xs}` — small labels and badge text |
| Caption XS | Inter | 12px | 400 | 2 | 0px | `{typography.caption-xs}` — fine print, secondary metadata |
| Caption XS Tight | Inter | 12px | 400 | 1.33 | 0px | `{typography.caption-xs-tight}` — compact captions |
| Caption XS Strong | Inter | 12px | 500 | 1.33 | 0px | `{typography.caption-xs-strong}` — bold captions |
| Caption XS Bold | Inter | 12px | 600 | 1.33 | 0px | `{typography.caption-xs-2}` — emphasized caption |
| Caption XS Extra Bold | Inter | 12px | 700 | 1.33 | 0px | `{typography.caption-xs-4}` — maximum caption emphasis |
| Caption XS Medium | Inter | 12px | 600 | 1.5 | 0px | `{typography.caption-xs-3}` — mid-weight caption |
| Body XS | Inter | 12px | 400 | 1.5 | 0px | `{typography.body-xs}` — smallest body text; fine print |

### Principles
- **Uppercase for urgency:** Display and heading roles universally uppercase to signal importance and drive attention to promotions and category navigation.
- **Tight leading on display:** The 28px display text uses a 0.57 line-height ratio (16px actual leading) to compress impact.
- **Consistent 1.5 line-height on body:** Body and label text consistently 1.5 for comfortable reading.
- **Weight contrast:** Hierarchy depends heavily on weight jumps (400 → 500 → 600 → 700 → 800) rather than size alone.
- **Label precision:** Forms and inputs use precise 14px and 12px weights (400–500) to signal secondary information without visual noise.

---

## 4. Component Stylings

### Buttons

#### Primary Button
- **Background:** `#D70018` (`{colors.primary}`)
- **Text Color:** `#FFFFFF` (white)
- **Text Style:** `{typography.button-md}` (14px, weight 600)
- **Padding:** `8px 16px`
- **Border:** `1px solid #D70018`
- **Border Radius:** `{rounded.md}` (12px)
- **Box Shadow:** None
- **Height:** 42px
- **Width:** 116px (as measured)

#### Secondary Button (Dark/Black variant)
- **Background:** `#000000`
- **Text Color:** `#FFFFFF`
- **Text Style:** `{typography.button-md}` (14px, weight 600)
- **Padding:** `8px 16px`
- **Border:** `1px solid #000000`
- **Border Radius:** `{rounded.md}` (12px)
- **Box Shadow:** None
- **Height:** 42px
- **Width:** 116px

#### Large Primary Button
- **Background:** `#D70018`
- **Text Color:** `#FFFFFF`
- **Text Style:** `{typography.button-lg}` (16px, weight 600, uppercase)
- **Padding:** `8px 16px`
- **Border:** `1px solid #D70018`
- **Border Radius:** `{rounded.sm}` (8px)
- **Box Shadow:** None
- **Height:** 40px
- **Width:** 282px (as measured)

#### Ghost / Outlined Button
- **Background:** `#EFF5FF` (light blue tint, hover-derived)
- **Text Color:** `#000000`
- **Text Style:** `{typography.button-md}` (14px, weight 400)
- **Padding:** `0px`
- **Border:** `3px solid #609AF6` (info blue)
- **Border Radius:** `16px 16px 0px 0px` (asymmetric; top rounded, bottom sharp)
- **Box Shadow:** None
- **Height:** 63.98px (as measured)
- **Width:** 404px (as measured)

### Cards & Containers

#### Product Card
- **Background:** `#FFFFFF`
- **Border:** 1px `{colors.hairline}` (`#CFCFD3`)
- **Border Radius:** `{rounded.xs}` (6px)
- **Padding:** `{spacing.md}` (16px)
- **Box Shadow:** `{rounded.md}` (12px; subtle inset lift as measured)
- **Text Color:** `{colors.body}` (`#1D1D20`)

#### Section Container (Alternating)
- **Background:** Alternates between `#FFFFFF` and `{colors.surface-alt}` (`#F2F2F3`)
- **Padding:** `{spacing.section}` (120px top/bottom) on desktop; `{spacing.lg}` (20px) on mobile
- **Border Radius:** `{rounded.none}` (0px; full-width sections)

#### Hero Section
- **Background:** Gradient (`linear-gradient(188.66deg, rgb(239, 245, 255) 28.75%, rgba(244, 251, 255, 0.4) 87.64%)`)
- **Overlay:** Optional gradient (`linear-gradient(in oklab, rgb(228, 84, 100) 0px, rgb(215, 0, 24) 100%)`)
- **Padding:** `{spacing.xl}` (24px horizontal) on mobile; `{spacing.xxxl}` (36px) on desktop
- **Border Radius:** `{rounded.md}` (12px)

### Inputs & Forms

#### Text Input
- **Background:** `#FFFFFF`
- **Text Color:** `{colors.body}` (`#1D1D20`)
- **Placeholder Color:** `{colors.neutral-1}` (`#71717A`)
- **Text Style:** `{typography.label-sm}` (14px, weight 400)
- **Padding:** `{spacing.md}` (16px)
- **Border:** `1px solid {colors.hairline}` (`#CFCFD3`)
- **Border Radius:** `{rounded.none}` (0px; sharp corners)
- **Box Shadow:** None
- **Height:** 44px (standard form height)
- **Focus State:** Border color shifts to `{colors.info}` (`#3B82F6`)

#### Select / Dropdown
- **Background:** `#FFFFFF`
- **Text Color:** `{colors.body}`
- **Text Style:** `{typography.label-sm}` (14px, weight 400)
- **Padding:** `{spacing.md}` (16px)
- **Border:** `1px solid {colors.hairline}`
- **Border Radius:** `{rounded.none}` (0px)
- **Dropdown Open State:** Border color `{colors.info}` (`#3B82F6`), shadow elevation md

#### Checkbox / Radio
- **Background (unchecked):** `#FFFFFF`
- **Background (checked):** `{colors.primary}` (`#D70018`)
- **Border:** `1px solid {colors.hairline}`
- **Border Radius:** `{rounded.xs}` (6px)
- **Size:** 16px × 16px

### Navigation

#### Top Navigation Bar
- **Background:** `{colors.primary}` (`#D70018`)
- **Height:** 56px (as measured)
- **Padding:** `{spacing.md}` (16px horizontal)
- **Text Color:** `#FFFFFF`
- **Text Style:** `{typography.body-sm}` (14px, weight 500)
- **Border Radius:** `{rounded.none}` (0px)
- **Box Shadow:** None

#### Navigation Link (Active)
- **Text Color:** `#FFFFFF`
- **Border Bottom:** 2px solid `#FFFFFF`
- **Text Style:** Bold weight (700)

#### Navigation Link (Inactive/Hover)
- **Text Color:** `#FFFFFF` (on red background)
- **Text Decoration:** Underline on hover

#### Breadcrumb / Category Link
- **Text Color:** `{colors.info}` (`#3B82F6`)
- **Text Style:** `{typography.body-sm}` (14px, weight 500)
- **Hover:** Text decoration underline

### Badges & Labels

#### Brand Badge
- **Background:** `{colors.primary}` (`#D70018`)
- **Text Color:** `#FFFFFF`
- **Text Style:** `{typography.caption-xs-strong}` (12px, weight 500)
- **Padding:** `{spacing.xs}` (8px) `{spacing.sm}` (12px)
- **Border Radius:** `{rounded.full}` (9999px; pill-shaped)

#### Info Badge
- **Background:** `{colors.info}` (`#3B82F6`)
- **Text Color:** `#FFFFFF`
- **Text Style:** `{typography.caption-xs-strong}` (12px, weight 500)
- **Padding:** `{spacing.xs}` (8px) `{spacing.sm}` (12px)
- **Border Radius:** `{rounded.full}` (9999px)

#### Neutral Badge
- **Background:** `{colors.surface-alt}` (`#F2F2F3`)
- **Text Color:** `{colors.neutral-1}` (`#71717A`)
- **Text Style:** `{typography.caption-xs}` (12px, weight 400)
- **Padding:** `{spacing.xs}` (8px) `{spacing.sm}` (12px)
- **Border Radius:** `{rounded.full}` (9999px)

---

## 5. Layout Principles

### Spacing System

The spacing scale is a geometric progression based on 4px increments:
- **`{spacing.xxs}`:** 4px — micro-adjustments, tight component gaps
- **`{spacing.xs}`:** 8px — compact margins, badge/button padding
- **`{spacing.sm}`:** 12px — small gaps, field spacing
- **`{spacing.md}`:** 16px — standard content padding, normal component margins
- **`{spacing.lg}`:** 20px — section padding on smaller viewports
- **`{spacing.xl}`:** 24px — generous component spacing, medium section padding
- **`{spacing.xxl}`:** 32px — large section spacing, inter-section gaps
- **`{spacing.xxxl}`:** 36px — premium section padding on tablet+
- **`{spacing.section}`:** 120px — full-width section top/bottom padding (desktop); collapses to `{spacing.lg}` on mobile

**Context:**
- Form groups: `{spacing.md}` (16px) between inputs
- Card padding: `{spacing.md}` (16px) on all sides
- Hero section padding: `{spacing.xl}` (24px) on mobile; `{spacing.xxxl}` (36px) on desktop, horizontal
- Grid gaps: `{spacing.md}` (16px) between product cards

### Grid & Container

- **Max Width:** 1232px (content column at 1280px viewport)
- **Column Strategy:** 
  - Mobile (375px): 1 column with full-width cards
  - Tablet (768px): 6 columns (derived from grid layout; likely 2–3 visible product columns)
  - Desktop (1024px+): 6 columns (3–6 product cards visible depending on card width)
- **Container Padding Horizontal:** 
  - Mobile: `{spacing.xs}` (8px)
  - Tablet: `{spacing.xs}` (8px)
  - Desktop (1280px+): `{spacing.md}` (16px)
- **Section Pattern:** Full-width alternating bands with centered max-width content area

### Whitespace Philosophy

CellphoneS employs generous whitespace to emphasize product focus and reduce cognitive load. Large sections (120px vertical padding) create breathing room between promotions and product grids. Horizontal gutters remain tight (8–16px) to maximize mobile screen real estate. Text rarely spans edge-to-edge; content containers maintain consistent margins. Whitespace increases with viewport size, ensuring the layout scales gracefully without cramping.

### Border Radius Scale

| Radius | Value | Components |
|---|---|---|
| Sharp | `{rounded.none}` (0px) | Inputs, full-width sections, image containers, footer |
| Extra Small | `{rounded.xs}` (6px) | Product card borders, small badges, tight containers |
| Small | `{rounded.sm}` (8px) | Overlay modals, button small variants, medium inputs |
| Medium | `{rounded.md}` (12px) | Primary buttons, standard cards, navigational dropdowns |
| Full | `{rounded.full}` (9999px) | CTA buttons (pill-shaped), badge pills, icon buttons |

**Note:** Button corners measure asymmetric in one variant: `16px 16px 0px 0px` (top rounded, bottom sharp); this is a calculated exception, not a standard radius value.

### Border Widths

| Width | Value | Usage |
|---|---|---|
| Thin | 1px | Default borders, input outlines, card edges, dividers |
| Medium | 3px | Outlined button borders, emphasis strokes, high-contrast dividers |

---

## 6. Depth & Elevation

### Elevation Scale

| Level | Treatment | Use |
|---|---|---|
| Flat | No shadow | Canvas background, section bands, form inputs |
| Micro | `rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.1) 0px 4px 6px -4px` | Button hover state, slight lift on interactive elements |
| Inset | `rgba(0, 0, 0, 0.05) -1px 0px 10px 0px inset, rgba(0, 0, 0, 0.03) 0px 2px 8px 0px` | Recessed button states, inset borders, secondary depth |
| Medium | `rgba(0, 0, 0, 0.11) 0px 4px 20px -8px, rgba(0, 0, 0, 0.06) 0px 0px 10px 0px` | Elevated cards, dropdown menus, modal overlays |

**Shadow Philosophy:**

CellphoneS employs a **layered-micro** elevation strategy. Rather than bold, single-layer shadows, depth emerges from near-transparent stacked layers. Most interactive elements receive a barely-perceptible lift (10–15px blur, 0.05–0.1 opacity black). This creates refinement without visual heaviness, keeping the bright red brand and product imagery as the focal point. Inset shadows on secondary button states suggest subtle press-in, reinforcing tactile feedback without requiring explicit focus states.

### Opacity Levels

| Level | Value | Usage |
|---|---|---|
| Disabled | 0.70 | Hover overlay on images, subtle transparency |
| Standard | 0.98–0.99 | Modal backdrops, semi-transparent overlays |
| Full | 1.00 | Solid fills, primary surfaces, text |

### Z-index / Layering

| Layer | Z-index | Purpose |
|---|---|---|
| Base | 1 | Default card and content stacking |
| Dropdown | 10–20 | Navigation dropdowns, category menus |
| Modal | 1000 | Full-screen overlays, lightboxes, alerts |

---

## 7. Do's and Don'ts

### Do
- **Use the primary red (`#D70018`) for all primary CTAs.** Every main call-to-action button, form submission, and critical link should use the brand red with white text.
- **Apply uppercase typography to high-impact zones.** Display text, section headings, and promotional copy benefit from uppercase styling to signal urgency and scan-ability.
- **Maintain pill-shaped buttons for main CTAs.** Use `{rounded.full}` (9999px) on large primary buttons to create a distinctive, inviting interaction model.
- **Stack spacing using the defined scale.** Always use values from `{spacing.xxs}` through `{spacing.section}` rather than arbitrary pixel values.
- **Nest shadows sparingly.** Rely on surface color alternation and border refinement before adding shadows; when shadows are needed, use the micro or inset treatments.
- **Ensure `{colors.hairline}` dividers separate major sections.** Subtle 1px borders between product rows and sections maintain structure without visual clutter.
- **Layer interactive states with color changes first.** Hover, focus, and active states should shift border color or background before introducing shadow elevation.
- **Test form inputs on mobile with minimum 44px height.** Ensure all form controls meet touch target guidelines.

### Don't
- **Don't use multiple bright accent colors in a single layout.** Stick to primary red and the info blue (`#3B82F6`) for interactive states; decorative accents should remain subtle.
- **Don't apply rounded corners to input fields.** Inputs and form containers use sharp (`{rounded.none}`) corners to signal functional precision and form seriousness.
- **Don't break the spacing scale.** Avoid arbitrary padding or margins outside the defined increments; this ensures consistency across responsive layouts.
- **Don't hide navigation without a menu toggle.** On mobile, always provide a hamburger or menu icon if links are hidden; the site measures 0 visible nav links across all viewports.
- **Don't use decorative colours (`#2B2B30`, `#2570EB`) as functional roles.** These have no measured semantic use; reserve them for illustrations, icons, or brand graphics only.
- **Don't apply shadows to every interactive element.** Use color and border changes as the primary feedback mechanism; shadow elevation should be rare and measured.
- **Don't exceed a max-width of 1232px for content.** Maintain this constraint to preserve focus and readability on ultra-wide displays.
- **Don't shrink section padding below `{spacing.lg}` (20px) on mobile.** Cramped layouts feel cluttered; preserve breathing room even on small screens.

---

## 8. Responsive Behavior

### Breakpoints

| Viewport | Content Width | Grid Columns | Layout Changes | Heading Size | Section Padding X |
|---|---|---|---|---|---|
| 375px (Mobile) | 367px | 5 | Single column product layout; nav toggle visible | `{typography.heading-sm}` (20px) | `{spacing.xs}` (8px) |
| 768px (Tablet) | 752px | 6 | Multi-column grid emerges; nav still collapsed | `{typography.heading-sm}` (20px) | `{spacing.xs}` (8px) |
| 1024px (Desktop) | 1008px | 6 | Full grid layout; sidebar navigation visible (conditional) | `{typography.heading-sm}` (20px) | `{spacing.xs}` (8px) |
| 1280px (Large) | 1232px | 6 | Max-width container; generous gutters | `{typography.heading-sm}` (20px) | `{spacing.md}` (16px) |
| 1440px+ (XL) | 1232px (capped) | 6 | No layout change; centered on screen | `{typography.heading-sm}` (20px) | `{spacing.md}` (16px) |

**Collapse Point:** Navigation links collapse to 0 visible items at all measured breakpoints; a menu toggle is always present.

### Touch Targets

- **Minimum interactive height:** 44px (buttons, form inputs)
- **Minimum interactive width:** 44px (icon buttons, checkboxes)
- **Comfortable tap area:** 48–56px (navigation items, primary CTAs)
- **Spacing between targets:** Minimum `{spacing.md}` (16px) to prevent accidental adjacent taps

### Collapsing Strategy

- **Mobile (375–767px):**
  - Single-column product layout
  - Hero section scales down; text remains uppercase but font sizes stable
  - Section padding collapses to `{spacing.xs}` (8px) horizontal
  - Navigation menu hidden; toggle icon visible
  - Form inputs and buttons stack full-width
  - Grid gaps remain `{spacing.md}` (16px)

- **Tablet (768–1023px):**
  - Multi-column grid emerges (likely 2–3 product columns visible)
  - Navigation still collapsed
  - Section padding remains `{spacing.xs}` (8px)
  - Hero section takes full tablet width
  - Buttons may begin to appear inline for short copy

- **Desktop (1024px+):**
  - Full 6-column grid layout
  - Navigation hidden (measurement shows 0 visible links at all sizes)
  - Section padding stays `{spacing.xs}` (8px) until 1280px
  - Hero section maintains centered max-width
  - Form layouts transition to multi-column

- **Large (1280px+):**
  - Section padding increases to `{spacing.md}` (16px)
  - Content container max-width enforced at 1232px
  - Centered alignment on ultra-wide screens

---

## 9. Agent Prompt Guide

### Quick Color Reference
- **Primary CTA:** `{colors.primary}` (`#D70018`) — all main buttons and brand accents
- **Background/Canvas:** `{colors.canvas}` (`#FFFFFF`) — default page and surface fill
- **Alternate Section:** `{colors.surface-alt}` (`#F2F2F3`) — every other section band
- **Heading Text:** `{colors.body}` (`#1D1D20`) — primary text and headlines
- **Body Text:** `{colors.body}` (`#1D1D20`) — body copy, same as headings
- **Interactive/Links:** `{colors.info}` (`#3B82F6`) — secondary CTAs, link colors, focus states
- **Borders/Dividers:** `{colors.hairline}` (`#CFCFD3`) — 1px card edges, section dividers
- **Secondary Text:** `{colors.neutral-1}` (`#71717A`) — placeholders, captions, metadata

### Iteration Guide

1. **Establish the red foundation first.** Every design begins with `#D70018` on primary buttons, top nav, and brand accents. This is non-negotiable.

2. **Use uppercase typography on high-visibility elements.** Section headings, promotional text, and button labels should default to uppercase using weights 600–800.

3. **Build spacing from the defined scale only.** Do not invent padding or margin values; choose from 4px, 8px, 12px, 16px, 20px, 24px, 32px, 36px, or 120px (section rhythm).

4. **Limit shadows to three scenarios:** hover lift (micro shadow), recessed states (inset shadow), or modal elevation (medium shadow). Avoid flat design except on canvas and inputs.

5. **Keep borders sharp on inputs and rounded on buttons.** Inputs use `0px` radius (sharp); primary CTAs use `9999px` (pill); other containers use `12px` (medium).

6. **Color alternation creates visual rhythm—not shadows.** Sections alternate between white and light gray (`#F2F2F3`); this achieves depth without relying on blur effects.

7. **Form inputs must hit 44px minimum height** for mobile touch targets; use `{spacing.md}` (16px) padding on all sides.

8. **Info blue (`#3B82F6`) is the only secondary brand color.** All links, secondary buttons, focus states, and info badges use this blue; it provides contrast against the warm red.

9. **Responsive padding shifts at 1280px:** Mobile and tablet use `{spacing.xs}` (8px) horizontal section padding; desktop and large use `{spacing.md}` (16px).

10. **Never exceed 1232px max-width** on content containers; this ensures readable line lengths and proper aspect ratios on ultra-wide displays.

---

## 10. Known Gaps

- **Interaction states partially inferred:** The extraction detected some hover and disabled states (e.g. `borderColor` changes, `opacity` modulation) but did not capture all interaction feedback scenarios (e.g. focus rings, keyboard navigation, loading states, toast notifications). Surfaces behind authentication were not visited.

- **No measured dark mode or theme variant:** The extraction analyzed a single light theme. If the brand ships a dark mode or alternate theme, it was not sampled and should be documented separately.

- **5 extracted colors lack semantic roles:** The colors `#2B2B30` and `#2570EB` are present in the token data but have no measured on-site usage. They are listed as decorative/unassigned; do not assume they have functional roles.

- **Gradient opacity and angle specificity:** Hero gradients were extracted verbatim, but edge-case gradient behavior (e.g. animation, overflow rendering) is not specified here.

- **No micro-interaction timing:** Transition durations, animation curves, and scroll-triggered effects were not extracted; UI motion patterns cannot be replicated from this document alone.

- **Elevation strategy is inferred from measurements:** The classification as "layered-micro" reflects the measured shadow values; however, explicit elevation guidelines in the brand's documentation (if any) were not accessible.

- **Breakpoint refinement required:** The measured breakpoints show content columns at specific widths, but exact trigger points for layout shifts (e.g. sidebar collapse, grid reflow) require live testing or code inspection.

- **Component coverage limits:** Only buttons, cards, inputs, navigation, and badges are documented. Other patterns (modals, popovers, tooltips, breadcrumbs, hero imagery sizing) are not fully specified.

- **Measurement scope:** Only 1 page analyzed (homepage). Internal product pages, checkout flows, and user account surfaces may have distinct patterns not captured here.

---