export const leadingZero = num => num < 10 ? `0${num}` : num;

export function cleanPhone(prettyPhoneNumber) {
    return prettyPhoneNumber.replace(/ |-|\(|\)|_/g, '');
}
