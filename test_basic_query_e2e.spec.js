const { test, expect } = require('@playwright/test');

test('Basic Query Execution E2E Test', async ({ page }) => {
  const screenshotDir = 'C:/Users/amogh/Downloads/tac-6/tac-6/agents/7b6c3cfd/e2e_test_runner_0_0/img/basic_query';
  const applicationUrl = 'http://localhost:5173';

  // Step 1: Navigate to the application
  console.log('Step 1: Navigating to application...');
  await page.goto(applicationUrl);
  await page.waitForLoadState('networkidle');

  // Step 2: Take screenshot of initial state
  console.log('Step 2: Taking initial screenshot...');
  const screenshot1 = `${screenshotDir}/01_initial_state.png`;
  await page.screenshot({ path: screenshot1, fullPage: true });

  // Step 3: Verify page title
  console.log('Step 3: Verifying page title...');
  const title = await page.title();
  expect(title).toBe('Natural Language SQL Interface');
  console.log('✓ Page title verified');

  // Step 4: Verify core UI elements
  console.log('Step 4: Verifying core UI elements...');

  const queryInput = page.locator('#query-input');
  await expect(queryInput).toBeVisible();
  console.log('✓ Query input found');

  const queryButton = page.locator('#query-button');
  await expect(queryButton).toBeVisible();
  console.log('✓ Query button found');

  const uploadButton = page.locator('#upload-data-button');
  await expect(uploadButton).toBeVisible();
  console.log('✓ Upload Data button found');

  const tablesSection = page.locator('#tables-section');
  await expect(tablesSection).toBeVisible();
  console.log('✓ Available Tables section found');

  // Step 5: Enter the query
  console.log('Step 5: Entering query...');
  await queryInput.fill('Show me all users from the users table');
  await page.waitForTimeout(500);

  // Step 6: Take screenshot of query input
  console.log('Step 6: Taking query input screenshot...');
  const screenshot2 = `${screenshotDir}/02_query_input.png`;
  await page.screenshot({ path: screenshot2, fullPage: true });

  // Step 7: Click the Query button
  console.log('Step 7: Clicking Query button...');
  await queryButton.click();

  // Wait for results to appear
  await page.waitForSelector('#results-section', {
    state: 'visible',
    timeout: 10000
  });
  await page.waitForTimeout(1000); // Wait for all data to load

  // Step 8: Verify query results appear
  console.log('Step 8: Verifying query results appear...');
  const resultsSection = page.locator('#results-section');
  await expect(resultsSection).toBeVisible();
  console.log('✓ Query results appear');

  // Step 9: Verify SQL translation is displayed
  console.log('Step 9: Verifying SQL translation...');
  const sqlDisplay = page.locator('#sql-display');
  await expect(sqlDisplay).toBeVisible();

  // Wait for SQL content to load (look for the SELECT keyword)
  await page.waitForFunction(() => {
    const element = document.querySelector('#sql-display');
    return element && element.textContent.includes('SELECT');
  }, { timeout: 10000 });

  const sqlText = await sqlDisplay.textContent();
  expect(sqlText).toContain('SELECT');
  expect(sqlText).toContain('users');
  console.log('✓ SQL translation verified');

  // Step 10: Take screenshot of SQL translation
  console.log('Step 10: Taking SQL translation screenshot...');
  const screenshot3 = `${screenshotDir}/03_sql_translation.png`;
  await page.screenshot({ path: screenshot3, fullPage: true });

  // Step 11: Verify results table contains data
  console.log('Step 11: Verifying results table contains data...');
  const resultsContainer = page.locator('#results-container');
  await expect(resultsContainer).toBeVisible();

  const tableRows = page.locator('#results-container table tbody tr');
  const rowCount = await tableRows.count();
  expect(rowCount).toBeGreaterThan(0);
  console.log(`✓ Results table contains ${rowCount} rows`);

  // Step 12: Take screenshot of results
  console.log('Step 12: Taking results screenshot...');
  const screenshot4 = `${screenshotDir}/04_results.png`;
  await page.screenshot({ path: screenshot4, fullPage: true });

  // Step 13: Click Hide button
  console.log('Step 13: Clicking Hide button...');
  const hideButton = page.locator('#toggle-results');
  await expect(hideButton).toBeVisible();
  await hideButton.click();
  await page.waitForTimeout(500);

  // Verify results section is hidden
  await expect(resultsSection).toBeHidden();
  console.log('✓ Hide button works');

  console.log('\n✅ All test steps passed successfully!');
});
