const API_URL = "/workspaces/Data-Analysis-Python/Weather_app/Backend/app.py";
async function fetchWeather() {
  const city = document.querySelector("#cityInput").value;
  const days = document.querySelector("#daysInput").value || 1;

  const response = await fetch(`${API_URL}?city=${city}&days=${days}`);
  const data = await response.json();

  console.log(data);
  document.querySelector("#output").innerHTML = `
    <h2>${data.city}</h2>
    <p>Timezone: ${data.timezone_abbr}</p>
    <ul>
      ${data.forecast
        .slice(0, 6)
        .map(f => `<li>${f.date}: ${f.temperature}°C</li>`)
        .join("")}
    </ul>
  `;
}
