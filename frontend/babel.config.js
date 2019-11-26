const plugins = [];

// npm run build でビルドする際 console の使用箇所があるとエラーになるので除去する
if(process.env.NODE_ENV === 'production') {
  plugin.push('transform-remove-console');
}

module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  plugins: plugins
};
