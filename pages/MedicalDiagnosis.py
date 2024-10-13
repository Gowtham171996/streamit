import transformers, torch

model_id = "ContactDoctor/Bio-Medical-Llama-3-8B"

pipeline = transformers.pipeline( "text-generation", model=model_id, model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto", )

messages = [ {"role": "system", "content": "You are an expert trained on healthcare and biomedical domain!"}, {"role": "user", "content": "I'm a 35-year-old male and for the past few months, I've been experiencing fatigue, increased sensitivity to cold, and dry, itchy skin. What is the diagnosis here?"}, ]

prompt = pipeline.tokenizer.apply_chat_template( messages, tokenize=False, add_generation_prompt=True )

terminators = [ pipeline.tokenizer.eos_token_id, pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>") ]

outputs = pipeline( prompt, max_new_tokens=256, eos_token_id=terminators, do_sample=True, temperature=0.6, top_p=0.9, ) 
print(outputs[0]["generated_text"][len(prompt):])