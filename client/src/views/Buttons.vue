<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <ball></ball>
        <hr>
      </div>
    </div>
  </div>
</template>
<script>
import ButtonsAll from '@/components/ButtonsAll.vue';

export default {
  name: 'ButtonsView',
  components: {
    ball: ButtonsAll,
  },
};
</script>
