# LlamaPhone - AI Model Guide

## Recommended Model: Qwen2.5-Coder

**Qwen2.5-Coder-7B-Instruct** is the recommended model for LlamaPhone.

### Why Qwen2.5-Coder?

| Feature | Rating |
|---------|--------|
| Code Generation | ⭐⭐⭐⭐⭐ |
| Function Calling | ⭐⭐⭐⭐⭐ |
| Python/Shell Scripts | ⭐⭐⭐⭐⭐ |
| Mobile Repair Context | ⭐⭐⭐⭐ |
| Memory Requirements | ⭐⭐⭐⭐ (7B params) |

### Installation

```bash
ollama pull qwen2.5-coder:7b
```

> Note: `install.bat` / `python setup.py` already pulls `qwen2.5-coder:7b` during onboarding.  
> Use the command above only if you want to pull it manually again.

### Quantized Versions

For systems with limited RAM/VRAM:

```bash
# Q4_K_M (Recommended - balanced)
ollama pull qwen2.5-coder:7b:q4_k_m

# Q5_K_M (Better quality, more RAM)
ollama pull qwen2.5-coder:7b:q5_k_m

# Q8_0 (Best quality, high RAM)
ollama pull qwen2.5-coder:7b:q8_0
```

## Alternative Models

### CodeLlama
```bash
ollama pull codellama:7b
```
- Good for general code
- Trained by Meta

### Mistral
```bash
ollama pull mistral:7b
```
- General purpose
- Fast inference

### Llama 3
```bash
ollama pull llama3:8b
```
- General purpose
- Good community support

## Importing Custom Models

### From Hugging Face

1. **Download GGUF file:**
```bash
# Using huggingface-cli
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct-GGUF qwen2.5-coder-7b-instruct-q4_k_m.gguf

# Or using wget
wget https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF/resolve/main/qwen2.5-coder-7b-instruct-q4_k_m.gguf
```

2. **Create Modelfile:**
```dockerfile
FROM ./qwen2.5-coder-7b-instruct-q4_k_m.gguf
TEMPLATE """{{ if .System }}{{ .System }}\n{{ end }}{{ .Prompt }}"""
PARAMETER num_ctx 4096
PARAMETER temperature 0.7
```

3. **Import to Ollama:**
```bash
ollama create llamaphone-ai -f Modelfile
ollama run llamaphone-ai "Hello"
```

### Ollama Library Models

```bash
# List available models
ollama list

# Search for models
ollama search qwen

# Pull specific model
ollama pull qwen2.5-coder:7b
```

## Model Selection in LlamaPhone

Models can be changed in **Settings → AI Configuration**:
- Select from available Ollama models
- Adjust temperature (creativity vs accuracy)
- Set max tokens for responses

## Hardware Requirements

| Model Size | RAM | VRAM | Use Case |
|-----------|-----|------|----------|
| 3B | 4GB | - | CPU only |
| 7B | 8GB | 4GB | Consumer GPU |
| 13B | 16GB | 8GB | Mid-range GPU |
| 34B | 32GB | 16GB | High-end GPU |

## Performance Tips

1. **Use quantized models** for faster inference
2. **Adjust context length** (num_ctx) based on task
3. **Lower temperature** (0.1-0.3) for more consistent code
4. **Keep model loaded** in Ollama for faster responses

## Troubleshooting

### Model not found
```bash
ollama list  # Check installed models
ollama pull <model_name>  # Download if missing
```

### Out of memory
- Use smaller quantization (Q4 instead of Q8)
- Reduce context length
- Close other applications

### Slow responses
- Use GPU acceleration if available
- Use quantized models
- Increase num_ctx if RAM allows
