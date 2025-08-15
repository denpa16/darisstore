const upath = require('upath');
const path = require('path');
const dirname = upath.toUnix(path.resolve(__dirname));

module.exports = {
    'pre-commit': `cd ${dirname} && ./node_modules/.bin/lint-staged -cwd ${dirname} -c .lintstagedrc`,
};
