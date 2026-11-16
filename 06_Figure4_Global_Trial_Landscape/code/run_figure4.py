import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont

SRC_IMG = '/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/06_Figure4_Global_Trial_Landscape/vector_figures/Figure4_trial_atlas.png'
im = Image.open(SRC_IMG).convert('RGB')
w, h = im.size
draw = ImageDraw.Draw(im)

FONT_PATH = '/System/Library/Fonts/Hiragino Sans GB.ttc'
if not os.path.exists(FONT_PATH):
    FONT_PATH = '/System/Library/Fonts/PingFang.ttc'

def get_font(size, bold=False):
    idx = 1 if bold else 0
    return ImageFont.truetype(FONT_PATH, size, index=idx)

INK = '#1A1A1A'
WHITE = '#FFFFFF'

def cover_and_text(box, text, font, color=INK, align='left', line_spacing=4):
    draw.rectangle(box, fill=WHITE)
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
        draw.text((cur_x, cur_y), line, fill=color, font=font)
        cur_y += line_heights[i] + line_spacing

f_ctry = get_font(22, bold=False)
f_ctry_b = get_font(22, bold=True)

# 1. Panel a: Map Legend Title
f_leg_t = get_font(22, bold=True)
cover_and_text((5, 700, 160, 765), "试验中心分布\n(含 ≥1 个中心)", f_leg_t, align='left')

# 2. Panel a: Countries
# Canada 112: (736, 62, 891, 83)
cover_and_text((730, 60, 905, 87), "加拿大 112", f_ctry_b, align='left')
# Germany 122: (955, 70, 1131, 97)
cover_and_text((950, 68, 1140, 99), "德国 122", f_ctry_b, align='left')
# UK 101: (729, 169, 820, 190)
cover_and_text((725, 166, 830, 193), "英国 101", f_ctry_b, align='left')
# France 154: (680, 260, 824, 274)
cover_and_text((675, 255, 830, 278), "法国 154", f_ctry_b, align='left')
# Spain 189: (694, 344, 824, 371)
cover_and_text((688, 340, 830, 374), "西班牙 189", f_ctry_b, align='left')
# Italy 155: (990, 421, 1097, 447)
cover_and_text((980, 417, 1105, 450), "意大利 155", f_ctry_b, align='left')
# USA 644: (92, 428, 207, 449)
cover_and_text((88, 425, 220, 452), "美国 644", f_ctry_b, align='left')
# China 256: (1287, 266, 1420, 287)
cover_and_text((1280, 262, 1430, 290), "中国 256", f_ctry_b, align='left')
# Japan 82: (1822, 291, 1940, 317)
cover_and_text((1815, 287, 1945, 320), "日本 82", f_ctry_b, align='left')
# South Korea 120: (1749, 466, 1967, 480)
cover_and_text((1740, 462, 1975, 484), "韩国 120", f_ctry_b, align='left')
# Australia 127: (1643, 984, 1814, 1005)
cover_and_text((1635, 980, 1825, 1009), "澳大利亚 127", f_ctry_b, align='left')

# 3. Panel b: Tumour Ring Labels
f_ring = get_font(23, bold=False)
# Haematologic 59: (551, 1131, 760, 1193)
cover_and_text((540, 1125, 770, 1198), "血液肿瘤\n59", f_ring, align='center')
# Pancreatic 77: (786, 1227, 947, 1300)
cover_and_text((775, 1220, 955, 1305), "胰腺癌\n77", f_ring, align='center')
# NSCLC 149: (950, 1511, 1130, 1600)
cover_and_text((945, 1505, 1140, 1605), "非小细胞肺癌\n149", f_ring, align='left')
# Histology-agnostic 152: (850, 2000, 1061, 2111)
cover_and_text((845, 1995, 1140, 2115), "组织不可知型\n152", f_ring, align='left')
# Multi-tumour 200: (520, 2258, 710, 2320)
cover_and_text((510, 2250, 720, 2325), "多癌种/实体瘤\n200", f_ring, align='center')
# Other 248: (1, 2000, 85, 2053)
cover_and_text((0, 1990, 100, 2060), "其他癌种\n248", f_ring, align='center')
# Colorectal 297: (75, 1260, 227, 1322)
cover_and_text((70, 1255, 235, 1328), "结直肠癌\n297", f_ring, align='center')

# 4. Panel b: Legends
f_lh = get_font(25, bold=True)
f_li = get_font(21, bold=False)

# Headers
# Header RAS: (1213, 1244, 1377, 1250) -> wait, header is around y=1240-1280
cover_and_text((1205, 1235, 1420, 1275), "RAS 相关性分类", f_lh, align='left')
cover_and_text((1645, 1235, 1850, 1275), "临床分期", f_lh, align='left')
cover_and_text((1205, 1790, 1420, 1830), "申办方性质", f_lh, align='left')
cover_and_text((1645, 1790, 1850, 1830), "试验状态", f_lh, align='left')

# RAS relation items: (1300, 1300, 1509, 1360), (1320, 1421, 1520, 1451)...
cover_and_text((1305, 1320, 1530, 1348), "直接靶向 RAS", f_li, align='left')
cover_and_text((1305, 1420, 1530, 1448), "RAS 调控因子", f_li, align='left')
cover_and_text((1305, 1520, 1600, 1548), "生物标志物筛选", f_li, align='left')
cover_and_text((1305, 1620, 1550, 1648), "试验提及 RAS", f_li, align='left')

# Phase items
cover_and_text((1750, 1320, 1870, 1348), "早期 I 期", f_li, align='left')
cover_and_text((1750, 1420, 1850, 1448), "I 期", f_li, align='left')
cover_and_text((1750, 1520, 1850, 1548), "II 期", f_li, align='left')
cover_and_text((1750, 1620, 1850, 1648), "III 期", f_li, align='left')

# Sponsor items
cover_and_text((1305, 1870, 1450, 1898), "医药企业", f_li, align='left')
cover_and_text((1305, 1950, 1500, 1978), "学术机构/其他", f_li, align='left')
cover_and_text((1305, 2030, 1450, 2058), "美国 NIH", f_li, align='left')
cover_and_text((1305, 2110, 1520, 2138), "临床试验协作网", f_li, align='left')
cover_and_text((1305, 2190, 1450, 2218), "政府机构", f_li, align='left')

# Status items
cover_and_text((1750, 1870, 1880, 1898), "已完成", f_li, align='left')
cover_and_text((1750, 1950, 1920, 1978), "招募/进行中", f_li, align='left')
cover_and_text((1750, 2030, 1880, 2058), "尚未招募", f_li, align='left')
cover_and_text((1750, 2110, 1880, 2138), "提前终止", f_li, align='left')
cover_and_text((1750, 2190, 1880, 2218), "其他/未知", f_li, align='left')

# 5. Panel c
f_c_ann = get_font(21, bold=False)
cover_and_text((1680, 2375, 1960, 2415), "统计截至 2026年10月", f_c_ann, align='right')

f_c_axis = get_font(24, bold=False)
cover_and_text((880, 2955, 1200, 3005), "首次注册年份", f_c_axis, align='center')

# Y axis: 'Trials per year'
draw.rectangle((0, 2400, 40, 2750), fill=WHITE)
txt_img = Image.new('RGBA', (350, 40), (255, 255, 255, 0))
txt_draw = ImageDraw.Draw(txt_img)
txt_draw.text((0, 2), "年注册试验数 (项)", fill=INK, font=f_c_axis)
rotated = txt_img.rotate(90, expand=True)
im.paste(rotated, (2, 2410), rotated)

# Save Chinese Outputs
FIG_DIR = '/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/06_Figure4_Global_Trial_Landscape/vector_figures'
out_cn_png = os.path.join(FIG_DIR, 'Figure4_trial_atlas_CN.png')
out_cn_pdf = os.path.join(FIG_DIR, 'Figure4_trial_atlas_CN.pdf')
out_cn_alias_png = os.path.join(FIG_DIR, 'Figure4_全球临床试验全景_中文版.png')
out_cn_alias_pdf = os.path.join(FIG_DIR, 'Figure4_全球临床试验全景_中文版.pdf')

im.save(out_cn_png, dpi=(400, 400))
im.save(out_cn_pdf, 'PDF', resolution=400)
shutil.copy2(out_cn_png, out_cn_alias_png)
shutil.copy2(out_cn_pdf, out_cn_alias_pdf)
print('Successfully generated Figure 4 CN PNG & PDF!')

SYNC_DIRS = [
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件_新配色预览",
    "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件",
    "/Users/wangnianfei/Desktop/ESMO/05_开源复现仓库/New_Color_Theme_Preview",
]

for sdir in SYNC_DIRS:
    if os.path.exists(sdir):
        for f in [out_cn_png, out_cn_pdf, out_cn_alias_png, out_cn_alias_pdf]:
            shutil.copy2(f, os.path.join(sdir, os.path.basename(f)))
        print('Synchronized to:', sdir)

legacy_dst = "/Users/wangnianfei/Desktop/ESMO/03_数据与图表/图件/图4_全球RAS试验全景-1.png"
if os.path.exists(os.path.dirname(legacy_dst)):
    shutil.copy2(out_cn_png, legacy_dst)
    print('Synchronized legacy file:', legacy_dst)
