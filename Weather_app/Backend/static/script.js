document.getElementById("getWeatherBtn").addEventListener("click", getWeather);

async function getWeather() {
  const city = document.getElementById("cityInput").value;
  const days = document.getElementById("daysInput").value || 1;

  if (!city) {
    alert("Please enter a city name!");
    return;
  }

  const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}&days=${days}`);
  const data = await res.json();

  if (data.error) {
    document.getElementById("output").textContent = "Error: " + data.error;
  } else {
    document.getElementById("output").textContent = JSON.stringify(data, null, 2);
  }
}