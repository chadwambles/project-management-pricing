"""Builds the project management pricing workbook.

Every number a reader sees is a formula over the Tiers sheet and the Inputs
panel, so changing a seat count or ticking a requirement recalculates the
whole comparison. Nothing is computed in Python and pasted in.
"""
import csv, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import LineChart, Reference

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "project-management-pricing-2026-10.xlsx")

ARIAL = "Arial"
INPUT = Font(name=ARIAL, size=10, color="0000FF")           # editable input
CALC = Font(name=ARIAL, size=10)                            # formula
LINK = Font(name=ARIAL, size=10, color="008000")            # link to another sheet
HEAD = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
TITLE = Font(name=ARIAL, size=14, bold=True)
SUB = Font(name=ARIAL, size=10, color="595959")
YELL = PatternFill("solid", fgColor="FFFF00")
NAVY = PatternFill("solid", fgColor="1F3864")
GREY = PatternFill("solid", fgColor="F2F2F2")
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))
MONEY = '$#,##0.00;($#,##0.00);-'
MONEY0 = '$#,##0;($#,##0);-'

tiers = list(csv.DictReader(open(os.path.join(SRC, "tiers.csv"))))
gates = {(r["vendor"], r["tier"]): r
         for r in csv.DictReader(open(os.path.join(SRC, "gates.csv")))}
bands = list(csv.DictReader(open(os.path.join(SRC, "volume_bands.csv"))))
addons = list(csv.DictReader(open(os.path.join(SRC, "addons.csv"))))
thin = list(csv.DictReader(open(os.path.join(SRC, "thin_set.csv"))))

wb = Workbook()

# ---------------------------------------------------------------------------
def header(ws, row, labels, widths=None):
    for i, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=i, value=t)
        c.font = HEAD; c.fill = NAVY
        c.alignment = Alignment(vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)

# ---------------------------------------------------------------------------
# Read me
# ---------------------------------------------------------------------------
ws = wb.active; ws.title = "Read me"
ws.column_dimensions["A"].width = 110
lines = [
 ("Project management software pricing, October 2026", TITLE),
 ("", None),
 ("A snapshot of what fifteen project management tools charge, and a model that works out "
  "which tier you actually land on once you say how big your team is and what it needs.", CALC),
 ("", None),
 ("HOW TO USE IT", Font(name=ARIAL, size=11, bold=True)),
 ("Open the Inputs sheet and change the cells in blue on a yellow background. Nothing else "
  "is meant to be edited. Every other number recalculates from those.", CALC),
 ("", None),
 ("WHAT EACH SHEET IS", Font(name=ARIAL, size=11, bold=True)),
 ("Inputs      the levers: team size, growth, billing cadence, and what the tool must do", CALC),
 ("Model       every tier scored against your inputs, with the reason any tier is ruled out", CALC),
 ("Grid        cost per month at six fixed team sizes, used by the comparison and the chart", CALC),
 ("Compare     the cheapest qualifying tier per vendor at each team size, and the chart", CALC),
 ("Tiers       the collected data, one row per vendor tier", CALC),
 ("Bands       vendors whose per-seat price falls as the team grows", CALC),
 ("Add-ons     capabilities sold separately rather than included in a tier", CALC),
 ("Thin set    price visibility across the wider category, no prices collected", CALC),
 ("Method      how the data was collected and what is wrong with it", CALC),
 ("", None),
 ("THE THREE THINGS TO KNOW BEFORE TRUSTING A NUMBER", Font(name=ARIAL, size=11, bold=True)),
 ("1. Prices were collected on 2 October 2026 from vendors' own pricing pages. "
  "Software pricing moves quarterly. This is a snapshot, not a feed.", CALC),
 ("2. A capability the pricing page does not claim is treated as absent. That is the right "
  "default for a buyer and it understates vendors with vague pages.", CALC),
 ("3. Two vendors do not price by seat at all. Basecamp charges a flat fee and TeamGantt "
  "charges by project, so a per-seat comparison does not describe them. They are in the "
  "model where it is meaningful and excluded where it is not.", CALC),
]
r = 1
for text, font in lines:
    c = ws.cell(row=r, column=1, value=text)
    if font: c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1

# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
ws = wb.create_sheet("Inputs")
ws.column_dimensions["A"].width = 44
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 60
ws["A1"] = "Inputs"; ws["A1"].font = TITLE
ws["A2"] = "Edit the blue cells only. Everything else in the workbook follows from them."
ws["A2"].font = SUB

rows = [
 (4, "YOUR TEAM", None, None, None),
 (5, "Seats today", 25, "0", "How many people need a paid seat now."),
 (6, "Annual growth in seats", 0.20, "0.0%", "Used to project seats over the horizon."),
 (7, "Horizon, months", 36, "0", "Length of the commitment you are costing."),
 (8, "Billing cadence", "annual", None, "annual or monthly. Annual is cheaper everywhere in this data, by 14% to 37%."),
 (10, "WHAT THE TOOL MUST DO", None, None, None),
 (11, "Require SAML single sign-on", "no", None, "yes or no. Set yes and watch how few tiers survive."),
 (12, "Require an audit log", "no", None, "yes or no."),
 (13, "Require Gantt or timeline views", "no", None, "yes or no."),
]
for row, label, val, fmt, note in rows:
    a = ws.cell(row=row, column=1, value=label)
    if val is None:
        a.font = Font(name=ARIAL, size=10, bold=True); continue
    a.font = CALC
    b = ws.cell(row=row, column=2, value=val)
    b.font = INPUT; b.fill = YELL; b.border = THIN
    if fmt: b.number_format = fmt
    c = ws.cell(row=row, column=3, value=note); c.font = SUB
    c.alignment = Alignment(wrap_text=True, vertical="center")

ws.add_data_validation(DataValidation(type="list", formula1='"annual,monthly"', allow_blank=False))
ws.data_validations.dataValidation[0].add("B8")
yn = DataValidation(type="list", formula1='"yes,no"', allow_blank=False)
ws.add_data_validation(yn); yn.add("B11"); yn.add("B12"); yn.add("B13")

ws["A15"] = "Seats at the end of the horizon"
ws["A15"].font = CALC
ws["B15"] = "=ROUND(B5*(1+B6)^(B7/12),0)"
ws["B15"].font = CALC; ws["B15"].number_format = "0"
ws["C15"] = "Calculated, not an input."; ws["C15"].font = SUB

# ---------------------------------------------------------------------------
# Tiers (the data)
# ---------------------------------------------------------------------------
ws = wb.create_sheet("Tiers")
cols = ["Vendor","Tier","Order","Pricing model","Price per seat, annual",
        "Price per seat, monthly","Flat price, annual","Flat price, monthly",
        "Min seats","Max seats","Free tier","Price visible","SAML SSO",
        "Audit log","Gantt or timeline","Notes","Source","Collected"]
header(ws, 1, cols, [16,24,7,13,13,13,12,12,9,9,9,12,10,10,11,52,46,11])
for i, t in enumerate(tiers):
    g = gates.get((t["vendor"], t["tier"]), {})
    def num(x):
        return float(x) if x not in ("", None) else None
    vals = [t["vendor"], t["tier"], int(t["tier_order"]), t["pricing_model"],
            num(t["price_annual_usd"]), num(t["price_monthly_usd"]),
            num(t["flat_annual_usd"]), num(t["flat_monthly_usd"]),
            num(t["min_seats"]), num(t["max_seats"]), t["is_free"],
            t["price_visible"], g.get("saml_sso",""), g.get("audit_log",""),
            g.get("gantt_timeline",""), t["notes"], t["pricing_url"], t["collected_on"]]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=i+2, column=j, value=v)
        c.font = CALC
        if j in (5,6,7,8): c.number_format = MONEY
    if i % 2:
        for j in range(1, len(cols)+1):
            ws.cell(row=i+2, column=j).fill = GREY
N = len(tiers)
LAST = N + 1

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
ws = wb.create_sheet("Model")
cols = ["Vendor","Tier","Seats billed","Within seat cap","Price published",
        "Meets requirements","Qualifies","Cost per month","Cost over horizon",
        "Why it is ruled out"]
header(ws, 1, cols, [16,24,11,12,12,13,10,13,14,46])
for i in range(N):
    r = i + 2; t = r  # same row number on Tiers
    f = lambda s: s.format(t=t)
    ws.cell(row=r, column=1, value=f("=Tiers!A{t}")).font = LINK
    ws.cell(row=r, column=2, value=f("=Tiers!B{t}")).font = LINK
    ws.cell(row=r, column=3,
            value=f("=MAX(Inputs!$B$5,IF(Tiers!I{t}=\"\",1,Tiers!I{t}))")).font = CALC
    ws.cell(row=r, column=4,
            value=f("=IF(Tiers!J{t}=\"\",1,IF(Inputs!$B$5<=Tiers!J{t},1,0))")).font = CALC
    ws.cell(row=r, column=5, value=f("=IF(Tiers!L{t}=\"public\",1,0)")).font = CALC
    ws.cell(row=r, column=6, value=f(
        "=IF(AND("
        "IF(Inputs!$B$11=\"yes\",Tiers!M{t}=\"yes\",TRUE),"
        "IF(Inputs!$B$12=\"yes\",Tiers!N{t}=\"yes\",TRUE),"
        "IF(Inputs!$B$13=\"yes\",Tiers!O{t}=\"yes\",TRUE)),1,0)")).font = CALC
    # Free tiers are excluded from the paid comparison: at small team sizes a
    # free tier wins trivially and tells the buyer nothing about cost.
    ws.cell(row=r, column=7,
            value=f("=IF(Tiers!K{t}=\"yes\",0,D{t}*E{t}*F{t})")).font = CALC
    ws.cell(row=r, column=8, value=f(
        "=IF(G{t}=0,\"\","
        "IF(Tiers!D{t}=\"per_seat\","
        "  IF(Inputs!$B$8=\"annual\",IF(Tiers!E{t}=\"\",\"\",Tiers!E{t}*C{t}),"
        "                            IF(Tiers!F{t}=\"\",\"\",Tiers!F{t}*C{t})),"
        "IF(Tiers!D{t}=\"flat\","
        "  IF(Inputs!$B$8=\"annual\",IF(Tiers!G{t}=\"\",\"\",Tiers!G{t}/12),"
        "                            IF(Tiers!H{t}=\"\",\"\",Tiers!H{t})),"
        "\"\")))")).font = CALC
    ws.cell(row=r, column=8).number_format = MONEY
    ws.cell(row=r, column=9,
            value=f("=IF(H{t}=\"\",\"\",H{t}*Inputs!$B$7)")).font = CALC
    ws.cell(row=r, column=9).number_format = MONEY0
    ws.cell(row=r, column=10, value=f(
        "=IF(Tiers!K{t}=\"yes\",\"free tier, excluded from the paid comparison\","
        "IF(D{t}=0,\"team is larger than this tier's seat cap\","
        "IF(E{t}=0,\"no published price, contact sales\","
        "IF(F{t}=0,\"does not meet a required capability\","
        "IF(H{t}=\"\",\"not priced on the chosen billing cadence\",\"\")))))")).font = CALC
    if i % 2:
        for j in range(1, len(cols)+1):
            ws.cell(row=r, column=j).fill = GREY

# ---------------------------------------------------------------------------
# Grid: cost at fixed team sizes
# ---------------------------------------------------------------------------
SIZES = [5, 10, 25, 50, 100, 250]
ws = wb.create_sheet("Grid")
ws["A1"] = "Cost per month at fixed team sizes"; ws["A1"].font = TITLE
ws["A2"] = ("Uses the capability requirements from Inputs but ignores the seat count there, "
            "so the comparison holds requirements fixed while team size varies.")
ws["A2"].font = SUB
header(ws, 4, ["Vendor","Tier"] + ["%d seats" % s for s in SIZES], [16,24,12,12,12,12,12,12])
for i in range(N):
    r = i + 5; t = i + 2
    ws.cell(row=r, column=1, value="=Tiers!A%d" % t).font = LINK
    ws.cell(row=r, column=2, value="=Tiers!B%d" % t).font = LINK
    for k, s in enumerate(SIZES):
        col = 3 + k
        ws.cell(row=r, column=col, value=(
            "=IF(Tiers!K{t}=\"yes\",\"\","
            "IF(Model!F{t}=0,\"\","
            "IF(Tiers!L{t}<>\"public\",\"\","
            "IF(AND(Tiers!J{t}<>\"\",{s}>Tiers!J{t}),\"\","
            "IF(Tiers!D{t}=\"per_seat\","
            "  IF(Inputs!$B$8=\"annual\",IF(Tiers!E{t}=\"\",\"\",Tiers!E{t}*MAX({s},IF(Tiers!I{t}=\"\",1,Tiers!I{t}))),"
            "                            IF(Tiers!F{t}=\"\",\"\",Tiers!F{t}*MAX({s},IF(Tiers!I{t}=\"\",1,Tiers!I{t})))),"
            "IF(Tiers!D{t}=\"flat\","
            "  IF(Inputs!$B$8=\"annual\",IF(Tiers!G{t}=\"\",\"\",Tiers!G{t}/12),"
            "                            IF(Tiers!H{t}=\"\",\"\",Tiers!H{t})),"
            "\"\"))))))").format(t=t, s=s)).font = CALC
        ws.cell(row=r, column=col).number_format = MONEY
    if i % 2:
        for j in range(1, 9):
            ws.cell(row=r, column=j).fill = GREY
GLAST = N + 4

# ---------------------------------------------------------------------------
# Compare: cheapest qualifying tier per vendor at each size
# ---------------------------------------------------------------------------
vendors = []
for t in tiers:
    if t["vendor"] not in vendors:
        vendors.append(t["vendor"])
ws = wb.create_sheet("Compare")
ws["A1"] = "Cheapest qualifying tier, by team size"; ws["A1"].font = TITLE
ws["A2"] = ("Blank means no tier from that vendor qualifies at that size: either every tier is "
            "capped below it, or none meets the requirements set on Inputs, or the tier that "
            "would is contact-sales.")
ws["A2"].font = SUB
header(ws, 4, ["Vendor"] + ["%d seats" % s for s in SIZES] + ["$ per seat at 100"],
       [20,13,13,13,13,13,13,16])
for i, v in enumerate(vendors):
    r = i + 5
    ws.cell(row=r, column=1, value=v).font = CALC
    for k, s in enumerate(SIZES):
        col = 2 + k
        gcol = get_column_letter(3 + k)
        # MINIFS returns 0, not an error, when no row qualifies. No real tier
        # costs nothing here (free tiers are excluded), so 0 means "none".
        ws.cell(row=r, column=col, value=(
            "=IF(IFERROR(_xlfn.MINIFS(Grid!${c}$5:${c}${last},Grid!$A$5:$A${last},$A{r}),0)=0,"
            "\"\",_xlfn.MINIFS(Grid!${c}$5:${c}${last},Grid!$A$5:$A${last},$A{r}))"
        ).format(c=gcol, last=GLAST, r=r)).font = CALC
        ws.cell(row=r, column=col).number_format = MONEY
    ws.cell(row=r, column=8, value="=IF(F{r}=\"\",\"\",F{r}/100)".format(r=r)).font = CALC
    ws.cell(row=r, column=8).number_format = MONEY
    if i % 2:
        for j in range(1, 9):
            ws.cell(row=r, column=j).fill = GREY
CLAST = len(vendors) + 4

ws.cell(row=CLAST + 2, column=1, value="Cheapest of all vendors").font = Font(
    name=ARIAL, size=10, bold=True)
for k in range(len(SIZES)):
    col = 2 + k
    L = get_column_letter(col)
    c = ws.cell(row=CLAST + 2, column=col,
                value="=IFERROR(MIN({L}5:{L}{last}),\"\")".format(L=L, last=CLAST))
    c.font = Font(name=ARIAL, size=10, bold=True); c.number_format = MONEY

# Six vendors charted rather than fifteen: the point is the shape of flat
# against per-seat pricing, and fifteen overlapping lines hides it.
PICK = ["Basecamp", "Zoho Projects", "Trello", "ClickUp", "Jira", "Asana"]
crow = CLAST + 4
ws.cell(row=crow, column=1, value="Chart data").font = Font(name=ARIAL, size=10, bold=True)
for k, s_ in enumerate(SIZES):
    c = ws.cell(row=crow, column=2 + k, value=s_)
    c.font = Font(name=ARIAL, size=10, bold=True)
for i, v in enumerate(PICK):
    r = crow + 1 + i
    ws.cell(row=r, column=1, value=v).font = CALC
    for k in range(len(SIZES)):
        L = get_column_letter(2 + k)
        ws.cell(row=r, column=2 + k, value=(
            "=IFERROR(INDEX(${L}$5:${L}${last},MATCH($A{r},$A$5:$A${last},0)),\"\")"
        ).format(L=L, last=CLAST, r=r)).font = CALC
        ws.cell(row=r, column=2 + k).number_format = MONEY

chart = LineChart()
chart.title = "Cheapest qualifying cost per month, by team size"
chart.y_axis.title = "Cost per month"
chart.x_axis.title = "Team size"
chart.height, chart.width = 10, 24
data = Reference(ws, min_col=1, max_col=1 + len(SIZES),
                 min_row=crow + 1, max_row=crow + len(PICK))
cats = Reference(ws, min_col=2, max_col=1 + len(SIZES), min_row=crow, max_row=crow)
chart.add_data(data, titles_from_data=True, from_rows=True)
chart.set_categories(cats)
ws.add_chart(chart, "A%d" % (crow + len(PICK) + 3))

# ---------------------------------------------------------------------------
# Bands, Add-ons, Thin set, Method
# ---------------------------------------------------------------------------
ws = wb.create_sheet("Bands")
ws["A1"] = "Vendors whose per-seat price falls as the team grows"; ws["A1"].font = TITLE
ws["A2"] = ("Collected by driving each vendor's own seat selector. The model above does not "
            "apply these bands; it uses list price, which overstates cost at large team sizes "
            "for these two vendors.")
ws["A2"].font = SUB
header(ws, 4, ["Vendor","Tier","Seats","Price per seat","Annual per user","Source","Collected"],
       [16,16,10,14,15,40,11])
for i, b in enumerate(bands):
    r = i + 5
    for j, k in enumerate(["vendor","tier","seats","price_annual_usd",
                           "annual_per_user_usd","source","collected_on"], 1):
        v = b[k]
        if k in ("seats","price_annual_usd","annual_per_user_usd") and v:
            v = float(v)
        c = ws.cell(row=r, column=j, value=v if v != "" else None); c.font = CALC
        if j in (4,5): c.number_format = MONEY

ws = wb.create_sheet("Add-ons")
ws["A1"] = "Capabilities sold separately"; ws["A1"].font = TITLE
ws["A2"] = ("A yes or no column cannot hold these. Hive sells single sign-on as a per-seat "
            "add-on, which is the only published price for SSO in the whole set.")
ws["A2"].font = SUB
header(ws, 4, ["Vendor","Tier","Add-on","Price","Unit","Notes","Collected"],
       [16,14,34,10,20,46,11])
for i, a in enumerate(addons):
    r = i + 5
    for j, k in enumerate(["vendor","tier","addon","price_usd","unit","notes","collected_on"], 1):
        v = a[k]
        if k == "price_usd" and v: v = float(v)
        c = ws.cell(row=r, column=j, value=v if v != "" else None); c.font = CALC
        if j == 4: c.number_format = MONEY

ws = wb.create_sheet("Thin set")
ws["A1"] = "Price visibility across the wider category"; ws["A1"].font = TITLE
ws["A2"] = ("No prices collected here, only whether a price is published at all. "
            "Rows marked browser_verified were checked by loading the page, because a plain "
            "text fetch reports false opacity on client-rendered prices.")
ws["A2"].font = SUB
header(ws, 4, ["Vendor","Frame rank","Paid tiers","Tiers priced","Tiers contact sales",
               "Free plan","Visibility","Confidence","In category","Source","Collected"],
       [20,11,11,12,16,10,18,18,11,44,11])
for i, t in enumerate(thin):
    r = i + 5
    for j, k in enumerate(["vendor","g2_rank","paid_tiers","tiers_with_price",
                           "tiers_contact_sales","free_plan","visibility","confidence",
                           "in_category","pricing_url","collected_on"], 1):
        v = t[k]
        if k in ("g2_rank","paid_tiers","tiers_with_price","tiers_contact_sales") and v:
            v = int(v)
        ws.cell(row=r, column=j, value=v if v != "" else None).font = CALC

ws = wb.create_sheet("Method")
ws.column_dimensions["A"].width = 110
method = [
 ("Method and what is wrong with it", TITLE),
 ("", None),
 ("THE SAMPLE", Font(name=ARIAL, size=11, bold=True)),
 ("Vendors were taken from the union of two public category listings, project management and "
  "task management, read on 2 October 2026 and ordered by review count. The listings' own page "
  "order was not used because it is influenced by sponsorship. The walk down that list and the "
  "reason for every vendor passed over is recorded in the project's frame file.", CALC),
 ("The first fifteen general-purpose work trackers publishing prices in US dollars form the "
  "deep set. Airtable was passed over as a database product, Quickbase as an application "
  "platform, and Adobe Workfront because it publishes no price at all.", CALC),
 ("", None),
 ("THREE WAYS THIS DATA CAN BE WRONG, ALL OF WHICH BIT DURING COLLECTION", Font(name=ARIAL, size=11, bold=True)),
 ("1. Pricing pages render both the monthly and the annual price into the page and hide one. "
  "Any plain text extraction concatenates them. Smartsheet Pro read as $129 a seat; it is $12 "
  "monthly and $9 annual. Every price here was therefore read from the rendered page.", CALC),
 ("2. The same extraction reports no price at all when prices are drawn by client-side script. "
  "Todoist came back as having no published prices. It publishes them. That error inflates any "
  "measure of price opacity, which is the thing being measured, so every dark result was "
  "re-checked in a browser.", CALC),
 ("3. A capability can be missing from a pricing page without being missing from the product. "
  "This workbook treats a capability the page does not claim as absent, which is correct for a "
  "buyer and unkind to vendors with vague pages.", CALC),
 ("", None),
 ("WHAT IS NOT IN HERE", Font(name=ARIAL, size=11, bold=True)),
 ("Negotiated pricing, nonprofit and education rates, currencies other than US dollars, and "
  "any tier whose price is only available through a sales conversation.", CALC),
 ("Volume banding is recorded for the two vendors that expose a seat selector, and is not "
  "applied in the model. For those two the model overstates cost at large team sizes.", CALC),
 ("Ten of the thirteen capabilities originally scoped were not collected to completion. Single "
  "sign-on and audit log were, because they are the two that decide the result.", CALC),
 ("", None),
 ("Collected 2 October 2026. Software pricing moves quarterly.", SUB),
]
r = 1
for text, font in method:
    c = ws.cell(row=r, column=1, value=text)
    if font: c.font = font
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 1

wb.save(OUT)
print("wrote", OUT)
print("%d tiers, %d vendors" % (N, len(vendors)))
