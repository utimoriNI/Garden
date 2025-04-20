```dataviewjs

const notes = await dv.query(`
	TABLE rows.file.link as Note, tags
	FROM "700_Project/Words"
	FLATTEN tags
	GROUP BY tags
	SORT tags
`)

let typeDict = {}
for(let note of notes.value.values){
	if(!typeDict.hasOwnProperty(note[0]))
		typeDict[note[0]] = []

	typeDict[note[0]].push([...note.slice(1)])	
}

for (let key of Object.keys(typeDict)) {
	dv.header(4, key)
	dv.table([...notes.value.headers.slice(1)],
		typeDict[key])
}
```
