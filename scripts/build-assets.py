"""Generate the SVG assets used by the profile README.

Run from the repository root:  python3 scripts/build-assets.py
All colors come from the profile photo and LinkedIn banner (charcoal + taupe).
"""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

BG_DARK = "#2f3135"
BG_MID = "#3e3f43"
BG_WARM = "#5c5148"
TAUPE = "#c9b29c"
SAND = "#efe4d8"
WHITE = "#ffffff"
MUTED = "#d6cabd"
FONT = "'Avenir Next', 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def gradient(id_: str) -> str:
    return (
        f'<linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="0.25">'
        f'<stop offset="0" stop-color="{BG_DARK}"/>'
        f'<stop offset="0.55" stop-color="{BG_MID}"/>'
        f'<stop offset="1" stop-color="{BG_WARM}"/></linearGradient>'
    )


def waveform(x0: int, x1: int, base: float, amp: float, animated: bool) -> str:
    """Audio-waveform bars, deterministic. Animated bars pulse gently."""
    bars = []
    for i, x in enumerate(range(x0, x1, 9)):
        env = math.sin(i * 0.045) * 0.5 + 0.5
        h = 6 + env * (amp * 0.35 + amp * abs(math.sin(i * 0.61) * math.cos(i * 0.23)))
        fade = min(1.0, (x - x0) / 300)
        opacity = 0.12 + 0.18 * fade
        delay = f' style="animation-delay:-{(i % 12) * 0.13:.2f}s"' if animated else ""
        bars.append(
            f'<rect class="bar" x="{x}" y="{base - h / 2:.1f}" width="3" height="{h:.1f}" '
            f'rx="1.5" fill="{SAND}" fill-opacity="{opacity:.2f}"{delay}/>'
        )
    return "".join(bars)


MOTION_CSS = """
<style>
  .bar { transform-box: fill-box; transform-origin: center; animation: pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { transform: scaleY(1); } 50% { transform: scaleY(.55); } }
  @media (prefers-reduced-motion: reduce) { .bar { animation: none; } }
</style>"""


def header() -> str:
    w, h = 800, 250
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Juan Esteban Mora Arcila, Frontend Developer">
{MOTION_CSS}
<defs>{gradient('g')}</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#g)"/>
{waveform(30, 770, 208, 30, True)}
<text x="400" y="66" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="600" letter-spacing="5" fill="{SAND}">CODE · DESIGN · MUSIC</text>
<text x="400" y="122" text-anchor="middle" font-family="{FONT}" font-size="46" font-weight="700" fill="{WHITE}">Juan Esteban Mora Arcila</text>
<text x="400" y="162" text-anchor="middle" font-family="{FONT}" font-size="25" font-weight="500" fill="{SAND}">Frontend Developer · Cali, Colombia</text>
</svg>
"""


def title(text: str) -> str:
    w, h = 700, 64
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{text}">
<rect x="0" y="40" width="{w}" height="1.5" fill="{TAUPE}" fill-opacity=".45"/>
<rect x="0" y="16" width="6" height="26" rx="3" fill="{TAUPE}"/>
<text x="20" y="36" font-family="{FONT}" font-size="24" font-weight="700" fill="{TAUPE}">{text}</text>
</svg>
"""


def avatar(avatar_b64: str) -> str:
    """Circular profile photo with a taupe ring (text lives in the README so it stays readable on mobile)."""
    size = 260
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="Photo of Juan Esteban Mora Arcila">
<defs><clipPath id="c"><circle cx="130" cy="130" r="116"/></clipPath></defs>
<circle cx="130" cy="130" r="125" fill="none" stroke="{TAUPE}" stroke-width="4"/>
<image x="14" y="14" width="232" height="232" clip-path="url(#c)" preserveAspectRatio="xMidYMid slice" href="data:image/jpeg;base64,{avatar_b64}" xlink:href="data:image/jpeg;base64,{avatar_b64}"/>
</svg>
"""


def pillars() -> str:
    """Four cards in a 2x2 grid so the text stays legible when GitHub scales it down on phones."""
    w, h = 520, 400
    items = [
        ("&lt;/&gt;", "Web development", "Responsive sites", "and interfaces"),
        ("{ }", "App development", "Solid logic,", "clean structure"),
        ("[db]", "Databases", "Well-organized", "data models"),
        ("◐", "Design &amp; 3D", "Blender, vector", "art, good taste"),
    ]
    cw, ch, gap = 250, 190, 20
    cards = []
    for i, (icon, head, l1, l2) in enumerate(items):
        x, y = (i % 2) * (cw + gap), (i // 2) * (ch + gap)
        cards.append(
            f'<g transform="translate({x},{y})">'
            f'<rect width="{cw}" height="{ch}" rx="16" fill="url(#g)"/>'
            f'<text x="24" y="54" font-family="{MONO}" font-size="26" font-weight="700" fill="{TAUPE}">{icon}</text>'
            f'<text x="24" y="100" font-family="{FONT}" font-size="21" font-weight="700" fill="{WHITE}">{head}</text>'
            f'<text x="24" y="133" font-family="{FONT}" font-size="17" fill="{MUTED}">{l1}</text>'
            f'<text x="24" y="157" font-family="{FONT}" font-size="17" fill="{MUTED}">{l2}</text>'
            f"</g>"
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Web development · App development · Databases · Design and 3D">
<defs>{gradient('g')}</defs>
{''.join(cards)}
</svg>
"""


def main() -> None:
    avatar_b64 = base64.b64encode((ASSETS / "avatar.jpg").read_bytes()).decode()
    files = {
        "header.svg": header(),
        "avatar.svg": avatar(avatar_b64),
        "pillars.svg": pillars(),
        "titles/about.svg": title("About me"),
        "titles/toolbox.svg": title("Toolbox"),
        "titles/latest.svg": title("Latest from my GitHub"),
        "titles/contact.svg": title("Let's talk"),
    }
    for name, svg in files.items():
        path = ASSETS / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(svg, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
