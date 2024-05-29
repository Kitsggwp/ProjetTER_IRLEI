
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
      uniqueRound: [],
      uniqueMetric: [],
      uniqueQueries:[],
      selectedMetric: 'not choosed',
      selectedRound: 'not choosed',
      selectedQuery: 'not choosed',
      x: null,
      y: null,
      xAxis: null,
      yAxis: null,
      svg: null,
      width: 800,
      height: 400,
      //option settings
      isQueryDropdownOpen: false,
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
    selectQuery(query) {
      this.selectedQuery = query;
      this.createChart(this.evals);
    },

    toggleQueryDropdown() {
      this.isQueryDropdownOpen = !this.isQueryDropdownOpen;
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
          const uniqueRound = [...new Set(response.data.map(ev => ev.Round))];
          this.uniqueRound = uniqueRound;
          const uniqueMetric = [...new Set(response.data.map(ev => ev.Metric))];
          this.uniqueMetric = uniqueMetric;
          const uniqueQuery = [...new Set(response.data.map(ev => ev.Query))];
          this.uniqueQuery = uniqueQuery;
          console.log("Unique Systems:", uniqueSystems);
          console.log("Unique Query:", uniqueQuery);
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
        const newData = this.evals.filter(d => d.Metric === newMetric && d.Query === this.selectedQuery);
        this.updateChart(newData, x, y, xAxis, yAxis, svg, width, height);
      });

      this.$watch('selectedRound', (newQuery) => {
        console.log("Query changed to:", newQuery);
        const newData = this.evals.filter(d => d.Metric === this.selectedMetric && d.Query === newQuery);
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
    selectQuery(Query) {
      this.selectedQuery = Query;
      const newData = this.evals.filter(d => d.Metric === this.selectedMetric && d.Query === Query);
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
      <div class="subtitle">Évaluation des requêtes</div>
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
        <button @click="toggleQueryDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i></i>
          <span>Requêtes</span>
          <span class="selected green">: {{ selectedQuery}}</span>
        </button>
        <Transition>
        <div v-if="isQueryDropdownOpen" class="absolute gridContainer" style="grid-template-columns: repeat(7, minmax(40px, 1fr));">         
          <a v-for="ev in uniqueQuery" :key="ev" :value="ev" @click="selectQuery(ev)"
            class=" green hover:bg-gray-600 ">{{ ev }}</a>
        </div>
        </Transition>
      </div>
      <div class="relative inline-block">
        <button @click="toggleMeasureDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i></i>
          
            <span>Mesures</span>
            <img style="margin-left: 5px; margin-right: 5px;" id="sbLogo" src="../assets/measure.svg" alt="mesure"></img>  
          <span class="selected green">: {{ selectedMetric }}</span>  
        </button>
        <Transition>
        <div v-if="isMeasureDropdownOpen" class="absolute gridContainer" style="margin-left: 150px;">         
          <a v-for="ev in uniqueMetric" :key="ev" :value="ev" @click="selectMetric(ev)"
            class=" green hover:bg-gray-600 ">{{ ev }}</a>
        </div>
        </Transition>
      </div>
    </div>
    <div class="mb-5">
      <select v-model="displayOption" class="bg-gray-800 text-white p-2 rounded">
        <option>Best/Worst Overall</option>
      </select>
      <input v-model="displayMeanMedian" class="ml-4" type="checkbox" />Display Mean/Median?
      <input v-model="displaySignificativeDifference" class="ml-4" type="checkbox" />Display Significative
      difference only?
    </div>
    <!-- Placeholder for graph -->
    <div id="graph">
      <div id="chart"></div>
        
    </div>
  </div>
</template>
