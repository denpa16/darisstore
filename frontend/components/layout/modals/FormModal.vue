<template>
    <div :class="$style.FormModal">
        <transition name="fade-fast" mode="out-in">
            <form
                :key="`status_${formStatus}`"
                :class="$style.wrapper"
                @submit.prevent="handleSubmit"
            >
                <div :class="$style.top">
                    <div
                        v-if="content.title"
                        :class="$style.title"
                        v-html="content.title"
                    />
                    <VIconButton
                        :class="$style.close"
                        icon="close"
                        color="secondary"
                        size="medium"
                        type="button"
                        @click="onClose"
                    />
                </div>
                <div
                    v-if="content.description"
                    :class="$style.description"
                    v-html="content.description"
                />

                <div v-if="formStatus !== formStatuses.default" :class="$style.bodyStatus">
                    <VIcon
                        v-if="content?.icon"
                        :class="$style.icon"
                        :name="content.icon"
                        size="custom"
                    />
                </div>
                <div v-else :class="$style.body">
                    <div
                        v-for="input in inputs"
                        :key="`TheForm_input_${input.name}`"
                    >
                        <VInput
                            v-if="input.type === 'input'"
                            v-model="input.vModel"
                            :placeholder="input.placeholder"
                            :title="input.label"
                            :mask="input.mask"
                            :required="input.required"
                            :error="input.error"
                            :msg="input.errorMsg"
                            :max-length="input.maxLength"
                            @input="checkField(input.name)"
                        />
                        <VTextarea
                            v-else-if="input.type === 'textarea'"
                            v-model="input.vModel"
                            :placeholder="input.placeholder"
                            :title="input.label"
                            :error="input.error"
                            :msg="input.errorMsg"
                            :max-length="input.maxLength"
                            @input="checkField(input.name)"
                        />
                    </div>
                </div>

                <div :class="$style.bottom">
                    <div v-if="content?.disclaimer" :class="$style.disclaimer">
                        {{ content.disclaimer }} <span :class="$style.time">{{ time }} сек</span>
                    </div>
                    <div v-else>
                        <VButton
                            :class="$style.btn"
                            :loading="isLoading"
                            :disabled="isFormNotValid"
                            type="submit"
                            size="medium"
                        >
                            Отправить
                        </VButton>

                        <div :class="$style.disclaimer">
                            Нажимая кнопку, вы подтверждаете свое согласие <br>
                            на&nbsp;обработку&nbsp;
                            <a :class="$style.policy" :href="policyLink">персональных данных</a>
                        </div>
                    </div>
                </div>
            </form>
        </transition>
    </div>
</template>

<script>
import {
    FORM_STATUSES,
    FORM_STATUSES_CONTENT, FORM_TYPES,
    FORM_TYPES_CONTENT,
} from '~/assets/js/constants/forms.js';
import { POLICY_LINK } from '~/assets/js/constants/index.js';
import { strValidate } from '~/assets/js/utils/validate-utils.js';
import { cleanPhone } from '~/assets/js/utils/numbers-utils.js';

export default {
    name: 'FormModal',

    props: {
        type: {
            type: String,
            default: FORM_TYPES.consult,
        },
    },

    data() {
        return {
            policyLink: POLICY_LINK,
            formStatuses: FORM_STATUSES,
            formStatus: FORM_STATUSES.default,
            time: 5,
            timer: null,
            inputs: [],

            isLoading: false,
        };
    },

    computed: {
        content() {
            if (this.formStatus === this.formStatuses.default) {
                return FORM_TYPES_CONTENT[this.type];
            }
            return FORM_STATUSES_CONTENT[this.formStatus];
        },

        isFormNotValid() {
            return this.inputs.some(i => i.error || !i.vModel);
        },
    },

    mounted() {
        this.inputs = this.content?.inputs;
    },

    beforeDestroy() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    },

    methods: {
        onClose() {
            this.$emit('close');
        },

        checkField(name) {
            this.inputs.forEach(i => {
                if (i.name === name) {
                    this.validateField(i);
                }
            });
        },

        validateField(input) {
            input.errorMsg = '';
            input.error = false;

            input.errorMsg = strValidate(input.vModel, input.regex, true);
            input.error = Boolean(input.errorMsg);
        },

        async handleSubmit() {
            try {
                this.isLoading = true;

                const formData = new FormData();
                formData.set('type', this.type);

                this.inputs.forEach(i => {
                    if (i.name === 'phone') {
                        formData.set(i.name, cleanPhone(i.vModel));
                    } else {
                        formData.set(i.name, i.vModel);
                    }
                });

                await this.$axios.$post(this.$api.request, formData);

                this.formStatus = this.formStatuses.success;
            } catch (e) {
                console.warn('[FormModal/handleSubmit]: request has wrong: ', e);
                this.formStatus = this.formStatuses.error;
            } finally {
                this.isLoading = false;
                this.setTimer();
            }
        },

        setTimer() {
            if (this.timer) {
                clearInterval(this.timer);
            }

            this.timer = setInterval(() => {
                this.time--;

                if (!this.time) {
                    clearInterval(this.timer);
                    this.onClose();
                }
            }, 1000);
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .FormModal {
        position: relative;
        height: 100%;
    }

    .top {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .close {
        position: absolute;
        top: .8rem;
        right: .8rem;
        z-index: 5;

        @include respond-to(mobile) {
            position: relative;
            inset: 0;
        }
    }

    .wrapper {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        padding: 3.2rem;

        @include respond-to(mobile) {
            padding: .8rem 1.6rem 1.6rem;
        }
    }

    .title {
        @include text(s20);

        color: $base-700;

        @include respond-to(mobile) {
            @include text(s16);
        }
    }

    .description {
        @include text(r14);

        margin-top: 1.2rem;
        color: $base-500;

        @include respond-to(mobile) {
            margin-top: .8rem;
        }
    }

    .bodyStatus {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-grow: 1;
    }

    .body {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        flex-grow: 1;
        margin: 4rem 0;

        @include respond-to(mobile) {
            margin: 1.6rem 0;
        }
    }

    .bottom {
        width: 100%;
        text-align: center;
    }

    .icon {
        width: 16rem;
        margin: auto;
        aspect-ratio: 1;
        color: $base-200;
    }

    .disclaimer {
        @include text(m12);

        color: $base-500;
    }

    .time {
        color: $primary-500;
    }

    .btn {
        width: 100%;
        margin-bottom: 1.2rem;
    }

    .policy {
        border-bottom: 1px solid $base-500;
        transition: $default-transition;

        @include hover {
            border-color: $base-200;
            color: $base-200;
        }
    }
</style>
