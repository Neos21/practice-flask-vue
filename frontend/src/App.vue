<template>
  <div id="app">
    <p><button type="button" v-on:click="onFetch">Fetch</button></p>
    <pre>Result : {{ result }}</pre>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import axios from 'axios';

@Component({})
export default class App extends Vue {
  /** Fetch したデータ */
  private result: string = '';
  
  /** Fetch ボタン押下時 */
  async onFetch() {
    const result = await axios.get('/api/spam');
    this.result = JSON.stringify(result.data);
  }
}
</script>

<style lang="scss">
#app {
  font-family: Helvetica, sans-serif;
}
</style>
