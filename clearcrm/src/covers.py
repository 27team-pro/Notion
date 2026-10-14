"""ClearCRM covers & marketplace images in the 27TEAM pixel style."""
import sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "src")
from icons import ICONS, grid

# 5x7 pixel font with detached-corner steps, like the "2" in the 27 logo
FONT = {
"A": [".###.","#...#","#...#","#####","#...#","#...#","#...#"],
"C": [".####","#....","#....","#....","#....","#....",".####"],
"E": ["#####","#....","#....","####.","#....","#....","#####"],
"L": ["#....","#....","#....","#....","#....","#....","#####"],
"M": ["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
"R": ["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
"T": ["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
"S": [".####","#....","#....",".###.","....#","....#","####."],
"O": [".###.","#...#","#...#","#...#","#...#","#...#",".###."],
"N": ["#...#","##..#","#.#.#","#..##","#...#","#...#","#...#"],
"D": ["####.","#...#","#...#","#...#","#...#","#...#","####."],
"I": ["#####","..#..","..#..","..#..","..#..","..#..","#####"],
"K": ["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
"G": [".####","#....","#....","#.###","#...#","#...#",".###."],
"P": ["####.","#...#","#...#","####.","#....","#....","#...."],
"U": ["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
"H": ["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
"F": ["#####","#....","#....","####.","#....","#....","#...."],
"W": ["#...#","#...#","#...#","#.#.#","#.#.#","##.##","#...#"],
"Y": ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
"V": ["#...#","#...#","#...#","#...#",".#.#.",".#.#.","..#.."],
"B": ["####.","#...#","#...#","####.","#...#","#...#","####."],
"J": ["..###","....#","....#","....#","....#","#...#",".###."],
"/": ["....#","....#","...#.","..#..",".#...","#....","#...."],
" ": [".....",".....",".....",".....",".....",".....","....."],
}
W, H = 5, 7

def text_px(d, s, x, y, cell, fill="white", gap=1):
    for ch in s.upper():
        g = FONT[ch]
        for gy, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == "#":
                    d.rectangle([x+gx*cell, y+gy*cell, x+(gx+1)*cell-1, y+(gy+1)*cell-1], fill=fill)
        x += (W+gap)*cell
    return x

def text_w(s, cell, gap=1):
    return len(s)*(W+gap)*cell - gap*cell

def icon_px(d, name, x, y, cell, fill="white"):
    for gy, row in enumerate(grid(name)):
        for gx, c in enumerate(row):
            if c == "#":
                d.rectangle([x+gx*cell, y+gy*cell, x+(gx+1)*cell-1, y+(gy+1)*cell-1], fill=fill)

INTER = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
INTERB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
LOGO_W = Image.open("src/27-white.png")
LOGO_B = Image.open("src/27-black.png")

def paste_logo(im, x, y, h, dark=True):
    lg = LOGO_W if dark else LOGO_B
    r = h / lg.height
    lg = lg.resize((int(lg.width*r), h), Image.LANCZOS)
    im.paste(lg, (x, y), lg)
    return lg.width

def grid_dots(d, w, h, step, col):
    for x in range(0, w, step):
        for y in range(0, h, step):
            d.rectangle([x, y, x+1, y+1], fill=col)

def notion_cover(path, title, icon_name=None, dark=True):
    """1500x600 Notion page cover. Content sits in the vertical middle band (Notion crops)."""
    w, h = 1500, 600
    bg, fg, mut = ("#000", "#fff", "#2a2a2a") if dark else ("#fff", "#000", "#dcdcdc")
    im = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(im)
    grid_dots(d, w, h, 30, mut)
    cell = 14
    tw = text_w(title, cell)
    x0 = (w - tw)//2
    if icon_name:
        isz = 9*cell
        x0 = (w - (tw + isz + 4*cell))//2
        icon_px(d, icon_name, x0, (h-isz)//2, cell, fg)
        x0 += isz + 4*cell
    text_px(d, title, x0, (h-7*cell)//2 + cell, cell, fg)
    f = ImageFont.truetype(INTER, 22)
    d.text((60, h-70), "CLEARCRM", font=ImageFont.truetype(INTERB, 22), fill=fg)
    d.text((w-60, h-70), "27TEAM.PRO", font=f, fill=fg, anchor="ra")
    im.save(path)

def marketplace(path, headline, sub, icons, dark=True, w=1920, h=1080):
    bg, fg, mut = ("#000", "#fff", "#242424") if dark else ("#fff", "#000", "#e2e2e2")
    im = Image.new("RGB", (w, h), bg); d = ImageDraw.Draw(im)
    grid_dots(d, w, h, 40, mut)
    pad = 120
    # top bar
    d.text((pad, 90), "27TEAM", font=ImageFont.truetype(INTERB, 30), fill=fg)
    d.text((w-pad, 90), "27TEAM.PRO", font=ImageFont.truetype(INTER, 30), fill=fg, anchor="ra")
    # headline (pixel)
    cell = 24
    y = 300
    for line in headline:
        text_px(d, line, pad, y, cell, fg); y += 9*cell
    f = ImageFont.truetype(INTER, 40)
    d.text((pad, y + 30), sub, font=f, fill=fg)
    # icon strip
    ic = 9; cs = 9*ic; gap = 44
    x = pad; iy = h - 120 - cs
    for n in icons:
        icon_px(d, n, x, iy, ic, fg); x += cs + gap
    # 27 logo bottom-right
    lh = 120
    lw = int(LOGO_W.width * lh / LOGO_W.height)
    paste_logo(im, w - pad - lw, h - 120 - lh, lh, dark)
    im.save(path)

if __name__ == "__main__":
    out = "covers"
    pages = {
        "dashboard": ("CLEARCRM", "clearcrm"),
        "tasks": ("TASKS", "tasks"), "projects": ("PROJECTS", "projects"),
        "category": ("CATEGORY", "category"), "resources": ("RESOURCES", "resources"),
        "content": ("CONTENT", "content"), "meetings": ("MEETINGS", "meetings"),
        "campaigns": ("CAMPAIGNS", "campaigns"), "leads": ("LEADS", "leads"),
        "clients": ("CLIENTS", "clients"), "deals": ("DEALS", "deals"),
        "team": ("TEAM", "team"), "start": ("START HERE", "start"),
        "analytics": ("ANALYTICS", "analytics"),
    }
    for k, (t, i) in pages.items():
        notion_cover(f"{out}/cover-{k}.png", t, i)
    strip = ["leads","campaigns","deals","clients","content","analytics","tasks","calendar"]
    marketplace(f"{out}/marketplace-01-hero.png", ["CLEARCRM"], "The marketing CRM for Notion. Leads, campaigns, deals and content in one place.", strip)
    marketplace(f"{out}/marketplace-01-hero-light.png", ["CLEARCRM"], "The marketing CRM for Notion. Leads, campaigns, deals and content in one place.", strip, dark=False)
    marketplace(f"{out}/marketplace-02-funnel.png", ["LEADS /", "CAMPAIGNS"], "Track every lead back to the campaign and channel that brought it.", ["leads","campaigns","channels","budget","target"])
    marketplace(f"{out}/marketplace-03-pipeline.png", ["DEALS /", "CLIENTS"], "Pipeline from New to Won, weighted forecast and revenue by stage.", ["deals","clients","analytics","meetings","mail"])
    marketplace(f"{out}/marketplace-04-content.png", ["CONTENT /", "TASKS"], "Content calendar, projects, tasks and a resource library for the team.", ["content","calendar","tasks","projects","resources"])
    # square thumbnail / profile
    sq = Image.new("RGB", (1080,1080), "#000"); d = ImageDraw.Draw(sq)
    grid_dots(d, 1080, 1080, 40, "#242424")
    icon_px(d, "clearcrm", (1080-9*60)//2, 200, 60)
    tw = text_w("CLEARCRM", 14); text_px(d, "CLEARCRM", (1080-tw)//2, 800, 14)
    d.text((540, 960), "BY 27TEAM", font=ImageFont.truetype(INTER, 30), fill="white", anchor="mm")
    sq.save(f"{out}/marketplace-thumb-square.png")
    print("ok")
