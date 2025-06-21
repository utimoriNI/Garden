---
cssclasses:
  - cards
  - cards-1-1
tags:
  - 🎁Topic
---
```dataview
LIST
FROM #🎁Topic/Life 
```

### その他Topic
```dataview
TABLE
FROM #🎁Topic   // 必要に応じてフォルダを指定
WHERE contains(file.etags, "#🎁Topic") AND all(file.etags, (tag) => !startswith(tag, "#🎁Topic/")) AND file.name != this.file.name
```
