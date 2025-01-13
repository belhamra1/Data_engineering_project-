import random

def generate_text(prompt, max_length=50):
    # Simple text generation logic (just appending random words)
    random_words = ["the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog", "stars", "shine", "moon"]
    
    # Starting the generated text with the provided prompt
    generated_text = prompt
    
    # Simulating text generation by adding random words to the prompt
    for _ in range(max_length):
        generated_text += " " + random.choice(random_words)
    
    return generated_text

# Example usage
prompt = "Once upon a time in a distant galaxy"
generated_text = generate_text(prompt)

# Print the generated text
print(f"Generated Text:\n{generated_text}")
