import { expect, test } from '@playwright/test';

// Список url страниц для тестирования
const pages = [
    '/',
];

test.describe('Hydration', () => {
    pages.forEach(url => {
        test(`has no hydration errors on the ${url} page`, async ({ page }) => {
            page.on('console', async msg => {
                const text = msg.text();

                // Проверяем, что сообщение не содержит текст ошибки
                await expect(text)
                    .not
                    .toContain('The client-side rendered virtual DOM tree is not matching server-rendered content');

                await expect(text)
                    .not
                    .toContain('[Vue warn]: Hydration');

                await expect(text)
                    .not
                    .toContain('Hydration completed but contains mismatches');
            });

            // Избегаем загрузки ненужных ресурсов
            await page.route('**/*.{png,jpg,jpeg,webp,css,woff2,woff,svg,png@webp,jpg@webp}', route => route.abort());

            await page.goto(url);

            await page.mouse.move(10, 100);

            await page.waitForTimeout(1500);
        });
    });
});
