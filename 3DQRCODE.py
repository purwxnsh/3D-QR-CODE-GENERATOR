import streamlit as st
import qrcode
import qrcode.image.svg
from PIL import Image
import io

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="3D QR Code Generator | Major Project",
    page_icon="✨",
    layout="centered"
)

# ----------------- Custom CSS -----------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        }
        h1, h2, h3, h4 {
            color: #ffdd59;
            text-align: center;
        }
        .card {
            background: rgba(255,255,255,0.15);
            padding: 20px;
            margin: 10px 0;
            border-radius: 15px;
            box-shadow: 0px 6px 15px rgba(0,0,0,0.3);
        }
        .stTextInput, .stSelectbox, .stButton>button, .stDownloadButton>button {
            border-radius: 12px;
            border: none;
            padding: 10px 15px;
            font-size: 16px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
        }
        .stButton>button {
            background: linear-gradient(135deg, #00ff99, #00ccff);
            color: black;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.07);
            box-shadow: 0px 6px 20px rgba(0,0,0,0.6);
        }
        .stDownloadButton>button {
            background: linear-gradient(135deg, #ff9966, #ff5e62);
            color: white;
            font-weight: bold;
        }
        footer {
            text-align: center;
            margin-top: 40px;
            color: #ddd;
            font-size: 14px;
        }
        .brand {
    color: #FF0000;
    font-weight: bold;
    animation: glow 1.5s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 5px #FF0000, 0 0 10px #FF0000; }
    to { text-shadow: 0 0 20px #FF0000, 0 0 30px #FF0000; }
}


    </style>
""", unsafe_allow_html=True)


# ----------------- Sidebar Navigation -----------------
st.sidebar.title("📂 Navigation")
menu = st.sidebar.radio("Go to", ["🎨 Generate QR", "🏠 Home", "👩‍💻 Developer"])

# ----------------- HOME -----------------
if menu == "🏠 Home":
    st.markdown("<h1>✨ 3D QR Code Generator ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>A modern & beautiful QR code generator built with Python and Streamlit.</p>", unsafe_allow_html=True)

    st.markdown("### 🚀 Features")
    st.markdown("""
    <div class="card">
    ✅ Generate QR Codes for URL, Text, WiFi, and Contacts <br>
    ✅ Customize colors, size, background <br>
    ✅ Download in PNG, SVG, PDF formats <br>
    ✅ 3D glassmorphism design with animations <br>
    ✅ Easy-to-use & ready for project submission
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Use Cases")
    st.markdown("""
    <div class="card">
    🔗 Share links quickly <br>
    📶 Save WiFi details <br>
    📇 Digital business cards (vCard) <br>
    📑 Event tickets / product packaging <br>
    🎓 Academic Major Project demonstration
    </div>
    """, unsafe_allow_html=True)

# ----------------- GENERATE QR -----------------
elif menu == "🎨 Generate QR":
    st.markdown("<h2>🎨 Generate Your QR Code</h2>", unsafe_allow_html=True)

    qr_type = st.selectbox("🔖 Select QR Code Type", ["URL", "Text", "WiFi", "Contact (vCard)"])

    data = ""
    if qr_type == "URL":
        data = st.text_input("🌐 Enter URL")
    elif qr_type == "Text":
        data = st.text_area("✍️ Enter Text")
    elif qr_type == "WiFi":
        ssid = st.text_input("📶 WiFi SSID")
        password = st.text_input("🔑 WiFi Password", type="password")
        data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    elif qr_type == "Contact (vCard)":
        name = st.text_input("👤 Name")
        phone = st.text_input("📞 Phone")
        email = st.text_input("📧 Email ID")
        data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"

    file_name = st.text_input("📂 File name", "myqrcode")

    col1, col2, col3 = st.columns(3)
    with col1:
        size = st.slider("⚖️ Size", 5, 20, 10)
    with col2:
        fill_color = st.color_picker("🎨 QR Color (RGB)", "#000000")
    with col3:
        bg_color = st.color_picker("🖼 Background (RGB)", "#ffffff")

    if st.button("🚀 Generate QR Code"):
        if data.strip() != "":
            qr = qrcode.QRCode(box_size=size, border=3)
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color=fill_color, back_color=bg_color)

            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            buf.seek(0)

            st.success("✅ QR Code Generated Successfully!")
            st.image(buf, caption="Here is your QR Code", width=300)

            colA, colB, colC = st.columns(3)
            with colA:
                st.download_button("⬇️ Download PNG", data=buf, file_name=f"{file_name}.png", mime="image/png")

            factory = qrcode.image.svg.SvgImage
            svg_img = io.BytesIO()
            qrcode.make(data, image_factory=factory).save(svg_img)
            with colB:
                st.download_button("⬇️ Download SVG", data=svg_img.getvalue(), file_name=f"{file_name}.svg", mime="image/svg+xml")

            pdf_img = io.BytesIO()
            qr_img.save(pdf_img, format="PDF")
            pdf_img.seek(0)
            with colC:
                st.download_button("⬇️ Download PDF", data=pdf_img, file_name=f"{file_name}.pdf", mime="application/pdf")
        else:
            st.warning("⚠️ Please enter required details!")


# ----------------- DEVELOPER -----------------
elif menu == "👩‍💻 Developer":
    st.markdown("<h2>👩‍💻 Developer Info</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    👩‍🎓 Name: PURWANSH CHAUDHARY <br>
    🎓 Course: Data Analyst <br>
    🏫 Institute: AGASTYAAN TECHNOLOGY <br>
    📧 Email: purwanshchaudhary@gmail.com <br>
    🌐 Social Media: https://www.instagram.com/purwxnsh <br><br>
    🎨 <span class="brand">PURWANSH CHAUDHARY</span>
    </div>
    """, unsafe_allow_html=True)

# ----------------- Footer -----------------

st.markdown("<footer>© 2025 3D QR Code Generator Project | <span class='brand'>Design by PURWANSH CHAUDAHRY</span> | Made with ❤️ in Python & Streamlit</footer>", unsafe_allow_html=True)


