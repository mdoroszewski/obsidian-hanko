#!/usr/bin/env python3
"""Tests for the Hanko theme. Standard library only.

Run from the theme folder:   python3 tests/test_theme.py
Another theme.css:           HANKO_THEME=/path/to/theme.css python3 tests/test_theme.py

Four groups:
1. Review rules of the Obsidian directory (no :has, no !important, no partially
   supported text-decoration forms, nothing loaded from outside).
2. Structure: braces, comments, Style Settings block, every variable defined.
3. Colour: plate values from Sanzo Wada's book, every text/background pair
   at least 4.5:1.
4. Rendering smoke test in headless Chrome with Obsidian's own app.css
   (skipped when Chrome or the Obsidian asar is not on this Mac).
"""
import glob
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
THEME = os.environ.get("HANKO_THEME") or os.path.join(os.path.dirname(HERE), "theme.css")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def read_theme():
    with open(THEME, encoding="utf-8") as f:
        return f.read()


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def strip_strings(css):
    """Blank out quoted strings of both kinds in order of appearance, so a
    quote mark inside the other kind of string (e.g. [data-task='"']) is safe."""
    return re.sub(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', '""', css)


def top_level_rules(css):
    """Count rules at the top level (an @media block counts once)."""
    depth, count = 0, 0
    for ch in strip_strings(strip_comments(css)):
        if ch == "{":
            if depth == 0:
                count += 1
            depth += 1
        elif ch == "}":
            depth -= 1
    return count


def block(css, selector):
    """Return the declarations of the first top-level block with this exact selector."""
    m = re.search(r"(?:^|\n)" + re.escape(selector) + r"\s*\{([^}]*)\}", css)
    return m.group(1) if m else ""


def declarations(body):
    out = {}
    for line in strip_comments(body).split(";"):
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def settings_block(css):
    m = re.search(r"/\*\s*@settings(.*?)\*/", css, flags=re.S)
    return m.group(1) if m else ""


def parse_settings(yaml_text):
    """Minimal parser for the Style Settings YAML: a list of flat maps,
    options as a list of maps."""
    items, cur, opt = [], None, None
    for raw in yaml_text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        text = line.strip()
        if indent == 2 and text == "-":
            cur = {}
            items.append(cur)
            opt = None
        elif indent == 4 and cur is not None and ":" in text:
            k, v = text.split(":", 1)
            cur[k.strip()] = v.strip()
            if k.strip() == "options":
                cur["options"] = []
        elif indent == 6 and text == "-" and cur is not None:
            opt = {}
            cur["options"].append(opt)
        elif indent == 8 and opt is not None and ":" in text:
            k, v = text.split(":", 1)
            opt[k.strip()] = v.strip()
    return items


def hex_of(value):
    """'#bb7125' or '187, 113, 37' -> (r, g, b)."""
    value = value.strip()
    if value.startswith("#"):
        h = value[1:]
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    nums = re.findall(r"\d+", value)
    if len(nums) == 3:
        return tuple(int(n) for n in nums)
    raise ValueError(value)


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


class ReviewRules(unittest.TestCase):
    """What the automated review on community.obsidian.md flags."""

    def setUp(self):
        self.css = strip_comments(read_theme())

    def test_no_has(self):
        self.assertEqual(self.css.count(":has("), 0)

    def test_no_important(self):
        self.assertEqual(self.css.count("!important"), 0)

    def test_no_text_decoration_longhands(self):
        hits = re.findall(r"text-decoration-(?:color|style|line|thickness|skip(?:-ink)?)\s*:", self.css)
        self.assertEqual(hits, [])

    def test_no_text_decoration_shorthand_with_two_values(self):
        hits = re.findall(r"text-decoration\s*:\s*[\w-]+\s+[\w#(-]", self.css)
        self.assertEqual(hits, [])

    def test_nothing_loaded_from_outside(self):
        self.assertNotIn("@import", self.css)
        self.assertNotIn("@font-face", self.css)
        self.assertEqual(re.findall(r"url\(\s*['\"]?https?://", self.css), [])


class Structure(unittest.TestCase):

    def setUp(self):
        self.raw = read_theme()
        self.css = strip_comments(self.raw)

    def test_comments_closed(self):
        self.assertEqual(self.raw.count("/*"), self.raw.count("*/"))

    def test_braces_balanced(self):
        t = strip_strings(self.css)
        self.assertEqual(t.count("{"), t.count("}"))

    def test_every_declaration_has_a_colon(self):
        bad = []
        for m in re.finditer(r"\{([^{}]*)\}", strip_strings(self.css)):
            for d in m.group(1).split(";"):
                if d.strip() and ":" not in d:
                    bad.append(d.strip()[:60])
        self.assertEqual(bad, [])

    def test_settings_block_present_and_english(self):
        items = parse_settings(settings_block(self.raw))
        self.assertGreater(len(items), 5)
        for it in items:
            self.assertIn("id", it)
            self.assertIn("title", it)
            self.assertIn(it["type"], {"heading", "class-toggle", "class-select", "info-text",
                                       "variable-text", "variable-number", "variable-number-slider",
                                       "variable-select", "variable-color", "variable-themed-color"})
            for key in ("title", "description"):
                if key in it:
                    self.assertFalse(re.search(r"[äöüÄÖÜß]", it[key]), f"{it['id']}: {key} not English")

    def test_settings_ids_unique(self):
        ids = [it["id"] for it in parse_settings(settings_block(self.raw))]
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_toggle_is_used_in_css(self):
        for it in parse_settings(settings_block(self.raw)):
            if it["type"] == "class-toggle":
                self.assertRegex(self.css, r"\." + re.escape(it["id"]) + r"\b", f"{it['id']} has no rule")
            if it["type"] == "class-select":
                for o in it.get("options", []):
                    if o["value"] != it.get("default"):
                        self.assertRegex(self.css, r"\." + re.escape(o["value"]) + r"\b",
                                         f"option {o['value']} has no rule")

    def test_every_hanko_variable_is_defined(self):
        defined = set(re.findall(r"(--hanko-[\w-]+)\s*:", self.css))
        used = set(re.findall(r"var\((--hanko-[\w-]+)", self.css))
        allowed_fallback_only = {"--hanko-tafel-1-dichte", "--hanko-tafel-2-dichte",
                                 "--hanko-tafel-3-dichte", "--hanko-tafel-4-dichte", "--hanko-aufsetzen"}
        missing = used - defined - allowed_fallback_only
        self.assertEqual(missing, set())

    def test_light_and_dark_define_the_same_values(self):
        light = set(declarations(block(self.css, ".theme-light")))
        dark = set(declarations(block(self.css, ".theme-dark")))
        light_only = {k for k in light - dark if not k.endswith("-dichte")}
        self.assertEqual(light_only, set(), "defined in light only")
        self.assertEqual(dark - light, set(), "defined in dark only")

    def test_mobile_hover_reveals_are_guarded(self):
        """Anything that appears on hover must sit under @media (hover: hover)
        and exclude .is-mobile (iOS keeps :hover after a tap)."""
        for cls in ("hanko-kopfzeile-still", "hanko-leisten-zurueck"):
            for m in re.finditer(r"body\." + cls + r"[^{]*\{", self.css):
                sel = m.group(0)
                if "prefers-reduced-motion" in self.css[max(0, m.start() - 400):m.start()]:
                    continue
                self.assertIn(":not(.is-mobile)", sel, sel[:80])
                before = self.css[:m.start()]
                self.assertGreater(before.rfind("@media (hover: hover)"), before.rfind("\n}\n"), sel[:80])


class Colour(unittest.TestCase):
    """Values from Farben.md: Wada plates No. 279 (light), 293 (dark), 327."""

    PLATE_LIGHT = {1: "bb7125", 2: "12354e", 3: "c2ae93", 4: "eea78c"}
    PLATE_DARK = {1: "bb7125", 2: "489b6e", 3: "709390", 4: "b5decc"}
    PLATE_327 = {2: "f37f94", 4: "c0a9b3"}
    ROLES = {  # light, dark
        "--hanko-rot": ("dd4027", "f15a30"),
        "--hanko-indigo": ("12354e", "97acc8"),   # Dark Tyrian Blue, plate 279 slot 2 (since 1.1)
        "--hanko-ocker": ("bb7125", "e2b540"),
        "--hanko-pflaume": ("8c4c62", "ca92a8"),
        "--hanko-ok": ("1a7444", "489b6e"),
        "--hanko-fett": ("ae5224", "bb7125"),
        "--hanko-grund": ("e0e0db", "111314"),
    }

    def setUp(self):
        self.css = strip_comments(read_theme())
        self.light = declarations(block(self.css, ".theme-light"))
        self.dark = declarations(block(self.css, ".theme-dark"))

    def _hex(self, rgb):
        return "%02x%02x%02x" % rgb

    def test_plates(self):
        for n, h in self.PLATE_LIGHT.items():
            self.assertEqual(self._hex(hex_of(self.light[f"--hanko-tafel-{n}-rgb"])), h, f"light plate {n}")
        for n, h in self.PLATE_DARK.items():
            self.assertEqual(self._hex(hex_of(self.dark[f"--hanko-tafel-{n}-rgb"])), h, f"dark plate {n}")
        alt = declarations(block(self.css, ".theme-light.hanko-tafel-hell-327"))
        for n, h in self.PLATE_327.items():
            self.assertEqual(self._hex(hex_of(alt[f"--hanko-tafel-{n}-rgb"])), h, f"plate 327 slot {n}")

    def test_raw_sienna_is_first_everywhere(self):
        for decl in (self.light, self.dark):
            self.assertEqual(self._hex(hex_of(decl["--hanko-tafel-1-rgb"])), "bb7125")

    def test_role_tones(self):
        for var, (l, d) in self.ROLES.items():
            self.assertEqual(self.light[var].lower(), "#" + l, var)
            self.assertEqual(self.dark[var].lower(), "#" + d, var)

    def test_rgb_triplets_match_hex(self):
        for decl in (self.light, self.dark):
            for k, v in decl.items():
                if k.endswith("-rgb") and k[:-4] in decl and decl[k[:-4]].startswith("#"):
                    self.assertEqual(hex_of(v), hex_of(decl[k[:-4]]), k)

    def test_text_contrast(self):
        for mode, decl in (("light", self.light), ("dark", self.dark)):
            paper = hex_of(decl["--hanko-papier"])
            surface = hex_of(decl["--hanko-flaeche"])
            self.assertGreaterEqual(contrast(hex_of(decl["--hanko-tinte"]), paper), 7, mode)
            self.assertGreaterEqual(contrast(hex_of(decl["--hanko-tinte-2"]), paper), 4.5, mode)
            self.assertGreaterEqual(contrast(hex_of(decl["--hanko-fett"]), surface), 4.5, mode)
            for n in (1, 2, 3, 4):
                pill = hex_of(decl[f"--hanko-tafel-{n}-rgb"])
                text = hex_of(decl[f"--hanko-tafel-{n}-schrift"])
                self.assertGreaterEqual(contrast(text, pill), 4.5, f"{mode} plate {n}")

    def test_bold_options_reach_contrast(self):
        for m in re.finditer(r"\.theme-(light|dark)\.hanko-fett-[\w-]+\s*\{([^}]*)\}", self.css):
            mode, body = m.group(1), m.group(2)
            decl = declarations(body)
            base = self.light if mode == "light" else self.dark
            value = decl["--hanko-fett"]
            ref = re.match(r"var\((--hanko-[\w-]+)\)", value)
            if ref:
                value = base[ref.group(1)]
            self.assertGreaterEqual(contrast(hex_of(value), hex_of(base["--hanko-flaeche"])), 4.5, m.group(0)[:40])


def obsidian_app_css():
    paths = sorted(glob.glob(os.path.expanduser("~/Library/Application Support/obsidian/obsidian-*.asar")))
    if not paths:
        return None
    with open(paths[-1], "rb") as f:
        f.seek(12)
        hdr_len = struct.unpack("<I", f.read(4))[0]
        hdr = json.loads(f.read(hdr_len).rstrip(b"\0").decode())
        node = hdr["files"].get("app.css")
        if not node:
            return None
        f.seek(16 + hdr_len + int(node["offset"]))
        return f.read(node["size"]).decode("utf-8", "replace")


FIXTURE = """
<div class="app-container"><div class="workspace">
<div class="nav-files-container">
  <div class="nav-folder"><div class="nav-folder-title" data-path="1 Projects"></div></div>
  <div class="nav-folder"><div class="nav-folder-title" data-path="2 Areas"></div></div>
  <div class="nav-folder"><div class="nav-folder-title" data-path="4 Archive"></div></div>
</div>
<div class="workspace-leaf-content" data-type="markdown">
<div class="markdown-reading-view"><div class="markdown-preview-view markdown-rendered wide seal">
<div class="markdown-preview-sizer">
  <ul><li data-task="*" class="task-list-item"><input type="checkbox" data-task="*" id="star"></li>
      <li data-task="p" class="task-list-item"><input type="checkbox" data-task="p" id="pro"></li></ul>
  <div class="callout" data-callout="note" data-callout-metadata="plain" id="plain"><div class="callout-title"><div class="callout-icon"></div></div></div>
  <div class="callout" data-callout="note" data-callout-metadata="no-title" id="notitle"><div class="callout-title" id="notitle-title"></div></div>
  <span class="internal-embed image-embed" alt="Eine Beschriftung" id="cap"><img></span>
  <span class="internal-embed image-embed" alt="bild.png" id="nocap"><img></span>
  <table><tbody><tr><td>a</td></tr><tr><td id="even">b</td></tr></tbody></table>
  <a class="internal-link" id="link">x</a>
</div></div></div></div>
<div class="kanban-plugin__lanes">
  <div class="kanban-plugin__lane-wrapper"><div class="kanban-plugin__lane" id="lane1"><div class="kanban-plugin__lane-header-wrapper" id="lane1h"></div></div></div>
  <div class="kanban-plugin__lane-wrapper"><div class="kanban-plugin__lane" id="lane2"><div class="kanban-plugin__lane-header-wrapper" id="lane2h"></div></div></div>
</div>
</div></div>
"""

SCRIPT = """
const cs = (sel, prop, pseudo) => getComputedStyle(document.querySelector(sel), pseudo || null).getPropertyValue(prop).trim();
const out = {};
out.rules = document.getElementById('theme').sheet.cssRules.length;
out.star_mask = cs('#star', '-webkit-mask-image', '::after');
out.star_border = cs('#star', 'border-top-color');
out.pro_border = cs('#pro', 'border-top-color');
out.plain_border_left = cs('#plain', 'border-left-width');
out.plain_border_top = cs('#plain', 'border-top-width');
out.notitle_display = cs('#notitle-title', 'display');
out.cap_after = cs('#cap', 'content', '::after');
out.nocap_after = cs('#nocap', 'content', '::after');
out.line_width = cs('.markdown-preview-view', '--file-line-width');
out.folder1 = cs('[data-path="1 Projects"]', 'background-color');
out.folder2 = cs('[data-path="2 Areas"]', 'background-color');
out.archive = cs('[data-path="4 Archive"]', 'background-color');
out.lane1h = cs('#lane1h', 'background-color');
out.lane2h = cs('#lane2h', 'background-color');
out.link_border = cs('#link', 'border-bottom-color');
out.seal_content = cs('.markdown-preview-sizer', 'content', '::before');
document.getElementById('out').textContent = JSON.stringify(out);
"""


@unittest.skipUnless(os.path.exists(CHROME), "Google Chrome not installed")
class Rendering(unittest.TestCase):
    """Loads Obsidian's app.css plus the theme into headless Chrome and reads
    computed styles. Light mode, desktop, with the caption switch on."""

    @classmethod
    def setUpClass(cls):
        app = obsidian_app_css()
        if app is None:
            raise unittest.SkipTest("Obsidian asar not found")
        theme = read_theme()
        html = ("<!doctype html><html><head><meta charset='utf-8'><style id='app'>" + app +
                "</style><style id='theme'>" + theme + "</style></head>"
                "<body class='theme-light mod-macos hanko-bild-unterschrift'>" + FIXTURE +
                "<pre id='out'></pre><script>" + SCRIPT + "</script></body></html>")
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(html)
        dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
                              "--virtual-time-budget=2000", "--dump-dom", "file://" + path],
                             capture_output=True, text=True, timeout=60).stdout
        os.unlink(path)
        m = re.search(r'<pre id="out">(.*?)</pre>', dom, flags=re.S)
        if not m:
            raise unittest.SkipTest("Chrome produced no output")
        cls.out = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))
        cls.expected_rules = top_level_rules(theme)

    def test_chrome_kept_every_rule(self):
        self.assertEqual(self.out["rules"], self.expected_rules, "Chrome dropped rules it could not parse")

    def test_task_glyphs(self):
        self.assertIn("url(", self.out["star_mask"])
        self.assertEqual(self.out["star_border"], "rgb(174, 82, 36)")   # Burnt Sienna, anchor
        self.assertEqual(self.out["pro_border"], "rgb(26, 116, 68)")    # Diamine Green

    def test_callout_modifiers(self):
        self.assertEqual(self.out["plain_border_left"], "2px")
        self.assertEqual(self.out["plain_border_top"], "0px")
        self.assertEqual(self.out["notitle_display"], "none")

    def test_image_caption_only_for_real_alt_text(self):
        self.assertIn("attr(alt)", self.out["cap_after"].replace('"', "")) if "attr" in self.out["cap_after"] \
            else self.assertEqual(self.out["cap_after"], '"Eine Beschriftung"')
        self.assertEqual(self.out["nocap_after"], "none")

    def test_helper_class_wide(self):
        self.assertEqual(self.out["line_width"], "50rem")

    def test_folders_and_lanes_carry_the_plate(self):
        self.assertEqual(self.out["folder1"], "rgb(187, 113, 37)")   # Raw Sienna
        self.assertEqual(self.out["folder2"], "rgb(18, 53, 78)")     # Dark Tyrian Blue
        self.assertEqual(self.out["archive"], "rgb(161, 163, 154)")  # Warm Gray
        self.assertEqual(self.out["lane1h"], "rgb(187, 113, 37)")
        self.assertEqual(self.out["lane2h"], "rgb(18, 53, 78)")

    def test_links_and_seal(self):
        self.assertEqual(self.out["link_border"], "rgb(221, 64, 39)")  # Red Orange
        self.assertNotEqual(self.out["seal_content"], "none")


if __name__ == "__main__":
    unittest.main(verbosity=2)
