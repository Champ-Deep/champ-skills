# Emoji to Icon Map

The fastest, highest-impact polish move is replacing emojis with a real icon family. This file maps the emojis AI reaches for to the exact icon names in **Lucide** and **Phosphor**, plus how to import them.

## The one-family rule

Pick **one** library per product and use it everywhere.
- **Lucide**: clean, even line set. The safe default for most SaaS and dashboards.
- **Phosphor**: multiple weights (thin, regular, bold, fill, duotone). Reach for it when you want expressive range.

Then lock the metrics:
- One base size in the chrome (commonly 16, 18, or 20px). Do not mix sizes within a row.
- One stroke weight (Lucide `strokeWidth` around 1.75, Phosphor `weight="regular"`).
- Let icons inherit `currentColor` so they pick up text color and states for free.
- Use icons semantically. If removing it loses no meaning, it was decoration. Remove it.

## Lookup table

| Emoji | Meaning | Lucide | Phosphor |
|-------|---------|--------|----------|
| link, chain | link | `link-2` | `Link` |
| bar chart | analytics | `bar-chart-3` | `ChartBar` |
| chart up | trend up | `trending-up` | `TrendUp` |
| chart down | trend down | `trending-down` | `TrendDown` |
| globe | domain, global | `globe` | `Globe` |
| gear | settings | `settings` | `Gear` |
| person | user, account | `user` | `User` |
| people | team | `users` | `UsersThree` |
| credit card | billing | `credit-card` | `CreditCard` |
| receipt | invoice | `receipt` | `Receipt` |
| money bag | revenue | `wallet` | `Wallet` |
| bell | notifications | `bell` | `Bell` |
| folder | group, project | `folder` | `Folder` |
| pencil | edit | `pencil` | `PencilSimple` |
| wastebasket | delete | `trash-2` | `Trash` |
| plus | create, add | `plus` | `Plus` |
| check | success, done | `check` | `Check` |
| check mark button | confirmed | `check-circle-2` | `CheckCircle` |
| cross mark | error, remove | `x` | `X` |
| star | favorite, featured | `star` | `Star` |
| house | home | `home` | `House` |
| calendar | date | `calendar` | `CalendarBlank` |
| magnifying glass | search | `search` | `MagnifyingGlass` |
| clock, alarm | time, expiry | `clock` | `Clock` |
| pin | location | `map-pin` | `MapPin` |
| rocket | launch, upgrade | `rocket` | `Rocket` |
| lightbulb | tips, ideas | `lightbulb` | `Lightbulb` |
| lock | secure, private | `lock` | `Lock` |
| open lock | public | `unlock` | `LockOpen` |
| key | API key, auth | `key` | `Key` |
| shield | protection | `shield-check` | `ShieldCheck` |
| envelope | email | `mail` | `Envelope` |
| phone | call | `phone` | `Phone` |
| mobile | device, mobile | `smartphone` | `DeviceMobile` |
| laptop | desktop | `monitor` | `Laptop` |
| clipboard | copy | `clipboard` | `Clipboard` |
| outbox, share | share | `share-2` | `ShareNetwork` |
| down arrow | download | `download` | `DownloadSimple` |
| up arrow | upload | `upload` | `UploadSimple` |
| recycle, arrows | refresh, sync | `refresh-cw` | `ArrowsClockwise` |
| eye | views, preview | `eye` | `Eye` |
| speech bubble | comments | `message-circle` | `ChatCircle` |
| lightning | fast, automation | `zap` | `Lightning` |
| target | goals, conversions | `target` | `Target` |
| label, tag | tags | `tag` | `Tag` |
| package | product, release | `package` | `Package` |
| info | information | `info` | `Info` |
| warning | warning | `alert-triangle` | `Warning` |
| question | help | `help-circle` | `Question` |
| fire | trending, hot | `flame` | `Flame` |
| three dots | more actions | `more-horizontal` | `DotsThree` |
| three dots vertical | row menu (kebab) | `more-vertical` | `DotsThreeVertical` |

If you need an emoji not listed here, search the library site for the closest concept. There is almost always a clean equivalent.

## Import snippets

### Lucide, React
```jsx
import { Link2, BarChart3, Settings, User } from "lucide-react";

<Link2 size={18} strokeWidth={1.75} />
<BarChart3 size={18} strokeWidth={1.75} />
```

### Lucide, vanilla HTML (CDN)
```html
<script src="https://unpkg.com/lucide@latest"></script>

<i data-lucide="link-2"></i>
<i data-lucide="bar-chart-3"></i>

<script>lucide.createIcons();</script>
```
Style the rendered SVG with `width`, `height`, `stroke-width`, and `color` on the `[data-lucide]` element or its parent.

### Phosphor, React
```jsx
import { Link, ChartBar, Gear, User } from "@phosphor-icons/react";

<Link size={18} weight="regular" />
<ChartBar size={18} weight="regular" />
```

### Phosphor, vanilla HTML (CDN)
```html
<script src="https://unpkg.com/@phosphor-icons/web"></script>

<i class="ph ph-link"></i>
<i class="ph ph-chart-bar"></i>
```
Switch weights with the class prefix: `ph` (regular), `ph-bold`, `ph-fill`, `ph-duotone`, `ph-thin`.

## Do not
- Mix Lucide and Phosphor in the same product.
- Use fill and line icons together in the same toolbar.
- Keep a single emoji "because it is fun." It breaks the family and re-introduces the tell.
