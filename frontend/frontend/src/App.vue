<script setup>

import { ref } from 'vue';
import Epoque from './components/Epoque.vue';
import Query from './components/Query.vue';
import System from './components/System.vue';
import Profil from './components/Profil.vue';
import Manage from './components/Manage.vue';
import axios from 'axios'
const searchTerm = ref('');
const isDropdownOpen = ref(false);
const currentWindow = ref('Epoque');
const isLoginScreenDisplayed = ref(false);
const isSignupScreenDisplayed = ref(false);

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
      <div class="flex">
        <input v-model="searchTerm" class="bg-gray-700 p-2 rounded" placeholder="Chercher un système" type="text" id="searchBar"/>
  
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
          Se connecter
          <i class="fas fa-chevron-down"></i>
          <img alt="Profile picture" id="pp" src="./assets/profile.png" />
          </button>
            <div v-if="isDropdownOpen" class="absolute bg-gray-700 text-white mt-1 rounded" id="profilDiv">
              <a @click="isLoginScreenDisplayed =! isLoginScreenDisplayed" class="green block" href="#"> Login</a>
              <a @click="isSignupScreenDisplayed =! isSignupScreenDisplayed" class="green block" href="#"> Sign up</a>
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
          <a @click="setCurrentComponent('Manage')"class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Settings</span>
          </a>
          <a class="flex items-center text-gray-300 hover:text-white" href="#">
            <img src="./assets/settings.svg" id="sbLogo"></img>
            <span>Accessibility</span>
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

        <!--Login -->
        <div v-if="isLoginScreenDisplayed" class="loginBox">
          
          <div class="loginContent">    
           </br>
          
            <b style="padding-right: 20px;">Connexion</b>
            <a style="border: 1px solid red; color: red; cursor: pointer;" @click="isLoginScreenDisplayed =! isLoginScreenDisplayed">X</a>
            </br>
            <div>
              <form @submit.prevent="submitFormLogin">
                <input type="text" placeholder="Username" name="username" v-model="username" required>
                <input type="password" placeholder="Mot de passe" name="password" v-model="password" required>
                <button type="submit">Connexion</button>
              </form>
             
           </div>
          </div>
          
          
        </div>
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
.loginBox{
  
  position: fixed;
  z-index: 1;
  width: 30%;
  height: 30%;
  left: 40%;
  top: 40%;
}
option{
  background-color: #1E2836;
  color: white;
}

.loginContent{
  background-color: #343D4D;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 1.5rem;
  color: white;
}

.headBar{
  padding: 1.5rem;
}
#profilDiv > a, .green {
  text-decoration: none;;
  transition: 0.4s;  
  background-color: #1E2836;
  padding: 0.5rem;
}

#profilDiv > a:hover {
  color: white;
  background-color: rgba(20, 255, 177, 0.511);
  transition: 0.4s;  
}

a:hover {
  color: white;
  background-color: rgba(20, 255, 177, 0.511);
  transition: 0.4s;  
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
#console{
  background-color: #0a0d11;
  color:white;
  font-family: system-ui;
  min-height: 300px;
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
    Manage
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
      user:'', //stocker les infos sur l'user connecté
      uniqueSystems:'', // liste evals avec nom des systems uniques
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
    //Sign up
    submitFormSignup(e) {
            const formData = {
                username: this.username,
                password: this.password,
                email: this.username,
            }

            axios
                .post('/api/v1/users/', formData)
                .then(response => {

                    this.$router.push('/log-in')
                    console.log(response)
                })
                .catch(error => {
                    console.log(error)
                })
        },
    //Login
        submitFormLogin(e) {
            const formData = {
                username: this.username,
                password: this.password,
            }
            console.log(formData)
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
                      })
                
                .catch(error => {
                    console.log(error)
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
              this.$router.push('/'); // Redirection vers la page de connexion
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
      getUser()  {
        axios.get('api/user/', {
                       headers: {
                        'Authorization': `Token ${this.$store.state.token}`
                        }
                   })
                        .then(userResponse => {
                            // Traiter les informations de l'utilisateur ici
                            this.user = userResponse.data
                            console.log(userResponse.data);
                         
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
                        console.log(response.data);
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
                        
                        const uniqueSystems = [...new Set(response.data.map(ev => ev.System_id))];
                        this.uniqueSystems = uniqueSystems;
                      //  console.log(response.data)
                        console.log(uniqueSystems)
                      })
                       .catch(error => {
                         console.error(error);
                      });
                    
      },
    }
};
</script>