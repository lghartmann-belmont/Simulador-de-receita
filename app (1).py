# =============================================================================
# Dashboard de Receita Líquida — Belmont Capital
# Identidade Visual: Azul Marinho #232D4B + Cinza Metálico #BCBEC0
# Deploy: Streamlit Cloud
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# 🎨  PALETA BELMONT CAPITAL — altere apenas aqui para redesenhar tudo
# ─────────────────────────────────────────────────────────────────────────────

# Cores da marca
PRIMARY         = "#232D4B"   # Azul marinho profundo (palavra "BELMONT")
PRIMARY_MID     = "#2E3D64"   # Variação intermediária — hover / depth
PRIMARY_LIGHT   = "#3A4F7A"   # Azul acinzentado — elementos secundários
SILVER          = "#BCBEC0"   # Cinza metálico (palavra "CAPITAL")
SILVER_LIGHT    = "#D8DADC"   # Prata clara — bordas e divisores
SILVER_SUBTLE   = "#F0F1F2"   # Quase branco — fundos alternativos de linha

# Status
ACCENT_SUCCESS  = "#2E7D52"   # Verde escuro — harmonioso com marinho
ACCENT_SUCCESS_L= "#3DAA6E"   # Verde médio — badges e deltas
ACCENT_DANGER   = "#B83232"   # Vermelho escuro — abaixo da meta
ACCENT_DANGER_L = "#D94F4F"   # Vermelho médio — deltas negativos
ACCENT_WARN     = "#A0722A"   # Âmbar escuro — alertas neutros

# Fundos
BG_PAGE         = "#1A2138"   # Fundo principal — escuro profundo (levemente mais escuro que PRIMARY)
BG_CARD         = "#232D4B"   # Fundo dos cards — azul marinho exato da marca
BG_CARD_HOVER   = "#2E3D64"   # Hover dos cards
BG_SIDEBAR      = "#161D30"   # Sidebar — mais escuro ainda para criar hierarquia
BG_SURFACE      = "#2A3554"   # Superfície elevada (gráficos, tabelas)
BG_INPUT        = "#1E2740"   # Fundo dos inputs na sidebar

# Textos — NUNCA preto sobre fundo escuro
TEXT_ON_DARK    = "#FFFFFF"   # Branco puro — títulos sobre azul marinho
TEXT_PRIMARY    = "#E8E9EA"   # Quase branco — texto principal sobre cards escuros
TEXT_SECONDARY  = "#BCBEC0"   # Cinza metálico — subtítulos e labels (cor da marca)
TEXT_MUTED      = "#8B909A"   # Cinza médio — textos auxiliares, ticks de eixo
TEXT_ACCENT     = "#D4D8E8"   # Azul-acinzentado claro — valores dos metrics

# Bordas
BORDER_CARD     = "#3A4F7A"   # Borda dos cards — azul acinzentado
BORDER_SUBTLE   = "#2E3D64"   # Divisores internos — quase invisíveis
BORDER_TABLE    = "#2A3554"   # Grade da tabela

# Paleta dos gráficos — gradiente marinho→prata da marca
CHART_PALETTE   = [
    "#3A4F7A",   # azul acinzentado
    "#BCBEC0",   # prata da marca
    "#2E3D64",   # azul médio
    "#8B909A",   # cinza médio
    "#232D4B",   # marinho primário
    "#D8DADC",   # prata clara
    "#1A2138",   # escuro
]

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Belmont Capital · Dashboard de Receita",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — IDENTIDADE VISUAL BELMONT CAPITAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    /* ── Fontes ── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

    /* ── Reset base ── */
    *, *::before, *::after {{ box-sizing: border-box; }}

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > section,
    [data-testid="stAppViewContainer"] .main,
    .main .block-container {{
        background-color: {BG_PAGE} !important;
        font-family: 'DM Sans', sans-serif !important;
        color: {TEXT_PRIMARY} !important;
    }}

    /* Remover barra de ferramentas e header padrão */
    [data-testid="stHeader"]  {{ background: transparent !important; box-shadow: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    #MainMenu {{ visibility: hidden; }}
    footer     {{ visibility: hidden; }}

    /* ── Bloco container — respiro lateral ── */
    .main .block-container {{
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 1600px;
    }}

    /* ─────────────────── SIDEBAR ─────────────────── */
    [data-testid="stSidebar"] {{
        background: {BG_SIDEBAR} !important;
        border-right: 1px solid {BORDER_CARD} !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.5rem;
    }}
    /* Todo texto da sidebar → claro */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] * {{
        color: {TEXT_PRIMARY} !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
    [data-testid="stSidebar"] h2 {{
        color: {TEXT_ON_DARK} !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.02em;
        border-bottom: 1px solid {BORDER_CARD};
        padding-bottom: 0.6rem;
        margin-bottom: 1rem;
    }}
    [data-testid="stSidebar"] h3 {{
        color: {SILVER} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.3rem !important;
    }}
    /* Inputs da sidebar */
    [data-testid="stSidebar"] input[type="number"],
    [data-testid="stSidebar"] input[type="text"] {{
        background: {BG_INPUT} !important;
        border: 1px solid {BORDER_CARD} !important;
        border-radius: 6px !important;
        color: {TEXT_ON_DARK} !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.88rem !important;
        transition: border-color 0.2s;
    }}
    [data-testid="stSidebar"] input[type="number"]:focus,
    [data-testid="stSidebar"] input[type="text"]:focus {{
        border-color: {SILVER} !important;
        box-shadow: 0 0 0 2px rgba(188,190,192,0.15) !important;
    }}
    [data-testid="stSidebar"] label {{
        color: {TEXT_SECONDARY} !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] hr {{
        border: none !important;
        border-top: 1px solid {BORDER_SUBTLE} !important;
        margin: 0.8rem 0 !important;
    }}
    /* Botões de incremento dos number_input */
    [data-testid="stSidebar"] button {{
        background: {BG_INPUT} !important;
        border-color: {BORDER_CARD} !important;
        color: {SILVER} !important;
    }}

    /* ─────────────────── TIPOGRAFIA GERAL ─────────────────── */
    h1, h2, h3, h4 {{
        font-family: 'Playfair Display', serif !important;
        color: {TEXT_ON_DARK} !important;
        font-weight: 700 !important;
    }}
    h4 {{ font-size: 1rem !important; margin-bottom: 0.6rem !important; }}
    p, li, span, div {{ font-family: 'DM Sans', sans-serif !important; }}

    /* ─────────────────── CARDS st.metric ─────────────────── */
    [data-testid="metric-container"] {{
        background: {BG_CARD} !important;
        border: 1px solid {BORDER_CARD} !important;
        border-radius: 10px !important;
        padding: 20px 24px 16px 24px !important;
        position: relative;
        overflow: hidden;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    }}
    /* Faixa de acento lateral esquerda */
    [data-testid="metric-container"]::before {{
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        background: linear-gradient(180deg, {SILVER} 0%, {PRIMARY_LIGHT} 100%);
        border-radius: 10px 0 0 10px;
    }}
    [data-testid="metric-container"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.45);
    }}
    /* Label do metric */
    [data-testid="metric-container"] label {{
        color: {TEXT_SECONDARY} !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
    /* Valor principal */
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {TEXT_ACCENT} !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        font-family: 'DM Sans', sans-serif !important;
        letter-spacing: -0.02em !important;
    }}
    /* Delta */
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        font-family: 'DM Sans', sans-serif !important;
    }}

    /* ─────────────────── CABEÇALHOS DE SEÇÃO ─────────────────── */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0 0 10px 0;
        margin: 32px 0 16px 0;
        border-bottom: 1px solid {BORDER_CARD};
        color: {TEXT_ON_DARK} !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.01em;
    }}
    .section-header .sh-dot {{
        width: 6px; height: 6px;
        border-radius: 50%;
        background: {SILVER};
        display: inline-block;
        flex-shrink: 0;
    }}
    .section-label {{
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: {TEXT_MUTED};
        font-family: 'DM Sans', sans-serif !important;
        margin-bottom: -6px;
    }}

    /* ─────────────────── HERO BANNER ─────────────────── */
    .hero-wrap {{
        background: linear-gradient(135deg, {BG_SIDEBAR} 0%, {PRIMARY} 55%, {PRIMARY_MID} 100%);
        border-radius: 14px;
        border: 1px solid {BORDER_CARD};
        padding: 30px 40px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 40px rgba(0,0,0,0.4);
    }}
    /* Padrão geométrico sutil no hero */
    .hero-wrap::after {{
        content: '';
        position: absolute;
        right: -60px; top: -60px;
        width: 280px; height: 280px;
        border-radius: 50%;
        border: 40px solid rgba(188,190,192,0.05);
        pointer-events: none;
    }}
    .hero-wrap::before {{
        content: '';
        position: absolute;
        right: 60px; bottom: -80px;
        width: 200px; height: 200px;
        border-radius: 50%;
        border: 30px solid rgba(188,190,192,0.04);
        pointer-events: none;
    }}
    .hero-eyebrow {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: {SILVER};
        margin-bottom: 6px;
    }}
    .hero-title {{
        font-family: 'Playfair Display', serif;
        font-size: 1.85rem;
        font-weight: 700;
        color: {TEXT_ON_DARK};
        line-height: 1.2;
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
    }}
    .hero-sub {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.88rem;
        color: {TEXT_SECONDARY};
        margin: 0;
    }}
    .hero-right-label {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: {SILVER};
        margin-bottom: 4px;
    }}
    .hero-right-value {{
        font-family: 'DM Sans', sans-serif;
        font-size: 2.1rem;
        font-weight: 700;
        color: {TEXT_ON_DARK};
        line-height: 1.1;
        letter-spacing: -0.03em;
    }}
    .hero-right-status {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.82rem;
        color: {TEXT_SECONDARY};
        margin-top: 4px;
    }}
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(188,190,192,0.10);
        border: 1px solid rgba(188,190,192,0.22);
        color: {SILVER_LIGHT};
        border-radius: 4px;
        padding: 4px 12px;
        font-size: 0.7rem;
        font-weight: 600;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 14px;
    }}

    /* ─────────────────── DIVISOR ─────────────────── */
    hr {{
        border: none !important;
        border-top: 1px solid {BORDER_SUBTLE} !important;
        margin: 1.5rem 0 !important;
    }}

    /* ─────────────────── TABELA ─────────────────── */
    [data-testid="stDataFrame"] {{
        border-radius: 10px !important;
        overflow: hidden !important;
        border: 1px solid {BORDER_CARD} !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
    }}
    /* Fundo da tabela */
    [data-testid="stDataFrame"] thead tr th {{
        background: {BG_SIDEBAR} !important;
        color: {SILVER} !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border-bottom: 1px solid {BORDER_CARD} !important;
        padding: 12px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
    [data-testid="stDataFrame"] tbody tr td {{
        background: {BG_CARD} !important;
        color: {TEXT_PRIMARY} !important;
        border-bottom: 1px solid {BORDER_SUBTLE} !important;
        font-size: 0.84rem !important;
        font-family: 'DM Sans', sans-serif !important;
        padding: 10px 16px !important;
    }}
    [data-testid="stDataFrame"] tbody tr:nth-child(even) td {{
        background: {BG_SURFACE} !important;
    }}
    [data-testid="stDataFrame"] tbody tr:hover td {{
        background: {BG_CARD_HOVER} !important;
    }}

    /* ─────────────────── SCROLLBAR ─────────────────── */
    ::-webkit-scrollbar               {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track         {{ background: {BG_SIDEBAR}; }}
    ::-webkit-scrollbar-thumb         {{ background: {BORDER_CARD}; border-radius: 3px; }}
    ::-webkit-scrollbar-thumb:hover   {{ background: {SILVER}; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAXAS FIXAS DE COMISSIONAMENTO (fonte: planilha Luiz.xlsx)
# ─────────────────────────────────────────────────────────────────────────────
TAXAS = {
    "captacao":     0.39442,
    "seguros":      0.19266741,
    "credito":      0.0078,
    "planejamento": 0.104,
    "milhas":       0.08667,
    "cambio":       0.0026001,
    "aurea":        0.563355,
}

METAS_DEFAULT = {
    "Captação de Recursos":    225_239.0,
    "Seguros":                  10_000.0,
    "Crédito":                  15_000.0,
    "Planejamento Financeiro":   8_000.0,
    "Gestão de Milhas":          5_000.0,
    "Câmbio":                    3_000.0,
    "Aurea Global":             12_000.0,
}


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES DE CÁLCULO
# ─────────────────────────────────────────────────────────────────────────────
def calc_captacao(estoque, captacoes, roa):
    return (estoque + captacoes) * roa * TAXAS["captacao"]

def calc_seguros(premio):
    return premio * TAXAS["seguros"]

def calc_credito(valor):
    return valor * TAXAS["credito"]

def calc_planejamento(valor):
    return valor * TAXAS["planejamento"]

def calc_milhas(valor):
    return valor * TAXAS["milhas"]

def calc_cambio(valor):
    return valor * TAXAS["cambio"]

def calc_aurea(custodia):
    return custodia * TAXAS["aurea"]

def brl(valor: float) -> str:
    """Formata como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def hex_rgba(hex_color: str, alpha: float = 1.0) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — INPUTS
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / marca na sidebar
    st.markdown(f"""
    <div style='padding: 0 0 18px 0; margin-bottom: 4px;'>
        <div style='font-family:"Playfair Display",serif; font-size:1.25rem;
                    font-weight:700; color:{TEXT_ON_DARK}; letter-spacing:0.04em;'>
            BELMONT
        </div>
        <div style='font-family:"DM Sans",sans-serif; font-size:0.68rem;
                    font-weight:600; color:{SILVER}; letter-spacing:0.22em;
                    text-transform:uppercase; margin-top:-2px;'>
            CAPITAL
        </div>
        <div style='width:32px; height:2px; background:{SILVER};
                    border-radius:2px; margin-top:8px;'></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Parâmetros")
    st.markdown("---")

    st.markdown("### 💰 Captação")
    estoque_custodia = st.number_input("Estoque em Custódia (R$)",
        min_value=0.0, value=539_620_953.0, step=1_000_000.0, format="%.0f",
        help="Saldo total sob custódia do cliente.")
    captacoes_novas = st.number_input("Captações Novas (R$)",
        min_value=0.0, value=14_750_000.0, step=500_000.0, format="%.0f",
        help="Volume de novas captações no período.")
    roa_medio = st.number_input("ROA Médio (%)",
        min_value=0.0, max_value=3.0, value=0.496, step=0.01, format="%.4f",
        help="Return on Assets médio da carteira")
    roa_decimal = roa_medio / 100

    st.markdown("---")
    st.markdown("### 🛡️ Seguros")
    premio_pago = st.number_input("Prêmio Pago (R$)",
        min_value=0.0, value=50_000.0, step=1_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### 🏦 Crédito")
    valor_emprestado = st.number_input("Valor Emprestado (R$)",
        min_value=0.0, value=2_000_000.0, step=100_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### 📋 Planejamento")
    valor_planejamento = st.number_input("Valor Combinado — Planejamento (R$)",
        min_value=0.0, value=80_000.0, step=5_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### ✈️ Milhas")
    valor_milhas = st.number_input("Valor Combinado — Milhas (R$)",
        min_value=0.0, value=60_000.0, step=5_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### 💱 Câmbio")
    valor_cambio = st.number_input("Valor em Real (R$)",
        min_value=0.0, value=1_000_000.0, step=50_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### 🌍 Aurea Global")
    valor_aurea = st.number_input("Valor em Custódia — Aurea (R$)",
        min_value=0.0, value=20_000.0, step=1_000.0, format="%.0f")

    st.markdown("---")
    st.markdown("### 🎯 Metas por Vertical")
    metas = {}
    for vertical, default_val in METAS_DEFAULT.items():
        metas[vertical] = st.number_input(f"Meta · {vertical}",
            min_value=0.0, value=default_val, step=1_000.0, format="%.0f")


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS
# ─────────────────────────────────────────────────────────────────────────────
receitas = {
    "Captação de Recursos":    calc_captacao(estoque_custodia, captacoes_novas, roa_decimal),
    "Seguros":                 calc_seguros(premio_pago),
    "Crédito":                 calc_credito(valor_emprestado),
    "Planejamento Financeiro": calc_planejamento(valor_planejamento),
    "Gestão de Milhas":        calc_milhas(valor_milhas),
    "Câmbio":                  calc_cambio(valor_cambio),
    "Aurea Global":            calc_aurea(valor_aurea),
}
total_receita = sum(receitas.values())
total_meta    = sum(metas.values())
atingimento   = (total_receita / total_meta * 100) if total_meta > 0 else 0.0
gap_total     = total_receita - total_meta


# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
status_txt   = "✦ Acima da Meta" if gap_total >= 0 else "▾ Abaixo da Meta"
status_color = ACCENT_SUCCESS_L if gap_total >= 0 else ACCENT_DANGER_L

st.markdown(f"""
<div class="hero-wrap">
  <div style="display:flex; justify-content:space-between; align-items:flex-end;
              flex-wrap:wrap; gap:24px; position:relative; z-index:1;">
    <div>
      <p class="hero-eyebrow">◆ Assessoria de Investimentos</p>
      <p class="hero-title">Dashboard de Comissionamento</p>
      <p class="hero-sub">Simulação de Receita Líquida · Belmont Capital</p>
      <span class="hero-badge">◆ Identidade Visual Belmont Capital</span>
    </div>
    <div style="text-align:right;">
      <p class="hero-right-label">Receita Total Simulada</p>
      <p class="hero-right-value">{brl(total_receita)}</p>
      <p class="hero-right-status">
        <span style="color:{status_color}; font-weight:700;">{status_txt}</span>
        &nbsp;·&nbsp; {atingimento:.1f}% da meta global
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# RESUMO EXECUTIVO — 4 CARDS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="sh-dot"></span>Resumo Executivo
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("RECEITA LÍQUIDA TOTAL", brl(total_receita),
              delta=f"{atingimento:.1f}% da meta", delta_color="normal")
with c2:
    st.metric("META TOTAL DO PERÍODO", brl(total_meta))
with c3:
    melhor = max(receitas, key=receitas.get)
    st.metric("MAIOR VERTICAL", melhor, delta=brl(receitas[melhor]))
with c4:
    dc = "inverse" if gap_total < 0 else "normal"
    st.metric("GAP PARA META",
              brl(abs(gap_total)),
              delta="Acima da meta ✦" if gap_total >= 0 else "Abaixo da meta ▾",
              delta_color=dc)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CARDS POR VERTICAL — 7 COLUNAS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="sh-dot"></span>Receita por Vertical
</div>
""", unsafe_allow_html=True)

icons = ["💰","🛡️","🏦","📋","✈️","💱","🌍"]
cols  = st.columns(7)
for i, (vertical, receita) in enumerate(receitas.items()):
    mv   = metas[vertical]
    dv   = ((receita / mv) - 1) * 100 if mv > 0 else 0
    with cols[i]:
        st.metric(f"{icons[i]} {vertical}", brl(receita),
                  delta=f"{dv:+.1f}% meta", delta_color="normal")


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="sh-dot"></span>Análise Visual
</div>
""", unsafe_allow_html=True)

# Configurações de layout comuns aos gráficos Plotly
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(color=TEXT_SECONDARY, size=11, family="DM Sans"),
    margin=dict(t=36, b=12, l=12, r=12),
)

col_g1, col_g2 = st.columns([1, 1.4])

# ── Donut ────────────────────────────────────────────────────────────────────
with col_g1:
    st.markdown(f"<p class='section-label'>Composição da Receita</p>", unsafe_allow_html=True)
    df_donut = pd.DataFrame({
        "Vertical": list(receitas.keys()),
        "Receita":  list(receitas.values()),
    })
    fig_donut = px.pie(df_donut, names="Vertical", values="Receita",
                       hole=0.60, color_discrete_sequence=CHART_PALETTE)
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label",
        textfont=dict(color=TEXT_PRIMARY, size=10.5, family="DM Sans"),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",
        marker=dict(line=dict(color=BG_PAGE, width=2.5)),
    )
    fig_donut.update_layout(
        **PLOT_LAYOUT,
        showlegend=False,
        annotations=[dict(
            text=f"<b style='font-size:13px'>{brl(total_receita)}</b>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color=TEXT_ON_DARK, family="DM Sans"),
        )],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Barras — Realizado vs Meta ────────────────────────────────────────────────
with col_g2:
    st.markdown(f"<p class='section-label'>Realizado vs Meta por Vertical</p>", unsafe_allow_html=True)
    verts     = list(receitas.keys())
    v_real    = [receitas[v] for v in verts]
    v_meta    = [metas[v]    for v in verts]
    bar_cores = [ACCENT_SUCCESS_L if r >= m else ACCENT_DANGER_L
                 for r, m in zip(v_real, v_meta)]

    fig_bar = go.Figure()
    # Barra Meta (fundo / referência)
    fig_bar.add_trace(go.Bar(
        name="Meta", x=verts, y=v_meta,
        marker_color=hex_rgba(PRIMARY_LIGHT, 0.45),
        marker_line_color=hex_rgba(SILVER, 0.30),
        marker_line_width=1,
        opacity=1,
    ))
    # Barra Realizado
    fig_bar.add_trace(go.Bar(
        name="Realizado", x=verts, y=v_real,
        marker_color=bar_cores,
        opacity=0.92,
    ))
    fig_bar.update_layout(
        **PLOT_LAYOUT,
        barmode="group",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.01,
            xanchor="right", x=1,
            font=dict(color=TEXT_SECONDARY, size=11),
            bgcolor="rgba(0,0,0,0)", borderwidth=0,
        ),
        xaxis=dict(
            tickangle=-28,
            gridcolor="rgba(0,0,0,0)",
            linecolor=BORDER_SUBTLE,
            tickfont=dict(color=TEXT_MUTED, size=9.5),
        ),
        yaxis=dict(
            gridcolor=hex_rgba(BORDER_SUBTLE, 0.5),
            linecolor="rgba(0,0,0,0)",
            tickprefix="R$ ", tickformat=",.0f",
            tickfont=dict(color=TEXT_MUTED, size=9.5),
        ),
        hovermode="x unified",
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: R$ %{y:,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Gauge — Termômetro ────────────────────────────────────────────────────────
st.markdown(f"<p class='section-label'>Termômetro de Atingimento da Meta Global</p>",
            unsafe_allow_html=True)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=atingimento,
    number={"suffix": "%",
            "font": {"size": 46, "color": TEXT_ON_DARK, "family": "DM Sans"}},
    delta={
        "reference": 100,
        "increasing": {"color": ACCENT_SUCCESS_L},
        "decreasing": {"color": ACCENT_DANGER_L},
        "suffix": "% vs meta",
        "font": {"size": 14},
    },
    gauge={
        "axis": {
            "range": [0, 150],
            "tickwidth": 1,
            "tickcolor": BORDER_CARD,
            "tickfont": {"color": TEXT_MUTED, "size": 10, "family": "DM Sans"},
            "dtick": 25,
        },
        "bar": {
            "color": SILVER,
            "thickness": 0.22,
        },
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "steps": [
            {"range": [0,   50],  "color": hex_rgba(ACCENT_DANGER,   0.12)},
            {"range": [50,  80],  "color": hex_rgba(ACCENT_WARN,     0.10)},
            {"range": [80,  100], "color": hex_rgba(PRIMARY_LIGHT,   0.18)},
            {"range": [100, 150], "color": hex_rgba(ACCENT_SUCCESS,  0.15)},
        ],
        "threshold": {
            "line": {"color": SILVER_LIGHT, "width": 3},
            "thickness": 0.85,
            "value": 100,
        },
    },
    title={
        "text": "% Atingimento da Meta Total",
        "font": {"size": 14, "color": TEXT_SECONDARY, "family": "DM Sans"},
    },
))
fig_gauge.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_SECONDARY, family="DM Sans"),
    height=300,
    margin=dict(t=40, b=10, l=100, r=100),
)
st.plotly_chart(fig_gauge, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABELA DINÂMICA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <span class="sh-dot"></span>Consolidação dos Cálculos
</div>
""", unsafe_allow_html=True)

inputs_desc = {
    "Captação de Recursos":    f"Estoque: {brl(estoque_custodia)} · Cap: {brl(captacoes_novas)} · ROA: {roa_medio:.4f}%",
    "Seguros":                 f"Prêmio Pago: {brl(premio_pago)}",
    "Crédito":                 f"Valor Emprestado: {brl(valor_emprestado)}",
    "Planejamento Financeiro": f"Valor Combinado: {brl(valor_planejamento)}",
    "Gestão de Milhas":        f"Valor Combinado: {brl(valor_milhas)}",
    "Câmbio":                  f"Valor em Real: {brl(valor_cambio)}",
    "Aurea Global":            f"Custódia: {brl(valor_aurea)}",
}
formula_desc = {
    "Captação de Recursos":    "(Estoque + Cap) × ROA × 0,39442",
    "Seguros":                 "Prêmio × 0,19266741",
    "Crédito":                 "Emprestado × 0,0078",
    "Planejamento Financeiro": "Combinado × 0,104",
    "Gestão de Milhas":        "Combinado × 0,08667",
    "Câmbio":                  "Valor Real × 0,0026001",
    "Aurea Global":            "Custódia × 0,563355",
}

rows = []
for vertical in receitas:
    rec   = receitas[vertical]
    meta  = metas[vertical]
    gap_v = rec - meta
    atg_v = (rec / meta * 100) if meta > 0 else 0.0
    rows.append({
        "Vertical":         vertical,
        "Inputs":           inputs_desc[vertical],
        "Fórmula":          formula_desc[vertical],
        "Receita Simulada": brl(rec),
        "Meta":             brl(meta),
        "GAP":              ("+" if gap_v >= 0 else "") + brl(abs(gap_v)),
        "Ating. (%)":       f"{atg_v:.1f}%",
        "Status":           "✦ Acima" if gap_v >= 0 else "▾ Abaixo",
    })

rows.append({
    "Vertical":         "▸ TOTAL",
    "Inputs":           "—",
    "Fórmula":          "—",
    "Receita Simulada": brl(total_receita),
    "Meta":             brl(total_meta),
    "GAP":              ("+" if gap_total >= 0 else "") + brl(abs(gap_total)),
    "Ating. (%)":       f"{atingimento:.1f}%",
    "Status":           "✦ Acima" if gap_total >= 0 else "▾ Abaixo",
})

st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<hr/>
<div style='display:flex; justify-content:space-between; align-items:center;
            padding: 4px 0 20px 0; flex-wrap:wrap; gap:8px;'>
  <div style='font-family:"Playfair Display",serif; font-size:0.95rem;
              color:{TEXT_SECONDARY}; letter-spacing:0.04em;'>
    BELMONT <span style='color:{TEXT_MUTED}; font-family:"DM Sans",sans-serif;
                         font-size:0.7rem; font-weight:600; letter-spacing:0.18em;'>
    CAPITAL</span>
  </div>
  <div style='font-family:"DM Sans",sans-serif; font-size:0.72rem;
              color:{TEXT_MUTED}; letter-spacing:0.04em;'>
    Dashboard de Comissionamento · Taxas: Luiz.xlsx ·
    Desenvolvido com Streamlit + Plotly
  </div>
</div>
""", unsafe_allow_html=True)
