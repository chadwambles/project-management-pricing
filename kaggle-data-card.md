# Kaggle upload sheet

Everything below is copy and paste. The sections match the fields Kaggle asks
for, in the order it asks for them.

---

## Title

```
Project Management Software Pricing, October 2026
```

## Subtitle

```
62 pricing tiers from 15 vendors, read from their own pricing pages on 2 October 2026
```

## Description (the Data Card)

```
**Collected 2 October 2026. Software pricing moves quarterly, so treat this as
a snapshot and not a feed.** Several of these vendors have almost certainly
changed a price, renamed a tier or moved a feature between tiers since. Every
row carries its own `collected_on` date and the source URL it was read from, so
you can check any single figure against the live page rather than trusting the
file.

What fifteen project management tools charge, with the tier structure, seat
caps, seat minimums and capability gates that decide which tier a team actually
lands on.

## The finding

There is no cheapest vendor. Below six seats it is Zoho Projects at $4 a seat.
From six up it is Basecamp, whose flat pricing never loses again: at a hundred
people its $59 Studio plan works out to 49 cents a seat.

Then you require one thing and the ranking inverts.

| what you require | cheapest at 100 seats | per seat | vendors still standing |
|---|---|---|---|
| nothing | Basecamp Studio | $0.49 | 14 of 15 |
| a Gantt or timeline view | Zoho Projects Premium | $4.00 | 11 |
| SAML single sign-on | Zoho Projects Enterprise | $9.00 | 5 |
| single sign-on and an audit log | Runrun.it Enterprise | $26.00 | 1 |

Requiring a timeline view costs eight times as much. Requiring single sign-on
costs eighteen times as much and removes ten of the fifteen vendors. Exactly
one priced tier out of sixty-two lists both single sign-on and an audit log.

So the thing forcing a team onto a tier is usually not headcount. It is a
security checkbox, and crossing it ejects you from the published-price part of
the market.

The sharpest version is a seat minimum rather than a seat price. A five-person
team that needs single sign-on pays Trello $875 a month, because Trello
Enterprise is the cheapest priced tier carrying SSO and it has a fifty-seat
minimum. Five people buy fifty seats.

## Files

| file | rows | what it holds |
|---|---|---|
| `tiers.csv` | 62 | one row per paid tier: prices on both cadences, seat caps, seat minimums, pricing model |
| `gates.csv` | 62 | thirteen capabilities per tier, as `yes`, `no` or `not_stated` |
| `frame.csv` | 50 | the sampling walk, with a recorded reason for every vendor passed over |
| `volume_bands.csv` | 10 | per-seat price against seat count, for the two vendors that expose a seat selector |
| `addons.csv` | 3 | capabilities sold separately rather than included in a tier |
| `thin_set.csv` | 18 | price visibility across the wider category, without full tier detail |

`project-management-pricing-2026-10.xlsx` is a model built on these files with
1,264 live formulas. Enter a team size, a billing cadence and a set of required
capabilities, and it returns the qualifying tier per vendor and a reason for
every vendor it ruled out.

## How the prices were read, and three ways this went wrong

Plain text extraction of a pricing page fails in three distinct ways, and all
three happened here before being caught.

**Concatenated prices.** Pricing pages render both the monthly and the annual
price into the page and hide one with a toggle, so text extraction returns them
joined. Smartsheet Pro read as `$129 per Member/month`. It is $12 monthly and
$9 annual. The giveaway was the other currencies, `$1713 AUD` and `$1612 CAD`.
Every price here was read from the rendered page instead.

**Invented opacity.** The same extraction reports no price at all when prices
are drawn by client-side script. Todoist came back as publishing nothing. It
publishes everything. That error inflates exactly the thing this dataset
measures, so every vendor that looked like contact-sales was re-checked in a
browser before being recorded that way.

**Silence read as absence.** A capability missing from a pricing page is not
necessarily missing from the product. This dataset treats an unclaimed
capability as absent, which is the right default for a buyer and unkind to
vendors with vague pages. That is why `not_stated` is a distinct value from
`no` in `gates.csv`. Only Teamwork.com explicitly says "Not included".

## The sample

Vendors come from the union of two public category listings, project management
and task management, read on 2 October 2026 and re-ordered by review count. The
listings' own page order was not used, because it is influenced by sponsorship:
vendors reappear as "Sponsored" on later pages.

The first fifteen general-purpose work trackers publishing prices in US dollars
form the deep set. `frame.csv` records the whole walk. Airtable is excluded as
a database product priced on records, Quickbase as an application platform,
Adobe Workfront for publishing no price at all.

## Limitations

Ten of the thirteen capabilities are incomplete. Single sign-on and audit log
were collected to completion because they decide the result. The rest are
recorded where a pricing page happened to state them.

Volume banding is recorded but not applied, so the model overstates Trello and
Jira at large team sizes.

Free tiers are excluded from the paid comparison, though `is_free` marks them.

No negotiated pricing, no nonprofit or education rates, US dollars only.
Microsoft Planner is absent because its pricing lives inside Microsoft 365
licensing and has no stable standalone page, which is its own small finding
about comparability.

## Code

The build script and the full write-up are on GitHub:
https://github.com/chadwambles/project-management-pricing
```

---

## Tags

```
business, software, pricing, saas, excel, data-analysis, business-analytics
```

## Provenance / Sources

```
Vendor pricing pages, read 2 October 2026:
smartsheet.com/pricing, monday.com/pricing, clickup.com/pricing,
trello.com/pricing, asana.com/pricing, notion.com/pricing,
atlassian.com/software/jira/pricing, basecamp.com/pricing, wrike.com/price,
runrun.it/en-US/plans-and-prices, teamwork.com/pricing,
teamgantt.com/pricing, hive.com/pricing, ganttpro.com/pricing,
zoho.com/projects/pricing.html

Sampling frame, read 2 October 2026:
g2.com/categories/project-management
g2.com/categories/task-management
```

## License

```
CC0: Public Domain
```

Published prices are factual observations, not creative work, so there is
nothing here to reserve. CC0 also means nobody has to ask before rebuilding
the comparison with fresher numbers, which is the useful thing to do with a
dated snapshot.

---

## File descriptions

Paste each into the file's description box after upload.

**tiers.csv**
```
One row per paid tier, 62 rows across 15 vendors. Prices on both billing
cadences where published, plus the seat cap, seat minimum and pricing model
that decide whether a team of a given size can buy the tier at all. Blank price
means no published price. Free tiers are marked and excluded from the paid
comparison.
```

**gates.csv**
```
Thirteen capabilities per tier, keyed to tiers.csv by vendor and tier. Values
are yes, no or not_stated. not_stated is deliberately distinct from no: it
means the pricing page did not mention the capability, which is not proof the
product lacks it. Only Teamwork.com explicitly states an exclusion. saml_sso
and audit_log are complete; the other eleven are recorded where a page stated
them.
```

**frame.csv**
```
The sampling walk. Fifty vendors from the union of two category listings,
re-ordered by review count rather than page order, with a recorded decision for
each: deep set, or thin set with the reason it was passed over. This is the file
that makes the sample auditable rather than asserted.
```

**volume_bands.csv**
```
Per-seat price against seat count for the two vendors that expose a seat
selector, Trello and Jira. Both reduce the per-seat price substantially as the
team grows. The workbook records these and does not apply them, so it
overstates both at large team sizes.
```

**addons.csv**
```
Capabilities sold separately rather than included in a tier. Small file, but it
is the mechanism by which an advertised tier price understates the real cost of
a requirement.
```

**thin_set.csv**
```
Price visibility across the wider category without full tier detail: how many
paid tiers each vendor has, how many carry a published price, and how many say
contact sales. This is the file behind the finding that total pricing blackout
is rare and selective opacity is the norm.
```

---

## Column descriptions

Optional on Kaggle, and tedious to enter by hand. The ones genuinely worth the
typing are the columns a reader would otherwise guess wrong about.

| file | column | description |
|---|---|---|
| tiers | `pricing_model` | `per_seat`, `flat` or `per_project`. Determines which price columns are populated. |
| tiers | `price_annual_usd` | Per seat per month when billed annually. Blank means not published on that cadence. |
| tiers | `flat_annual_usd` | Whole-tier monthly price when billed annually, for flat-priced tiers. Independent of headcount. |
| tiers | `min_seats` | Seat minimum. A team smaller than this still pays for this many. |
| tiers | `max_seats` | Seat cap, blank where none. |
| tiers | `is_free` | `yes` marks a free tier, excluded from the paid comparison. |
| tiers | `price_visible` | `yes` if a price is published, `no` if the tier says contact sales. |
| gates | `not_stated` (value) | The page did not mention the capability. Not the same as `no`. |
| gates | `automation_cap_month` | Stated monthly automation run limit, not a yes/no. |
| frame | `set` | `deep` for the 15 fully collected vendors, `thin` for the rest. |
| frame | `exclusion_reason` | Why a vendor was not in the deep set. Blank for deep-set vendors. |
| frame | `g2_categories` | `PM`, `TM` or both, naming which listing the vendor appeared on. |
| thin_set | `visibility` | Summary of how much of the tier ladder carries a published price. |
| thin_set | `confidence` | How certain the visibility reading is, given client-rendered pages. |
| thin_set | `in_category` | Whether the vendor is a general-purpose work tracker by this project's rule. |
| all files | `collected_on` | The date that row was read. |
| all files | `pricing_url` / `source_url` | The page that row was read from. |
