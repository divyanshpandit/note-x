document.addEventListener("DOMContentLoaded", () => {
  const themeBtn   = document.getElementById("theme-btn");
  const deleteBtn  = document.getElementById("delete-btn");
  const sendBtn    = document.getElementById("send-btn");
  const textarea   = document.getElementById("chat-input");
  const form       = document.getElementById("prompt-form");
  const msgZone    = document.getElementById("msg-zone");
  const spinnerTpl = document.getElementById("spinner-tmpl").content;

  /* ─── Theme toggle ─── */
  themeBtn.onclick = () => {
    document.body.classList.toggle("light-mode");
    themeBtn.textContent =
      document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
  };

  /* ─── Clear textarea ─── */
  deleteBtn.onclick = () => (textarea.value = "");

  /* ─── Send click ─── */
  sendBtn.onclick = () => textarea.value.trim() && form.requestSubmit();

  /* ─── Intercept form submit ─── */
  form.addEventListener("submit", async e => {
    e.preventDefault();

    // show spinner
    msgZone.innerHTML = "";
    msgZone.appendChild(spinnerTpl.cloneNode(true));

    // POST via fetch; ask for JSON response instead of redirect
    const resp = await fetch("/", {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },   // key line
      body: new FormData(form)
    });

    const data   = await resp.json();      // { task_id: "..." }
    const taskId = data.task_id;
    pollStatus(taskId);
  });

  /* ─── Poll backend ─── */
  async function pollStatus(id) {
    const res  = await fetch(`/api/status/${id}`);
    const data = await res.json();

    if (data.state === "SUCCESS") {
      showDownload(id);
    } else if (data.state === "FAILURE") {
      msgZone.textContent = "Error: " + (data.error ?? "unknown");
    } else {
      setTimeout(() => pollStatus(id), 3000);
    }
  }

  /* ─── Show download button ─── */
  function showDownload(id) {
    msgZone.innerHTML =
      `<a class="dl-btn" href="/download/${id}" download>⬇ Download PDF</a>`;
  }

  /* ─── Ctrl+Enter shortcut ─── */
  textarea.addEventListener("keydown", e => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      sendBtn.click();
    }
  });
});
