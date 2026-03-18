import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from pathlib import Path

# ---- tracker.md を読み込む ----
tracker_path = Path(__file__).parent / "tracker.md"
text = tracker_path.read_text(encoding="utf-8")

# ---- Tier ごとの色設定 ----
TIER_STYLES = {
    "A": {"color": "C0392B", "bg": "FADBD8"},
    "B": {"color": "E67E22", "bg": "FDEBD0"},
    "C": {"color": "2980B9", "bg": "D6EAF8"},
    "D": {"color": "7F8C8D", "bg": "F2F3F4"},
}
WHITE     = "FFFFFF"
HEADER_BG = "2C3E50"

# ---- tracker.md をパース ----
# Tier セクションを検出: "## Tier A（...）" の形式
section_pattern = re.compile(r"^## Tier ([ABCD])[（(]", re.MULTILINE)
# テーブル行を検出: | で始まる行（ヘッダー行・区切り行を除く）
row_pattern = re.compile(r"^\|(.+)\|$", re.MULTILINE)
# マークダウンリンク [text](url) → text
link_pattern = re.compile(r"\[([^\]]+)\]\([^)]+\)")

sections = []
section_matches = list(section_pattern.finditer(text))

for i, match in enumerate(section_matches):
    tier = match.group(1)
    start = match.end()
    end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(text)
    block = text[start:end]

    rows = []
    for row_match in row_pattern.finditer(block):
        cells = [c.strip() for c in row_match.group(1).split("|")]
        # ヘッダー行（企業名 を含む）と区切り行（--- を含む）をスキップ
        if any("企業名" in c or "---" in c for c in cells):
            continue
        # マークダウンリンクを除去
        cells = [link_pattern.sub(r"\1", c) for c in cells]
        # 空行をスキップ
        if all(c == "" or c == "-" for c in cells):
            continue
        # 6列に揃える（足りない場合は空文字で補完）
        while len(cells) < 6:
            cells.append("")
        rows.append(tuple(cells[:6]))

    if rows:
        sections.append({"tier": tier, "rows": rows})

# ---- Excel 生成 ----
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "求職トラッカー"

thin = Side(style="thin", color="CCCCCC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

headers = ["企業名", "ターゲット職種", "採用形態", "ステータス", "応募日", "次のアクション"]

# ヘッダー行
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=h)
    cell.font = Font(bold=True, color=WHITE, size=11)
    cell.fill = PatternFill("solid", fgColor=HEADER_BG)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = border
ws.row_dimensions[1].height = 24

# データ行
current_row = 2
for section in sections:
    tier = section["tier"]
    style = TIER_STYLES.get(tier, TIER_STYLES["D"])

    # セクション見出し行
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=6)
    label_cell = ws.cell(row=current_row, column=1, value=f"Tier {tier}")
    label_cell.font = Font(bold=True, color=WHITE, size=10)
    label_cell.fill = PatternFill("solid", fgColor=style["color"])
    label_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    label_cell.border = border
    ws.row_dimensions[current_row].height = 20
    current_row += 1

    for row_data in section["rows"]:
        for col, val in enumerate(row_data, 1):
            cell = ws.cell(row=current_row, column=col, value=val)
            cell.fill = PatternFill("solid", fgColor=style["bg"])
            cell.alignment = Alignment(
                vertical="center", wrap_text=True,
                horizontal="center" if col in (3, 4, 5) else "left"
            )
            cell.font = Font(size=10)
            cell.border = border
        ws.row_dimensions[current_row].height = 32
        current_row += 1

# 列幅
col_widths = [22, 30, 14, 12, 12, 44]
for i, w in enumerate(col_widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

ws.freeze_panes = "A2"

# 保存（スクリプトと同じフォルダに出力）
out = Path(__file__).parent / "求職トラッカー.xlsx"
wb.save(out)
print(f"saved: {out}")
