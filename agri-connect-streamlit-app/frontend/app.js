/**
 * AgriConnect Web Application Logic (Version 2.1)
 * Enhanced with Dynamic OpenAI Market Discovery, Overhauled Voice Assistant,
 * Interactive Kisan AI Chatbot, and Agricultural Live Wallpaper.
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
  mapInstance: null,
  wallpaperActive: true,
  chatHistory: []
};

// Embedded fallback data in case /api/data is unreachable
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

// Application Bootstrapping
document.addEventListener("DOMContentLoaded", async () => {
  await loadData();
  setupNavigation();
  setupMobileDrawer();
  setupInputs();
  setupVoice();
  setupDynamicMandiDiscovery();
  setupChatbot();
  initLiveWallpaper();
  renderApp();
});

// Load Database
async function loadData() {
  try {
    const res = await fetch("/api/data");
    if (res.ok) {
      appData = await res.json();
      updateMarketDataStatus();
      return;
    }
  } catch (e) {
    // Try static data.json next
  }

  try {
    const res2 = await fetch("data.json");
    if (res2.ok) {
      appData = await res2.json();
      updateMarketDataStatus();
      return;
    }
  } catch (e2) {
    console.warn("Using embedded fallback data");
  }

  appData = FALLBACK_DATA;
  updateMarketDataStatus();
}

function updateMarketDataStatus() {
  const status = document.getElementById("market-data-status");
  if (!status || !appData) return;
  const date = appData.last_updated || "demo date";
  const source = appData.update_source || "demo database";
  status.textContent = `Market data checked daily · Updated ${date} · Source: ${source}`;
}

// Navigation Handling
function setupNavigation() {
  const navItems = document.querySelectorAll(".nav-item");
  navItems.forEach(item => {
    item.addEventListener("click", e => {
      e.preventDefault();
      const page = item.getAttribute("data-page");
      switchPage(page);
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

    locInput.addEventListener("keypress", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        discoverNearbyMandis();
      }
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

  const gradeSelect = document.getElementById("select-grade");
  if (gradeSelect) {
    gradeSelect.addEventListener("change", e => {
      state.selectedGrade = e.target.value;
      renderSellingPlan();
    });
  }

  document.querySelectorAll(".segment-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".segment-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.sellingPath = btn.getAttribute("data-path");
      renderSellingPlan();
    });
  });

  const accHeader = document.querySelector(".accordion-header");
  if (accHeader) {
    accHeader.addEventListener("click", () => {
      const body = document.querySelector(".accordion-body");
      body.classList.toggle("open");
    });
  }
}

/* ==========================================================
   DYNAMIC OPENAI & SPATIAL MANDI DISCOVERY
   ========================================================== */
function setupDynamicMandiDiscovery() {
  const btn = document.getElementById("btn-discover-mandis");
  if (btn) {
    btn.addEventListener("click", discoverNearbyMandis);
  }
}

async function discoverNearbyMandis() {
  const location = (state.location || "").trim();
  const btn = document.getElementById("btn-discover-mandis");
  const statusDiv = document.getElementById("mandi-discovery-status");

  if (!location) {
    showToast("Please enter a town or village name first!");
    return;
  }

  if (btn) {
    btn.classList.add("loading");
    btn.innerHTML = `<span>⏳</span> Searching...`;
  }

  if (statusDiv) {
    statusDiv.innerHTML = `<div class="mandi-discovery-badge" style="background:#eef6ea; color:#235d47;"><span>🔍</span> Finding nearest APMC mandis for ${location}...</div>`;
  }

  try {
    const res = await fetch("/api/market-lookup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({
        location: location,
        crop: state.selectedCrop,
      })
    });

    if (res.ok) {
      const result = await res.json();
      if (result.markets && result.markets.length > 0) {
        // Merge into current dataset without duplicates
        result.markets.forEach(newMarket => {
          const idx = appData.markets.findIndex(m => m.market.toLowerCase() === newMarket.market.toLowerCase());
          if (idx >= 0) {
            appData.markets[idx] = newMarket;
          } else {
            appData.markets.push(newMarket);
          }
        });

        if (result.rentals) {
          result.rentals.forEach(newRental => {
            const rIdx = appData.rentals.findIndex(r => r.market.toLowerCase() === newRental.market.toLowerCase());
            if (rIdx >= 0) {
              appData.rentals[rIdx] = newRental;
            } else {
              appData.rentals.push(newRental);
            }
          });
        }

        const sourceLabel = result.source === "openai" ? "OpenAI Intelligence" : "Agricultural Spatial Engine";
        if (statusDiv) {
          statusDiv.innerHTML = `<div class="mandi-discovery-badge"><span>✅</span> Added ${result.markets.length} Mandis near ${location} via ${sourceLabel}</div>`;
        }
        showToast(`Discovered ${result.markets.length} nearby markets!`);

        renderSellingPlan();
        if (state.currentPage === "market-map") {
          renderMarketMapPage();
        }
      }
    } else {
      if (statusDiv) statusDiv.innerHTML = "";
    }
  } catch (err) {
    console.warn("Market discovery lookup error:", err);
    if (statusDiv) statusDiv.innerHTML = "";
  } finally {
    if (btn) {
      btn.classList.remove("loading");
      btn.innerHTML = `<span>🔍</span> Discover Mandis`;
    }
  }
}

function jsonStringify(obj) {
  try {
    return JSON.stringify(obj);
  } catch (e) {
    return "{}";
  }
}

/* ==========================================================
   VOICE ASSISTANT (OVERHAULED & VISUALIZED)
   ========================================================== */
let voiceAnimId = null;

function setupVoice() {
  const micBtn = document.getElementById("btn-voice-record");
  const langSelect = document.getElementById("select-voice-lang");
  const voiceAlert = document.getElementById("voice-feedback-alert");
  const interimBox = document.getElementById("voice-interim-preview");
  const waveCanvas = document.getElementById("voice-waveform-canvas");

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
        showToast("Speech Recognition requires Chrome, Edge, or a browser with Web Speech API.");
      });
    }
    return;
  }

  let recognition = null;
  let isListening = false;

  function initRecognition() {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true; // Real-time words as you speak!

    recognition.onstart = () => {
      isListening = true;
      micBtn.classList.add("listening");
      micBtn.innerHTML = `<span>🔴</span> Listening... Speak now`;
      if (waveCanvas) {
        waveCanvas.style.display = "block";
        startWaveformAnimation(waveCanvas);
      }
      if (interimBox) {
        interimBox.style.display = "block";
        interimBox.innerHTML = `Listening in <strong>${state.voiceLanguage}</strong>...`;
      }
      if (voiceAlert) voiceAlert.style.display = "none";
    };

    recognition.onresult = event => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      if (interimBox && (interimTranscript || finalTranscript)) {
        interimBox.innerHTML = `Heard: "<strong>${finalTranscript || interimTranscript}</strong>"`;
      }

      if (finalTranscript) {
        state.voiceNote = finalTranscript;
        handleVoiceTranscript(finalTranscript);
      }
    };

    recognition.onerror = event => {
      stopListeningState();
      let msg = `Microphone notice (${event.error}).`;
      if (event.error === "not-allowed") {
        msg = "Microphone access was blocked. Please click the lock icon in your browser address bar to allow microphone access.";
      } else if (event.error === "no-speech") {
        msg = "No speech was detected. Please try tapping again and speaking closer to the mic.";
      }
      if (voiceAlert) {
        voiceAlert.className = "voice-alert info";
        voiceAlert.style.display = "block";
        voiceAlert.textContent = msg;
      }
    };

    recognition.onend = () => {
      stopListeningState();
    };
  }

  function stopListeningState() {
    isListening = false;
    if (micBtn) {
      micBtn.classList.remove("listening");
      micBtn.innerHTML = `<span>🎙️</span> Tap microphone to speak`;
    }
    if (waveCanvas) {
      waveCanvas.style.display = "none";
      if (voiceAnimId) cancelAnimationFrame(voiceAnimId);
    }
  }

  if (micBtn) {
    micBtn.addEventListener("click", () => {
      if (isListening) {
        if (recognition) recognition.stop();
        stopListeningState();
        return;
      }

      try {
        initRecognition();
        const langCode = (appData.voice.languages[state.voiceLanguage]) || "te-IN";
        recognition.lang = langCode;
        recognition.start();
      } catch (err) {
        console.warn("Speech recognition start issue:", err);
        stopListeningState();
      }
    });
  }
}

function startWaveformAnimation(canvas) {
  const ctx = canvas.getContext("2d");
  let step = 0;

  function renderWave() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = "#287a55";

    const width = canvas.width;
    const height = canvas.height;
    const midY = height / 2;

    for (let x = 0; x < width; x++) {
      const y = midY + Math.sin((x * 0.05) + step) * 12 * Math.sin((x * 0.01) + step * 0.5);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    step += 0.15;
    voiceAnimId = requestAnimationFrame(renderWave);
  }

  renderWave();
}

function handleVoiceTranscript(transcript) {
  const voiceAlert = document.getElementById("voice-feedback-alert");
  const detected = detectCropFromText(transcript);

  if (voiceAlert) {
    voiceAlert.style.display = "block";
    if (detected) {
      voiceAlert.className = "voice-alert success";
      voiceAlert.innerHTML = `✅ Heard: "<em>${transcript}</em>". Found <strong>${detected}</strong>! Updated prices below.`;
      state.selectedCrop = detected;
    } else {
      voiceAlert.className = "voice-alert info";
      voiceAlert.innerHTML = `ℹ️ Heard: "<em>${transcript}</em>". Choose your crop below to calculate prices.`;
    }
  }

  renderApp();
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
  const hints = appData.location_distance_hints || {};

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

  const gradeNote = document.getElementById("grade-note");
  if (gradeNote && appData.quality_grades[grade]) {
    gradeNote.textContent = `${appData.quality_grades[grade].description}. Prices below are adjusted for this grade.`;
  }

  // Calculate Market Prices & Best Option
  let marketsCalculated = appData.markets.map(m => {
    const price = applyQualityPrice((m.prices && m.prices[crop]) ? m.prices[crop] : 25, grade);
    const distance = getMarketDistance(m, userLoc);
    const rental = appData.rentals.find(r => r.market === m.market) || { daily_rent: 350, security_deposit: 800, landmark: m.landmarks || "APMC Yard" };
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

  marketsCalculated.sort((a, b) => b.estimatedShopNet - a.estimatedShopNet);
  const bestMarket = marketsCalculated.length > 0 ? marketsCalculated[0] : null;

  if (!bestMarket) return;

  // Calculate Buyers
  let matchingBuyers = appData.buyers.filter(b => b.crop === crop).map(b => {
    const adjustedPrice = applyQualityPrice(b.price, grade);
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

      recBanner.innerHTML = `<strong>Fair-price recommendation:</strong> ${recommendation} could leave about <strong>₹${recValue.toLocaleString("en-IN")} net</strong> for ${quantity.toLocaleString("en-IN")} kg after estimated travel and selling costs.`;
    } else {
      recBanner.innerHTML = `<strong>Estimated shop earning:</strong> ₹${bestMarket.estimatedShopNet.toLocaleString("en-IN")} net for ${quantity.toLocaleString("en-IN")} kg after estimated travel and 3 days of rent.`;
    }
  }

  // Render Selling Path
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
  const marketRentals = appData.rentals.filter(r => r.market === bestMarket.market);
  const shopSelect = document.getElementById("select-shop");
  const daysInput = document.getElementById("input-rental-days");

  if (!state.rentalShop || !marketRentals.some(r => r.shop === state.rentalShop)) {
    state.rentalShop = marketRentals.length > 0 ? marketRentals[0].shop : "";
  }

  if (shopSelect) {
    shopSelect.innerHTML = "";
    if (marketRentals.length === 0) {
      const opt = document.createElement("option");
      opt.value = "Stall A";
      opt.textContent = "Market Yard Stall (₹350/day)";
      shopSelect.appendChild(opt);
    } else {
      marketRentals.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r.shop;
        opt.textContent = `${r.shop} (₹${r.daily_rent}/day)`;
        if (r.shop === state.rentalShop) opt.selected = true;
        shopSelect.appendChild(opt);
      });
    }

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

  const selectedRental = marketRentals.find(r => r.shop === state.rentalShop) || marketRentals[0] || { daily_rent: 350, security_deposit: 800, landmark: bestMarket.landmarks || "Market Yard" };
  const dailyRent = selectedRental.daily_rent;
  const deposit = selectedRental.security_deposit;
  const amountToCarry = dailyRent * days + deposit;
  const finalShopNet = Math.round(bestMarket.adjustedPrice * quantity - dailyRent * days - transportCost * bestMarket.userDistance * 2);

  document.getElementById("metric-daily-rent").textContent = `₹${dailyRent.toLocaleString("en-IN")}`;
  document.getElementById("metric-deposit").textContent = `₹${deposit.toLocaleString("en-IN")}`;
  document.getElementById("metric-amount-carry").textContent = `₹${amountToCarry.toLocaleString("en-IN")}`;
  document.getElementById("metric-shop-net").textContent = `₹${finalShopNet.toLocaleString("en-IN")}`;

  document.getElementById("shop-landmark-info").innerHTML = `<strong>Landmark:</strong> ${selectedRental.landmark}<br><strong>Shop location:</strong> ${bestMarket.location} · ${bestMarket.userDistance} km from your location`;

  const btnDirections = document.getElementById("btn-directions");
  const btnViewMarket = document.getElementById("btn-view-market");

  const directionsUrl = `https://www.google.com/maps/dir/?api=1${userLoc ? `&origin=${encodeURIComponent(userLoc)}` : ""}&destination=${encodeURIComponent(bestMarket.location + " market")}`;
  const viewUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(bestMarket.location + " market")}`;

  btnDirections.href = directionsUrl;
  btnViewMarket.href = viewUrl;

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

  if (!state.mapInstance && window.L) {
    state.mapInstance = L.map("map-container").setView([16.30, 80.45], 8);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '© OpenStreetMap contributors'
    }).addTo(state.mapInstance);
  }

  if (state.mapInstance && window.L) {
    // Clear previous markers
    if (state.markerGroup) {
      state.markerGroup.clearLayers();
    } else {
      state.markerGroup = L.layerGroup().addTo(state.mapInstance);
    }

    const bounds = [];
    appData.markets.forEach(m => {
      if (m.latitude && m.longitude) {
        bounds.push([m.latitude, m.longitude]);
        const marker = L.marker([m.latitude, m.longitude]).addTo(state.markerGroup);
        marker.bindPopup(`
          <div style="font-family:'DM Sans',sans-serif;">
            <h4 style="margin:0 0 4px; color:#173b35;">${m.market}</h4>
            <p style="margin:0 0 6px; font-size:12px; color:#555;">${m.landmarks}</p>
            <a href="https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(m.location + " market")}" target="_blank" style="color:#287a55; font-weight:bold; font-size:12px;">Directions ↗</a>
          </div>
        `);
      }
    });

    if (bounds.length > 0) {
      state.mapInstance.fitBounds(bounds, { padding: [30, 30] });
    }

    setTimeout(() => {
      state.mapInstance.invalidateSize();
    }, 200);
  }

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

  renderRegionalVideos(state.location || "");
}

const REGIONAL_VIDEOS = {
  kurnool: { title: "Kurnool farming lessons", query: "Kurnool agriculture farmer market Telugu" },
  warangal: { title: "Warangal crop and mandi lessons", query: "Warangal agriculture farmer market Telugu" },
  rajahmundry: { title: "Godavari farming lessons", query: "Rajahmundry Godavari agriculture farmer Telugu" },
  anantapur: { title: "Anantapur dryland farming lessons", query: "Anantapur dryland farming farmer Telugu" },
  khammam: { title: "Khammam chilli market lessons", query: "Khammam chilli farming farmer Telugu" },
  default: { title: "Regional farmer learning", query: "Indian farmer crop market price Telugu" }
};

function renderRegionalVideos(location) {
  const container = document.getElementById("regional-videos");
  if (!container) return;
  const key = Object.keys(REGIONAL_VIDEOS).find((name) => name !== "default" && location.toLowerCase().includes(name)) || "default";
  const video = REGIONAL_VIDEOS[key];
  const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(video.query)}`;
  container.innerHTML = `<div class="video-card"><div class="video-art">▶</div><div><span class="section-kicker">${key === "default" ? "FARM LEARNING" : key.toUpperCase()}</span><h4>${video.title}</h4><p>Open a curated regional search for crop care, local markets, and farmer practices.</p><a class="btn btn-outline" target="_blank" rel="noopener" href="${searchUrl}">Watch regional lessons ↗</a></div></div>`;
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

/* ==========================================================
   KISAN AI CHATBOT ENGINE
   ========================================================== */
function setupChatbot() {
  const fab = document.getElementById("kisan-ai-fab");
  const chatWindow = document.getElementById("kisan-chat-window");
  const closeBtn = document.getElementById("btn-close-chat");
  const settingsBtn = document.getElementById("btn-chat-settings");
  const settingsOverlay = document.getElementById("chat-settings-overlay");
  const closeSettingsBtn = document.getElementById("btn-close-settings");
  const saveKeyBtn = document.getElementById("btn-save-key");
  const keyInput = document.getElementById("input-openai-key");
  const sendBtn = document.getElementById("btn-send-chat");
  const inputField = document.getElementById("input-chat-msg");
  const micChatBtn = document.getElementById("btn-chat-mic");

  if (keyInput) keyInput.disabled = true;

  // Toggle Chat Window
  if (fab && chatWindow) {
    fab.addEventListener("click", () => {
      chatWindow.style.display = chatWindow.style.display === "flex" ? "none" : "flex";
      if (chatWindow.style.display === "flex") {
        inputField.focus();
      }
    });
  }

  if (closeBtn && chatWindow) {
    closeBtn.addEventListener("click", () => {
      chatWindow.style.display = "none";
    });
  }

  // Toggle Settings Overlay
  if (settingsBtn && settingsOverlay) {
    settingsBtn.addEventListener("click", () => {
      settingsOverlay.classList.toggle("open");
    });
  }

  if (closeSettingsBtn && settingsOverlay) {
    closeSettingsBtn.addEventListener("click", () => {
      settingsOverlay.classList.remove("open");
    });
  }

  if (saveKeyBtn && keyInput) {
    saveKeyBtn.addEventListener("click", () => {
      showToast("AI keys are managed securely by the app administrator.");
      settingsOverlay.classList.remove("open");
    });
  }

  // Send Message Handlers
  if (sendBtn && inputField) {
    sendBtn.addEventListener("click", () => {
      sendChatMessage(inputField.value);
    });

    inputField.addEventListener("keypress", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendChatMessage(inputField.value);
      }
    });
  }

  // Quick chips
  document.querySelectorAll(".quick-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-query");
      sendChatMessage(q);
    });
  });

  // Voice to Chat
  if (micChatBtn) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const chatRec = new SpeechRecognition();
      chatRec.interimResults = false;
      let chatListening = false;

      micChatBtn.addEventListener("click", () => {
        if (chatListening) {
          chatRec.stop();
          return;
        }
        chatRec.lang = (appData.voice.languages[state.voiceLanguage]) || "en-IN";
        try {
          chatRec.start();
          chatListening = true;
          micChatBtn.classList.add("listening");
        } catch (e) {
          console.warn("Chat speech start error:", e);
        }
      });

      chatRec.onresult = event => {
        chatListening = false;
        micChatBtn.classList.remove("listening");
        const transcript = event.results[0][0].transcript;
        if (inputField) inputField.value = transcript;
        sendChatMessage(transcript);
      };

      chatRec.onerror = () => {
        chatListening = false;
        micChatBtn.classList.remove("listening");
      };

      chatRec.onend = () => {
        chatListening = false;
        micChatBtn.classList.remove("listening");
      };
    }
  }
}

async function sendChatMessage(text) {
  const msg = (text || "").trim();
  if (!msg) return;

  const container = document.getElementById("chat-messages-container");
  const inputField = document.getElementById("input-chat-msg");

  if (inputField) inputField.value = "";

  // Append User Bubble
  appendChatBubble(msg, "user");

  // Append Typing Bubble
  const typingBubble = document.createElement("div");
  typingBubble.className = "chat-bubble typing";
  typingBubble.innerHTML = `<span>🌱</span> Kisan AI is thinking...`;
  container.appendChild(typingBubble);
  container.scrollTop = container.scrollHeight;

  state.chatHistory.push({ role: "user", content: msg });

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonStringify({
        message: msg,
        history: state.chatHistory,
      })
    });

    typingBubble.remove();

    if (res.ok) {
      const data = await res.json();
      const reply = data.reply || "Namaste! I am here to help. Please ask your question again.";
      appendChatBubble(formatMarkdown(reply), "bot");
      state.chatHistory.push({ role: "assistant", content: reply });
    } else {
      appendChatBubble("I could not reach the network right now, but please ask again!", "bot");
    }
  } catch (err) {
    typingBubble.remove();
    appendChatBubble("Namaste! Please check your connection and ask again.", "bot");
  }
}

function appendChatBubble(htmlContent, type) {
  const container = document.getElementById("chat-messages-container");
  if (!container) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${type}`;
  bubble.innerHTML = htmlContent;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

function formatMarkdown(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/• /g, "<br>• ")
    .replace(/\n\n/g, "<br><br>")
    .replace(/\n/g, "<br>");
}

/* ==========================================================
   AGRICULTURAL LIVE WALLPAPER (CANVAS MOTION ENGINE)
   ========================================================== */
function initLiveWallpaper() {
  const canvas = document.getElementById("live-wallpaper-canvas");
  const toggleBtn = document.getElementById("btn-toggle-wallpaper");
  const statusText = document.getElementById("wallpaper-status-text");

  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let animationId = null;
  let particles = [];
  const particleCount = 28;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  resize();
  window.addEventListener("resize", resize);

  // Initialize floating golden pollen particles
  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      radius: Math.random() * 2.5 + 1.2,
      color: Math.random() > 0.4 ? "rgba(243, 179, 61, 0.45)" : "rgba(40, 122, 85, 0.25)",
      speedX: (Math.random() - 0.5) * 0.4 + 0.15,
      speedY: -Math.random() * 0.6 - 0.2, // Drifting upwards like morning field pollen
      phase: Math.random() * Math.PI * 2
    });
  }

  function draw() {
    if (!state.wallpaperActive) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Subtle golden morning sunbeam gradient at top-right
    const sunGlow = ctx.createRadialGradient(
      canvas.width * 0.85, canvas.height * 0.1, 10,
      canvas.width * 0.85, canvas.height * 0.1, canvas.width * 0.45
    );
    sunGlow.addColorStop(0, "rgba(243, 225, 157, 0.12)");
    sunGlow.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.fillStyle = sunGlow;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Render floating pollen
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.shadowColor = "rgba(243, 179, 61, 0.6)";
      ctx.shadowBlur = 4;
      ctx.fill();

      // Motion update
      p.x += p.speedX + Math.sin(p.phase) * 0.3;
      p.y += p.speedY;
      p.phase += 0.02;

      // Wrap around screen boundaries
      if (p.y < -10) {
        p.y = canvas.height + 10;
        p.x = Math.random() * canvas.width;
      }
      if (p.x > canvas.width + 10) p.x = -10;
      if (p.x < -10) p.x = canvas.width + 10;
    });

    animationId = requestAnimationFrame(draw);
  }

  draw();

  // Pause when tab is not visible to conserve battery
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      if (animationId) cancelAnimationFrame(animationId);
    } else if (state.wallpaperActive) {
      draw();
    }
  });

  // Toggle button handler
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      state.wallpaperActive = !state.wallpaperActive;
      canvas.style.opacity = state.wallpaperActive ? "0.85" : "0";
      if (statusText) statusText.textContent = state.wallpaperActive ? "ON" : "ECO";
      if (state.wallpaperActive) {
        draw();
        showToast("Live Wallpaper: Activated 🌿");
      } else {
        if (animationId) cancelAnimationFrame(animationId);
        showToast("Live Wallpaper: Eco Mode 🍃");
      }
    });
  }
}
