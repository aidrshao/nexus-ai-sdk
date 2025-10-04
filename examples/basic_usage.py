"""
Basic usage examples for Nexus AI SDK.

This demonstrates the core features of the SDK with simple examples.
"""

from nexusai import NexusAIClient


def main():
    """Run basic usage examples."""
    # Initialize client (reads from .env file)
    print("Initializing Nexus AI client...")
    client = NexusAIClient()

    # Example 1: Text Generation (Simple Mode)
    print("\n=== Example 1: Text Generation (Simple Mode) ===")
    try:
        response = client.text.generate(
            prompt="写一首关于春天的短诗，不超过4行",
            temperature=0.7,
            max_tokens=100,
        )
        print(f"Generated text:\n{response.text}")
        if response.usage:
            print(f"Tokens used: {response.usage.total_tokens}")
    except Exception as e:
        print(f"Error: {e}")

    # Example 2: Streaming Text Generation
    print("\n=== Example 2: Streaming Text Generation ===")
    try:
        print("Streaming response: ", end="", flush=True)
        for chunk in client.text.stream(
            prompt="用一句话介绍人工智能",
            max_tokens=50,
        ):
            if "delta" in chunk and "content" in chunk["delta"]:
                print(chunk["delta"]["content"], end="", flush=True)
        print()  # New line
    except Exception as e:
        print(f"Error: {e}")

    # Example 3: Create and Use Session
    print("\n=== Example 3: Session Management ===")
    try:
        # Create session
        session = client.sessions.create(
            name="Test Session",
            agent_config={
                "temperature": 0.7,
                "system_prompt": "You are a helpful assistant.",
            },
        )
        print(f"Created session: {session.id}")

        # First message
        response1 = session.invoke("我叫小明")
        print(f"Assistant: {response1.response.content}")

        # Second message - session remembers context
        response2 = session.invoke("我叫什么名字?")
        print(f"Assistant: {response2.response.content}")

        # Get history
        history = session.history(limit=5)
        print(f"Conversation history: {len(history)} messages")

        # Clean up
        session.delete()
        print("Session deleted")
    except Exception as e:
        print(f"Error: {e}")

    # Example 4: Image Generation
    print("\n=== Example 4: Image Generation ===")
    try:
        print("Generating image (this may take a while)...")
        image = client.images.generate(
            prompt="A beautiful sunset over mountains, digital art",
            size="1024x1024",
        )
        print(f"Image generated: {image.image_url}")
        print(f"Dimensions: {image.width}x{image.height}")
    except Exception as e:
        print(f"Error: {e}")

    # Close client
    client.close()
    print("\n=== Examples completed ===")


if __name__ == "__main__":
    main()
