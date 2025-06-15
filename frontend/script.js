const API_BASE = "http://localhost:8000";

document.getElementById("logFile").addEventListener("change", function (e) {
  const fileName = e.target.files[0]?.name || "";
  document.getElementById("fileName").textContent = fileName;
});

document
  .getElementById("analyzeBtn")
  .addEventListener("click", async function () {
    const fileInput = document.getElementById("logFile");
    const file = fileInput.files[0];

    if (!file) {
      showError("Please select a log file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    await analyzeData(API_BASE + "/analyze", {
      method: "POST",
      body: formData,
    });
  });

document
  .getElementById("analyzeTextBtn")
  .addEventListener("click", async function () {
    const textInput = document.getElementById("logText");
    const text = textInput.value.trim();

    if (!text) {
      showError("Please enter some log entries first");
      return;
    }

    const logs = text.split("\n").filter((line) => line.trim());

    await analyzeData(API_BASE + "/analyze-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(logs),
    });
  });

async function analyzeData(url, options) {
  showLoading();
  hideError();
  hideResults();

  try {
    const response = await fetch(url, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed");
    }

    displayResults(data);
  } catch (error) {
    console.error("Error:", error);
    showError("Error analyzing logs: " + error.message);
  } finally {
    hideLoading();
  }
}

function displayResults(data) {
  const statsCard = document.getElementById("statsCard");
  const templatesDiv = document.getElementById("templates");

  // Display statistics
  statsCard.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${data.statistics.total_logs}</div>
                    <div class="stat-label">Total Logs</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${data.statistics.unique_templates}</div>
                    <div class="stat-label">Templates Found</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${data.statistics.coverage_percentage}%</div>
                    <div class="stat-label">Coverage</div>
                </div>
            `;

  // Display templates
  templatesDiv.innerHTML = "";
  data.templates.forEach((template) => {
    const templateCard = document.createElement("div");
    templateCard.className = "template-card";

    templateCard.innerHTML = `
                    <div class="template-header">
                        <span class="template-id">Template #${
                          template.id
                        }</span>
                        <span class="template-count">${
                          template.count
                        } occurrences</span>
                    </div>
                    <div class="template-pattern">${template.template}</div>
                    <div><strong>Confidence:</strong> ${(
                      template.confidence * 100
                    ).toFixed(1)}%</div>
                    <div class="examples">
                        <strong>Examples:</strong>
                        ${template.examples
                          .map(
                            (example) => `<div class="example">${example}</div>`
                          )
                          .join("")}
                    </div>
                `;

    templatesDiv.appendChild(templateCard);
  });

  showResults();
}

function showLoading() {
  document.getElementById("loading").style.display = "block";
}

function hideLoading() {
  document.getElementById("loading").style.display = "none";
}

function showResults() {
  document.getElementById("results").style.display = "block";
}

function hideResults() {
  document.getElementById("results").style.display = "none";
}

function showError(message) {
  const errorDiv = document.getElementById("error");
  errorDiv.textContent = message;
  errorDiv.style.display = "block";
}

function hideError() {
  document.getElementById("error").style.display = "none";
}
