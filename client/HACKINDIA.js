let mediaRecorder;
let audioChunks = [];
let recordedBlob = null;

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


// ❌ ERROR HANDLER (UNCHANGED)
function showError(msg) {
  document.getElementById("resultContainer").innerHTML = `
    <div class="error-box">
      ⚠️ ${msg}
    </div>
  `;
}
