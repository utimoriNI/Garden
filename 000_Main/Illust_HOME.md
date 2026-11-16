
```dataview
TABLE tags
FROM "300_Input"
WHERE contains(tags, "Illust")
SORT tags
```


```dataview
TABLE rows.file.link as Note
FROM "600_Knowledge"
WHERE contains(tags, "Illust")
```
