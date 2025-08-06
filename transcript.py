import re
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# Challenge: 
# How to know roles in Transcript
# How to know who is candidate
# How to scoring meeting content
# How to scoring candidate based on his/her answers
# - Detect question
# - Detect answer
# - Define correct answer
# - Compare correct answer
# How to handle long video audio
# How to select context window fit each type of meetings
# How to improve correctness of scoring using the labelled data set
# What is pipeline and workflow
# Should be integrated with Apache Airflow
# @todo: need to remove loop words, e.g. "cai cai cai cai"
if torch.cuda.is_available():
    # Need to install CUDA driver or CUDA toolkit.
    # sudo apt install nvidia-cuda-toolkit
    # sudo apt install ffmpeg
    print("CUDA is available")
else:
    print("CUDA is not available")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    # chunk_length_s=30,
    return_timestamps=True,
    batch_size=2048,  # batch size for inference - set based on your device
    torch_dtype=torch_dtype,
    device=device,
)

def transcript(input_file_name: str, language: str="vietnamese"):

    result = pipe(f"audio_output/{input_file_name}.mp3", generate_kwargs={"language": f"{language}"})

    with open(f"transcript/{input_file_name}.md", "w", encoding="utf-8") as file:
            file.write(result["text"])

if __name__ == "__main__":
     transcript("son_interview")