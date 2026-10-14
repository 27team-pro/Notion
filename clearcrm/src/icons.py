"""ClearCRM pixel icon set — 27TEAM style.
Every icon is a 9x9 grid of square cells, 1-cell strokes, staircase diagonals
that touch at the corners, exactly like the "2" in the 27 logo.
"""
import os, sys
from PIL import Image, ImageDraw

ICONS = {
    # brand mark: stepped C
    "clearcrm": """
.........
..######.
.#.......
.#.......
.#.......
.#.......
.#.......
..######.
.........
""",
    "home": """
....#....
...###...
..#####..
.#######.
#########
.##...##.
.##.#.##.
.##.#.##.
.#######.
""",
    "clients": """
...###...
..#####..
..#####..
..#####..
...###...
.........
.#######.
#########
#########
""",
    "team": """
.##...##.
####.####
####.####
.##...##.
.........
###...###
####.####
####.####
.........
""",
    "leads": """
#########
#########
.#######.
..#####..
...###...
...###...
...###...
...###...
...#.....
""",
    "deals": """
...######
.......##
......#.#
.....#..#
....#...#
...#.....
..#......
.#.......
#........
""",
    "campaigns": """
.......##
.....####
...######
#########
#########
.##.#####
.##..####
.##....##
.........
""",
    "content": """
.#.....#.
#########
#########
#.......#
#.##.##.#
#.......#
#.##.##.#
#.......#
#########
""",
    "tasks": """
#########
#.......#
#......##
#.....#.#
##...#..#
#.#.#...#
#..#....#
#.......#
#########
""",
    "projects": """
####.....
#########
#.......#
#.......#
#.......#
#.......#
#.......#
#.......#
#########
""",
    "category": """
#####....
#.#..#...
#.....#..
#......#.
.#......#
..#....#.
...#..#..
....##...
.........
""",
    "resources": """
###...###
#..#.#..#
#...#...#
#...#...#
#...#...#
#...#...#
#...#...#
####.####
.........
""",
    "meetings": """
#########
#.......#
#.#.#.#.#
#.......#
#########
.##......
.#.......
#........
.........
""",
    "workspaces": """
###.#####
###.#####
###.#####
.........
#####.###
#####.###
#####.###
.........
.........
""",
    "analytics": """
.......##
.......##
....##.##
....##.##
.##.##.##
.##.##.##
.##.##.##
.........
#########
""",
    "channels": """
....#....
.#..#..#.
..#.#.#..
...###...
#########
...###...
..#.#.#..
.#..#..#.
....#....
""",
    "budget": """
.........
.#######.
#.......#
.#######.
#.......#
.#######.
#.......#
.#######.
.........
""",
    "start": """
##.......
####.....
######...
########.
#########
########.
######...
####.....
##.......
""",
    "add": """
...###...
...###...
...###...
#########
#########
#########
...###...
...###...
...###...
""",
    "menu": """
#########
#########
.........
.........
#########
#########
.........
.........
#########
""",
    "calendar": """
.#.....#.
#########
#.......#
#.#.#.#.#
#.......#
#.#.#.#.#
#.......#
#.#.#.#.#
#########
""",
    "target": """
#########
#.......#
#.#####.#
#.#...#.#
#.#.#.#.#
#.#...#.#
#.#####.#
#.......#
#########
""",
    "settings": """
...#.#...
.#######.
.#######.
###...###
.##...##.
###...###
.#######.
.#######.
...#.#...
""",
    "mail": """
#########
##.....##
#.#...#.#
#..#.#..#
#...#...#
#.......#
#.......#
#########
.........
""",
}

def grid(name):
    rows = [r for r in ICONS[name].strip("\n").split("\n")]
    assert len(rows) == 9 and all(len(r) == 9 for r in rows), (name, [len(r) for r in rows])
    return rows

def render(name, cell=40, pad=0, fg=(0,0,0,255), bg=(0,0,0,0)):
    rows = grid(name)
    size = cell*9 + pad*2
    im = Image.new("RGBA", (size, size), bg)
    d = ImageDraw.Draw(im)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == "#":
                d.rectangle([pad+x*cell, pad+y*cell, pad+(x+1)*cell-1, pad+(y+1)*cell-1], fill=fg)
    return im

def svg(name, fg="#000"):
    rows = grid(name)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1" height="1"/>'
                    for y, r in enumerate(rows) for x, ch in enumerate(r) if ch == "#")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 9 9" shape-rendering="crispEdges">'
            f'<g fill="{fg}">{rects}</g></svg>')

if __name__ == "__main__":
    out = sys.argv[1]
    for sub in ["png-black", "png-white", "png-tile", "svg"]:
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    for n in ICONS:
        render(n, cell=40, pad=20).save(f"{out}/png-black/{n}.png")
        render(n, cell=40, pad=20, fg=(255,255,255,255)).save(f"{out}/png-white/{n}.png")
        render(n, cell=40, pad=60, fg=(255,255,255,255), bg=(0,0,0,255)).save(f"{out}/png-tile/{n}.png")
        open(f"{out}/svg/{n}.svg", "w").write(svg(n))
    # contact sheet
    names = list(ICONS)
    cols = 6; cs = 200
    rows_n = (len(names)+cols-1)//cols
    sheet = Image.new("RGB", (cols*cs, rows_n*(cs+40)), "black")
    from PIL import ImageFont
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
    d = ImageDraw.Draw(sheet)
    for i, n in enumerate(names):
        ic = render(n, cell=12, fg=(255,255,255,255))
        x, y = (i%cols)*cs, (i//cols)*(cs+40)
        sheet.paste(ic, (x+(cs-108)//2, y+40), ic)
        d.text((x+cs//2, y+170), n, fill="white", font=f, anchor="mm")
    sheet.save(f"{out}/contact-sheet.png")
    print(len(names), "icons")
