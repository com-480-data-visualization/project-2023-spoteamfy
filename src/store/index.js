import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    index: 0,   //index of selected emotion  
    clicked_emotion: null,    //boolean if emotion is clicked
    new_emotion: 0,     //boolean is first time emotion is clicked
    genre: null,      //Genre selected
  },
  mutations: {
    setIndex(state, newIndex) {   // Add new mutation to update index
      state.index = newIndex;
    },
    setClickedEmotion(state, newEmotion) { // Add new mutation to update clicked_emotion
      state.clicked_emotion = newEmotion;
    },
    setNewEmotion(state, newEmotion) { // Add new mutation to update new_emotion
      state.new_emotion = newEmotion;
    },
    setGenre(state, newGenre) { // Add new mutation to update genre
      state.genre = newGenre;
    },
  },
  
});
