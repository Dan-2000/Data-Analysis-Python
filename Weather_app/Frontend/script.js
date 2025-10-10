async function getWeather() {
  const city = document.getElementById("city").value;
  const days = document.getElementById("days").value || 1;
  const response = await fetch(`/api/weather?city=${city}&days=${days}`);
  const data = await response.json();

  if (data.error) {
    document.getElementById("output").innerText = data.error;
    return;
  }

  let html = `<h2>${data.city}</h2><ul>`;
  for (let f of data.forecast.slice(0, 10)) {
    html += `<li>${f.date} → ${f.temperature.toFixed(1)}°C</li>`;
  }
  html += "</ul>";
  document.getElementById("output").innerHTML = html;
}
