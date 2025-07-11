import subprocess
import os

def convert_video_to_audio(video_path, audio_path, audio_format="mp3"):
    """
    Convert a video file to an audio file using FFmpeg.

    Args:
        video_path (str): Path to the input video file.
        audio_path (str): Path to the output audio file (including file name and extension).
        audio_format (str): Desired audio format (e.g., "mp3", "aac", "wav").
                            Default is "mp3".
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at path '{video_path}'")
        return

    # Kiểm tra và tạo thư mục chứa file audio nếu chưa có
    output_dir = os.path.dirname(audio_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created folder: {output_dir}")

    # Building the FFmpeg command
    # -i: Input file
    # -vn: Exclude video stream (extract audio only)
    # -acodec libmp3lame: Use the MP3 encoder (or change depending on the format)
    # -q:a 0: Highest audio quality (only applies to some codecs like MP3)
    # -map 0:a: Extract only the first audio stream from the input file

    # For formats other than MP3, you may need to adjust the codec
    # Example: for AAC -> "-c:a aac -b:a 192k"
    # Example: for WAV -> "-c:a pcm_s16le"

    
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-map", "0:a", # Select the first sound stream
    ]
    
    if audio_format == "mp3":
        command.extend(["-acodec", "libmp3lame", "-q:a", "0"]) # High quality for MP3
    elif audio_format == "aac":
        command.extend(["-c:a", "aac", "-b:a", "192k"]) # Bitrate for AAC
    elif audio_format == "wav":
        command.extend(["-c:a", "pcm_s16le"]) # Codec for WAV
    else:
        # Defaults to using the "copy" codec if none is specified clearly
        print(f"Warning: Audio format '{audio_format}' is not supported correctly. "
              "FFmpeg will try to use the default codec.")
        
    command.append(audio_path)

    try:
        print(f"Đang chuyển đổi: '{video_path}' sang '{audio_path}'...")
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Chuyển đổi hoàn tất!")
        print(process.stdout)
        if process.stderr:
            print(process.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi chuyển đổi: {e}")
        print("Đầu ra lỗi FFmpeg:")
        print(e.stderr)
    except FileNotFoundError:
        print("Lỗi: FFmpeg không tìm thấy. Đảm bảo FFmpeg đã được cài đặt và có trong PATH của bạn.")

# --- Cách sử dụng ---
if __name__ == "__main__":
    input_video = "sample_videos/ai_presentation.mp4"
    output_audio_mp3 = "audio_output/ai_presentation.mp3"
    output_audio_aac = "audio_output/ai_presentation.aac"
    output_audio_wav = "audio_output/ai_presentation.wav"

    # Ví dụ 1: Chuyển đổi sang MP3
    convert_video_to_audio(input_video, output_audio_mp3, audio_format="mp3")

    # Ví dụ 2: Chuyển đổi sang AAC
    convert_video_to_audio(input_video, output_audio_aac, audio_format="aac")
    
    # Ví dụ 3: Chuyển đổi sang WAV
    convert_video_to_audio(input_video, output_audio_wav, audio_format="wav")
    
    