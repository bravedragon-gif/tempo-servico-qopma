import streamlit as st
import pandas as pd
import datetime
from data_loader import load_officers, save_officers, calculate_officer_retirement, add_ymd, sub_ymd
import io

# Set page config
st.set_page_config(
    page_title="Gestão de Tempo de Serviço - QOPMA",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper to format YMD list/tuple to string
def format_ymd(ymd):
    if not ymd:
        return "0 anos, 0 meses, 0 dias"
    y, m, d = ymd
    y_str = f"{y} ano" if y == 1 else f"{y} anos"
    m_str = f"{m} mês" if m == 1 else f"{m} meses"
    d_str = f"{d} dia" if d == 1 else f"{d} dias"
    
    parts = []
    if y > 0: parts.append(y_str)
    if m > 0: parts.append(m_str)
    if d > 0 or not parts: parts.append(d_str)
    
    if len(parts) == 3:
        return f"{parts[0]}, {parts[1]} e {parts[2]}"
    elif len(parts) == 2:
        return f"{parts[0]} e {parts[1]}"
    else:
        return parts[0]

# Custom CSS for styling
st.markdown("""
<style>
    .kpi-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .kpi-val {
        font-size: 28px;
        font-weight: bold;
        color: #1f77b4;
    }
    .kpi-title {
        font-size: 14px;
        color: #555;
    }
</style>
""", unsafe_style=class_name if 'class_name' in locals() else None)

# Main Title
st.title("🎖️ Gestão de Tempo de Serviço e Reserva Remunerada")
st.subheader("Quadro de Oficiais Policiais Militares de Administração (QOPMA)")
st.markdown("---")

# 1. Sidebar Controls
st.sidebar.header("Filtros & Configurações")

# Reference/Current Date
ref_date_input = st.sidebar.date_input(
    "Data de Projeção / Cálculo",
    value=datetime.date.today(),
    help="Altere esta data para projetar quem estará apto para a reserva no futuro!"
)
ref_date_str = ref_date_input.strftime("%d/%m/%Y")

# Load data and apply calculations based on chosen reference date
officers = load_officers()
for off in officers:
    # Recalculate with chosen calculation date
    calcs = calculate_officer_retirement(
        off['entry_date'],
        off['ffaa_time'],
        off['civil_time'],
        ref_date_str
    )
    off.update(calcs)

# Search
search_query = st.sidebar.text_input("Buscar por Nome", "").strip()

# Posto Filter
posts = ["Todos"] + sorted(list(set(off['rank'] for off in officers)))
rank_filter = st.sidebar.selectbox("Filtrar por Posto", posts)

# Status RR Filter
rr_filter = st.sidebar.selectbox("Apto para Reserva (RR)?", ["Todos", "SIM", "NÃO"])

# Agregado Filter
agregado_filter = st.sidebar.selectbox("Agregado?", ["Todos", "SIM", "NÃO"])

# Apply Filters
filtered_officers = officers

if search_query:
    filtered_officers = [o for o in filtered_officers if search_query.lower() in o['name'].lower()]

if rank_filter != "Todos":
    filtered_officers = [o for o in filtered_officers if o['rank'] == rank_filter]

if rr_filter != "Todos":
    is_apt = rr_filter == "SIM"
    filtered_officers = [o for o in filtered_officers if o['rr_status'] == is_apt]

if agregado_filter != "Todos":
    is_agr = agregado_filter == "SIM"
    filtered_officers = [o for o in filtered_officers if o['agregado'] == is_agr]

# 2. KPI Metrics Row
st.markdown("### 📊 Indicadores Gerais")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

total_count = len(officers)
majores_count = sum(1 for o in officers if o['rank'] == 'MAJ')
capitaes_count = sum(1 for o in officers if o['rank'] == 'CAP')
agregados_count = sum(1 for o in officers if o['agregado'])
apto_count = sum(1 for o in officers if o['rr_status'])
nao_apto_count = total_count - apto_count
pct_apto = (apto_count / total_count * 100) if total_count > 0 else 0

with col1:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total de Oficiais</div><div class='kpi-val'>{total_count}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total de Majores</div><div class='kpi-val' style='color:#0d9488;'>{majores_count}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total de Capitães</div><div class='kpi-val' style='color:#7c3aed;'>{capitaes_count}</div></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total de Agregados</div><div class='kpi-val' style='color:#64748b;'>{agregados_count}</div></div>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Apto para Reserva (RR)</div><div class='kpi-val' style='color:green;'>{apto_count}</div></div>", unsafe_allow_html=True)
with col6:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Não Apto Faltando Tempo</div><div class='kpi-val' style='color:orange;'>{nao_apto_count}</div></div>", unsafe_allow_html=True)
with col7:
    st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Taxa de Elegibilidade</div><div class='kpi-val'>{pct_apto:.1f}%</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Main Data Table
st.markdown(f"### 📋 Lista de Oficiais (Calculado para {ref_date_str})")

# Construct dataframe for display
rows = []
for o in filtered_officers:
    rows.append({
        'N.º': o['id'],
        'Posto': o['rank'],
        'Nome': o['name'],
        'Agregado': "SIM" if o['agregado'] else "NÃO",
        'Entrada PMDF': o['entry_date'],
        'Tempo PMDF': format_ymd(o['pmdf_time']),
        'Tempo FFAA': format_ymd(o['ffaa_time']),
        'Tempo Civil': format_ymd(o['civil_time']),
        'Tempo Total': format_ymd(o['total_time']),
        'Tempo Pedágio': format_ymd(o['toll_time']),
        'Apto RR?': "SIM" if o['rr_status'] else "NÃO",
        'Tempo Faltante': format_ymd(o['missing_time'])
    })

if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export options
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        # Excel export
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='TempoServico')
        st.download_button(
            label="📥 Exportar Tabela para Excel (XLSX)",
            data=buffer.getvalue(),
            file_name=f"Tempo_Servico_QOPMA_{ref_date_input.strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Nenhum policial encontrado com os filtros aplicados.")

st.markdown("---")

# 4. Detail, Edit, Add, Delete Sections (Tabs)
tab_detail, tab_add, tab_edit_del = st.tabs([
    "🔍 Memorial de Cálculo Detalhado",
    "➕ Cadastrar Novo Oficial",
    "⚙️ Editar / Excluir Oficial"
])

# TAB 1: Memorial de Cálculo
with tab_detail:
    st.markdown("### Memorial de Cálculo Individual")
    if filtered_officers:
        selected_officer = st.selectbox(
            "Selecione um oficial para ver o cálculo detalhado:",
            filtered_officers,
            format_func=lambda o: f"{o['rank']} {o['name']} (ID: {o['id']})"
        )
        
        if selected_officer:
            o = selected_officer
            st.markdown(f"#### **{o['rank']} {o['name']}** (Data de Entrada: {o['entry_date']})")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.markdown("**1. Composição do Tempo de Serviço**")
                st.write(f"- **Tempo PMDF (cálculo de calendário):** {format_ymd(o['pmdf_time'])} (de {o['entry_date']} até {ref_date_str})")
                st.write(f"- **Tempo de Forças Armadas (FFAA):** {format_ymd(o['ffaa_time'])}")
                st.write(f"- **Tempo de Serviço Civil:** {format_ymd(o['civil_time'])}")
                st.markdown(f"**Tempo de Serviço Total (soma administrativa):** `{format_ymd(o['total_time'])}`")
                
            with col_d2:
                st.markdown("**2. Cálculo do Pedágio (Transição 17%)**")
                st.write(f"- **Data de Corte da Reforma:** `31/12/2019`")
                st.write(f"- **Data Limite para 30 anos (aniversário):** `{o['target_date']}`")
                st.write(f"- **Dias Faltantes em 31/12/2019:** {o['missing_days_at_cutoff']} dias")
                st.write(f"- **Pedágio Calculado (17%):** {o['toll_days']} dias")
                st.markdown(f"**Tempo de Pedágio Convertido:** `{format_ymd(o['toll_time'])}`")
            
            st.markdown("---")
            st.markdown("**3. Requisito e Status da Reserva**")
            
            req_time_str = format_ymd(o['required_time'])
            st.write(f"- **Tempo Total Requerido para Reserva (30 anos + Pedágio):** `{req_time_str}`")
            st.write(f"- **Tempo de Serviço Atual Acumulado:** `{format_ymd(o['total_time'])}`")
            
            if o['rr_status']:
                st.success(f"✔️ **APTO PARA A RESERVA REMUNERADA:** O oficial completou o requisito total de tempo!")
            else:
                st.warning(f"⏳ **NÃO APTO:** Faltam `{format_ymd(o['missing_time'])}` de tempo total de serviço.")
                
            # Check for known spreadsheet anomalies
            known_anomalies = {
                37: "No arquivo original, a soma de dias de PMDF + Civil deu 47 dias. O correto leva ao carry de 1 mês para a coluna de meses, totalizando 32a 0m 17d em vez de 31a 11m 17d.",
                41: "No arquivo original, o mês da coluna FFAA (1 mês) não foi somado na planilha original (exibindo 31a 5m em vez de 31a 6m).",
                43: "No arquivo original, o mês da coluna Civil (1 mês) não foi somado na planilha original (exibindo 27a 10m em vez de 27a 11m).",
                45: "No arquivo original, a soma de dias deu 33 dias. O correto leva ao carry de 1 mês, resultando em 28a 0m 3d em vez de 27a 11m 3d."
            }
            if o['id'] in known_anomalies:
                st.info(f"💡 **Nota de Consistência:** {known_anomalies[o['id']]}")
    else:
        st.write("Nenhum policial carregado.")

# TAB 2: Cadastrar Novo Oficial
with tab_add:
    st.markdown("### Cadastrar Novo Policial Militar")
    with st.form("add_officer_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            new_id = st.number_input("N.º (Identificador)", min_value=1, value=len(officers)+1)
            new_rank = st.selectbox("Posto", ["MAJ", "CAP"])
            new_name = st.text_input("Nome Completo")
            new_agregado = st.checkbox("Agregado (SIM)")
            new_entry = st.date_input("Data de Entrada na PMDF", value=datetime.date(1999, 10, 1))
        
        with col_f2:
            st.markdown("**Tempo Externo FFAA (Forças Armadas)**")
            col_ff1, col_ff2, col_ff3 = st.columns(3)
            ffaa_y = col_ff1.number_input("Anos FFAA", min_value=0, max_value=50, value=0)
            ffaa_m = col_ff2.number_input("Meses FFAA", min_value=0, max_value=11, value=0)
            ffaa_d = col_ff3.number_input("Dias FFAA", min_value=0, max_value=29, value=0)
            
            st.markdown("**Tempo Externo Serviço Civil**")
            col_cv1, col_cv2, col_cv3 = st.columns(3)
            civil_y = col_cv1.number_input("Anos Civil", min_value=0, max_value=50, value=0)
            civil_m = col_cv2.number_input("Meses Civil", min_value=0, max_value=11, value=0)
            civil_d = col_cv3.number_input("Dias Civil", min_value=0, max_value=29, value=0)
            
        submit_add = st.form_submit_button("Salvar Novo Oficial")
        
        if submit_add:
            if not new_name.strip():
                st.error("Erro: O nome não pode estar vazio!")
            else:
                # Add to list
                new_off = {
                    'id': int(new_id),
                    'rank': new_rank,
                    'name': new_name.strip().upper(),
                    'agregado': new_agregado,
                    'entry_date': new_entry.strftime("%d/%m/%Y"),
                    'current_date': ref_date_str,
                    'ffaa_time': [int(ffaa_y), int(ffaa_m), int(ffaa_d)],
                    'civil_time': [int(civil_y), int(civil_m), int(civil_d)]
                }
                
                # Check for duplicate ID
                if any(o['id'] == new_off['id'] for o in officers):
                    st.error(f"Erro: Já existe um oficial cadastrado com o número {new_id}!")
                else:
                    all_offs = load_officers() # Load current database state
                    all_offs.append(new_off)
                    save_officers(all_offs)
                    st.success(f"Oficial {new_rank} {new_name} salvo com sucesso! A página será atualizada.")
                    st.rerun()

# TAB 3: Editar / Excluir Oficial
with tab_edit_del:
    st.markdown("### Editar ou Excluir Registro")
    if officers:
        off_to_modify = st.selectbox(
            "Selecione o oficial que deseja alterar/excluir:",
            officers,
            format_func=lambda o: f"{o['rank']} {o['name']} (ID: {o['id']})",
            key="off_modify"
        )
        
        if off_to_modify:
            o = off_to_modify
            
            # Format entry date
            entry_parsed = datetime.datetime.strptime(o['entry_date'], "%d/%m/%Y").date()
            
            with st.form("edit_officer_form"):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    edit_rank = st.selectbox("Alterar Posto", ["MAJ", "CAP"], index=0 if o['rank']=="MAJ" else 1)
                    edit_name = st.text_input("Alterar Nome", value=o['name'])
                    edit_agregado = st.checkbox("Agregado (SIM)", value=o['agregado'])
                    edit_entry = st.date_input("Alterar Data de Entrada", value=entry_parsed)
                
                with col_e2:
                    st.markdown("**Alterar Tempo FFAA**")
                    col_eff1, col_eff2, col_eff3 = st.columns(3)
                    eff_y = col_eff1.number_input("Anos FFAA", min_value=0, value=o['ffaa_time'][0], key="ey_ff")
                    eff_m = col_eff2.number_input("Meses FFAA", min_value=0, value=o['ffaa_time'][1], key="em_ff")
                    eff_d = col_eff3.number_input("Dias FFAA", min_value=0, value=o['ffaa_time'][2], key="ed_ff")
                    
                    st.markdown("**Alterar Tempo Civil**")
                    col_ecv1, col_ecv2, col_ecv3 = st.columns(3)
                    ecv_y = col_ecv1.number_input("Anos Civil", min_value=0, value=o['civil_time'][0], key="ey_cv")
                    ecv_m = col_ecv2.number_input("Meses Civil", min_value=0, value=o['civil_time'][1], key="em_cv")
                    ecv_d = col_ecv3.number_input("Dias Civil", min_value=0, value=o['civil_time'][2], key="ed_cv")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit_edit = st.form_submit_button("💾 Salvar Alterações")
                with col_btn2:
                    submit_del = st.form_submit_button("❌ Excluir Policial", type="secondary")
                    
                if submit_edit:
                    if not edit_name.strip():
                        st.error("Erro: O nome não pode estar vazio!")
                    else:
                        all_offs = load_officers()
                        for idx, item in enumerate(all_offs):
                            if item['id'] == o['id']:
                                all_offs[idx] = {
                                    'id': o['id'],
                                    'rank': edit_rank,
                                    'name': edit_name.strip().upper(),
                                    'agregado': edit_agregado,
                                    'entry_date': edit_entry.strftime("%d/%m/%Y"),
                                    'current_date': ref_date_str,
                                    'ffaa_time': [int(eff_y), int(eff_m), int(eff_d)],
                                    'civil_time': [int(ecv_y), int(ecv_m), int(ecv_d)]
                                }
                                break
                        save_officers(all_offs)
                        st.success("Alterações salvas com sucesso! Recarregando...")
                        st.rerun()
                        
                if submit_del:
                    all_offs = load_officers()
                    all_offs = [item for item in all_offs if item['id'] != o['id']]
                    save_officers(all_offs)
                    st.success("Registro excluído com sucesso! Recarregando...")
                    st.rerun()
    else:
        st.write("Nenhum policial cadastrado.")
