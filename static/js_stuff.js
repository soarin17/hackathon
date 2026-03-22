async function searchStock() {
    const symbol = document.getElementById("symbol").value.toUpperCase();
    const resultDiv = document.getElementById("result");

    resultDiv.classList.remove("visible");
    resultDiv.innerHTML = "Loading...";
    resultDiv.classList.add("visible");

    try {
        const res = await fetch(`/stock/${symbol}`);
        const data = await res.json();

        if (data.error) {
            resultDiv.innerHTML = `<p style="color:#e05555;">Error: ${data.error}</p>`;
            return;
        }

        resultDiv.innerHTML = `
            <h2>${data.symbol}</h2>
            <div class="price">$${data.price}</div>
            <h3>AI Analysis</h3>
            <p>${data.ai_analysis}</p>
        `;

    } catch (err) {
        resultDiv.innerHTML = `<p style="color:#e05555;">Error loading data.</p>`;
        console.error(err);
    }
}