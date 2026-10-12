# Project management software pricing

What fifteen project management tools charge, and a model that works out which
tier you actually land on once you say how big your team is and what it needs
to do.

Collected 2 October 2026 from vendors' own pricing pages. Software pricing
moves quarterly, so this is a snapshot, not a feed. Every row carries its own
`collected_on` date and source URL.

## The finding

**There is no cheapest vendor.** Below six seats it is Zoho Projects at $4 a
seat. From six up it is Basecamp, whose flat pricing never loses again: at a
hundred people its $59 Studio plan is 49 cents a seat.

Then you require one thing and the ranking inverts.

| what you require | cheapest at 100 seats | per seat | vendors still standing |
|---|---|---|---|
| nothing | Basecamp Studio | $0.49 | 14 of 15 |
| a Gantt or timeline view | Zoho Projects Premium | $4.00 | 11 |
| SAML single sign-on | Zoho Projects Enterprise | $9.00 | 5 |
| single sign-on and an audit log | Runrun.it Enterprise | $26.00 | 1 |

Requiring a timeline view costs eight times as much. Requiring single sign-on
costs eighteen times as much and removes ten of the fifteen vendors. Exactly
one priced tier in the entire set, out of sixty-two, lists both single sign-on
and an audit log.

**So the thing forcing you onto a tier is usually not headcount.** It is a
security checkbox, and crossing it ejects you from the published-price part of
the market.

The sharpest version of that is a seat minimum rather than a seat price. A
five-person team that needs single sign-on pays Trello **$875 a month**,
because Trello Enterprise is the cheapest priced tier carrying SSO at scale and
it has a fifty-seat minimum. Five people buy fifty seats.

## Where prices are published, and where they are not

Across thirty in-category vendors:

| | vendors | share |
|---|---|---|
| every tier priced | 13 | 43% |
| top tier hidden | 15 | 50% |
| no tier priced at all | 2 | 7% |

Total blackout is rare. Only Adobe Workfront and Lytho publish nothing.
**Selective opacity is the norm**, and it is selective in a consistent
direction: the hidden tier is usually the one where single sign-on lives.

Four vendors never name single sign-on anywhere on their pricing page, so a
buyer cannot tell whether it exists at any price: monday.com, Jira, Basecamp
and TeamGantt.

## Three pricing models, not one

Fifty-four of sixty-two tier rows price per seat. Basecamp and ProofHub charge
a flat fee regardless of headcount. TeamGantt charges by project, $120 a month
for five projects and $24 for each one after.

The unit a buyer wants to compare in does not exist for several of these
vendors, which is why the workbook reports a blank rather than a number where a
per-seat comparison would be meaningless.

## Volume banding

Two vendors expose a seat selector and both reduce the per-seat price
substantially as the team grows. Trello Enterprise runs from $17.50 a seat at
fifty users down to $7.70 at 4,405. Jira is flat to a hundred users and then
drops. The workbook records these in `data/volume_bands.csv` and does **not**
apply them, so it overstates both at large team sizes.

## The sample

Vendors come from the union of two public category listings, project management
and task management, read on 2 October 2026 and ordered by review count. The
listings' own page order was not used because it is influenced by sponsorship:
vendors reappear as "Sponsored" on later pages.

The first fifteen general-purpose work trackers publishing prices in US dollars
form the deep set. `data/frame.csv` records the whole walk, including a reason
for every vendor passed over. Airtable is excluded as a database product priced
on records, Quickbase as an application platform, Adobe Workfront for
publishing no price at all.

## Three ways this data can be wrong, all of which happened

**Concatenated prices.** Pricing pages render both the monthly and the annual
price into the page and hide one with a toggle. Any plain text extraction
returns them joined. Smartsheet Pro read as `$129 per Member/month`. It is $12
monthly and $9 annual. The giveaway was the other currencies: `$1713 AUD` and
`$1612 CAD`. Every price here was read from the rendered page instead.

**Invented opacity.** The same extraction reports no price at all when prices
are drawn by client-side script. Todoist came back as having zero published
prices. It publishes them. That error inflates exactly the thing this project
measures, so every vendor that looked contact-sales was re-checked in a
browser before being recorded as such.

**Silence read as absence.** A capability missing from a pricing page is not
necessarily missing from the product. This dataset treats an unclaimed
capability as absent, which is the right default for a buyer and unkind to
vendors with vague pages. It is also why `not_stated` is a distinct value from
`no` in `data/gates.csv`: only Teamwork.com explicitly says "Not included".

## Repository

```
build_workbook.py       builds the .xlsx from data/, 1,264 live formulas
project-management-pricing-2026-10.xlsx   the model
data/
  frame.csv             the 50-vendor walk, with a decision for each
  tiers.csv             62 tier rows: prices, caps, minimums, pricing model
  gates.csv             capability by tier; yes, no, or not_stated
  volume_bands.csv      per-seat price against seat count, where published
  addons.csv            capabilities sold separately rather than included
  thin_set.csv          price visibility across the wider category
```

Rebuild:

```
py build_workbook.py
```

Needs `openpyxl`. Nothing else.

## Limitations

**Ten of thirteen scoped capabilities are incomplete.** Single sign-on and
audit log were collected to completion because they decide the result.
The rest are recorded where a pricing page happened to state them.

**The thin set is eighteen vendors, not the full thirty-five.** The remainder
are mostly sub-hundred-review tools and adjacent products, whiteboards and time
trackers, that the category rule excludes anyway.

**Microsoft Planner has no stable public pricing page.** Its pricing lives
inside Microsoft 365 licensing, which is its own small finding about
comparability.

**Promotional pricing is recorded but not modelled.** monday.com currently
bills AI credits as a separate mandatory line and discounts them to zero. That
is a price rise sitting in plain sight and the model does not anticipate it.

**No negotiated pricing, no nonprofit or education rates, US dollars only.**
