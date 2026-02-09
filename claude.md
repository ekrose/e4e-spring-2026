# Economics for Everyone Course Website

This is the course website for **Economics for Everyone (Spring 2026)**, taught by John List and Evan Rose at the University of Chicago.

## Technology Stack

- **Quarto**: Static site generator that compiles `.qmd` files to HTML
- **RevealJS**: Lecture slides are rendered as reveal.js presentations
- **GitHub Pages**: Site deploys from the `/docs` directory

## Project Structure

```
e4e-spring-2026/
├── _quarto.yml          # Main Quarto configuration
├── index.qmd            # Homepage
├── schedule.qmd         # Course schedule
├── about.qmd            # About page
├── styles.css           # Custom CSS (UChicago branding)
├── e4e-logo.svg         # Course logo
├── logo.svg             # Navbar logo
├── lectures/
│   ├── index.qmd        # Lectures listing page
│   ├── *.qmd            # Individual lecture slides
│   └── images/          # Lecture images and diagrams
└── docs/                # Compiled output (do not edit directly)
```

## Creating Lectures from Notes

When given notes for a new lecture, create a `.qmd` file in `/lectures/` following this format:

### Lecture YAML Header

```yaml
---
title: "Lecture Title"
subtitle: "Economics for Everyone"
format:
  revealjs:
    theme: simple
    slide-number: true
    preview-links: auto
---
```

### Slide Formatting Conventions

**New slides**: Use `---` (three dashes) to separate slides

**Incremental reveals**: Use `. . .` (dot space dot space dot) to make content appear on click
```markdown
First point appears immediately.

. . .

This appears after a click.

. . .

This appears after another click.
```

**Section headers**: Use `#` with maroon background for major sections
```markdown
# Section Title {background-color="#800000"}

Optional subtitle text
```

**Regular slide headers**: Use `##` for standard slides
```markdown
## Slide Title

Content here...
```

**Block quotes**: Use `>` for key insights or definitions
```markdown
> **Key insight:** This is an important takeaway.
```

**Two-column layouts**:
```markdown
:::: {.columns}
::: {.column width="60%"}
Left column content
:::
::: {.column width="40%"}
Right column content
:::
::::
```

**Images**:
```markdown
![](images/filename.svg){fig-align="center" width="70%"}
```

**Speaker notes / references**: Hidden from slides but preserved in source
```markdown
::: {.notes}
Reference: Author (Year). "Title." Journal.
:::
```

### Content Guidelines

1. **Keep slides concise** - Use bullet points, not paragraphs
2. **Use incremental reveals liberally** - Helps pace the lecture
3. **Include discussion questions** - Engage students
4. **Add interactive elements** - Games, polls, live demonstrations
5. **Cite sources in notes blocks** - Keep references but don't clutter slides
6. **Use blockquotes for key takeaways** - Makes them stand out

### Lecture Style

The lectures follow this pedagogical pattern:
- Start with a core economic principle
- Present real-world examples and evidence
- Include interactive activities (games, polls)
- Discuss policy implications
- Address counterarguments and nuances
- End with key takeaways

## Styling

The site uses **University of Chicago branding**:
- Primary color: `#800000` (UChicago Maroon)
- Accent color: `#ff8243` (Orange)
- Font: Inter (Google Fonts)

Use these colors for section headers and emphasis.

## Building the Site

To compile all pages and lectures:
```bash
quarto render
```

Output goes to `/docs/` which is served by GitHub Pages.

To preview locally:
```bash
quarto preview
```

## Adding a New Lecture

1. Create `lectures/new-lecture.qmd` with the standard YAML header
2. Add any images to `lectures/images/`
3. Update `lectures/index.qmd` to link to the new lecture
4. Run `quarto render` to compile

## Course Schedule Reference

The course runs for 9 weeks (March 24 - May 21, 2026):
- **John List teaches**: Weeks 1-5 (Basics, Causation, Experiments, Education, Scaling)
- **Evan Rose teaches**: Weeks 6-9 (Incentives, Markets, Quasi-experiments, Labor/AI)

Lectures are Tuesday & Thursday, 11:00am - 12:20pm.

## Common Tasks

### Converting notes to slides
When given rough notes, transform them into properly formatted RevealJS slides following the conventions above. Focus on:
- Breaking content into digestible slides
- Adding incremental reveals for pacing
- Creating section headers for major topic shifts
- Including discussion prompts and interactive elements

### Creating diagrams
For economic concepts, create SVG diagrams and save to `lectures/images/`. Use simple, clean designs with the UChicago color palette.

### Updating the schedule
Edit `schedule.qmd` directly. The schedule uses a simple markdown table format.
