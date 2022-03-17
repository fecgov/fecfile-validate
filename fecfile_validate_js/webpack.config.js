const path = require('path');
const terser = require('terser-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/index.ts',
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
        include: [
          path.resolve(__dirname, 'src')
        ],
        exclude: [
          path.resolve(__dirname, 'node_modules/'),
          // path.resolve(__dirname, 'test.ts')
        ],
      },
      {
        test: /\.js$/,
        enforce: 'pre',
        use: ["source-map-loader"]
      }
    ]
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins: [
    new CopyPlugin({
      patterns: [{
        from: '../schema/*.json',
        to: ({ context, absoluteFilename }) => {
            return 'schema/[name][ext]';
        }
      }],
      options: {
        concurrency: 100
      }
    })
  ],
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'dist')
  },
  optimization: {
    // minimize: true,
    minimizer: [
      new terser({
        parallel: true
      })
    ]
  }
};
