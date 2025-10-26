import streamlit as st

# ---------- User Storage ----------
if "users" not in st.session_state:
    st.session_state.users = {}

# ---------- Page Tracking ----------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- Property Storage ----------
# ---------- Property Storage ----------
if "properties" not in st.session_state:
    st.session_state.properties = []

# ---------- Sample properties for testing ----------
if not st.session_state.properties:
    st.session_state.properties = [
        {
            "name": "Sunny Apartments",
            "location": "hyderabad",
            "price": 5000000,
            "bedrooms": 3,
            "amenities": ["Pool", "Gym"]
        },
        {
            "name": "Green Villa",
            "location": "vizag",
            "price": 12000000,
            "bedrooms": 5,
            "amenities": ["Garden", "Parking"]
        },
        {
            "name": "Cozy Plot",
            "location": "bengulore",
            "price": 3000000,
            "bedrooms": 0,
            "amenities": []
        }
    ]

# ---------- Function to change page ----------
def go_to(page):
    st.session_state.page = page

# ---------- Dark Theme & Styles ----------
st.markdown(
    """
    <style>
    .stApp {background-color: #1c1c1c; color: #ffffff; font-family: 'Segoe UI', sans-serif;}
    .title {color: #ffffff; text-align: center;}
    .subheader {color: #cccccc; text-align: center;}
    .stButton>button {background-color: #3498db; color: white; height: 3em; width: 8em; border-radius: 10px; border: none; font-size: 16px;}
    .stTextInput>div>div>input {background-color: #2c2c2c; color: #ffffff;}
    .stNumberInput>div>div>input {background-color: #2c2c2c; color: #ffffff;}
    .stSelectbox>div>div>div>select {background-color: #2c2c2c; color: #ffffff;}
    .stMultiselect>div>div>div {background-color: #2c2c2c; color: #ffffff;}
    .stSlider>div>div>div>div {background-color: #2c2c2c; color: #ffffff;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Home Page ----------------
if st.session_state.page == "home":
    st.markdown("<h1 class='title'>🏠 Real Estate Location Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Find the best locations for your real estate investments with ease!</p>", unsafe_allow_html=True)

    st.image(
        "https://images.unsplash.com/photo-1598300056820-1c25aa9d6c60?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxMTc3M3wwfDF8c2VhcmNofDR8fHJlYWwlMjBlc3RhdGUlMjBob21lfGVufDB8fHx8MTY5ODA2NzA1MQ&ixlib=rb-4.0.3&q=80&w=800",
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Get Started"):
        go_to("signup")

# ---------------- Sign Up Page ----------------
elif st.session_state.page == "signup":
    st.markdown("<h1 class='title'>📝 Create an Account</h1>", unsafe_allow_html=True)
    new_user = st.text_input("Username", placeholder="Enter a unique username")
    new_pass = st.text_input("Password", type="password", placeholder="Enter a strong password")

    if st.button("Sign Up"):
        if new_user in st.session_state.users:
            st.error("❌ User already exists!")
        elif new_user == "" or new_pass == "":
            st.warning("⚠️ Please fill in both fields")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("✅ Account created successfully!")
            st.info("Go to Login page to access your account")
            go_to("login")

    if st.button("Back to Home"):
        go_to("home")

# ---------------- Login Page ----------------
elif st.session_state.page == "login":
    st.markdown("<h1 class='title'>🔑 Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.success(f"Welcome {username}! 🎉")
            go_to("role_selection")
        else:
            st.error("❌ Invalid username or password")

    if st.button("Back to Home"):
        go_to("home")

# ---------------- Role Selection Page ----------------
elif st.session_state.page == "role_selection":
    st.markdown("<h1 class='title'>👤 Select Your Role</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Choose whether you are a Property Manager or a Buyer</p>", unsafe_allow_html=True)

    role = st.radio("Select Role:", ["Property Manager", "Buyer"])

    if st.button("Continue"):
        if role == "Property Manager":
            go_to("manager_page")
        else:
            go_to("buyer_page")

# ---------------- Property Manager Page ----------------
elif st.session_state.page == "manager_page":
    st.markdown("<h1 class='title'>🏢 Property Manager Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Add or update your property details</p>", unsafe_allow_html=True)

    property_name = st.text_input("Property Name")
    location = st.text_input("Location")
    price = st.number_input("Price (₹)", min_value=100000)
    bedrooms = st.slider("Bedrooms", 1, 10)
    amenities = st.multiselect("Amenities", ["Pool", "Gym", "Parking", "Garden"])

    if st.button("Add/Update Property"):
        st.session_state.properties.append({
            "name": property_name,
            "location": location,
            "price": price,
            "bedrooms": bedrooms,
            "amenities": amenities
        })
        st.success("✅ Property details updated successfully!")

# ---------------- Buyer Page ----------------
elif st.session_state.page == "buyer_page":
    st.markdown("<h1 class='title'>🏘️ Available Properties</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Filter and view property details shared by Property Managers</p>", unsafe_allow_html=True)


    if st.session_state.properties:
        # --- Filters ---
        locations = list({prop['location'] for prop in st.session_state.properties})
        locations.sort()
        selected_location = st.selectbox("Filter by Location:", ["All"] + locations)

        min_price = min(prop['price'] for prop in st.session_state.properties)
        max_price = max(prop['price'] for prop in st.session_state.properties)
        selected_price = st.slider("Filter by Price (₹):", min_price, max_price, (min_price, max_price))

        min_bedrooms = min(prop['bedrooms'] for prop in st.session_state.properties)
        max_bedrooms = max(prop['bedrooms'] for prop in st.session_state.properties)
        selected_bedrooms = st.slider("Filter by Bedrooms:", min_bedrooms, max_bedrooms, (min_bedrooms, max_bedrooms))

        all_amenities = ["Pool", "Gym", "Parking", "Garden"]
        selected_amenities = st.multiselect("Filter by Amenities:", all_amenities)

        # --- Display filtered properties ---
        filtered_properties = []
        for prop in st.session_state.properties:
            if (selected_location == "All" or prop['location'] == selected_location) and \
               (selected_price[0] <= prop['price'] <= selected_price[1]) and \
               (selected_bedrooms[0] <= prop['bedrooms'] <= selected_bedrooms[1]) and \
               all(amenity in prop['amenities'] for amenity in selected_amenities):
                filtered_properties.append(prop)

        if filtered_properties:
            for prop in filtered_properties:
                st.write(f"**Property Name:** {prop['name']}")
                st.write(f"**Location:** {prop['location']}")
                st.write(f"**Price:** ₹{prop['price']}")
                st.write(f"**Bedrooms:** {prop['bedrooms']}")
                st.write(f"**Amenities:** {', '.join(prop['amenities'])}")
                st.markdown("---")
        else:
            st.info("No properties match your filters.")
    else:
        st.info("No properties available yet.")


# ---------------- Real Estate Predictor Page ----------------
elif st.session_state.page == "predictor":
    st.markdown("<h1 class='title'>📍 Real Estate Location Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subheader'>Enter your preferences to find the best location for investment</p>", unsafe_allow_html=True)

    budget = st.number_input("Budget (₹)", min_value=100000, step=50000)
    property_type = st.selectbox("Property Type", ["Apartment", "Villa", "Plot"])
    bedrooms = st.slider("Number of Bedrooms", 1, 5)
    location_preference = st.text_input("Preferred Location (optional)")
    amenities = st.multiselect("Amenities", ["Pool", "Gym", "Parking", "Garden"])

    if st.button("Predict Location"):
        predicted_location = "Downtown, CityX"  # Placeholder for ML model
        st.success(f"Recommended Location: {predicted_location}")
