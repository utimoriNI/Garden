---
cssclasses:
  - cards
  - cards-cols-1
---

```dataviewjs
const p = dv.pages("#Fleeting");
dv.table(["title", "createdAt"], p.sort(x=>x.file.mday, "desc").map(x => [x.file.link, x.file.cday]));
```
