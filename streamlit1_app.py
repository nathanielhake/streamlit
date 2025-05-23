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

const margin = {{top: 20, right: 30, bottom: 40, left: 60}},
      width = 600 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

const svg = d3.select("#chart")
  .html("")
  .append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", `translate(${{margin.left}},${{margin.top}})`);

const x = d3.scaleTime()
  .domain(d3.extent(data, d => d.date))
  .range([0, width]);

const y = d3.scaleLinear()
  .domain([0, d3.max(data, d => d.sales)]).nice()
  .range([height, 0]);

svg.append("g")
  .attr("transform", `translate(0,${{height}})`)
  .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b")));

svg.append("g").call(d3.axisLeft(y));

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

// Tooltip line and circle
const focus = svg.append("g").style("display", "none");

focus.append("line")
  .attr("class", "x-hover-line")
  .attr("stroke", "gray")
  .attr("stroke-width", 1)
  .attr("y1", 0)
  .attr("y2", height);

focus.append("circle")
  .attr("r", 5)
  .attr("fill", "orange")
  .attr("stroke", "black");

const tooltip = d3.select("#chart").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);

svg.append("rect")
  .attr("width", width)
  .attr("height", height)
  .style("fill", "none")
  .style("pointer-events", "all")
  .on("mouseover", () => {{
    focus.style("display", null);
    tooltip.style("opacity", 1);
  }})
  .on("mouseout", () => {{
    focus.style("display", "none");
    tooltip.style("opacity", 0);
  }})
  .on("mousemove", (event) => {{
    const bisectDate = d3.bisector(d => d.date).left;
    const mouse = d3.pointer(event)[0];
    const x0 = x.invert(mouse);
    const i = bisectDate(data, x0, 1);
    const d0 = data[i - 1];
    const d1 = data[i];
    const d = x0 - d0.date > d1.date - x0 ? d1 : d0;

    focus.select("circle")
      .attr("cx", x(d.date))
      .attr("cy", y(d.sales));

    focus.select(".x-hover-line")
      .attr("x1", x(d.date))
      .attr("x2", x(d.date));

    tooltip.html(`<b>${{d3.timeFormat("%B")(d.date)}}</b><br/>Sales: ${{d.sales.toLocaleString()}}`)
      .style("position", "fixed")
      .style("left", (event.clientX + 10) + "px")
      .style("top", (event.clientY - 40) + "px");
  }});
</script>
"""

components.html(html_code, height=420)
