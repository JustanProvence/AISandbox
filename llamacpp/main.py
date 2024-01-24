from llama_cpp import Llama
llm = Llama(model_path="./models/mistral/mistral-7b-v0.1.Q5_K_S.gguf")
output = llm(
      "Q: Name the planets in the solar system? A: ", # Prompt
      max_tokens=64, # Generate up to 32 tokens
      stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
      echo=True # Echo the prompt back in the output
) # Generate a completion, can also call create_completion

print(output)
