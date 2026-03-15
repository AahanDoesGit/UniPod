"""
UNI//POD — Design Tokens
All colors, sizes, and typography constants.
"""

# ── Colors (RGB tuples) ──────────────────────────────────────────────────────
BG_VOID       = (8,   8,   14)    # #08080E  — primary background
BG_SURFACE    = (14,  14,  28)    # #0E0E1C  — navbar, wheel fill
BG_LIFT       = (20,  20,  40)    # #141428  — subtle raised
NEON_PRIMARY  = (0,   255, 209)   # #00FFD1  — main neon accent
NEON_SECONDARY= (123, 47,  255)   # #7B2FFF  — violet accent
NEON_DIM      = (0,   102, 90)    # #00665A  — inactive progress
TEXT_BRIGHT   = (238, 238, 244)   # #EEEEF4  — selected / title text
TEXT_MID      = (136, 136, 170)   # #8888AA  — normal list items
TEXT_DARK     = (58,  58,  90)    # #3A3A5A  — disabled / chevrons
DIVIDER       = (22,  22,  42)    # #16162A  — 1px separators

# Glow flash overlay (alpha handled separately)
GLOW_COLOR    = NEON_PRIMARY

# ── Dimensions ───────────────────────────────────────────────────────────────
SCREEN_W      = 240
SCREEN_H      = 320
NAVBAR_H      = 28
CONTENT_Y     = 38           # navbar height + 10px margin
CONTENT_H     = 170          # usable list area height
SEPARATOR_Y   = 208
WHEEL_Y_START = 212
ITEM_H        = 34
VISIBLE_ROWS  = 5

# Click wheel
WHEEL_CX      = 120
WHEEL_CY      = 266
WHEEL_R_OUTER = 46
WHEEL_R_INNER = 15
WHEEL_FLASH_ALPHA = 140      # ~55% of 255
WHEEL_FLASH_MS    = 180

# Progress ring (Now Playing)
RING_CX       = 120
RING_CY       = 112
RING_R_OUTER  = 50
RING_R_INNER  = 47           # 3px stroke
RING_HALO_R   = 54

# ── Font Sizes ────────────────────────────────────────────────────────────────
FONT_TINY     = 8
FONT_SMALL    = 9
FONT_BODY     = 11
FONT_MEDIUM   = 12
FONT_LARGE    = 13
FONT_TITLE    = 22

# ── Transition ────────────────────────────────────────────────────────────────
TRANSITION_MS    = 200
TRANSITION_STEPS = 10
