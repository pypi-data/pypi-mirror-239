def generate_images_pdf(
        images_list,
        pdf_file_path: str,
        images_labels_list=None,
        images_per_row: int = 3,
):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from PIL import Image

    # Set up the PDF canvas
    page_width, page_height = letter
    margin = 0.125 * inch
    image_width = (page_width - 2 * margin) / images_per_row
    image_height = image_width

    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Calculate the horizontal gap between images
    horizontal_gap = (page_width - 2 * margin - images_per_row * image_width) / (images_per_row - 1)
    vertical_gap = (0.5 * inch) if images_labels_list else (0.125 * inch)

    # # Iterate over the QR code images and arrange them in the PDF
    # x = margin
    # y = page_height - margin

    for i, qr_image_bytes in enumerate(images_list):
        # Convert BytesIO to PIL Image
        qr_image = Image.open(qr_image_bytes)

        # Resize the image using ImageReader
        qr_image_reader = ImageReader(qr_image)
        qr_image_width, qr_image_height = qr_image.size
        resize_ratio = min(image_width / qr_image_width, image_height / qr_image_height)
        qr_image_width *= resize_ratio
        qr_image_height *= resize_ratio

        # Calculate the position of the current image
        row = i // images_per_row
        col = i % images_per_row
        x = margin + col * (image_width + horizontal_gap)
        y = page_height - (margin + (row + 1) * image_height + row * vertical_gap)  # Adjusted y coordinate

        # Draw the image on the canvas
        pdf_canvas.drawImage(qr_image_reader, x, y, width=qr_image_width, height=qr_image_height)

        # Calculate the center of the image
        if images_labels_list:
            image_center_x = x + qr_image_width / 2

            # Calculate the position of the label or caption
            caption_y = y - 0.25 * inch

            # Center the label or caption horizontally
            caption_text = images_labels_list[i]
            caption_width = pdf_canvas.stringWidth(caption_text)
            caption_x = image_center_x - caption_width / 2

            # Draw the label or caption on the canvas
            pdf_canvas.drawString(caption_x, caption_y, caption_text)

    # Save and close the PDF
    pdf_canvas.save()


def read_values_from_excel_column(file_path: str, column_name: str):
    try:
        import pandas as pd

        df = pd.read_excel(file_path)
        column_values = df[column_name].astype(str).tolist()
        return column_values

    except KeyError as e:
        return f"read_values_from_excel_column, Error: {e}. Column '{column_name}' not found in the Excel file."

    except Exception as e:
        return f"read_values_from_excel_column, An error occurred: {e}"