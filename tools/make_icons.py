"""アプリアイコン（そろばん玉のたまちゃん）を icons/ に出力する。"""
import os
from PIL import Image, ImageDraw

S = 1024
out = os.path.join(os.path.dirname(__file__), "..", "icons")
img = Image.new("RGB", (S, S), "#E9F3F0")
d = ImageDraw.Draw(img)
k = S / 120  # mascot viewBox 120 wide
oy = (S - 90 * k) / 2
P = lambda x, y: (x * k, oy + y * k)
d.rounded_rectangle([P(55, -20), P(65, 110)], radius=4 * k, fill="#7C8B96")
bead = [P(8, 45), P(21, 31), P(47, 17), P(60, 12), P(73, 17), P(99, 31), P(112, 45), P(99, 59), P(73, 73), P(60, 78), P(47, 73), P(21, 59)]
d.polygon(bead, fill="#9A5A33")
d.line([P(22, 36), P(48, 22), P(60, 17), P(72, 22), P(92, 32)], fill="#C8865A", width=int(4 * k), joint="curve")
for cx in (45, 75):
    d.ellipse([P(cx - 4.5, 40.5), P(cx + 4.5, 49.5)], fill="#2A170C")
    d.ellipse([P(cx + .1, 42.1), P(cx + 2.9, 44.9)], fill="#FFFFFF")
for cx in (36, 84):
    d.ellipse([P(cx - 5, 51), P(cx + 5, 57)], fill="#F29C9C")
d.arc([P(55, 49), P(65, 58)], 20, 160, fill="#2A170C", width=int(2.5 * k))
os.makedirs(out, exist_ok=True)
for n in (512, 192, 180):
    img.resize((n, n), Image.LANCZOS).save(os.path.join(out, f"icon-{n}.png"))
print("ok")
