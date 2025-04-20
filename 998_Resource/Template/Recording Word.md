<%*
const {autoprop} = this.app.plugins.plugins["metaedit"].api;
_%>
Mean:: <% await autoprop("mean") %>
Comment:: <% await autoprop("Comment") %>


---
