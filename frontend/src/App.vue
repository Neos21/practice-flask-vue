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
      <button type="button" v-on:click="onGetBalance">Load Balance</button>
    </p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
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
  
  /** エラーメッセージ */
  private errorMessage: string = '';
  
  /** 初期処理 : 要素がマウントされた時 */
  private async mounted() {
    await this.onGetBalance();
  }
  
  /** 資産を取得する */
  private async onGetBalance() {
    try {
      this.errorMessage = '';
      // 現在の資産を取得する
      const result: any = await axios.get('/api/balance');
      this.btc = `${result.data['btc']}`;
      this.eth = `${result.data['eth']}`;
      await this.onCalc();
    }
    catch(error) {
      console.error(error);
      this.errorMessage = `${error}`;
    }
  }
  
  /** レートを計算する */
  private async onCalc() {
    try {
      this.errorMessage = '';
      const result: any = await axios.post('/api/calculator', {
        btc: `${this.btc}`,
        eth: `${this.eth}`
      });
      this.btcJpy   = `${result.data['btc_jpy']}`;
      this.ethJpy   = `${result.data['eth_jpy']}`;
      this.totalJpy = `${result.data['total_jpy']}`;
    }
    catch(error) {
      console.error(error);
      this.errorMessage = `${error}`;
    }
  }
  
  // TODO : 入力した資産額を保存する仕組み
  // TODO : 通貨の種類を増やしても動的に対応する仕組み
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
</style>
