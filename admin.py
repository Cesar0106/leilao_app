# admin.py

import streamlit as st
from database import SessionLocal, Leilao, Lance

def main():
    st.title("Página do Administrador")

    st.sidebar.write("Bem-vindo, Administrador!")
    session = SessionLocal()

    # Formulário para adicionar leilões
    st.header("Adicionar Leilão")
    with st.form("adicionar_leilao_form"):
        item = st.text_input("Item", max_chars=100)
        descricao = st.text_area("Descrição")
        valor_minimo = st.number_input("Valor Mínimo", min_value=0.0, step=0.01)
        submit = st.form_submit_button("Adicionar")

    if submit:
        if item and valor_minimo >= 0:
            novo_leilao = Leilao(item=item, descricao=descricao, valor_minimo=valor_minimo)
            session.add(novo_leilao)
            session.commit()
            st.success(f"Leilão '{item}' adicionado com sucesso!")
        else:
            st.error("Preencha todos os campos obrigatórios.")

    # Listar leilões existentes (somente ativos)
    st.header("Leilões Disponíveis")
    leiloes = session.query(Leilao).filter(Leilao.ativo == True).all()
    for leilao in leiloes:
        col1, col2, col3 = st.columns([3, 1, 1])  # Adicionar uma terceira coluna
        with col1:
            st.write(f"**{leilao.item}** - Valor Mínimo: R$ {leilao.valor_minimo:.2f}")
        with col2:
            ver_lances = st.button("Ver Lances", key=f'ver_lances_{leilao.id}')
        with col3:
            deletar = st.button("Apagar", key=f'deletar_{leilao.id}')
        
        if ver_lances:
            # Exibir lances em um expander
            with st.expander(f"Lances para '{leilao.item}'"):
                lances = session.query(Lance).filter_by(leilao_id=leilao.id).order_by(Lance.valor.desc()).all()
                if lances:
                    for lance in lances:
                        st.write(f"Usuário: {lance.usuario} - Valor: R$ {lance.valor:.2f}")
                else:
                    st.write("Nenhum lance para este leilão.")
        
        if deletar:
            leilao.ativo = False
            session.commit()
            st.success(f"Leilão '{leilao.item}' foi removido da visualização.")
            st.rerun() 

    session.close()

if __name__ == "__main__":
    main()
