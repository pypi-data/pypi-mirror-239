import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import requests.exceptions

class WebPageAnalyzer:
    def __init__(self, url):
        self.url = url

    def fetch_page_content(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error al acceder a la página:", e)
            self.page_text = None
            return

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text()
        self.page_text = re.sub(r'\s+', ' ', page_text)

    def analyze_sentiments(self):
        if self.page_text is not None:
            try:
                analysis = TextBlob(self.page_text)
                sentiment_score = analysis.sentiment.polarity
            except Exception as e:
                print("Error en el análisis de sentimientos:", e)
                sentiment_score = 0

            if sentiment_score > 0:
                sentiment = 'Positivo'
            elif sentiment_score == 0:
                sentiment = 'Neutral'
            else:
                sentiment = 'Negativo'

            return sentiment, sentiment_score

    def classify_words(self):
        if self.page_text is not None:
            try:
                words = self.page_text.split()
                positive_words = []
                negative_words = []

                for word in words:
                    word_analysis = TextBlob(word)
                    word_polarity = word_analysis.sentiment.polarity
                    if word_polarity > 0:
                        positive_words.append(word)
                    elif word_polarity < 0:
                        negative_words.append(word)
            except Exception as e:
                print("Error en la clasificación de palabras:", e)
                positive_words = []
                negative_words = []

            return positive_words, negative_words

class CustomWebPageAnalyzer(WebPageAnalyzer):
    def __init__(self, url):
        super().__init__(url)

    def custom_analysis(self):
        self.fetch_page_content()  # Recuperar el contenido de la página
        sentiment, sentiment_score = self.analyze_sentiments()  # Analizar sentimientos
        positive_words, negative_words = self.classify_words()  # Clasificar palabras

        print("Análisis personalizado:")
        print("Sentimiento: ", sentiment)
        print("Puntuación de Sentimiento: ", sentiment_score)
        print("Palabras Positivas:")
        print(positive_words)
        print("Palabras Negativas:")
        print(negative_words)


