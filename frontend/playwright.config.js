import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests', 
  use: {
    baseURL: 'http://localhost:5173', 
    browserName: 'chromium',        
    headless: true,                  
    screenshot: 'only-on-failure',  
    trace: 'on-first-retry',        
  },
});
