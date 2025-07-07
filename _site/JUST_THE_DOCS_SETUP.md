# Just the Docs Layout Setup

This setup provides a pure Just the Docs layout without any custom HTML components.

## Files Created

1. **`_config_just_the_docs.yml`** - Clean configuration file
2. **`_layouts/just_the_docs_clean.html`** - Minimal layout file
3. **`just_the_docs_demo.md`** - Demo page showing the layout
4. **`JUST_THE_DOCS_SETUP.md`** - This documentation

## How to Use

### Option 1: Replace Current Config
1. Backup your current `_config.yml`
2. Replace with `_config_just_the_docs.yml`
3. Rename to `_config.yml`

### Option 2: Use as Alternative Config
1. Run Jekyll with the alternative config:
   ```bash
   jekyll serve --config _config_just_the_docs.yml
   ```

## Key Features

### ✅ What's Included
- Pure Just the Docs theme
- Auto-generated navigation from collections
- Built-in search functionality
- Responsive design
- Code syntax highlighting
- Callouts and admonitions
- Tables and lists
- Heading anchors

### ❌ What's Removed
- Custom masthead HTML
- Custom footer HTML
- Custom head includes
- Custom navigation menus
- Profile photos and custom styling

## Configuration Options

The `_config_just_the_docs.yml` includes these key settings:

```yaml
just_the_docs:
  color_scheme: light          # or "dark"
  title: true                  # Show site title
  search: true                 # Enable search
  back_to_top: true           # Back to top button
  gh_edit_link: false         # GitHub edit links
  last_edit_timestamp: false  # Last modified date
  last_edit_author: false     # Last modified author
  footer_content: false       # Custom footer
  heading_anchors: true       # Anchor links on headings
```

## Navigation Structure

The navigation is automatically generated from your `_technical` collection:

- Each folder becomes a section
- Each `.md` file becomes a page
- Use `nav_order` in front matter to control order
- Use `parent` to create nested pages

## Page Front Matter

For pages using this layout:

```yaml
---
layout: just_the_docs_clean
title: "Page Title"
parent: "Section Name"
nav_order: 1
---
```

## Benefits

1. **Cleaner Code**: No custom HTML to maintain
2. **Better Performance**: Fewer HTTP requests
3. **Easier Maintenance**: Standard Just the Docs updates
4. **Consistent Styling**: No custom CSS conflicts
5. **Better Accessibility**: Built-in accessibility features

## Migration Steps

If you want to migrate from your current setup:

1. **Backup everything**
2. **Replace `_config.yml`** with the clean version
3. **Remove custom includes** from `_includes/`
4. **Update page layouts** to use `just_the_docs_clean`
5. **Test thoroughly** before deploying

## Customization

If you need minimal customization:

1. **Colors**: Change `color_scheme` to "dark"
2. **Logo**: Add `logo: path/to/logo.png` to config
3. **External Links**: Modify `nav_external_links` in config
4. **Search**: Adjust search settings in config

## Troubleshooting

### Navigation Not Showing
- Ensure files are in the `_technical` collection
- Check that `output: true` is set for the collection
- Verify front matter has correct `layout` and `title`

### Search Not Working
- Check that `search: true` and `search_enabled: true` are set
- Ensure `search_full_content: true` if needed
- Verify `search_provider: lunr` is set

### Styling Issues
- Remove any custom CSS files
- Clear browser cache
- Check for conflicting theme settings 