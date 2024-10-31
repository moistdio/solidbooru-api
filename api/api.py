import asyncio
import os
from flask import Flask, redirect, request, jsonify, Blueprint, url_for
from api.stablehorde.client import StableHordeAPI
from api.stablehorde.models import GenerationInput, ModelGenerationInputStable, ModelPayloadLorasStable
from db.models.models import Image, db

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

# Load configuration from environment variables
API_KEY = os.getenv("STABLE_HORDE_API_KEY", "EwZVK3w4rLZbzLGlnHBwNw")

def get_json_data():
    if request.content_type.startswith('application/json'):
        try:
            return request.get_json()
        except Exception as e:
            return None, f"Invalid JSON data: {str(e)}"
    else:
        return request.form.to_dict(), None

def create_generation_input(prompt):
    formated_prompt = f"score_9, score_8_up, score_7_up, BREAK, {prompt} ### score_1, score_2, score_3, text"

    params = ModelGenerationInputStable(
        sampler_name="k_euler_a",
        cfg_scale=3.5,
        height=1344,
        width=768,
        steps=30,
        clip_skip=2,
        karras=True,
        loras=[
            ModelPayloadLorasStable(
                name="850521",
                clip=0.5
            ).to_dict()
        ],
        n=1
    )

    return GenerationInput(
        prompt=formated_prompt,
        params=params,
        models=['Pony Realism'],
        r2=True
    )

@api_bp.route('/image/generate', methods=['POST'])
async def generate_image_route():
    data, error = get_json_data()
    if error:
        return jsonify({"message": error}), 400

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"message": "Prompt is required"}), 400

    generation_input = create_generation_input(prompt)

    try:
        async with StableHordeAPI(api_key=API_KEY) as stablehorde_client:
            response_data = await stablehorde_client.txt2img_request(generation_input)

            if not response_data.id:
                return jsonify({"message": "Failed to generate image"}), 400

            uuid = response_data.id
            image = Image(uuid=uuid, url=response_data.id, prompt=prompt)

            db.session.add(image)
            db.session.commit()

            return redirect(url_for('user_bp.home', uuid=uuid))

    except Exception as e:
        return jsonify({"message": str(e)}), 400

@api_bp.route('/image/check/', methods=['GET'])
async def check_image_route():
    image_id = request.args.get('id')
    if not image_id:
        return jsonify({"message": "Image ID is required"}), 400
    
    image = Image.query.filter_by(uuid=image_id).first()
    if not image:
        return jsonify({"message": "Image not found"}), 404
    
    if image.done:
        return jsonify(image.to_dict()), 200

    try:
        async with StableHordeAPI(api_key=API_KEY) as stablehorde_client:
            response_data = await stablehorde_client.generate_check(image_id)
            return jsonify(response_data.to_dict()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@api_bp.route('/image/get/', methods=['GET'])
async def get_image_route():
    image_id = request.args.get('id')
    if not image_id:
        return jsonify({"message": "Image ID is required"}), 400
    
    image = Image.query.filter_by(uuid=image_id).first()
    if not image:
        return jsonify({"message": "Image not found"}), 404
    
    if image.done:
        return jsonify(image.to_dict()), 200

    try:
        async with StableHordeAPI(api_key=API_KEY) as stablehorde_client:
            response_data = await stablehorde_client.generate_from_txt(image_id)

            if not response_data['img_status'].done:
                return jsonify(image.to_dict()), 200
            
            if not image.done:
                image.url = response_data['img_status'].generations[0].img
                image.seed = response_data['img_status'].generations[0].seed
                image.done = True
                db.session.commit()

            return jsonify(image.to_dict()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

