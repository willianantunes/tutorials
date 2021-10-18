const {defaults} = require('jest-config')

module.exports = {
    ...defaults,
    moduleFileExtensions: ['js'],
    testPathIgnorePatterns: ['<rootDir>/scripts/', '<rootDir>/node_modules/'],
    collectCoverage: true,
    coveragePathIgnorePatterns: ['/scripts/', '/node_modules/'],
    coverageReporters: ['json', 'lcov', 'text', 'text-summary'],
    collectCoverageFrom: ['rave_of_phonetics/apps/core/static/core/js/**/*.{js,jsx,ts,tsx}']
}
