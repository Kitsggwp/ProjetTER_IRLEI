<script>
import { ref } from 'vue';
import * as d3 from 'd3';
import axios from 'axios';
//import { s } from 'vite/dist/node/types.d-jgA8ss1A';

export default {
  data() {
    return {
      //Graph settings
      evals: [],
      uniqueSystems: [],
      selectedMetric: 'desiredMetric',
      selectedRound: 'desiredRound',
      x: null,
      y: null,
      xAxis: null,
      yAxis: null,
      svg: null,
      width: 800,
      height: 400,
      //option settings
      isEpochDropdownOpen: false,
      isMeasureDropdownOpen: false,
      displayMeanMedian: false,
      displaySignificativeDifference: false



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
      console.log("get eval");
      axios.get('/api/eval/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
      .then(response => {
        this.evals = response.data;
        
        const uniqueSystems = [...new Set(response.data.map(ev => ev.System_id))];
        this.uniqueSystems = uniqueSystems;
        
        console.log("Unique Systems:", uniqueSystems);

        this.createChart(response.data);
      })
      .catch(error => {
        console.error(error);
      });
    },
    createChart(data) {
      console.log("Original Data:", data);

      // Configuration du graphique
      const margin = { top: 20, right: 30, bottom: 40, left: 40 };
      const width = this.width - margin.left - margin.right;
      const height = this.height - margin.top - margin.bottom;

      // Supprimer l'ancien graphique si nécessaire
      d3.select("#chart").selectAll("*").remove();

      // Création du conteneur SVG
      const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      // Définir les échelles
      const x = d3.scaleBand()
        .range([0, width])
        .padding(0.1);

      const y = d3.scaleLinear()
        .range([height, 0]);

      // Ajouter les axes
      const xAxis = svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`);

      const yAxis = svg.append("g")
        .attr("class", "y-axis");

      // Initialiser les données
      const initialData = data.filter(d => d.Metric === this.selectedMetric);
      this.updateChart(initialData, x, y, xAxis, yAxis, svg, width, height);

      // Stocker les références pour les futures mises à jour
      this.x = x;
      this.y = y;
      this.xAxis = xAxis;
      this.yAxis = yAxis;
      this.svg = svg;

      // Mettre à jour le graphique chaque fois que `selectedMetric` ou `selectedRound` changent
      this.$watch('selectedMetric', (newMetric) => {
        console.log("Metric changed to:", newMetric);
        const newData = this.evals.filter(d => d.Metric === newMetric && d.Round === this.selectedRound);
        this.updateChart(newData, x, y, xAxis, yAxis, svg, width, height);
      });

      this.$watch('selectedRound', (newRound) => {
        console.log("Round changed to:", newRound);
        const newData = this.evals.filter(d => d.Metric === this.selectedMetric && d.Round === newRound);
        this.updateChart(newData, x, y, xAxis, yAxis, svg, width, height);
      });
    },
    compareAxes(newData, x) {
      const newXDomain = newData.map(d => d.system);
      const currentXDomain = x.domain();
      return newXDomain.length === currentXDomain.length && newXDomain.every((val, index) => val === currentXDomain[index]);
    },
    updateChart(data, x, y, xAxis, yAxis, svg, width, height) {
      console.log("Updating Data:", data);

      // Transformer les données pour D3.js
      const transformedData = data.map(d => ({
        system: d.System_id,  // Ajustez en fonction de votre structure de données réelle
        value: d.Value        // Ajustez en fonction de votre structure de données réelle
      }));
      console.log("Transformed Data:", transformedData);

      // Vérifiez si les absisses ont changé
      const xChanged = !this.compareAxes(transformedData, x);

      // Mettre à jour les échelles
      if (xChanged) {
        x.domain(transformedData.map(d => d.system));
        xAxis.call(d3.axisBottom(x));
      }
      y.domain([0, d3.max(transformedData, d => d.value)]).nice();

      // Mettre à jour l'axe Y
      yAxis.transition().duration(1000).call(d3.axisLeft(y));

      // Liaison des données
      const bars = svg.selectAll(".bar")
        .data(transformedData);

      // Ajouter de nouvelles barres
      bars.enter()
        .append("rect")
        .attr("class", "bar")
        .merge(bars) // fusionner avec les éléments existants
        .transition()
        .duration(1000)
        .attr("x", d => x(d.system))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", "steelblue");

      // Supprimer les barres qui ne sont plus nécessaires
      bars.exit().remove();
    },
    selectMetric(metric) {
      this.selectedMetric = metric;
      const newData = this.evals.filter(d => d.Metric === metric && d.Round === this.selectedRound);
      this.updateChart(newData, this.x, this.y, this.xAxis, this.yAxis, this.svg, this.width, this.height);
    },
    selectRound(round) {
      this.selectedRound = round;
      const newData = this.evals.filter(d => d.Metric === this.selectedMetric && d.Round === round);
      this.updateChart(newData, this.x, this.y, this.xAxis, this.yAxis, this.svg, this.width, this.height);
    }
  },
  mounted() {
    this.getEval();
  }
};
</script>

<template>
  <div class="bg-gray-700 p-5 rounded-lg framed">
    <div class="flex justify-between items-center mb-5">
      <div class="subtitle">Évaluation des époques</div>
      <div>
        <a>
          <button @click="toggleFilterDropdown" class="cursor-pointer">
            <img id="sbLogo" src="../assets/filter.svg" alt="Filter Icon"></img>
          </button>
        </a>
        <a>
          <button @click="toggleGearDropdown" class="cursor-pointer">
            <img id="sbLogo" src="../assets/gear.svg" alt="Gear Icon"></img>
          </button>
        </a>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-4 mb-5">
      <div class="relative inline-block">
        <button @click="toggleEpochDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-calendar-alt mr-2"></i>
          <span>Époques</span>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <div v-if="isEpochDropdownOpen" class="absolute bg-gray-800 text-white mt-1 rounded">
          <a @click="selectRound('1')" class=" green block px-4 py-2 hover:bg-gray-600" >1</a>
          <a @click="selectRound('2')" class=" green block px-4 py-2 hover:bg-gray-600" >2</a>
          <a @click="selectRound('3')" class=" green block px-4 py-2 hover:bg-gray-600" >3</a>
          <a @click="selectRound('4')" class=" green block px-4 py-2 hover:bg-gray-600" >4</a>
          <a @click="selectRound('5')" class=" green block px-4 py-2 hover:bg-gray-600" >5</a>

        </div>
      </div>
      <div class="relative inline-block">
        <button @click="toggleMeasureDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-tachometer-alt mr-2"></i>
          <a style="color: white;">
            <span>Mesures</span>
            <img style="margin-left: 5px; margin-right: 5px;" id="sbLogo" src="../assets/measure.svg"
              alt="mesure"></img>
          </a>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <div v-if="isMeasureDropdownOpen" class="absolute bg-gray-800 text-white mt-1 rounded">
          <a @click="selectMetric('recip_rank')" class="green block px-4 py-2 hover:bg-gray-600" >recip_rank</a>
          <a @click="selectMetric('P_15')" class="green block px-4 py-2 hover:bg-gray-600" >P_15</a>
          <a @click="selectMetric('map')" class="green block px-4 py-2 hover:bg-gray-600" >Map</a>
          <a @click="selectMetric('iprec_at_recall_0.40')" class="green block px-4 py-2 hover:bg-gray-600">iprec_at_recall_0.40</a>

        </div>
      </div>
    </div>
    <div class="mb-5">
      Highlight :
      <select class="bg-gray-800 text-white p-2 rounded" name="highlightEpoque" id="highlightEpoque">
        <option>X</option>
        <option>Best/Worst Overall</option>
      </select>

      <input v-model="displayMeanMedian" class="ml-4" type="checkbox" />Display Mean/Median?
      <input v-model="displaySignificativeDifference" class="ml-4" type="checkbox" />Display Significative
      difference only?
    </div>
    <!-- Placeholder for graph -->
    <div id="graph">

      <div id="chart">

      </div>
    </div>
  </div>
</template>
