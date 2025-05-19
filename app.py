from flask import Flask, render_template, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import io
import random

app = Flask(__name__)

# Load the pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_caption(image):
    # Preprocess the image
    pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    # Generate caption
    output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
    caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    return caption

def add_emoji_to_caption(caption):
    emoji_map = {
        'dog': '🐶', 'cat': '🐱', 'bird': '🐦', 'car': '🚗', 'tree': '🌳', 'flower': '🌸',
        'food': '🍽️', 'pizza': '🍕', 'cake': '🍰', 'beach': '🏖️', 'mountain': '🏔️',
        'sun': '☀️', 'cloud': '☁️', 'rain': '🌧️', 'snow': '❄️', 'person': '🧑',
        'child': '🧒', 'baby': '👶', 'man': '👨', 'woman': '👩', 'people': '🧑‍🤝‍🧑',
        'phone': '📱', 'computer': '💻', 'book': '📖', 'horse': '🐴', 'bicycle': '🚲',
        'bus': '🚌', 'train': '🚆', 'boat': '⛵', 'city': '🏙️', 'street': '🛣️',
        'park': '🏞️', 'lake': '🏞️', 'river': '🏞️', 'drink': '🥤', 'coffee': '☕',
        'tea': '🍵', 'fruit': '🍎', 'vegetable': '🥦', 'ice cream': '🍦', 'chocolate': '🍫',
        'smile': '😊', 'happy': '😃', 'sad': '😢', 'angry': '😠', 'love': '❤️',
        'heart': '❤️', 'star': '⭐', 'night': '🌙', 'day': '🌞', 'sky': '🌌',
        'ocean': '🌊', 'sea': '🌊', 'fish': '🐟', 'rabbit': '🐰', 'bear': '🐻',
        'lion': '🦁', 'tiger': '🐯', 'elephant': '🐘', 'monkey': '🐒', 'panda': '🐼',
        'koala': '🐨', 'fox': '🦊', 'wolf': '🐺', 'cow': '🐮', 'pig': '🐷', 'sheep': '🐑',
        'chicken': '🐔', 'duck': '🦆', 'goose': '🪿', 'deer': '🦌', 'frog': '🐸', 'turtle': '🐢',
        'snake': '🐍', 'zebra': '🦓', 'giraffe': '🦒', 'camel': '🐫', 'kangaroo': '🦘',
        'whale': '🐋', 'dolphin': '🐬', 'shark': '🦈', 'octopus': '🐙', 'crab': '🦀',
        'lobster': '🦞', 'shrimp': '🦐', 'snail': '🐌', 'butterfly': '🦋', 'bee': '🐝',
        'ant': '🐜', 'spider': '🕷️', 'ladybug': '🐞', 'penguin': '🐧', 'owl': '🦉',
        'eagle': '🦅', 'parrot': '🦜', 'peacock': '🦚', 'swan': '🦢', 'flamingo': '🦩',
        'rooster': '🐓', 'turkey': '🦃', 'dove': '🕊️', 'bat': '🦇', 'unicorn': '🦄',
        'dragon': '🐉', 'crocodile': '🐊', 'hippo': '🦛', 'rhino': '🦏', 'gorilla': '🦍',
        'leopard': '🐆', 'cheetah': '🐆', 'jaguar': '🐆', 'panther': '🐆', 'lynx': '🐈',
        'cougar': '🐈', 'bobcat': '🐈', 'caracal': '🐈', 'serval': '🐈', 'ocelot': '🐈',
        'clouded leopard': '🐆', 'snow leopard': '🐆',
    }
    for word, emoji in emoji_map.items():
        if word in caption.lower():
            return f"{emoji} {caption}"
    return caption

def make_insta_friendly(caption):
    hashtag_map = {
        'dog': '#dog #dogsofinstagram', 'cat': '#cat #catsofinstagram', 'beach': '#beach #sunnydays',
        'mountain': '#mountain #nature', 'food': '#foodie #yum', 'cake': '#cake #dessert',
        'car': '#car #drive', 'flower': '#flowers #bloom', 'sun': '#sunshine', 'city': '#citylife',
        'tree': '#trees #nature', 'river': '#river #water', 'lake': '#lake #relax', 'bird': '#bird #wildlife',
        'baby': '#baby #cute', 'child': '#kids #childhood', 'people': '#friends #goodtimes',
        'night': '#night #lights', 'sky': '#sky #clouds', 'ocean': '#ocean #waves',
    }
    hashtags = set()
    for word, tags in hashtag_map.items():
        if word in caption.lower():
            hashtags.update(tags.split())
    hashtags.update(['#InstaPic', '#PhotoOfTheDay', '#InstaGood'])

    fun_phrases = [
        'What do you think?',
        'Love this view!',
        'Vibes only ✨',
        'Captured the moment!',
        'Memories made here.',
        'Insta vibes!',
        'Too good not to share!',
        'Feeling this!',
        'Can you relate?',
        'Drop a ❤️ if you like this!'
    ]
    phrase = random.choice(fun_phrases)

    # Capitalize first letter after emoji (if present)
    parts = caption.split(' ', 1)
    if len(parts) > 1 and parts[0].encode('unicode_escape').startswith(b'\\U'):
        main_caption = parts[1].strip()
        if main_caption:
            main_caption = main_caption[0].upper() + main_caption[1:]
        caption = f"{parts[0]} {main_caption}"
    else:
        caption = caption.strip().capitalize()

    # Ensure caption ends with a full stop
    if not caption.endswith('.'):
        caption += '.'

    # Compose three-line caption, each on a new line
    return f"{caption}\n{phrase}\n{' '.join(sorted(hashtags))}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-caption', methods=['POST'])
def generate_caption_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    try:
        # Read and process the image
        image = Image.open(io.BytesIO(file.read()))
        caption = generate_caption(image)
        caption_with_emoji = add_emoji_to_caption(caption)
        insta_caption = make_insta_friendly(caption_with_emoji)
        return jsonify({'caption': insta_caption})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 