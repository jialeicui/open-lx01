"""
Example integration of Azure TTS with the main application.

This shows how the TTS service can be integrated into the existing
LLM response flow to generate audio for responses.
"""

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from common.config import load_config
from tts.service import get_tts_service
from tts.azure import AzureTTSError


# Load configuration and TTS service at module level
config = load_config()
tts_service = get_tts_service(config.azure_tts)


def create_tts_endpoints(app):
    """
    Add TTS endpoints to the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.post("/tts/synthesize")
    async def synthesize_text(text: str, voice: str = None, language: str = "en-US"):
        """
        Synthesize text to speech and return audio file.
        
        Args:
            text: Text to synthesize
            voice: Voice name (optional, uses default from config)
            language: Language code (default: en-US)
            
        Returns:
            Audio file as streaming response
        """
        if not tts_service:
            raise HTTPException(
                status_code=503, 
                detail="Azure TTS not configured. Please set AZURE_TTS_SUBSCRIPTION_KEY and AZURE_TTS_REGION environment variables."
            )
        
        try:
            # Override voice if specified
            if voice:
                tts_service.azure_tts.voice = voice
            
            # Generate audio
            audio_stream = tts_service.text_to_audio_stream(text, language)
            
            # Return as streaming response
            return StreamingResponse(
                BytesIO(audio_stream.read()),
                media_type="audio/wav",
                headers={"Content-Disposition": "attachment; filename=tts_output.wav"}
            )
            
        except AzureTTSError as e:
            raise HTTPException(status_code=500, detail=f"TTS Error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
    @app.get("/tts/status")
    async def tts_status():
        """
        Check if TTS service is available.
        
        Returns:
            TTS service status information
        """
        if tts_service:
            return {
                "available": True,
                "region": tts_service.azure_tts.region,
                "voice": tts_service.azure_tts.voice,
                "output_format": tts_service.azure_tts.output_format
            }
        else:
            return {
                "available": False,
                "message": "Azure TTS not configured. Set AZURE_TTS_SUBSCRIPTION_KEY and AZURE_TTS_REGION environment variables."
            }
    
    @app.get("/tts/voices")
    async def list_common_voices():
        """
        Return a list of commonly used voices.
        
        Returns:
            Dictionary of voices organized by language
        """
        return {
            "english": {
                "en-US-JessaNeural": "Jessa (US, Female)",
                "en-US-BrandonNeural": "Brandon (US, Male)",
                "en-US-MichelleNeural": "Michelle (US, Female)",
                "en-GB-LibbyNeural": "Libby (UK, Female)",
                "en-AU-NatashaNeural": "Natasha (Australian, Female)"
            },
            "chinese": {
                "zh-CN-XiaoxiaoNeural": "Xiaoxiao (Mainland, Female)",
                "zh-CN-YunxiNeural": "Yunxi (Mainland, Male)",
                "zh-CN-YunyangNeural": "Yunyang (Mainland, Male)"
            },
            "other": {
                "fr-FR-DeniseNeural": "Denise (French, Female)",
                "de-DE-KatjaNeural": "Katja (German, Female)",
                "es-ES-ElviraNeural": "Elvira (Spanish, Female)",
                "ja-JP-NanamiNeural": "Nanami (Japanese, Female)"
            }
        }


def enhance_llm_response_with_tts(llm_response_text: str) -> dict:
    """
    Enhance LLM response with TTS audio if service is available.
    
    Args:
        llm_response_text: Text response from LLM
        
    Returns:
        Dictionary with text response and optional audio data
    """
    result = {
        "text": llm_response_text,
        "has_audio": False,
        "audio_data": None
    }
    
    if tts_service and llm_response_text:
        try:
            # Generate audio for the response
            audio_bytes = tts_service.text_to_audio_bytes(llm_response_text)
            result["has_audio"] = True
            result["audio_data"] = audio_bytes
            result["audio_size"] = len(audio_bytes)
        except AzureTTSError:
            # TTS failed, but we still have text response
            pass
    
    return result


# Example usage in message handler
def example_enhanced_message_handler(text: str) -> dict:
    """
    Example of how to integrate TTS into the existing message flow.
    
    Args:
        text: Input text from user
        
    Returns:
        Enhanced response with optional audio
    """
    # This would be replaced with actual LLM call
    llm_response = f"I heard you say: {text}. This is my response."
    
    # Enhance with TTS
    enhanced_response = enhance_llm_response_with_tts(llm_response)
    
    return enhanced_response