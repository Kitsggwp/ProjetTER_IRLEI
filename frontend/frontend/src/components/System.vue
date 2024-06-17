<script setup>
import MultiSelect from 'primevue/multiselect';
</script>

<template>


  <div class="bg-gray-700 p-5 rounded-lg framed">
    <div class="flex justify-between items-center mb-5">
      <div class="subtitle">Systems table</div>

    </div>
    <div class="flex mb-5">

      <div>
        System :
        <select v-model="selectedSystem" class="mr-2 p-2" @change="getRoundbySystemSelected">
          <option value="">Select System</option>
          <option v-for="system in uniqueSystems" :key="system" :value="system.System_id">{{ system.System_id + " / " +
          system.Team }}</option>
        </select>
      </div>
      <div v-if="selectedSystem" :class="{ 'text-red-500': selectedRound.length === 0 }">
        Round :
        <select v-model="selectedRound" class="mr-2 p-2" @change="getQueryandMetricbySystemandRoundselected">
          <option value="">Select Round</option>
          <option v-for=" round  in  uniqueRounds " :key="round" :value="round">{{ round }}</option>
        </select>
      </div>
      <div v-if="selectedRound.length > 0" :class="{ 'text-red-500': selectedQuery.length === 0 }">
        Queries :
        <MultiSelect v-model="selectedQuery" :maxSelectedLabels="3" display="chip" selectedItemsLabel
          :options="uniqueQueries" placeholder="Select Queries" filter class="w-full md:w-20rem"
          @change="fetchMetricsData" />
        <div :class="{ 'text-red-500': selectedQuery.length === 0 }">
          {{ selectedQuery.length }} queries selected.
        </div>

      </div>
    </div>
    <div>
    </div>
    <div class="message" v-if="selectedQuery.length === 0">
      Fill in the parameters ! (System, round and queries)</div>
    <table v-else class="table-auto w-full bg-white">
      <thead>
        <tr>
          <th>Metric</th>
          <th>Average value for the {{ selectedSystem
            }}</th>
          <th>Average on all systems</th>
          <th>Maximum value on all systems</th>
          <th>Minimum value on all systems</th>
          <th>Median on all systems</th>
          <th>Standard deviation on all systems</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for=" metric  in  metricsData " :key="metric.name">
          <td
            title="
If the average value of the selected system is higher than that of all systems then there is a green arrow otherwise if it is lower a red arrow if it equals nothing">
            {{ metric.name }}
            <span
              :class="{ 'text-green-500': metric.selected_value > metric.average_value, 'text-red-500': metric.selected_value < metric.average_value }">
              {{ getMetricIcon(metric) }}
            </span>
          </td>
          <td>{{ metric.selected_value }}</td>
          <td>{{ metric.average_value }}</td>
          <td>{{ metric.max_value }}</td>
          <td>{{ metric.min_value }}</td>
          <td>{{ metric.median_value }}</td>
          <td>{{ metric.std_deviation }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';


export default {
  components: {
    MultiSelect
  },
  data() {
    return {
      selectedSystem: '',
      selectedRound: '',
      selectedQuery: '',
      uniqueSystems: [],
      uniqueRounds: [],
      uniqueQueries: [],
      UniqueMetrics: [],
      metricsData: [],
      filteredEvals: '',
    };
  },
  computed: {
    ...mapState(['token']),
    ...mapState(['evals']),

  },
  created() {
    this.getSystem();
    //this.getAverage("UGA_English_BM25", "q07225045", [], "map")
  },
  methods: {
    // Si un des paramètre est vide, cela les prends tous en comptes.
    // Par exemple getAverage("UGA_English_BM25", "q07225045", [], "map") prend en compte tous les rounds.
    async getAverage(system, query, round, metric) {
      try {
        const response = await axios.get('/api/eval/average-values/', {
          headers: {
            'Authorization': `Token ${this.token}`
          },
          params: {
            system: system,
            query: query,
            round: round,
            metric: metric
          },
          paramsSerializer: params => {
            return Object.entries(params).map(([key, value]) => {
              if (Array.isArray(value)) {
                return value.map(v => `${key}=${v}`).join('&');
              }
              return `${key}=${value}`;
            }).join('&');
          }
        });
        console.log("system :" + system, "query : " + query, "round : " + round, "metric : " + metric,
          "moyenne : " + response.data.average_value,
          "mediane : " + response.data.median_value,
          "écart_type : " + response.data.std_deviation
        );
        return response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getSystem() {
      const evals = this.evals;
      console.log(evals)
      // Extraire les systèmes uniques des évaluations filtrées
      const uniqueSystems = Array.from(new Map(evals.map(item => [item.System_id, { System_id: item.System_id, Team: item.Team }])).values());
      this.uniqueSystems = uniqueSystems;
    },
    async getRoundbySystemSelected() {
      // Filtrer les évaluations en fonction du système sélectionné
      const filteredEvals = this.evals.filter(evaluation => evaluation.System_id === this.selectedSystem);
      this.filteredEvals = filteredEvals
      // Extraire les rounds uniques des évaluations filtrées
      const uniqueRounds = [...new Set(filteredEvals.map(ev => ev.Round))];
      this.uniqueRounds = uniqueRounds;

      this.selectedQuery = []
      this.selectedRound = []

    },
    async getQueryandMetricbySystemandRoundselected() {
      /*  try {
         const response = await axios.get('/api/eval/', {
           headers: {
             'Authorization': `Token ${this.token}`
           }
         });
         this.evals = response.data; */
      const filteredEvalsandrounds = this.filteredEvals.filter(evaluation => evaluation.Round === this.selectedRound);

      // Extraire les requêtes uniques des évaluations filtrées
      let uniqueQueries = [...new Set(filteredEvalsandrounds.map(ev => ev.Query))];
      uniqueQueries = uniqueQueries.filter((metric) => metric !== 'all')
      this.uniqueQueries = uniqueQueries;

      // Extraire les metrics uniques des évaluations filtrées
      let uniqueMetrics = [...new Set(filteredEvalsandrounds.map(ev => ev.Metric))];
      uniqueMetrics = uniqueMetrics.filter((metric) => metric !== 'runid')
      uniqueMetrics = uniqueMetrics.filter((metric) => metric !== 'num_q')
      uniqueMetrics = uniqueMetrics.filter((metric) => metric !== 'gm_map')
      this.uniqueMetrics = uniqueMetrics;
      this.selectedQuery = []
      console.log(uniqueQueries);
    },
    async fetchMetricsData() {
      if (this.selectedSystem && this.selectedRound && this.selectedQuery.length !== 0) {
        console.log(this.selectedQuery)
        const metricsData = [];

        for (const metric of this.uniqueMetrics) {
          const dataforall = await this.getAverage("", this.selectedQuery, this.selectedRound, metric);
          const dataforonesystem = await this.getAverage(this.selectedSystem, this.selectedQuery, this.selectedRound, metric);
          metricsData.push({
            name: metric,
            selected_value: dataforonesystem.average_value,
            average_value: dataforall.average_value,
            median_value: dataforall.median_value,
            std_deviation: dataforall.std_deviation,
            max_value: dataforall.max_value,
            min_value: dataforall.min_value,
          });
        }
        this.metricsData = metricsData;
      }
    },
    getMetricIcon(metric) {
      if (metric.selected_value > metric.average_value) {
        return '▲';
      } else if (metric.selected_value < metric.average_value) {
        return '▼';
      } else {
        return '';
      }
    },
  }
};
</script>

<style>
.table-auto {
  width: 100%;
  border-collapse: collapse;
}

.table-auto th,
.table-auto td {
  border: 1px solid #ddd;
  padding: 8px;
}

.text-green-500 {
  color: green;
}

.text-red-500 {
  color: red;
}

.text-white {
  color: white;
}

.p-multiselect-panel .p-multiselect-header {
  display: flex;
  flex-direction: column-reverse;
  align-items: flex-start;
}

.p-multiselect-header .p-checkbox {
  position: relative;
  margin-bottom: 20px;
}

.p-multiselect-header .p-checkbox:nth-of-type(1)::after {
  content: "All";
  position: absolute;
  left: 30px;
  top: 50%;
  transform: translateY(-50%);
  font-weight: bold;
}

.message {
  color: red;
}
</style>
