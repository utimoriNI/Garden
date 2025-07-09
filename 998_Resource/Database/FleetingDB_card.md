---
cssclasses:
  - cards
  - cards-cols-1
  - timeline
---
```dataviewjs
const p = dv.pages("#Fleeting");

let rows =await Promise.all(
	p.map(async x => {

// コンテンツを処理
    let content = await dv.io.load(x.file.path);
    content = content.replace(/^---[\s\S]*?---\n/, ''); // YAMLフロントマターを除去
    content = content.replace(/\n+/g, ' ').trim(); // 改行を空白に変換
    content = content.replace(/^---\s*\[\[\d{4}-\d{2}-\d{2}\]\]\s*/m, ''); // 日付のリンクを除去
	content = content.replace(/^\s*!\[\[.*?\]\]\s*/gm, ''); // ![[FleetingDB_card]] のような埋め込みリンク行を除去

	  // 画像リンクを除去
    let noImages = content.replace(/!\[.*?\]\(.*?\)/g, "");
    // フロントマターを除去
    let noFrontmatter = noImages.replace(/^---[\s\S]*?---/, "");
    // 本文全体（必要ならtrimやsliceで調整）
    let body = noFrontmatter.trim();


   // プレビューテキストを生成
    const preview = body.length > 60 ? body.substring(0, 60) + "..." : body;
	return [x.file.link, preview || "", x.file.frontmatter.created]
	})
);

// createdで新しい順にソート（降順）
rows.sort((a, b) => {
    const dateA = new Date(a[2]); // a[2] = created
    const dateB = new Date(b[2]); // b[2] = created
    return dateB - dateA; // 新しい順（降順）
});

dv.table(["title", "preview", "createdAt", ], rows);

```

