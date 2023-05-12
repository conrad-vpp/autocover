from flask import Flask, jsonify
import openai
import xml.etree.ElementTree as ET

app = Flask(__name__)

openai.api_key = 'your-api-key'

def parse_fdx(fdx_file):
    tree = ET.parse(fdx_file)
    root = tree.getroot()
    content = root.find('Content')

    scenes = []
    scene = []

    for paragraph in content.findall('Paragraph'):
        paragraph_type = paragraph.get('Type')
        if paragraph_type == 'Scene Heading':
            if scene:
                scenes.append(scene)
                scene = []
        scene.append(paragraph.find('Text').text)

    if scene:
        scenes.append(scene)

    return scenes

def generate_synopsis(scene):
    scene_text = ' '.join(scene)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{scene_text}\n\nSynopsis:",
        temperature=0.3,
        max_tokens=60
    )

    synopsis = response.choices[0].text.strip()

    return synopsis

@app.route('/parse', methods=['GET'])
def parse_and_generate_synopsis():
    with open('path_to_your_file.fdx', 'r') as file:
        scenes = parse_fdx(file)
    
    scene_synopses = []
    for scene in scenes:
        scene_text = ' '.join(scene)
        synopsis = generate_synopsis(scene)
        scene_synopses.append({
            'scene': scene_text,
            'synopsis': synopsis
        })

    return jsonify(scene_synopses), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
