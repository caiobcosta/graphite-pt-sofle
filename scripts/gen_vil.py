"""Build a Vial .vil for the Tergo Sofle (wired, rev0) with the Graphite-PT keymap.
Layer indices follow the stock firmware: 0 Basic, 1 Adept, 2 Custom, 3 Symbols/Nav (L2),
4 Adjust (L3), 5 Media (L4), 6 Numpad (L5), 7 Mouse. Layers 8-15 are empty."""
import json
from pathlib import Path
import urllib.request
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache"; CACHE.mkdir(exist_ok=True)
def fetch(url, name):
    """Download a third-party reference file once into cache/ (not committed)."""
    p = CACHE / name
    if not p.exists():
        urllib.request.urlretrieve(url, p)
    return p
TERGO_INFO = ("https://raw.githubusercontent.com/TergoTeclados/vial-qmk-firmware/vial/keyboards/tergo_sofle/rev0/info.json", "tergo_sofle_rev0_info.json")
SOFLE_GEO = ("https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/sofle/rev1/keyboard.json", "sofle_rev1_keyboard.json")
VIAL_KC = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/keycodes/keycodes.py", "vial_keycodes.py")
VIAL_ANY = ("https://raw.githubusercontent.com/vial-kb/vial-gui/main/src/main/python/any_keycode.py", "vial_any_keycode.py")
INFO = json.load(open(fetch(*TERGO_INFO)))
POS = [tuple(k["matrix"]) for k in INFO["layouts"]["LAYOUT"]["layout"]]   # 60 LAYOUT slots -> (row, col)
ROWS, COLS, LAYERS = 10, 6, 16
UID = int.from_bytes(bytes([0x05, 0xCD, 0x9F, 0x8A, 0xF4, 0xDF, 0xDE, 0xB2]), "little")

_ = "KC_TRNS"; X = "KC_NO"
# ABNT2 physical keys (OS input source = Portuguese Brazil ABNT2)
CCED, ACUT, TILD, QUOT_BR = "KC_SCLN", "KC_LBRC", "KC_QUOT", "KC_GRV"
SCLN_BR, SLSH_BR = "KC_SLSH", "KC_RO"            # ;:  and  /?
LBRC_BR, RBRC_BR, BSLS_BR = "KC_RBRC", "KC_BSLS", "KC_NUBS"
def S_(k): return f"LSFT({k})"
GRAVE_BR, CIRC_BR = S_(ACUT), S_(TILD)             # ` and ^ are Shift+dead keys on ABNT2
SYMB, ADJ, MEDIA, NUMPAD, MOUSE = 3, 4, 5, 6, 7

def layout(rows):
    """rows: list of 60 keycodes in LAYOUT order."""
    assert len(rows) == 60, len(rows)
    grid = [[X]*COLS for _ in range(ROWS)]
    for kc, (r, c) in zip(rows, POS): grid[r][c] = kc
    return grid

BASE = layout([
 "KC_ESC","KC_1","KC_2","KC_3","KC_4","KC_5",                         "KC_6","KC_7","KC_8","KC_9","KC_0","KC_MINS",
 "KC_TAB","KC_B","KC_L","KC_D","KC_V","KC_Z",                         QUOT_BR,"KC_F","KC_U","KC_O","KC_J","KC_EQL",
 "KC_LSFT","KC_N","KC_R","KC_T","KC_S","KC_G",                        "KC_Y","KC_H","KC_A","KC_E","KC_I","KC_RSFT",
 CCED,"KC_Q","KC_X","KC_M","KC_C","KC_W", f"MO({MEDIA})",   "TD(0)",   "KC_K","KC_P","KC_COMM","KC_DOT",SCLN_BR,SLSH_BR,
          "TD(1)",TILD,ACUT,f"MO({SYMB})","KC_SPC",          "KC_ENT","KC_BSPC","KC_RGUI","KC_RALT","KC_RCTL",
])
ADEPT = layout([_]*60)        # stock Adept = home-row mods on QWERTY positions; left empty on purpose (see message)
CUSTOM = [row[:] for row in BASE]
SYMBNAV = layout([
 "KC_F1","KC_F2","KC_F3","KC_F4","KC_F5","KC_F6",                     "KC_F7","KC_F8","KC_F9","KC_F10","KC_F11","KC_F12",
 "KC_INS",GRAVE_BR,CIRC_BR,S_("KC_EQL"),S_(LBRC_BR),S_(RBRC_BR),       "KC_PGUP","KC_HOME","KC_UP","KC_END",S_(LBRC_BR),S_(RBRC_BR),
 "KC_PSCR",TILD,"KC_EQL","KC_MINS",S_("KC_9"),S_("KC_0"),              "KC_PGDN","KC_LEFT","KC_DOWN","KC_RGHT",S_("KC_9"),S_("KC_0"),
 "KC_PAUS",BSLS_BR,S_(BSLS_BR),S_("KC_MINS"),LBRC_BR,RBRC_BR, _, _,    "USER02","LALT(KC_LEFT)","KC_ESC","LALT(KC_RGHT)",LBRC_BR,RBRC_BR,
          _,_,_,_,_,                                                  "LALT(KC_8)","KC_DEL","LALT(KC_RBRC)","LALT(KC_BSLS)","LSA(KC_0)",   # • DEL ª º °
])
ADJUST = layout([
 _,_,_,_,_,_,                                                          _,_,_,_,_,_,
 "RGB_SPI","RGB_VAI","RGB_SAI","RGB_HUI","RGB_MOD","RGB_TOG",          X,X,X,X,X,_,
 "RGB_SPD","RGB_VAD","RGB_SAD","RGB_HUD","RGB_RMOD","USER00",          X,X,X,X,X,_,
 _,X,"DF(0)","DF(1)","DF(2)","USER01", _,                     _,       X,X,X,X,"NK_TOGG",_,
          _,_,_,_,_,                                                  _,_,_,_,_,
])
MEDIAL = layout([
 _,_,_,_,_,_,                                                          _,_,_,_,_,_,
 _,X,X,X,X,X,                                                          X,X,X,X,X,_,
 _,X,X,X,X,X,                                                          X,"KC_VOLD","KC_MUTE","KC_VOLU",X,_,
 _,X,X,X,X,X, _,                                               _,       X,"KC_MPRV","KC_MPLY","KC_MNXT",X,_,
          _,_,_,_,_,                                                  _,_,_,_,_,
])
NUMPADL = layout([
 _,_,_,_,_,_,                                                          X,"KC_NLCK","KC_PSLS","KC_PAST","KC_PMNS",_,
 _,X,X,X,X,X,                                                          X,"KC_P7","KC_P8","KC_P9","KC_PPLS",_,
 _,X,X,X,X,X,                                                          X,"KC_P4","KC_P5","KC_P6","KC_PPLS",_,
 _,X,X,X,X,X, _,                                               _,       X,"KC_P1","KC_P2","KC_P3","KC_PENT",_,
          _,_,_,_,_,                                                  _,"KC_COMM","KC_P0","KC_P0","KC_PDOT",
])
MOUSEL = layout([
 _,_,_,_,_,_,                                                          _,_,_,_,_,_,
 _,X,X,X,X,X,                                                          "KC_WH_U",X,"KC_MS_U",X,X,_,
 _,"KC_LGUI","KC_LALT","KC_LCTL","KC_LSFT",X,                          "KC_WH_D","KC_MS_L","KC_MS_D","KC_MS_R",X,_,
 _,"LGUI(KC_Z)","LGUI(KC_X)","LGUI(KC_C)","LGUI(KC_V)",X, _,   _,       X,X,X,X,X,_,
          _,_,_,_,_,                                                  "KC_BTN2","KC_BTN1","KC_BTN3",_,_,
])
EMPTY = layout([_]*60)
layers = [BASE, ADEPT, CUSTOM, SYMBNAV, ADJUST, MEDIAL, NUMPADL, MOUSEL] + [EMPTY]*8
assert len(layers) == LAYERS

# encoders: [ccw, cw] per (layer, encoder); 0 = left (L4), 1 = right (L3)
enc0 = [["KC_WH_L","KC_WH_R"], ["LGUI(KC_EQL)","LGUI(KC_MINS)"]]
encoders = [enc0] + [[[_,_],[_,_]] for _l in range(LAYERS-1)]

# tap dance 0 (right encoder click): tap = Cmd+0 (zoom 100%), hold = layer 4 (L3)
tap_dance = [["LGUI(KC_0)", f"MO({ADJ})", "KC_NO", "KC_NO", 300],
             [CIRC_BR, f"MO({NUMPAD})", "KC_NO", "KC_NO", 200]]   # 1st left thumb: tap = ^ (dead), hold = numpad

# QMK settings as exported from the author's keyboard (tapping term etc.). Replace with {} to keep yours.
QMK_SETTINGS = {"1": 0, "2": 50, "3": 0, "4": 175, "5": 5, "6": 5000, "7": 300, "8": 3, "9": 0, "10": 16, "11": 8, "12": 5, "13": 32, "14": 0, "15": 80, "16": 8, "17": 40, "18": 10, "19": 80, "20": 5, "21": 0}
vil = {"version": 1, "uid": UID, "layout": layers, "encoder_layout": encoders,
       "layout_options": -1, "macro": [], "vial_protocol": 6, "via_protocol": 9,
       "tap_dance": tap_dance, "combo": [], "key_override": [], "alt_repeat_key": [], "settings": QMK_SETTINGS}
out = ROOT / "keymap" / "tergo-sofle-graphite-pt.vil"
json.dump(vil, open(out, "w"), ensure_ascii=False)
print("wrote", out, "uid", UID)
