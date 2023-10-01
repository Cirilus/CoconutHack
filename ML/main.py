from tqdm.auto import tqdm
import pandas as pd
import torch
from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity

category_df = pd.read_csv('ML/catalog.csv',sep =',')

broad_categories = list(category_df['Категория'].unique())
narrow_categories = list(category_df['Тема'].unique())


# Load a pretrained model and tokenizer
model_name = "ai-forever/sbert_large_mt_nlu_ru"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).cpu()
classes_list = narrow_categories
# Initialize a list to store class embeddings
class_embeddings_list = []

# Iterate through each class description
for class_desc in tqdm(classes_list):
    # Encode the class description and compute the embeddings
    class_desc_encoded = tokenizer(f"Этот текст про {class_desc}", padding=True,max_length = 512, truncation=True, return_tensors="pt")
    class_embeddings = model(**class_desc_encoded).last_hidden_state.mean(dim=1)
    class_embeddings_list.append(class_embeddings)

# Convert the list of class embeddings into a tensor
class_embeddings = torch.cat(class_embeddings_list, dim=0)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def classify_by_embeddings(text):
    # Encode the text and compute the embeddings
    text_encoded = tokenizer(text, padding=True, max_length=512, truncation=True, return_tensors="pt")

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**text_encoded)

    # Perform pooling. In this case, mean pooling
    sentence_embeddings = mean_pooling(model_output, text_encoded['attention_mask'])
    similarity_matrix = cosine_similarity(sentence_embeddings, class_embeddings.detach().numpy())
    category = int(similarity_matrix.argmax(axis=1))
    return str(category_df[category_df['Тема'] == narrow_categories[category]].iloc[0, 0]), str(
        narrow_categories[category])
