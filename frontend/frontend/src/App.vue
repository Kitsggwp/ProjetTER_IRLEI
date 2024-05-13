<script setup>

import { ref } from 'vue';
import Epoque from './components/Epoque.vue';
import Query from './components/Query.vue';
import System from './components/System.vue';

const searchTerm = ref('');
const currentUser = 'Matthew Parker';
const isDropdownOpen = ref(false);
const currentWindow = ref('Epoque');

const currentComponent = ref('Epoque'); // Par défaut : affiche Epoque
const setCurrentComponent = (componentName) => {
  currentComponent.value = componentName;
};



const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};



</script>


<template>
  <!-- Headbar -->

    <div class="bg-gray-900 headBar flex justify-between items-center">
      <h1 id="title">Interface recherche</h1>
      <div>
        <input v-model="searchTerm" class="bg-gray-700 p-2 rounded" placeholder="Chercher un système" type="text" id="searchBar"/>
        <div class="inline-block relative">
          <button class="ml-4 bg-gray-700 p-2 rounded" @click="toggleDropdown" id="profileButton">
            {{ currentUser }}
            <i class="fas fa-chevron-down"></i>
            <img alt="Profile picture" id="pp"src="./assets/profile.png" />
          </button>
          <div v-if="isDropdownOpen" class="absolute bg-gray-700 text-white mt-1 rounded">
            <a class="green block px-4 py-2 hover:bg-gray-600" href="#">Profile</a>
            <a class="green block px-4 py-2 hover:bg-gray-600" href="#">Logout</a>
          </div>
        </div>
      </div>
    </div>
      <!-- Sidebar -->
    <div class="flex">
      <div class="bg-gray-900 p-5" id="sidebar">
        
        <div class="text-gray-400">IRLEI</div>
        <div class="mt-10">
          <a @click="setCurrentComponent('Epoque')" class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/calendarW.svg" id="sbLogo"></img>
            <span>Époques</span>
          </a>
          <a @click="setCurrentComponent('Query')" class="flex items-center text-gray-300 hover:text-white" href="#">
            <img  src="./assets/loupe.svg" id="sbLogo"></img>
            <span>Requêtes</span>
          </a>
          <a @click="setCurrentComponent('System')" class="flex items-center text-gray-300 hover:text-white" href="#">
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
        <!-- Fenêtre qui change -->
        <component :is="currentComponent"></component>
      </div>
    </div>
  
</template>



<style>
body{
  background-color: #111827
}
#title{
  color: white;
  font-weight: bolder;
  font-size: 1.5rem;
  
}

button{
  background: none;
  border: none;
  border-radius: 5px;
  padding: 5px;
  margin-right : 10px;
  color: white;
  font-size: 1rem;
  font-family: Arial, Helvetica, sans-serif;
  cursor: pointer;
}

select{
  background: none;
  border: none;
  border-radius: 5px;
  padding: 5px;
  margin-right : 10px;
  color: white;
  font-size: 1rem;
  font-family: Arial, Helvetica, sans-serif;
  cursor: pointer;
}

.subtitle{
  color: white;
  font-size: 1.25rem;
  font-weight: bolder;
  
}

.headBar{
  padding: 1.5rem;
}

#sidebar {
  bottom: 0;
  width:20%;
}
#sidebar a {
  padding: 0.75rem;
  margin-bottom: 1rem;
}
#sidebar > div > a, .green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
  
  
}

#sidebar > div > a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }

#searchBar {
  border-radius: 5px;
  height : 2.5rem;
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  
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
#graph{
  padding: 20px;
  border: 1px solid white;
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
<script>
import { ref } from 'vue';

export default {
  components: {
    Epoque,
    Query,
    System
  },
  setup() {
    return {
      searchTerm,
      currentUser,
      isDropdownOpen,
      currentWindow,
      setCurrentComponent,
      currentComponent,
      toggleDropdown
    };
  }
};
</script>