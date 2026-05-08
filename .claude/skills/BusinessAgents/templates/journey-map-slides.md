# User Impact Journey Map — Slide Structures

Use the `templates/slides-base.html` template as the HTML wrapper. Build one slide per simulated situation, plus a title slide and a summary slide.

## Title Slide

```html
<section class="active">
  <div class="label">End User Impact</div>
  <h1>How [Solution Name] Changes Your Day</h1>
  <p>For [persona role] in [industry] — [N] situations simulated</p>
</section>
```

## Situation Slide (one per simulated situation)

```html
<section>
  <div class="label">Situation [N]</div>
  <h2>[Situation Name]</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;margin-top:1rem">
    <div>
      <div class="label" style="color:#ef4444">Before</div>
      <ul>
        <li>[Key before step 1 — from the task-level drill or journey phase]</li>
        <li>[Key before step 2]</li>
        <li>[Key before step 3]</li>
      </ul>
    </div>
    <div>
      <div class="label" style="color:#22c55e">After</div>
      <ul>
        <li>[Key after step 1]</li>
        <li>&#10003; [Eliminated step — mark with checkmark]</li>
        <li>[Key after step 3]</li>
      </ul>
    </div>
  </div>
  <p style="margin-top:1.5rem;color:#3b82f6">&#9201; [Time saved estimate] &nbsp;|&nbsp; &#10007; [Error reduction] &nbsp;|&nbsp; &#9733; [Quality note]</p>
</section>
```

## Summary Slide (last)

```html
<section>
  <div class="label">Summary</div>
  <h2>Key Benefits</h2>
  <p class="big">~[X] hrs/week saved</p>
  <ul>
    <li>[Top benefit 1 — from simulation cross-situation summary]</li>
    <li>[Top benefit 2]</li>
    <li>[Top benefit 3]</li>
  </ul>
  <p style="margin-top:2rem;color:#64748b">[Call to action — from the one-pager closing line if available, otherwise generate one]</p>
</section>
```

## Data Source

Read the most recent file matching `outputs/ideas/<working-slug>/simulation-*-<YYYY-MM-DD>.md` (by date — do NOT read the onepager file, which contains `-onepager-` in the name). If no simulation report exists, tell the founder to run `/BusinessAgents:simulate_user` first.
