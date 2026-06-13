(function () {
  const data = window.READING_NOTE_EXPLORER_DATA;
  const state = {
    topic: null,
    noteId: null,
    search: "",
  };

  const topicListEl = document.getElementById("topic-list");
  const noteListEl = document.getElementById("note-list");
  const detailEl = document.getElementById("detail");
  const topicTitleEl = document.getElementById("topic-title");
  const topicMetaEl = document.getElementById("topic-meta");
  const searchInputEl = document.getElementById("search-input");

  function escapeHtml(value) {
    return value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function slugTopic(topic) {
    return topic.replace(/^Topic\//, "");
  }

  function noteMatchesSearch(note, search) {
    if (!search) {
      return true;
    }
    const haystack = [
      note.title,
      note.preview,
      note.fragment,
      note.memo,
      note.myTake,
      note.topics.join(" "),
      note.tags.join(" "),
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(search.toLowerCase());
  }

  function topicNotes(topic) {
    const record = data.topics.find((item) => item.name === topic);
    if (!record) {
      return [];
    }
    return record.noteIds
      .map((noteId) => data.notes[noteId])
      .filter(Boolean)
      .filter((note) => noteMatchesSearch(note, state.search));
  }

  function setHash() {
    const parts = new URLSearchParams();
    if (state.topic) {
      parts.set("topic", state.topic);
    }
    if (state.noteId) {
      parts.set("note", state.noteId);
    }
    window.location.hash = parts.toString();
  }

  function readHash() {
    const params = new URLSearchParams(window.location.hash.slice(1));
    const fallbackTopic = data.topics[0] ? data.topics[0].name : null;
    state.topic = params.get("topic") || fallbackTopic;
    const notes = topicNotes(state.topic);
    state.noteId = params.get("note") || (notes[0] ? notes[0].id : null);
  }

  function renderTopics() {
    topicListEl.innerHTML = data.topics
      .map((topic) => {
        const active = topic.name === state.topic ? "active" : "";
        return `
          <button class="topic-chip ${active}" data-topic="${escapeHtml(topic.name)}">
            <span>${escapeHtml(slugTopic(topic.name))}</span>
            <strong>${topic.count}</strong>
          </button>
        `;
      })
      .join("");

    topicListEl.querySelectorAll("[data-topic]").forEach((button) => {
      button.addEventListener("click", () => {
        state.topic = button.getAttribute("data-topic");
        const notes = topicNotes(state.topic);
        state.noteId = notes[0] ? notes[0].id : null;
        setHash();
        render();
      });
    });
  }

  function renderNoteList() {
    const notes = topicNotes(state.topic);
    topicTitleEl.textContent = state.topic ? slugTopic(state.topic) : "No topic";
    topicMetaEl.textContent = `${notes.length} notes / ${data.noteCount} total`;

    if (!notes.length) {
      noteListEl.innerHTML = `<div class="empty">該当する note がありません。</div>`;
      return;
    }

    if (!notes.some((note) => note.id === state.noteId)) {
      state.noteId = notes[0].id;
      setHash();
    }

    noteListEl.innerHTML = notes
      .map((note) => {
        const active = note.id === state.noteId ? "active" : "";
        const topics = note.topics.map((topic) => `<span class="pill">${escapeHtml(slugTopic(topic))}</span>`).join("");
        return `
          <button class="note-card ${active}" data-note-id="${escapeHtml(note.id)}">
            <div class="note-card-header">
              <h3>${escapeHtml(note.title)}</h3>
              <span class="source-type">${escapeHtml(note.sourceType || "unknown")}</span>
            </div>
            <div class="pill-row">${topics}</div>
            <p>${escapeHtml(note.preview || "本文プレビューなし")}</p>
          </button>
        `;
      })
      .join("");

    noteListEl.querySelectorAll("[data-note-id]").forEach((button) => {
      button.addEventListener("click", () => {
        state.noteId = button.getAttribute("data-note-id");
        setHash();
        renderDetail();
        renderNoteList();
      });
    });
  }

  function renderMeta(label, value) {
    if (!value) {
      return "";
    }
    return `<div class="meta-row"><span>${escapeHtml(label)}</span><strong>${escapeHtml(value)}</strong></div>`;
  }

  function renderSection(title, body) {
    if (!body) {
      return "";
    }
    return `
      <section class="detail-section">
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(body).replaceAll("\n", "<br>")}</p>
      </section>
    `;
  }

  function renderRelatedCard(item) {
    const note = data.notes[item.noteId];
    if (!note) {
      return "";
    }
    const reasons = item.reasons
      .map((reason) => `<span class="reason">${escapeHtml(reason)}</span>`)
      .join("");
    return `
      <button class="related-card" data-note-id="${escapeHtml(note.id)}">
        <div class="related-card-header">
          <h4>${escapeHtml(note.title)}</h4>
          <span>${item.score}</span>
        </div>
        <p>${escapeHtml(note.preview || "本文プレビューなし")}</p>
        <div class="reason-row">${reasons}</div>
      </button>
    `;
  }

  function renderDetail() {
    const note = state.noteId ? data.notes[state.noteId] : null;
    if (!note) {
      detailEl.innerHTML = `<div class="empty">note を選ぶと詳細が出ます。</div>`;
      return;
    }

    const topicPills = note.topics.map((topic) => `<span class="pill">${escapeHtml(slugTopic(topic))}</span>`).join("");
    const relatedHtml = note.related.map(renderRelatedCard).join("");

    detailEl.innerHTML = `
      <article class="detail-card">
        <div class="detail-header">
          <div>
            <p class="eyebrow">Reading Note</p>
            <h2>${escapeHtml(note.title)}</h2>
          </div>
          <a class="path-link" href="obsidian://open?path=${encodeURIComponent(note.path)}">${escapeHtml(note.path)}</a>
        </div>

        <div class="pill-row">${topicPills}</div>

        <div class="meta-grid">
          ${renderMeta("Source type", note.sourceType)}
          ${renderMeta("Source", note.sourceContainer || note.sourceBook)}
          ${renderMeta("MOC", note.mocs.join(", "))}
          ${renderMeta("Consist of", note.consistsOf.join(", "))}
        </div>

        ${renderSection("Preview", note.preview)}
        ${renderSection("Fragment", note.fragment)}
        ${renderSection("Memo", note.memo)}
        ${renderSection("My Take", note.myTake)}
      </article>

      <section class="related-section">
        <div class="column-header">
          <div>
            <p class="eyebrow">Related Notes</p>
            <h3>同じ topic を起点に読める近傍</h3>
          </div>
        </div>
        <div class="related-list">
          ${relatedHtml || `<div class="empty">この topic 内で強い関連はまだ見つかっていません。</div>`}
        </div>
      </section>
    `;

    detailEl.querySelectorAll("[data-note-id]").forEach((button) => {
      button.addEventListener("click", () => {
        state.noteId = button.getAttribute("data-note-id");
        setHash();
        renderNoteList();
        renderDetail();
      });
    });
  }

  function render() {
    renderTopics();
    renderNoteList();
    renderDetail();
  }

  searchInputEl.addEventListener("input", (event) => {
    state.search = event.target.value.trim();
    renderNoteList();
    renderDetail();
  });

  window.addEventListener("hashchange", () => {
    readHash();
    render();
  });

  readHash();
  render();
})();
