import os
import json
from PyPDF2 import PdfFileReader
import torch
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration, TrainingArguments, Trainer, RagTokenForGeneration, RagConfig, DataCollatorForRag


def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfFileReader(file)
        text = ''
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()
        return text

pdf_dir = 'pdf_documents/'
data = []
for file_name in os.listdir(pdf_dir):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_dir, file_name)
        text = extract_text_from_pdf(file_path)
        data.append({'file_name': file_name, 'text': text})

with open('preprocessed_data.json', 'w') as file:
    json.dump(data, file)


tokenizer = RagTokenizer.from_pretrained('facebook/rag-token-base')
retriever = RagRetriever.from_pretrained('facebook/rag-token-base')
generator = RagSequenceForGeneration.from_pretrained('facebook/rag-token-base')


class PDFDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]['text']

dataset = PDFDataset(data)
data_collator = DataCollatorForRag(tokenizer=tokenizer, retriever=retriever)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=2, collate_fn=data_collator)

config = RagConfig()
model = RagTokenForGeneration(config=config)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.1)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(3):
    for batch in dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()


def generate_text(query, model, tokenizer, retriever, max_length=100):
    inputs_dict = tokenizer.prepare_seq2seq_batch([query], return_tensors='pt')
    inputs_dict = inputs_dict.to(device)
    generated = model.generate(input_ids=inputs_dict.input_ids, attention_mask=inputs_dict.attention_mask,
                               max_length=max_length, num_beams=4, retriever=retriever)
    return tokenizer.decode(generated[0], skip_special_tokens=True)

queries = ["What is the importance of renewable energy?", 
           "How does climate change affect biodiversity?"]

for query in queries:
    generated_text = generate_text(query, model, tokenizer, retriever)
    print("Query:", query)
    print("Generated Text:", generated_text)
    print()


output_dir = './rag_model'
os.makedirs(output_dir, exist_ok=True)
tokenizer.save_pretrained(output_dir)
retriever.save_pretrained(output_dir)
generator.save_pretrained(output_dir)
