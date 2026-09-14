from __future__ import annotations

import streamlit as st

from .data import BUYERS, CROPS, MARKETS, QUALITY_GRADES, RENTALS, apply_quality_price, distances_from, market_rows
from .maps import google_maps_directions_url, google_maps_url, render_market_map
from .voice import crop_from_voice, render_voice_input


def inject_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root { --ink:#173b35; --leaf:#287a55; --sun:#f3b33d; --paper:#fbf8ef; --line:#d9e4d4; }
        .stApp { background:linear-gradient(135deg,#f8f4e5 0%,#edf5e6 52%,#dbe9d8 100%); color:var(--ink); }
        .stApp, .stApp p, .stApp label, [data-testid='stMarkdownContainer'] { font-family:'DM Sans',sans-serif; }
        h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:var(--ink) !important; }
        [data-testid='stSidebar'] { background:linear-gradient(180deg,#173b35,#235d47); }
        [data-testid='stSidebar'] * { color:#f8f4e6 !important; }
        .hero { position:relative; isolation:isolate; overflow:hidden; min-height:250px; padding:2rem 2.2rem; border:1px solid rgba(209,187,122,.75); border-radius:20px; background:linear-gradient(100deg,rgba(255,252,239,.97) 0%,rgba(255,252,239,.93) 48%,rgba(243,225,157,.25) 100%); box-shadow:0 18px 38px rgba(38,75,48,.13); }
        .hero-copy { position:relative; z-index:2; max-width:64%; }
        .eyebrow { color:#a06419; font-weight:700; letter-spacing:.08em; text-transform:uppercase; font-size:.76rem; }
        .hero h1 { margin:.35rem 0 .4rem; font-size:2.45rem; word-break:normal; overflow-wrap:normal; hyphens:none; }
        .hero p { max-width:560px; }
        .farmer-frame { position:absolute; right:2.3rem; bottom:0; width:215px; height:222px; border:8px solid rgba(255,252,239,.78); border-bottom:0; border-radius:108px 108px 0 0; background:#718a62; box-shadow:0 14px 0 rgba(23,59,53,.1),0 18px 32px rgba(23,59,53,.2); overflow:hidden; }
        .farmer-photo { display:block; width:100%; height:100%; object-fit:cover; object-position:center; filter:saturate(1.08) contrast(1.03); }
        @media (max-width:700px) { .hero { min-height:360px; padding:1.5rem; } .hero-copy { max-width:100%; } .hero h1 { font-size:2.15rem; } .farmer-frame { right:50%; transform:translateX(50%); width:170px; height:176px; } }
        .choice { padding:1rem 1.15rem; border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.63); min-height:132px; }
        .choice-icon { font-size:2rem; }
        div[data-testid='stMetric'] { background:rgba(255,255,255,.6); border:1px solid var(--line); padding:1rem; border-radius:14px; }
        .stButton>button { border-radius:10px; font-weight:700; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar() -> str:
    with st.sidebar:
        st.markdown("# 🌾 AgriConnect")
        st.caption("Your simple path from field to fair price")
        page = st.radio("Go to", ["My selling plan", "Market map", "Buyer offers"], label_visibility="collapsed")
        st.markdown("---")
        st.caption("Built for voice-first farm decisions")
    return page


def render_header() -> None:
    st.markdown(
        '<div class="hero"><div class="hero-copy"><div class="eyebrow">Today\'s selling desk</div><h1>Sell with confidence.</h1><p>Find a nearby market, compare today\'s prices, and choose the path that works best for your harvest.</p></div><div class="farmer-frame" aria-hidden="true"><img class="farmer-photo" src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=700&q=85" alt="Farmer working in a green field"></div></div>',
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    render_header()
    st.write("")
    location_col, quantity_col, transport_col = st.columns(3)
    current_location = location_col.text_input(
        "Your current village or location",
        placeholder="Example: Mangalagiri, Andhra Pradesh",
        key="current_location",
    )
    quantity = quantity_col.number_input("Harvest quantity (kg)", min_value=1, value=500, step=50, key="harvest_quantity")
    transport_cost = transport_col.number_input("Transport cost per km (₹)", min_value=0, value=12, step=1, key="transport_cost")
    voice_text = ""
    with st.expander("🎙️ Speak instead of typing", expanded=False):
        voice_text = render_voice_input()
    detected_crop = crop_from_voice(voice_text) if voice_text else None
    if voice_text:
        if detected_crop:
            st.success(f"I found **{detected_crop}** in your voice note, so its prices are ready below.")
        else:
            st.info(f"Your voice note: {voice_text}. Choose the crop below so I can show its data.")
    st.subheader("What are you selling?")
    crop_options = list(CROPS)
    crop = st.pills(
        "Choose your crop",
        crop_options,
        format_func=lambda item: f"{CROPS[item]['icon']} {item}",
        default=detected_crop,
        key="crop_choice",
    )
    if not crop:
        st.caption("Pick one crop to see its best price and nearby selling choices.")
        return

    grade_col, grade_note_col = st.columns([1, 2])
    grade = grade_col.selectbox("Crop quality grade", list(QUALITY_GRADES), key="quality_grade")
    grade_note_col.info(f"{QUALITY_GRADES[grade]['description']}. Prices below are adjusted for this grade.")
    rows = market_rows(crop)
    rows["Price (₹/kg)"] = rows["Price (₹/kg)"].map(lambda price: apply_quality_price(price, grade))
    distances = distances_from(current_location)
    rows["Your distance (km)"] = rows["Location"].map(distances).fillna(rows["Distance (km)"])
    days = 3
    rows["Estimated shop net"] = rows.apply(
        lambda market: market["Price (₹/kg)"] * quantity
        - RENTALS.loc[RENTALS["Market"] == market["Market"], "Daily rent"].iloc[0] * days
        - transport_cost * market["Your distance (km)"] * 2,
        axis=1,
    )
    best = rows.loc[rows["Estimated shop net"].idxmax()]
    rental_options = RENTALS[RENTALS["Market"] == best["Market"]]
    rental_details = rental_options.iloc[0]
    shop_net = int(best["Estimated shop net"])
    offers = BUYERS[BUYERS["Crop"] == crop].copy()
    if not offers.empty:
        offers["Distance"] = offers["Location"].map(distances).fillna(best["Your distance (km)"])
        offers["Price"] = offers["Price"].map(lambda price: apply_quality_price(price, grade))
        offers["Net earning"] = offers["Price"] * quantity - transport_cost * offers["Distance"] * 2
        best_buyer = offers.loc[offers["Net earning"].idxmax()]
        buyer_net = int(best_buyer["Net earning"])
    else:
        best_buyer = None
        buyer_net = 0
    st.write("")
    metrics = st.columns(3)
    metrics[0].metric("Fair price for grade", f"₹{best['Price (₹/kg)']:.2f}/kg")
    metrics[1].metric("Best nearby market", best["Location"])
    metrics[2].metric("Your distance", f"{best['Your distance (km)']} km")
    if best_buyer is not None:
        recommendation = "Rent a shop" if shop_net >= buyer_net else f"Sell to {best_buyer['Buyer']}"
        recommendation_value = max(shop_net, buyer_net)
        st.info(f"**Fair-price recommendation:** {recommendation} could leave about **₹{recommendation_value:,} net** for {quantity:,} kg after estimated travel and selling costs. This compares nearby options, not only the highest quote.")
    else:
        st.info(f"**Estimated shop earning:** ₹{shop_net:,} net for {quantity:,} kg after estimated travel and 3 days of rent.")
    st.subheader("Choose how you want to sell")
    choice = st.segmented_control("Selling path", ["🏪 Rent a shop", "🤝 Sell to a buyer"], default="🏪 Rent a shop", key="selling_path")
    if choice == "🏪 Rent a shop":
        st.success(f"A shop at {best['Market']} could help you sell directly at ₹{best['Price (₹/kg)']:.2f}/kg for {grade.lower()}.")
        rental = st.selectbox("Choose a shop", rental_options["Shop"].tolist(), key="rental_shop")
        rental_details = rental_options[rental_options["Shop"] == rental].iloc[0]
        days = st.number_input("How many days will you sell?", min_value=1, max_value=31, value=3, step=1, key="rental_days")
        shop_net = int(best["Price (₹/kg)"] * quantity - rental_details["Daily rent"] * days - transport_cost * best["Your distance (km)"] * 2)
        rent_col, deposit_col, total_col = st.columns(3)
        rent_col.metric("Daily rent", f"₹{rental_details['Daily rent']:,}")
        deposit_col.metric("Refundable deposit", f"₹{rental_details['Security deposit']:,}")
        total_col.metric("Amount to carry", f"₹{int(rental_details['Daily rent'] * days + rental_details['Security deposit']):,}")
        st.metric("Estimated net earning", f"₹{shop_net:,}", help="Gross crop sale minus rent and estimated round-trip transport. Deposit is refundable and not subtracted.")
        st.markdown(f"**Landmark:** {rental_details['Landmark']}  \n**Shop location:** {best['Location']} · {best['Your distance (km)']} km from your location")
        st.link_button("Open route from my location", google_maps_directions_url(best["Location"], current_location), icon=":material/directions:")
        st.link_button("Open this market in Google Maps", google_maps_url(best["Location"]), icon=":material/map:")
        st.dataframe(rows, width="stretch", hide_index=True)
    else:
        offers = offers.sort_values("Net earning", ascending=False)
        if offers.empty:
            st.info("No direct buyers are listed for this crop yet.")
        else:
            for _, buyer in offers.iterrows():
                with st.container(border=True):
                    details = st.columns([2, 1, 1])
                    details[0].markdown(f"**{buyer['Buyer']}**  \n{buyer['Type']} · {buyer['Location']}")
                    details[1].markdown(f"**₹{buyer['Price']}/kg**  \nNet: ₹{int(buyer['Net earning']):,}")
                    if details[2].button("Connect", key=f"connect_{buyer['Buyer']}", icon=":material/phone:"):
                        st.toast(f"Request sent to {buyer['Buyer']}")


def render_map_page() -> None:
    st.title("Market map")
    st.write("See markets, roads, and familiar landmarks before you leave the farm.")
    render_market_map()
    for _, market in MARKETS.iterrows():
        with st.container(border=True):
            left, right = st.columns([3, 1])
            left.markdown(f"**{market['Market']}** · {market['Distance']} km away  \nLandmarks: {market['Landmarks']}")
            right.link_button("Directions", google_maps_directions_url(market["Location"], st.session_state.get("current_location", "")), icon=":material/directions:")
            right.link_button("View market", google_maps_url(market["Location"]), icon=":material/map:")


def render_buyers_page() -> None:
    st.title("Buyer offers")
    st.write("Compare direct buyers by crop, offer, quantity, and location.")
    crop = st.selectbox("Filter by crop", list(CROPS))
    offers = BUYERS[BUYERS["Crop"] == crop]
    st.dataframe(offers[["Buyer", "Price", "Quantity", "Location", "Type"]], width="stretch", hide_index=True)


def run() -> None:
    inject_theme()
    page = sidebar()
    if page == "My selling plan":
        render_dashboard()
    elif page == "Market map":
        render_map_page()
    else:
        render_buyers_page()