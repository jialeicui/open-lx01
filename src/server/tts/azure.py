import textwrap
import typing
from io import BytesIO

import requests


class AzureTTSError(Exception):
    """Custom exception for Azure TTS errors."""

    pass


class AzureTTS:
    """
    Azure Text-to-Speech service client.

    Supports both file output and streaming audio generation.
    Reference: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech
    """

    def __init__(
        self,
        subscription_key: str,
        region: str,
        voice: str = "en-US-JessaNeural",
        output_format: str = "riff-24khz-16bit-mono-pcm",
    ):
        """
        Initialize Azure TTS client.

        Args:
            subscription_key: Azure Speech service subscription key
            region: Azure region (e.g., 'eastus', 'westus2')
            voice: Voice name for synthesis (default: en-US-JessaNeural)
            output_format: Audio output format
        """
        self.subscription_key = subscription_key
        self.region = region
        self.voice = voice
        self.output_format = output_format
        self.base_url = (
            f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        )
        self.token_url = (
            f"https://{self.region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        )
        self._access_token: typing.Optional[str] = None

    def get_token(self) -> str:
        """
        Get access token for Azure Speech Service.

        Returns:
            Access token string

        Raises:
            AzureTTSError: If token acquisition fails
        """
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-type": "application/x-www-form-urlencoded",
        }

        response = requests.post(self.token_url, headers=headers)

        if response.status_code == 200:
            self._access_token = response.text
            return self._access_token
        else:
            raise AzureTTSError(
                f"Failed to get access token: {response.status_code} - {response.text}"
            )

    def _build_ssml(self, text: str, language: str = "en-US") -> str:
        """
        Build SSML markup for the given text.

        Args:
            text: Text to synthesize
            language: Language code

        Returns:
            SSML markup string
        """
        return textwrap.dedent(
            f"""\
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='{language}'>
                <voice name='{self.voice}'>
                    {text}
                </voice>
            </speak>"""
        )

    def synthesize_to_file(
        self, text: str, filename: str, language: str = "en-US"
    ) -> None:
        """
        Synthesize text to speech and save to a file.

        Args:
            text: Text to synthesize
            filename: Output file path
            language: Language code

        Raises:
            AzureTTSError: If synthesis fails
        """
        audio_data = self.synthesize_to_bytes(text, language)

        with open(filename, "wb") as f:
            f.write(audio_data)

    def synthesize_to_bytes(self, text: str, language: str = "en-US") -> bytes:
        """
        Synthesize text to speech and return audio data as bytes.

        Args:
            text: Text to synthesize
            language: Language code

        Returns:
            Audio data as bytes

        Raises:
            AzureTTSError: If synthesis fails
        """
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": self.output_format,
            "User-Agent": "open-lx01-tts",
        }

        ssml_body = self._build_ssml(text, language)

        response = requests.post(self.base_url, headers=headers, data=ssml_body)

        if response.status_code == 200:
            return response.content
        else:
            raise AzureTTSError(
                f"Failed to synthesize speech: {response.status_code} - {response.text}"
            )

    def synthesize_to_stream(self, text: str, language: str = "en-US") -> BytesIO:
        """
        Synthesize text to speech and return as a BytesIO stream.

        Args:
            text: Text to synthesize
            language: Language code

        Returns:
            BytesIO stream containing audio data

        Raises:
            AzureTTSError: If synthesis fails
        """
        audio_data = self.synthesize_to_bytes(text, language)
        return BytesIO(audio_data)

    # Backward compatibility with existing method name
    def synthesize(self, text: str, filename: str) -> None:
        """
        Legacy method for backward compatibility.

        Args:
            text: Text to synthesize
            filename: Output file path
        """
        self.synthesize_to_file(text, filename)
