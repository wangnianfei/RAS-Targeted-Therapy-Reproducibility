import os, sys, shutil, math, base64
from PIL import Image, ImageDraw, ImageFont

SRC_IMG = '/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/06_Figure4_Global_Trial_Landscape/vector_figures/Figure4_trial_atlas.png'
base_im = Image.open(SRC_IMG).convert('RGB')
w, h = base_im.size

xc, yc = 530.5, 1721.4
R_out = 512.8
BLUE = (31, 58, 95)
RED = (166, 58, 46)
WHITE = (255, 255, 255)
INK = (26, 26, 26)

# -------------------------------------------------------------------------
# Step 1: Base geometric restoration of the dark blue wedge
# -------------------------------------------------------------------------
# Restore the dark blue wedge and clear all text in the white space up to x=1245
for y in range(1950, 2085):
    for x in range(850, 1245):
        ang = math.degrees(math.atan2(y - yc, x - xc))
        r = math.hypot(x - xc, y - yc)
        sec_color = BLUE if ang >= 28.85 else RED
        if r >= R_out + 1.2:
            base_im.putpixel((x, y), WHITE)
        elif 26.0 <= ang <= 55.5:
            if r <= R_out - 1.2:
                base_im.putpixel((x, y), sec_color)
            else:
                alpha = (R_out + 1.2 - r) / 2.4
                c = (
                    int(round(alpha * sec_color[0] + (1 - alpha) * WHITE[0])),
                    int(round(alpha * sec_color[1] + (1 - alpha) * WHITE[1])),
                    int(round(alpha * sec_color[2] + (1 - alpha) * WHITE[2]))
                )
                base_im.putpixel((x, y), c)

# -------------------------------------------------------------------------
# Step 2: English Version
# -------------------------------------------------------------------------
im_en = base_im.copy()
draw_en = ImageDraw.Draw(im_en)
f_en28 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28)

text_ha = "Histology-agnostic"
text_num = "152"
bbox_ha = f_en28.getbbox(text_ha)
w_ha = bbox_ha[2] - bbox_ha[0]
bbox_num = f_en28.getbbox(text_num)
w_num = bbox_num[2] - bbox_num[0]

# Placed cleanly in the white corridor: x=985 has 25px clearance from ring, 31px from legend
x_ha = 985
y_ha = 1995
draw_en.text((x_ha, y_ha), text_ha, fill=INK, font=f_en28)
x_num = x_ha + (w_ha - w_num) / 2
draw_en.text((x_num, y_ha + 38), text_num, fill=INK, font=f_en28)

# -------------------------------------------------------------------------
# Step 3: Chinese Version
# -------------------------------------------------------------------------
im_cn = base_im.copy()
draw_cn = ImageDraw.Draw(im_cn)

FONT_PATH = '/System/Library/Fonts/Hiragino Sans GB.ttc'
if not os.path.exists(FONT_PATH):
    FONT_PATH = '/System/Library/Fonts/PingFang.ttc'

def get_font(size, bold=False):
    idx = 1 if bold else 0
    return ImageFont.truetype(FONT_PATH, size, index=idx)

def cover_box(box):
    draw_cn.rectangle(box, fill=WHITE)

def cover_circle_safe_box(box):
    for y in range(box[1], box[3]):
        for x in range(box[0], box[2]):
            if math.hypot(x - xc, y - yc) > R_out + 1.2:
                im_cn.putpixel((x, y), WHITE)

def render_text(box, text, font, color=INK, align='left', line_spacing=4):
    lines = text.split('\n')
    line_heights = [font.getbbox(l)[3] - font.getbbox(l)[1] for l in lines]
    total_h = sum(line_heights) + (len(lines) - 1) * line_spacing
    cur_y = (box[1] + box[3] - total_h) / 2
    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        lw = bbox[2] - bbox[0]
        if align == 'center':
            cur_x = (box[0] + box[2] - lw) / 2
        elif align == 'right':
            cur_x = box[2] - lw
        else:
            cur_x = box[0]
        draw_cn.text((cur_x, cur_y), line, fill=color, font=font)
        cur_y += line_heights[i] + line_spacing

# Map Legend Title
f_leg_t = get_font(22, bold=True)
cover_box((5, 700, 155, 765))
render_text((5, 700, 155, 765), "试验中心分布\n(含 ≥1 个中心)", f_leg_t, align='left')

# Map Countries (exact ink bboxes with safe margins)
f_ctry_b = get_font(22, bold=True)
cover_box((730, 58, 900, 86))
render_text((730, 58, 900, 86), "加拿大 112", f_ctry_b, align='left')

cover_box((950, 66, 1138, 100))
render_text((950, 66, 1138, 100), "德国 122", f_ctry_b, align='left')

cover_box((724, 165, 825, 193))
render_text((724, 165, 825, 193), "英国 101", f_ctry_b, align='left')

cover_box((674, 249, 828, 277))
render_text((674, 249, 828, 277), "法国 154", f_ctry_b, align='left')

cover_box((689, 340, 828, 374))
render_text((689, 340, 828, 374), "西班牙 189", f_ctry_b, align='left')

cover_box((985, 417, 1102, 450))
render_text((985, 417, 1102, 450), "意大利 155", f_ctry_b, align='left')

cover_box((87, 424, 212, 452))
render_text((87, 424, 212, 452), "美国 644", f_ctry_b, align='left')

cover_box((1282, 264, 1424, 292))
render_text((1282, 264, 1424, 292), "中国 256", f_ctry_b, align='left')

cover_box((1817, 287, 1945, 320))
render_text((1817, 287, 1945, 320), "日本 82", f_ctry_b, align='left')

cover_box((1743, 462, 1972, 490))
render_text((1743, 462, 1972, 490), "韩国 120", f_ctry_b, align='left')

cover_box((1638, 980, 1819, 1008))
render_text((1638, 980, 1819, 1008), "澳大利亚 127", f_ctry_b, align='left')

# Panel b Tumour Sector Labels (guarded by circle boundary)
f_ring = get_font(23, bold=False)
cover_circle_safe_box((545, 1120, 770, 1200))
render_text((545, 1120, 770, 1200), "血液肿瘤\n59", f_ring, align='center')

cover_circle_safe_box((780, 1220, 952, 1292))
render_text((780, 1220, 952, 1292), "胰腺癌\n77", f_ring, align='center')

cover_circle_safe_box((1012, 1505, 1140, 1580))
render_text((1035, 1505, 1180, 1580), "非小细胞肺癌\n149", f_ring, align='left')

# Histology-agnostic in Chinese: centered in white space
render_text((980, 1995, 1150, 2075), "组织不可知型\n152", f_ring, align='center')

cover_circle_safe_box((515, 2252, 715, 2325))
render_text((515, 2252, 715, 2325), "多癌种/实体瘤\n200", f_ring, align='center')

cover_circle_safe_box((0, 1985, 90, 2058))
render_text((0, 1985, 90, 2058), "其他癌种\n248", f_ring, align='center')

cover_circle_safe_box((70, 1255, 230, 1327))
render_text((70, 1255, 230, 1327), "结直肠癌\n297", f_ring, align='center')

# Panel b Legend Headers & Items
f_lh = get_font(25, bold=True)
f_li = get_font(21, bold=False)

cover_box((1205, 1238, 1425, 1275))
render_text((1205, 1238, 1425, 1275), "RAS 相关性分类", f_lh, align='left')

cover_box((1645, 1238, 1765, 1275))
render_text((1645, 1238, 1765, 1275), "临床分期", f_lh, align='left')

cover_box((1205, 1775, 1360, 1818))
render_text((1205, 1775, 1360, 1818), "申办方性质", f_lh, align='left')

cover_box((1645, 1775, 1765, 1812))
render_text((1645, 1775, 1765, 1812), "试验状态", f_lh, align='left')

# RAS relation items
cover_box((1315, 1315, 1515, 1352))
render_text((1315, 1315, 1515, 1352), "直接靶向 RAS", f_li, align='left')

cover_box((1315, 1415, 1525, 1452))
render_text((1315, 1415, 1525, 1452), "RAS 调控因子", f_li, align='left')

cover_box((1315, 1518, 1595, 1550))
render_text((1315, 1518, 1595, 1550), "生物标志物筛选", f_li, align='left')

cover_box((1315, 1620, 1545, 1650))
render_text((1315, 1620, 1545, 1650), "试验提及 RAS", f_li, align='left')

# Phase items
cover_box((1755, 1315, 1835, 1348))
render_text((1755, 1315, 1835, 1348), "早期 I 期", f_li, align='left')

cover_box((1755, 1415, 1820, 1448))
render_text((1755, 1415, 1820, 1448), "I 期", f_li, align='left')

cover_box((1755, 1518, 1820, 1550))
render_text((1755, 1518, 1820, 1550), "II 期", f_li, align='left')

cover_box((1755, 1620, 1820, 1650))
render_text((1755, 1620, 1820, 1650), "III 期", f_li, align='left')

# Sponsor items
cover_box((1315, 1850, 1435, 1882))
render_text((1315, 1850, 1435, 1882), "医药企业", f_li, align='left')

cover_box((1315, 1930, 1405, 1956))
render_text((1315, 1930, 1405, 1956), "学术机构/其他", f_li, align='left')

cover_box((1315, 2010, 1375, 2035))
render_text((1315, 2010, 1375, 2035), "美国 NIH", f_li, align='left')

cover_box((1315, 2090, 1440, 2116))
render_text((1315, 2090, 1440, 2116), "临床试验协作网", f_li, align='left')

cover_box((1315, 2170, 1380, 2195))
render_text((1315, 2170, 1380, 2195), "政府机构", f_li, align='left')

# Status items
cover_box((1755, 1850, 1915, 1882))
render_text((1755, 1850, 1915, 1882), "已完成", f_li, align='left')

cover_box((1755, 1930, 1885, 1962))
render_text((1755, 1930, 1885, 1962), "招募/进行中", f_li, align='left')

cover_box((1755, 2010, 1952, 2042))
render_text((1755, 2010, 1952, 2042), "尚未招募", f_li, align='left')

cover_box((1755, 2090, 1955, 2122))
render_text((1755, 2090, 1955, 2122), "提前终止", f_li, align='left')

cover_box((1755, 2170, 1955, 2195))
render_text((1755, 2170, 1955, 2195), "其他/未知", f_li, align='left')

# Panel c Timeline
f_c_ann = get_font(21, bold=False)
cover_box((1740, 2400, 1950, 2432))
render_text((1740, 2400, 1950, 2432), "统计截至 2026年10月", f_c_ann, align='right')

f_c_axis = get_font(24, bold=False)
cover_box((920, 2815, 1190, 2850))
render_text((920, 2815, 1190, 2850), "首次注册年份", f_c_axis, align='center')

# Y axis: 'Trials per year'
cover_box((0, 2450, 32, 2690))
txt_img = Image.new('RGBA', (350, 30), (255, 255, 255, 0))
txt_draw = ImageDraw.Draw(txt_img)
f_c_y = get_font(21, bold=False)
txt_draw.text((0, 2), "年注册试验数 (项)", fill=INK, font=f_c_y)
rotated = txt_img.rotate(90, expand=True)
im_cn.paste(rotated, (4, 2465), rotated)

# -------------------------------------------------------------------------
# Step 4: Save and Synchronize
# -------------------------------------------------------------------------
FIG_DIR = '/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/06_Figure4_Global_Trial_Landscape/vector_figures'

def save_svg(png_path, svg_path):
    with open(png_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    svg_content = f"""<?xml version='1.0' encoding='UTF-8' ?>
<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='481.89pt' height='684.86pt' viewBox='0 0 481.89 684.86'>
<rect width='100%' height='100%' style='stroke: none; fill: #FFFFFF;'/>
<image width='481.89' height='684.86' x='0' y='0' preserveAspectRatio='none' xlink:href='data:image/png;base64,{encoded_string}'/>
</svg>"""
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

# English outputs
out_en_png = os.path.join(FIG_DIR, 'Figure4_trial_atlas_EN.png')
out_en_pdf = os.path.join(FIG_DIR, 'Figure4_trial_atlas_EN.pdf')
out_en_svg = os.path.join(FIG_DIR, 'Figure4_trial_atlas_EN.svg')

im_en.save(out_en_png, dpi=(400, 400))
im_en.save(out_en_pdf, 'PDF', resolution=400)
save_svg(out_en_png, out_en_svg)

# Legacy aliases for EN
shutil.copy2(out_en_png, os.path.join(FIG_DIR, 'Figure4_trial_atlas.png'))
shutil.copy2(out_en_pdf, os.path.join(FIG_DIR, 'Figure4_trial_atlas.pdf'))
shutil.copy2(out_en_svg, os.path.join(FIG_DIR, 'Figure4_trial_atlas.svg'))

# Chinese outputs
out_cn_png = os.path.join(FIG_DIR, 'Figure4_trial_atlas_CN.png')
out_cn_pdf = os.path.join(FIG_DIR, 'Figure4_trial_atlas_CN.pdf')
out_cn_svg = os.path.join(FIG_DIR, 'Figure4_trial_atlas_CN.svg')
out_cn_alias_png = os.path.join(FIG_DIR, 'Figure4_全球临床试验全景_中文版.png')
out_cn_alias_pdf = os.path.join(FIG_DIR, 'Figure4_全球临床试验全景_中文版.pdf')
out_cn_alias_svg = os.path.join(FIG_DIR, 'Figure4_全球临床试验全景_中文版.svg')

im_cn.save(out_cn_png, dpi=(400, 400))
im_cn.save(out_cn_pdf, 'PDF', resolution=400)
save_svg(out_cn_png, out_cn_svg)

shutil.copy2(out_cn_png, out_cn_alias_png)
shutil.copy2(out_cn_pdf, out_cn_alias_pdf)
shutil.copy2(out_cn_svg, out_cn_alias_svg)

print('Successfully generated Figure 4 EN and CN suite!')

# Synchronize across directories
SYNC_DIRS = [
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件_新配色预览",
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件",
    "/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/New_Color_Theme_Preview",
]

for sdir in SYNC_DIRS:
    if os.path.exists(sdir):
        for f in [out_en_png, out_en_pdf, out_en_svg,
                  out_cn_png, out_cn_pdf, out_cn_svg,
                  out_cn_alias_png, out_cn_alias_pdf, out_cn_alias_svg]:
            shutil.copy2(f, os.path.join(sdir, os.path.basename(f)))
        print('Synchronized to:', sdir)

legacy_dst = "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件/图4_全球RAS试验全景-1.png"
if os.path.exists(os.path.dirname(legacy_dst)):
    shutil.copy2(out_cn_png, legacy_dst)
    print('Synchronized legacy file:', legacy_dst)
