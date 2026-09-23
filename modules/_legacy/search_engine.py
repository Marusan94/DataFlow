"""Search Engine local para EduAnalytics HUB.
Basado en build-your-own-x: Vector Space (Boyter) + TF-IDF (Loria) + RAG light.
Sin dependencias pesadas. Trabaja sobre el CSV de 100 registros del repo.
Copiar a: Eduanalytics/modules/search_engine.py
"""
import math


class VectorCompare:
    def concordance(self, document: str) -> dict:
        if not isinstance(document, str):
            raise ValueError('document must be str')
        con = {}
        for word in document.lower().split():
            con[word] = con.get(word, 0) + 1
        return con

    def magnitude(self, concordance: dict) -> float:
        if not isinstance(concordance, dict):
            raise ValueError('concordance must be dict')
        return math.sqrt(sum(c ** 2 for c in concordance.values()))

    def relation(self, c1: dict, c2: dict) -> float:
        if not isinstance(c1, dict) or not isinstance(c2, dict):
            raise ValueError('args must be dict')
        top = sum(cnt * c2[w] for w, cnt in c1.items() if w in c2)
        denom = self.magnitude(c1) * self.magnitude(c2)
        return top / denom if denom != 0 else 0.0


def tf(word: str, doc_words: list) -> float:
    return doc_words.count(word) / len(doc_words) if doc_words else 0.0


def n_containing(word: str, docs: list) -> int:
    return sum(1 for d in docs if word in d)


def idf(word: str, docs: list) -> float:
    return math.log(len(docs) / (1 + n_containing(word, docs)))


def tfidf(word: str, doc_words: list, docs: list) -> float:
    return tf(word, doc_words) * idf(word, docs)


def row_to_text(row) -> str:
    """Convierte una fila del CSV en documento buscable.
    Acepta dict o pandas Series. Usa los 8 campos canónicos + extras.
    """
    def g(k, default=''):
        try:
            v = row[k] if isinstance(row, dict) else row.get(k, default)
        except Exception:
            v = default
        return '' if v is None else str(v)
    parts = [
        g('nombre'), g('tipo_usuario'), g('materia'),
        g('habilidades'), g('grupo_id'), g('tipo_apoyo'),
        f"nota {g('nota')}", f"asistencia {g('asistencia')}",
        g('estado_asistencia'), g('email'),
    ]
    return ' '.join(p for p in parts if p).lower()


def build_index(texts: list) -> list:
    v = VectorCompare()
    return [v.concordance(t) for t in texts]


def search(query: str, docs: list, texts: list = None, top_k: int = 5) -> list:
    """Busca query sobre docs (lista de dicts/rows).
    Si texts es None, se genera con row_to_text.
    Retorna [(score, doc, snippet)] ordenado por score desc.
    """
    v = VectorCompare()
    if texts is None:
        texts = [row_to_text(d) for d in docs]
    index = build_index(texts)
    q_con = v.concordance(query.lower())
    scored = []
    for con, doc, txt in zip(index, docs, texts):
        rel = v.relation(q_con, con)
        if rel > 0:
            # boost TF-IDF simple: palabras raras pesan más
            q_words = query.lower().split()
            docs_split = [t.split() for t in texts]
            q_split = query.lower().split()
            bonus = sum(tfidf(w, q_split, docs_split) for w in q_words) * 0.1
            scored.append((rel + bonus, doc, txt[:160]))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_k]


def retrieve(query: str, docs: list, k: int = 3) -> list:
    return [doc for _, doc, _ in search(query, docs, top_k=k)]


def build_prompt(query: str, contexts: list) -> str:
    if isinstance(contexts[0], dict) if contexts else False:
        ctx_txt = [row_to_text(c)[:200] for c in contexts]
    else:
        ctx_txt = [str(c)[:200] for c in contexts]
    ctx = '\n- '.join(ctx_txt)
    return (
        'Eres un analista educativo experto en los datos que el usuario subio.\n'
        f'Contexto:\n- {ctx}\n\nPregunta: {query}\n'
        'Responde solo con el contexto. Si no alcanza, dilo y sugiere que filtro aplicar.'
    )


def render_search_tab(df=None):
    """Tab Streamlit reactivo. Importa streamlit solo aqui para boot liviano."""
    import streamlit as st
    import pandas as pd

    st.title('🔎 Buscador Educativo')
    st.caption('Vector Space + TF-IDF local · Sin API · RAG light')

    if df is None:
        try:
            df = st.session_state.get('df_edu')
        except Exception:
            df = None
    if df is None:
        try:
            df = pd.read_csv('datos_educativos.csv')
        except Exception:
            st.warning('Sube el CSV en Analytics o deja datos_educativos.csv junto a app.py')
            return

    docs = df.to_dict(orient='records')

    # query param compartible para persistencia
    try:
        q0 = st.query_params.get('q', '')
    except Exception:
        q0 = ''

    @st.fragment
    def search_box():
        q = st.text_input('Buscar estudiante, materia, habilidad, grupo...',
                          value=q0, placeholder='ej: python baja asistencia grupo 9',
                          key='search_q')
        top_k = st.slider('Resultados', 3, 10, 5, key='search_k')
        if not q.strip():
            st.info('Escribe para buscar. Prueba: "matematicas nota baja" o "python grupo 9"')
            return
        try:
            st.query_params['q'] = q
        except Exception:
            pass
        with st.status('Buscando en 100 registros...', expanded=False):
            results = search(q, docs, top_k=top_k)
        if not results:
            st.warning('Sin coincidencias. Prueba con materia o habilidad.')
            return
        for score, doc, snippet in results:
            nombre = doc.get('nombre', '?') if isinstance(doc, dict) else '?'
            st.markdown(f"**{nombre}** · `{score:.3f}` · {snippet}")
        with st.expander('Prompt RAG para Analista IA'):
            st.code(build_prompt(q, [d for _, d, _ in results[:3]]), language='markdown')

    search_box()
