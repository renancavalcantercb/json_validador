import streamlit as st
import json

REQUIRED_FIELDS = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
]

# Estilo visual centralizado, opcional
st.markdown(
    """
    <style>
    .block-container {max-width: 700px !important;margin:auto;}
    textarea, .stTextArea textarea {min-height:160px !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align:center; color:#1ABC9C;'>🧩 JSON Firebase/MongoDB Validador</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center'>Cole abaixo seu <b>JSON do Firebase/Google Cloud</b>.<br>Aceita tanto <code>JSON bonito</code> quanto <code>string JSON escapada</code> (variável de ambiente/MongoDB).</p>",
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

input_text = st.text_area(
    "💾 Cole aqui o JSON:", height=180, placeholder="Cole o conteúdo aqui..."
)


def try_parse_json(text):
    try:
        loaded = json.loads(text)
        if isinstance(loaded, dict):
            return loaded, False
        if isinstance(loaded, str):
            try:
                loaded2 = json.loads(loaded)
                if isinstance(loaded2, dict):
                    return loaded2, True
            except Exception:
                pass
        return None, None
    except Exception:
        return None, None


submit_btn = st.button("✅ Validar e preparar", use_container_width=True)

if submit_btn:
    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("🔎 Validando..."):
        parsed, was_escaped = try_parse_json(input_text)

    if parsed is None:
        st.error(
            "❌ O JSON está inválido! Nem como objeto direto, nem como string escapada."
        )
        st.stop()
    missing = [f"`{f}`" for f in REQUIRED_FIELDS if f not in parsed]
    if missing:
        st.warning(f"⚠️ Campos obrigatórios ausentes: {', '.join(missing)}")
        st.stop()

    st.success("🟩 JSON válido!")

    if was_escaped:
        st.info("O JSON já estava no formato escapado 😀")

    st.markdown("<br><hr>", unsafe_allow_html=True)

    json_string = json.dumps(parsed, indent=2, ensure_ascii=False)
    if not was_escaped:
        escapado = json.dumps(json_string, ensure_ascii=False)
        st.markdown("#### Para VARIÁVEL DE AMBIENTE / MongoDB:")
        st.code(escapado, language="json")
        st.caption("⬆️ Use direto no MongoDB ou .env!")
        st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Para leitura humana (formatado):")
    st.code(json_string, language="json")

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        "🚀 Pronto! Agora é só copiar e colar nos seus secrets/MongoDB ou abrir um PR seguro."
    )

st.markdown("---")
st.caption(
    "🔒 Seu JSON permanece local. Não armazenamos nem transmitimos nenhum dado inserido."
)
