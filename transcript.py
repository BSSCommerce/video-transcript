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
    chunk_length_s=30,
    batch_size=16,  # batch size for inference - set based on your device
    torch_dtype=torch_dtype,
    device=device,
)

result = pipe("audio_output/ai_presentation.mp3", generate_kwargs={"language": "vietnamese"})

print(result["text"])
