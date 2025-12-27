# Ollama SDK Streamlit Examples

This directory contains **32 individual interactive Streamlit pages**, each demonstrating a specific feature of the Ollama SDK.

## 🎯 Structure

Each page includes **two tabs**:
- **🎯 Demo**: Interactive demonstration with Streamlit UI
- **📄 Source Code**: Original source code from `/src` directory

## 📁 All Pages (01-32)

### 💬 Chat Examples (01-05)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 01 | 💬 Chat | `chat.py` | Basic question-answer interaction |
| 02 | 💬 Chat Stream | `chat-stream.py` | Streaming responses |
| 03 | 💬 Chat History | `chat-with-history.py` | Conversation context management |
| 04 | 💬 Chat Logprobs | `chat-logprobs.py` | Token probability analysis |
| 05 | 💬 Async Chat | `async-chat.py` | Asynchronous operations |

### ✨ Generate Examples (06-13)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 06 | ✨ Generate | `generate.py` | Simple text generation |
| 07 | ✨ Generate Stream | `generate-stream.py` | Streaming generation |
| 08 | ✨ Generate Logprobs | `generate-logprobs.py` | Generation with probabilities |
| 09 | ✨ Async Generate | `async-generate.py` | Async text generation |
| 10 | 🧠 Thinking | `thinking.py` | DeepSeek-R1 reasoning |
| 11 | 🧠 Thinking Generate | `thinking-generate.py` | Generation with reasoning |
| 12 | 🧠 Thinking Levels | `thinking-levels.py` | Different thinking levels |
| 13 | 💻 Fill in Middle | `fill-in-middle.py` | Code completion |

### 🖼️ Vision Examples (14-16)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 14 | 🖼️ Multimodal Chat | `multimodal-chat.py` | Image question-answering |
| 15 | 🖼️ Multimodal Generate | `multimodal-generate.py` | XKCD comic explanation |
| 16 | 🖼️ Structured Outputs Image | `structured-outputs-image.py` | Extract structured data from images |

### 🛠️ Tools Examples (17-21)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 17 | 🛠️ Tools | `tools.py` | Function calling basics |
| 18 | 🛠️ Async Tools | `async-tools.py` | Async function calling |
| 19 | 🛠️ Multi Tool | `multi-tool.py` | Multiple tool calls |
| 20 | 🛠️ GPT-OSS Tools | `gpt-oss-tools.py` | GPT-OSS integration |
| 21 | 🛠️ GPT-OSS Tools Stream | `gpt-oss-tools-stream.py` | Streaming with tools |

### 🌐 Web Search Examples (22-24)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 22 | 🌐 Web Search | `web-search.py` | Web search and fetch |
| 23 | 🌐 Web Search GPT-OSS | `web-search-gpt-oss.py` | Advanced browser tools |
| 24 | 🌐 Web Search MCP | `web-search-mcp.py` | MCP server integration |

### ⚙️ Utilities Examples (25-32)

| # | Page | Source | Description |
|---|------|--------|-------------|
| 25 | ⚙️ List | `list.py` | List available models |
| 26 | ⚙️ PS | `ps.py` | Process status (loaded models) |
| 27 | ⚙️ Show | `show.py` | Detailed model information |
| 28 | ⚙️ Pull | `pull.py` | Download models |
| 29 | ⚙️ Create | `create.py` | Create custom models |
| 30 | ⚙️ Embed | `embed.py` | Generate embeddings |
| 31 | ⚙️ Structured Outputs | `structured-outputs.py` | Structured JSON responses |
| 32 | ⚙️ Async Structured Outputs | `async-structured-outputs.py` | Async structured outputs |

## 🚀 Running the Application

### Prerequisites
1. Install Ollama: https://ollama.com/
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Pull required models:
   ```bash
   ollama pull gemma3
   ollama pull llama3.2
   ollama pull llama3.1
   ```

### Start the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Navigation

- Use the **sidebar** to select any of the 32 pages
- Each page has two tabs:
  - **🎯 Demo**: Try the interactive example
  - **📄 Source Code**: See the original implementation
- Configure settings in the sidebar (model selection, parameters, etc.)
- Experiment and learn!

## 🎯 Key Features

### Two-Tab Layout
Every page follows the same pattern:
1. **Demo Tab**: Interactive Streamlit UI for hands-on learning
2. **Source Code Tab**: Original Python code for reference

### Interactive Controls
- Model selection dropdowns
- Parameter adjustments (temperature, max tokens, etc.)
- File uploads for images
- Text inputs for prompts
- Buttons to trigger actions
- Real-time streaming visualizations

### Learning-Focused
- Clear titles and descriptions
- Inline documentation
- Example prompts pre-filled
- Tips and warnings where needed
- Error handling with helpful messages

## 💡 Tips

1. **Start Simple**: Begin with Chat (01) and Generate (06) examples
2. **Compare Models**: Try different models to see behavior differences
3. **Read Source**: Check the source code tab to understand implementation
4. **Experiment**: Modify parameters to see how they affect output
5. **Check Original**: Source files in `/src` have additional comments

## 🔧 Configuration

### Model Settings
Most pages allow you to configure:
- **Model**: Choose from gemma3, llama3.1, llama3.2, qwen3, etc.
- **Temperature**: 0.0 (deterministic) to 2.0 (very random)
- **Max Tokens**: Limit response length

### Ollama Settings
Configure Ollama server in `~/.ollama/config.json` or via environment variables:
- `OLLAMA_HOST`: Server address (default: http://localhost:11434)
- `OLLAMA_MODELS`: Model storage location

## 📖 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Model Library](https://ollama.com/library)

## 🐛 Troubleshooting

### Common Issues

**"Model not found"**
- Solution: Run `ollama pull <model-name>` first

**"Connection refused"**
- Solution: Make sure Ollama is running (`ollama serve`)

**"Out of memory"**
- Solution: Use smaller models or quantized versions

**Slow responses**
- Solution: Use smaller models or enable GPU acceleration

## 📝 Notes

- **Original scripts** are preserved in `/src` directory
- **Async examples** show synchronous alternatives (Streamlit limitation)
- **Web search** requires proper Ollama configuration
- **Vision models** need appropriate vision-capable models (llava, gemma3, etc.)
- **GPT-OSS examples** require GPT-OSS model installation

## 🤝 Contributing

To add new examples:
1. Add your script to `/src` directory
2. Create a new page file in `/pages` with two-tab structure
3. Update this README
4. Update main `app.py` if needed
5. Test thoroughly

Enjoy exploring the Ollama SDK! 🦙

## 🚀 Running the Application

### Prerequisites
1. Install Ollama: https://ollama.com/
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Pull required models:
   ```bash
   ollama pull gemma3
   ollama pull llama3.2
   ollama pull llama3.1
   ```

### Start the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📚 Navigation

- Use the **sidebar** to navigate between different pages
- Each page contains multiple tabs for related examples
- Configure settings in the sidebar of each page
- Experiment with different models and parameters

## 🎯 Key Features

### Interactive Examples
- All examples are interactive - no need to edit code
- Real-time feedback and results
- Visual output formatting

### Model Selection
- Choose from multiple models via dropdown
- Compare model behaviors
- Test with different model sizes

### Streaming Support
- See responses as they're generated
- Better user experience for long outputs
- Real-time progress indicators

### Error Handling
- Clear error messages
- Graceful degradation
- Helpful tips and warnings

## 💡 Tips

1. **Model Availability**: Make sure models are downloaded before using them
2. **Resource Usage**: Larger models require more RAM/VRAM
3. **Streaming**: Enable streaming for better UX with long responses
4. **Temperature**: Lower values (0-0.3) for deterministic outputs, higher (0.7-1.0) for creative
5. **Context**: Maintain chat history for coherent conversations

## 🔧 Configuration

### Model Settings
- **Temperature**: Controls randomness (0.0 = deterministic, 2.0 = very random)
- **Max Tokens**: Limits response length
- **Top P**: Nucleus sampling parameter
- **System Prompt**: Guides model behavior

### Ollama Settings
Configure Ollama server in `~/.ollama/config.json` or via environment variables:
- `OLLAMA_HOST`: Server address (default: http://localhost:11434)
- `OLLAMA_MODELS`: Model storage location

## 📖 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Model Library](https://ollama.com/library)

## 🐛 Troubleshooting

### Common Issues

**"Model not found"**
- Solution: Run `ollama pull <model-name>` first

**"Connection refused"**
- Solution: Make sure Ollama is running (`ollama serve`)

**"Out of memory"**
- Solution: Use smaller models or quantized versions

**Slow responses**
- Solution: Use smaller models or enable GPU acceleration

## 📝 Notes

- Original scripts are preserved in `/src` directory
- Each Streamlit page combines multiple related scripts
- Some advanced features (async, MCP) have limited support in Streamlit
- Web search requires appropriate Ollama configuration

## 🤝 Contributing

To add new examples:
1. Add your script to `/src` directory
2. Integrate it into the appropriate page in `/pages`
3. Update this README
4. Test thoroughly

Enjoy exploring the Ollama SDK! 🦙
