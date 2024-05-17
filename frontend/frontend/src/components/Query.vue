<script setup>
import { ref } from 'vue';

const isEpochDropdownOpen = ref(false);
const isMeasureDropdownOpen = ref(false);
const displayMeanMedian = ref(false);
const displayOption = ref('Best/Worst');
const displaySignificativeDifference = ref(false);

const toggleEpochDropdown = () => {
  isEpochDropdownOpen.value = !isEpochDropdownOpen.value;
};

const toggleMeasureDropdown = () => {
  isMeasureDropdownOpen.value = !isMeasureDropdownOpen.value;
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
        <button @click="toggleEpochDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-calendar-alt mr-2"></i>
          <span>Requêtes</span>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <div v-if="isEpochDropdownOpen" class="absolute bg-gray-800 text-white mt-1 rounded">
          <a class="green block px-4 py-2 hover:bg-gray-600" href="#">001</a>
          <a class=" green block px-4 py-2 hover:bg-gray-600" href="#">002</a>
          <a class=" green block px-4 py-2 hover:bg-gray-600" href="#">003</a>
          <a class=" green block px-4 py-2 hover:bg-gray-600" href="#">004</a>
          <a class=" green block px-4 py-2 hover:bg-gray-600" href="#">...</a>
        </div>
      </div>
      <div class="relative inline-block">
        <button @click="toggleMeasureDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
          <i class="fas fa-tachometer-alt mr-2"></i>
          <a style="color: white;">
            <span>Mesures</span>
            <img style="margin-left: 5px; margin-right: 5px;" id="sbLogo" src="../assets/measure.svg" alt="mesure"></img>
        </a>
          <i class="fas fa-chevron-down ml-2"></i>
        </button>
        <div v-if="isMeasureDropdownOpen" class="absolute bg-gray-800 text-white mt-1 rounded">
          <a class="green block px-4 py-2 hover:bg-gray-600" href="#">recip_rank</a>
          <a class="green block px-4 py-2 hover:bg-gray-600" href="#">other_metric</a>
        </div>
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
      <img alt="Line graph showing system performance over time with multiple lines for different systems"
        height="400" src="../assets/graphique2.png" width="600" />
        <iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Fdesign%2F2yyD2VY6aAer33Ns7pWHfd%2FIMH-copilote%3Fm%3Ddev%26node-id%3D38%253A37" allowfullscreen></iframe>
    </div>
  </div>
</template>
