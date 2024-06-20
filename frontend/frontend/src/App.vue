<script setup>

import { ref } from 'vue';
import Epoque from './components/Epoque.vue';
import Query from './components/Query.vue';
import System from './components/System.vue';
import Profil from './components/Profil.vue';
import Manage from './components/Manage.vue';
import EpoqueDelta from './components/EpoqueDelta.vue';
import HelpContact from './components/HelpContact.vue';
import axios from 'axios'
const searchTerm = ref('');
const isDropdownOpen = ref(false);
const currentWindow = ref('Epoque');
const isLoginScreenDisplayed = ref(false);


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
  <title>IRLEI interface</title>
  <div class="bg-gray-900 headBar flex justify-between items-center">
    <h1 id="title">IRLEI</h1>
    <div class="flex">
      <!--
      <input v-model="searchTerm" class="bg-gray-700 p-2 rounded" placeholder="Search un système" type="text"
        id="searchBar" />
      -->
      <div v-if="isAuthenticated" class="inline-block relative">
        <!-- Contenu à afficher lorsque l'utilisateur est connecté -->
        <button class="ml-4 bg-gray-700 p-2 rounded" @click="toggleDropdown" id="profileButton">
          {{ name }}
          <i class="fas fa-chevron-down"></i>
          <img alt="Profile picture" id="pp" src="./assets/profile.png" />
        </button>
        <div v-if="isDropdownOpen" class="absolute bg-gray-700 text-white mt-1 rounded" id="profilDiv">
          <a class="green block" href="#">Profile</a>
          <a @click="logout" class="green block" href="#">Logout</a>
        </div>
      </div>
      <div v-else>
        <!-- Contenu à afficher lorsque l'utilisateur n'est pas connecté -->
        <button class="ml-4 bg-gray-700 p-2 rounded" @click="toggleDropdown" id="profileButton">
          Log in
          <i class="fas fa-chevron-down"></i>
          <img alt="Profile picture" id="pp" src="./assets/profile.png" />
        </button>
        <div v-if="isDropdownOpen" class="absolute bg-gray-700 text-white mt-1 rounded" id="profilDiv">
          <a @click="isLoginScreenDisplayed = !isLoginScreenDisplayed" class="green block" href="#"> Login</a>
        </div>
      </div>

    </div>
  </div>

  <!-- Sidebar -->
  <div class="flex">
    <div class="bg-gray-900 p-5" id="sidebar">

      <div class="mt-10">
        <div style="border: 1px solid white;"> <!--Rubrique analyse -->
          <h3>Analysis tool</h3>
          <a @click="setCurrentComponent('Epoque')" class="flex green items-center text-gray-300 hover:text-white"
            href="#">
            <img src="./assets/calendarW.svg" id="sbLogo"></img>
            <span>Round</span>
          </a>
          <a @click="setCurrentComponent('Query')" class="flex green items-center text-gray-300 hover:text-white"
            href="#">
            <img src="./assets/loupe.svg" id="sbLogo"></img>
            <span>Query</span>
          </a>
          <a @click="setCurrentComponent('System')" class="flex green items-center text-gray-300 hover:text-white"
            href="#">
            <img src="./assets/system.svg" id="sbLogo"></img>
            <span>System Diagnosis</span>
          </a>
          <a @click="setCurrentComponent('EpoqueDelta')" class="flex green items-center text-gray-300 hover:text-white"
            href="#">
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Round comparison</span>
          </a>
        </div>

        <div style="border: 1px solid white;"> <!--Rubrique paramètre -->
          <h3>System and user management</h3>
          <a v-if="user && user.length > 0 && (user[0].is_superuser || user.length > 1)"
            @click="setCurrentComponent('Manage')" class="flex green items-center text-gray-300 hover:text-white"
            href="#">
            <!--v-if="user.length > 1"-->
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Settings</span>
          </a>
          <!--Todo dont forget to delete the display=none -->
          <a class="green flex items-center text-gray-300 hover:text-white" style="display: none;" href="#"> 
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Accessibility</span>
          </a>
        </div>
      </div>
      <div @click="setCurrentComponent('HelpContact')" class="absolute bottom-0 p-5">
        <a>Help</a>
        <a>Contact us</a>
      </div>
    </div>
    <!-- Main content -->
    <div class="flex-1 p-10" id="main">
      <!-- Fenêtre qui change -->
      <Transition name="fade" mode="out-in">
        <component :is="currentComponent"></component>
      </Transition>

      <!--Login -->
      <div v-if="isLoginScreenDisplayed" class="loginBox">

        <div class="loginContent">
          </br>

          <b style="padding-right: 20px;">Log In</b>
          <a style="border: 1px solid red; color: red; cursor: pointer;"
            @click="isLoginScreenDisplayed = !isLoginScreenDisplayed">X</a>
          </br>
          <div>
            <form @submit.prevent="submitFormLogin">
              <input type="text" placeholder="Username" name="username" v-model="username"
                :class="{ 'input-error': usernameError }" required>
              <input type="password" placeholder="Mot de passe" name="password" v-model="password"
                :class="{ 'input-error': passwordError }" required>
              <button type="submit">Log In</button>
            </form>

          </div>
        </div>


      </div>
    </div>
  </div>

</template>



<style>
body {
  background-color: #111827
}

#title {
  color: white;
  font-weight: bolder;
  font-size: 1.5rem;

}

button {
  background: none;
  border: none;
  border-radius: 5px;
  padding: 5px;
  margin-right: 10px;
  color: white;
  font-size: 1rem;
  font-family: Arial, Helvetica, sans-serif;
  cursor: pointer;
}

select {
  background: none;
  border: none;
  border-radius: 5px;
  padding: 5px;
  margin-right: 10px;
  color: white;
  font-size: 1rem;
  font-family: Arial, Helvetica, sans-serif;
  cursor: pointer;
}

.subtitle {
  color: white;
  font-size: 1.25rem;
  font-weight: bolder;

}

.loginBox {

  position: fixed;
  z-index: 1;
  width: 30%;
  height: 30%;
  left: 40%;
  top: 40%;
}

h3 {
  color: white;
  font-size: 0.8rem;
  justify-content: center;
  display: flex;
  padding: 0.5rem;
  text-align: center;
}

option {
  background-color: #1E2836;
  color: white;
}

.loginContent {
  background-color: #343D4D;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.5rem;
  color: white;
}

.headBar {
  padding: 1.5rem;
}

.gridContainer {

  display: grid;
  grid-template-columns: repeat(3, minmax(150px, 1fr));
  /* Adjust the minmax value to fit your needs */
  padding: 10px;

}

#profilDiv>a,
.green {
  text-decoration: none;
  ;
  transition: 0.4s;
  background-color: #1E2836;
  padding: 0.5rem;
}

#profilDiv>a:hover {
  color: white;
  background-color: rgba(33, 240, 171, 0.642);
  transition: 0.4s;
}

a:hover {
  color: white;
  background-color: rgb(54, 179, 137);
  transition: 0.3s;
}

#sidebar {
  bottom: 0;
  width: 20%;
}

#sidebar a {
  padding: 0.75rem;
  margin-bottom: 1rem;
}

#sidebar>div>a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

#sidebar>div>a:hover {
  background-color: hsla(160, 100%, 37%, 0.2);
}

#searchBar {
  border-radius: 5px;
  height: 2.5rem;
  display: inline-block;
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;

}

#main {
  background-color: #1E2836;
  width: 100%;
}

#console {
  background-color: #0a0d11;
  color: white;
  font-family: system-ui;
  min-height: 300px;
}

#profileButton {
  color: white;
  height: 2.5rem;
}

#pp {
  height: 25px;
  width: 25px;
  vertical-align: middle;
}

#sbLogo {
  height: 20px;
  width: 20px;
  vertical-align: middle;
  color: white;
  margin-right: 10px;
}

#graph {
  padding: 20px;
  border: 1px solid white;
}

.cursor-pointer {
  cursor: pointer;
  background: none;
}

.a,
img {
  align-items: center;
  margin: 0px;
  padding: 0px;
}

.bg-gray-600 {
  background-color: #4a5361;
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

.rounded-lg {
  border-radius: 0.375rem;
}

.framed {
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.input-error {
  border: 1px solid red;
}

/* Ajoutez le reste des classes ici */
</style>
<script>
import { ref } from 'vue';

export default {
  components: {
    Epoque,
    Query,
    System,
    Profil,
    Manage,
    EpoqueDelta,
    HelpContact
  },
  setup() {
    return {
      searchTerm,
      currentUser,
      isDropdownOpen,
      currentWindow,
      setCurrentComponent,
      currentComponent,
      toggleDropdown,
    };

  },
  data() {
    return {
      teams: [], // Pour stocker la liste des équipes récupérées depuis l'API
      evals: [], // stocker toutes les evals
      user: '', //stocker les infos sur l'user connecté
      uniqueSystems: '', // liste evals avec nom des systems uniques
      usernameError: false,  // Property to track username error
      passwordError: false,  // Property to track password error
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token

    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  },
  created() {

    // Récupérer le token d'authentification depuis le local storage ou votre store Vuex
    const token = this.$store.state.token;
    if (!token) {
      console.error('Token d\'authentification non trouvé.');
    } else {
      // Si on est connecté on récupère les infos des tables Teams, evals et les infos du user connecté
      this.getEval()

      this.getTeam()

      this.getUser()

    }


  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated
    },
    name() {

      return this.$store.state.username;



    }
  },
  methods: {
    //Login
    submitFormLogin(e) {
      const formData = {
        username: this.username,
        password: this.password,
      }
      axios
        .post('/api/v1/token/login', formData)
        .then(response => {
          console.log(response)

          const token = response.data.auth_token
          const username = formData.username

          this.$store.commit('setToken', token)
          localStorage.setItem('username', username);
          localStorage.setItem('token', token);

          this.$store.commit('setToken', { token, username });

          axios.defaults.headers.common['Authorization'] = "Token " + token

          localStorage.setItem("token", token)

          // Récupère les infos du user connecté et les mets dans la variables user
          this.getUser();

          // Récupère les infos de la table Eval et les mets dans la variables evals
          this.getEval();

          // Récupère les infos de la table Team et les mets dans la variables teams
          this.getTeam();

          window.location.reload();
        })

        .catch(error => {
          console.log(error)
          if (error.response && error.response.status === 400) {
            // Assuming 400 status indicates incorrect credentials
            this.usernameError = true;
            this.passwordError = true;
          }
        })

    },


    //Logout
    logout() {
      const token = this.$store.state.token;

      if (token) {
        console.log(token);
        axios.post('/api/v1/token/logout', token, {
          headers: {
            'Authorization': `Token ${token}`
          }
        })
          .then(response => {
            console.log(response);
            // Gérer la réponse de la déconnexion si nécessaire
            // Supprimer le token du local storage
            localStorage.removeItem('token');
            // Réinitialiser le state de l'utilisateur dans le store Vuex
            this.$store.commit('removeToken');
            // Rediriger l'utilisateur vers la page de connexion ou une autre page si nécessaire
            this.user = [];
            this.teams = [];
            this.evals = [];
            window.location.reload();
          })
          .catch(error => {
            console.error(error);
            // Gérer les erreurs de déconnexion si nécessaire
          });
      } else {
        console.error('Token not found in local storage.');
        // Gérer le cas où le token n'est pas trouvé dans le stockage local
      }
    },

    // récupère les données du user connecté et les met dans la variable user
    getUser() {
      axios.get('api/user/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(userResponse => {
          // Traiter les informations de l'utilisateur ici
          this.user = userResponse.data

          this.$store.commit('setUser', userResponse.data)
          localStorage.setItem('user', userResponse.data);
          console.log(this.$store.state.user);

        })
        .catch(userError => {
          console.error('Erreur lors de la récupération des informations de l\'utilisateur :', userError);
        });
    },
    // récupère les données de la table team et les met dans la variable teams
    getTeam() {
      axios.get('api/team/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(response => {
          this.teams = response.data
          this.$store.commit('setTeams', response.data)
          console.log(this.$store.state.teams);
        })
        .catch(error => {
          console.error(error);
        });
    },

    // récupère les données de la table eval et les met dans la variable evals, met tous les system_id différents dans la variable uniqueSystems
    getEval() {
      console.log("get eval")
      axios.get('api/eval/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(response => {
          // console.log(response.data);
          this.evals = response.data
          this.$store.commit('setEvals', response.data)
          const uniqueSystems = [...new Set(response.data.map(ev => ev.System_id))];
          this.uniqueSystems = uniqueSystems;
          //  console.log(response.data)
          console.log(this.$store.state.evals)
        })
        .catch(error => {
          console.error(error);
        });

    },
  }
};
</script>