"""app.py - frontend + backend in one (Streamlit).  Run: streamlit run app.py"""
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Market Basket Analysis", layout="wide")


@st.cache_data
def q(sql):
    con = sqlite3.connect("basket.db")
    df = pd.read_sql(sql, con)
    con.close()
    return df


st.title("Market Basket Analysis with FP-Growth")
st.caption("UCI Online Retail dataset | rules stored in SQLite")

rules = q("SELECT * FROM rules")
st.sidebar.header("Filters")
min_conf = st.sidebar.slider("Min confidence", 0.3, 1.0, 0.4, 0.05)
min_lift = st.sidebar.slider("Min lift", 1.0, 10.0, 1.5, 0.5)
f = rules[(rules.confidence >= min_conf) & (rules.lift >= min_lift)]

t1, t2, t3, t4 = st.tabs(["Top rules", "Recommender", "FP-Growth vs Apriori",
                          "Evaluation"])

with t1:
    st.metric("Rules matching filters", len(f))
    st.dataframe(f.sort_values("lift", ascending=False).round(3), width="stretch")
    fig = px.scatter(f, x="support", y="confidence", color="lift", size="lift",
                     hover_data=["antecedents", "consequents"],
                     title="Support vs Confidence (colour = lift)")
    st.plotly_chart(fig, width="stretch")

with t2:
    items = sorted({i for s in rules.antecedents for i in s.split(", ")})
    pick = st.selectbox("Customer has this item in the basket:", items)
    only = st.checkbox("Only rules where this is the only item (simplest case)", value=True)
    safe = pick.replace("'", "''")          # escape quotes in product names
    cond = f"antecedents = '{safe}'" if only else f"antecedents LIKE '%{safe}%'"
    res = q(f"SELECT antecedents AS if_basket_has, consequents AS recommend, confidence, lift "
            f"FROM rules WHERE {cond} ORDER BY lift DESC LIMIT 10")
    st.write("Customers who buy this also tend to buy:")
    st.dataframe(res.round(3), width="stretch")
    if not only:
        st.caption("Rules where the item is one of several on the 'if' side only apply "
                   "if the customer has those other items too.")

with t3:
    c = q("SELECT * FROM runtime_comparison")
    st.dataframe(c.round(3))
    fig = px.line(c.melt(id_vars="min_support", value_vars=["fpgrowth_sec", "apriori_sec"]),
                  x="min_support", y="value", color="variable", markers=True,
                  title="Runtime vs minimum support (lower support = harder problem)")
    st.plotly_chart(fig, width="stretch")

with t4:
    e = q("SELECT * FROM evaluation").iloc[0]
    a, b, c_ = st.columns(3)
    a.metric("Hit rate @5", f"{e.hit_rate_at_5:.1%}")
    b.metric("Coverage", f"{e.coverage:.1%}")
    c_.metric("Precision when covered", f"{e.precision_when_covered:.1%}")
    st.write(f"Tested on {int(e.n_test_baskets)} unseen baskets: one item hidden per basket, "
             "rules try to predict it.")
