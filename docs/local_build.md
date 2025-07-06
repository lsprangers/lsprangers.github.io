## Ruby Setup
- Downloaded ruby via homebrew
- Setup gemfile
```
    export PATH="/opt/homebrew/opt/ruby/bin:$PATH" && bundle install && bundle exec jekyll serve
```

## Submodules
`git submodule add https://github.com/lsprangers/implementations-and-systems-design.git _content/implementations`

To update: `git submodule update --remote`