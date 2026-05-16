import os
from fpdf import FPDF

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_PATH = None
for p in ["/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
          "/System/Library/Fonts/Hiragino Sans GB.ttc"]:
    if os.path.exists(p):
        FONT_PATH = p
        break


class JPPDF(FPDF):
    def __init__(self):
        super().__init__()
        if FONT_PATH:
            self.add_font("JP", "", FONT_PATH)
            self.add_font("JP", "B", FONT_PATH)
            self.f = "JP"
        else:
            self.f = "Helvetica"

    def header_title(self, title):
        self.set_font(self.f, "B", 18)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(3)

    def section(self, title):
        self.set_font(self.f, "B", 11)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def kv(self, key, value):
        self.set_font(self.f, "B", 9)
        self.cell(40, 6, key, new_x="RIGHT")
        self.set_font(self.f, "", 9)
        self.cell(0, 6, value, new_x="LMARGIN", new_y="NEXT")

    def table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [180 / len(headers)] * len(headers)
        self.set_font(self.f, "B", 9)
        self.set_fill_color(68, 114, 196)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, align="C", fill=True)
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font(self.f, "", 9)
        for row in rows:
            for i, val in enumerate(row):
                self.cell(col_widths[i], 6, str(val), border=1, align="C")
            self.ln()


def generate_quality_inspection():
    pdf = JPPDF()
    pdf.add_page()

    pdf.header_title("品質検査結果報告書")

    pdf.set_font(pdf.f, "", 9)
    pdf.cell(0, 5, "報告書番号: QC-2025-0178", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.cell(0, 5, "検査日: 2025-04-22", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.ln(3)

    pdf.section("1. 製品情報")
    pdf.kv("製品名:", "高精度ベアリング HB-7200A")
    pdf.kv("ロット番号:", "LOT-2025-04-0053")
    pdf.kv("製造ライン:", "第3製造ライン（大阪工場）")
    pdf.kv("製造日:", "2025-04-20")
    pdf.kv("検査数量:", "500個（抜取り検査: 50個）")
    pdf.ln(3)

    pdf.section("2. 検査担当")
    pdf.kv("検査員:", "佐藤一郎（品質管理部）")
    pdf.kv("承認者:", "田中部長（品質保証部）")
    pdf.kv("検査規格:", "JIS B 1521:2018 準拠")
    pdf.ln(3)

    pdf.section("3. 寸法検査結果")
    headers = ["検査項目", "規格値", "実測平均", "最小値", "最大値", "判定"]
    rows = [
        ("外径 (mm)", "72.00 ±0.02", "72.003", "71.985", "72.018", "合格"),
        ("内径 (mm)", "35.00 ±0.015", "35.001", "34.988", "35.012", "合格"),
        ("幅 (mm)", "17.00 ±0.03", "17.005", "16.978", "17.025", "合格"),
        ("真円度 (μm)", "≤ 5.0", "2.8", "1.2", "4.6", "合格"),
        ("表面粗さ Ra (μm)", "≤ 0.4", "0.25", "0.18", "0.38", "合格"),
    ]
    col_widths = [35, 28, 25, 22, 22, 18]
    pdf.table(headers, rows, col_widths)
    pdf.ln(3)

    pdf.section("4. 性能試験結果")
    headers2 = ["試験項目", "基準値", "測定値", "判定"]
    rows2 = [
        ("回転トルク (N・cm)", "≤ 2.5", "1.8", "合格"),
        ("振動値 (μm)", "≤ 15", "8.3", "合格"),
        ("騒音レベル (dB)", "≤ 45", "38", "合格"),
        ("耐荷重試験 (kN)", "≥ 25.0", "28.5", "合格"),
        ("耐久回転数 (万回転)", "≥ 100", "152", "合格"),
    ]
    col_widths2 = [45, 35, 30, 20]
    pdf.table(headers2, rows2, col_widths2)
    pdf.ln(3)

    pdf.section("5. 総合判定")
    pdf.set_font(pdf.f, "B", 12)
    pdf.set_text_color(0, 128, 0)
    pdf.cell(0, 10, "総合判定: 合格", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font(pdf.f, "", 9)
    pdf.ln(2)
    pdf.kv("不良率:", "0.0%（0/50個）")
    pdf.kv("Cpk値:", "1.85（工程能力十分）")
    pdf.ln(3)

    pdf.section("6. 備考")
    pdf.set_font(pdf.f, "", 9)
    pdf.multi_cell(0, 5, "・全項目において規格内であり、出荷可能と判断する。\n・前回ロット(LOT-2025-04-0052)と比較し、真円度が改善傾向。\n・次回検査時は耐久試験のサンプル数を10個に増加予定。")

    out_path = os.path.join(OUTPUT_DIR, "quality_inspection.pdf")
    pdf.output(out_path)
    print(f"Generated: {out_path}")


def generate_delivery_note():
    pdf = JPPDF()
    pdf.add_page()

    pdf.header_title("納品書")

    pdf.set_font(pdf.f, "", 9)
    pdf.cell(0, 5, "納品書番号: DL-2025-03421", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.cell(0, 5, "納品日: 2025-04-25", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.ln(3)

    pdf.section("納品先")
    pdf.kv("会社名:", "株式会社山田製作所")
    pdf.kv("住所:", "愛知県豊田市トヨタ町1番地")
    pdf.kv("担当者:", "鈴木次郎 様")
    pdf.kv("発注番号:", "PO-2025-8890")
    pdf.ln(3)

    pdf.section("納品元")
    pdf.kv("会社名:", "東海精密工業株式会社")
    pdf.kv("住所:", "静岡県浜松市中区田町230-21")
    pdf.kv("担当者:", "高橋三郎")
    pdf.kv("TEL:", "053-456-7890")
    pdf.ln(3)

    pdf.section("納品明細")
    headers = ["No.", "品番", "品名", "数量", "単位", "備考"]
    rows = [
        ("1", "HB-7200A", "高精度ベアリング", "200", "個", ""),
        ("2", "HB-7200B", "高精度ベアリング（防水）", "100", "個", "新規"),
        ("3", "SL-3300", "シールリング", "300", "個", ""),
        ("4", "GR-500W", "専用グリース", "20", "kg", ""),
        ("5", "MT-100", "取付治具セット", "5", "セット", "貸出品"),
    ]
    col_widths = [12, 25, 50, 18, 18, 27]
    pdf.table(headers, rows, col_widths)
    pdf.ln(5)

    pdf.section("特記事項")
    pdf.set_font(pdf.f, "", 9)
    pdf.multi_cell(0, 5, "・品番HB-7200B は初回納品のため、品質検査報告書(QC-2025-0178)を添付。\n・MT-100（取付治具セット）は貸出品です。使用後にご返却ください。\n・検収期限: 2025年5月9日")
    pdf.ln(5)

    pdf.set_font(pdf.f, "", 8)
    pdf.cell(0, 5, "受領確認欄:", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "受領日: ______年______月______日  受領者サイン: ________________", new_x="LMARGIN", new_y="NEXT")

    out_path = os.path.join(OUTPUT_DIR, "delivery_note.pdf")
    pdf.output(out_path)
    print(f"Generated: {out_path}")


def generate_meeting_minutes():
    pdf = JPPDF()
    pdf.add_page()

    pdf.header_title("議事録")

    pdf.set_font(pdf.f, "", 9)
    pdf.cell(0, 5, "文書番号: MTG-2025-0415-01", new_x="LMARGIN", new_y="NEXT", align="R")
    pdf.ln(3)

    pdf.section("会議情報")
    pdf.kv("会議名:", "Q1レビュー & Q2計画会議")
    pdf.kv("日時:", "2025年4月15日（火）14:00〜16:00")
    pdf.kv("場所:", "本社5F 会議室A（オンライン併用）")
    pdf.kv("出席者:", "木村部長、松本課長、渡辺、小林、加藤（計5名）")
    pdf.kv("議事録作成:", "加藤")
    pdf.ln(3)

    pdf.section("1. Q1実績報告（松本課長）")
    pdf.set_font(pdf.f, "", 9)
    pdf.multi_cell(0, 5, "・売上: 目標比 112%（18.5億円 / 目標16.5億円）\n・新規顧客獲得: 8社（目標5社を上回る）\n・主要案件: A社向けベアリング量産（3.2億円）が大きく貢献\n・課題: 原材料費高騰により粗利率が前年比 -2.3pt")
    pdf.ln(3)

    pdf.section("2. Q2計画（木村部長）")
    pdf.set_font(pdf.f, "", 9)
    pdf.multi_cell(0, 5, "・売上目標: 20億円（前年同期比 +15%）\n・重点施策:\n  1. A社追加案件の受注確定（5月末目標）\n  2. B社向け新製品(HB-7200B)の量産立上げ\n  3. 海外展開: タイ工場での試作開始（6月）\n・投資計画: 検査装置1台追加導入（予算2,500万円）")
    pdf.ln(3)

    pdf.section("3. 決定事項")
    headers = ["No.", "決定事項", "担当", "期限"]
    rows = [
        ("1", "A社追加案件の見積提出", "松本", "2025/5/10"),
        ("2", "HB-7200B量産ラインの工程設計完了", "渡辺", "2025/5/20"),
        ("3", "タイ工場視察の出張計画策定", "小林", "2025/5/15"),
        ("4", "検査装置の選定・稟議書作成", "加藤", "2025/5/30"),
    ]
    col_widths = [12, 75, 20, 28]
    pdf.table(headers, rows, col_widths)
    pdf.ln(3)

    pdf.section("4. 次回会議")
    pdf.kv("日時:", "2025年5月20日（火）14:00〜")
    pdf.kv("議題:", "Q2進捗確認、A社案件状況、タイ工場計画詳細")

    out_path = os.path.join(OUTPUT_DIR, "meeting_minutes.pdf")
    pdf.output(out_path)
    print(f"Generated: {out_path}")


if __name__ == "__main__":
    generate_quality_inspection()
    generate_delivery_note()
    generate_meeting_minutes()
    print("\nDone! Additional sample PDFs generated.")
