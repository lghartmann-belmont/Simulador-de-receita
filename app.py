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
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard de Receita | Comissionamento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS CUSTOMIZADO — visual moderno, tema escuro azulado
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fundo e tipografia global */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    [data-testid="stSidebar"] {
        background: #1e293b;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

    /* Títulos */
    h1, h2, h3 { color: #f8fafc !important; font-family: 'Segoe UI', sans-serif; }

    /* Cards de métricas */
    [data-testid="metric-container"] {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }
    [data-testid="metric-container"] label { color: #94a3b8 !important; font-size: 0.82rem !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

    /* Separadores de seção */
    .section-header {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1rem;
        margin: 24px 0 12px 0;
        letter-spacing: 0.03em;
    }

    /* Tabela */
    [data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

    /* Divisor */
    hr { border-color: #334155; }

    /* Sidebar slider label */
    .stSlider > label { font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAXAS FIXAS DE COMISSIONAMENTO (fonte: planilha Luiz.xlsx)
# ─────────────────────────────────────────────────────────────────────────────
TAXAS = {
    "captacao":        0.39442,       # fator sobre (Estoque + Captações) * ROA
    "seguros":         0.19266741,    # sobre Prêmio Pago
    "credito":         0.0078,        # sobre Valor Emprestado
    "planejamento":    0.104,         # sobre Valor Combinado
    "milhas":          0.08667,       # sobre Valor Combinado
    "cambio":          0.0026001,     # sobre Valor em Real
    "aurea":           0.563355,      # sobre Valor Custódia
}

# ─────────────────────────────────────────────────────────────────────────────
# METAS DEFAULT (valores de referência extraídos da planilha)
# ─────────────────────────────────────────────────────────────────────────────
METAS_DEFAULT = {
    "Captação de Recursos": 225_239.0,
    "Seguros":               10_000.0,
    "Crédito":               15_000.0,
    "Planejamento Financeiro": 8_000.0,
    "Gestão de Milhas":       5_000.0,
    "Câmbio":                 3_000.0,
    "Aurea Global":          12_000.0,
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
    """Formata valor como moeda brasileira."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — INPUTS DO USUÁRIO
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Parâmetros de Simulação")
    st.markdown("---")

    # ── 1. CAPTAÇÃO DE RECURSOS ──────────────────────────────────────────────
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
        format="%.4f", help="Return on Assets médio da carteira (ex: 0.496 = 0,496%)"
    )
    roa_decimal = roa_medio / 100

    st.markdown("---")
    # ── 2. SEGUROS ───────────────────────────────────────────────────────────
    st.markdown("### 🛡️ Seguros")
    premio_pago = st.number_input(
        "Prêmio Pago (R$)",
        min_value=0.0, value=50_000.0, step=1_000.0, format="%.0f",
        help="Valor total de prêmios de seguros pagos pelos clientes."
    )

    st.markdown("---")
    # ── 3. CRÉDITO ───────────────────────────────────────────────────────────
    st.markdown("### 🏦 Crédito")
    valor_emprestado = st.number_input(
        "Valor Emprestado (R$)",
        min_value=0.0, value=2_000_000.0, step=100_000.0, format="%.0f",
        help="Saldo total de crédito concedido no período."
    )

    st.markdown("---")
    # ── 4. PLANEJAMENTO FINANCEIRO ───────────────────────────────────────────
    st.markdown("### 📋 Planejamento Financeiro")
    valor_planejamento = st.number_input(
        "Valor Combinado — Planejamento (R$)",
        min_value=0.0, value=80_000.0, step=5_000.0, format="%.0f",
        help="Honorários combinados de serviços de planejamento financeiro."
    )

    st.markdown("---")
    # ── 5. GESTÃO DE MILHAS ──────────────────────────────────────────────────
    st.markdown("### ✈️ Gestão de Milhas")
    valor_milhas = st.number_input(
        "Valor Combinado — Milhas (R$)",
        min_value=0.0, value=60_000.0, step=5_000.0, format="%.0f",
        help="Valor total dos programas de milhas geridos."
    )

    st.markdown("---")
    # ── 6. CÂMBIO ────────────────────────────────────────────────────────────
    st.markdown("### 💱 Câmbio")
    valor_cambio = st.number_input(
        "Valor em Real (R$)",
        min_value=0.0, value=1_000_000.0, step=50_000.0, format="%.0f",
        help="Volume total de operações cambiais em reais."
    )

    st.markdown("---")
    # ── 7. AUREA GLOBAL ──────────────────────────────────────────────────────
    st.markdown("### 🌍 Aurea Global")
    valor_aurea = st.number_input(
        "Valor em Custódia — Aurea (R$)",
        min_value=0.0, value=20_000.0, step=1_000.0, format="%.0f",
        help="Patrimônio sob custódia na plataforma Aurea Global."
    )

    st.markdown("---")
    # ── METAS PERSONALIZADAS ─────────────────────────────────────────────────
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
rec_captacao    = calc_captacao(estoque_custodia, captacoes_novas, roa_decimal)
rec_seguros     = calc_seguros(premio_pago)
rec_credito     = calc_credito(valor_emprestado)
rec_planejamento = calc_planejamento(valor_planejamento)
rec_milhas      = calc_milhas(valor_milhas)
rec_cambio      = calc_cambio(valor_cambio)
rec_aurea       = calc_aurea(valor_aurea)

receitas = {
    "Captação de Recursos":   rec_captacao,
    "Seguros":                rec_seguros,
    "Crédito":                rec_credito,
    "Planejamento Financeiro": rec_planejamento,
    "Gestão de Milhas":       rec_milhas,
    "Câmbio":                 rec_cambio,
    "Aurea Global":           rec_aurea,
}
total_receita = sum(receitas.values())
total_meta    = sum(metas.values())
atingimento   = (total_receita / total_meta * 100) if total_meta > 0 else 0.0


# ─────────────────────────────────────────────────────────────────────────────
# CABEÇALHO DO DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 8px 0 4px 0;'>
    <span style='font-size:2.4rem; font-weight:800; color:#38bdf8; letter-spacing:-1px;'>
        📊 Dashboard de Comissionamento
    </span><br>
    <span style='color:#94a3b8; font-size:1rem;'>
        Simulação de Receita Líquida por Vertical · Assessoria de Investimentos
    </span>
</div>
""", unsafe_allow_html=True)
st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# CARDS DE RESUMO — LINHA SUPERIOR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📌 Resumo Executivo</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💵 Receita Líquida Total",
        value=formatar_brl(total_receita),
        delta=f"{atingimento:.1f}% da meta",
        delta_color="normal",
    )
with col2:
    st.metric(
        label="🎯 Meta Total",
        value=formatar_brl(total_meta),
    )
with col3:
    melhor_vertical = max(receitas, key=receitas.get)
    st.metric(
        label="🏆 Maior Vertical",
        value=melhor_vertical,
        delta=formatar_brl(receitas[melhor_vertical]),
    )
with col4:
    gap = total_meta - total_receita
    delta_color = "inverse" if gap > 0 else "normal"
    st.metric(
        label="📉 GAP para Meta",
        value=formatar_brl(abs(gap)),
        delta="Acima da meta ✅" if gap <= 0 else "Abaixo da meta ⚠️",
        delta_color=delta_color,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Cards individuais por vertical ───────────────────────────────────────────
st.markdown('<div class="section-header">📂 Receita por Vertical</div>', unsafe_allow_html=True)

cols = st.columns(7)
icons = ["💰", "🛡️", "🏦", "📋", "✈️", "💱", "🌍"]

for i, (vertical, receita) in enumerate(receitas.items()):
    meta_v = metas[vertical]
    delta_v = ((receita / meta_v) - 1) * 100 if meta_v > 0 else 0
    with cols[i]:
        st.metric(
            label=f"{icons[i]} {vertical}",
            value=formatar_brl(receita),
            delta=f"{delta_v:+.1f}% meta",
            delta_color="normal",
        )


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Análise Visual</div>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns([1, 1.4])

# ── Gráfico 1: Donut — Composição da Receita ─────────────────────────────────
with col_g1:
    st.markdown("#### 🍩 Composição da Receita")
    df_donut = pd.DataFrame({
        "Vertical": list(receitas.keys()),
        "Receita":  list(receitas.values()),
    })

    fig_donut = px.pie(
        df_donut,
        names="Vertical",
        values="Receita",
        hole=0.55,
        color_discrete_sequence=px.colors.sequential.Blues_r + px.colors.sequential.Purp_r,
    )
    fig_donut.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Receita: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
    )
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", size=11),
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        annotations=[dict(
            text=f"<b>Total</b><br>{formatar_brl(total_receita)}",
            x=0.5, y=0.5, font_size=13, showarrow=False,
            font_color="#38bdf8",
        )],
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Gráfico 2: Barras — Realizado vs Meta ────────────────────────────────────
with col_g2:
    st.markdown("#### 📊 Realizado vs Meta por Vertical")
    verticais   = list(receitas.keys())
    vals_real   = [receitas[v] for v in verticais]
    vals_meta   = [metas[v]    for v in verticais]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Meta",
        x=verticais,
        y=vals_meta,
        marker_color="#334155",
        marker_line_color="#64748b",
        marker_line_width=1,
        opacity=0.85,
    ))
    fig_bar.add_trace(go.Bar(
        name="Realizado",
        x=verticais,
        y=vals_real,
        marker_color=[
            "#22d3ee" if r >= m else "#f87171"
            for r, m in zip(vals_real, vals_meta)
        ],
        opacity=0.9,
    ))

    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", size=11),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(color="#cbd5e1"),
        ),
        xaxis=dict(tickangle=-30, gridcolor="#1e293b", linecolor="#334155"),
        yaxis=dict(
            gridcolor="#334155", linecolor="#334155",
            tickprefix="R$ ", tickformat=",.0f",
        ),
        margin=dict(t=40, b=10, l=10, r=10),
        hovermode="x unified",
    )
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: R$ %{y:,.2f}<extra></extra>"
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ── Gráfico 3: Gauge — Atingimento Geral ─────────────────────────────────────
st.markdown("#### 🎯 Termômetro de Atingimento da Meta Global")
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=atingimento,
    number={"suffix": "%", "font": {"size": 40, "color": "#38bdf8"}},
    delta={
        "reference": 100,
        "increasing": {"color": "#22d3ee"},
        "decreasing": {"color": "#f87171"},
        "suffix": "% vs 100%",
    },
    gauge={
        "axis": {"range": [0, 150], "tickwidth": 1, "tickcolor": "#64748b"},
        "bar": {"color": "#0ea5e9", "thickness": 0.25},
        "bgcolor": "rgba(0,0,0,0)",
        "borderwidth": 0,
        "steps": [
            {"range": [0,   50],  "color": "#1e293b"},
            {"range": [50,  80],  "color": "#1e3a5f"},
            {"range": [80,  100], "color": "#1e4a6b"},
            {"range": [100, 150], "color": "#14532d"},
        ],
        "threshold": {
            "line": {"color": "#22c55e", "width": 4},
            "thickness": 0.8,
            "value": 100,
        },
    },
    title={"text": "% Atingimento da Meta Total", "font": {"size": 16, "color": "#94a3b8"}},
))
fig_gauge.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    height=280,
    margin=dict(t=30, b=10, l=60, r=60),
)
st.plotly_chart(fig_gauge, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABELA DINÂMICA DE CONFERÊNCIA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔎 Tabela Dinâmica — Consolidação dos Cálculos</div>', unsafe_allow_html=True)

inputs_desc = {
    "Captação de Recursos":   f"Estoque: {formatar_brl(estoque_custodia)} | Cap: {formatar_brl(captacoes_novas)} | ROA: {roa_medio:.4f}%",
    "Seguros":                f"Prêmio Pago: {formatar_brl(premio_pago)}",
    "Crédito":                f"Valor Emprestado: {formatar_brl(valor_emprestado)}",
    "Planejamento Financeiro": f"Valor Combinado: {formatar_brl(valor_planejamento)}",
    "Gestão de Milhas":       f"Valor Combinado: {formatar_brl(valor_milhas)}",
    "Câmbio":                 f"Valor em Real: {formatar_brl(valor_cambio)}",
    "Aurea Global":           f"Custódia: {formatar_brl(valor_aurea)}",
}

formula_desc = {
    "Captação de Recursos":   "(Estoque + Captações) × ROA × 0,39442",
    "Seguros":                "Prêmio × 0,19266741",
    "Crédito":                "Emprestado × 0,0078",
    "Planejamento Financeiro": "Combinado × 0,104",
    "Gestão de Milhas":       "Combinado × 0,08667",
    "Câmbio":                 "Valor Real × 0,0026001",
    "Aurea Global":           "Custódia × 0,563355",
}

rows = []
for vertical in receitas:
    rec   = receitas[vertical]
    meta  = metas[vertical]
    gap_v = rec - meta
    atg_v = (rec / meta * 100) if meta > 0 else 0.0
    rows.append({
        "Vertical":           vertical,
        "Inputs":             inputs_desc[vertical],
        "Fórmula":            formula_desc[vertical],
        "Receita Simulada":   f"R$ {rec:>14,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Meta":               f"R$ {meta:>14,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "GAP (R$)":           f"R$ {gap_v:>+14,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Atingimento (%)":    f"{atg_v:.1f}%",
        "Status":             "✅ Acima" if gap_v >= 0 else "⚠️ Abaixo",
    })

# Linha de totais
rows.append({
    "Vertical":          "**TOTAL**",
    "Inputs":            "—",
    "Fórmula":           "—",
    "Receita Simulada":  f"R$ {total_receita:>14,.2f}".replace(",","X").replace(".",",").replace("X","."),
    "Meta":              f"R$ {total_meta:>14,.2f}".replace(",","X").replace(".",",").replace("X","."),
    "GAP (R$)":          f"R$ {(total_receita-total_meta):>+14,.2f}".replace(",","X").replace(".",",").replace("X","."),
    "Atingimento (%)":   f"{atingimento:.1f}%",
    "Status":            "✅ Acima" if total_receita >= total_meta else "⚠️ Abaixo",
})

df_tabela = pd.DataFrame(rows)
st.dataframe(df_tabela, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#475569; font-size:0.78rem; padding-bottom:12px;'>
    Dashboard de Comissionamento · Assessoria de Investimentos · 
    Taxas fixas conforme planilha Luiz.xlsx · Desenvolvido com Streamlit + Plotly
</div>
""", unsafe_allow_html=True)
