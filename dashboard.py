import pandas as pd
import plotly.express as px
import streamlit as st
import glob

def load_dashboard():
    st.title("🎓 JoSAA Analysis Dashboard")
    st.markdown("---")

    @st.cache_data
    def get_data():
        all_files = glob.glob("./all data/*allrounds.csv")
        if not all_files:
            st.error("FATAL: No data files found in './all data/' directory.")
            return pd.DataFrame()
        df_list = [pd.read_csv(file, on_bad_lines='skip') for file in all_files]
        df = pd.concat(df_list, ignore_index=True)
        df.dropna(subset=['year', 'College', 'Branch'], inplace=True)
        df['year'] = df['year'].astype(int)
        return df

    df = get_data()

    if not df.empty:
        st.sidebar.header("Please Filter Here:")
        
        # --- Sidebar Filters ---
        selected_years = st.sidebar.multiselect(
            "Select Year:",
            options=sorted(df["year"].unique(), reverse=True),
            default=[2023] # Default to the most recent year for faster loading
        )
        
        # Create a temporary dataframe based on year selection to populate other filters
        df_for_options = df[df['year'].isin(selected_years)]

        selected_colleges = st.sidebar.multiselect(
            "Select College:",
            options=sorted(df_for_options['College'].unique())
        )
        
        if selected_colleges:
            df_for_options = df_for_options[df_for_options['College'].isin(selected_colleges)]

        selected_branches = st.sidebar.multiselect(
            "Select Branch:",
            options=sorted(df_for_options['Branch'].unique())
        )

        selected_quota = st.sidebar.multiselotect("Select Quota:", options=df["Quota"].unique(), default=["AI"])
        selected_caste = st.sidebar.multiselect("Select Caste:", options=df["Caste"].unique(), default=["OPEN"])
        selected_gender = st.sidebar.multiselect("Select Gender:", options=df["Gender"].unique(), default=["Gender-Neutral"])
        
        # --- Filtering Logic (Applied at the end for robustness) ---
        df_selection = df[
            df['year'].isin(selected_years) &
            df['Quota'].isin(selected_quota) &
            df['Caste'].isin(selected_caste) &
            df['Gender'].isin(selected_gender)
        ]
        if selected_colleges:
            df_selection = df_selection[df_selection['College'].isin(selected_colleges)]
        if selected_branches:
            df_selection = df_selection[df_selection['Branch'].isin(selected_branches)]

        # --- Display Results ---
        st.header("Filtered Results")
        if df_selection.empty:
            st.warning("No data available for the selected filters.")
        else:
            # (The rest of the KPI and charting code remains the same)
            st.subheader("Key Performance Indicators")
            avg_opening_rank = int(round(df_selection["Opening Rank"].mean(), 0))
            avg_closing_rank = int(round(df_selection["Closing Rank"].mean(), 0))
            best_opening_rank = int(df_selection["Opening Rank"].min())
            max_closing_rank = int(df_selection["Closing Rank"].max())
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric(label="Avg. Opening Rank", value=f"{avg_opening_rank:,}")
            kpi2.metric(label="Avg. Closing Rank", value=f"{avg_closing_rank:,}")
            kpi3.metric(label="Best Opening Rank", value=f"{best_opening_rank:,}")
            kpi4.metric(label="Max. Closing Rank", value=f"{max_closing_rank:,}")

            st.markdown("---")
            st.subheader("Visualizations")
            rank_by_college = df_selection.groupby("College")[["Opening Rank", "Closing Rank"]].mean().sort_values("Closing Rank").reset_index()
            fig = px.bar(rank_by_college, x="College", y=["Opening Rank", "Closing Rank"], title="<b>Average Opening & Closing Ranks by College</b>", template="plotly_white", barmode='group', labels={"value": "Average Rank", "variable": "Rank Type"})
            fig.update_layout(xaxis_title="College", yaxis_title="Average Rank", xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Detailed Data View")
            st.dataframe(df_selection)