const stampGroup = document.getElementById("platform-stamps");
const form = document.getElementById("copy-form");
const generateBtn = document.getElementById("generate-btn");
const formHint = document.getElementById("form-hint");
const loading = document.getElementById("loading");
const loadingText = document.getElementById("loading-text");
const errorContainer = document.getElementById("error-container");
const resultsSection = document.getElementById("results-section");
const resultsTitle = document.getElementById("results-title");
const resultsGrid = document.getElementById("results-grid");
const emptyState = document.getElementById("empty-state");
const compareCheckbox = document.getElementById("compare-mode");

// --- platform stamp multi-select -------------------------------------------------
stampGroup.addEventListener("click", (e) => {
  const btn = e.target.closest(".stamp");
  if (!btn) return;
  btn.classList.toggle("active");
});

function getSelectedPlatforms() {
  return [...stampGroup.querySelectorAll(".stamp.active")].map((b) => b.dataset.platform);
}

// --- rendering helpers -------------------------------------------------------------
function dialHTML(pct, label) {
  return `
    <div class="dial" style="--pct:${pct}">
      <div class="dial-inner">${label}</div>
    </div>`;
}

function cardHTML(item, variantLabel) {
  const pctColor = item.compliant ? "ok" : "over";
  const pctLabelText = item.compliant ? "Within limit" : "Over limit";
  const tempPct = Math.min(Math.max(item.temperature, 0), 1);
  const download = `data:text/plain;charset=utf-8,${encodeURIComponent(item.text)}`;

  return `
    <article class="card">
      <div class="card-top">
        <div>
          <div class="card-platform">${item.platform}</div>
          ${variantLabel ? `<div class="card-variant-label">${variantLabel}</div>` : ""}
        </div>
        ${dialHTML(tempPct, item.temperature.toFixed(2))}
      </div>
      <div class="card-text">${escapeHTML(item.text)}</div>
      <div class="card-meta">
        <span>top_p ${item.top_p}</span>
        <span class="pill ${pctColor}">${item.char_count}/${item.limit} · ${pctLabelText}</span>
      </div>
      <div class="card-actions">
        <a class="btn-download" href="${download}" download="${item.platform}_${(variantLabel || 'copy').toLowerCase()}.txt">Download .txt</a>
      </div>
    </article>`;
}

function escapeHTML(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// --- submit handler ------------------------------------------------------------------
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorContainer.innerHTML = "";
  formHint.textContent = "";

  const product = document.getElementById("product").value.trim();
  const description = document.getElementById("description").value.trim();
  const tone = document.getElementById("tone").value;
  const platforms = getSelectedPlatforms();
  const compareMode = compareCheckbox.checked;

  if (!product || !description || platforms.length === 0) {
    formHint.textContent = "Fill product name, description, and pick at least one platform.";
    return;
  }

  generateBtn.disabled = true;
  loading.style.display = "flex";
  loadingText.textContent = compareMode
    ? "Running 3 temperature levels on one platform…"
    : "Compiling prompt and calling the model…";
  resultsSection.style.display = "none";
  emptyState.style.display = "none";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product, description, tone, platforms, compare_mode: compareMode }),
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    renderResults(data);
  } catch (err) {
    errorContainer.innerHTML = `<div class="error-box">${escapeHTML(err.message)}</div>`;
    emptyState.style.display = "block";
  } finally {
    generateBtn.disabled = false;
    loading.style.display = "none";
  }
});

function renderResults(data) {
  resultsGrid.innerHTML = "";
  emptyState.style.display = "none";

  if (data.mode === "compare") {
    resultsTitle.textContent = `Temperature comparison — ${data.results[0].platform}`;
    data.results.forEach((item) => {
      resultsGrid.insertAdjacentHTML("beforeend", cardHTML(item, item.label));
    });
  } else {
    resultsTitle.textContent = "Results";
    data.results.forEach((item) => {
      resultsGrid.insertAdjacentHTML("beforeend", cardHTML(item, null));
    });
  }

  resultsSection.style.display = "block";
}