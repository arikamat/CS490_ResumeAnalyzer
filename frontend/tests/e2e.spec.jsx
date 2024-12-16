import { test, expect } from '@playwright/test'; 
import fs from 'fs';
import path from 'path';

test('Signup, Login, and Upload Flow', async ({ page }) => {
  const testEmail = 'testuser8@example.com';
  const testUsername = 'testuser';
  const testPassword = 'password123';
  const testFilePath = './tests/resume.pdf';
  const testJobDescription = 'This is a test job description for validation purposes.';

  await page.goto('/register');
  await page.fill('input[placeholder="Email"]', testEmail);
  await page.fill('input[placeholder="Username"]', testUsername);
  await page.fill('input[placeholder="Password"]', testPassword);
  await page.fill('input[placeholder="Confirm Password"]', testPassword);
  await page.click('input[type="submit"]');
  await expect(page).toHaveURL('/login');
  await page.fill('input[placeholder="Email"]', testEmail);
  await page.fill('input[placeholder="Password"]', testPassword);
  await page.click('input[type="submit"]');
  await expect(page).toHaveURL('/upload');

  const fileInput = page.locator('#file-input');
  await fileInput.setInputFiles(testFilePath);
  const successMessage = page.locator('.success');
  await expect(successMessage).toHaveText('File is ready to upload');
  await page.click('button:has-text("Upload")');
  await expect(successMessage).toHaveText('File uploaded successfully!');

  const textArea = page.locator('textarea[placeholder="Enter job description here..."]');
  await textArea.fill(testJobDescription);
  const charInfo = page.locator('.char-info p:first-child');
  await expect(charInfo).toHaveText(`${testJobDescription.length} / 5000 characters`);
  await page.click('button:has-text("Upload Job Description")');
  const successMessage2 = page.locator('.success2');
  await expect(successMessage2).toHaveText('Job description uploaded successfully!');

  await page.goto('/dashboard');
  const downloadPromise = page.waitForEvent('download');
  await page.click('button:has-text("Generate PDF")');
  // const download = await downloadPromise;
  // const downloadPath = path.resolve(process.cwd(), 'resume');
  // await download.saveAs(downloadPath);
  // expect(fs.existsSync(downloadPath)).toBe(true);
  // const fileContent = fs.readFileSync(downloadPath);
  // expect(fileContent.slice(0, 4).toString()).toBe('%PDF');
});
