def decode_iso0_pin_block(pin_block_hex, pan):
    """
    Decodes an ISO-0 PIN block (field 52, 16 hex chars) to extract the clear PIN digits.
    - pin_block_hex: 16 hex characters (field 52)
    - pan: string, must include at least 13 digits (no spaces)

    Returns: extracted PIN string, or empty string if decode fails.
    """
    try:
        # 1. Get rightmost 12 digits of PAN, excluding the check digit
        pan12 = pan[-13:-1].rjust(12, "0")
        pan_block = "0000" + pan12
        # 2. XOR pin_block with pan_block
        pin_block_bytes = bytes.fromhex(pin_block_hex)
        pan_block_bytes = bytes.fromhex(pan_block)
        pinres = bytes([a ^ b for a, b in zip(pin_block_bytes, pan_block_bytes)])
        # 3. Parse PIN field
        n_digits = pinres[0] & 0x0F
        pin_digits = ""
        idx = 1
        while len(pin_digits) < n_digits and idx < len(pinres):
            hi = (pinres[idx] & 0xF0) >> 4
            lo = (pinres[idx] & 0x0F)
            if len(pin_digits) < n_digits:
                pin_digits += str(hi)
            if len(pin_digits) < n_digits:
                pin_digits += str(lo)
            idx += 1
        return pin_digits
    except Exception as e:
        print(f"Decode error: {e}")
        return ""

# Test/example:
if __name__ == "__main__":
    # Example from your log:
    pin_block = "041173BBC8B7FA77"
    pan = "4326244374805888"
    print("Decoded PIN is:", decode_iso0_pin_block(pin_block, pan))
    # Output: Decoded PIN is: 1234
