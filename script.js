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
    document.getElementById("message").textContent = "Error: " + data.error;
    document.getElementById("carousel").style.display = "none";
  } else {
    document.getElementById("message").textContent = "";
    buildCarousel(data.forecast);
    document.getElementById("carousel").style.display = "block";
  }
}

function buildCarousel(forecast) {
  const slidesContainer = document.querySelector(".slides");
  slidesContainer.innerHTML = "";

  const indicatorsContainer = document.querySelector(".indicators");
  indicatorsContainer.innerHTML = "";

  const hoursPerSlide = 10;
  let currentSlide = 0;

  const totalSlides = Math.ceil(forecast.length / hoursPerSlide);

  for (let i = 0; i < forecast.length; i += hoursPerSlide) {
    const slide = document.createElement("div");
    slide.className = "slide";

    for (let j = i; j < i + hoursPerSlide && j < forecast.length; j++) {
      const hourData = forecast[j];
      const date = new Date(hourData.date);
      const dateStr = date.toLocaleDateString();
      const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      const temp = Math.round(hourData.temperature * 10) / 10; // round to 1 decimal

      const hourDiv = document.createElement("div");
      hourDiv.className = "hour";
      hourDiv.innerHTML = `<div>${dateStr}</div><div>${time}</div><div>${temp}°C</div>`;
      slide.appendChild(hourDiv);
    }

    slidesContainer.appendChild(slide);
  }

  // Create indicators
  for (let k = 0; k < totalSlides; k++) {
    const indicator = document.createElement("span");
    indicator.className = "indicator";
    if (k === 0) indicator.classList.add("active");
    indicator.addEventListener("click", () => {
      currentSlide = k;
      updateSlide();
      updateIndicators();
    });
    indicatorsContainer.appendChild(indicator);
  }

  // Add navigation
  const prevBtn = document.querySelector(".prev");
  const nextBtn = document.querySelector(".next");

  function updateSlide() {
    slidesContainer.style.transform = `translateX(-${currentSlide * 100}%)`;
  }

  function updateIndicators() {
    const indicators = document.querySelectorAll(".indicator");
    indicators.forEach((ind, index) => {
      if (index === currentSlide) {
        ind.classList.add("active");
      } else {
        ind.classList.remove("active");
      }
    });
  }

  prevBtn.addEventListener("click", () => {
    currentSlide = (currentSlide > 0) ? currentSlide - 1 : totalSlides - 1;
    updateSlide();
    updateIndicators();
  });

  nextBtn.addEventListener("click", () => {
    currentSlide = (currentSlide < totalSlides - 1) ? currentSlide + 1 : 0;
    updateSlide();
    updateIndicators();
  });
}