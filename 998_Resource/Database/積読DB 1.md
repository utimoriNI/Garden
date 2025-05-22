---
cssclasses: []
---

```dataviewjs
const headings = ["Name", "Status"];
const query = "#📚Book";
const limit = 30;

const {fieldModifier: f} = this.app.plugins.plugins["metadata-menu"].api;

dv.table(headings,
	await Promise.all(dv.pages(query)
	.map(async p=> [
		p.file.link,
		await f(dv, p, "Status")
		])
));
```

