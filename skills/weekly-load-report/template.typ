// Weekly training-load report template for Northfield FC
// Expects report_data.json alongside this file.

#let data = json("report_data.json")

#let nf-navy = rgb("#0a2540")
#let nf-amber = rgb("#d98b00")
#let nf-red = rgb("#b23a3a")
#let nf-muted = rgb("#6b7280")

#set page(
  paper: "a4",
  margin: (x: 1.8cm, y: 1.8cm),
  header: [
    #set text(size: 9pt, fill: nf-muted)
    Northfield FC · Performance Analytics · Squad #data.squad
    #h(1fr)
    #data.week_label
  ],
  footer: [
    #set text(size: 8pt, fill: nf-muted)
    Generated #data.generated_at
    #h(1fr)
    Synthetic data — teaching use only
  ],
)

#set text(font: "Liberation Sans", size: 10pt)

// Masthead
#block(
  fill: nf-navy,
  inset: (x: 14pt, y: 10pt),
  radius: 4pt,
  width: 100%,
)[
  #set text(fill: white)
  #text(size: 16pt, weight: "bold")[Weekly Training Load]
  #h(1fr)
  #text(size: 11pt)[#data.squad · #data.week_label]
]

#v(10pt)

// Summary paragraph
#block(
  fill: luma(245),
  inset: 12pt,
  radius: 3pt,
  width: 100%,
)[
  #set par(justify: true, leading: 0.8em)
  #data.summary_paragraph
]

#v(8pt)

// Player table
#let flag-colour(flag) = if flag == "red" {
  nf-red
} else if flag == "amber" {
  nf-amber
} else {
  none
}

#let header-cell(label) = [
  #set text(weight: "bold", size: 9pt, fill: white)
  #label
]

#let cell(content, flag: "none") = {
  let c = flag-colour(flag)
  if c == none {
    [#content]
  } else {
    text(fill: c, weight: "bold")[#content]
  }
}

#table(
  columns: (1fr, 0.7fr, 0.6fr, 1fr, 1fr, 1fr, 1fr),
  align: (left, center, center, right, right, right, right),
  stroke: (x, y) => if y == 0 { (bottom: 1pt + nf-navy) } else { (bottom: 0.3pt + luma(220)) },
  fill: (x, y) => if y == 0 { nf-navy } else { none },
  header-cell[Player],
  header-cell[Pos],
  header-cell[Sess],
  header-cell[Total (km)],
  header-cell[HSR (m)],
  header-cell[Sprint (m)],
  header-cell[Δ vs prev],
  ..data.rows.map(r => (
    [#r.player_id],
    [#r.position],
    [#r.sessions],
    cell(r.total_distance_km, flag: r.flag),
    cell(r.hsr_m, flag: r.flag),
    cell(r.sprint_m, flag: r.flag),
    cell(
      if r.delta_pct == none { "–" } else { str(r.delta_pct) + "%" },
      flag: r.flag,
    ),
  )).flatten()
)

#v(14pt)

// Legend
#block[
  #set text(size: 8pt, fill: nf-muted)
  #text(fill: nf-red, weight: "bold")[■] red = ±>20% change from last week ·
  #text(fill: nf-amber, weight: "bold")[■] amber = 15–20% change ·
  uncoloured = within ±15%
]
