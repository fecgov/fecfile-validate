/**
 *
 */
process.env.CHROME_BIN = require('puppeteer').executablePath();
const webpack = require('webpack');
const webpackConfig = require('./webpack.config.js');
delete webpackConfig.entry;
delete webpackConfig.output;

module.exports = function(config) {
  // const browserify = {
  //   debug: true,
  // };
  
  config.set({
    logLevel: 'debug',
    basePath: '',
    frameworks: ['webpack', 'jasmine'],
    // exclude: [],
    plugins: [
      'karma-typescript',
      'karma-webpack',
      'karma-jasmine',
      'karma-chrome-launcher',
      // 'karma-coverage',
    ],
    // client: {
    //   jasmine: {
    //     //
    //   }
    // },
    files: [
      { pattern: './tests/**/*.js', type: 'module' },
      { pattern: './tests/**/*.ts', type: 'module' }
    ],
    // karmaTypescriptConfig: {
    //   compilerOptions: {
    //     module: 'node'
    //   },
    //   tsconfig: './tsconfig.json'
    // },
    preprocessors: {
      // './dist/index.js': ['webpack'],
      // './tests/**/*.ts': 'karma-typescript',
      // 'tests/**/*.js': ['webpack'],
      './tests/**/*.js': ['webpack'],
      // 'tests/**/*.ts': ['webpack'],
    },
    webpack: webpackConfig,
    // reporters: [
    //   'progress',
    //   'coverage'
    // ],
    browsers: ['ChromeHeadless'],
    // browserify: browserify,
  });
}
