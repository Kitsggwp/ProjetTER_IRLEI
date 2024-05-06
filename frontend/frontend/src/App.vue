<script setup>
import axios from 'axios';
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue';
import TheWelcome from './components/TheWelcome.vue';
import WelcomeItem from './components/WelcomeItem.vue';
</script>

<template>
  <div id="app">
    <div id="headBar">
       <--! Barre de navigation !-->
      <nav>
        <ul>
          <li><RouterLink to="/">Accueil</RouterLink></li>
          <li><RouterLink to="/about">A propos</RouterLink></li>
          <li><RouterLink to="/contact">Contact</RouterLink></li>
        </ul>
      </nav> 
    </div>
    <div class="menu">
      <ul>
        <li @click="currentTab = 'Epoque'" :class="{ 'active': currentTab === 'Epoque' }">Epoque</li>
        <li @click="currentTab = 'Requête'" :class="{ 'active': currentTab === 'Requête' }">Requête</li>
        <li @click="currentTab = 'Système'" :class="{ 'active': currentTab === 'Système' }">Système</li>
      </ul>
    </div>
    <div id="mid">
      <header>
        <h1>Interface IRLEI</h1>
      </header>

      <div class="parameters">
        <h2>Paramètres</h2>
        <div class="parameter">
          <label for="epoque">Epoque:</label>
          <select id="epoque" v-model="selectedEpoques" multiple>
            <option v-for="epoque in epoques" :value="epoque">{{ epoque }}</option>
          </select>
        </div>
        <div class="parameter">
          <label for="systeme">Système:</label>
          <select id="systeme" v-model="selectedSystemes" multiple>
            <option v-for="systeme in systemes" :value="systeme">{{ systeme }}</option>
          </select>
        </div>
        <div class="parameter">
          <label for="mesure">Mesure:</label>
          <select id="mesure" v-model="selectedMesures" multiple>
            <option v-for="mesure in mesures" :value="mesure">{{ mesure }}</option>
          </select>
        </div>
      </div>

      <div class="content">
        <div v-if="currentTab === 'Epoque'">
          <h2>Epoque</h2>
          <HelloWorld></HelloWorld>
        </div>
        <div v-else-if="currentTab === 'Requête'">
          <h2>Requête</h2>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris dapibus urna nibh, nec consectetur erat
            cursus eu. Etiam vitae dui eu ligula egestas tempus. Nam non vestibulum sapien. Pellentesque sagittis felis
            quam. Proin enim nisi, porttitor quis diam nec, blandit scelerisque ligula. Vestibulum ante ipsum primis in
            faucibus orci luctus et ultrices posuere cubilia curae; Nulla vel congue neque. Sed in est molestie,
            convallis augue ut, pulvinar velit. Vestibulum id urna leo. Cras pulvinar magna ipsum, vitae iaculis ipsum
            auctor eu. Etiam tristique ut quam eget consequat. Morbi eleifend massa quis orci viverra, eu porta sem
            malesuada. Morbi justo ligula, pharetra nec ligula vel, dapibus suscipit erat. Donec sed lobortis ante.
            Aliquam sit amet viverra est. Suspendisse id justo consectetur orci tincidunt suscipit.

            Integer porttitor neque mi, eu aliquam sem aliquam quis. Pellentesque sit amet accumsan justo. Suspendisse
            congue ipsum vitae quam elementum, at placerat enim scelerisque. Quisque id sem sed nulla convallis egestas
            mattis non risus. Pellentesque convallis non lectus eget interdum. Etiam faucibus eros ac ex feugiat, a
            ultrices lacus ultricies. Suspendisse a finibus mi. Proin accumsan ex ut nisi fringilla eleifend. Sed id
            congue tellus.

            Donec consequat pharetra purus id ornare. Sed finibus dui quis ante congue finibus. Maecenas vel facilisis
            leo. Etiam vel ipsum quis tortor hendrerit fringilla. Nam et erat lobortis, vestibulum metus sed, ultricies
            tortor. Mauris id euismod ex. Nunc ac magna a neque venenatis fermentum. Quisque vel sapien tortor.
            Suspendisse venenatis rhoncus nunc, ut bibendum libero molestie in. Sed tristique eget lorem a dignissim.
            Cras fringilla luctus congue. Aenean rutrum nibh fermentum leo dapibus tempor.</p>
          <!-- Contenu de la page Requête -->
        </div>
        <div v-else>
          <h2>Système</h2>
          <TheWelcome></TheWelcome>
          <!-- Contenu de la page Système -->
        </div>
      </div>
    </div>

  </div>
</template>

<script>




export default {
  data() {

    return {
      selectedEpoques: [],
      selectedSystemes: [],
      selectedMesures: [],
      epoques: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      systemes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      mesures: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      responseData: null,
      currentTab: 'Epoque' // Onglet actif par défaut
    };
  },
  methods: {
    fetchData() {
      axios.get('http://127.0.0.1:8000/test')
        .then(response => {
          this.responseData = response.data;
          console.log(response.data)
        })
        .catch(error => {
          console.error('Erreur lors de la récupération des données :', error);
        });
    }
  },
  mounted() {
    this.fetchData(); // Appeler fetchData lorsque le composant est monté
  }
};
</script>

<style>
.parameters {
  margin-top: 40px;
}

.parameters {
  display: flex;
  justify-content: center;
  flex-direction: row;
  margin-right: 20px;
  /* Ajoute un espacement entre les paramètres */
}

.parameters label {
  margin-right: 5px;
  /* Ajoute un petit espacement entre le label et le select */
}

#app {
  display: flex;
  flex-direction: row;
}

#mid {
  display: flex;
  flex-direction: column;
}

/* Styles pour le menu */
.menu {
  width: 200px;
  background-color: #f2f2f2;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  color: black;
}

.menu ul {
  list-style-type: none;
  padding: 0;
}

.menu li {
  padding: 15px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}

.menu li.active {
  background-color: #ddd;
}

/* Styles pour le header */
header {
  position: fixed;
  top: 0;
  padding: 20px;
}

/* Styles pour le contenu */
.content {
  padding: 20px;
}
</style>
