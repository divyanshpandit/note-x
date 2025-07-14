document.addEventListener("DOMContentLoaded", () => {
  const themeBtn   = document.getElementById("theme-btn");
  const deleteBtn  = document.getElementById("delete-btn");
  const sendBtn    = document.getElementById("send-btn");
  const textarea   = document.getElementById("chat-input");
  const form       = document.getElementById("prompt-form");
  const msgZone    = document.getElementById("msg-zone");
  const spinnerTpl = document.getElementById("spinner-tmpl").content;

  themeBtn.onclick = () => {
    document.body.classList.toggle("light-mode");
    themeBtn.textContent =
      document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
  };

  deleteBtn.onclick = () => (textarea.value = "");

  sendBtn.onclick = () => textarea.value.trim() && form.requestSubmit();

  form.addEventListener("submit", async e => {
    e.preventDefault();

    msgZone.innerHTML = "";
    msgZone.appendChild(spinnerTpl.cloneNode(true));

    const resp = await fetch("/", {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: new FormData(form)
    });

    const data   = await resp.json();
    const taskId = data.task_id;
    pollStatus(taskId);
  });

  async function pollStatus(id) {
    const res  = await fetch(`/api/status/${id}`);
    const data = await res.json();

    if (data.state === "SUCCESS") {
      showDownload(id);
    } else if (data.state === "FAILURE") {
      msgZone.textContent = "Error: " + (data.result?.error || "unknown");
    } else {
      setTimeout(() => pollStatus(id), 3000);
    }
  }

  function showDownload(id) {
    msgZone.innerHTML =
      `<a class="dl-btn" href="/download/${id}" download>⬇ Download PDF</a>`;
  }

  textarea.addEventListener("keydown", e => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      sendBtn.click();
    }
  });
});
