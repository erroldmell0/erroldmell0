# How this profile README is built

`build_card.py` generates `dark.svg` and `light.svg` -- the terminal card the README
embeds. The README picks between them with `<picture>` + `prefers-color-scheme`.

## Regenerating

```bash
pip install pillow
python build_card.py
```

Then bump the `?v=` on the image URLs in `README.md` -- without it
`raw.githubusercontent.com` keeps serving the cached copy for a few minutes.

## Editing the card

Everything on the right-hand panel lives in `LINES` in `build_card.py`. Rows are
`(label, value)`; `__head__`, `__blank__` and `__section__` are layout rows. Keep the list at 25 entries or fewer -- beyond that the text overflows the
panel. Values are capped at ~48 characters for the same reason.

To change the portrait, drop a new `avatar.png` in and adjust `CROP` (a
left/top/right/bottom box in source pixels). A tight crop on the subject reads
far better than the full frame -- busy backgrounds turn to noise at this scale.

## Why almost nothing animates

GitHub renders this SVG inside `<img>`, and in that context the SMIL timeline
never advances past `t=0`. Any animation whose value at `t=0` hides its element
(`opacity="0"`, `width="0"`, a reveal mask at `height="0"`) therefore hides it
permanently -- the card renders as an empty terminal frame. Every element must be
fully visible with no animation applied; decorative loops are fine only when
their first keyframe is the visible state.
