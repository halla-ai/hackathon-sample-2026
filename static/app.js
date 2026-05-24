const form = document.querySelector("#ask-form");
const question = document.querySelector("#question");
const answer = document.querySelector("#answer");
const mode = document.querySelector("#mode");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = question.value.trim();
  if (!text) return;

  answer.textContent = "Thinking...";
  mode.textContent = "running";

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Request failed");
    }
    answer.textContent = data.answer;
    mode.textContent = data.mode;
  } catch (error) {
    answer.textContent = error instanceof Error ? error.message : String(error);
    mode.textContent = "error";
  }
});
