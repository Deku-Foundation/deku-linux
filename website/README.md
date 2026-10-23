# Deku Linux website preview

This directory contains a static, dependency-free website prototype intended to move into the dedicated GitHub Pages repository, `Deku-Foundation.github.io`.

## Preview locally

Open `index.html` in a browser, or run a simple local static server from this directory:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Design and content principles

- Responsive, editorial layout with neutral colors and a restrained green accent.
- Semantic HTML, keyboard-visible focus, a skip link, mobile navigation, and reduced-motion support.
- No analytics, tracking scripts, backend, package manager, or framework dependency.
- No fake downloads, release dates, stability claims, or security claims.
- All technical directions are clearly labeled as under evaluation.

## Publishing

This is a preview inside the project repository, not the live website. The recommended final location is the independent organization site repository `Deku-Foundation.github.io`. After that repository exists and is accessible, move these files to its root, add a pinned GitHub Pages workflow, enable Pages in repository settings, and verify the deployment before announcing the URL.
