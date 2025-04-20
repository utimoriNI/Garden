---
cssclasses: []
---
```dataview
TABLE without ID rows.file.link as title,tags
FROM "600_Knowledge"
FLATTEN tags
GROUP BY tags
```

