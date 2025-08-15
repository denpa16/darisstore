import {INPUTS} from '~/assets/js/constants/inputs.js';

export const FORM_STATUSES = {
    default: 'default',
    success: 'success',
    error: 'error',
};

export const FORM_TYPES = {
    consult: 'consultation',
    toWork: 'partnership',
};

export const FORM_STATUSES_CONTENT = {
    [FORM_STATUSES.error]: {
        title: 'Возникла техническая ошибка',
        description: 'Мы стараемся делать все, чтобы такого больше не&nbsp;повторилось',
        icon: 'terminal',
        disclaimer: 'Окно закроется автоматически через',
    },
    [FORM_STATUSES.success]: {
        title: 'Заявка отправлена',
        description: 'Спасибо за заявку,&nbsp;мы перезвоним вам&nbsp;в ближайшее время',
        icon: 'letter',
        disclaimer: 'Окно закроется автоматически через',
    },
};

export const FORM_TYPES_CONTENT = {
    [FORM_TYPES.toWork]: {
        title: 'Написать нам',
        description: 'Оставьте заявку и&nbsp;и мы&nbsp;перезвоним в ближайшее время',
        inputs: [INPUTS.name, INPUTS.phone, INPUTS.comment],
    },
    [FORM_TYPES.consult]: {
        title: 'Получить консультацию',
        description: 'Оставьте заявку и&nbsp;и мы перезвоним <br> вам',
        inputs: [INPUTS.name, INPUTS.phone],
    },
};
