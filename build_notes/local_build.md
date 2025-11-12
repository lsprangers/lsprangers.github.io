## Ruby Setup
- Downloaded ruby via homebrew
- Setup gemfile
```
    export PATH="/opt/homebrew/opt/ruby/bin:$PATH" && bundle install && bundle exec jekyll serve
```

`gem install jekyll bundler`

# Folder Structure
For any folder, the `index.md` or `index.mdx` will be rendered when clicking on it, and any `subdoc.md` will be displayed underneath the folder

For example below, clicking on Foo would render `docs/foo/index.mdx`, and we'd see `Thing` as a sub-document you can click on
```
docs/
    foo/
        thing.md
        index.mdx
    bar/
        thang.md
        index.mdx
    baz/
        tang.md
        index.md
```

## Linking anchors
Relative link (recommended):
Apply to index.mdx
[Celery Queue's](/docs/architecture_components/messaging/Queue/#celery-queues)
or, if you are in a different directory:
Apply to index.mdx
[Celery Queue's](/docs/architecture_components/messaging/Queue/#celery-queues)
Absolute link (if you want to use the full site path):
Apply to index.mdx
[Celery Queue's](/docs/architecture_components/messaging/Queue/#celery-queues)
Note: The /docs/ prefix is used if your Docusaurus site is configured with the default docs base path

# Blog
Example blog structure posted in `2021-08026-welcome`

# Docusaurus
`npm install`
`npm run start`
`npm run clear`

Real one: `npm run build`