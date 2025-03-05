import qrcode
from PIL import Image, ImageDraw, ImageFont

def validate_upi_id(upi_id):
    return "@" in upi_id and len(upi_id) >= 5

def validate_amount(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False

# Get user inputs
upi_id = input("Enter your UPI ID: ")

# Validate UPI ID
while not validate_upi_id(upi_id):
    print("Invalid UPI ID! Please enter a valid one.")
    upi_id = input("Enter your UPI ID: ")

recipient_name = input("Enter recipient name: ")  # Used in QR data and displayed as text below QR

amount = input("Enter the amount to be paid: ₹")

# Validate amount
while not validate_amount(amount):
    print("Invalid amount! Please enter a numeric value.")
    amount = input("Enter the amount to be paid: ₹")

# Create UPI payment URL (Includes recipient name)
google_pay_url = f'upi://pay?pa={upi_id}&pn={recipient_name}&am={amount}&cu=INR'

# Generate QR Code
google_pay_qr = qrcode.make(google_pay_url)

# Function to add recipient name and amount text below the QR code
def add_text_to_qr(qr_image, recipient_name, amount):
    # Convert the QR code to an editable image
    qr_image = qr_image.convert("RGB")
    
    try:
        font = ImageFont.truetype("/Library/Fonts/DejaVuSans.ttf", 40)
    except IOError:
        print("Font not found. Falling back to default font.")
        font = ImageFont.load_default()
    
    # Text to add
    text_1 = f"{recipient_name}"  # Recipient name
    text_2 = f"₹{amount}"  # Amount
    
    # Calculate text height
    line_height = font.getsize("A")[1]
    text_height = (line_height * 2) + 30  # Adjust padding as needed
    
    img_width, img_height = qr_image.size
    new_height = img_height + text_height
    
    # Create a new blank image with extra space for text
    new_image = Image.new("RGB", (img_width, new_height), "white")
    new_image.paste(qr_image, (0, 0))
    
    draw = ImageDraw.Draw(new_image)
    
    # Calculate text positions
    text_width_1, _ = draw.textsize(text_1, font=font)
    text_width_2, _ = draw.textsize(text_2, font=font)
    
    text_position_1 = ((img_width - text_width_1) // 2, img_height + 10)
    text_position_2 = ((img_width - text_width_2) // 2, img_height + line_height + 20)
    
    # Draw text
    draw.text(text_position_1, text_1, font=font, fill="black")
    draw.text(text_position_2, text_2, font=font, fill="black")
    
    return new_image

# Add recipient name and amount text below the QR code
google_pay_qr_with_text = add_text_to_qr(google_pay_qr, recipient_name, amount)

# Display the QR code with text
google_pay_qr_with_text.show()

print("QR code with recipient name and amount has been generated.")