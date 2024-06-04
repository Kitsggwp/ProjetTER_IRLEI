<script setup>
import MultiSelect from 'primevue/multiselect';
</script>

<template>
  <div class="bg-gray-700 p-5 rounded-lg framed">
    <div class="flex justify-between items-center mb-5">
      <div class="subtitle">Tableau des systèmes</div>
    </div>
    <div class="flex mb-5">
      System :
      <select v-model="selectedSystem" class="mr-2 p-2" @change="fetchMetricsData">
        <option value="">Sélectionner un système</option>
        <option v-for="system in uniqueSystems" :key="system" :value="system.System_id">{{ system.System_id + " / " +
        system.Team }}</option>
      </select>
      Rounds :
      <MultiSelect v-model="selectedRound" :maxSelectedLabels="5" display="chip" :options="uniqueRounds"
        placeholder="Select Rounds" class="w-full md:w-20rem" @change="fetchMetricsData" />
      Queries :
      <MultiSelect v-model="selectedQuery" :maxSelectedLabels="5" display="chip" :options="uniqueQueries"
        placeholder="Select Queries" class="w-full md:w-20rem" @change="fetchMetricsData" />
    </div>
    <div>
    </div>
    <table class="table-auto w-full bg-white">
      <thead>
        <tr>
          <th>Métrique</th>
          <th>Valeur moyenne pour le système sélectionné</th>
          <th>Valeur maximum sur tous les systèmes</th>
          <th>Valeur minimum sur tous les systèmes</th>
          <th>Moyenne sur tous les systèmes</th>
          <th>Médiane sur tous les systèmes</th>
          <th>Écart type sur tous les systèmes</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="metric in metricsData" :key="metric.name">
          <td :class="getMetricClass(metric)"
            title="Le nom s'affiche en rouge si il est inférieur à la moyenne, en vert si il est supérieur, en blanc si il est égale.">
            {{ metric.name }}</td>
          <td>{{ metric.selected_value }}</td>
          <td>{{ metric.max_value }}</td>
          <td>{{ metric.min_value }}</td>
          <td>{{ metric.average_value }}</td>
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
      metricsData: []
    };
  },
  computed: {
    ...mapState(['token'])
  },
  created() {
    this.getEval();
    //this.getAverage('', '4', '2', 'map');
  },
  methods: {
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
    async getEval() {
      try {
        const response = await axios.get('/api/eval/', {
          headers: {
            'Authorization': `Token ${this.token}`
          }
        });
        this.evals = response.data;


        const uniqueSystems = Array.from(
          new Map(response.data.map(item => [item.System_id, { System_id: item.System_id, Team: item.Team }])).values()
        );
        this.uniqueSystems = uniqueSystems;
        const uniqueRounds = [...new Set(response.data.map(ev => ev.Round))];
        this.uniqueRounds = uniqueRounds;
        let uniqueQueries = [...new Set(response.data.map(ev => ev.Query))];
        uniqueQueries = uniqueQueries.filter((metric) => metric !== 'all')
        this.uniqueQueries = uniqueQueries;
        let UniqueMetrics = [...new Set(response.data.map(ev => ev.Metric))];
        UniqueMetrics = UniqueMetrics.filter((metric) => metric !== 'runid')
        this.UniqueMetrics = UniqueMetrics;
      } catch (error) {
        console.error(error);
      }
    },
    async fetchMetricsData() {
      if (this.selectedSystem) {
        const metricsData = [];
        let UniqueMetricsFiltered = this.UniqueMetrics;
        if (this.selectedQuery !== "") {
          UniqueMetricsFiltered = UniqueMetricsFiltered.filter((metric) => metric !== 'num_q')
          UniqueMetricsFiltered = UniqueMetricsFiltered.filter((metric) => metric !== 'gm_map')
        }
        for (const metric of UniqueMetricsFiltered) {
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
    getMetricClass(metric) {
      if (metric.selected_value > metric.average_value) {
        return 'text-green-500';
      } else if (metric.selected_value < metric.average_value) {
        return 'text-red-500';
      } else {
        return 'text-white';
      }
    }
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
</style>
