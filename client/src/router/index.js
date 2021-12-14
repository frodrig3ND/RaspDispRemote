import Vue from 'vue';
import VueRouter from 'vue-router';
import Buttons from '../views/Buttons.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/soundboard',
    name: 'Remote Soundboard',
    component: Buttons,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
