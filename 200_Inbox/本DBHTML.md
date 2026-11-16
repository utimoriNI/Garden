```dataviewjs
const p = dv.el("input")
p.placeholder = "..."
p.style = "font-size:large;border-radius:3px;"
const btn = dv.el("button", "＋")
btn.style = "font-size:small;margin:5px;width:40px;"
const b = dv.el("div", "")
b.style = "max-height:14000px;"
disp()

p.onkeyup = () => disp()

btn.onclick = () =>{
  navigator.clipboard.writeText(p.value)
  s = "obsidian-book-search-plugin:open-book-search-modal"
  app.commands.executeCommandById(s) 
}

function disp(){
  const  d = dv.pages('"300_Input/Book"').where(x=>(x.status == '読みたい'))
  .filter(x => (x.title + x.subtitle + x.author + x.description).includes([p.value]))
  .sort(x => x.file.ctime, "desc")
  .map(x => `<tr style="font-size:small;padding:4px;"><td><a class=internal-link href="${x.file.name}"><img style="max-width:60px;" src="${x.cover}"></a></td><td><a class=internal-link href="${x.file.name}">${x.title}</a></td><td>${x.author}</td><td>${(x.publisher || "")}</td></tr>`)
  b.innerHTML = "<br><table style='width:100%;'>" + d.join("\n") + "</table>"
}
```
