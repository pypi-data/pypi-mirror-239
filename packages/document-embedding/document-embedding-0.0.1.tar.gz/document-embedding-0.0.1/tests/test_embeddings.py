from sentence_transformers import SentenceTransformer

from document_embedding.average import AverageDocumentEmbedding
from document_embedding.pert import PertDocumentEmbedding

text = """
Nach den Wahlen ist vor den Wahlen. Dieses Bonmot gilt nach den Nationalratswahlen für alle Parteien, besonders aber für die Sozialdemokraten. Die SP Schweiz muss die Nachfolge von Bundesrat Alain Berset regeln. Um maximal auf sich aufmerksam zu machen, hat die Partei am Montagabend in Genf die Roadshow ihrer Kandidatin und ihrer fünf Kandidaten eröffnet.

Vor einem wichtigen Wahltag steht auch die SP Genf. Sie muss am Sonntag den Ständeratssitz von Carlo Sommaruga verteidigen. So eröffnete Sommaruga die Bundesrat-Roadshow in Genf gleich selbst, redete seine Partei sowie sich selbst stark und umriss deren wichtigste Anliegen: Sicherung der Kaufkraft, Sicherung akzeptabler Krankenkassenprämien und Schaffung einer 13. AHV-Rente. Doch welche Pläne haben die Bundesratskandidaten, sollten sie am 13. Dezember in die Landesregierung gewählt werden? Und wie mächtig sind sie der französischen Sprache?
"""


def test_average_embeddings():
    transformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    model = AverageDocumentEmbedding(transformer, "german")

    embedding = model.encode([text])[0]

    print(embedding)


def test_bottom_average():
    transformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    model = AverageDocumentEmbedding(transformer, "german", range_start=0.5)

    embedding = model.encode([text])[0]

    print(embedding)


def test_top_average():
    transformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    model = AverageDocumentEmbedding(transformer, "german", range_stop=0.5)

    embedding = model.encode([text])[0]

    print(embedding)


def test_pert_embeddings():
    transformer = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    model = PertDocumentEmbedding(transformer, "german")

    embedding = model.encode([text])[0]

    print(embedding)
