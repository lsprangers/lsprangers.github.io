---
layout: just_the_docs_clean
title: "Just the Docs Demo"
parent: "Technical"
nav_order: 1
---

# Just the Docs Demo

This is a demonstration of a pure Just the Docs layout without any custom HTML components.

## Features

- **Clean Navigation**: Auto-generated from your collections
- **Search**: Built-in search functionality
- **Responsive**: Works on all devices
- **No Custom HTML**: Pure Just the Docs theme

## Configuration

The layout uses the following configuration:

```yaml
just_the_docs:
  color_scheme: light
  title: true
  search: true
  back_to_top: true
  gh_edit_link: false
  last_edit_timestamp: false
  last_edit_author: false
  footer_content: false
  heading_anchors: true
```

## Navigation Structure

The navigation is automatically generated from your `_technical` collection and follows the folder structure. Each markdown file becomes a page in the navigation.

## Code Example

```python
def hello_world():
    print("Hello, Just the Docs!")
    return "Success"
```

## Lists

- Item 1
- Item 2
- Item 3

## Tables

| Feature | Status |
|---------|--------|
| Search | ✅ Enabled |
| Navigation | ✅ Auto-generated |
| Custom HTML | ❌ Disabled |
| Responsive | ✅ Yes |

## Callouts

{: .note }
This is a note callout.

{: .warning }
This is a warning callout.

{: .tip }
This is a tip callout. 