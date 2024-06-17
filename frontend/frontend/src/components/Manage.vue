<script setup>
import { ref } from 'vue';
import axios from 'axios'
let displayAccountCreation = ref(false);
let displayAccountDelete = ref(false);
let displayAccount = ref(false);
let displayFileInput = ref(false);
let displayFileDelete = ref(false);
let displayFile = ref(false);
let displayUserEditForm = ref(false);
let displayTeam = ref(false);
let displayTeamInput = ref(false);
let displayTeamDelete = ref(false);

const DisplayMethod = (section, event) => {
  switch (section) {
    case "user":
      displayAccountCreation.value = false;
      displayAccountDelete.value = false;
      displayAccount.value = false;
      displayUserEditForm.value = false;
      switch (event) {
        case "displayAccountCreation":
          displayAccountCreation.value = true;
          break;
        case "displayAccountDelete":
          displayAccountDelete.value = true;
          break;
        case "displayAccount":
          displayAccount.value = true;
          break;
        case "displayUserEditForm":
          displayUserEditForm.value = true;
          break;
        default:
          break;
      }
      break;
    case "system":
      displayFileInput.value = false;
      displayFileDelete.value = false;
      displayFile.value = false;
      switch (event) {
        case "displayFileInput":
          displayFileInput.value = true;
          break;
        case "displayFileDelete":
          displayFileDelete.value = true;
          break;
        case "displayFile":
          displayFile.value = true;
          break;
        default:
          break;
      }
      break;
    case "team":
      displayTeam.value = false;
      displayTeamInput.value = false;
      displayTeamDelete.value = false;
      switch (event) {
        case "displayTeamInput":
          displayTeamInput.value = true;
          break;
        case "displayTeamDelete":
          displayTeamDelete.value = true;
          break;
        case "displayTeam":
          displayTeam.value = true;
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }
};
</script>

<template>

  <div class="bg-gray-700 p-5 rounded-lg">
    User Management
    <div class="manageUser">

      <div class="manageUser">
        <button @click="DisplayMethod('user', 'displayAccountCreation')" class="cursor-pointer">Create a user</button>
        <button @click="DisplayMethod('user', 'displayUserEditForm')" class="cursor-pointer">Edit a user</button>
        <button @click="DisplayMethod('user', 'displayAccountDelete')" class="cursor-pointer">Delete a user</button>
        <button @click="DisplayMethod('user', 'displayAccount')" class="cursor-pointer">View users</button>
      </div>
      <Transition>
        <div v-if="displayAccountCreation">
          <form @submit.prevent="submitFormRegister">
            <input type="text" placeholder="Username" v-model="username" required>
            <input type="text" placeholder="Password" v-model="password" required>
            <input type="text" placeholder="Description (optional)" v-model="userinfo">
            <select v-model="selectedUserTeam">
              <option disabled value="">Select a team</option>
              <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
            </select>
            <input type="checkbox" id="checkbox" v-model="is_superuser" />
            <label for="checkbox">Admin: {{ is_superuser }}</label>
            <button class="cursor-pointer" type="submit">Create</button>
          </form>
          <br />
          Log:
          <div style="background-color: #110618" id="console">
            {{ consoleAccountCreationMessage }}
          </div>
        </div>
      </Transition>

      <div v-if="displayUserEditForm">
        <form @submit.prevent="updateUser">
          <label for="useredit">User to edit</label>
          <select id="useredit" v-model="selectedUserId" @change="loadUserData" required>
            <option disabled value="">Select a user</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>

          <!-- Form to edit user details -->
          <div v-if="editedUser.id">
            <input type="text" placeholder="Edit username" v-model="editedUser.username" required>
            <input type="password" placeholder="Edit password" v-model="editedUser.password">
            <input type="text" placeholder="Edit description" v-model="editedUser.info">

            <label for="team">Team:</label>
            <select id="team" v-model="editedUser.team">
              <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
            </select>

            <input type="checkbox" id="checkbox" v-model="editedUser.is_superuser" />
            <label for="checkbox">Admin: {{ editedUser.is_superuser }}</label>
            <button type="submit">Save</button>
            <div>
              Leave password field empty if you do not want to change it.
            </div>
          </div>

        </form>

        <br />
        Log:
        <div class="bg-gray-800" id="console">
          {{ consoleEditUserMessage }}
        </div>
      </div>

      <div v-if="displayAccountDelete">
        <form @submit.prevent="deleteUserById">
          <select v-model="selectedUser" required>
            <option disabled value="">Select a user</option>
            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
          </select>
          <button class="cursor-pointer" type="submit">Delete</button>
        </form>
        <br />
        Log:
        <div class="bg-gray-800" id="console">
          {{ consoleDeleteAccountMessage }}
        </div>
      </div>

      <div v-if="displayAccount">
        <table>
          <thead>
            <tr>
              <th>Username</th>
              <th>Team</th>
              <th>Admin</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.username }}</td>
              <td>{{ user.team }}</td>
              <td>{{ user.is_superuser }}</td>
              <td>{{ user.info }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    System Management
    <div class="manageSystem">

      <div>
        <button @click="DisplayMethod('system', 'displayFileInput')" class="cursor-pointer">Add / Update evaluation
          files</button>
        <button @click="DisplayMethod('system', 'displayFileDelete')" class="cursor-pointer">Remove a system</button>
        <button @click="DisplayMethod('system', 'displayFile')" class="cursor-pointer">View systems</button>
      </div>
      <div v-if="displayFileInput">
        <form @submit.prevent="submitFormAddEval">
          <div>
            Step 1: Select the directory with directory rounds inside, ensuring the directory names match the round
            names and contain
            the evaluation files</div>
          <label for="directory-input" class="custom-button">
            {{ buttonText }}
          </label>
          <input id="directory-input" type="file" @change="handleFileChange" webkitdirectory required
            class="custom-file-input">
          <br />
          <div>
            Step 2: Select the team associated with the systems you have added</div>
          <select v-model="selectedTeam" required>
            <option disabled value="">Select a team</option>
            <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
          </select>
          <div> Step 3: If your systems belong to the same "family", you can name them here (optional)</div>
          <input type="text" placeholder="System collection" v-model="systemcollection">
          <br>
          -------------------------
          <br>
          <button class="cursor-pointer" type="submit">Create</button>
        </form>
        <!--Console-->
        <br />
        Log:
        <div style="background-color: #040D05;" id="console">
          {{ consoleaddsystemMessage }}
        </div>
      </div>

      <div v-if="displayFileDelete">
        <form @submit.prevent="deleteEvalBySystem">
          <select v-model="selectedSystem" required>
            <option disabled value="">Select a system</option>
            <option value="">Deleted all systems</option>
            <option v-for="ev in uniqueSystems" :key="ev" :value="ev">{{ ev.System_id }} / {{ ev.Team }}</option>
          </select>
          <button type="submit">Delete</button>
        </form>
        <!--Console-->
        <br />
        Log:
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
            <tr v-for="(ev, index) in uniqueSystems" :key="index">
              <td>{{ ev.System_id }}</td>
              <td>{{ ev.Team }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    Team Management
    <div class="manageTeam">

      <div>
        <button @click="DisplayMethod('team', 'displayTeamInput')" class="cursor-pointer">Create a team</button>
        <button @click="DisplayMethod('team', 'displayTeamDelete')" class="cursor-pointer">Delete a team</button>
        <button @click="DisplayMethod('team', 'displayTeam')" class="cursor-pointer">View teams</button>
      </div>
      <div v-if="displayTeamInput">
        <form @submit.prevent="addTeam">
          <input type="text" placeholder="Team name" v-model="teamname" required>
          <button type="submit">Create</button>
        </form>
        <br />
        Log:
        <div class="bg-gray-800" id="console">
          {{ consoleaddteamMessage }}
        </div>
      </div>

      <div v-if="displayTeamDelete">
        <form @submit.prevent="deleteTeamById">
          <select v-model="team" required>
            <option disabled value="">Select a team</option>
            <option v-for="team in teams" :key="team.name" :value="team.name">{{ team.name }}</option>
          </select>
          <button type="submit">Delete</button>
        </form>
        <br />
        Log:
        <div class="bg-gray-800" id="console">
          {{ consoledeleteteamMessage }}
        </div>
      </div>

      <div v-if="displayTeam">
        <table>
          <thead>
            <tr>
              <th>Team Name</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(team, index) in teams" :key="index">
              <td>{{ team.name }}</td>
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
      is_superuser: false,
      //message dans les div consoles
      consoleaddsystemMessage: '',
      consoledeletesystemMessage: '',
      consoleAccountCreationMessage: '',
      consoleDeleteAccountMessage: '',
      consoleEditUserMessage: '',
      consoleaddteamMessage: '',
      consoledeleteteamMessage: '',

      selectedUserId: '', // ID de l'utilisateur sélectionné
      editedUser: {}, // Données de l'utilisateur en cours d'édition
      teamname: '',
      buttonText: "Select Directory",
    };
  },
  created() {
    // Récupérer le token d'authentification depuis le store Vuex
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
    handleFileChange(event) {
      const files = event.target.files;
      console.log("Files selected:", files); // Vérifiez si cette ligne s'affiche dans la console
      if (files.length > 0) {
        this.buttonText = `${files.length} files selected`;
      } else {
        this.buttonText = "Select Directory";
      }
      console.log("Button text updated to:", this.buttonText); // Vérifiez si cette ligne s'affiche dans la console
    },

    loadUserData() {
      const user = this.users.find(user => user.id === this.selectedUserId);
      if (user) {
        this.editedUser = { ...user }; // Copie les données de l'utilisateur sélectionné dans editedUser
      }
    },
    //Sign up
    submitFormRegister(e) {
      const formData = {
        username: this.username,
        password: this.password,
        team: this.selectedUserTeam,
        info: this.userinfo,
        is_superuser: this.is_superuser
      }
      axios
        .post('/api/v1/users/', formData)
        .then(response => {

          this.$router.push('/')
          console.log(response)
          this.consoleAccountCreationMessage = "Successful operation"
          this.getUsers()
        })
        .catch(error => {
          console.log(error)
          this.consoleAccountCreationMessage = error
        })
    },

    getUsers() {
      axios.get('api/user/userslist', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(userResponse => {
          // Traiter les informations de l'utilisateur ici
          this.users = userResponse.data
          this.$store.commit('setUser', userResponse.data)
          console.log(userResponse.data);

        })
        .catch(userError => {
          console.error('Erreur lors de la récupération des informations de l\'utilisateur :', userError);
        });
    },

    deleteUserById() {

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
          this.consoleDeleteAccountMessage = "Successful operation"
          // Mettez à jour votre interface utilisateur si nécessaire
        })
        .catch(error => {
          console.error(error);
          this.consoleAccountCreationMessage = error
        });
    },

    updateUser() {
      const passwordValue = this.editedUser.password // Supprimer les espaces vides
      const passwordToSend = passwordValue ? passwordValue : "nothingtochange"; // Si vide, envoyez nothingtochange

      axios.put(`api/user/${this.editedUser.id}/`, {
        username: this.editedUser.username,
        password: passwordToSend,
        team: this.editedUser.team,
        info: this.editedUser.info,
        is_superuser: this.editedUser.is_superuser
      }, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`,
        }
      }).then(response => {
        console.log(response.data);
        this.getUsers()
        this.consoleEditUserMessage = "Successful operation"
        // Traitez la réponse ici, mettez à jour l'interface utilisateur si nécessaire
      }).catch(error => {
        console.error(error);
        this.consoleEditUserMessage = error
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
          this.$store.commit('setTeams', response.data)
          console.log(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    },

    addTeam() {
      axios.post('api/team/', { name: this.teamname, info: this.teaminfo }, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })

        .then(response => {

          this.consoleaddteamMessage = "Successful operation"
          this.getTeam()


        })
        .catch(error => {
          this.consoleaddteamMessage = "Erreur : " + error;
        });

    },



    deleteTeamById() {
      axios.delete(`/api/team/${this.team}/`, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`,
        }
      }).then(response => {
        this.consoledeleteteamMessage = "Successful operation"
        this.getTeam(); // Refresh the team list after deletion
      }).catch(error => {
        this.consoledeleteteamMessage = error
        console.error(error);
      });
    },


    // CRUD EVAL
    getEval() {
      axios.get('api/eval/', {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })
        .then(response => {

          this.evals = response.data
          this.$store.commit('setEvals', response.data)
          const uniqueSystems = Array.from(
            new Map(response.data.map(item => [item.System_id, { System_id: item.System_id, Team: item.Team }])).values()
          );

          this.uniqueSystems = uniqueSystems;

        })
        .catch(error => {
          console.error(error);
        });

    },



    addEval(newEval) {
      this.consoleaddsystemMessage = "Traitement en cours...";
      axios.post('api/eval/', newEval, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }
      })

        .then(response => {

          this.consoleaddsystemMessage = "Successful operation : " + response.data.message;
          this.getEval()


        })
        .catch(error => {
          this.consoleaddsystemMessage = "Error : " + error;
        });

    },

    deleteEvalBySystem() {
      this.consoledeletesystemMessage = "Traitement en cours...";
      let AllEvalsDelete = [];
      this.evals.forEach(element => {
        if (element.System_id === this.selectedSystem.System_id) {
          AllEvalsDelete.push(element.id)
        }
      });

      axios.delete(`api/eval/`, {
        headers: {
          'Authorization': `Token ${this.$store.state.token}`
        }, data: {
          ids: AllEvalsDelete
        }
      })
        .then(response => {
          console.log(response);
          this.consoledeletesystemMessage = "Successful operation : " + response.data.message;
          this.getEval()

        })
        .catch(error => {
          console.error(error);
          this.consoledeletesystemMessage = "Error : " + error;
        });



    },

    //Upload
    processEvalFile(file) {
      return new Promise((resolve, reject) => {
        // Utilisation de l'expression régulière pour capturer le nom complet du dossier contenant le fichier
        const folderMatch = file.webkitRelativePath.match(/\/([^/]+)\/[^/]+$/);
        const round = folderMatch ? folderMatch[1].trim() : null;  // Nom du dossier parent immédiat
        // Utiliser le nom du fichier comme valeur pour le système avant le premier point
        const systemMatch = file.name.match(/^([^\.]+)/);
        const system = systemMatch ? systemMatch[1].trim() : file.name.trim();

        const reader = new FileReader();
        reader.onload = (event) => {
          const content = event.target.result;
          const lines = content.split('\n');

          /*  for (const line of lines) {
             const parts = line.trim().split('\t');
             if (parts.length === 3) {
               const metric = parts[0];
               const value = parts[2];
               if (metric === "runid") {
                 system = value;
               }
             }
           } */
          for (const line of lines) {
            const parts = line.trim().split('\t');
            if (parts.length === 3) {
              if (parts[0] !== "num_ret" && parts[0] !== "num_rel" && parts[0] !== "num_rel_ret") {
                const metric = parts[0].trim();
                const query = parts[1].trim();
                const value = parts[2].trim();
                const newEval = {
                  System_collection: this.systemcollection,
                  Team: this.selectedTeam,
                  System_id: system,
                  Round: round,
                  Query: query,
                  Metric: metric,
                  Value: value
                };
                this.allNewEvals.push(newEval);
              }
            }
          }
          resolve(); // Résoudre la promesse une fois que toutes les opérations sont terminées
        };
        reader.readAsText(file);
      });
    },

    submitFormAddEval(event) {
      const files = event.target[0].files;
      this.traverseFiles(files);

    },

    traverseFiles(files) {
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
.manageUser {
  background-color: #37203D;
}

.manageSystem {
  background-color: #203D32;
}

.manageTeam {
  background-color: #946453;
}

table th {
  color: white;
  font-weight: bold;
  /* Changer la couleur du texte en noir */
}

button:hover,
select:hover {
  font-weight: bold;
}

table tr {
  color: white;
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

.custom-file-input {
  display: none;
}

.custom-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #284723;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  text-align: center;
}

.custom-button:hover {
  background-color: #35612f;
}
</style>
