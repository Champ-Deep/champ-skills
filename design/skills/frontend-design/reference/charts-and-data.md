# Charts & Data Visualization

## Chart Selection Framework

Choose chart type based on the **question** the data answers, not aesthetics.

| Question Type | Chart Families |
|--------------|----------------|
| **Comparison** — how do items rank or differ? | Bar, Column, Dot Plot, Bullet |
| **Trend** — how does something change over time? | Line, Area, Step, Candlestick |
| **Distribution** — how is data spread? | Histogram, Box Plot, Violin, Density |
| **Composition** — what makes up the whole? | Pie, Donut, Stacked Bar, Treemap, Waffle |
| **Relationship** — how do two variables relate? | Scatter, Bubble, Heatmap, Correlation |
| **Part-to-whole over time** | Stacked Area, Streamgraph, Alluvial |
| **Geographic** | Choropleth, Dot Map, Hex Map |
| **Flow / Process** | Sankey, Chord, Network |

---

## The 25 Chart Types

### Comparison Charts

**1. Bar Chart (Horizontal)**
- Use when: Comparing categories with long labels, ranking items
- Best for: "Which category is largest?" with 4–20 categories
- Axis: Categories on Y, values on X
- DO: Sort by value unless order has semantic meaning
- DON'T: Use when categories have natural order (use column chart)

**2. Column Chart (Vertical)**
- Use when: Comparing categories with short labels, time-based comparisons
- Best for: Monthly/quarterly comparisons, small category counts (<12)
- Axis: Categories on X, values on Y
- DO: Start Y-axis at 0 for honest comparison
- DON'T: Use for more than 12 categories (use bar chart)

**3. Grouped Bar/Column Chart**
- Use when: Comparing multiple series across the same categories
- Best for: "How does A vs B compare across categories?"
- Limit: 2–4 groups maximum. More creates visual noise.
- DO: Use consistent color coding per group

**4. Dot Plot**
- Use when: Comparing a precise value across many categories (cleaner than bars)
- Best for: Survey results, rankings, sparse data
- DO: Sort by value. Use connecting lines for before/after comparisons.

**5. Bullet Chart**
- Use when: Showing performance vs target in a single compact element
- Best for: KPI dashboards, goal tracking
- Components: Performance bar + target marker + background bands

### Trend Charts

**6. Line Chart**
- Use when: Showing continuous data over time
- Best for: Metrics over days/weeks/months, multiple series comparison
- DO: Use direct labels on lines instead of legend when possible
- DON'T: Use for categorical (non-continuous) X axis
- DON'T: Use more than 5–6 lines (use small multiples instead)

**7. Area Chart**
- Use when: Emphasizing volume/magnitude over time, not just trend
- Best for: Revenue, user counts, where the "area" communicates quantity
- DO: Use with transparency for overlapping series
- DON'T: Use stacked area for more than 3–4 categories (illegible)

**8. Stacked Area Chart**
- Use when: Showing how parts of a total change over time
- Best for: Market share evolution, revenue by segment
- Limitation: Individual segment trends are hard to read — use stacked bar for snapshots

**9. Step Chart**
- Use when: Values change discretely, not continuously (pricing tiers, policy changes)
- Best for: Subscription pricing history, tax brackets

**10. Candlestick / OHLC**
- Use when: Financial time series (open, high, low, close)
- Best for: Stock prices, trading data
- DO: Provide hover tooltips with all four values

### Distribution Charts

**11. Histogram**
- Use when: Showing frequency distribution of a continuous variable
- Best for: Age distribution, response time distribution, score distribution
- DO: Vary bin size to show different patterns — fixed bins can mislead

**12. Box Plot (Box & Whisker)**
- Use when: Comparing distributions across groups, showing median + quartiles
- Best for: A/B test results, comparing groups
- Components: Median line, box (IQR), whiskers (1.5×IQR), outlier dots

**13. Violin Plot**
- Use when: Same as box plot but showing full distribution shape
- Best for: When distribution shape matters, not just quartiles
- DO: Include a box plot inside the violin for reference

**14. Density Plot (KDE)**
- Use when: Smooth distribution curves, overlapping distributions
- Best for: Comparing two or three overlapping distributions

**15. Scatter Plot**
- Use when: Showing relationship between two continuous variables
- Best for: Correlation, clustering, outlier detection
- DO: Add a trend line when correlation is the point
- DON'T: Use for more than ~500 points without sampling/density

### Composition Charts

**16. Pie Chart**
- Use when: Showing one or two dominant segments of a whole
- Best for: 2–4 slices maximum where one slice dominates
- DON'T: Use for more than 5 slices (use bar chart instead)
- DON'T: Use for comparing similar-sized slices (too hard to read)

**17. Donut Chart**
- Use when: Same as pie, but center space holds a key number
- Best for: Single metric dashboards (e.g., "68% complete")
- Note: Same limitations as pie chart apply

**18. Treemap**
- Use when: Showing hierarchical part-to-whole with many categories
- Best for: File system sizes, budget breakdowns, market caps
- DO: Label only cells above a minimum size

**19. Waffle Chart**
- Use when: Showing a single percentage in a more readable way than pie
- Best for: "1 in 10 users" type statistics, accessibility-friendly compositions

**20. Stacked Bar Chart**
- Use when: Showing part-to-whole across categories
- Best for: Survey response distributions, budget allocations
- Limitation: Middle segments are hard to compare — only first and last are easy to read

### Relationship & Flow Charts

**21. Bubble Chart**
- Use when: Scatter plot with a third variable encoded as bubble size
- Best for: Country comparisons (GDP vs life expectancy vs population)
- DO: Size bubbles by area, not radius

**22. Heatmap**
- Use when: Showing density or correlation in a matrix
- Best for: Calendar activity, correlation matrices, confusion matrices
- DO: Use perceptually uniform color scales (viridis, plasma)
- DON'T: Use rainbow color scales (misleading and inaccessible)

**23. Sankey Diagram**
- Use when: Showing flow quantities between states
- Best for: User flow (funnel), budget flows, energy flows
- DO: Width = quantity. Sort nodes by flow volume.

**24. Chord Diagram**
- Use when: Showing bidirectional relationships between nodes
- Best for: Trade flows, migration, relationship matrices
- Caution: Very hard to read with >8 nodes

**25. Network Graph**
- Use when: Showing connections between entities
- Best for: Social networks, dependency graphs, knowledge graphs
- Caution: Force-directed layouts are beautiful but not always readable. Use adjacency matrices for dense networks.

---

## Design Principles for Data

### Color in Data Visualization

**Sequential**: For ordered data from low to high (e.g., light to dark blue)
**Diverging**: For data with a meaningful midpoint (e.g., temperature, political lean)
**Categorical**: For distinct unordered groups — use max 7–8 distinct hues

**Never use rainbow/jet scales** — perceptually nonuniform, misleading, and inaccessible to colorblind users.

**Always test with deuteranopia simulation** — 8% of men can't distinguish red/green.

### Accessibility for Charts

- Don't rely on color alone — use patterns, direct labels, or both
- Provide data table alternative for all charts
- Chart title should state the conclusion: "Mobile users up 40% YoY" not "Mobile Users"
- Tooltips for detail-on-demand — don't over-clutter the base chart

### Responsive Chart Behavior

| Breakpoint | Adaptation |
|-----------|------------|
| < 480px | Single metric, sparkline, or simplified bar |
| 480–768px | Simplified axes, fewer data points, larger touch targets |
| > 768px | Full chart with all labels and legend |

- Simplify, don't just shrink — a full chart at 320px is unreadable
- Prefer horizontal bar charts on mobile (category labels don't truncate)
- Hide secondary gridlines on small screens

### Chart Annotations

High-impact events should be annotated directly on charts:
- Vertical reference lines for date events ("Product launch")
- Callout boxes for significant data points
- Trend line with equation when correlation is the message

### Always Include

- **Axis labels** with units ("Revenue ($M)", not "Revenue")
- **Source** for external data
- **Date range** in chart title or subtitle
- **Sample size** for survey/research data (n = 1,204)
- **Tooltip** with precise values on hover

---

**Avoid**: 3D charts (always misleading). Dual Y-axes (almost always misleading). Truncated Y-axes without reason. Starting pie charts at non-noon positions. Using gradients to add "dimension" to bars.
