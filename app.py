import streamlit as st
from database import SessionLocal, Leilao, Lance

def main():
    st.title("Leilão de Aliyot na Sinagoga")

    session = SessionLocal()

    leiloes = session.query(Leilao).filter(Leilao.ativo == True).all()
    if not leiloes:
        st.warning("Nenhum leilão disponível no momento.")
        session.close()
        return

    leilao_selecionado = st.selectbox(
        "Selecione um leilão",
        leiloes,
        format_func=lambda l: f"{l.item} (ID: {l.id})"
    )

    st.write(f"**Descrição:** {leilao_selecionado.descricao}")
    st.write(f"**Valor Mínimo:** R$ {leilao_selecionado.valor_minimo:.2f}")

    with st.form("Dar Lance"):
        usuario = st.text_input("Seu Nome", max_chars=50)
        valor = st.number_input("Valor do Lance", min_value=leilao_selecionado.valor_minimo, step=0.01)
        submit = st.form_submit_button("Enviar Lance")

        if submit:
            if usuario and valor:
                lance_mais_alto = session.query(Lance).filter_by(leilao_id=leilao_selecionado.id).order_by(Lance.valor.desc()).first()
                if lance_mais_alto and valor <= lance_mais_alto.valor:
                    st.error(f"O valor do lance deve ser maior que o lance atual de R$ {lance_mais_alto.valor:.2f}.")
                else:
                    novo_lance = Lance(
                        leilao_id=leilao_selecionado.id,
                        usuario=usuario,
                        valor=valor
                    )
                    session.add(novo_lance)
                    session.commit()
                    st.success("Lance registrado com sucesso!")
            else:
                st.error("Preencha todos os campos.")

    st.header("Lance Atual")
    lance_mais_alto = session.query(Lance).filter_by(leilao_id=leilao_selecionado.id).order_by(Lance.valor.desc()).first()

    if lance_mais_alto:
        st.write(f"**Valor do Lance Atual:** R$ {lance_mais_alto.valor:.2f}")
    else:
        st.write("Ainda não há lances para este leilão.")

    session.close()

if __name__ == "__main__":
    main()
