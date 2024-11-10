def read_subtitle_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Prepare a list to hold the extracted content
        extracted_lines = []

        # Extracting the content from the subtitle file
        for line in lines:
            line = line.strip()
            if line and not line[0].isdigit() and '-->' not in line:
                extracted_lines.append(line)  # Append the actual subtitle text to the list

        # Write the extracted lines to a new output file
        with open(output_file, 'w', encoding='utf-8') as output:
            for subtitle in extracted_lines:
                output.write(subtitle + ',')  # Write each subtitle on a new line

        print(f'Extracted content saved to: {output_file}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    input_file = "C:\\Users\\chang\\Desktop\\Automation_whisper_tts\\captions.txt"
    output_file = "C:\\Users\\chang\\Desktop\\Automation_whisper_tts\\captions_processsed.txt"
    read_subtitle_file(input_file, output_file)
