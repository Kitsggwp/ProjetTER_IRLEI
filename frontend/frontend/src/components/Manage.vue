<script setup>
import { ref } from 'vue';
const displayAccountCreation = ref(false);
const displayFileInput = ref(false);
</script>

<template>
    <div class="bg-gray-700 p-5 rounded-lg">
        Gestion des utilisateurs
        <div class="bg-gray-800">

            <div class="bg-gray-600">
                <button @click="displayAccountCreation = !displayAccountCreation" class="cursor-pointer">Créer un
                    utilisateur</button>
                <button class="cursor-pointer">Modifier un utilisateur</button>
                <button class="cursor-pointer">Supprimer un utilisateur</button>
            </div>
            <div v-if="displayAccountCreation">
                <form @submit.prevent="submitFormRegister">
                    <input type="text" placeholder="Nom d'utilisateur">
                    <input type="text" placeholder="Mot de passe">
                    <input type="text" placeholder="Team">
                    <button class="cursor-pointer" type="submit">Créer</button>
                </form>
            </div>

        </div>
        Gestion des systèmes
        <div class="bg-gray-800">

            <div class="bg-gray-600">
                <button @click="displayFileInput = !displayFileInput" class="cursor-pointer">Ajouter des fichiers
                    d'évaluations</button>
                <button class="cursor-pointer"> Retirer un système de la base de données</button>
            </div>
            <div v-if="displayFileInput">
                <form @submit.prevent="submitFormAddEval">
                <input type="file">
                <button class="cursor-pointer">check file</button>
                <br />
                <input type="text" placeholder="Team">
                <input type="text" placeholder="System collection">
                <button class="cursor-pointer" type="submit">Créer</button>
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