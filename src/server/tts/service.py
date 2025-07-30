"""
Azure TTS service module for easy integration and dependency injection.
"""

import typing
from io import BytesIO

from common.config import AzureTTSConfig
from tts.azure import AzureTTS


class TTSService:
    """Text-to-Speech service interface."""

    def __init__(self, azure_config: AzureTTSConfig):
        """
        Initialize TTS service with Azure configuration.

        Args:
            azure_config: Azure TTS configuration
        """
        self.azure_tts = AzureTTS(
            subscription_key=azure_config.subscription_key,
            region=azure_config.region,
            voice=azure_config.voice,
            output_format=azure_config.output_format,
        )

    def text_to_audio_stream(self, text: str, language: str = "en-US") -> BytesIO:
        """
        Convert text to audio stream.

        Args:
            text: Text to synthesize
            language: Language code

        Returns:
            BytesIO stream containing audio data

        Raises:
            AzureTTSError: If synthesis fails
        """
        return self.azure_tts.synthesize_to_stream(text, language)

    def text_to_audio_bytes(self, text: str, language: str = "en-US") -> bytes:
        """
        Convert text to audio bytes.

        Args:
            text: Text to synthesize
            language: Language code

        Returns:
            Audio data as bytes

        Raises:
            AzureTTSError: If synthesis fails
        """
        return self.azure_tts.synthesize_to_bytes(text, language)

    def text_to_audio_file(
        self, text: str, filename: str, language: str = "en-US"
    ) -> None:
        """
        Convert text to audio file.

        Args:
            text: Text to synthesize
            filename: Output file path
            language: Language code

        Raises:
            AzureTTSError: If synthesis fails
        """
        self.azure_tts.synthesize_to_file(text, filename, language)


def get_tts_service(
    azure_config: typing.Optional[AzureTTSConfig],
) -> typing.Optional[TTSService]:
    """
    Factory function to create TTS service if configuration is available.

    Args:
        azure_config: Azure TTS configuration

    Returns:
        TTSService instance if config is provided, None otherwise
    """
    if azure_config is None:
        return None

    return TTSService(azure_config)
