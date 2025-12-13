---
---
```dataview
TABLE without id tags,rows.file.link as タイトル
FROM "300_Input"
WHERE tag != "📚Book"
FLATTEN tags
GROUP BY tags
```
