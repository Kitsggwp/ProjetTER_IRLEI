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
      height: 400,
      isEpochDropdownOpen: false,
      isMeasureDropdownOpen: false,
      displayMeanMedian: false,
      displaySignificativeDifference: false,
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
        .sort((a, b) => d3.ascending(a.Round, b.Round));

      // Calculer les valeurs min et max de la colonne Value
      const [minValue, maxValue] = d3.extent(filteredData, d => d.Value);
      // Ajuster l'échelle de couleur
      const colorScale = d3.scaleQuantile()
        .domain([minValue, maxValue])
        .range(d3.schemeSpectral[9]);

      const groupedData = Array.from(
        d3.group(filteredData, d => d.Round),
        ([key, value]) => ({
          Round: key,
          Mean: d3.mean(value, d => d.Value)
        })
      );

      const svgElement = this.GroupedBarChart(filteredData, {
        x: d => d.Round,
        y: d => d.Value - groupedData.find(group => group.Round === d.Round).Mean,
        //y: d => d.Value - d3.mean(filteredData, d => d.Value),
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
          .sort((a, b) => d3.ascending(a.Round, b.Round));

          const groupedData = Array.from(
        d3.group(newData, d => d.Round),
        ([key, value]) => ({
          Round: key,
          Mean: d3.mean(value, d => d.Value)
        })
      );

        const [minValue, maxValue] = d3.extent(newData, d => d.Value); // Utiliser newData pour calculer min et max

        const newSvgElement = this.GroupedBarChart(newData, {
          x: d => d.Round,
          y: d => d.Value - groupedData.find(group => group.Round === d.Round).Mean,
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
          colorScale: d3.scaleQuantile()
            .domain([minValue, maxValue])
            .range(d3.schemeSpectral[9])
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
          .sort((a, b) => d3.ascending(a.Round, b.Round));

        const newSvgElement = this.GroupedBarChart(newData, {
          x: d => d.Round,
          y: d => d.Value - d3.mean(newData, d => d.Value),
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
      if (yDomain === undefined) yDomain = [d3.min(Y), d3.max(Y)];
      if (zDomain === undefined) zDomain = Z;
      xDomain = new d3.InternSet(xDomain);
      zDomain = new d3.InternSet(zDomain);

      const I = d3.range(X.length).filter(i => xDomain.has(X[i]) && zDomain.has(Z[i]));
      colorScale = d3.scaleQuantile()
        .domain(yDomain)
        .range(d3.schemeSpectral[9])

      const xScale = d3.scaleBand()
        .domain(X)
        .range(xRange)
        .padding(xPadding);
      const yScale = yType()
        .domain(yDomain)
        .range(yRange);

      const xzScale = d3.scaleBand()
        .domain(zDomain)
        .range([0, xScale.bandwidth()])
        .padding(zPadding);
      const color = colorScale;

      const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

      svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(yScale).ticks(height / 60).tickFormat(yFormat))
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
          .attr("x", -marginLeft)
          .attr("y", 10)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(yLabel));

      const bar = svg.append("g")
        .selectAll("rect")
        .data(I)
        .join("rect")
        .attr("x", i => xScale(X[i]) + xzScale(Z[i]))
        .attr("y", i => yScale(Math.max(0, Y[i])))
        .attr("width", xzScale.bandwidth())
        .attr("height", i => Math.abs(yScale(0) - yScale(Y[i])))
        .attr("fill", i => Z[i] === test_system ? '#ff0000' : color(Y[i]))
        .on("mouseover", function (event, d) {
          const roundedValue = Y[d].toFixed(3);
          d3.select(".detailsBox")
            .html(`<p>Round: ${X[d]}</p><p>Value: ${roundedValue}</p><p>System ID: ${Z[d]}</p>`)
            .style("display", "block");
        });

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

      let tickAdjust = g => g.selectAll(".tick line").attr("y1", marginTop + marginBottom - height);
      let x;

      // Continuous
      if (color.interpolate) {
        const n = Math.min(color.domain().length, color.range().length);

        x = color.copy().rangeRound(d3.quantize(d3.interpolate(marginLeft, width - marginRight), n));

        svg.append("image")
          .attr("x", marginLeft)
          .attr("y", marginTop)
          .attr("width", width - marginLeft - marginRight)
          .attr("height", height - marginTop - marginBottom)
          .attr("preserveAspectRatio", "none")
          .attr("xlink:href", ramp(color.copy().domain(d3.quantize(d3.interpolate(0, 1), n))).toDataURL());

        // scaleSequentialQuantile doesn’t implement ticks or tickFormat.
        if (!x.ticks) {
          if (tickValues === undefined) tickValues = d3.range(n);
          if (typeof tickFormat !== "function") tickFormat = d3.format(tickFormat === undefined ? ",f" : tickFormat);
        }
      }

      // Discrete
      else if (color.invertExtent) {
        const thresholds = color.thresholds ? color.thresholds() // scaleQuantize
          : color.quantiles ? color.quantiles() // scaleQuantile
            : color.domain(); // scaleThreshold

        const thresholdFormat = tickFormat === undefined ? d => d
          : typeof tickFormat === "string" ? d3.format(tickFormat)
            : tickFormat;

        x = d3.scaleLinear()
          .domain([-1, color.range().length - 1])
          .rangeRound([marginLeft, width - marginRight]);

        svg.append("g")
          .selectAll("rect")
          .data(color.range())
          .join("rect")
          .attr("x", (d, i) => x(i - 1))
          .attr("y", marginTop)
          .attr("width", (d, i) => x(i) - x(i - 1))
          .attr("height", height - marginTop - marginBottom)
          .attr("fill", d => d);

        if (tickValues === undefined) tickValues = d3.range(thresholds.length);
        tickFormat = thresholdFormat;
      }

      svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x)
          .ticks(ticks, typeof tickFormat === "string" ? tickFormat : undefined)
          .tickFormat(typeof tickFormat === "function" ? tickFormat : undefined)
          .tickSize(tickSize)
          .tickValues(tickValues))
        .call(tickAdjust)
        .call(g => g.select(".domain").remove())
        .call(g => g.append("text")
          .attr("x", marginLeft)
          .attr("y", marginTop + marginBottom - height - 6)
          .attr("fill", "currentColor")
          .attr("text-anchor", "start")
          .text(title));

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
    this.createChart(this.evals);
  }
};
</script>


<template>
  <div class="bg-gray-700 p-5 rounded-lg framed">
    <div class="flex justify-between items-center mb-5">
      <div class="subtitle">Rounds Analysis</div>

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
          <span>M</span>
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
    </div>
    <div class="mb-5 white">
      Highlight :
      <select class="bg-gray-800 text-white p-2 rounded" name="highlightEpoque" id="highlightEpoque">
        <option>X</option>
        <option>Best/Worst Overall</option>
      </select>

      <input v-model="displayMeanMedian" class="ml-4" type="checkbox" /> <span>Display Mean</span>
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

#legendBox {
  border: 1px solid white;
  width: 500px;
  height: 80px;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
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
