<script setup lang="ts">
// #region Imports

// Types
import { useFormCheck } from '@idaproject/form/composables/useFormCheck.ts';
import { useRegCheck } from '@idaproject/form/composables/useRegCheck.ts';

import { useSmartCaptcha } from '@idaproject/form/composables/useSmartCaptcha.ts';
import { useModalAnchorURLModify } from '@idaproject/form/composables/useModalAnchorOpen';
import type { ContactFormFields, ContactFormProps } from '~/components/modals/types';

// Components
import BaseModal from '~/components/modals/BaseModal.vue';
import FormSuccess from '@/components/modals/components/FormSuccess.vue';

// #endregion

// #region Props
const {
    title = 'Обращение в ИДАПРОДЖЕКТ',
} = defineProps<ContactFormProps>();
// #endregion

// #region Data
const fields = ref<ContactFormFields>({ name: '', phone: '', email: '', project: '', subject: '', message: '', personal: true, file: null });
const errors = ref<Record<string, string>>({});
const isLoading = ref<boolean>(false);

const specs = {
    project: [
        { value: '1', label: 'ЖК 1' },
        { value: '2', label: 'ЖК 2' },
    ],
    feedback_type: [
        { value: '1', label: 'Предложение' },
        { value: '2', label: 'Вопрос' },
    ],
};

const REQUIRED_FIELDS = ['name', 'email', 'phone', 'message'];

const { regCheck } = useRegCheck();
const { checkEmptyFields, getErrors, hasError, formStatus } = useFormCheck(errors, fields, REQUIRED_FIELDS);

// Добавляет якорь (#feedback) к url при показе модалки, и удаляет его при скрытии
useModalAnchorURLModify('contact-form');
const config = useRuntimeConfig();
const { checkCaptcha, restartCaptcha } = useSmartCaptcha(config.public.CAPTCHA, config.public.CAPTCHA_TEST, config.public.IS_DEV);

const { $fetchData } = useNuxtApp();

// #endregion


// #region Methods
async function submitForm() {
    checkEmptyFields();

    if (isLoading.value || hasError.value) {
        return;
    }

    try {
        isLoading.value = true;

        const data = new FormData();
        data.append('request_type', 'feedback');
        data.append('name', fields.value.name);
        data.append('phone', fields.value.phone);
        data.append('email', fields.value.email);
        if (fields.value.subject) {
            data.append('feedback_category', fields.value.subject);
        }
        data.append('comment', fields.value.message);
        if (fields.value.project) {
            data.append('project', fields.value.project);
        }

        if (fields.value.file?.length) {
            data.append('feedback_file', fields.value.file[0]);
        }

        // Проверка капчи
        const token = await checkCaptcha();

        if (token) {
            data.append('token', token as string);
        }

        await $fetchData.formsMock.sendContactForm(data, {
            // @ts-expect-error содержание ответа ошибки неизвестно
            onResponseError({ response }) {
                if (response._data) {
                    errors.value = getErrors(response._data);
                }
            },
        });

        nextTick(() => {
            formStatus.value = 'success';
        });
    // @ts-expect-error any/unknown плодит ошибки
    } catch (err: object) {
        console.warn('[ContactModal/submit] POST request failed: ', err);

        nextTick(() => {
            if (!hasError) {
                formStatus.value = 'error';
            }
        });
    } finally {
        isLoading.value = false;
        restartCaptcha();
    }
}
// #endregion
</script>

<template>
    <BaseModal>
        <div :class="$style.ContactModal">
            <div
                v-show="!formStatus"
                :class="$style.title"
                v-html="title"
            >
            </div>

            <form
                v-show="!formStatus"
                :class="$style.content"
                @submit.prevent=""
            >

                <div
                    :class="$style.rows"
                    data-scroll-lock-scrollable
                >
                    <div :class="$style.row">
                        <VInput
                            v-model="fields.name"
                            :class="[$style.item, $style._half]"
                            name="name"
                            label="Имя"
                            placeholder="Введите имя"
                            :msg="errors.name"
                            :error="Boolean(errors.name)"
                            :required="REQUIRED_FIELDS.includes('name')"
                            @input="errors.name = ''"
                            @update:model-value="errors.name = regCheck(fields.name, 'multyLang', true)"
                        />

                        <VInput
                            v-model="fields.phone"
                            :class="[$style.item, $style._half]"
                            name="phone"
                            mask="phone"
                            label="Номер телефона"
                            placeholder="+7 (XXX) XXX-XX-XX"
                            :msg="errors.phone"
                            :error="Boolean(errors.phone)"
                            :required="REQUIRED_FIELDS.includes('phone')"
                            @input="errors.phone = ''"
                            @update:model-value="errors.phone = regCheck(fields.phone, 'phone', true)"
                        />
                    </div>
                    <div :class="$style.row">
                        <VInput
                            v-model="fields.email"
                            :class="[$style.item, $style._half]"
                            name="email"
                            label="E-mail"
                            placeholder="Введите e-mail"
                            :msg="errors.email"
                            :error="Boolean(errors.email)"
                            :required="REQUIRED_FIELDS.includes('email')"
                            @input="errors.email = ''"
                            @update:model-value="errors.email = regCheck(fields.email, 'email', true)"
                        />

                        <VSelect
                            v-model="fields.project"
                            :class="[$style.item, $style._half]"
                            :msg="errors.project"
                            :error="Boolean(errors.project)"
                            placeholder="Выберите проект"
                            label="Проект"
                            reset-label=""
                            value-name="value"
                            label-name="label"
                            :specs="specs.project"
                            mobile-modal
                            name="project"
                            @update:model-value="errors.project = ''"
                        />
                    </div>

                    <div :class="$style.row">
                        <VSelect
                            v-model="fields.subject"
                            :class="[$style.item, $style._full]"
                            :msg="errors.subject"
                            :error="Boolean(errors.subject)"
                            label="Тема обращения"
                            reset-label=""
                            placeholder="Выберите тему"
                            value-name="value"
                            label-name="label"
                            :specs="specs.feedback_type"
                            mobile-modal
                            name="subject"
                            @update:model-value="errors.subject = ''"
                        />
                    </div>

                    <div :class="$style.row">
                        <VTextArea
                            v-model="fields.message"
                            :class="[$style.item, $style._full]"
                            name="message"
                            label="Сообщение"
                            placeholder="Введите сообщение"
                            :msg="errors.message"
                            :error="Boolean(errors.message)"
                            :required="REQUIRED_FIELDS.includes('message')"
                            @input="errors.message = ''"
                            @update:model-value="errors.message = regCheck(fields.message, 'multyLang', true)"
                        />
                    </div>

                    <div :class="$style.row">
                        <VFile
                            :class="[$style.item, $style._full, $style._file]"
                            label="Загрузите файл или перетащите в поле"
                            mobile-label="Загрузите файл"
                            name="file"
                            @change="fields.file = $event"
                        />
                    </div>
                </div>

                <VButton
                    :class="$style.button"
                    round
                    name="submit"
                    :disabled="!fields.personal"
                    @click="submitForm"
                >
                    Отправить
                </VButton>

                <div :class="$style.personal">
                    Нажимая на кнопку, вы даете согласие<br>
                    на обработку своих
                    <a
                        href="https://level.ru/privacy-policy/"
                        target="_blank"
                    >персональных данных</a>
                </div>
            </form>
            <transition name="fade-fast">
                <FormSuccess
                    v-if="formStatus"
                    title="Успешно отправлено"
                    description="Ваше обращение зарегистрировано.<br>Мы свяжемся с вами по указанным контактам."
                    :error="formStatus === 'error'"
                />
            </transition>
        </div>
    </BaseModal>
</template>

<style module lang="scss">
    .ContactModal {
        .personal {
            @include text(l4);

            margin-top: 2.4rem;
            line-height: 1.3;

            @include respond-to(tablet) {
                margin-top: 1.6rem;
            }

            @include respond-to(mobile) {
                margin-bottom: 2rem;
            }

            a {
                text-decoration: underline;
                color: $base-600;
            }
        }

        @include respond-to(mobile) {
            height: calc(100dvh - 42px);
        }
    }

    .title {
        @include text(h3);

        @include respond-to(tablet) {
            @include text(l2-regular);

            width: calc(100% + 4rem);
            margin-left: -2rem;
            padding: 0 6.4rem 2.2rem 2rem;
            border-bottom: 1px solid $base-200;
        }
    }

    .content {
        margin-top: 4rem;

        @include respond-to(tablet) {
            margin-top: 2rem;
        }
    }

    .rows {
        @include respond-to(tablet) {
            overflow: auto;
            margin: 0 -2rem;
            padding: 0 2rem;
        }

        @include respond-to(mobile) {
            max-height: calc(100dvh - 24rem);
        }
    }

    .row {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-top: 2.4rem;

        @include respond-to(tablet) {
            flex-direction: column;
            margin-top: 0;
        }

        &:first-child {
            margin-top: 0;

            .item {
                &:first-child {
                    @include respond-to(tablet) {
                        margin-top: 0;
                    }
                }
            }
        }
    }

    .item {
        @include respond-to(tablet) {
            margin-top: 2rem;
        }

        &._half {
            width: calc(50% - .6rem);

            @include respond-to(tablet) {
                width: 100%;
            }
        }

        &._full {
            width: 100%;
        }

        &._file {
            overflow: hidden;
        }
    }

    .button {
        width: 100%;
        margin-top: 4rem;

        @include respond-to(tablet) {
            margin-top: 2rem;
        }

        @include respond-to(mobile) {
            margin-top: 4rem;
        }
    }
</style>
