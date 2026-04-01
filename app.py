# =============================================================================
# Dashboard de Simulação de Receita Líquida por Comissionamento
# Autor: Desenvolvedor Python / Analista Quantitativo Sênior
# Baseado na planilha de metas Luiz.xlsx
# Deploy: Streamlit Cloud
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────────────
# 🎨 CONFIGURAÇÃO CENTRAL DE CORES — ALTERE AQUI PARA REDESENHAR O DASHBOARD
# Basta trocar os valores hexadecimais abaixo; todo o visual se adapta sozinho.
# ─────────────────────────────────────────────────────────────────────────────

PRIMARY         = "#1A56DB"   # Cor principal — mude aqui para trocar o tema inteiro
PRIMARY_LIGHT   = "#3B82F6"   # Variação mais clara do primário
PRIMARY_DARK    = "#1E40AF"   # Variação mais escura do primário
PRIMARY_SUBTLE  = "#DBEAFE"   # Tom pastel para fundos e destaques leves

ACCENT_SUCCESS  = "#16A34A"   # Verde  — metas atingidas / positivo
ACCENT_DANGER   = "#DC2626"   # Vermelho — abaixo da meta / negativo
ACCENT_WARN     = "#D97706"   # Âmbar  — alertas intermediários

BG_PAGE         = "#F0F6FF"   # Fundo da página (branco azulado suave)
BG_CARD         = "#FFFFFF"   # Fundo dos cards / painéis
BG_SIDEBAR      = "#1E40AF"   # Fundo da sidebar
BG_SIDEBAR_TEXT = "#EFF6FF"   # Texto dentro da sidebar

TEXT_HEADING    = "#1E3A5F"   # Cor dos títulos e cabeçalhos
TEXT_BODY       = "#374151"   # Texto corrido
TEXT_MUTED      = "#6B7280"   # Texto secundário / labels

BORDER_COLOR    = "#BFDBFE"   # Cor das bordas dos cards
DIVIDER_COLOR   = "#BFDBFE"   # Cor dos separadores hr

CHART_PALETTE   = [           # Paleta sequencial para gráfico de pizza/donut
    "#1A56DB", "#3B82F6", "#60A5FA",
    "#93C5FD", "#BFDBFE", "#1D4ED8", "#2563EB",
]

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Receita | Comissionamento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS DINÂMICO — gerado a partir das variáveis de cor acima
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Base global ── */
    html, body, [data-testid="stAppViewContainer"], [class*="main"] {{
        background-color: {BG_PAGE} !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: {TEXT_BODY};
    }}
    [data-testid="stHeader"]  {{ background: transparent !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {BG_SIDEBAR} 0%, {PRIMARY_DARK} 100%) !important;
        border-right: none;
        box-shadow: 4px 0 24px rgba(30,64,175,0.18);
    }}
    [data-testid="stSidebar"] * {{ color: {BG_SIDEBAR_TEXT} !important; }}
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stTextInput  input {{
        background: rgba(255,255,255,0.12) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: #fff !important;
        border-radius: 8px;
    }}
    [data-testid="stSidebar"] hr  {{ border-color: rgba(255,255,255,0.2) !important; }}
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3  {{ color: #fff !important; font-weight: 700 !important; }}

    /* ── Tipografia ── */
    h1, h2, h3, h4 {{
        color: {TEXT_HEADING} !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* ── Cards st.metric ── */
    [data-testid="metric-container"] {{
        background: {BG_CARD};
        border: 1px solid {BORDER_COLOR};
        border-top: 4px solid {PRIMARY};
        border-radius: 12px;
        padding: 18px 22px 14px 22px;
        box-shadow: 0 2px 12px rgba(26,86,219,0.08);
        transition: box-shadow 0.2s;
    }}
    [data-testid="metric-container"]:hover {{ box-shadow: 0 6px 24px rgba(26,86,219,0.18); }}
    [data-testid="metric-container"] label {{
        color: {TEXT_MUTED} !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {PRIMARY} !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
    }}
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {{
        font-size: 0.78rem !important;
        font-weight: 600 !important;
    }}

    /* ── Cabeçalhos de seção ── */
    .section-header {{
        background: linear-gradient(90deg, {PRIMARY} 0%, {PRIMARY_LIGHT} 100%);
        color: #fff !important;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 28px 0 14px 0;
        letter-spacing: 0.04em;
        box-shadow: 0 4px 14px rgba(26,86,219,0.22);
    }}

    /* ── Hero banner ── */
    .hero-banner {{
        background: linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY} 60%, {PRIMARY_LIGHT} 100%);
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(26,86,219,0.22);
    }}
    .hero-badge {{
        display: inline-block;
        background: rgba(255,255,255,0.18);
        color: #fff;
        border-radius: 20px;
        padding: 3px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-top: 10px;
        border: 1px solid rgba(255,255,255,0.3);
    }}

    /* ── Tabela ── */
    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid {BORDER_COLOR};
        box-shadow: 0 2px 12px rgba(26,86,219,0.06);
    }}

    /* ── Outros ── */
    hr {{ border-color: {DIVIDER_COLOR} !important; }}
    ::-webkit-scrollbar       {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: {BG_PAGE}; }}
    ::-webkit-scrollbar-thumb {{ background: {PRIMARY_LIGHT}; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAXAS FIXAS DE COMISSIONAMENTO (fonte: planilha Luiz.xlsx)
# ─────────────────────────────────────────────────────────────────────────────
TAXAS = {
    "captacao":     0.39442,     # fator sobre (Estoque + Captações) * ROA
    "seguros":      0.19266741,  # sobre Prêmio Pago
    "credito":      0.0078,      # sobre Valor Emprestado
    "planejamento": 0.104,       # sobre Valor Combinado
    "milhas":       0.08667,     # sobre Valor Combinado
    "cambio":       0.0026001,   # sobre Valor em Real
    "aurea":        0.563355,    # sobre Valor Custódia
}

# ─────────────────────────────────────────────────────────────────────────────
# METAS DEFAULT (valores de referência extraídos da planilha)
# ─────────────────────────────────────────────────────────────────────────────
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
# FUNÇÕES DE CÁLCULO — regras de negócio encapsuladas
# ─────────────────────────────────────────────────────────────────────────────

def calc_captacao(estoque: float, captacoes: float, roa: float) -> float:
    """Receita = ((Estoque Custódia + Captações Novas) * ROA Médio) * 0.39442"""
    return (estoque + captacoes) * roa * TAXAS["captacao"]

def calc_seguros(premio: float) -> float:
    """Receita = Prêmio Pago * 0.19266741"""
    return premio * TAXAS["seguros"]

def calc_credito(valor: float) -> float:
    """Receita = Valor Emprestado * 0.0078"""
    return valor * TAXAS["credito"]

def calc_planejamento(valor: float) -> float:
    """Receita = Valor Combinado * 0.104"""
    return valor * TAXAS["planejamento"]

def calc_milhas(valor: float) -> float:
    """Receita = Valor Combinado * 0.08667"""
    return valor * TAXAS["milhas"]

def calc_cambio(valor: float) -> float:
    """Receita = Valor em Real * 0.0026001"""
    return valor * TAXAS["cambio"]

def calc_aurea(custodia: float) -> float:
    """Receita = Valor Custódia * 0.563355"""
    return custodia * TAXAS["aurea"]

def formatar_brl(valor: float) -> str:
    """Formata valor como moeda brasileira (R$ 1.234,56)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def hex_to_rgba(hex_color: str, alpha: float = 1.0) -> str:
    """Converte cor hex para rgba() para uso em gráficos Plotly."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — INPUTS DO USUÁRIO
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parâmetros de Simulação")
    st.markdown("---")

    st.markdown("### 💰 Captação de Recursos")
    estoque_custodia = st.number_input(
        "Estoque em Custódia (R$)",
        min_value=0.0, value=539_620_953.0, step=1_000_000.0,
        format="%.0f", help="Saldo total sob custódia do cliente."
    )
    captacoes_novas = st.number_input(
        "Captações Novas (R$)",
        min_value=0.0, value=14_750_000.0, step=500_000.0,
        format="%.0f", help="Volume de novas captações no período."
    )
    roa_medio = st.number_input(
        "ROA Médio (%)",
        min_value=0.0, max_value=3.0, value=0.496, step=0.01,
        format="%.4f", help="Return on Assets médio (ex: 0.496 = 0,496%)"
    )
    roa_decimal = roa_medio / 100

    st.markdown("---")
    st.markdown("### 🛡️ Seguros")
    premio_pago = st.number_input(
        "Prêmio Pago (R$)",
        min_value=0.0, value=50_000.0, step=1_000.0, format="%.0f",
        help="Valor total de prêmios de seguros pagos pelos clientes."
    )

    st.markdown("---")
    st.markdown("### 🏦 Crédito")
    valor_emprestado = st.number_input(
        "Valor Emprestado (R$)",
        min_value=0.0, value=2_000_000.0, step=100_000.0, format="%.0f",
        help="Saldo total de crédito concedido no período."
    )

    st.markdown("---")
    st.markdown("### 📋 Planejamento Financeiro")
    valor_planejamento = st.number_input(
        "Valor Combinado — Planejamento (R$)",
        min_value=0.0, value=80_000.0, step=5_000.0, format="%.0f",
        help="Honorários combinados de serviços de planejamento financeiro."
    )

    st.markdown("---")
    st.markdown("### ✈️ Gestão de Milhas")
    valor_milhas = st.number_input(
        "Valor Combinado — Milhas (R$)",
        min_value=0.0, value=60_000.0, step=5_000.0, format="%.0f",
        help="Valor total dos programas de milhas geridos."
    )

    st.markdown("---")
    st.markdown("### 💱 Câmbio")
    valor_cambio = st.number_input(
        "Valor em Real (R$)",
        min_value=0.0, value=1_000_000.0, step=50_000.0, format="%.0f",
        help="Volume total de operações cambiais em reais."
    )

    st.markdown("---")
    st.markdown("### 🌍 Aurea Global")
    valor_aurea = st.number_input(
        "Valor em Custódia — Aurea (R$)",
        min_value=0.0, value=20_000.0, step=1_000.0, format="%.0f",
        help="Patrimônio sob custódia na plataforma Aurea Global."
    )

    st.markdown("---")
    st.markdown("### 🎯 Metas por Vertical (R$)")
    metas = {}
    for vertical, default_val in METAS_DEFAULT.items():
        metas[vertical] = st.number_input(
            f"Meta — {vertical}",
            min_value=0.0, value=default_val, step=1_000.0, format="%.0f",
        )


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS PRINCIPAIS
# ─────────────────────────────────────────────────────────────────────────────
rec_captacao     = calc_captacao(estoque_custodia, captacoes_novas, roa_decimal)
rec_seguros      = calc_seguros(premio_pago)
rec_credito      = calc_credito(valor_emprestado)
rec_planejamento = calc_planejamento(valor_planejamento)
rec_milhas       = calc_milhas(valor_milhas)
rec_cambio       = calc_cambio(valor_cambio)
rec_aurea        = calc_aurea(valor_aurea)

receitas = {
    "Captação de Recursos":    rec_captacao,
    "Seguros":                 rec_seguros,
    "Crédito":                 rec_credito,
    "Planejamento Financeiro": rec_planejamento,
    "Gestão de Milhas":        rec_milhas,
    "Câmbio":                  rec_cambio,
    "Aurea Global":            rec_aurea,
}
total_receita = sum(receitas.values())
total_meta    = sum(metas.values())
atingimento   = (total_receita / total_meta * 100) if total_meta > 0 else 0.0
gap_total     = total_receita - total_meta


# ─────────────────────────────────────────────────────────────────────────────
# HERO BANNER — CABEÇALHO PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
status_emoji = "✅" if gap_total >= 0 else "⚠️"
st.markdown(f"""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
            <p style="font-size:2rem; font-weight:800; color:#fff; margin:0; letter-spacing:-0.5px;">
                📊 Dashboard de Comissionamento
            </p>
            <p style="font-size:0.95rem; color:{PRIMARY_SUBTLE}; margin:4px 0 0 0;">
                Simulação de Receita Líquida por Vertical · Assessoria de Investimentos
            </p>
            <span class="hero-badge">🔵 Tema Corporativo · Azul &amp; Branco</span>
        </div>
        <div style="text-align:right;">
            <p style="color:{PRIMARY_SUBTLE}; font-size:0.78rem; margin:0; font-weight:600;
                       text-transform:uppercase; letter-spacing:0.06em;">Receita Total Simulada</p>
            <p style="color:#fff; font-size:2.2rem; font-weight:800; margin:0; letter-spacing:-1px;">
                {formatar_brl(total_receita)}
            </p>
            <p style="color:{PRIMARY_SUBTLE}; font-size:0.88rem; margin:4px 0 0 0;">
                {status_emoji} {atingimento:.1f}% da meta global
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CARDS DE RESUMO EXECUTIVO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📌 Resumo Executivo</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💵 Receita Líquida Total", formatar_brl(total_receita),
              delta=f"{atingimento:.1f}% da meta", delta_color="normal")
with col2:
    st.metric("🎯 Meta Total do Período", formatar_brl(total_meta))
with col3:
    melhor = max(receitas, key=receitas.get)
    st.metric("🏆 Maior Vertical", melhor, delta=formatar_brl(receitas[melhor]))
with col4:
    st.metric("📉 GAP para Meta", formatar_brl(abs(gap_total)),
              delta="Acima da meta ✅" if gap_total >= 0 else "Abaixo da meta ⚠️",
              delta_color="inverse" if gap_total < 0 else "normal")

st.markdown("<br>", unsafe_allow_html=True)

# ── Cards individuais por vertical ───────────────────────────────────────────
st.markdown('<div class="section-header">📂 Receita por Vertical</div>', unsafe_allow_html=True)

cols  = st.columns(7)
icons = ["💰", "🛡️", "🏦", "📋", "✈️", "💱", "🌍"]
for i, (vertical, receita) in enumerate(receitas.items()):
    meta_v  = metas[vertical]
    delta_v = ((receita / meta_v) - 1) * 100 if meta_v > 0 else 0
    with cols[i]:
        st.metric(f"{icons[i]} {vertical}", formatar_brl(receita),
                  delta=f"{delta_v:+.1f}% meta", delta_color="normal")


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Análise Visual</div>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns([1, 1.4])

# ── Donut — Composição da Receita ────────────────────────────────────────────
with col_g1:
    st.markdown(f"<h4 style='color:{TEXT_HEADING};'>🍩 Composição da Receita</h4>",
                unsafe_allow_html=True)
    df_donut = pd.DataFrame({"Vertical": list(receitas.keys()),
                              "Receita":  list(receitas.values())})
    fig_donut = px.pie(df_donut, names="Vertical", values="Receita",
                       hole=0.56, color_discrete_sequence=CHART_PALETTE)
    fig_donut.update_traces(
        textposition="outside", textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
        marker=dict(line=dict(color=BG_CARD, width=2)),
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_BODY, size=11, family="Inter"),
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(text=f"<b>Total</b><br>{formatar_brl(total_receita)}",
                          x=0.5, y=0.5, font_size=12, showarrow=False,
                          font_color=PRIMARY)],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Barras — Realizado vs Meta ────────────────────────────────────────────────
with col_g2:
    st.markdown(f"<h4 style='color:{TEXT_HEADING};'>📊 Realizado vs Meta por Vertical</h4>",
                unsafe_allow_html=True)
    verticais = list(receitas.keys())
    vals_real = [receitas[v] for v in verticais]
    vals_meta = [metas[v]    for v in verticais]
    cores = [ACCENT_SUCCESS if r >= m else ACCENT_DANGER
             for r, m in zip(vals_real, vals_meta)]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Meta", x=verticais, y=vals_meta,
        marker_color=hex_to_rgba(PRIMARY_SUBTLE, 1.0),
        marker_line_color=PRIMARY_LIGHT, marker_line_width=1.5, opacity=0.95,
    ))
    fig_bar.add_trace(go.Bar(
        name="Realizado", x=verticais, y=vals_real,
        marker_color=cores, opacity=0.88,
    ))
    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_BODY, size=11, family="Inter"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(color=TEXT_MUTED),
                    bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(tickangle=-30, gridcolor="rgba(0,0,0,0)", linecolor=BORDER_COLOR,
                   tickfont=dict(color=TEXT_MUTED, size=10)),
        yaxis=dict(gridcolor=PRIMARY_SUBTLE, linecolor=BORDER_COLOR,
                   tickprefix="R$ ", tickformat=",.0f",
                   tickfont=dict(color=TEXT_MUTED, size=10)),
        margin=dict(t=40, b=10, l=10, r=10),
        hovermode="x unified",
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: R$ %{y:,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Gauge — Atingimento Geral ─────────────────────────────────────────────────
st.markdown(f"<h4 style='color:{TEXT_HEADING}; margin-top:8px;'>🎯 Termômetro de Atingimento da Meta Global</h4>",
            unsafe_allow_html=True)
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=atingimento,
    number={"suffix": "%", "font": {"size": 44, "color": PRIMARY, "family": "Inter"}},
    delta={"reference": 100,
           "increasing": {"color": ACCENT_SUCCESS},
           "decreasing": {"color": ACCENT_DANGER},
           "suffix": "% vs meta"},
    gauge={
        "axis": {"range": [0, 150], "tickwidth": 1, "tickcolor": TEXT_MUTED,
                 "tickfont": {"color": TEXT_MUTED, "size": 11}},
        "bar": {"color": PRIMARY, "thickness": 0.26},
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "steps": [
            {"range": [0,   50],  "color": hex_to_rgba(ACCENT_DANGER,  0.08)},
            {"range": [50,  80],  "color": hex_to_rgba(ACCENT_WARN,    0.10)},
            {"range": [80,  100], "color": hex_to_rgba(PRIMARY,        0.10)},
            {"range": [100, 150], "color": hex_to_rgba(ACCENT_SUCCESS, 0.12)},
        ],
        "threshold": {"line": {"color": ACCENT_SUCCESS, "width": 4},
                      "thickness": 0.82, "value": 100},
    },
    title={"text": "% Atingimento da Meta Total",
           "font": {"size": 15, "color": TEXT_MUTED, "family": "Inter"}},
))
fig_gauge.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT_BODY, family="Inter"),
    height=290,
    margin=dict(t=30, b=10, l=80, r=80),
)
st.plotly_chart(fig_gauge, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABELA DINÂMICA DE CONFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔎 Tabela Dinâmica — Consolidação dos Cálculos</div>',
            unsafe_allow_html=True)

inputs_desc = {
    "Captação de Recursos":    f"Estoque: {formatar_brl(estoque_custodia)} | Cap: {formatar_brl(captacoes_novas)} | ROA: {roa_medio:.4f}%",
    "Seguros":                 f"Prêmio Pago: {formatar_brl(premio_pago)}",
    "Crédito":                 f"Valor Emprestado: {formatar_brl(valor_emprestado)}",
    "Planejamento Financeiro": f"Valor Combinado: {formatar_brl(valor_planejamento)}",
    "Gestão de Milhas":        f"Valor Combinado: {formatar_brl(valor_milhas)}",
    "Câmbio":                  f"Valor em Real: {formatar_brl(valor_cambio)}",
    "Aurea Global":            f"Custódia: {formatar_brl(valor_aurea)}",
}
formula_desc = {
    "Captação de Recursos":    "(Estoque + Captações) × ROA × 0,39442",
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
        "Receita Simulada": formatar_brl(rec),
        "Meta":             formatar_brl(meta),
        "GAP (R$)":         ("+" if gap_v >= 0 else "") + formatar_brl(abs(gap_v)),
        "Atingimento (%)":  f"{atg_v:.1f}%",
        "Status":           "✅ Acima" if gap_v >= 0 else "⚠️ Abaixo",
    })

rows.append({
    "Vertical":         "TOTAL",
    "Inputs":           "—",
    "Fórmula":          "—",
    "Receita Simulada": formatar_brl(total_receita),
    "Meta":             formatar_brl(total_meta),
    "GAP (R$)":         ("+" if gap_total >= 0 else "") + formatar_brl(abs(gap_total)),
    "Atingimento (%)":  f"{atingimento:.1f}%",
    "Status":           "✅ Acima" if total_receita >= total_meta else "⚠️ Abaixo",
})

st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; color:{TEXT_MUTED}; font-size:0.78rem; padding-bottom:16px;'>
    Dashboard de Comissionamento · Assessoria de Investimentos ·
    Taxas fixas conforme <b>Luiz.xlsx</b> · Desenvolvido com Streamlit + Plotly ·
    <span style='color:{PRIMARY}; font-weight:600;'>Tema: Azul &amp; Branco Corporativo</span>
</div>
""", unsafe_allow_html=True)
