import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="D3 Area Chart", layout="centered")
st.title("🚗 North America Car Sales (Dummy Data)")
st.caption("Interactive area chart with D3.js and tooltips")

# Dummy monthly car sales data
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
    background: #fff;
    padding: 6px 10px;
    border: 1px solid #ccc;
    font-size: 12px;
    pointer-events: none;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }}
</style>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
// Parse data
const data = {data_json}.map(d => {{
  return {{
    date: new Date(d.month + "-01"),
    sales: d.sales
  }};
}});

// Dimensions
const margin = {{top: 20, right: 30, bottom: 40, left: 60}},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

// SVG setup
const svg = d3.select("#chart")
  .html("")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Scales
const x = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.sales)]).nice()
  .range([height, 0]);

// Axes
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b")));

svg.append("g")
  .call(d3.axisLeft(y));

// Axis labels
svg.append("text")
  .attr("x", width / 2)
  .attr("y", height + margin.bottom - 5)
  .style("text-anchor", "middle")
  .text("Month");

svg.append("text")
  .attr("transform", "rotate(-90)")
  .attr("x", -height / 2)
  .attr("y", -margin.left + 15)
  .style("text-anchor", "middle")
  .text("Car Sales");

// Area
const area = d3.area()
  .x(d => x(d.date))
  .y0(height)
  .y1(d => y(d.sales))
  .curve(d3.curveMonotoneX);

svg.append("path")
  .datum(data)
  .attr("fill", "steelblue")
  .attr("d", area);

// Tooltip
const tooltip = d3.select("#chart").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

svg.selectAll("circle")
  .data(data)
  .enter()
  .append("circle")
  .attr("cx", d => x(d.date))
  .attr("cy", d => y(d.sales))
  .attr("r", 4)
  .attr("fill", "orange")
  .on("mouseover", (event, d) => {{
    tooltip.transition().duration(200).style("opacity", .9);
    tooltip.html(`<b>${{d3.timeFormat("%B")(d.date)}}</b><br/>Sales: ${{d.sales.toLocaleString()}}`)
      .style("position", "fixed")
      .style("left", (event.clientX + 10) + "px")
      .style("top", (event.clientY - 40) + "px");
  }})
  .on("mouseout", () => tooltip.transition().duration(300).style("opacity", 0));
</script>
"""

# Render it
components.html(html_code, height=400)
