<script>
import { ref } from 'vue';
import * as d3 from 'd3';
import axios from 'axios';

export default {
  data() {
    return {
      evals: [],
      uniqueSystems: [],
      uniqueRound: [],
      uniqueMetric: [],
      selectedMetric: 'not choosed',
      selectedRound: null,
      selectedQueries: 'all',
      x: null,
      y: null,
      xAxis: null,
      yAxis: null,
      svg: null,
      width: 800,
      height: 600,
      isEpochDropdownOpen: false,
      isMeasureDropdownOpen: false,
      displayMeanMedian: false,
      displayLabel: false,
      checked:false
    };
  },
  methods: {
    selectMetric(metric) {
      this.selectedMetric = metric;
      this.createChart(this.evals);
    },
    selectRound(round) {
      this.selectedRound = round;
      this.createChart(this.evals);
    },
    toggleEpochDropdown() {
      this.isEpochDropdownOpen = !this.isEpochDropdownOpen;
    },
    toggleMeasureDropdown() {
      this.isMeasureDropdownOpen = !this.isMeasureDropdownOpen;
    },
    toggleDisplayLabel() {
      if (this.displayLabel) {
        d3.selectAll(".label").style("display", "block");
      } else {
        d3.selectAll(".label").style("display", "none");
      }
      
      
    },

    getEval() {
      axios.get('/api/eval/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(response => {
          this.evals = response.data;
          this.uniqueSystems = [...new Set(response.data.map(ev => ev.System_id))];
          this.uniqueRound = [...new Set(response.data.map(ev => ev.Round))];
          this.uniqueMetric = [...new Set(response.data.map(ev => ev.Metric))];
          this.createChart(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    
    createChart(data) {
      
      const margin = { top: 30, right: 0, bottom: 30, left: 40 };
      const width = this.width - margin.left - margin.right;
      const height = this.height - margin.top - margin.bottom;

      const filteredData = data
        .filter(d => d.Metric === this.selectedMetric && (this.selectedRound === null || d.Round === this.selectedRound) && d.Query === this.selectedQueries)
        .sort((a, b) => d3.descending(a.Value, b.Value))
        .sort((a, b) => d3.ascending(a.Round, b.Round));
        

      // Ajuster l'échelle de couleur
      const colorScale = d3.scaleLinear()
        .domain([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        .range(d3.schemeSpectral[10]);

      const svgElement = this.GroupedBarChart(filteredData, {
        x: d => d.Round,
        y: d => d.Value,
        z: d => d.System_id,
        marginTop: margin.top,
        marginRight: margin.right,
        marginBottom: margin.bottom,
        marginLeft: margin.left,
        width: this.width,
        height: this.height,
        yLabel: 'Value',
        div_name: '#chart',
        test_system: 'test_system_id',
        zDomain: this.uniqueSystems,
        colorScale: colorScale
      });

      d3.select("#chart").selectAll("*").remove();
      d3.select("#chart").node().appendChild(svgElement);

      // Add legend
      const legendElement = this.Legend(colorScale, { title: "Value", tickFormat: ".2f" });
      d3.select("#legendBox").selectAll("*").remove();
      d3.select("#legendBox").node().appendChild(legendElement);
      

      this.$watch('selectedMetric', (newMetric) => {
        const newData = this.evals
          .filter(d => d.Metric === newMetric && (this.selectedRound === null || d.Round === this.selectedRound) && d.Query === this.selectedQueries)
          .sort((a, b) => d3.descending(a.Value, b.Value))
          .sort((a, b) => d3.ascending(a.Round, b.Round));
          

          

        const newSvgElement = this.GroupedBarChart(newData, {
          x: d => d.Round,
          y: d => d.Value,
          z: d => d.System_id,
          marginTop: margin.top,
          marginRight: margin.right,
          marginBottom: margin.bottom,
          marginLeft: margin.left,
          width: this.width,
          height: this.height,
          yLabel: 'Value',
          div_name: '#chart',
          test_system: 'test_system_id',
          colorScale: colorScale
        });
        d3.select("#chart").selectAll("*").remove();
        d3.select("#chart").node().appendChild(newSvgElement);

        // Update legend
        const legendElement = this.Legend(colorScale, { title: "Value", tickFormat: ".2f" });
        d3.select("#legendBox").selectAll("*").remove();
        d3.select("#legendBox").node().appendChild(legendElement);
      });

      this.$watch('selectedRound', (newRound) => {
        const newData = this.evals
          .filter(d => d.Metric === this.selectedMetric && (newRound === null || d.Round === newRound) && d.Query === this.selectedQueries)
          .sort((a, b) => d3.descending(a.Value, b.Value))
          .sort((a, b) => d3.ascending(a.Round, b.Round));

        const newSvgElement = this.GroupedBarChart(newData, {
          x: d => d.Round,
          y: d => d.Value,
          z: d => d.System_id,
          marginTop: margin.top,
          marginRight: margin.right,
          marginBottom: margin.bottom,
          marginLeft: margin.left,
          width: this.width,
          height: this.height,
          yLabel: 'Value',
          div_name: '#chart',
          test_system: 'test_system_id',
          colorScale: colorScale
        });
        d3.select("#chart").selectAll("*").remove();
        d3.select("#chart").node().appendChild(newSvgElement);
        
        // Update legend
        const legendElement = this.Legend(colorScale, { title: "Value", tickFormat: ".2f" });
        d3.select("#legendBox").selectAll("*").remove();
        d3.select("#legendBox").node().appendChild(legendElement);
      });
    },
    GroupedBarChart(data, {
      x = (d, i) => i,
      y = d => d,
      z = () => 1,
      title,
      marginTop = 30,
      marginRight = 0,
      marginBottom = 30,
      marginLeft = 40,
      width = 640,
      height = 400,
      xDomain,
      xRange = [marginLeft, width - marginRight],
      xPadding = 0.1,
      yType = d3.scaleLinear,
      yDomain,
      yRange = [height - marginBottom, marginTop],
      zDomain,
      zPadding = 0.05,
      yFormat,
      yLabel,
      div_name,
      test_system,
      colorScale
    } = {}) {
      
      const X = d3.map(data, x);
      const Y = d3.map(data, y);
      const Z = d3.map(data, z);
      
      if (xDomain === undefined) xDomain = X;
      if (yDomain === undefined) yDomain = [d3.min(Y) < 0 ? d3.min(Y) : 0, d3.max(Y) < 0 ? 0 : d3.max(Y)];
      if (zDomain === undefined) zDomain = Z;
      xDomain = new d3.InternSet(xDomain);
      zDomain = new d3.InternSet(zDomain);

      const I = d3.range(X.length).filter(i => xDomain.has(X[i]) && zDomain.has(Z[i]));

      const xScale = d3.scaleBand(xDomain, xRange).paddingInner(xPadding);
      const yScale = yType(yDomain, yRange);

      const xzScale = d3.scaleBand(zDomain, [0, xScale.bandwidth()]).padding(zPadding);
      const color = colorScale;

      const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

      svg.append("g")
        .attr("transform", `translate(${marginLeft},0 )`)
        .call(d3.axisLeft(yScale).ticks(height / 60, yFormat))
        .call(g => g.select(".domain"))
        .call(g => g.append("text")
          .attr("x", -marginLeft)
          .attr("y", "-15px")
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(yLabel))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", "-15px");
        

      const bar = svg.append("g")
        .selectAll("rect")
        .data(I)
        .join("rect")
        .attr("x", i => xScale(X[i]) + xzScale(Z[i]))
        .attr("y", i => yScale(Y[i]))
        .attr("width", xzScale.bandwidth())
        .attr("height", i => yScale(0) - yScale(Y[i]))
        .attr("fill", i => Z[i] === test_system ? '#ff0000' : color(Y[i]))
        .attr("title", i => Y[i])
        .on("mouseover", function (event, d) {
          d3.select(".detailsBox")
            .html(`<p>Round: ${X[d]}</p><p>Value: ${Y[d]}</p><p>System ID: ${Z[d]}</p>`)
            .style("display", "block");
        });
       
       
      svg.selectAll(".text")
        .data(I)
        .enter()
        .append("text")
        .attr("class", "label")

      
        //.attr("x", i => xScale(X[i]) + xzScale(Z[i]))
        //.attr("y", i => yScale(Y[i]))
        //.attr("x", (function(d) { return x(d.Round); }  ))
        //.attr("y", function(d) { return y(d.System_id); })

        .attr("dy", ".75em")
        .text(function (i) { return Z[i]; })
        .attr("fill", "white")
        .attr("transform", i => {
          return 'translate(' + (parseInt(xScale(X[i])) + parseInt(xzScale(Z[i]))+15 )+ ',' + parseInt(yScale(Y[i])+10) + '),rotate(90)';
        })
        .attr('x', 0)
        .attr('y', 0)

    if(this.displayLabel){
          d3.selectAll(".label").style("display", "block");
        } else {
          d3.selectAll(".label").style("display", "none");
        }
      if (title) bar.append("title")
        .text(title);

      svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(xScale).tickSizeOuter(0));
      
        


      return svg.node();
    },
    Legend(color, {
  title,
  tickSize = 6,
  width = 320,
  height = 44 + tickSize,
  marginTop = 18,
  marginRight = 0,
  marginBottom = 16 + tickSize,
  marginLeft = 0,
  ticks = width / 64,
  tickFormat,
  tickValues
} = {}) {
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .style("overflow", "visible")
    .style("display", "block");

  let x;

  // Discrete (Ordinal) Scale
  const categories = color.domain().slice(0, 10).sort((a, b) => a - b);
  
  x = d3.scaleBand()
    .domain(categories)
    .range([marginLeft, width - marginRight]);
  
    

  svg.append("g")
    .selectAll("rect")
    .data(categories)
    .join("rect")
    .attr("x", d => x(d))
    .attr("y", marginTop)
    .attr("width", x.bandwidth())
    .attr("height", height - marginTop - marginBottom)
    .attr("fill", d => color(d));

  svg.append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x).ticks(ticks).tickValues([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]))
    .call(d3.axisBottom(x).tickSize(0).tickFormat(d3.format(".2f")))
    .select(".domain").remove();

  svg.append("text")
    .attr("x", marginLeft)
    .attr("y", marginTop + marginBottom - height - 6)
    .attr("fill", "currentColor")
    .attr("text-anchor", "start")
    .text(title);

  return svg.node();


      function ramp(color, n = 256) {
        const canvas = document.createElement("canvas");
        canvas.width = n;
        canvas.height = 1;
        const context = canvas.getContext("2d");
        for (let i = 0; i < n; ++i) {
          context.fillStyle = color(i / (n - 1));
          context.fillRect(i, 0, 1, 1);
        }
        return canvas;
      }
    
    },
    
    
  },
  
  
  
  mounted() {
    this.getEval();

  }
};

</script>


<template>
  <div class="bg-gray-700 p-5 rounded-lg framed">
    <div class="flex justify-between items-center mb-5">
      <div class="subtitle">Rounds Analysis</div>
      <div>

      </div>
    </div>
    <div class="grid grid-cols-2 gap-4 mb-5">
      <div class="relative inline-block">
        <button @click="toggleEpochDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-calendar-alt mr-2"></i>
          <span>Rounds</span>
          <span class="selected green">: {{ selectedRound != null ? selectedRound : "All" }}</span>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <!--   <select @click="selectRound(selected)" v-model="selected">
          <option disabled value="">Sélectionnez une époque</option>
          <option v-for="ev in uniqueRound" :key="ev" :value="ev">{{ ev }}
          </option>
        </select>
        <span>value : </span> -->
        <Transition>
          <div v-if="isEpochDropdownOpen" class="absolute gridContainer"
            style="grid-template-columns: repeat(3, minmax(30px, 1fr));">

            <a v-for="ev in uniqueRound" :key="ev" :value="ev" @click="selectRound(ev)"
              class=" green block px-4 py-2 hover:bg-gray-600">{{ ev }}</a>
            <a @click="selectRound(null)" class=" green block px-4 py-2 hover:bg-gray-600">All</a>
          </div>
        </Transition>
      </div>
      <div class="relative inline-block">
        <button @click="toggleMeasureDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-tachometer-alt mr-2"></i>
          <span>Metric</span>
          <img style="margin-left: 5px; margin-right: 5px;" id="sbLogo" src="../assets/measure.svg" alt="mesure"></img>
          <span class="selected green">: {{ selectedMetric }}</span>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <Transition>
          <div v-if="isMeasureDropdownOpen" class="absolute gridContainer">
            <a v-for="ev in uniqueMetric" :key="ev" :value="ev" @click="selectMetric(ev)"
              class=" green hover:bg-gray-600 ">{{ ev }}</a>
          </div>
        </Transition>
      </div>
      <div class="options">
        <input id="labelCB" style="margin: 10px" @click="toggleDisplayLabel"  class="ml-4" type="button" value="Hide system label" />
        <span class="info"> <br/>Data are system ordered, from the better performing, to the worst performing</span>
      </div>
    </div>
    <div class="mb-5 white">



      <!--input v-model="displaySignificativeDifference" class="ml-4" type="checkbox" /><span>Display Significative difference only?</span-->

    </div>
    <!-- Placeholder for graph -->
    <div id="graph">

      <div id="chart">

      </div>
      <br />
      <div class="flex">
        <div class="detailsBox"></div>
        <div id="legendBox"></div>
      </div>
    </div>
  </div>
</template>
<style>
#details,
.detailsBox {
  border: 1px solid white;
  width: 300px;
  height: 80px;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}

.label {
font-size: 10px;
padding: 2px;
margin:2px;

}

#legendBox {
  border: 1px solid white;
  width: 500px;
  height: 80px;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}
.info{
  padding: 20px;
  font-size: 12px;

}


option {
  color: black
}

body {
  color: white
}


.v-enter-active,
.v-leave-active {
  transition: opacity 0.1s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
