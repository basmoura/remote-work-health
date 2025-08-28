# work_arrangement x regiao
# hours_per_week x work_arrangement x burnout_level
# work_arrangement x work_life_balance
# work_arrangement x mental_health_status
# work_arrangement x gender
# work_arrangement x age
# gender x mental_health_status

import plotly.express as px
import streamlit as st

from app.src.data_prep import load


def main():
    df = get_data()
    csv = convert_for_download(df)

    st.header("Atividade 3 - Análise de Dados")
    st.markdown("*Utilize o botão abaixo para fazer download do dataset*")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="data.csv",
        mime="text/csv",
        icon=":material/download:",
    )

    st.subheader("Gráficos")

    df_region_work_arrangement = (
        df.groupby(["region", "work_arrangement"])
        .agg(count=("work_arrangement", "count"))
        .reset_index()
    )

    options = df_region_work_arrangement["region"].unique()

    st.markdown("**Gráfico interattivo**")
    selection = st.segmented_control(
        "Selecione o continente", options, selection_mode="multi"
    )

    if not selection:
        temp_df = df_region_work_arrangement
    else:
        temp_df = df_region_work_arrangement[
            df_region_work_arrangement["region"].isin(selection)
        ]

    region_work_arrangement = px.histogram(
        temp_df,
        x="work_arrangement",
        y="count",
        color="region",
        title="Total of Work Arrangement per Continent",
        barmode="group",
        text_auto=True,
    )

    region_work_arrangement.update_layout(
        xaxis_title="Work Arrangement", yaxis_title="Count"
    )

    st.plotly_chart(region_work_arrangement)

    hour_week_work_life_score = px.histogram(
        df,
        x="hours_per_week",
        color="work_life_balance_score",
        title="Hours Per Week x Worklife Balance Score",
    )
    hour_week_work_life_score.update_layout(
        xaxis_title="Hours Per Week", yaxis_title="Count"
    )

    st.plotly_chart(hour_week_work_life_score)

    burnout_level_hours_week = px.density_heatmap(
        df,
        x="burnout_level",
        y="hours_per_week",
        z="hours_per_week",
        histfunc="count",
        title="Burnout Level x Hours Per Week",
    )
    burnout_level_hours_week.update_layout(
        xaxis_title="Burnout Level", yaxis_title="Hours Per Week"
    )

    st.plotly_chart(burnout_level_hours_week)

    st.subheader("Conteúdo extra")
    st.video("https://youtu.be/l4n88DmjKOk?si=YxFjJxXvzjcbhs5t")


@st.cache_data
def get_data():
    df = load()
    return df


@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")


if __name__ == "__main__":
    main()
