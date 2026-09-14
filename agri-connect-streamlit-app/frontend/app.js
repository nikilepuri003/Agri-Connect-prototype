/**
 * AgriConnect Web Application Logic
 * Implements interactive calculations, dynamic views, voice input, and map visualization.
 */

// Global Application State
let appData = null;
let state = {
  currentPage: "selling-plan",
  location: "",
  quantity: 500,
  transportCost: 12,
  selectedCrop: "Tomato",
  selectedGrade: "Standard grade",
  sellingPath: "shop",
  rentalShop: "",
  rentalDays: 3,
  voiceLanguage: "Telugu",
  detectedCrop: null,
  voiceNote: "",
  mapInstance: null
};

// Embedded fallback data in case /api/data is unreachable (e.g. opening index.html directly from filesystem)
const FALLBACK_DATA = {
  crops: {
    "Tomato": { "icon": "🍅", "unit": "₹/kg" },
    "Chilli": { "icon": "🌶️", "unit": "₹/kg" },
    "Rice": { "icon": "🌾", "unit": "₹/kg" },
    "Cotton": { "icon": "☁️", "unit": "₹/kg" },
    "Wheat": { "icon": "🌱", "unit": "₹/kg" }
  },
  quality_grades: {
    "Premium grade": { "adjustment": 1.12, "description": "Clean, fresh, uniform produce" },
    "Standard grade": { "adjustment": 1.00, "description": "Good market-ready produce" },
    "Value grade": { "adjustment": 0.88, "description": "Mixed size or lower visual quality" }
  },
  markets: [
    { "market": "Guntur Market", "location": "Guntur", "latitude": 16.3067, "longitude": 80.4365, "prices": { "Tomato": 22, "Chilli": 105, "Rice": 32, "Cotton": 68, "Wheat": 30 }, "distance": 5, "landmarks": "NTR Bus Stand · Guntur Railway Station" },
    { "market": "Vijayawada Market", "location": "Vijayawada", "latitude": 16.5062, "longitude": 80.6480, "prices": { "Tomato": 25, "Chilli": 115, "Rice": 35, "Cotton": 72, "Wheat": 33 }, "distance": 35, "landmarks": "Benz Circle · Vijayawada Railway Station" },
    { "market": "Tenali Market", "location": "Tenali", "latitude": 16.2430, "longitude": 80.6400, "prices": { "Tomato": 23, "Chilli": 110, "Rice": 33, "Cotton": 70, "Wheat": 31 }, "distance": 30, "landmarks": "Tenali Railway Station · Clock Tower" },
    { "market": "Narasaraopet Market", "location": "Narasaraopet", "latitude": 16.2342, "longitude": 80.0490, "prices": { "Tomato": 24, "Chilli": 108, "Rice": 31, "Cotton": 69, "Wheat": 29 }, "distance": 45, "landmarks": "Narasaraopet Railway Station · Palnadu Road" },
    { "market": "Bapatla Market", "location": "Bapatla", "latitude": 15.9042, "longitude": 80.4670, "prices": { "Tomato": 21, "Chilli": 102, "Rice": 34, "Cotton": 71, "Wheat": 32 }, "distance": 50, "landmarks": "Bapatla Beach Road · Railway Station" }
  ],
  rentals: [
    { "market": "Guntur Market", "shop": "Vegetable lane A", "daily_rent": 450, "security_deposit": 1200, "landmark": "Near NTR Bus Stand" },
    { "market": "Vijayawada Market", "shop": "Fresh produce lane 3", "daily_rent": 650, "security_deposit": 1800, "landmark": "Near Benz Circle" },
    { "market": "Tenali Market", "shop": "Farmer row 2", "daily_rent": 350, "security_deposit": 900, "landmark": "Near Clock Tower" },
    { "market": "Narasaraopet Market", "shop": "Main yard stall 8", "daily_rent": 300, "security_deposit": 750, "landmark": "Near Railway Station" },
    { "market": "Bapatla Market", "shop": "Coastal market row 1", "daily_rent": 275, "security_deposit": 700, "landmark": "Near Beach Road" }
  ],
  location_distance_hints: {
    "mangalagiri": { "Guntur": 28, "Vijayawada": 18, "Tenali": 35, "Narasaraopet": 70, "Bapatla": 65 },
    "tenali": { "Guntur": 30, "Vijayawada": 32, "Tenali": 3, "Narasaraopet": 68, "Bapatla": 38 },
    "guntur": { "Guntur": 5, "Vijayawada": 35, "Tenali": 30, "Narasaraopet": 45, "Bapatla": 50 },
    "vijayawada": { "Guntur": 35, "Vijayawada": 5, "Tenali": 32, "Narasaraopet": 65, "Bapatla": 75 },
    "bapatla": { "Guntur": 50, "Vijayawada": 75, "Tenali": 38, "Narasaraopet": 85, "Bapatla": 5 },
    "narasaraopet": { "Guntur": 45, "Vijayawada": 65, "Tenali": 68, "Narasaraopet": 5, "Bapatla": 85 }
  },
  buyers: [
    { "buyer": "ABC Vegetables", "crop": "Tomato", "price": 24, "quantity": "500–2,000 kg", "location": "Vijayawada", "type": "Fresh produce retailer" },
    { "buyer": "FreshMart", "crop": "Tomato", "price": 23, "quantity": "500–1,500 kg", "location": "Guntur", "type": "Supermarket chain" },
    { "buyer": "Agro Foods Ltd", "crop": "Chilli", "price": 118, "quantity": "1,000–5,000 kg", "location": "Vijayawada", "type": "Food processor" },
    { "buyer": "Sri Lakshmi Traders", "crop": "Rice", "price": 36, "quantity": "2,000–10,000 kg", "location": "Tenali", "type": "Grain wholesaler" },
    { "buyer": "FarmFresh Pvt Ltd", "crop": "Cotton", "price": 73, "quantity": "1,000–5,000 kg", "location": "Guntur", "type": "Textile supplier" },
    { "buyer": "Green Valley", "crop": "Wheat", "price": 35, "quantity": "500–3,000 kg", "location": "Bapatla", "type": "Flour mill" },
    { "buyer": "Organic Harvest", "crop": "Tomato", "price": 22, "quantity": "1,000–4,000 kg", "location": "Narasaraopet", "type": "Organic grocer" },
    { "buyer": "City Farmers Market", "crop": "Chilli", "price": 115, "quantity": "2,000–8,000 kg", "location": "Guntur", "type": "Local market collective" }
  ],
  voice: {
    languages: {
      "English": "en-IN",
      "Hindi": "hi-IN",
      "Telugu": "te-IN",
      "Tamil": "ta-IN",
      "Kannada": "kn-IN",
      "Malayalam": "ml-IN",
      "Marathi": "mr-IN",
      "Bengali": "bn-IN",
      "Any other language": "en-IN"
    },
    crop_words: {
      "tomato": "Tomato", "టమాటా": "Tomato", "tamatar": "Tomato",
      "chilli": "Chilli", "chili": "Chilli", "mirchi": "Chilli", "మిర్చి": "Chilli",
      "rice": "Rice", "paddy": "Rice", "biyyam": "Rice", "బియ్యం": "Rice",
      "cotton": "Cotton", "kapas": "Cotton", "పత్తి": "Cotton",
      "wheat": "Wheat", "gehun": "Wheat", "గోధుమ": "Wheat"
    }
  }
};

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  setupNavigation();
  setupMobileDrawer();
  setupInputs();
  setupVoice();
  renderApp();
});

// Load Database
async function loadData() {
  try {
    const res = await fetch("/api/data");
    if (res.ok) {
      appData = await res.json();
      return;
    }
  } catch (e) {
    // Try static data.json next
  }

  try {
    const res2 = await fetch("data.json");
    if (res2.ok) {
      appData = await res2.json();
      return;
    }
  } catch (e2) {
    console.warn("Using embedded fallback data");
  }

  appData = FALLBACK_DATA;
}

// Navigation Handling
function setupNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", e => {
      e.preventDefault();
      const page = item.getAttribute("data-page");
      switchPage(page);
      
      // Close mobile drawer if open
      document.querySelector(".sidebar").classList.remove("open");
    });
  });
}

function setupMobileDrawer() {
  const toggleBtn = document.getElementById("mobile-menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });
  }
}

function switchPage(page) {
  state.currentPage = page;
  document.querySelectorAll(".nav-item").forEach(el => {
    el.classList.toggle("active", el.getAttribute("data-page") === page);
  });

  document.querySelectorAll(".page-view").forEach(view => {
    view.style.display = "none";
  });

  const activeView = document.getElementById(`view-${page}`);
  if (activeView) {
    activeView.style.display = "block";
  }

  if (page === "market-map") {
    renderMarketMapPage();
  } else if (page === "buyer-offers") {
    renderBuyerOffersPage();
  } else {
    renderSellingPlan();
  }
}

// Inputs and Form Handlers
function setupInputs() {
  const locInput = document.getElementById("input-location");
  const qtyInput = document.getElementById("input-quantity");
  const costInput = document.getElementById("input-transport");

  if (locInput) {
    locInput.addEventListener("input", e => {
      state.location = e.target.value.trim();
      renderSellingPlan();
    });
  }

  if (qtyInput) {
    qtyInput.addEventListener("input", e => {
      state.quantity = Math.max(1, parseFloat(e.target.value) || 1);
      renderSellingPlan();
    });
  }

  if (costInput) {
    costInput.addEventListener("input", e => {
      state.transportCost = Math.max(0, parseFloat(e.target.value) || 0);
      renderSellingPlan();
    });
  }

  // Quality grade change
  const gradeSelect = document.getElementById("select-grade");
  if (gradeSelect) {
    gradeSelect.addEventListener("change", e => {
      state.selectedGrade = e.target.value;
      renderSellingPlan();
    });
  }

  // Selling path segmented control
  document.querySelectorAll(".segment-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".segment-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.sellingPath = btn.getAttribute("data-path");
      renderSellingPlan();
    });
  });

  // Accordion toggle
  const accHeader = document.querySelector(".accordion-header");
  if (accHeader) {
    accHeader.addEventListener("click", () => {
      const body = document.querySelector(".accordion-body");
      body.classList.toggle("open");
    });
  }
}

// Voice Assistant with Web Speech API
function setupVoice() {
  const micBtn = document.getElementById("btn-voice-record");
  const langSelect = document.getElementById("select-voice-lang");
  const voiceAlert = document.getElementById("voice-feedback-alert");

  // Populate voice languages
  if (langSelect && appData && appData.voice) {
    langSelect.innerHTML = "";
    Object.keys(appData.voice.languages).forEach(lang => {
      const opt = document.createElement("option");
      opt.value = lang;
      opt.textContent = lang;
      if (lang === "Telugu") opt.selected = true;
      langSelect.appendChild(opt);
    });

    langSelect.addEventListener("change", e => {
      state.voiceLanguage = e.target.value;
    });
  }

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    if (micBtn) {
      micBtn.addEventListener("click", () => {
        showToast("Web Speech is not supported in this browser. Please type below.");
      });
    }
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  let isListening = false;

  if (micBtn) {
    micBtn.addEventListener("click", () => {
      if (isListening) {
        recognition.stop();
        return;
      }

      const langCode = (appData.voice.languages[state.voiceLanguage]) || "en-IN";
      recognition.lang = langCode;

      try {
        recognition.start();
        isListening = true;
        micBtn.classList.add("listening");
        micBtn.innerHTML = `<span>🔴</span> Listening... Tap to stop`;
      } catch (err) {
        console.error("Speech recognition error:", err);
      }
    });

    recognition.onresult = event => {
      isListening = false;
      micBtn.classList.remove("listening");
      micBtn.innerHTML = `<span>🎙️</span> Tap microphone to speak`;

      const transcript = event.results[0][0].transcript;
      state.voiceNote = transcript;
      handleVoiceTranscript(transcript);
    };

    recognition.onerror = event => {
      isListening = false;
      micBtn.classList.remove("listening");
      micBtn.innerHTML = `<span>🎙️</span> Tap microphone to speak`;
      if (voiceAlert) {
        voiceAlert.className = "voice-alert info";
        voiceAlert.style.display = "block";
        voiceAlert.textContent = `Microphone notice: ${event.error}. You can continue typing below.`;
      }
    };

    recognition.onend = () => {
      isListening = false;
      micBtn.classList.remove("listening");
      micBtn.innerHTML = `<span>🎙️</span> Tap microphone to speak`;
    };
  }
}

function handleVoiceTranscript(transcript) {
  const voiceAlert = document.getElementById("voice-feedback-alert");
  const detected = detectCropFromText(transcript);

  if (voiceAlert) {
    voiceAlert.style.display = "block";
    if (detected) {
      voiceAlert.className = "voice-alert success";
      voiceAlert.innerHTML = `✅ Heard: "<em>${transcript}</em>". Found <strong>${detected}</strong>! Prices are updated below.`;
      state.selectedCrop = detected;
    } else {
      voiceAlert.className = "voice-alert info";
      voiceAlert.innerHTML = `ℹ️ Heard: "<em>${transcript}</em>". Pick your crop below to view prices.`;
    }
  }

  renderSellingPlan();
}

function detectCropFromText(text) {
  if (!text || !appData || !appData.voice) return null;
  const lowered = text.toLowerCase();
  for (const [word, crop] of Object.entries(appData.voice.crop_words)) {
    if (lowered.includes(word.toLowerCase())) {
      return crop;
    }
  }
  return null;
}

// Distance Calculation Helpers
function getMarketDistance(market, userLocation) {
  if (!userLocation) return market.distance;
  const lowerLoc = userLocation.toLowerCase();
  const hints = appData.location_distance_hints;

  for (const [key, distMap] of Object.entries(hints)) {
    if (lowerLoc.includes(key)) {
      if (distMap[market.location] !== undefined) {
        return distMap[market.location];
      }
    }
  }
  return market.distance;
}

function applyQualityPrice(basePrice, grade) {
  const adj = appData.quality_grades[grade] ? appData.quality_grades[grade].adjustment : 1.0;
  return Math.round(basePrice * adj * 100) / 100;
}

// Core Rendering Engine
function renderApp() {
  renderCropPills();
  renderQualityOptions();
  renderSellingPlan();
}

function renderCropPills() {
  const container = document.getElementById("crop-pills-container");
  if (!container || !appData) return;

  container.innerHTML = "";
  Object.entries(appData.crops).forEach(([cropName, meta]) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `pill-btn ${state.selectedCrop === cropName ? "active" : ""}`;
    btn.innerHTML = `<span>${meta.icon}</span> <span>${cropName}</span>`;
    btn.addEventListener("click", () => {
      state.selectedCrop = cropName;
      renderCropPills();
      renderSellingPlan();
    });
    container.appendChild(btn);
  });
}

function renderQualityOptions() {
  const select = document.getElementById("select-grade");
  if (!select || !appData) return;

  select.innerHTML = "";
  Object.keys(appData.quality_grades).forEach(grade => {
    const opt = document.createElement("option");
    opt.value = grade;
    opt.textContent = grade;
    if (grade === state.selectedGrade) opt.selected = true;
    select.appendChild(opt);
  });
}

function renderSellingPlan() {
  if (!appData || state.currentPage !== "selling-plan") return;

  const crop = state.selectedCrop;
  const grade = state.selectedGrade;
  const quantity = state.quantity;
  const transportCost = state.transportCost;
  const userLoc = state.location;

  // Grade description
  const gradeNote = document.getElementById("grade-note");
  if (gradeNote && appData.quality_grades[grade]) {
    gradeNote.textContent = `${appData.quality_grades[grade].description}. Prices below are adjusted for this grade.`;
  }

  // Calculate Market Prices & Best Option
  let marketsCalculated = appData.markets.map(m => {
    const price = applyQualityPrice(m.prices[crop] || 0, grade);
    const distance = getMarketDistance(m, userLoc);
    const rental = appData.rentals.find(r => r.market === m.market) || { daily_rent: 400 };
    const defaultDays = 3;
    const estimatedShopNet = Math.round(price * quantity - rental.daily_rent * defaultDays - transportCost * distance * 2);

    return {
      ...m,
      adjustedPrice: price,
      userDistance: distance,
      rental: rental,
      estimatedShopNet: estimatedShopNet
    };
  });

  // Sort by Estimated Shop Net descending
  marketsCalculated.sort((a, b) => b.estimatedShopNet - a.estimatedShopNet);
  const bestMarket = marketsCalculated[0];

  // Calculate Buyers for this crop
  let matchingBuyers = appData.buyers.filter(b => b.crop === crop).map(b => {
    const adjustedPrice = applyQualityPrice(b.price, grade);
    // Find distance to buyer location
    const matchedMarket = marketsCalculated.find(m => m.location.toLowerCase() === b.location.toLowerCase());
    const buyerDistance = matchedMarket ? matchedMarket.userDistance : bestMarket.userDistance;
    const netEarning = Math.round(adjustedPrice * quantity - transportCost * buyerDistance * 2);

    return {
      ...b,
      adjustedPrice: adjustedPrice,
      distance: buyerDistance,
      netEarning: netEarning
    };
  });

  matchingBuyers.sort((a, b) => b.netEarning - a.netEarning);
  const bestBuyer = matchingBuyers.length > 0 ? matchingBuyers[0] : null;

  // Update 3 Metrics Cards
  document.getElementById("metric-fair-price").textContent = `₹${bestMarket.adjustedPrice.toFixed(2)}/kg`;
  document.getElementById("metric-best-market").textContent = bestMarket.location;
  document.getElementById("metric-distance").textContent = `${bestMarket.userDistance} km`;

  // Recommendation Banner
  const recBanner = document.getElementById("recommendation-banner");
  if (recBanner) {
    if (bestBuyer) {
      const shopNet = bestMarket.estimatedShopNet;
      const buyerNet = bestBuyer.netEarning;
      const recommendation = shopNet >= buyerNet ? "Rent a shop" : `Sell to ${bestBuyer.buyer}`;
      const recValue = Math.max(shopNet, buyerNet);

      recBanner.innerHTML = `<strong>Fair-price recommendation:</strong> ${recommendation} could leave about <strong>₹${recValue.toLocaleString("en-IN")} net</strong> for ${quantity.toLocaleString("en-IN")} kg after estimated travel and selling costs. This compares nearby options, not only the highest quote.`;
    } else {
      recBanner.innerHTML = `<strong>Estimated shop earning:</strong> ₹${bestMarket.estimatedShopNet.toLocaleString("en-IN")} net for ${quantity.toLocaleString("en-IN")} kg after estimated travel and 3 days of rent.`;
    }
  }

  // Render Selling Path (Shop vs Buyer)
  const shopContainer = document.getElementById("selling-path-shop");
  const buyerContainer = document.getElementById("selling-path-buyer");

  if (state.sellingPath === "shop") {
    shopContainer.style.display = "block";
    buyerContainer.style.display = "none";
    renderShopPath(bestMarket, marketsCalculated, quantity, transportCost, userLoc);
  } else {
    shopContainer.style.display = "none";
    buyerContainer.style.display = "block";
    renderBuyerPath(matchingBuyers);
  }
}

function renderShopPath(bestMarket, allMarkets, quantity, transportCost, userLoc) {
  // Available shops for best market
  const marketRentals = appData.rentals.filter(r => r.market === bestMarket.market);
  const shopSelect = document.getElementById("select-shop");
  const daysInput = document.getElementById("input-rental-days");

  if (!state.rentalShop || !marketRentals.some(r => r.shop === state.rentalShop)) {
    state.rentalShop = marketRentals.length > 0 ? marketRentals[0].shop : "";
  }

  if (shopSelect) {
    shopSelect.innerHTML = "";
    marketRentals.forEach(r => {
      const opt = document.createElement("option");
      opt.value = r.shop;
      opt.textContent = `${r.shop} (₹${r.daily_rent}/day)`;
      if (r.shop === state.rentalShop) opt.selected = true;
      shopSelect.appendChild(opt);
    });

    shopSelect.onchange = e => {
      state.rentalShop = e.target.value;
      renderShopPath(bestMarket, allMarkets, quantity, transportCost, userLoc);
    };
  }

  const days = parseInt(daysInput.value) || state.rentalDays;
  state.rentalDays = days;

  daysInput.oninput = e => {
    state.rentalDays = Math.max(1, Math.min(31, parseInt(e.target.value) || 1));
    renderShopPath(bestMarket, allMarkets, quantity, transportCost, userLoc);
  };

  const selectedRental = marketRentals.find(r => r.shop === state.rentalShop) || marketRentals[0] || { daily_rent: 400, security_deposit: 1000, landmark: "Market yard" };
  const dailyRent = selectedRental.daily_rent;
  const deposit = selectedRental.security_deposit;
  const amountToCarry = dailyRent * days + deposit;
  const finalShopNet = Math.round(bestMarket.adjustedPrice * quantity - dailyRent * days - transportCost * bestMarket.userDistance * 2);

  document.getElementById("metric-daily-rent").textContent = `₹${dailyRent.toLocaleString("en-IN")}`;
  document.getElementById("metric-deposit").textContent = `₹${deposit.toLocaleString("en-IN")}`;
  document.getElementById("metric-amount-carry").textContent = `₹${amountToCarry.toLocaleString("en-IN")}`;
  document.getElementById("metric-shop-net").textContent = `₹${finalShopNet.toLocaleString("en-IN")}`;

  document.getElementById("shop-landmark-info").innerHTML = `<strong>Landmark:</strong> ${selectedRental.landmark}<br><strong>Shop location:</strong> ${bestMarket.location} · ${bestMarket.userDistance} km from your location`;

  // Route Buttons
  const btnDirections = document.getElementById("btn-directions");
  const btnViewMarket = document.getElementById("btn-view-market");

  const directionsUrl = `https://www.google.com/maps/dir/?api=1${userLoc ? `&origin=${encodeURIComponent(userLoc)}` : ""}&destination=${encodeURIComponent(bestMarket.location + " market")}`;
  const viewUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(bestMarket.location + " market")}`;

  btnDirections.href = directionsUrl;
  btnViewMarket.href = viewUrl;

  // Render Market Comparison Table
  const tableBody = document.querySelector("#market-comparison-table tbody");
  if (tableBody) {
    tableBody.innerHTML = "";
    allMarkets.forEach(m => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${m.market}</strong></td>
        <td>${m.location}</td>
        <td>₹${m.adjustedPrice.toFixed(2)}</td>
        <td>${m.userDistance} km</td>
        <td><strong>₹${m.estimatedShopNet.toLocaleString("en-IN")}</strong></td>
        <td>${m.landmarks}</td>
      `;
      tableBody.appendChild(tr);
    });
  }
}

function renderBuyerPath(buyers) {
  const container = document.getElementById("buyers-list-container");
  if (!container) return;

  container.innerHTML = "";
  if (buyers.length === 0) {
    container.innerHTML = `<div class="info-note">No direct buyers are listed for this crop yet.</div>`;
    return;
  }

  buyers.forEach(buyer => {
    const card = document.createElement("div");
    card.className = "buyer-card";
    card.innerHTML = `
      <div class="buyer-info">
        <h4>${buyer.buyer}</h4>
        <p>${buyer.type} · ${buyer.location} · Required: ${buyer.quantity}</p>
      </div>
      <div class="buyer-pricing">
        <div class="price-tag">₹${buyer.adjustedPrice}/kg</div>
        <div class="net-tag">Net: ₹${buyer.netEarning.toLocaleString("en-IN")}</div>
      </div>
      <button class="btn btn-primary" onclick="connectWithBuyer('${buyer.buyer}')">
        <span>📞</span> Connect
      </button>
    `;
    container.appendChild(card);
  });
}

function connectWithBuyer(buyerName) {
  showToast(`Request sent to ${buyerName}!`);
}

function showToast(message) {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `<span>🌾</span> ${message}`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Market Map Page
function renderMarketMapPage() {
  if (!appData) return;

  const mapDiv = document.getElementById("map-container");
  if (!mapDiv) return;

  // Initialize Leaflet map if not already done
  if (!state.mapInstance && window.L) {
    state.mapInstance = L.map("map-container").setView([16.30, 80.45], 9);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(state.mapInstance);

    // Add markers for each market
    appData.markets.forEach(m => {
      const marker = L.marker([m.latitude, m.longitude]).addTo(state.mapInstance);
      marker.bindPopup(`
        <div style="font-family:'DM Sans',sans-serif;">
          <h4 style="margin:0 0 4px; color:#173b35;">${m.market}</h4>
          <p style="margin:0 0 6px; font-size:12px; color:#555;">${m.landmarks}</p>
          <a href="https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(m.location + " market")}" target="_blank" style="color:#287a55; font-weight:bold; font-size:12px;">Directions ↗</a>
        </div>
      `);
    });
  } else if (state.mapInstance) {
    setTimeout(() => {
      state.mapInstance.invalidateSize();
    }, 150);
  }

  // Render market cards list
  const list = document.getElementById("map-markets-list");
  if (list) {
    list.innerHTML = "";
    appData.markets.forEach(m => {
      const card = document.createElement("div");
      card.className = "buyer-card";
      card.innerHTML = `
        <div class="buyer-info">
          <h4>${m.market}</h4>
          <p>${m.distance} km away · Landmarks: ${m.landmarks}</p>
        </div>
        <div class="btn-row" style="margin:0;">
          <a href="https://www.google.com/maps/dir/?api=1${state.location ? `&origin=${encodeURIComponent(state.location)}` : ""}&destination=${encodeURIComponent(m.location + " market")}" target="_blank" class="btn btn-primary">
            Directions ↗
          </a>
          <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(m.location + " market")}" target="_blank" class="btn btn-outline">
            View Market
          </a>
        </div>
      `;
      list.appendChild(card);
    });
  }
}

// Buyer Offers Page
function renderBuyerOffersPage() {
  if (!appData) return;

  const cropSelect = document.getElementById("select-buyer-page-crop");
  if (cropSelect && cropSelect.children.length === 0) {
    Object.keys(appData.crops).forEach(crop => {
      const opt = document.createElement("option");
      opt.value = crop;
      opt.textContent = crop;
      cropSelect.appendChild(opt);
    });

    cropSelect.addEventListener("change", () => {
      updateBuyerPageTable(cropSelect.value);
    });
  }

  updateBuyerPageTable(cropSelect ? cropSelect.value : "Tomato");
}

function updateBuyerPageTable(selectedCrop) {
  const tableBody = document.querySelector("#all-buyers-table tbody");
  if (!tableBody || !appData) return;

  const offers = appData.buyers.filter(b => b.crop === selectedCrop);
  tableBody.innerHTML = "";

  offers.forEach(b => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong>${b.buyer}</strong></td>
      <td>₹${b.price}/kg</td>
      <td>${b.quantity}</td>
      <td>${b.location}</td>
      <td>${b.type}</td>
    `;
    tableBody.appendChild(tr);
  });
}

