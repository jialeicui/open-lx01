"""
Tests for Azure TTS functionality.
"""

import os
import tempfile
import unittest.mock
from io import BytesIO

import pytest

from common.config import AzureTTSConfig
from tts.azure import AzureTTS, AzureTTSError
from tts.service import TTSService, get_tts_service


class TestAzureTTS:
    """Test cases for Azure TTS class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.subscription_key = "test_key"
        self.region = "eastus"
        self.voice = "en-US-JessaNeural"
        self.azure_tts = AzureTTS(
            subscription_key=self.subscription_key, region=self.region, voice=self.voice
        )

    def test_init(self):
        """Test Azure TTS initialization."""
        assert self.azure_tts.subscription_key == self.subscription_key
        assert self.azure_tts.region == self.region
        assert self.azure_tts.voice == self.voice
        assert "eastus.tts.speech.microsoft.com" in self.azure_tts.base_url
        assert "eastus.api.cognitive.microsoft.com" in self.azure_tts.token_url

    def test_build_ssml(self):
        """Test SSML building."""
        text = "Hello, world!"
        ssml = self.azure_tts._build_ssml(text)

        assert "speak version='1.0'" in ssml
        assert "en-US-JessaNeural" in ssml
        assert "Hello, world!" in ssml
        assert "xml:lang='en-US'" in ssml

    def test_build_ssml_with_custom_language(self):
        """Test SSML building with custom language."""
        text = "Bonjour le monde!"
        language = "fr-FR"
        ssml = self.azure_tts._build_ssml(text, language)

        assert f"xml:lang='{language}'" in ssml
        assert text in ssml

    @unittest.mock.patch("requests.post")
    def test_get_token_success(self, mock_post):
        """Test successful token acquisition."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.text = "mock_access_token"
        mock_post.return_value = mock_response

        token = self.azure_tts.get_token()

        assert token == "mock_access_token"
        assert self.azure_tts._access_token == "mock_access_token"

        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == self.azure_tts.token_url
        assert (
            call_args[1]["headers"]["Ocp-Apim-Subscription-Key"]
            == self.subscription_key
        )

    @unittest.mock.patch("requests.post")
    def test_get_token_failure(self, mock_post):
        """Test token acquisition failure."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        with pytest.raises(AzureTTSError, match="Failed to get access token: 401"):
            self.azure_tts.get_token()

    @unittest.mock.patch.object(AzureTTS, "get_token")
    @unittest.mock.patch("requests.post")
    def test_synthesize_to_bytes_success(self, mock_post, mock_get_token):
        """Test successful synthesis to bytes."""
        # Mock token
        mock_get_token.return_value = "mock_token"

        # Mock synthesis response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b"mock_audio_data"
        mock_post.return_value = mock_response

        text = "Hello, world!"
        result = self.azure_tts.synthesize_to_bytes(text)

        assert result == b"mock_audio_data"

        # Verify the request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == self.azure_tts.base_url
        assert call_args[1]["headers"]["Authorization"] == "Bearer mock_token"
        assert call_args[1]["headers"]["Content-Type"] == "application/ssml+xml"
        assert text in call_args[1]["data"]

    @unittest.mock.patch.object(AzureTTS, "get_token")
    @unittest.mock.patch("requests.post")
    def test_synthesize_to_bytes_failure(self, mock_post, mock_get_token):
        """Test synthesis failure."""
        # Mock token
        mock_get_token.return_value = "mock_token"

        # Mock synthesis response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        with pytest.raises(AzureTTSError, match="Failed to synthesize speech: 400"):
            self.azure_tts.synthesize_to_bytes("Hello, world!")

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_bytes")
    def test_synthesize_to_stream(self, mock_synthesize):
        """Test synthesis to stream."""
        mock_synthesize.return_value = b"mock_audio_data"

        result = self.azure_tts.synthesize_to_stream("Hello, world!")

        assert isinstance(result, BytesIO)
        assert result.read() == b"mock_audio_data"

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_bytes")
    def test_synthesize_to_file(self, mock_synthesize):
        """Test synthesis to file."""
        mock_synthesize.return_value = b"mock_audio_data"

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            self.azure_tts.synthesize_to_file("Hello, world!", tmp_path)

            with open(tmp_path, "rb") as f:
                content = f.read()

            assert content == b"mock_audio_data"
        finally:
            os.unlink(tmp_path)

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_file")
    def test_legacy_synthesize_method(self, mock_synthesize_to_file):
        """Test legacy synthesize method for backward compatibility."""
        self.azure_tts.synthesize("Hello, world!", "test.wav")

        mock_synthesize_to_file.assert_called_once_with("Hello, world!", "test.wav")


class TestTTSService:
    """Test cases for TTS service."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = AzureTTSConfig(
            subscription_key="test_key", region="eastus", voice="en-US-JessaNeural"
        )
        self.service = TTSService(self.config)

    def test_init(self):
        """Test TTS service initialization."""
        assert self.service.azure_tts is not None
        assert self.service.azure_tts.subscription_key == "test_key"
        assert self.service.azure_tts.region == "eastus"

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_stream")
    def test_text_to_audio_stream(self, mock_synthesize):
        """Test text to audio stream conversion."""
        mock_stream = BytesIO(b"mock_audio_data")
        mock_synthesize.return_value = mock_stream

        result = self.service.text_to_audio_stream("Hello, world!")

        assert result == mock_stream
        mock_synthesize.assert_called_once_with("Hello, world!", "en-US")

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_bytes")
    def test_text_to_audio_bytes(self, mock_synthesize):
        """Test text to audio bytes conversion."""
        mock_synthesize.return_value = b"mock_audio_data"

        result = self.service.text_to_audio_bytes("Hello, world!")

        assert result == b"mock_audio_data"
        mock_synthesize.assert_called_once_with("Hello, world!", "en-US")

    @unittest.mock.patch.object(AzureTTS, "synthesize_to_file")
    def test_text_to_audio_file(self, mock_synthesize):
        """Test text to audio file conversion."""
        self.service.text_to_audio_file("Hello, world!", "test.wav")

        mock_synthesize.assert_called_once_with("Hello, world!", "test.wav", "en-US")


class TestTTSServiceFactory:
    """Test cases for TTS service factory function."""

    def test_get_tts_service_with_config(self):
        """Test factory function with valid config."""
        config = AzureTTSConfig(subscription_key="test_key", region="eastus")

        service = get_tts_service(config)

        assert service is not None
        assert isinstance(service, TTSService)

    def test_get_tts_service_without_config(self):
        """Test factory function without config."""
        service = get_tts_service(None)

        assert service is None
