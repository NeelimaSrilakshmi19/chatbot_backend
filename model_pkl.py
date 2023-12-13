import pickle
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

# Function to load the model and vectorizer using pickle
def load_model_and_vectorizer_pickle(model_filename, vectorizer_filename):
    with open(model_filename, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    
    with open(vectorizer_filename, 'rb') as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    
    return loaded_model, loaded_vectorizer

def extractive_summarization(document, num_sentences=1):
    sentences = document.split('. ')
    summary = '. '.join(sentences[:num_sentences])

    return summary

def retrieve_documents_with_summary_loaded_pickle(user_query, model, vectorizer, df, num_documents=10, num_summary_sentences=2):
    query_vector = vectorizer.transform([user_query])
    predicted_topic = model.predict(query_vector)[0]
    topic_documents = df[df['topic'] == predicted_topic]

    # Check if there are no documents for the predicted topic
    if topic_documents.empty:
        print("No documents found for the predicted topic.")
        return None, None

    topic_vectors = vectorizer.transform(topic_documents['summary'])

    # Check if there are not enough documents for the specified number
    if topic_vectors.getnnz() < num_documents:
        print(f"Not enough documents for the specified number ({num_documents}). Using all available documents.")
        num_documents = topic_vectors.getnnz()

    cosine_similarities = linear_kernel(query_vector, topic_vectors).flatten()

    # Check if there are not enough documents for the specified number
    if len(cosine_similarities) < num_documents:
        print(f"Not enough cosine similarities for the specified number ({num_documents}). Using all available similarities.")
        num_documents = len(cosine_similarities)

    top_document_indices = cosine_similarities.argsort()[:-num_documents-1:-1]
    top_summary = None
    top_topic = None

    for idx in top_document_indices:
        doc_info = topic_documents.iloc[idx]['summary']
        if top_summary is None:
            top_summary = extractive_summarization(doc_info, num_sentences=num_summary_sentences)
            top_topic = topic_documents.iloc[idx]['topic']
            #print(top_topic)

    return top_summary, top_topic

# Example of how to use the loaded model and vectorizer
loaded_classifier, loaded_vectorizer = load_model_and_vectorizer_pickle('logistic_regression_model.pkl', 'count_vectorizer.pkl')
user_query = "what is tourism"
df = pd.read_csv('abc.csv')
top_summary, top_topic = retrieve_documents_with_summary_loaded_pickle(user_query, loaded_classifier, loaded_vectorizer, df)

# Print the result
print("Top Document Summary:")
print(top_summary)
print("Top Topic:")
print(top_topic)
