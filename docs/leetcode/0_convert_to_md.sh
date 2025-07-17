#!/bin/bash

# Usage: ./0_convert_to_md.sh /path/to/sourcefile.ext

src="$1"
filename=$(basename -- "$src")
extension="${filename##*.}"
name="${filename%.*}"

# Convert filename to Title Case for Markdown title
title=$(echo "$name" | sed -E 's/(^|_)([a-z])/\U\2/g' | sed 's/_/ /g')

# Map extension to language and folder
case "$extension" in
  cpp) lang="cpp"; folder="cpp";;
  py) lang="python"; folder="python";;
  js) lang="javascript"; folder="javascript";;
  java) lang="java"; folder="java";;
  *) lang="$extension"; folder="other";;
esac

# Output markdown file path
outdir="docs/leetcode/$folder"
mkdir -p "$outdir"
outfile="$outdir/$name.md"

# Write to markdown file
{
  echo "---"
  echo "title: $title"
  echo "category: Leetcode Solutions"
  echo "difficulty: Advanced"
  echo "show_back_link: true"
  echo "---"
  echo
  echo "# $title"
  echo
  echo '```'"$lang"
  cat "$src"
  echo '```'
} > "$outfile"

echo "Created $outfile"