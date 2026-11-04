# Graphite-PT for the Tergo Sofle

A keymap for the [Tergo Sofle](https://tecladoergonomico.com.br/loja/tergo-sofle/) (a Sofle v2, wired, Vial firmware, ABNT2 edition) built around the [Graphite](https://github.com/rdavison/graphite-layout) letter layout, adapted for Brazilian Portuguese. The operating system stays on the regular **Portuguese (Brazil) ABNT2** input source; the whole remap lives in the keyboard.

![Base layer with the symbols and numpad layers](cheatsheet/cheatsheet.png)

## The layout

```
ESC   1   2   3   4   5                 6   7   8   9   0   -_
TAB   B   L   D   V   Z                 '   F   U   O   J   =+
SHFT  N   R   T   S   G                 Y   H   A   E   I   SHFT
Ç     Q   X   M   C   W   [L4]   [L3]   K   P   ,   .   ;   /
          ^/L5  ~   ´   L2  SPC   ENT  BKSP CMD OPT CTRL
```

Letters are Graphite with two changes measured on a Brazilian Portuguese corpus:

- **O and U swapped.** It removes the two dominant same-finger bigrams of Portuguese on Graphite, `ao` and `eu`. Same-finger bigrams drop from 2.37% to 1.40% (English stays at 1.08%).
- **V and W swapped.** V is 1.2% of Portuguese letters and sat on the inner bottom key, the hardest reach on a column-staggered board; W (0.06%) takes that key instead.

Everything else follows from the ABNT2 input source: `Ç` is a real key, `´` and `~` are the ABNT2 dead keys and sit on the **left thumb** (2.6 accents per 100 letters, and all vowels are on the right hand, so accent + vowel alternates hands). `Shift+~` gives `^`, `Shift+´` gives `` ` ``.

### Layers

| Layer | Access | Contents |
|---|---|---|
| 0 Base | | letters above |
| 3 Symbols and navigation ("L2") | hold left thumb 4 | F1 to F12, `` ` ^ + { } ``, `~ = - ( )`, `\ \| _ [ ]` on the left; arrows, Home, End, PgUp, PgDn, Caps Word, Opt+arrows, Esc on the right; `{ } ( ) [ ]` mirrored on the right outer columns; `Del` on the Backspace thumb; `•`, `ª`, `º`, `°` on the other right thumbs |
| 6 Numpad ("L5") | hold left thumb 1 | numpad on the right hand, `,` on the Backspace thumb |
| 4 Adjust ("L3") | hold the right encoder | RGB, default layer selection, NKRO |
| 5 Media ("L4") | press the left encoder | volume, play, prev, next |

Left thumb 1 is a tap dance: tap gives `^` (dead), hold gives the numpad layer. The right encoder is a tap dance too: tap sends `Cmd+0` (zoom 100%), hold activates the Adjust layer. Encoders: left turns horizontal scroll, right turns zoom (`Cmd+-` / `Cmd+=`).

The layer numbers follow the stock Tergo firmware (0 Basic, 1 Adept, 2 Custom, 3 Symbols, 4 Adjust, 5 Media, 6 Numpad, 7 Mouse). Layer 1 is left empty on purpose: home-row mods only make sense after the letters are automatic. Layer 7 has no access key.

### Why not Colemak or BR Nativo

Nine layouts were scored on a 1.1 million letter Portuguese corpus (Wikipedia) and a 570 thousand letter English one, simulating a column-staggered split board. Home row use, pinky load, hand alternation, same-finger bigrams (SFB) and index lateral stretches (LSB), Portuguese:

| Layout | home | pinky | alternation | SFB | LSB |
|---|---|---|---|---|---|
| QWERTY ABNT2 | 34% | 18% | 52% | 8.9% | 4.5% |
| Colemak ABNT2 | 75% | 26% | 59% | 2.1% | 0.4% |
| Colemak-DH | 74% | 26% | 59% | 2.1% | 3.2% |
| BR Nativo | 78% | 16% | 77% | 3.1% | 0.9% |
| Gallium v2 | 63% | 15% | 75% | 2.4% | 2.5% |
| Graphite | 60% | 15% | 76% | 2.4% | 0.05% |
| **Graphite-PT** | 61% | 16% | 75% | **1.4%** | 0.04% |

Colemak puts A and O on the pinkies (26% pinky load in Portuguese). BR Nativo is good in Portuguese but poor in English (4% SFB). Both are also OS-level drivers, which a programmable keyboard does not need.

Punctuation placement was measured too. Comma under A costs an `a,` same-finger bigram (0.3%); it was kept there anyway for the familiar `, . ; /` order.

## Installing

Requirements: Tergo Sofle wired with the stock Vial firmware (ABNT2 build), [Vial](https://get.vial.today/), and the **Portuguese (Brazil) ABNT2** input source on the computer (tested on macOS; the `•ªº°` thumb keys use macOS Option combinations and will differ on Windows and Linux).

1. In Vial, save your current layout first (File, Save current layout). Loading a `.vil` replaces every layer, encoder, tap dance and macro.
2. File, Load saved layout, pick `keymap/tergo-sofle-graphite-pt.vil`.
3. Print `cheatsheet/cheatsheet.pdf` (A4 landscape). `cheatsheet-combined.pdf` is a single-layer version with the L2 and L5 legends in the corners of each key, meant for black and white printers.

The file carries the UID of the Tergo Sofle rev0. For any other Sofle with Vial, load it anyway when Vial asks: the matrix is the same 10 x 6, only the encoder and tap dance details may need adjusting.

## Regenerating

Everything is generated from `scripts/`, Python 3 with no third-party packages. Reference files (the Tergo `info.json`, the Sofle geometry from QMK, the Vial keycode table) are downloaded once into `cache/`.

```sh
python3 scripts/gen_vil.py        # writes keymap/tergo-sofle-graphite-pt.vil
python3 scripts/normalize.py      # normalizes keycode names, validates them against Vial, prints the layers
sh scripts/build_cheatsheets.sh   # HTML, PDF and PNG cheat sheets (needs Chrome and poppler)
```

Layout scoring: `python3 scripts/analyze.py corpus/pt.txt corpus/en.txt` (plain text files; the ones used here were Wikipedia article extracts). `sfb.py` lists the worst bigrams, `punct.py` compares punctuation placements, `tune.py` is a greedy single-swap optimizer. `dump_layout.swift` prints what each key and modifier combination produces on a macOS keyboard layout, which is how the Option combinations were found.

## Credits

- [Graphite](https://github.com/rdavison/graphite-layout) by rdavison.
- [Tergo Teclados](https://github.com/TergoTeclados) for the Sofle and its [Vial firmware](https://github.com/TergoTeclados/vial-qmk-firmware).
- [Vial](https://get.vial.today/).

## Resumo em português

Keymap para o Tergo Sofle (com fio, Vial, versão ABNT2) com as letras do Graphite adaptadas ao português: O e U trocados (elimina os bigramas "ao" e "eu" no mesmo dedo), V e W trocados (tira o V da tecla interna de baixo), Ç na coluna externa esquerda, acentos agudo e til nos polegares esquerdos. O sistema continua em Português Brasil ABNT2; todo o remapeamento está no firmware. Para instalar: salve o layout atual no Vial, carregue `keymap/tergo-sofle-graphite-pt.vil` e imprima `cheatsheet/cheatsheet.pdf`. Detalhes, medições e geradores acima.
