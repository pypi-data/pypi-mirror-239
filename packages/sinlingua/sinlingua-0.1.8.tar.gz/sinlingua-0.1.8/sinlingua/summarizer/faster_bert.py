# -*- coding: utf-8 -*-
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sinling import SinhalaTokenizer
from googletrans import Translator
import numpy as np
import string
from sklearn.metrics.pairwise import cosine_similarity

punctuation = set(string.punctuation)
stopwords = ["සහ",
    "සමග",
    "සමඟ",
    "අහා",
    "ආහ්",
    "ආ",
    "ඕහෝ",
    "අනේ",
    "අඳෝ",
    "අපොයි",
    "අපෝ",
    "අයියෝ",
    "ආයි",
    "ඌයි",
    "චී",
    "චිහ්",
    "චික්",
    "හෝ‍",
    "දෝ",
    "දෝහෝ",
    "මෙන්",
    "සේ",
    "වැනි",
    "බඳු",
    "වන්",
    "අයුරු",
    "අයුරින්",
    "ලෙස",
    "වැඩි",
    "ශ්‍රී",
    "හා",
    "ය",
    "නිසා",
    "නිසාවෙන්",
    "බවට",
    "බව",
    "බවෙන්",
    "නම්",
    "වැඩි",
    "සිට",
    "දී",
    "මහා",
    "මහ",
    "පමණ",
    "පමණින්",
    "පමන",
    "වන",
    "විට",
    "විටින්",
    "මේ",
    "මෙලෙස",
    "මෙයින්",
    "ඇති",
    "ලෙස",
    "සිදු",
    "වශයෙන්",
    "යන",
    "සඳහා",
    "මගින්",
    "හෝ‍",
    "ඉතා",
    "ඒ",
    "එම",
    "ද",
    "අතර",
    "විසින්",
    "සමග",
    "පිළිබඳව",
    "පිළිබඳ",
    "තුළ",
    "බව",
    "වැනි",
    "මහ",
    "මෙම",
    "මෙහි",
    "මේ",
    "වෙත",
    "වෙතින්",
    "වෙතට",
    "වෙනුවෙන්",
    "වෙනුවට",
    "වෙන",
    "ගැන",
    "නෑ",
    "අනුව",
    "නව",
    "පිළිබඳ",
    "විශේෂ",
    "දැනට",
    "එහෙන්",
    "මෙහෙන්",
    "එහේ",
    "මෙහේ",
    "ම",
    "තවත්",
    "තව",
    "සහ",
    "දක්වා",
    "ට",
    "ගේ",
    "එ",
    "ක",
    "ක්",
    "බවත්",
    "බවද",
    "මත",
    "ඇතුලු",
    "ඇතුළු",
    "මෙසේ",
    "වඩා",
    "වඩාත්ම",
    "නිති",
    "නිතිත්",
    "නිතොර",
    "නිතර",
    "ඉක්බිති",
    "දැන්",
    "යලි",
    "පුන",
    "ඉතින්",
    "සිට",
    "සිටන්",
    "පටන්",
    "තෙක්",
    "දක්වා",
    "සා",
    "තාක්",
    "තුවක්",
    "පවා",
    "ද",
    "හෝ‍",
    "වත්",
    "විනා",
    "හැර",
    "මිස",
    "මුත්",
    "කිම",
    "කිම්",
    "ඇයි",
    "මන්ද",
    "හෙවත්",
    "නොහොත්",
    "පතා",
    "පාසා",
    "ගානෙ",
    "තව",
    "ඉතා",
    "බොහෝ",
    "වහා",
    "සෙද",
    "සැනින්",
    "හනික",
    "එම්බා",
    "එම්බල",
    "බොල",
    "නම්",
    "වනාහි",
    "කලී",
    "ඉඳුරා",
    "අන්න",
    "ඔන්න",
    "මෙන්න",
    "උදෙසා",
    "පිණිස",
    "සඳහා",
    "අරබයා",
    "නිසා",
    "එනිසා",
    "එබැවින්",
    "බැවින්",
    "හෙයින්",
    "සේක්",
    "සේක",
    "ගැන",
    "අනුව",
    "පරිදි",
    "විට",
    "තෙක්",
    "මෙතෙක්",
    "මේතාක්",
    "තුරු",
    "තුරා",
    "තුරාවට",
    "තුලින්",
    "නමුත්",
    "එනමුත්",
    "වස්",
    "මෙන්",
    "ලෙස",
    "පරිදි",
    "එහෙත්"]  # Define the Sinhala stopword list

class FBertTextSummarizer:
    def __init__(self, batch_size=5):
        self.tokenizer = SinhalaTokenizer()
        self.stopwords = stopwords
        self.punctuation = punctuation
        self.distilbert_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
        self.distilbert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')
        self.translator = Translator()
        self.batch_size = batch_size

    def __preprocess_sentences(self, text_corpus):
        sentences = self.tokenizer.split_sentences(text_corpus)
        sentences = [sent.strip() for sent in sentences]
        cleaned = [sent for sent in sentences if sent not in self.stopwords and sent not in self.punctuation]
        return cleaned, sentences

    def __create_distilbert_embeddings(self, cleaned_sentences):
        sentence_embeddings = []
        for i in range(0, len(cleaned_sentences), self.batch_size):
            batch = cleaned_sentences[i:i+self.batch_size]
            inputs = self.distilbert_tokenizer(batch, return_tensors="pt", max_length=512, truncation=True, padding='max_length', add_special_tokens=True)
            with torch.no_grad():
                outputs = self.distilbert_model(**inputs)
            embeddings = [output.mean(dim=1).squeeze().numpy() for output in outputs.last_hidden_state]
            sentence_embeddings.extend(embeddings)
        return np.array(sentence_embeddings)

    def __append_fullstop(self, text):
        if text and text[-1] not in punctuation:
            return text + '.'
        return text

    def __get_summary(self, top_n_sentences, sentences):
        sentence_organizer = {k: v for v, k in enumerate(sentences)}
        mapped_top_n_sentences = [(cleaned, sentence_organizer[cleaned]) for cleaned in top_n_sentences]
        mapped_top_n_sentences = sorted(mapped_top_n_sentences, key=lambda x: x[1])
        ordered_scored_sentences = [element[0] for element in mapped_top_n_sentences]
        summary = " ".join([self.__append_fullstop(sentence) for sentence in ordered_scored_sentences])
        return summary

    def summarize_by_percent(self, text, percent=20):
        """
        Summarize a given text based on a specified percentage of its length.

        This method leverages the embeddings generated using DistilBERT to rank the sentences in the text by importance. It then selects the top-ranked sentences based on the specified percentage of the text's total sentences.

        Parameters:
        -----------
        text : str
            The text to be summarized.
        percent : int, optional (default = 20)
            The percentage of the original text's sentences to be retained in the summary. It determines the number of most important sentences to be included.

        Returns:
        --------
        str
            The summarized text.

        Notes:
        ------
        - The method prioritizes retaining the semantic meaning of the original text.
        - Ensure that the text is preprocessed for optimal summarization results.
        - The returned summary will have sentences ordered as they appear in the original text.
        """
        cleaned, original = self.__preprocess_sentences(text)
        sentence_embeddings = self.__create_distilbert_embeddings(cleaned)
        average_embedding = np.mean(sentence_embeddings, axis=0).reshape(1, -1)
        cosine_similarities = cosine_similarity(sentence_embeddings, average_embedding).squeeze()
        total_sentences = len(cleaned)
        top_n = int(total_sentences * (percent / 100))
        top_n_sentences = [cleaned[i] for i in cosine_similarities.argsort()[-top_n:][::-1]]
        return self.__get_summary(top_n_sentences, original)

    def summarize_by_word_count(self, text, word_count=100):
        """
        Summarize a given text based on a specified word count limit.

        This method leverages the embeddings generated using DistilBERT to rank the sentences in the text by importance. It then selects the top-ranked sentences until the desired word count limit is reached or exceeded.

        Parameters:
        -----------
        text : str
            The text to be summarized.
        word_count : int (default = 100)
            The maximum number of words desired in the summary. The method will select the most important sentences until this word limit is reached or exceeded.

        Returns:
        --------
        str
            The summarized text.

        Notes:
        ------
        - The method prioritizes retaining the semantic meaning of the original text. As a result, the returned summary might slightly exceed the specified word count limit.
        - Ensure that the text is preprocessed for optimal summarization results.
        - The returned summary will have sentences ordered as they appear in the original text.
        """
        cleaned, original = self.__preprocess_sentences(text)
        sentence_embeddings = self.__create_distilbert_embeddings(cleaned)
        average_embedding = np.mean(sentence_embeddings, axis=0).reshape(1, -1)
        cosine_similarities = cosine_similarity(sentence_embeddings, average_embedding).squeeze()
        current_count = 0
        selected_sentences = []
        sorted_sentences = [cleaned[i] for i in cosine_similarities.argsort()[::-1]]
        for sentence in sorted_sentences:
            tokens = self.tokenizer.tokenize(sentence)
            if current_count + len(tokens) <= word_count:
                current_count += len(tokens)
                selected_sentences.append(sentence)
            if current_count >= word_count:
                break
        return self.__get_summary(selected_sentences, original)

    def translate_to_english(self, text):
        """
        Translate the given text from Sinhala (si) to English (en).

        This method leverages a translation service to convert the provided Sinhala text into English. In case of any translation errors, it prints the error message and returns an empty string.

        Parameters:
        -----------
        text : str
            The Sinhala text to be translated to English.

        Returns:
        --------
        str
            The translated English text. If an error occurs during the translation, an empty string is returned.

        Notes:
        ------
        - The quality and accuracy of the translation might vary based on the translation service used.
        - Ensure good internet connectivity for optimal results, as this function might rely on online translation services.
        """
        try:
            return self.translator.translate(text, src='si', dest='en').text
        except Exception as e:
            print(f"Error during translation: {str(e)}")
            return ""

