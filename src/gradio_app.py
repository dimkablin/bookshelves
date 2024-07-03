import gradio as gr
import json

from models.speech2text import transcribe_audio
from models.llama_inference import generate
from utils import json2excel, json_is_correct

from env import DEFAULT_JSON
CURR_JSON = DEFAULT_JSON


def gradio_interface(audio):
    # update json format response
    response_format = {
        "type": "json_object",
        "schema": CURR_JSON
    }

    # transcribe and structure
    for transcription in transcribe_audio(audio):
        yield transcription, ""

    for response in generate(transcription, response_format):
        yield transcription, response


def generate_excel(structured_text):
    # convert to excel
    excel_file = json2excel(structured_text)
    return excel_file


def json_update(json_schema: str) -> str:
    global CURR_JSON

    if json_is_correct(json_schema):
        CURR_JSON = json.loads(json_schema)
        return CURR_JSON
    else:
        return "Invalid JSON scheme"


with gr.Blocks() as demo:
    gr.Markdown("# Структурирование учета книг через голосовой ввод")

    # Голос -> Текст -> Файл эксель
    with gr.Tab("Обработка"):
        audio_input = gr.Audio(type="filepath", label="Загрузите аудиофайл")
        transcription_output = gr.Textbox(label="Транскрипция")
        structured_text_output = gr.Textbox(label="Структурированный текст")
        
        generate_button = gr.Button("Поехали!")
        generate_button.click(fn=gradio_interface, inputs=audio_input, outputs=[transcription_output, structured_text_output])
        
        excel_file_output = gr.File(label="Скачать Excel файл")
        
        generate_excel_button = gr.Button("Сгенерировать excel файл")
        generate_excel_button.click(fn=generate_excel, inputs=structured_text_output, outputs=excel_file_output)

    # Редачить JSON схему
    with gr.Tab("Настройки"):
        json_input = gr.Textbox(value=json.dumps(CURR_JSON, ensure_ascii=False, indent=4), lines=15, label="Отредактировать JSON схему")
        json_output = gr.JSON(value=CURR_JSON, label="JSON схема")

        update_button = gr.Button("Обновить JSON схему")
        update_button.click(fn=json_update, inputs=json_input, outputs=json_output)
