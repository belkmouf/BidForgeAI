export default {
  projects: [
    {
      displayName: 'server',
      preset: 'ts-jest/presets/default-esm',
      testEnvironment: 'node',
      roots: ['<rootDir>/server'],
      testMatch: ['**/__tests__/**/*.test.ts', '**/*.test.ts'],
      testPathIgnorePatterns: ['/node_modules/', '/__tests__/utils/'],
      extensionsToTreatAsEsm: ['.ts'],
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '^@shared/(.*)$': '<rootDir>/shared/$1',
      },
      setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
      transform: {
        '^.+\\.tsx?$': ['ts-jest', {
          tsconfig: 'tsconfig.test.json',
          useESM: true,
          diagnostics: false,
        }],
      },
      transformIgnorePatterns: [
        'node_modules/(?!(@neondatabase)/)',
      ],
      collectCoverageFrom: [
        'server/**/*.ts',
        '!server/**/*.d.ts',
        '!server/index.ts',
        '!**/node_modules/**',
      ],
    },
    {
      displayName: 'client',
      preset: 'ts-jest/presets/default-esm',
      testEnvironment: 'jsdom',
      roots: ['<rootDir>/client/src'],
      testMatch: ['**/__tests__/**/*.tsx', '**/*.test.tsx'],
      extensionsToTreatAsEsm: ['.ts', '.tsx'],
      moduleNameMapper: {
        '^(\\.{1,2}/.*)\\.js$': '$1',
        '^@/(.*)$': '<rootDir>/client/src/$1',
        '^@shared/(.*)$': '<rootDir>/shared/$1',
      },
      setupFilesAfterEnv: [
        '<rootDir>/jest.setup.js',
        '@testing-library/jest-dom',
      ],
      transform: {
        '^.+\\.tsx?$': ['ts-jest', {
          tsconfig: 'tsconfig.json',
          useESM: true,
        }],
      },
      collectCoverageFrom: [
        'client/src/**/*.{ts,tsx}',
        '!client/src/**/*.d.ts',
        '!**/node_modules/**',
      ],
    },
  ],
  coverageThreshold: {
    global: {
      branches: 60,
      functions: 60,
      lines: 60,
      statements: 60,
    },
  },
  collectCoverage: false,
  coverageDirectory: 'coverage',
};
