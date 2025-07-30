#!/usr/bin/env python3
"""
Azure TTS Demo Script

This script demonstrates how to use the Azure Text-to-Speech functionality.
Users can fill in their Azure credentials and test the TTS functionality.

Usage:
    python demo_azure_tts.py

Environment Variables:
    AZURE_TTS_SUBSCRIPTION_KEY: Your Azure Speech service subscription key
    AZURE_TTS_REGION: Your Azure region (e.g., 'eastus', 'westus2')
    AZURE_TTS_VOICE: Voice name (optional, default: 'en-US-JessaNeural')

Example:
    export AZURE_TTS_SUBSCRIPTION_KEY="your_subscription_key_here"
    export AZURE_TTS_REGION="eastus"
    python demo_azure_tts.py
"""

import argparse
import os
import sys
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from common.config import AzureTTSConfig
from tts.azure import AzureTTSError
from tts.service import TTSService


def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(
        description="Azure TTS Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--text",
        default="Hello! This is a test of Azure Text to Speech service. The audio generation is working correctly!",
        help="Text to synthesize (default: sample text)",
    )
    parser.add_argument(
        "--output",
        default="demo_output.wav",
        help="Output audio file path (default: demo_output.wav)",
    )
    parser.add_argument("--voice", help="Voice name (overrides environment variable)")
    parser.add_argument(
        "--language", default="en-US", help="Language code (default: en-US)"
    )
    parser.add_argument(
        "--subscription-key",
        help="Azure subscription key (overrides environment variable)",
    )
    parser.add_argument(
        "--region", help="Azure region (overrides environment variable)"
    )
    parser.add_argument(
        "--stream-demo",
        action="store_true",
        help="Demonstrate streaming functionality by returning audio as bytes",
    )

    args = parser.parse_args()

    # Get configuration from environment variables or command line arguments
    subscription_key = args.subscription_key or os.getenv("AZURE_TTS_SUBSCRIPTION_KEY")
    region = args.region or os.getenv("AZURE_TTS_REGION")
    voice = args.voice or os.getenv("AZURE_TTS_VOICE", "en-US-JessaNeural")

    if not subscription_key:
        print("❌ Error: Azure subscription key not provided!")
        print(
            "Please set AZURE_TTS_SUBSCRIPTION_KEY environment variable or use --subscription-key"
        )
        print("\nExample:")
        print("  export AZURE_TTS_SUBSCRIPTION_KEY='your_key_here'")
        print("  python demo_azure_tts.py")
        return 1

    if not region:
        print("❌ Error: Azure region not provided!")
        print("Please set AZURE_TTS_REGION environment variable or use --region")
        print("\nExample:")
        print("  export AZURE_TTS_REGION='eastus'")
        print("  python demo_azure_tts.py")
        return 1

    print("🎤 Azure TTS Demo Starting...")
    print(f"📝 Text: {args.text}")
    print(f"🗣️  Voice: {voice}")
    print(f"🌍 Language: {args.language}")
    print(f"📍 Region: {region}")
    print("-" * 50)

    try:
        # Create configuration
        config = AzureTTSConfig(
            subscription_key=subscription_key, region=region, voice=voice
        )

        # Create TTS service
        tts_service = TTSService(config)

        if args.stream_demo:
            print("🔄 Testing streaming functionality...")

            # Get audio as bytes
            audio_bytes = tts_service.text_to_audio_bytes(args.text, args.language)
            print(f"✅ Successfully generated {len(audio_bytes)} bytes of audio data")

            # Also save to file
            with open(args.output, "wb") as f:
                f.write(audio_bytes)
            print(f"💾 Audio saved to: {args.output}")

            # Test stream method
            audio_stream = tts_service.text_to_audio_stream(args.text, args.language)
            stream_data = audio_stream.read()
            print(f"🌊 Stream method returned {len(stream_data)} bytes")

        else:
            print("💾 Generating audio file...")

            # Generate audio file
            tts_service.text_to_audio_file(args.text, args.output, args.language)
            print(f"✅ Audio successfully generated: {args.output}")

        # Check if file exists and show size
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"📊 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

            print("\n🎵 You can now play the audio file with:")
            print(f"  - VLC: vlc {args.output}")
            print(f"  - Windows: start {args.output}")
            print(f"  - macOS: open {args.output}")
            print(f"  - Linux: xdg-open {args.output}")

        print("\n✨ Demo completed successfully!")
        return 0

    except AzureTTSError as e:
        print(f"❌ Azure TTS Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your subscription key is correct")
        print("2. Verify your Azure region is correct")
        print("3. Ensure your Azure Speech service is active")
        print("4. Check your internet connection")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
