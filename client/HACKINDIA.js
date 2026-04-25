let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;

const API_BASE = "http://127.0.0.1:8000";

// 🎙 RECORD BUTTON
document.getElementById("recordBtn").addEventListener("click", async () => {

  if (!mediaRecorder || mediaRecorder.state === "inactive") {

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = e => audioChunks.push(e.data);

    mediaRecorder.onstop = () => {
      recordedBlob = new Blob(audioChunks, { type: "audio/webm" });
      document.getElementById("audioStatus").innerText = "🎧 Audio recorded";
    };

    mediaRecorder.start();
    document.getElementById("audioStatus").innerText = "Recording...";

  } else {
    mediaRecorder.stop();
  }
});


// 📁 UPLOAD BUTTON
document.getElementById("uploadBtn").addEventListener("click", () => {
  document.getElementById("audioUpload").click();
});

document.getElementById("audioUpload").addEventListener("change", (e) => {
  recordedBlob = e.target.files[0];
  document.getElementById("audioStatus").innerText = "📁 Audio uploaded";
});


// 🚀 SUBMIT BUTTON
document.getElementById("submitBtn").addEventListener("click", async () => {

  const text = document.getElementById("textInput").value;

  try {
    let res;

    // 🟢 AUDIO
    if (recordedBlob) {

      const formData = new FormData();
      formData.append("file", recordedBlob);

      console.log("📤 Sending audio to:", `${API_BASE}/api/voice/verify`);

      res = await fetch(`${API_BASE}/api/voice/verify`, {
        method: "POST",
        body: formData
      });

    }

    // 🟡 TEXT
    else if (text) {

      console.log("📤 Sending text to:", `${API_BASE}/api/verify/text`);

      res = await fetch(`${API_BASE}/api/verify/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
      });

    }

    else {
      showError("Enter text or audio");
      return;
    }

    if (!res.ok) {
      const errorData = await res.json();
      showError(errorData.detail || "Something went wrong");
      return;
    }

    const data = await res.json();
    console.log("✅ Response:", data);

    let displayText = `
      <div style="margin-top:20px; color: #f5d76e;">
        <p><b>📊 Score:</b> ${data.final_score}/100</p>
        <p><b>📝 Verdict:</b> ${data.verdict}</p>
        <p><b>💭 Reasoning:</b> ${data.ai_reasoning}</p>
        <p><b>🌐 Language:</b> ${data.detected_language}</p>
      </div>
    `;

    document.getElementById("resultContainer").innerHTML = displayText;

  } catch (err) {
    console.error("❌ Error:", err);
    showError("Failed to fetch: " + err.message);
  }
});


// ❌ ERROR HANDLER
function showError(msg) {
  document.getElementById("resultContainer").innerHTML = `
    <div class="error-box">⚠️ ${msg}</div>
  `;
}