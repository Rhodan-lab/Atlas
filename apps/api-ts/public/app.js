const statsElement = document.querySelector("#stats");
const conceptsElement = document.querySelector("#concepts");
const resultsElement = document.querySelector("#search-results");
const form = document.querySelector("#search-form");
const queryInput = document.querySelector("#query");
const reloadButton = document.querySelector("#reload");

async function request(path) {
    const response = await fetch(path);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error ?? `Request failed: ${response.status}`);
    return payload;
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"]/g, character => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",
    })[character]);
}

function card(concept, score = null) {
    const tags = concept.tags.map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join("");
    return `<article class="card">
        ${score === null ? "" : `<div class="score">SCORE ${escapeHtml(score)}</div>`}
        <h3>${escapeHtml(concept.title)}</h3>
        <p>${escapeHtml(concept.summary)}</p>
        <div class="tags">${tags}</div>
    </article>`;
}

async function loadStats() {
    const stats = await request("/api/stats");
    statsElement.textContent = `${stats.concepts} concepts · ${stats.relations} relations · format v${stats.formatVersion}`;
}

async function loadConcepts() {
    conceptsElement.textContent = "Loading…";
    try {
        const payload = await request("/api/concepts");
        conceptsElement.innerHTML = payload.concepts.map(concept => card(concept)).join("");
    } catch (error) {
        conceptsElement.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    }
}

async function search(query) {
    resultsElement.textContent = "Searching…";
    try {
        const payload = await request(`/api/search?q=${encodeURIComponent(query)}&limit=12`);
        resultsElement.innerHTML = payload.results.length
            ? payload.results.map(result => card(result.concept, result.score)).join("")
            : "<p>No matching concepts.</p>";
    } catch (error) {
        resultsElement.innerHTML = `<p class="error">${escapeHtml(error.message)}</p>`;
    }
}

form.addEventListener("submit", event => {
    event.preventDefault();
    const query = queryInput.value.trim();
    if (query) search(query);
});
reloadButton.addEventListener("click", loadConcepts);

Promise.all([loadStats(), loadConcepts()]).catch(error => {
    statsElement.textContent = error.message;
});
search(queryInput.value);
