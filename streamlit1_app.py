import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="D3 Area Chart with Tooltip", layout="centered")
st.title("🚘 Dynamic D3 Area Chart – Car Sales in North America")
st.caption("Includes vertical cursor line and interactive tooltip")

# Dummy data
sales_data = [
    {"month": "2024-01", "sales": 12000},
    {"month": "2024-02", "sales": 15000},
    {"month": "2024-03", "sales": 17000},
    {"month": "2024-04", "sales": 13000},
    {"month": "2024-05", "sales": 18000},
    {"month": "2024-06", "sales": 20000},
    {"month": "2024-07", "sales": 22000},
    {"month": "2024-08", "sales": 21000},
    {"month": "2024-09", "sales": 19500},
    {"month": "2024-10", "sales": 23000},
    {"month": "2024-11", "sales": 24000},
    {"month": "2024-12", "sales": 26000},
]

data_json = json.dumps(sales_data)

html_code = f"""
<div id="chart"></div>
<style>
.tooltip {{
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  padding: 6px 10px;
  font-size: 12px;
  pointer-events: none;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}}
</style>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = {data_json}.map(d => {{
  return {{
    date: new Date(d.month + "-01"),
    sales: d.sales
  }};
}});

const margin
