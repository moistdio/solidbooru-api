import asyncio
from flask import Flask, redirect, request, jsonify, Blueprint, url_for
from api.stablehorde.client import StableHordeAPI
from api.stablehorde.models import GenerationInput, ModelGenerationInputStable, ModelPayloadLorasStable
from db.models.models import Image, db

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

@api_bp.route('/image/generate', methods=['POST'])
async def generate_image_route():
    if request.content_type.startswith('application/json'):
        try:
            data = await request.get_json()
        except Exception as e:
            return jsonify({"message": f"Invalid JSON data: {str(e)}"}), 400
    else:
        data = request.form.to_dict()

    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"message": "Prompt is required"}), 400

    params = ModelGenerationInputStable(
        sampler_name="k_euler",
        cfg_scale=1.0,
        height=1024,
        width=1024,
        steps=8,
        loras=[
            ModelPayloadLorasStable(
                name="790683",
            ).to_dict()
        ],
        n=1
    )

    generation_input = GenerationInput(
        prompt=prompt,
        params=params,
        models=['Flux.1-Schnell fp8 (Compact)'],
        r2=True
    )

    try:
        async with StableHordeAPI(api_key="EwZVK3w4rLZbzLGlnHBwNw") as stablehorde_client:
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

    try:
        async with StableHordeAPI(api_key="EwZVK3w4rLZbzLGlnHBwNw") as stablehorde_client:
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
        async with StableHordeAPI(api_key="EwZVK3w4rLZbzLGlnHBwNw") as stablehorde_client:
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
