from googletrans import Translator

def translate_text(text, src_language='auto', dest_language='en'):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=dest_language)
    return translation.text

def translate_file(input_file, output_file, src_lang='auto', dest_lang='en'):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        translated_content = translate_text(content, src_language=src_lang, dest_language=dest_lang)
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_content)

        print(f'Translated content saved as: {output_file}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    input_file = "C:\\Users\\chang\\Desktop\\Automation_whisper_tts\\captions_processsed.txt"
    output_file = "C:\\Users\\chang\\Desktop\\Automation_whisper_tts\\captions_es.txt"
    src_lang = 'zh-CN'
    dest_lang = 'es'

    translate_file(input_file, output_file, src_lang, dest_lang)
