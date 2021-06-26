from numpy.core.fromnumeric import argmax
import torch
from transformers import AlbertForQuestionAnswering
from app.models.tokenization_kbalbert import KbAlbertCharTokenizer

MODEL_PATH = "app/models"

tokenizer = KbAlbertCharTokenizer.from_pretrained(MODEL_PATH)  
model = AlbertForQuestionAnswering.from_pretrained(MODEL_PATH)

class FinanceQA:
    def __init__(self, model: model, tokenizer: tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.inputs = None
        self.sentence_embedding = None
        self.tokens = None

    def tokenize(self, question, context):
        encoding = self.tokenizer.encode_plus(text=question, text_pair=context)
        self.inputs = encoding['input_ids'] # Token embeddings
        self.sentence_embedding = encoding['token_type_ids'] # Segment embeddings
        self.tokens = self.tokenizer.convert_ids_to_tokens(self.inputs) # Input tokens

    def get_answer(self, question, context):
        self.tokenize(question, context)
        
        start_scores, end_scores = self.model(input_ids=torch.tensor([self.inputs]), 
        token_type_ids=torch.tensor([self.sentence_embedding]))
        start_index = torch.argmax(start_scores)
        end_index = torch.argmax(end_scores)

        answer = ' '.join(self.tokens[start_index:end_index+1])
        corrected_answer = ''
        for word in answer.split():
            if word[0:2] == '##':
                corrected_answer += word[2:]
            else:
                corrected_answer += ' ' + word
        
        return corrected_answer
    

QAModel = FinanceQA(model, tokenizer)




