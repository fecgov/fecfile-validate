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
    basePath: './',
    frameworks: ['webpack', 'jasmine'],
    plugins: [
      'karma-typescript',
      'karma-webpack',
      'karma-jasmine',
      'karma-chrome-launcher',
      // 'karma-coverage',
    ],
    files: [
      { pattern: './test.ts', type: 'module' }
    ],
    karmaTypescriptConfig: {
      compilerOptions: {
        module: 'node'
      },
      tsconfig: './tsconfig.json'
    },
    preprocessors: {
      './test.ts': ['webpack'],
    },
    webpack: webpackConfig,
    reporters: [
      'progress'
    ],
    color: true,
    browsers: ['ChromeHeadless']
  });
}
