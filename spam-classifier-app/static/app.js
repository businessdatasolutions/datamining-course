const messageInput = document.getElementById("message");
const classifyBtn = document.getElementById("classify-btn");
const resultDiv = document.getElementById("result");

classifyBtn.addEventListener("click", async () => {
  const text = messageInput.value.trim();
  if (!text) return;

  classifyBtn.disabled = true;
  classifyBtn.textContent = "Classifying...";

  try {
    const response = await fetch("/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();

    resultDiv.className = `result ${data.prediction}`;
    resultDiv.innerHTML = `
      <div class="label">${data.prediction}</div>
      <div class="details">
        Confidence: ${data.confidence}% &mdash;
        Ham: ${data.ham_prob}% | Spam: ${data.spam_prob}%
      </div>
    `;
  } catch {
    resultDiv.className = "result";
    resultDiv.innerHTML = `<div class="details">Error classifying message.</div>`;
  } finally {
    classifyBtn.disabled = false;
    classifyBtn.textContent = "Classify";
  }
});
