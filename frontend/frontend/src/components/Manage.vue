<script setup>
import { ref } from 'vue';
import axios from 'axios'
const displayAccountCreation = ref(false);
const displayAccountDelete = ref(false);
const displayAccount = ref(false);
const displayFileInput = ref(false);
const displayFileDelete = ref(false);
const displayFile = ref(false);
const displayUserEditForm = ref(false);
const displayTeam = ref(false);
const displayTeamInput = ref(false);
const displayTeamDelete = ref(false);

</script>

<template>

  <div class="bg-gray-700 p-5 rounded-lg">
    Gestion des utilisateurs
    <div class="bg-gray-800">

      <div class="bg-gray-600">
        <button @click="displayAccountCreation = !displayAccountCreation" class="cursor-pointer">Créer un
          utilisateur</button>
        <button @click="displayUserEditForm = !displayUserEditForm" class="cursor-pointer">Modifier un
          utilisateur</button>
        <button @click="displayAccountDelete = !displayAccountDelete" class="cursor-pointer">Supprimer un
          utilisateur</button>
        <button @click="displayAccount = !displayAccount" class="cursor-pointer">Visualiser les
          utilisateurs</button>
      </div>
    <Transition>
      <div v-if="displayAccountCreation">
        <form @submit.prevent="submitFormRegister">
          <input type="text" placeholder="Nom d'utilisateur" v-model="username"><br/>
          <input type="text" placeholder="Mot de passe" v-model="password"><br/>
          <input type="text" placeholder="Description" v-model="userinfo"><br/>
          <select v-model="selectedUserTeam" required>
            <option disabled value="">Sélectionnez une équipe</option>
            <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Créer</button>
        </form>
      </div>
    </Transition>

      <div v-if="displayUserEditForm">
        <form @submit.prevent="updateUser">
          <label for="useredit">User à modifier</label>
          <select id="useredit" v-model="editedUser.id" required>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>

          <input type="text" placeholder=" Modifier username" v-model="editedUser.username" required>
          <input type="password" placeholder="Modifier password" v-model="editedUser.password" required>
          <input type="text" placeholder=" Modifier description" v-model="editedUser.info" required>

          <label for="team">Team :</label>
          <select id="team" v-model="editedUser.team" required>
            <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
          </select>

          <button type="submit">Enregistrer</button>
        </form>
      </div>

      <div v-if="displayAccountDelete">
        <form @submit.prevent="deleteUserById">
          <select v-model="selectedUser" required>
            <option disabled value="">Sélectionnez un utilisateur</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Supprimer</button>
        </form>
      </div>

      <div v-if="displayAccount">
        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Team</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.team }}</td>
              <td>{{ user.info }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    Gestion des systèmes
    <div class="bg-gray-800">

      <div class="bg-gray-600">
        <button @click="displayFileInput = !displayFileInput" class="cursor-pointer">Ajouter des fichiers
          d'évaluations</button>
        <button class="cursor-pointer" @click="displayFileDelete = !displayFileDelete"> Retirer un système </button>
        <button class="cursor-pointer" @click="displayFile = !displayFile"> Visualiser les systèmes
        </button>
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
          {{ consoleaddsystemMessage }}
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
          {{ consoledeletesystemMessage }}
        </div>
      </div>

      <div v-if="displayFile">
        <table>
          <thead>
            <tr>
              <th>System_id</th>
              <th>Team</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(system, index) in uniqueSystems" :key="index">
              <td>{{ system.System_id }}</td>
              <td>{{ system.Team }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    Gestion des teams
    <div class="bg-gray-800">

      <div class="bg-gray-600">
        <button @click="displayTeamInput = !displayTeamInput" class="cursor-pointer">Ajouter une team</button>
        <button class="cursor-pointer" @click="displayTeamDelete = !displayTeamDelete"> Retirer une team </button>
        <button class="cursor-pointer" @click="displayTeam = !displayTeam"> Visualiser les teams
        </button>
      </div>
      <div v-if="displayTeamInput">
        <form @submit.prevent="addTeam">
          <input type="text" placeholder="Name" v-model="teamname">
          <input type="text" placeholder="Info" v-model="teaminfo">
          <button class="cursor-pointer" type="submit">Créer</button>
        </form>
        <!--Console-->
        <br />
        Log :
        <div class="bg-gray-800" id="console">
          {{ consoleaddsystemMessage }}
        </div>
      </div>

      <div v-if="displayTeamDelete">
        <form @submit.prevent="deleteTeamById">
          <select v-model="team" required>
            <option disabled value="">Sélectionnez une team</option>
            <option v-for="team in teams" :key="team.name" :value="team.name">{{ team.name }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Supprimer</button>
        </form>
        <!--Console-->
        <br />
        Log :
        <div class="bg-gray-800" id="console">
          {{ consoledeletesystemMessage }}
        </div>
      </div>

      <div v-if="displayTeam">
        <table>
          <thead>
            <tr>
              <th>Team</th>
              <th>Info</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(team, index) in teams" :key="index">
              <td>{{ team.name }}</td>
              <td>{{ team.info }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>



</template>

<script>
import { ref } from 'vue';

export default {
  data() {
    return {
      selectedUserTeam: '', // Pour stocker l'ID de l'équipe sélectionnée lors de la création d'un user
      selectedTeam: '', // Pour stocker l'ID de l'équipe sélectionnée lors de la création des evals
      team: '', // Pour stocker l'ID de l'équipe sélectionnée lors de la suppression d'une team
      teams: [], // Pour stocker la liste des équipes récupérées depuis l'API
      evals: [], // stocker toutes les evals
      selectedSystem: '', // Pour stocker le système sélectionné dans la liste déroulante
      selectedUser: '', //Pour stocker le user sélectionné dans la liste déroulante
      uniqueSystems: [], // liste evals avec nom des systems uniques
      users: '', //stocker les infos sur les users
      allNewEvals: [],
      //message dans les div consoles
      consoleaddsystemMessage: '',
      consoledeletesystemMessage: '',
      editedUser: {
        id: '',
        username: '',
        password: '',
        team: ''
      },
      teamname: '',
    };
  },
  created() {
    // Récupérer le token d'authentification depuis le local storage ou store Vuex
    const token = this.$store.state.token;
    if (!token) {
      console.error('Token d\'authentification non trouvé.');
    } else {
      // récupérer la liste des users de la bdd
      this.getUsers()

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
        team: this.selectedUserTeam,
        info: this.userinfo
      }
      console.log(formData)
      axios
        .post('/api/v1/users/', formData)
        .then(response => {

          this.$router.push('/')
          console.log(response)
          this.getUsers()
        })
        .catch(error => {
          console.log(error)
        })
    },

    getUsers() {
      axios.get('api/users/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(userResponse => {
          // Traiter les informations de l'utilisateur ici
          this.users = userResponse.data
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
          this.getUsers()
          // Mettez à jour votre interface utilisateur si nécessaire
        })
        .catch(error => {
          console.error(error);
        });



    },

    updateUser() {
      console.log(this.editedUser.info)
      axios.put(`api/user/${this.editedUser.id}/`, {
        username: this.editedUser.username,
        password: this.editedUser.password,
        team: this.editedUser.team,
        info: this.editedUser.info
      }, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`,
        }
      }).then(response => {
        console.log(response.data);
        this.getUsers()
        // Traitez la réponse ici, mettez à jour l'interface utilisateur si nécessaire
      }).catch(error => {
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

    addTeam() {
      console.log(this.teamname)
      axios.post('api/team/', { name: this.teamname, info: this.teaminfo }, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })

        .then(response => {

          this.consoleaddsystemMessage = "Opération réussie"
          this.getTeam()


        })
        .catch(error => {
          this.consoleaddsystemMessage = "Erreur : " + error;
        });

    },



    deleteTeamById() {
      console.log(this.team)
      axios.delete(`/api/team/${this.team}/`, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`,
        }
      }).then(response => {
        this.getTeam(); // Refresh the team list after deletion
      }).catch(error => {
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

          const uniqueSystems = Array.from(
            new Map(response.data.map(item => [item.System_id, { System_id: item.System_id, Team: item.Team }])).values()
          );

          this.uniqueSystems = uniqueSystems;
          //  console.log(response.data)
          console.log(this.uniqueSystems)
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

          this.consoleaddsystemMessage = "Opération réussie : " + response.data.message;
          this.getEval()


        })
        .catch(error => {
          this.consoleaddsystemMessage = "Erreur : " + error;
        });

    },

    deleteEvalBySystem() {
      console.log(this.selectedSystem)
      let AllEvalsDelete = [];
      this.evals.forEach(element => {
        if (element.System_id === this.selectedSystem.System_id) {
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
          console.log(response);
          this.consoledeletesystemMessage = "Opération réussie";
          this.getEval()

        })
        .catch(error => {
          console.error(error);
          this.consoledeletesystemMessage = "Erreur : " + error;
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
<style>
table th {
  color: black;
  /* Changer la couleur du texte en noir */
}

table td {
  color: white;
  /* Changer la couleur du texte en noir */
}

option {
  color: black
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease-out;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
