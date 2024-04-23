from llm.init import model, generation_config, safety_settings,video_model, json_converter_model


def predict(context, prompt, parser):
    try:
        chain = prompt | model | parser
        completion = chain.invoke(context)
        return completion
    except Exception as e:
        raise e

def predict_with_video(video, text):
    try:
        responses = video_model.generate_content(
        [video, text],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False)
        return responses.text
    except Exception as e:
        raise e

def convert_json(context, prompt, parser):
    try:
        chain = prompt | json_converter_model | parser
        completion = chain.invoke(context)
        return completion
    except Exception as e:
        raise e