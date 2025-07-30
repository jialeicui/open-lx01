# Azure Text-to-Speech (TTS) Implementation

This module provides Azure Text-to-Speech functionality for the Open-LX01 project, enabling audio stream generation from text using Azure Cognitive Services Speech API.

## Features

- ✅ **Streaming Audio Generation**: Generate audio as bytes, streams, or files
- ✅ **Modular Design**: Clean separation of concerns with service layer
- ✅ **Comprehensive Testing**: Full test coverage with mocked Azure API calls
- ✅ **Easy Configuration**: Environment variable based configuration
- ✅ **Error Handling**: Custom exceptions for robust error management
- ✅ **Demo Script**: Ready-to-use demo for testing with your Azure credentials

## Quick Start

### 1. Set Environment Variables

```bash
export AZURE_TTS_SUBSCRIPTION_KEY="your_azure_subscription_key"
export AZURE_TTS_REGION="eastus"  # or your preferred region
export AZURE_TTS_VOICE="en-US-JessaNeural"  # optional
```

### 2. Run the Demo

```bash
cd src/server
python demo_azure_tts.py
```

### 3. Use in Your Code

```python
from common.config import AzureTTSConfig
from tts.service import TTSService

# Create configuration
config = AzureTTSConfig(
    subscription_key="your_key",
    region="eastus",
    voice="en-US-JessaNeural"
)

# Create service
tts_service = TTSService(config)

# Generate audio as bytes (for streaming)
audio_bytes = tts_service.text_to_audio_bytes("Hello, world!")

# Generate audio as stream
audio_stream = tts_service.text_to_audio_stream("Hello, world!")

# Generate audio file
tts_service.text_to_audio_file("Hello, world!", "output.wav")
```

## API Reference

### AzureTTS Class

The core Azure TTS client that handles direct Azure API communication.

```python
from tts.azure import AzureTTS

tts = AzureTTS(
    subscription_key="your_key",
    region="eastus",
    voice="en-US-JessaNeural",
    output_format="riff-24khz-16bit-mono-pcm"
)

# Get audio as bytes
audio_bytes = tts.synthesize_to_bytes("Hello, world!")

# Get audio as stream
audio_stream = tts.synthesize_to_stream("Hello, world!")

# Save to file
tts.synthesize_to_file("Hello, world!", "output.wav")
```

### TTSService Class

High-level service interface that provides a cleaner API.

```python
from tts.service import TTSService, get_tts_service
from common.config import AzureTTSConfig

# Direct instantiation
config = AzureTTSConfig(subscription_key="key", region="region")
service = TTSService(config)

# Factory method
service = get_tts_service(config)  # Returns None if config is None
```

### Configuration

Azure TTS configuration is handled through the `AzureTTSConfig` class:

```python
from common.config import AzureTTSConfig

config = AzureTTSConfig(
    subscription_key="your_azure_subscription_key",
    region="eastus",  # Azure region
    voice="en-US-JessaNeural",  # Voice name
    output_format="riff-24khz-16bit-mono-pcm"  # Audio format
)
```

## Supported Audio Formats

The implementation supports various Azure TTS output formats:

- `riff-24khz-16bit-mono-pcm` (default)
- `riff-16khz-16bit-mono-pcm`
- `audio-24khz-48kbitrate-mono-mp3`
- `audio-16khz-32kbitrate-mono-mp3`
- And many more...

## Supported Voices

Azure TTS supports hundreds of voices across multiple languages. Some popular examples:

### English
- `en-US-JessaNeural` (default)
- `en-US-BrandonNeural`
- `en-US-MichelleNeural`
- `en-GB-LibbyNeural`
- `en-AU-NatashaNeural`

### Chinese
- `zh-CN-XiaoxiaoNeural`
- `zh-CN-YunxiNeural`
- `zh-CN-YunyangNeural`

### Other Languages
- `fr-FR-DeniseNeural` (French)
- `de-DE-KatjaNeural` (German)
- `es-ES-ElviraNeural` (Spanish)
- `ja-JP-NanamiNeural` (Japanese)

For a complete list, see [Azure TTS Voice Gallery](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#neural-voices).

## Demo Script Options

The demo script supports various options:

```bash
# Basic usage
python demo_azure_tts.py

# Custom text
python demo_azure_tts.py --text "Your custom text here"

# Different voice
python demo_azure_tts.py --voice "zh-CN-XiaoxiaoNeural" --language "zh-CN"

# Stream demo (shows bytes generation)
python demo_azure_tts.py --stream-demo

# Command line credentials (alternative to env vars)
python demo_azure_tts.py --subscription-key "your_key" --region "eastus"
```

## Error Handling

The module provides custom exception handling:

```python
from tts.azure import AzureTTSError

try:
    audio_bytes = tts_service.text_to_audio_bytes("Hello")
except AzureTTSError as e:
    print(f"TTS Error: {e}")
    # Handle the error (check credentials, network, etc.)
```

Common error scenarios:
- Invalid subscription key
- Wrong region
- Network connectivity issues
- Invalid voice name
- Rate limiting

## Testing

Run the comprehensive test suite:

```bash
# Run all TTS tests
python -m pytest tests/test_azure_tts.py -v

# Run with coverage
python -m pytest tests/test_azure_tts.py --cov=tts --cov-report=html
```

The tests cover:
- Azure TTS class functionality
- Service layer functionality
- Error handling
- Configuration management
- Mocked Azure API interactions

## Integration with Open-LX01

The TTS service integrates seamlessly with the existing Open-LX01 configuration system:

```python
from common.config import load_config
from tts.service import get_tts_service

# Load configuration (includes Azure TTS if env vars are set)
config = load_config()

# Get TTS service (None if not configured)
tts_service = get_tts_service(config.azure_tts)

if tts_service:
    # TTS is available
    audio_bytes = tts_service.text_to_audio_bytes("Hello from Open-LX01!")
else:
    # TTS not configured
    print("Azure TTS not configured")
```

## Azure Setup

To use this functionality, you need:

1. **Azure Subscription**: Create an Azure account if you don't have one
2. **Speech Service**: Create a Speech service resource in Azure Portal
3. **Subscription Key**: Get your subscription key from the resource
4. **Region**: Note the region where you created the resource

### Azure Portal Steps:
1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new resource → AI + Machine Learning → Speech
3. Fill in the details and create the resource
4. Go to your Speech resource → Keys and Endpoint
5. Copy Key 1 (your subscription key) and Region

## Troubleshooting

### Common Issues

1. **"Failed to get access token: 401"**
   - Check your subscription key is correct
   - Verify the key is for the Speech service (not other Azure services)

2. **"Failed to get access token: 403"**
   - Check your Azure subscription is active
   - Verify the Speech service resource is running

3. **"Failed to synthesize speech: 400"**
   - Check the voice name is correct and supported
   - Verify the text is not too long (max ~5000 characters)

4. **"Failed to synthesize speech: 429"**
   - You're hitting rate limits
   - Wait a moment and try again
   - Consider upgrading your Azure pricing tier

### Debug Mode

Enable debug logging to see detailed HTTP requests:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run your TTS code
```

## Performance Considerations

- **Caching**: The module caches access tokens for efficiency
- **Rate Limits**: Azure has rate limits; consider implementing retry logic for production
- **Audio Size**: Generated audio size depends on text length and format
- **Network**: Requires internet connectivity to Azure services

## Contributing

When contributing to the TTS functionality:

1. Add tests for new features
2. Update this documentation
3. Follow the existing code style
4. Test with real Azure credentials when possible
5. Consider backward compatibility

## License

This module is part of the Open-LX01 project and follows the same license terms.