---
cssclasses:
  - cards
  - cards-cols-1
  - timeline
---

```dataviewjs
const p = dv.pages("#Fleeting");
dv.table(["title", "createdAt", "preview"], p.sort(x=>x.file.mday, "desc").map(x => {

// コンテンツを処理

    let content = x.file.content || "";
    content = content.replace(/^---[\s\S]*?---\n/, ''); // YAMLフロントマターを除去
    content = content.replace(/\n+/g, ' ').trim(); // 改行を空白に変換


   // プレビューテキストを生成
    const preview = content.length > 120 ? content.substring(0, 120) + "..." : content;
	console.log(content)
	return [x.file.link, x.file.cday, preview || ""]
	})
);
```

