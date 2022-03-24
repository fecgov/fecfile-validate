import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';

export default [
  {
    input: 'src/index.js',
    output: {
      file: 'dist/index.js',
      format: 'cjs'
    },
    plugins: [
      nodeResolve(),
      commonjs(),
      json()
    ]
  },
  {
    input: 'src/index.js',
    output: [
      {
        file: 'dist/index-cjs.js',
        format: 'cjs'
      },
      {
        file: 'dist/index-es.js',
        format: 'es'
      }
    ],
    plugins: [
      nodeResolve(),
      commonjs(),
      json()
    ]
  }
];
