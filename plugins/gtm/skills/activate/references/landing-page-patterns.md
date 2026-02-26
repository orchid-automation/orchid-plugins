# Landing Page Patterns

Vendored reference for the `/gtm:activate` skill. Use these patterns when generating `landing-page.html`. If the `/frontend-design` ecosystem skill is available, prefer it for visual polish.

---

## Table of Contents

- [Hero Section Patterns](#hero-section-patterns)
- [Feature Section Layouts](#feature-section-layouts)
- [Social Proof Patterns](#social-proof-patterns)
- [CTA Patterns and Placement](#cta-patterns-and-placement)
- [FAQ Section from Objection Map](#faq-section-from-objection-map)
- [Mobile-First Considerations](#mobile-first-considerations)
- [Page Structure Template](#page-structure-template)

---

## Hero Section Patterns

The hero is the first thing visitors see. Pick ONE pattern based on product positioning.

### Pattern 1: Problem-Agitate

Lead with the pain. Works when the ICP has a well-known, expensive problem.

```
[Headline: State the problem they're sick of]
[Subheadline: Agitate -- what it costs them]
[CTA button: The escape]
```

**Example:**
```html
<h1>Still stitching together 6 tools to run outbound?</h1>
<p>Your team wastes 11 hours/week on manual data entry between your CRM,
   email tool, and spreadsheets. That's $47K/year in lost productivity.</p>
<a href="#pricing">Replace the stack -- start free</a>
```

### Pattern 2: Transformation

Lead with the outcome. Works when the benefit is aspirational or hard to quantify.

```
[Headline: The after-state they want]
[Subheadline: How the product gets them there]
[CTA button: Start the transformation]
```

**Example:**
```html
<h1>Go from code commit to market-ready in one afternoon</h1>
<p>The GTM engine scans your codebase, researches your market, builds positioning,
   and generates landing pages, email sequences, and sales collateral -- automatically.</p>
<a href="#demo">See it in action</a>
```

### Pattern 3: Social Proof Lead

Lead with credibility. Works when you have strong numbers or recognizable customers.

```
[Headline: Impressive metric or customer proof]
[Subheadline: What the product does]
[CTA button: Join them]
```

**Example:**
```html
<h1>2,400 teams ship their GTM in under 4 hours</h1>
<p>From codebase scan to landing page, email sequences, and ABM lists.
   One command. No marketing team required.</p>
<a href="#signup">Join them -- free to start</a>
```

---

## Feature Section Layouts

### Layout 1: Outcome Grid

3 or 4 cards in a row. Each card = one buyer outcome (not a feature spec).

```html
<section class="grid grid-cols-1 md:grid-cols-3 gap-8 py-16 px-4 max-w-6xl mx-auto">
  <div class="text-center p-6">
    <div class="text-4xl mb-4"><!-- emoji or SVG icon --></div>
    <h3 class="text-xl font-bold mb-2">[Outcome headline]</h3>
    <p class="text-gray-600">[How the feature delivers this outcome. 1-2 sentences.]</p>
  </div>
  <!-- repeat for each feature -->
</section>
```

**Rule:** Max 4 cards. Each headline is a result ("Cut onboarding from 2 weeks to 2 hours"), not a feature name ("Advanced Onboarding Module").

### Layout 2: Alternating Rows

Feature + screenshot/visual, alternating left-right. Works for products with strong UI.

```html
<section class="py-16 px-4 max-w-6xl mx-auto">
  <div class="flex flex-col md:flex-row items-center gap-12 mb-16">
    <div class="md:w-1/2">
      <h3 class="text-2xl font-bold mb-4">[Outcome headline]</h3>
      <p class="text-gray-600 mb-4">[Description]</p>
      <ul class="space-y-2 text-gray-600">
        <li>[Specific proof point]</li>
        <li>[Specific proof point]</li>
      </ul>
    </div>
    <div class="md:w-1/2">
      <!-- visual placeholder: code block, screenshot, or diagram -->
    </div>
  </div>
  <!-- second row: reversed order with md:flex-row-reverse -->
</section>
```

### Layout 3: Comparison Table

Us vs. the alternative (manual process, competitor, or status quo). Works for replacement products.

```html
<section class="py-16 px-4 max-w-4xl mx-auto">
  <h2 class="text-3xl font-bold text-center mb-12">Before vs. After</h2>
  <div class="grid grid-cols-2 gap-0">
    <div class="bg-red-50 p-8 rounded-l-xl">
      <h3 class="font-bold text-red-800 mb-4">Without [Product]</h3>
      <ul class="space-y-3 text-red-700">
        <li>[Pain point 1]</li>
        <li>[Pain point 2]</li>
        <li>[Pain point 3]</li>
      </ul>
    </div>
    <div class="bg-green-50 p-8 rounded-r-xl">
      <h3 class="font-bold text-green-800 mb-4">With [Product]</h3>
      <ul class="space-y-3 text-green-700">
        <li>[Outcome 1]</li>
        <li>[Outcome 2]</li>
        <li>[Outcome 3]</li>
      </ul>
    </div>
  </div>
</section>
```

---

## Social Proof Patterns

### Metrics Bar

A row of 3-4 key numbers. Place below the hero or between feature sections.

```html
<section class="bg-gray-50 py-12">
  <div class="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
    <div>
      <div class="text-3xl font-bold text-blue-600">[Number]</div>
      <div class="text-gray-600 text-sm">[What it measures]</div>
    </div>
    <!-- repeat -->
  </div>
</section>
```

**Number sources from upstream files:**
- Total capabilities from 01-scan.md (e.g., "87 features mapped")
- Integration count from 01-scan.md (e.g., "12 integrations")
- Cost comparison from 03-position.md (e.g., "10x cheaper than building in-house")
- Time savings (e.g., "4 hours vs. 4 weeks")

### Testimonial Cards

If testimonials exist in upstream data, use this layout. Otherwise skip -- do not fabricate quotes.

```html
<div class="bg-white rounded-xl shadow p-6">
  <p class="text-gray-700 mb-4">"[Exact quote]"</p>
  <div class="flex items-center gap-3">
    <div class="w-10 h-10 bg-gray-300 rounded-full"></div>
    <div>
      <div class="font-bold text-sm">[Name]</div>
      <div class="text-gray-500 text-xs">[Title, Company]</div>
    </div>
  </div>
</div>
```

### Logo Bar

A row of company/integration logos. Use text names if actual logos are unavailable.

```html
<section class="py-8 border-y border-gray-100">
  <p class="text-center text-gray-400 text-sm mb-6">Integrates with</p>
  <div class="flex justify-center items-center gap-8 flex-wrap opacity-60">
    <span class="text-lg font-semibold text-gray-400">[Company/Tool]</span>
    <!-- repeat -->
  </div>
</section>
```

---

## CTA Patterns and Placement

### CTA Button Styles

**Primary (high contrast):**
```html
<a href="#" class="inline-block bg-blue-600 text-white font-bold py-3 px-8 rounded-lg
   hover:bg-blue-700 transition">
  [Action verb] + [Outcome] -- [Risk reducer]
</a>
```

**Examples of strong CTAs:**
- "Start free -- no credit card"
- "See the demo (2 min)"
- "Get your GTM package"
- "Try it on your codebase"

**Weak CTAs to avoid:**
- "Learn more"
- "Get started"
- "Submit"
- "Click here"

### Placement Rules

1. **Hero**: Primary CTA. Most important. Above the fold.
2. **After features**: Secondary CTA. Reinforces after they understand the value.
3. **After pricing**: Primary CTA again. They've seen the price, now commit.
4. **Footer**: Final CTA. Catches scrollers who read everything.

**Sticky nav CTA** (optional):
```html
<nav class="fixed top-0 w-full bg-white/90 backdrop-blur z-50 border-b">
  <div class="max-w-6xl mx-auto flex justify-between items-center py-3 px-4">
    <span class="font-bold">[Product]</span>
    <a href="#pricing" class="bg-blue-600 text-white text-sm font-bold py-2 px-4 rounded-lg">
      [CTA]
    </a>
  </div>
</nav>
```

---

## FAQ Section from Objection Map

Convert every objection from 03-position.md's objection map into a Q&A pair.

### Conversion pattern

| Objection Map | FAQ |
|--------------|-----|
| Objection: "It's too expensive" | Q: "How does pricing compare to [competitor]?" |
| Response: "We're 60% less..." | A: "We're 60% less than [competitor] because..." |
| Proof: "$X vs $Y" | A (cont.): "For example, [proof point]" |

### HTML pattern

```html
<section class="py-16 px-4 max-w-3xl mx-auto">
  <h2 class="text-3xl font-bold text-center mb-12">Frequently Asked Questions</h2>
  <div class="space-y-6">
    <details class="border-b pb-4">
      <summary class="font-bold cursor-pointer py-2">[Question]</summary>
      <p class="text-gray-600 mt-2">[Answer with proof point]</p>
    </details>
    <!-- repeat -->
  </div>
</section>
```

**Rules:**
- Minimum 5 FAQs, maximum 10
- Every FAQ maps to a real objection from 03-position.md
- Never invent FAQs that aren't grounded in the objection map
- Order from most common objection to least common

---

## Mobile-First Considerations

### Layout rules

- All grids collapse to single column on mobile (`grid-cols-1 md:grid-cols-3`)
- Hero text is centered on mobile, left-aligned on desktop
- CTA buttons are full-width on mobile (`w-full md:w-auto`)
- Padding: `px-4` on mobile, `px-0` on desktop (use `max-w-*` containers)
- Font sizes: hero headline `text-3xl md:text-5xl`, body `text-base`
- Images and visuals stack below text on mobile

### Accessibility

- All interactive elements have hover/focus states
- Color contrast: text on colored backgrounds must pass WCAG AA (4.5:1 ratio)
- Use semantic HTML: `<nav>`, `<main>`, `<section>`, `<footer>`
- CTA buttons are `<a>` or `<button>`, never `<div>` with click handlers
- FAQ uses `<details>/<summary>` for native expand/collapse (no JavaScript needed)
- Skip link at top: `<a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>`

### Performance

- No custom fonts (use `font-family: system-ui, -apple-system, sans-serif`)
- No images unless absolutely necessary (use emoji or inline SVG for icons)
- Single CDN dependency (Tailwind) -- no other external resources
- Total HTML file should be under 500 lines

---

## Page Structure Template

Full page skeleton for reference:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Product] -- [One-liner value prop]</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>html { scroll-behavior: smooth; }</style>
</head>
<body class="bg-white text-gray-900">

  <!-- Skip link -->
  <a href="#main" class="sr-only focus:not-sr-only">Skip to content</a>

  <!-- Nav -->
  <nav>...</nav>

  <main id="main">
    <!-- Hero -->
    <section>...</section>

    <!-- Social proof metrics bar -->
    <section>...</section>

    <!-- Features (3-4 outcomes) -->
    <section>...</section>

    <!-- Before/After or Comparison -->
    <section>...</section>

    <!-- Pricing -->
    <section id="pricing">...</section>

    <!-- FAQ from objection map -->
    <section>...</section>

    <!-- Final CTA -->
    <section>...</section>
  </main>

  <!-- Footer -->
  <footer class="bg-gray-50 py-8 text-center text-gray-500 text-sm">
    <p>[Product] -- [tagline]</p>
  </footer>

</body>
</html>
```
