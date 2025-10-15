import streamlit as st

# -------------------------------
# Streamlit App Configuration
# -------------------------------
st.set_page_config(page_title="Hex Comparator", page_icon="🔢", layout="centered")

# -------------------------------
# Title and Instructions
# -------------------------------
st.title("🔢 Hex Value Comparator")
st.write(
    "Enter a hexadecimal value (e.g. `0x1A`, `1A`, or `FF`). "
    "The app will tell you whether its numeric value is **greater than 2**, **less than 2**, or **equal to 2**."
)

# -------------------------------
# User Input
# -------------------------------
hex_input = st.text_input("Enter Hex Value", placeholder="e.g. 0x1A or FF")

# -------------------------------
# Helper Function
# -------------------------------
def parse_hex(s: str):
    """Convert hex string to integer with validation."""
    if not s:
        raise ValueError("Input cannot be empty.")
    s = s.strip()

    # Allow optional + or - sign
    sign = 1
    if s[0] in ['+', '-']:
        if s[0] == '-':
            sign = -1
        s = s[1:]

    # Remove optional 0x prefix
    if s.lower().startswith("0x"):
        s = s[2:]

    # Validate hex digits
    allowed = set("0123456789abcdefABCDEF")
    if not all(ch in allowed for ch in s):
        raise ValueError(f"Invalid hex digits: '{s}'")

    # Convert to integer
    return sign * int(s, 16)

# -------------------------------
# Main Logic
# -------------------------------
if hex_input:
    try:
        value = parse_hex(hex_input)
        st.write(f"**Decimal Value:** `{value}`")
        st.write(f"**Normalized Hex:** `0x{abs(value):X}`")

        if value > 2:
            st.success("✅ The value is **greater than 2**.")
        elif value < 2:
            st.info("ℹ️ The value is **less than 2**.")
        else:
            st.warning("⚠️ The value is **equal to 2**.")

        st.write("---")
        st.write(f"**Binary Representation:** `{bin(value)[2:] if value >= 0 else '-' + bin(abs(value))[2:]}`")

    except ValueError as e:
        st.error(f"❌ Invalid input: {e}")
else:
    st.write("👆 Enter a hex value above to see the result.")

st.caption("Built with ❤️ using Streamlit. Run locally with: `streamlit run app.py`")
