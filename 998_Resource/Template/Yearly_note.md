




```dataviewjs
const source = '"100_Periodic/Daily"'
const results = dv.pages(source).filter(p => p.file.ctime.year === 2024).sort(p => p.file.ctime, 'desc')

const list = results.flatMap(p => {
	return p.file.lists.where(item => item.section.subpath === "Log" && item.position.start.col ===0).map(item => {
		return [p.file.link, dv.markdownTaskList([item])];
	});
});

dv.table(['file','Log'], list)
```

