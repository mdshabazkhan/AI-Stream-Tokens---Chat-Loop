import sys
from openai import OpenAI

client = OpenAI()

def main():
    # 1. Initialize an empty history list
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("🤖 AI Streamer with Memory active!")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # 2. Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            print("AI: ", end="")
            
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=messages, # Send the WHOLE history now
                stream=True,
            )

            # 3. Track the full AI response as it streams
            full_response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content # Build the string token by token
                    print(content, end="")
                    sys.stdout.flush()

            # 4. Add the finished AI response to history
            messages.append({"role": "assistant", "content": full_response})
            print() 
            
        except Exception as e:
            print(f"\nError: {e}")
            break

if __name__ == "__main__":
    main()

