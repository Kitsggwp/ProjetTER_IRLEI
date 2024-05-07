<script setup>

import { ref } from 'vue';

const searchTerm = ref('');
const currentUser = 'Matthew Parker';
const isDropdownOpen = ref(false);
const isEpochDropdownOpen = ref(false);
const isMeasureDropdownOpen = ref(false);
const displayOption = ref('Best/Worst');
const displayMeanMedian = ref(false);
const displaySignificativeDifference = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const toggleEpochDropdown = () => {
  isEpochDropdownOpen.value = !isEpochDropdownOpen.value;
};

const toggleMeasureDropdown = () => {
  isMeasureDropdownOpen.value = !isMeasureDropdownOpen.value;
};


</script>


<template>
  <!-- Headbar -->

    <div class="bg-gray-900 p-4 flex justify-between items-center">
      <h1 class="text-xl">Interface recherche</h1>
      <div>
        <input v-model="searchTerm" class="bg-gray-700 p-2 rounded" placeholder="Chercher un système" type="text" id="searchBar"/>
        <div class="inline-block relative">
          <button class="ml-4 bg-gray-700 p-2 rounded" @click="toggleDropdown" id="profileButton">
            {{ currentUser }}
            <i class="fas fa-chevron-down"></i>
            <img alt="Profile picture" id="pp"src="./assets/profile.png" />
          </button>
          <div v-if="isDropdownOpen" class="absolute bg-gray-700 text-white mt-1 rounded">
            <a class="block px-4 py-2 hover:bg-gray-600" href="#">Profile</a>
            <a class="block px-4 py-2 hover:bg-gray-600" href="#">Logout</a>
          </div>
        </div>
      </div>
    </div>
    <div class="flex">
      <!-- Sidebar -->
      <div class="bg-gray-900 p-5" id="sidebar">
        
        <div class="text-gray-400">IRLEI</div>
        <div class="mt-10">
          <a class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/calendarW.svg" id="sbLogo"></img>
            <span>Époques</span>
          </a>
          <a class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/loupe.svg" id="sbLogo"></img>
            <span>Requêtes</span>
          </a>
          <a class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/system.svg" id="sbLogo"></img>
            <span>Systèmes</span>
          </a>
          <a class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Settings</span>
          </a>
          
        </div>
        <div class="absolute bottom-0 p-5">
          <div>Help</div>
          <div>Contact us</div>
        </div>
      </div>
      <!-- Main content -->
      <div class="flex-1 p-10" id="main">
        <div class="bg-gray-700 p-5 rounded-lg framed">
          <div class="flex justify-between items-center mb-5">
            <div class="text-gray-400">Côté macro / tâches d'évaluation globale</div>
              <div>
                <a>
                  <button class="cursor-pointer">
                    <img id="sbLogo" src="./assets/filter.svg"></img>
                  </button>
                </a>
                <a>
                  <button class="cursor-pointer">
                    <img id="sbLogo" src="./assets/gear.svg"></img>
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
                <a class="block px-4 py-2 hover:bg-gray-600" href="#">2023</a>
                <a class="block px-4 py-2 hover:bg-gray-600" href="#">2022</a>
              </div>
            </div>
            <div class="relative inline-block">
              <button @click="toggleMeasureDropdown" class="flex items-center bg-gray-800 text-white p-2 rounded">
                <i class="fas fa-tachometer-alt mr-2"></i>
                <span>Mesures</span>
                <i class="fas fa-chevron-down ml-2"></i>
              </button>
              <div v-if="isMeasureDropdownOpen" class="absolute bg-gray-800 text-white mt-1 rounded">
                <a class="block px-4 py-2 hover:bg-gray-600" href="#">recip_rank</a>
                <a class="block px-4 py-2 hover:bg-gray-600" href="#">other_metric</a>
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
          <div>
            <!-- Placeholder for graph -->
            <img alt="Line graph showing system performance over time with multiple lines for different systems"
              height="400" src="./assets/graphique.png" width="600" />
          </div>
        </div>
      </div>
    </div>
  
</template>



<style>

#sidebar {
  bottom: 0;
  width:20%;
}
#sidebar a {
  padding: 0.75rem;
  margin-bottom: 1rem;
}

#searchBar {
  border-radius: 5px;
  height : 2.5rem;
  display: inline-block;
}
#main {
  background-color: #1E2836;
  width: 100%;
}
#profileButton{
color: white;
height: 2.5rem;
}
#pp{
  height: 25px;
  width: 25px;
  vertical-align: middle;
}
#sbLogo{
  height: 20px;
  width: 20px;
  vertical-align: middle;
  color: white;
  margin-right: 10px;
}
.cursor-pointer{
  cursor: pointer;
  background: none;
}

.a,img{
  align-items: center;
  margin:0px;
  padding:0px;
}

.bg-gray-700 {
  background-color: #343D4D;
}

.bg-gray-800 {
  background-color: #1E2836;
}

.bg-gray-900 {
  background-color: #111827;
}

.text-white {
  color: #ffffff;
}

.min-h-screen {
  min-height: 100vh;
}

.p-4 {
  padding: 1rem;
}

.p-5 {
  padding: 1.25rem;
}

.mb-5 {
  margin-bottom: 1.25rem;
}

.ml-4 {
  margin-left: 1rem;
}

.ml-2 {
  margin-left: 0.5rem;
}

.mt-10 {
  margin-top: 2.5rem;
}

.justify-between {
  justify-content: space-between;
}

.items-center {
  align-items: center;
}
.relative {
  position: relative;
}
.flex {
  display: flex;
}
.inline-block {
  display: inline-block;
}
.block {
  display: block;
}

.w-64 {
  width: 16rem;
}
.rounded-lg{
  border-radius: 0.375rem;
}
.framed{
  margin: 2rem;
  padding: 2rem;
}
.text-xl {
  font-size: 1.25rem;
}

.text-gray-400 {
  color: #bdc3c7;
}

.span {
  color: #ffffff;

}

.hover\:text-white:hover {
  color: #ffffff;
}

.absolute {
  position: absolute;
}

.bottom-0 {
  bottom: 0;
}

.min-h-screen {
  min-height: 100vh;
}

body {
  line-height: inherit;
}


/* Ajoutez le reste des classes Tailwind traduites en CSS ici */
</style>
