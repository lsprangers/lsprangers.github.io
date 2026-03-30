# Structure
- `docs/`: Place technical writing, docs, and other items here
- `blog/`: Place to write up personal blogs
- `src/pages/`: Static pages like About Me, Resume, etc...
- `static/`: Images, files, etc
    - Can be used via `/img/your-image.png`

## Sidebar Navigation
Docusaurus auto-generates sidebar from `docs/` folder structure

Custom sidebar can be configured in `sidebars.js`

Custom Navigation Bar --> Edit docusaurus.config.js → themeConfig.navbar to add links to About, Resume, Projects, Blog, etc.


# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
npm run build
```