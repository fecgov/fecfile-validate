const path = require('path');
const terser = require('terser-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

module.exports = {
  entry: './src/index.ts',
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
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
