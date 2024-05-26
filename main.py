import argparse
import logging
import librosa
import soundfile as sf
import speech_recognition as sr


def change_speed(sound, rate, speed):
    # Изменение скорости воспроизведения
    return librosa.resample(sound, orig_sr=rate, target_sr=rate * speed)


def change_volume(sound, gain):
    # Изменение громкости
    return sound * (10 ** (gain / 20.0))


def process_audio(input_file, output_file, speed, volume):
    # Загрузка аудиофайла
    sound, rate = librosa.load(input_file, sr=None)

    # Изменение скорости
    if speed != 1.0:
        sound = change_speed(sound, rate, 1/speed)

    # Изменение громкости
    if volume != 0:
        sound = change_volume(sound, volume)

    # Сохранение обработанного файла
    sf.write(output_file, sound, rate)
    print(f"Измененнвый файл сохранен как {output_file}")


def transcribe_audio(input_file, log_file, languages):
    # Расшифровка аудиофайла в текст
    recognizer = sr.Recognizer()

    with sr.AudioFile(input_file) as source:
        audio_data = recognizer.record(source)

    text = recognizer.recognize_sphinx(audio_data, language=languages)
    print("Транскрипция аудио:")
    print(text)

    logger = logging.getLogger(log_file)

    # Логирование результата в JSON файл
    transcription_log = {
        "Входной файл": input_file,
        "Транскрипция аудио": text
    }

    with open(log_file, 'a') as log:
        log.write(f"{transcription_log}\n")

    logger.info("Транскрипция Завершина", extra={"Входной файл": input_file, "Транскрипция аудио": text})
    return text


def main():
    parser = argparse.ArgumentParser(description="Именение и транскрипция WAV аудио файла.")
    parser.add_argument("input_file", type=str, help="Путь исходного файла WAV.")
    parser.add_argument("--output_file", type=str, help="Путь куда будет сохранен новый WAV файл.")
    parser.add_argument("--speed", type=float, default=1.0, help="Как ускорить (По умолчанию: 1.0).")
    parser.add_argument("--volume", type=int, default=0, help="Изменить громкость (По умолчанию: 0).")
    parser.add_argument("--transcribe", action='store_true', help="Транскрипция аудио в текст.")
    parser.add_argument("--log_file", type=str, default="transcription_log.json",
                        help="Путь сохранений логов транскрипции (по умолчанию: transcription_log.json).")
    parser.add_argument("--languages", type=str, default="en-US",
                        help="Выбор языка с перевода аудио файл (eu-US/ru-RU) (по умолчанию: eu-US).")

    args = parser.parse_args()

    if args.output_file:
        process_audio(args.input_file, args.output_file, args.speed, args.volume)

    if args.transcribe:
        transcribe_audio(args.input_file, args.log_file, args.languages)


if __name__ == "__main__":
    main()
