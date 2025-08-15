import fs from 'fs';

export default function nuxtDelayHydrationExclude(config) {
    const excludePaths = config.excludePaths;
    const URLS_TO_SKIP = new RegExp(`^(${excludePaths.join('|')})(\\/|$)|(^|\\/+)(${excludePaths.join('|')})(\\/|$)`);

    this.nuxt.hook('build:templates', ({
        templatesFiles,
    }) => {
        const clientTemplate = templatesFiles.find(t => t.dst === 'client.js');

        if (clientTemplate) {
            const fileContent = fs.readFileSync(clientTemplate.src, { encoding: 'utf-8' });
            const replace = `
                const delayDisabled = window.location.pathname.match(${URLS_TO_SKIP})
                delayDisabled ?
                    false :
                    await delayHydration()
                console.warn('delay-hydration is:', delayDisabled ? 'disabled' : 'enabled')
            `;

            const regex = /(?<!const\s+hydrationEvent\s+=\s+)(await\s+delayHydration\(\))/g;
            const modifiedContent = fileContent.replace(regex, replace);
            fs.writeFileSync(clientTemplate.src, modifiedContent, 'utf-8');
        }
    });
}
