from flask import Flask, request, Response
from PIL import Image
import io

app = Flask(__name__)

def generate_image(width, height, color, image_format):
    # Validate input parameters
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        return None, "Invalid width or height parameter."
    if color not in ['red', 'green', 'blue']:
        return None, "Invalid color parameter."
    if image_format not in ['jpeg', 'png', 'gif']:
        return None, "Invalid format parameter."

    # Generate the image
    color_dict = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255)}
    image = Image.new('RGB', (width, height), color_dict[color])

    # Convert the image to bytes in the specified format
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image_format)
    image_bytes = image_bytes.getvalue()

    return image_bytes, None

@app.route('/generate_image', methods=['GET'])
def api_generate_image():
    # Get the input parameters
    width = request.args.get('width', type=int)
    height = request.args.get('height', type=int)
    color = request.args.get('color')
    image_format = request.args.get('format')

    # Generate the image bytes
    image_bytes, error = generate_image(width, height, color, image_format)
    if error:
        return Response(error, status=400, mimetype='text/plain')

    # Return the image bytes as a response
    return Response(image_bytes, status=200, mimetype='image/{}'.format(image_format))

if __name__ == '__main__':
    app.run()
