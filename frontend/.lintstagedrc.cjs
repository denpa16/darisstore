// const declarationFiles = [];

module.exports = {
    '*.(ts|js|vue)': [
        'eslint --cache',
    ],
    '*.(scss|vue)': [
        'stylelint --allow-empty-input',
    ],
    // '*.{vue,ts}': (filenames) => {
    //     const files = [...filenames, ...declarationFiles];
    //     return `vue-tsc-files --noEmit -p ./tsconfig.json ${files.join(' ')}`;
    // },
};
