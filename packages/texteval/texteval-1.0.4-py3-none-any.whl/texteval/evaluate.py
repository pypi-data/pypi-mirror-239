
import nltk
from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Evaluator:
    def __init__(self):
        self.rouge = Rouge()
        self.tfidf_vectorizer = TfidfVectorizer()
        nltk.download('punkt')

    def rouge_evaluation(self, system_summary: str, reference_summary: str) -> dict:
        scores = self.rouge.get_scores(system_summary, reference_summary)
        return scores[0]  # Extract the ROUGE scores

    def bleu_evaluation(self, system_summary: str, reference_summary: str) -> float:
        reference = [reference_summary.split()]
        candidate = system_summary.split()
        bleu_score = nltk.translate.bleu_score.sentence_bleu(reference, candidate)
        return bleu_score

    def cosine_similarity_evaluation(self, system_summary: str, input_text: str) -> float:
        tfidf_matrix = self.tfidf_vectorizer.fit_transform([system_summary, input_text])
        cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
        return cosine_sim[0][0]





