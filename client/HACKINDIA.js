let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;
<<<<<<< HEAD

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


// 🚀 SUBMIT BUTTON (UPDATED LOGIC)
document.getElementById("submitBtn").addEventListener("click", async () => {

  const text = document.getElementById("textInput").value;

  try {
    let res;

    // 🟢 PRIORITY: AUDIO
    if (recordedBlob) {

      const formData = new FormData();
      formData.append("file", recordedBlob);

      res = await fetch("http://localhost:8000/api/verify-audio", {
        method: "POST",
        body: formData
      });

    }

    // 🟡 TEXT INPUT
    else if (text) {

      res = await fetch("http://localhost:8000/api/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

    }

    // ❌ NOTHING ENTERED
    else {
      showError("Enter text or audio");
      return;
    }
=======

// Get API base URL (works both local and production)
const API_BASE = "http://127.0.0.1:8000";

// 🎙 RECORD BUTTON
document.getElementById("recordBtn").addEventListener("click", async () => {
>>>>>>> a4da717 (fix:routing issues)

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


<<<<<<< HEAD
// ❌ ERROR HANDLER (UNCHANGED)
=======
// 📁 UPLOAD BUTTON
document.getElementById("uploadBtn").addEventListener("click", () => {
  document.getElementById("audioUpload").click();
});

document.getElementById("audioUpload").addEventListener("change", (e) => {
  recordedBlob = e.target.files[0];
  document.getElementById("audioStatus").innerText = "📁 Audio uploaded";
});


// 🚀 SUBMIT BUTTON (UPDATED WITH CORRECT ENDPOINTS)
document.getElementById("submitBtn").addEventListener("click", async () => {

  const text = document.getElementById("textInput").value;

  try {
    let res;

    // 🟢 PRIORITY: AUDIO
    if (recordedBlob) {

      const formData = new FormData();
      formData.append("file", recordedBlob);

      console.log("📤 Sending audio to:", `${API_BASE}/api/voice/verify`);

      res = await fetch(`${API_BASE}/api/voice/verify`, {
        method: "POST",
        body: formData
      });

    }

    // 🟡 TEXT INPUT
    else if (text) {

      console.log("📤 Sending text to:", `${API_BASE}/api/verify/text`);

      res = await fetch(`${API_BASE}/api/verify/text`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
      body: JSON.stringify({
  text: text,   // use true for testing (important)
})
      });

    }

    // ❌ NOTHING ENTERED
    else {
      showError("Enter text or audio");
      return;
    }

    // Check if response is OK
    if (!res.ok) {
      const errorData = await res.json();
      showError(`Error: ${errorData.detail || res.statusText}`);
      return;
    }

    const data = await res.json();

    console.log("✅ Response received:", data);

    // Handle different response formats
    let displayText = "";
    
    if (data.verification) {
      // Voice verification response
      const v = data.verification;
      displayText = `
        <div style="margin-top:20px; color: #f5d76e;">
          <p><b>🎙 Transcribed:</b> ${data.transcribed_text}</p>
          <p><b>📊 Score:</b> ${v.final_score}/100</p>
          <p><b>📝 Verdict:</b> ${v.verdict}</p>
          <p><b>💭 Reasoning:</b> ${v.ai_reasoning}</p>
        </div>
      `;
    } else if (data.final_score !== undefined) {
      // Text verification response
      displayText = `
        <div style="margin-top:20px; color: #f5d76e;">
          <p><b>📊 Score:</b> ${data.final_score}/100</p>
          <p><b>📝 Verdict:</b> ${data.verdict}</p>
          <p><b>💭 Reasoning:</b> ${data.ai_reasoning}</p>
          <p><b>🌐 Language:</b> ${data.detected_language}</p>
        </div>
      `;
    } else if (data.score !== undefined) {
      // Generic response
      displayText = `
        <div style="margin-top:20px; color: #f5d76e;">
          <p><b>Score:</b> ${data.score}</p>
          <p>${data.reasoning || data.verdict || "Verification complete"}</p>
        </div>
      `;
    }

    document.getElementById("resultContainer").innerHTML = displayText;

  } catch (err) {
    console.error("❌ Error:", err);
    showError("Failed to fetch: " + err.message);
  }
});


// ❌ ERROR HANDLER
>>>>>>> a4da717 (fix:routing issues)
function showError(msg) {
  console.error("Error:", msg);
  document.getElementById("resultContainer").innerHTML = `
    <div class="error-box">
      ⚠️ ${msg}
    </div>
  `;
}
