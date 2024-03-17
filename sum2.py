from transformers import T5ForConditionalGeneration, T5Tokenizer, pipeline

# Load the model and tokenizer from the local directory
model = T5ForConditionalGeneration.from_pretrained('./my_t5_model')
tokenizer = T5Tokenizer.from_pretrained('./my_t5_model')

# Create the summarization pipeline using the locally loaded model and tokenizer
summarizer = pipeline('summarization', model=model, tokenizer=tokenizer)

