---
cssclasses:
  - cards
  - cards-1-1
---

```dataview
TABLE WITHOUT ID
	("![cover|90](" + cover + ")") as Cover,
	link(file.link,title) as Title,
	Status
FROM "300_Input/Book"
WHERE Status = "積読"
```
