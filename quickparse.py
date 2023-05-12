from flask import Flask, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

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

@app.route('/parse', methods=['GET'])
def parse_and_store_scenes():
    with open('TakeaBreath_121521.fdx', 'r') as file:
        scenes = parse_fdx(file)
    
    scene_texts = []
    for scene in scenes:
        scene_text = ' '.join(scene)
        scene_texts.append(scene_text)

    return jsonify(scene_texts), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)


