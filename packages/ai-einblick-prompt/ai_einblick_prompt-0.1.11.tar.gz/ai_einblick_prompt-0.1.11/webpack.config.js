const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  plugins: [
    new CopyWebpackPlugin({
      patterns: [{ from: './static/**' }]
    })
  ],
  resolve: {
    fallback: {
      fs: false
    }
  },
  module: {
    rules: [
      {
        test: /.+\.wasm$/,
        type: 'asset/source'
      },
      {
        test: /\.svg$/,
        type: 'asset/source'
      }
    ]
  }
};
