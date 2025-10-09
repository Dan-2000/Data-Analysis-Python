  async function getWeather() {
      const city = document.getElementById("city").value.trim();
      if (!city) return alert("Please enter a city");

      const res = await fetch(`/api/weather?city=${city}`);
      const data = await res.json();
      const out = document.getElementById("output");

      if (data.error) {
        out.innerHTML = `<p style="color:red;">${data.error}</p>`;
        return;
      }

      let html = `<h3>Weather for ${data.city}</h3><ul>`;
      for (let i = 0; i < 10; i++) {
        html += `<li>${data.time[i]} → ${data.temperature_2m[i].toFixed(1)}°C</li>`;
      }
      html += "</ul>";
      out.innerHTML = html;