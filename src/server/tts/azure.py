import textwrap

import requests


class AzureTTS:
    # https://learn.microsoft.com/en-us/azure/ai-services/speech-service/rest-text-to-speech?tabs=streaming
    def __init__(
        self, subscription_key: str, region: str, voice: str = "en-US-JessaNeural"
    ):
        self.subscription_key = subscription_key
        self.region = region
        self.voice = voice
        self.base_url = (
            f"https://{self.region}.tts.speech.microsoft.com/cognitiveservices/v1"
        )

    def synthesize(self, text, filename):
        # Synthesize the text to speech
        url = self.base_url
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
            "User-Agent": "tts",
        }
        body = textwrap.dedent(
            f"""\
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
                <voice name='{self.voice}'>
                    {text}
                </voice>
            </speak>"""
        )
        response = requests.post(url, headers=headers, data=body)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to synthesize speech: {response.text}")
