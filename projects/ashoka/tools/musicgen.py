import sys, time, torch, scipy.io.wavfile as w
from transformers import AutoProcessor, MusicgenForConditionalGeneration
model_id, prompt, secs, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
torch.manual_seed(int(sys.argv[5]) if len(sys.argv) > 5 else 1)
torch.set_num_threads(4)
p = AutoProcessor.from_pretrained(model_id); m = MusicgenForConditionalGeneration.from_pretrained(model_id)
t = time.time()
inp = p(text=[prompt], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=3.0, max_new_tokens=int(secs * 50))
sr = m.config.audio_encoder.sampling_rate
w.write(out, sr, a[0].T.numpy() if a.shape[1] > 1 else a[0, 0].numpy())
print(f"{out}: {secs}s in {time.time()-t:.0f}s")
