async function searchStock() {
    const symbol = document.getElementById("symbol").value.toUpperCase();
    const resultDiv = document.getElementById("result");

    resultDiv.innerHTML = "Loading...";

    try {
        const res = await fetch(`/stock/${symbol}`);
        const data = await res.json();

        if (data.error) {
            resultDiv.innerHTML = "Error: " + data.error;
            return;
        }

        let eventsHtml = "<ul>";
        for (const event of data.events) {
            eventsHtml += `<li>${event}</li>`;
        }
        eventsHtml += "</ul>";

        resultDiv.innerHTML = `
            <h2>${symbol}</h2>
            <p>Price: $${data.price}</p>
            <p>Prediction: ${data.prediction}</p>
            <h3>Big Events:</h3>
            ${eventsHtml}
        `;

    } catch (err) {
        resultDiv.innerHTML = "Error loading data.";
        console.error(err);
    }
}