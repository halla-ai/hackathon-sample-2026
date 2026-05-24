const form = document.querySelector("#review-form");
const cv = document.querySelector("#cv");
const result = document.querySelector("#result");
const mode = document.querySelector("#mode");
const submitBtn = document.querySelector("#submit-btn");

function renderList(title, items, emptyText) {
  if (!items || items.length === 0) {
    return `<section class="result-block"><h3>${title}</h3><p class="empty">${emptyText}</p></section>`;
  }
  const lis = items.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  return `<section class="result-block"><h3>${title}</h3><ul>${lis}</ul></section>`;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderResult(data) {
  const flags = data.red_flags || [];
  const flagsBlock =
    flags.length > 0
      ? `<section class="result-block result-block--flag"><h3>⚠ Red flags</h3><ul>${flags
          .map((flag) => `<li>${escapeHtml(flag)}</li>`)
          .join("")}</ul></section>`
      : "";
  result.innerHTML = [
    renderList("✓ Strengths", data.strengths, "No clear strengths surfaced — try expanding the CV."),
    renderList("✗ Weaknesses", data.weaknesses, "No weaknesses flagged."),
    renderList("→ Suggestions", data.suggestions, "No suggestions returned."),
    flagsBlock,
  ].join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = cv.value.trim();
  if (text.length < 20) {
    result.innerHTML = `<p class="error">Paste at least 20 characters of CV text.</p>`;
    mode.textContent = "error";
    return;
  }

  submitBtn.disabled = true;
  result.innerHTML = `<p class="placeholder">Reviewing… this takes a few seconds.</p>`;
  mode.textContent = "running";

  try {
    const response = await fetch("/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cv: text }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    renderResult(data);
    mode.textContent = data.mode;
  } catch (error) {
    result.innerHTML = `<p class="error">${escapeHtml(error instanceof Error ? error.message : String(error))}</p>`;
    mode.textContent = "error";
  } finally {
    submitBtn.disabled = false;
  }
});
