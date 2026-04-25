document.getElementById("submitBtn").addEventListener("click", async () => {
  const text = document.getElementById("textInput").value;

  if (!text) {
    showError("Enter text first");
    return;
  }

  try {
    const res = await fetch("http://localhost:8000/api/verify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    const data = await res.json();

    document.getElementById("resultContainer").innerHTML = `
      <div style="margin-top:20px;">
        <p><b>Score:</b> ${data.score}</p>
        <p>${data.reasoning}</p>
      </div>
    `;

  } catch (err) {
    showError("Failed to fetch");
  }
});

function showError(msg) {
  document.getElementById("resultContainer").innerHTML = `
    <div class="error-box">
      ⚠️ ${msg}
    </div>
  `;
}