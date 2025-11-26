module.exports = {
  testDir: '.',
  testMatch: 'test_basic_query_e2e_runner_1.spec.js',
  timeout: 60000,
  use: {
    headless: false,
    viewport: { width: 1280, height: 720 },
    screenshot: 'on',
    video: 'off',
  },
};
