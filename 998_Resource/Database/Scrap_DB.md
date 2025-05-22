---
cssclasses:
  - cards
  - cards-1-1
---
```dataviewjs
dv.table(["title"], dv.pages("#Scrap").sort(x=>x.file.mday, "desc").map(x => [x.file.frontmatter.image ? dv.span(`!${x.file.frontmatter.image.slice(0,-2)}|150x150]]`):"",x.file.link]));
```
