# File config
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import whisper
from moviepy import * 
from openai import OpenAI
from utils import *

FILENAME = "venom1"
INPUT_VIDEO_PATH = os.getcwd() + "/videos/" + FILENAME + ".mp4"
OUTPUT_TEXT_PATH = os.getcwd() + "/output_files/" + FILENAME + ".txt"


def chat(prompt):
    """
    Open Ai Chat prompt.
    """
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "assistant",
                "content": prompt,
            },
        ],
    )
    return completion.choices[0].message.content

def text_to_speech(input_text_path, output_audio_path):
    """
    Generate text.
    """
    text = '¿Cómo es que Venom terminó eligiendo a Eddie? Él no come a los buenos, ni a los conocidos, ni a los transeúntes; en resumen, solo se alimenta de los malos. Viéndolo de esta manera, Venom también podría considerarse un héroe que elimina a los villanos, no tan diferente de un superhéroe. ¿Recuerdas cuando éramos niños y veíamos Spider-Man 3? ¡Ese Venom fue una sombra de la infancia! ¿Por qué las películas de Venom cambiaron tanto? Primero, un poco de ciencia: los simbiontes en sí no tienen una moralidad inherente, depende de quién los hospede. Si se alojan en un héroe, el simbionte es bueno, y si se alojan en un villano, el simbionte es malo. En la primera película de Venom, hay una línea que lo explica muy bien, aunque en ese momento no lo entendí completamente. ¿Esto no es simplemente un "simbionte común"? ¿Qué tiene de especial? Hasta que luego vi que Venom, para proteger la Tierra, estaba dispuesto a luchar contra sus propios semejantes, y entendí que no se puede ver a Venom desde la perspectiva humana. Es un extraterrestre, y su planeta natal, el planeta Klyntar, está desolado, completamente cubierto de una capa negra. Al llegar a la Tierra, Venom ve un mundo lleno de vida: desiertos, ciudades, montañas, paisajes... después de haber visto tanta miseria en su planeta natal, ¿quién querría regresar? En cuanto a la biodiversidad, Klyntar solo tiene simbiontes, no como la Tierra, que tiene una riqueza de especies completamente diferente. Solo en los seres humanos hay una increíble variedad de formas y especies. Venom, al estar en la Tierra, se siente atraído por esos pequeños animales y siempre quiere probar cosas nuevas. En esta película, por fin se divierte un poco: se "prueba" al hospedarse en un pez y una rana. Para Venom, la mayor ventaja de la Tierra es que aquí ha experimentado lo que significa el amor, algo que nunca había conocido en su planeta, gracias a Eddie y la señora Chen. Venom solía decir que era el más débil de los simbiontes. En su planeta, no era nada especial. Y es que en Klyntar, incluso los más débiles tienen un nombre, pero Venom nunca osó decir el suyo. Sin embargo, la Tierra es diferente, aquí hay algo que lo atrae y lo hace querer quedarse: los humanos, con sus emociones, su amor, su luz. Es un lugar donde, una vez que te encariñas, es difícil dejarlo. Venom también siente lo mismo. Todo tiene un final, y parece que su vida "normal" con Eddie está llegando a su fin. Venom no puede dejar ir los momentos felices que pasó con Eddie, montando en moto, disfrutando en un bar, o incluso bailando con la señora Chen en un club. En esta película, Venom va tachando cosas de su lista de deseos, sabiendo que probablemente este será el final de su historia. Es posible que en la tercera película de la saga, Venom y Eddie se despidan para siempre, tal como lo indica el subtítulo: "Última parte". Si es así, lo más probable es que Venom decida sacrificarse para proteger a Eddie. Pero yo creo que Venom no se despedirá del todo. Después de todo, en la película de Spider-Man: No Way Home quedó un pequeño detalle: Venom dejó algo en la Tierra, y no olvidemos la escena post-créditos de Spider-Man: No Way Home, donde se abre la posibilidad de que el multiverso de Venom regrese a la Tierra en el futuro. Claro, esto son solo especulaciones. En general, Venom: La última batalla lleva la saga a su clímax, tanto en acción como en emoción. Después de seis años, el regreso de la saga a China ha traído nuevos efectos visuales y un toque de creatividad. La combinación de lo tonto y lo genial de Venom sigue intacta. La Tierra, como su segundo hogar, siempre será el lugar donde Venom luchará por quedarse, aunque lluevan más simbiontes del cielo o incluso el "dios de los simbiontes", Knull, decida invadir. Venom siempre estará decidido a proteger este mundo. Y cuando le dice a Eddie "I\'m with you to the end" (Estoy contigo hasta el final), sabe que su vínculo con la Tierra y con Eddie es más fuerte que cualquier otra cosa.'
    client = OpenAI()
    with open(input_text_path, "r") as file:
        lines = file.readlines()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(input_text_path, output_audio_path)

def speed_up_audio(input_file, output_file, speed_factor=1.5):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Speed up the audio by changing the playback speed
    # Speed factor > 1 will speed up, < 1 will slow down
    sped_up_audio = audio.speedup(playback_speed=speed_factor)

    # Export the sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")

    print(f"Audio saved as {output_file}")

def remove_silence(input_file, output_file, silence_thresh=-40, min_silence_len=1000):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Split the audio based on silence
    chunks = split_on_silence(audio, 
                              min_silence_len=min_silence_len, 
                              silence_thresh=silence_thresh)

    # Concatenate the non-silent chunks back together
    final_audio = AudioSegment.empty()
    for chunk in chunks:
        final_audio += chunk

    # Export the result to a file
    final_audio.export(output_file, format="wav")

    print(f"Audio without silence saved to {output_file}")

# Function to generate subtitles using Whisper
def generate_subtitles(video_file, output_srt, model="turbo"):
    try:
        result = model.transcribe(video_file)
        
        # Save subtitles in SRT format
        with open(output_srt, "w") as f:
            for i, segment in enumerate(result["segments"]):
                start = segment["start"]
                end = segment["end"]
                text = segment["text"].strip()
                
                f.write(f"{i + 1}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{text}\n\n")
                
        print(f"Subtitles saved to {output_srt}")
    except Exception as e:
        print(f"An error occurred while generating subtitles: {e}")

# Helper function to format time in SRT forma
def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02}:{mins:02}:{secs:02},{millis:03}"

def add_subtitles_to_video(video_file, srt_file, output_video):
    try:
        video = VideoFileClip(video_file)
        
        # Read SRT file
        with open(srt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        subtitles = []
        for i in range(0, len(lines), 4):  # SRT blocks are typically 4 lines each
            start_time = parse_srt_time(lines[i + 1].split(" --> ")[0].strip())
            end_time = parse_srt_time(lines[i + 1].split(" --> ")[1].strip())
            text = lines[i + 2].strip()
            
            # Create a subtitle text clip
            subtitle_clip = TextClip(
                    text=text,  # Text content
                    font="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Use a valid system font
                    font_size=50,  # Font size (note: fontsize, not font_size)
                    color="white",  # Text color
                    bg_color="black",  # Background color for better readability
                    size=(video.w, None),  # Match video width
                    duration = end_time - start_time
                )
            subtitle_clip.with_start(start_time)
            subtitle_clip.with_end(end_time)
            subtitle_clip.with_position(("center", "bottom"))
            subtitle_clip.start = start_time
            subtitle_clip.end = end_time


    
            subtitles.append(subtitle_clip)
        
        print(subtitles)
        # Overlay subtitles on the video
        final_video = CompositeVideoClip([video, *subtitles])
        final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")
        print(f"Video with subtitles saved to {output_video}")
    except Exception as e:
        print(f"An error occurred while adding subtitles: {e}")

# Helper function to parse SRT time
def parse_srt_time(srt_time):
    h, m, s = srt_time.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
