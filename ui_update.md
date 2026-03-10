# Groove Log — UI Redesign Decisions

This document captures every design decision for the UI overhaul. Use it as a reference when making further changes or asking an agent to modify specific aspects.

---

## Phase 1: Theme System

### D1: CSS Custom Properties
Replace all 46 hardcoded color values in App.css with CSS custom properties on `:root` (light theme) and `[data-theme="dark"]` (dark theme). This is the single prerequisite for all other visual changes.

```css
:root {
  --bg: #FAF7F2;
  --surface: #F0EBE3;
  --text-primary: #1A1714;
  --text-secondary: #7A6F62;
  --border: #E0D8CE;
  --accent: #D4A843;
  --accent-hover: #E8C060;
  --danger: #C45040;
  --success: #6B8F5E;
}
[data-theme="dark"] {
  --bg: #1A1714;
  --surface: #2A2520;
  --text-primary: #F5F0E8;
  --text-secondary: #A09888;
  --border: #3A3530;
}
```

### D2: Dark Theme
Add `[data-theme="dark"]` overrides plus `@media (prefers-color-scheme: dark)` as fallback when no manual preference is stored. Dark theme should feel like "a dimly lit record store."

### D3: ThemeProvider Context
Create a React context that reads localStorage for saved preference, falls back to `prefers-color-scheme`, sets `data-theme` attribute on `<html>`, and exposes `toggleTheme()`.

### D4: Theme Toggle in Nav
Sun/moon icon button at the far right of the sticky top bar. Ghost style: no background, `var(--text-secondary)`, amber on hover.

---

## Phase 2: Color Corrections

### D5: Replace Blue with Amber
Replace every instance of `#4a90d9` (blue) with `var(--accent)` / `var(--accent-hover)`. Affects: active tabs, primary buttons, spinner, progress bars, focus rings, checkboxes, toggle switch, upload hover, undo links, selection toolbar.

### D6: Replace Green Action Buttons with Amber
Green `#2e7d32` is only for success text/status indicators. All action buttons (Add to Collection, Fetch Collection, Sync progress) use `var(--accent)` instead.

### D7: Standardize Danger Red
Replace three different reds (`#c0392b`, `#c62828`, `#b71c1c`) with a single `var(--danger)` (#C45040) across all destructive buttons, error messages, and disconnect actions.

### D8: Standardize Success Green
Replace `#2e7d32` in `.login-success` and `.collection-delete-message` with `var(--success)` (#6B8F5E).

### D9: Warm All Neutral Grays
Replace every cool gray with its warm equivalent:
- `#fff` / `#f5f5f5` / `#fafafa` → `var(--bg)` or `var(--surface)`
- `#e0e0e0` / `#eee` / `#ccc` → `var(--border)`
- `#888` / `#999` / `#666` / `#555` → `var(--text-secondary)`
- `#333` / `#1a1a1a` → `var(--text-primary)`

---

## Phase 3: Navigation & Information Architecture

### D10: Consolidate Nav to Two Primary Items + Avatar
Merge Single Search and Batch into one "Identify" page (with sub-cards/toggle for single vs batch). Keep Collection as a top-level destination. Move Review and Issues to sub-views within Identify (shown via badge counters). Move Profile to an avatar button/dropdown at far right of nav. Result: `[Identify] [Collection]` on left, `[theme toggle] [avatar]` on right.

### D11: Logo in Nav Bar, Left-Aligned
Place the icon (5rem) + wordmark (4rem) horizontal lockup at the left edge of a sticky top bar. Remove the separate centered `.app-header` section that currently displays the logo below tabs.

### D12: Remove Subtitle from Authenticated Views
"Identify your records by photo" only appears on the login page. Returning users don't need it.

### D13: Default Route to Collection
If the user has a synced collection (`completed_at` is set), route `/` to `/collection`. If no collection, route to `/identify`.

### D14: Review and Issues as Contextual Sub-views
Within Identify, show badge/counter for pending review items. Review and Issues appear as sub-tabs below the upload area, not as top-level nav destinations.

---

## Phase 4: Card & Layout Styling

### D15: Remove Borders from All Cards
Remove `border: 1px solid #e0e0e0` from all cards. Use `var(--surface)` background against `var(--bg)` for contrast. In light mode, add subtle shadow `0 1px 3px rgba(26,23,20,0.06)`.

### D16: Square Album Art (No Rounded Corners)
Set `border-radius: 0` on `.collection-cover`, `.result-cover`, and collection card top overflow clip. Per branding: "records are square."

### D17: Hover Lift on Collection Cards
On hover: `transform: translateY(-2px)`, `box-shadow: 0 4px 12px rgba(26,23,20,0.08)`, `border-bottom: 2px solid var(--accent)`. Add `transition: transform 0.2s, box-shadow 0.2s`.

### D18: Larger Collection Cards
Change preferred card width from 180px to 220px (`minmax(200px, 1fr)`). Album art should be prominent.

### D19: Restyle Inputs (LITA-Inspired)
`var(--surface)` background, bottom-border-only style (`1px solid var(--border)`), upgrading to `var(--accent)` on focus. Placeholder in `var(--text-secondary)`.

### D20: Warm Upload Zone
Hover/drag: amber border + warm amber tint `rgba(212,168,67,0.06)`. Idle dashed border: `var(--border)`.

### D21: Warm Modal Overlays
Backdrop: `rgba(26,23,20,0.5)` light / `rgba(26,23,20,0.85)` dark. Modal background: `var(--surface)`.

### D22: Warm Selection Toolbar
Background: `rgba(212,168,67,0.08)` with `border-color: var(--accent)`. Selected card outline: `var(--accent)`.

### D23: Missing-Cover Placeholder
`var(--surface)` background + centered vinyl icon (from `vinyl.svg` — copy `~/Downloads/vinyl.svg` to `frontend/src/assets/vinyl.svg`, replacing the old one) at 40% size in `var(--text-secondary)` at 30% opacity.

---

## Phase 5: Typography

### D24: Load JetBrains Mono
Add `JetBrains+Mono:wght@400` to Google Fonts link in `index.html`.

### D25: Apply JetBrains Mono to Metadata
Use `font-family: 'JetBrains Mono', monospace` on: `.result-meta span`, `.collection-card-meta span`, `.debug-panel` children. Font size: `0.75rem`.

### D26: Apply Noto Serif Display Consistently
Ensure all heading-like elements (profile section titles, issues section titles, batch summary, empty state headings, public collection owner name) use `font-family: 'Noto Serif Display'`.

### D27: Lowercase App Title
Change `<title>Groove Log</title>` to `<title>groove log</title>`.

---

## Phase 6: Button System

### D34: Redefine Button Variants
- **Primary**: `var(--accent)` background, `#1A1714` text, `4px` border-radius, hover `var(--accent-hover)`.
- **Secondary**: transparent background, amber border, amber text, hover fills amber at 10% opacity.
- **Danger**: `var(--danger)` background, cream/white text.
- **Ghost**: no border, `var(--text-secondary)` text, hover reveals `var(--surface)` background.

### D35: Fix btn-nav
Change from blue tint to secondary style: transparent background, `var(--text-secondary)` text, `var(--surface)` on hover.

---

## Phase 7: Interaction Polish

### D28: Vinyl Spinner
Replace the generic CSS border-spinner with a rotating `vinyl.svg` (from `frontend/src/assets/vinyl.svg`). CSS animation: `rotate(360deg)` over 1.2s linear infinite. Color via `currentColor` in `var(--text-secondary)`. Use everywhere `.spinner` appears.

### D29: Skeleton Loading for Collection Grid
When loading, render 8-12 placeholder cards with `var(--surface)` background and shimmer animation (linear-gradient sweep from `var(--surface)` to `var(--border)` and back).

### D30: Improve Empty States
Each empty state gets the vinyl icon at 3rem in `var(--text-secondary)` at 40% opacity plus warm copy:
- Empty collection: "No records yet. Sync from Discogs to get started."
- Empty review: "All caught up. Upload photos to identify more records."
- Empty issues: "No issues — everything looks good."

### D31: Toast Notification System
Bottom-center toast container. Style: `var(--surface)` background, box-shadow, 2px left border (`var(--accent)` success, `var(--danger)` errors), auto-dismiss 3s with fade-out. Use for: "Added to collection", "Deleted N records", "Link copied", "Sync started".

### D32: Page Transition Animations
Route content gets a 200ms fade-in (opacity 0→1) on mount. CSS-only `@keyframes fadeIn`.

### D33: Accessible Focus Rings
Global `:focus-visible` style: `outline: 2px solid var(--accent); outline-offset: 2px`. Remove all `outline: none` declarations.

---

## Phase 8: Iconography

### D36: Consistent Icon Style
All SVG icons should be thin line (1.5-2px stroke), not filled. Default color: `currentColor` inheriting `var(--text-secondary)`. Replace any filled icons (`vinyl.svg`, `cd.svg`, `single-search.svg`, `batch.svg`, `hide.svg`, `view.svg`) with line-style versions using `currentColor`.

### D37: Active Tab Icon Color
`.mode-tab.active .tab-icon`: tint amber via CSS `filter` or `color` change, not just opacity increase.

---

## Phase 9: Login Page

### D38: Rebrand Login Page
Background: `var(--bg)`. Card: `var(--surface)`. Logo: horizontal lockup (icon left of wordmark). Primary button: amber. Input focus: amber. Google button hover: `var(--surface)`. Link buttons: amber text. Divider: `var(--border)`.

### D39: Warm Login Subtitle
Change to something shorter and on-brand. Consider: "Your records, identified." or just remove entirely.

---

## Phase 10: Miscellaneous

### D40: Human-Friendly Error Copy
Audit all error strings. Use conversational phrasing: "Couldn't reach Discogs. Try again?" not "Error 503: Service Unavailable."

### D41: Toggle Switch to Amber
`.toggle-switch.toggle-on` background: `var(--accent)`.

### D42: Avatar Border Warm
`.profile-avatar-large` border: `var(--border)`.

### D43: Drop Dark Mode
Remove dark mode entirely. Delete `ThemeContext.tsx`, remove `ThemeProvider` wrapper from `App.tsx`, remove `ThemeToggle` component, remove `[data-theme="dark"]` and `@media (prefers-color-scheme: dark)` blocks from `index.css`, remove `.btn-theme-toggle` CSS. Light-only for now. **Status: DONE**

### D44: Vibrant Color Palette (Mamdani-inspired)
Replace the muted amber palette with a more vibrant, energetic one inspired by the Zohran Mamdani campaign (warm, energetic, approachable):
- `--accent`: `#D4A843` → `#F5A623` (vibrant amber)
- `--accent-hover`: `#E8C060` → `#FFB938`
- `--accent-text`: `#8F6E1A` → `#B07A0A`
- `--accent-subtle`: updated to match
- `--danger`: `#C45040` → `#E84230` (warmer vermillion)
- `--danger-subtle`: updated to match
**Status: DONE**

### D45: Swap Heading Font to Coustard
Replace Noto Serif Display with Coustard (chunky vintage serif, 400/900 weights). Updated Google Fonts link and all CSS references. **Status: DONE**

### D46: Zohran-Inspired Color Palette
Full palette swap based on Zohran Mamdani campaign colors:
- `--bg`: `#F4E3CD` (beige), `--surface`: `#ECD5B8`
- `--accent`: `#2B1BDF` (lighter blue), `--accent-text`: `#2717B0` (deeper blue)
- `--accent-hover`: `#3D2EF0`, `--on-accent`: `#F4E3CD` (beige on blue)
- `--danger`: `#F31C05` (red), `--on-danger`: `#FFFFFF`
- `--text-primary`: `#1A1520`, `--text-secondary`: `#5C4F6A`
- Yellow `#F49E03` available as secondary accent (not yet assigned to a token)
**Status: DONE**

### D48: Outline-Style Action Buttons
Change the "Wrong", "Dismiss", and "Accept + Add" buttons (and similar action buttons in BatchReview/ReviewView) from filled backgrounds to outline style: transparent background, colored border, colored text. On hover, fill with the color at low opacity. This matches the vintage/editorial aesthetic better and reduces visual weight competing with album art. Applies to `.btn-wrong`, `.btn-dismiss`, `.btn-collection` (and variants).

### D47: Logo SVGs — Beige Fill with Blue Outline
Updated `icon.svg` and `logo.svg`: `fill="#F4E3CD"` with `stroke="#2717B0"` and `paint-order="stroke fill"`. Removed `currentColor`. TODO: finalize stroke width in a vector editor and expand strokes to paths. **Status: IN PROGRESS**

---

## Security Findings (From Review)

These should be addressed alongside the UI update:

| # | Severity | Issue | File |
|---|----------|-------|------|
| S1 | HIGH | Open redirect via unvalidated `authorize_url` | `DiscogsAuth.tsx:32`, `ProfilePage.tsx:141` |
| S2 | HIGH | No file size limit on image upload — add 5 MB max (largest real label is 2.6 MB) | `ImageUpload.tsx:19-26` |
| S3 | HIGH | No file size limit on batch ZIP upload — add 750 MB max (150 images × 5 MB) | `BatchUpload.tsx:16-21` |
| S4 | MEDIUM | No file size gate before avatar resize — add 10 MB pre-resize check to prevent decompression bombs (the `resizeImage()` function already compresses to 256×256 JPEG, so this is only a memory safety gate) | `ProfilePage.tsx:83-90` |
| S5 | MEDIUM | Clipboard API failure silently ignored | `CollectionView.tsx:303-309` |
| S6 | MEDIUM | Settings fetch error silently defaults (shows wrong state) | `ProfilePage.tsx:57-64` |
| S7 | MEDIUM | Price API errors silently suppressed at two levels | `api.ts:254-258`, `ResultCard.tsx:24` |

---

## Architecture Notes (From Exploration)

- **46 unique hardcoded colors** in App.css, zero CSS custom properties
- **Dead code**: `DiscogsAuth.tsx` is imported nowhere; `Ranchers` font referenced but never loaded
- **Mixed icon system**: 5/12 SVGs use `currentColor`, 7 have hardcoded black fills
- **No media queries**: responsive behavior is clamp + JS resize listener (inconsistent)
- **`window.confirm()`** in BatchReview (lines 131, 147) — can't be styled, needs custom modal
- **`CollectionView.tsx`** is 561 lines with ~15 state variables — needs decomposition
- **`SingleSearchPage` and `PublicCollectionPage`** defined inline in App.tsx — should be extracted

---

## Implementation Priority

1. **Phase 1** (D1-D4, D9): Theme system — unlocks everything else
2. **Phase 2** (D5-D8): Color corrections — biggest visual impact per effort
3. **Phase 4** (D15-D23): Card/layout — makes the app feel like a record store
4. **Phase 6** (D34-D35): Button system — visual consistency
5. **Phase 3** (D10-D14): Navigation restructure — biggest UX improvement
6. **Phase 5** (D24-D27): Typography refinement
7. **Phase 7** (D28-D33): Interaction polish
8. **Phase 8-10** (D36-D42): Final touches
