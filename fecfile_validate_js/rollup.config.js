import { nodeResolve } from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import json from '@rollup/plugin-json';
import { terser } from 'rollup-plugin-terser';

const isProduction = process.env.BUILD === 'production';

export default [
  {
    input: 'src/index.js',
    output: [
      {
        file: 'dist/index.js',
        format: 'cjs',
        sourcemap: true
      },
      {
        file: 'dist/index-es.js',
        format: 'es',
        sourcemap: true
      }
    ],
    plugins: [
      nodeResolve(),
      commonjs(),
      json(),
      isProduction && terser()
    ]
  }
];
