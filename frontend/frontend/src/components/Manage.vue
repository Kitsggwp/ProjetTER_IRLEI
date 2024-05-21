<script setup>
import { ref } from 'vue';
import axios from 'axios'
const displayAccountCreation = ref(false);
const displayAccountDelete = ref(false);
const displayFileInput = ref(false);
const displayFileDelete = ref(false);

</script>

<template>
  <div class="bg-gray-700 p-5 rounded-lg">
    Gestion des utilisateurs
    <div class="bg-gray-800">

      <div class="bg-gray-600">
        <button @click="displayAccountCreation = !displayAccountCreation" class="cursor-pointer">Créer un
          utilisateur</button>
        <button class="cursor-pointer">Modifier un utilisateur</button>
        <button @click="displayAccountDelete = !displayAccountDelete" class="cursor-pointer">Supprimer un
          utilisateur</button>
      </div>
      <div v-if="displayAccountCreation">
        <form @submit.prevent="submitFormRegister">
          <input type="text" placeholder="Nom d'utilisateur" v-model="username">
          <input type="text" placeholder="Mot de passe" v-model="password">
          <select v-model="selectedTeam" required>
            <option disabled value="">Sélectionnez une équipe</option>
            <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Créer</button>
        </form>
      </div>

      <!-- marche pas pour le moment -->
      <div v-if="displayAccountDelete">
        <form @submit.prevent="deleteUserById">
          <select v-model="selectedUser" required>
            <option disabled value="">Sélectionnez un utilisateur</option>
            <option v-for="user in user" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Supprimer</button>
        </form>
      </div>

    </div>
    Gestion des systèmes
    <div class="bg-gray-800">

      <div class="bg-gray-600">
        <button @click="displayFileInput = !displayFileInput" class="cursor-pointer">Ajouter des fichiers
          d'évaluations</button>
        <button class="cursor-pointer" @click="displayFileDelete = !displayFileDelete"> Retirer un système de la base de
          données</button>
      </div>
      <div v-if="displayFileInput">
        <form @submit.prevent="submitFormAddEval">
          <input type="file" directory webkitdirectory>
          <br />
          <select v-model="selectedTeam" required>
            <option disabled value="">Sélectionnez une équipe</option>
            <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
          </select>
          <input type="text" placeholder="System collection" v-model="systemcollection">
          <button class="cursor-pointer" type="submit">Créer</button>
        </form>
        <!--Console-->
        <br />
        Log :
        <div class="bg-gray-800" id="console">

        </div>
      </div>

      <div v-if="displayFileDelete">
        <form @submit.prevent="deleteEvalBySystem">
          <select v-model="selectedSystem">
            <option disabled value="">Sélectionnez un système</option>
            <option v-for="ev in uniqueSystems" :key="ev" :value="ev">{{ ev }}</option>
          </select>
          <button type="submit">Supprimer</button>
        </form>
        <!--Console-->
        <br />
        Log :
        <div class="bg-gray-800" id="console">

        </div>
      </div>
    </div>
  </div>

</template>

<script>
import { ref } from 'vue';

export default {
  data() {
    return {
      selectedTeam: '', // Pour stocker l'ID de l'équipe sélectionnée
      teams: [], // Pour stocker la liste des équipes récupérées depuis l'API
      evals: [], // stocker toutes les evals
      selectedSystem: '', // Pour stocker le système sélectionné dans la liste déroulante
      selectedUser: '', //Pour stocker le user sélectionné dans la liste déroulante
      uniqueSystems: '', // liste evals avec nom des systems uniques
      user: '', //stocker les infos sur les users
      allNewEvals: []
    };
  },
  created() {
    // Récupérer le token d'authentification depuis le local storage ou store Vuex
    const token = this.$store.state.token;
    if (!token) {
      console.error('Token d\'authentification non trouvé.');
    } else {
      // récupérer les infos utilisateurs (group, username...)
      this.getUser()

      // récupérer les evals
      this.getEval()

      //récupérer les teams
      this.getTeam()
    }



  },
  methods: {
    //Sign up
    submitFormRegister(e) {
      const formData = {
        username: this.username,
        password: this.password,
        team: this.selectedTeam
      }
      console.log(formData)
      axios
        .post('/api/v1/users/', formData)
        .then(response => {

          this.$router.push('/')
          console.log(response)
        })
        .catch(error => {
          console.log(error)
        })
    },

    getUser() {
      axios.get('api/users/', {
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

    deleteUserById() {
      console.log(this.selectedUser)

      axios.delete(`api/user/bulk-delete/`, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }, data: {
          ids: [this.selectedUser]
        }
      })
        .then(response => {
          //console.log(response.data.message);
          this.getUser()
          // Mettez à jour votre interface utilisateur si nécessaire
        })
        .catch(error => {
          console.error(error);
        });



    },
    //CRUD Team
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

    // CRUD EVAL
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

    addEval(newEval) {
      console.log(newEval)
      axios.post('api/eval/', newEval, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })

        .then(response => {

          console.log("normalement ca marche");
          this.getEval()


        })
        .catch(error => {
          console.error(error);
        });

    },

    deleteEvalBySystem() {
      console.log(this.selectedSystem)
      let AllEvalsDelete = [];
      this.evals.forEach(element => {
        if (element.System_id === this.selectedSystem) {
          AllEvalsDelete.push(element.id)
        }
      });
      console.log(AllEvalsDelete)

      axios.delete(`api/eval/`, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }, data: {
          ids: AllEvalsDelete
        }
      })
        .then(response => {
          //console.log(response.data.message);
          this.getEval()
          // Mettez à jour votre interface utilisateur si nécessaire
        })
        .catch(error => {
          console.error(error);
        });



    },

    //Upload
    processEvalFile(file) {
      return new Promise((resolve, reject) => {
        const roundMatch = file.webkitRelativePath.match(/\/([^/]+)_round/);
        const round = roundMatch ? roundMatch[1] : null;
        let system = 0;
        const reader = new FileReader();
        reader.onload = (event) => {
          const content = event.target.result;
          const lines = content.split('\n');
          for (const line of lines) {
            const parts = line.trim().split('\t');
            if (parts.length === 3) {
              const metric = parts[0];
              const value = parts[2];
              if (metric === "runid") {
                system = value;
              }
            }
          }
          for (const line of lines) {
            const parts = line.trim().split('\t');
            if (parts.length === 3) {
              const metric = parts[0];
              const query = parts[1];
              const value = parts[2];
              const newEval = { System_collection: this.systemcollection, Team: this.selectedTeam, System_id: system, Round: round, Query: query, Metric: metric, Value: value };
              this.allNewEvals.push(newEval);
            }
          }
          resolve(); // Résoudre la promesse une fois que toutes les opérations sont terminées
        };
        reader.readAsText(file);
      });
    },


    submitFormAddEval(event) {
      const files = event.target[0].files;
      console.log(event)
      this.traverseFiles(files);

    },

    traverseFiles(files) {
      console.log("traversefile");
      const promises = [];
      for (const file of files) {
        promises.push(this.processEvalFile(file));
      }
      Promise.all(promises).then(() => {
        this.addEval(this.allNewEvals);
      });
    },

  },





};
</script>