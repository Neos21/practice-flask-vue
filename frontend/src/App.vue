<template>
  <div id="app">
    <table>
      <thead>
        <tr>
          <th>Currency</th>
          <th>Balance</th>
          <th>JPY Rate</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>BTC</th>
          <td class="balance"><input type="text" v-model="btc" placeholder="BTC"></td>
          <td class="price">{{ btcJpy }} JPY</td>
        </tr>
        <tr>
          <th>ETH</th>
          <td class="balance"><input type="text" v-model="eth" placeholder="ETH"></td>
          <td class="price">{{ ethJpy }} JPY</td>
        </tr>
        <tr>
          <th colspan="2">Total</th>
          <td class="price">{{ totalJpy }} JPY</td>
        </tr>
      </tbody>
    </table>
    <p>
      <button type="button" v-on:click="onCalc">Calc</button>
      <button type="button" v-on:click="onLoadBalance">Load Balance</button>
      <button type="button" v-on:click="onSaveBalance">Save Balance</button>
    </p>
    <p v-if="infoMessage"  class="info-message">{{ infoMessage }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import axios from 'axios';

@Component({})
export default class App extends Vue {
  /** BTC */
  private btc: string = '0';
  /** BTC の日本円レート */
  private btcJpy: string = '0';
  /** ETH */
  private eth: string = '0';
  /** ETH の日本円レート */
  private ethJpy: string = '0';
  /** 合計 */
  private totalJpy: string = '0';
  
  /** 情報メッセージ */
  private infoMessage: string = '';
  /** エラーメッセージ */
  private errorMessage: string = '';
  
  /** 初期処理 : 要素がマウントされた時 */
  private async mounted() {
    this.onLoadBalance();
    this.onCalc();
  }
  
  /** 資産を取得する */
  private onLoadBalance() {
    this.infoMessage = '';
    this.errorMessage = '';
    let isLoaded = false;
    
    const btc = localStorage.getItem('btc');
    if(btc) {
      this.btc = btc;
      isLoaded = true;
    }
    else {
      localStorage.setItem('btc', '0');
    }
    
    const eth = localStorage.getItem('eth');
    if(eth) {
      this.eth = eth;
      isLoaded = true;
    }
    else {
      localStorage.setItem('eth', '0');
    }
    
    if(isLoaded) {
      this.infoMessage = 'Loaded.';
    }
    else {
      this.errorMessage = 'Load failed : LocalStorage is unavailable.'
    }
  }
  
  /** 資産を保存する */
  private async onSaveBalance() {
    this.infoMessage = '';
    this.errorMessage = '';
    let isSaved = false;
    
    if(!this.btc) {
      this.btc = '0';
    }
    if(!this.eth) {
      this.eth = '0';
    }
    
    if(this.btc) {
      localStorage.setItem('btc', this.btc);
      isSaved = true;
    }
    
    if(this.eth) {
      localStorage.setItem('eth', this.eth);
      isSaved = true;
    }
    
    if(isSaved) {
      this.infoMessage = 'Saved.';
    }
    else {
      this.errorMessage = 'Save failed : LocalStorage is unavailable.';
    }
  }
  
  /** レートを計算する */
  private async onCalc() {
    this.infoMessage = 'Calculating...';
    this.errorMessage = '';
    
    try {
      const result: any = await axios.post('/api/calculator', {
        btc: `${this.btc}`,
        eth: `${this.eth}`
      });
      this.btcJpy   = `${result.data['btc_jpy']}`;
      this.ethJpy   = `${result.data['eth_jpy']}`;
      this.totalJpy = `${result.data['total_jpy']}`;
      this.infoMessage = 'Completed.';
    }
    catch(error) {
      this.infoMessage = '';
      console.error(error);
      this.errorMessage = `${error}`;
    }
  }
}
</script>

<style lang="scss">
html {
  font-family: Helvetica, sans-serif;
}

table {
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: .25rem .5rem;
}

.balance input,
.price {
  text-align: right;
}

.info-message {
  color: #08f;
}

.error-message {
  color: #f00;
}
</style>
