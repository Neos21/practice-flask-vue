module.exports = {
  // 静的ファイルの格納先ディレクトリ名
  assetsDir: 'static',
  // 開発サーバの仕様
  devServer: {
    proxy: {
      // '/api/**' へのアクセスを Flask サーバにする https://qiita.com/Ryoma0413/items/c41d10d2e6e2a420c3cf
      '/api/': {
        target: 'http://localhost:5000'
      }
    }
  }
};
