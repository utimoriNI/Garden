---
cssclasses:
  - cards
  - cards-1-1
---

```dataviewjs
const p = dv.pages("#Scrap");
console.log("p",p[0])
dv.table(["title"], p.sort(x=>x.file.mday, "desc").map(x => [x.file.link]));
```




