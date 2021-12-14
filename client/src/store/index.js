import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

/* eslint no-shadow: ["error", { "allow": ["state"] }] */

Vue.use(Vuex);

const state = {
  buttons: [],
  button: [],
  buttonTypes: [],
};

const getters = {
  buttonList: (state) => (state.buttons),
  curbutton: (state) => (state.button),
  buttonTypeList: (state) => (state.buttonTypes),
};

const actions = {
  async fetchButtons({ commit }) {
    const response = await axios.get('http://localhost:8000/actions');
    commit('setButtons', response.data);
  },
  async fetchButtonTypes({ commit }) {
    const response = await axios.get('http://localhost:8000/action_types');
    commit('setButtonTypes', response.data);
  },
  async addButton({ commit }, button) {
    const response = await axios.post('http://localhost:8000/actions', button);
    commit('addNewButton', response.data);
  },
  async fetchButton({ commit }, id) {
    const response = await axios.get(`http://localhost:8000/actions/${id}`);
    commit('setButton', response.data);
  },
  async editButton({ commit }, payload) {
    const response = await axios.put(`http://localhost:8000/actions/${payload.id}`, payload.data);
    commit('modButton', response.data);
  },
  async deleteButton({ commit }, id) {
    await axios.delete(`http://localhost:8000/actions/${id}`);
    commit('removeButton', id);
  },
};

const mutations = {
  setButtons: (state, buttons) => {
    state.buttons = buttons;
  },
  setButton: (state, button) => {
    state.button = button;
  },
  setButtonTypes: (state, buttonTypes) => {
    state.buttonTypes = buttonTypes;
  },
  addNewButton: (state, button) => { state.buttons.unshift(button); },
  modButton(state, button) {
    const index = state.buttons.findIndex((item) => item.id === button.id);
    state.buttons[index].name = button.name;
    state.buttons[index].num = button.num;
    state.buttons[index].order = button.order;
  },
  removeButton(state, id) {
    const ibutton = state.buttons.filter((button) => button.id !== id);
    state.buttons.splice(ibutton, 1);
  },
};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
