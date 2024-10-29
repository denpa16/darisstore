const upath = require('upath');
const path = require('path');
const dirname = upath.toUnix(path.resolve(__dirname));

module.exports = {
    'pre-push': `cd ${dirname} && npx playwright test`,
    'pre-commit': `cd ${dirname} && ./node_modules/.bin/lint-staged -cwd ${dirname} -c .lintstagedrc.cjs`,
    'commit-msg': `cd ${dirname} && npx --no -- commitlint --edit $1 --config commitlint.config.mjs`,
};
