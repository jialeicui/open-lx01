"""
Text-to-Speech (TTS) module for Azure Speech Services.

This module provides easy-to-use interfaces for converting text to speech
using Azure Cognitive Services Speech API.

Classes:
    AzureTTS: Core Azure TTS client
    TTSService: High-level service interface
    AzureTTSError: Custom exception for TTS errors

Functions:
    get_tts_service: Factory function for creating TTS service instances

Example:
    >>> from common.config import AzureTTSConfig
    >>> from tts.service import TTSService
    >>>
    >>> config = AzureTTSConfig(
    ...     subscription_key="your_key",
    ...     region="eastus"
    ... )
    >>> service = TTSService(config)
    >>> audio_bytes = service.text_to_audio_bytes("Hello, world!")
"""

from .azure import AzureTTS, AzureTTSError
from .service import TTSService, get_tts_service

__all__ = ["AzureTTS", "AzureTTSError", "TTSService", "get_tts_service"]
