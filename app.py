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
    "The app will tell you whether its numeric value is **greater than 2**, **less than 2**, or **equal to 2**. "
    "It can also handle **very large hexadecimal values** and display their **scientific notation**."
)

# -------------------------------
# User Input
# -------------------------------
hex_input = st.text_input(
    "Enter Hex Value",
    placeholder="e.g. 0x1A, FF, or a very large hex like f2e3447a8ee9a2be1ce33aa8b4964becc13586fcdb9eec1656428809cdb58d29"
)

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

        # Shorten long hex for display
        hex_str = hex_input.strip().lower().replace("0x", "")
        if len(hex_str) > 30:
            short_hex = f"{hex_str[:15]}...{hex_str[-15:]}"
        else:
            short_hex = hex_str

        # Convert to scientific notation if large
        if abs(value) >= 1e10:
            sci_notation = f"{value:.4e}"
        else:
            sci_notation = "Not applicable (small number)"

        # Display information
        st.write(f"**Decimal Value:** `{value}`")
        st.write(f"**Scientific Notation:** `{sci_notation}`")
        st.write(f"**Hex (trimmed for display):** `{short_hex}`")
        st.write(f"**Number of Hex Digits:** `{len(hex_str)}`")
        st.write(f"**Bit Length:** `{value.bit_length()} bits`")

        # Comparison logic
        if value > 2:
            st.success("✅ The value is **greater than 2**.")
        elif value < 2:
            st.info("ℹ️ The value is **less than 2**.")
        else:
            st.warning("⚠️ The value is **equal to 2**.")

        st.write("---")

        # Show binary representation only for manageable lengths
        if value.bit_length() <= 256:
            st.write(f"**Binary Representation:** `{bin(value)[2:]}`")
        else:
            st.write("🧮 Binary representation too large to display fully.")
            st.code(f"{bin(value)[:100]}... (truncated)", language="text")

        st.caption("✅ Python supports arbitrarily large integers — no overflow errors!")

    except ValueError as e:
        st.error(f"❌ Invalid input: {e}")
else:
    st.write("👆 Enter a hex value above to see the result.")


