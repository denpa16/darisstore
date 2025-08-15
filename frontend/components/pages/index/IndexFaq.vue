<template>
    <section :class="[$style.IndexFaq, 'container']">
        <div :class="$style.leftSide">
            <h2 :class="$style.title">Отвечаем, <br> на ваши вопросы</h2>

            <div :class="$style.bottom">
                <p :class="$style.disclaimer">Если вы ненашли ответа на свой вопрос, оставьте заявку и&nbsp;мы&nbsp;расскажем вам все, что вы хотите знать</p>

                <VButton :class="$style.btn" @click="handleRequest">Написать нам</VButton>
            </div>
        </div>

        <div>
            <VAccordion>
                <VAccordionItem
                    v-for="(faq, ind) in faqs"
                    :key="`faq_${ind}`"
                    :default-opened="!ind"
                >
                    <template #header-content>
                        {{ faq.question }}
                    </template>

                    <div v-html="faq.answer"/>
                </VAccordionItem>
            </VAccordion>
        </div>

        <div :class="$style.consultForm" @click="handleRequest">
            <div :class="$style.formTitle" v-html="consultForm.title"/>
            <div :class="$style.formDescription" v-html="consultForm.description"/>

            <VIconButton
                :class="$style.formBtn"
                icon="arrow-right"
                size="small"
                color="secondary"
            />

            <VImage :class="$style.formBg" image="/images/form-faq.png"/>
        </div>
    </section>
</template>

<script>

export default {
    name: 'IndexFaq',

    props: {
        faqs: {
            type: Array,
            default: () => [],
        },
    },

    data() {
        return {
            consultForm: {
                title: 'Не нашли ответ на свой вопрос?',
                description: 'Оставьте заявку и&nbsp;мы&nbsp;расскажем <br> вам все, что вы хотите знать',
            },
        };
    },

    methods: {
        handleRequest() {
            this.$modal.open(() => import('@/components/layout/modals/FormModal.vue'), {
                position: 'right',
            });
        },
    },
};
</script>

<style
    lang="scss"
    module
>
    .IndexFaq {
        display: grid;
        grid-template-columns: 1fr 1.4fr;
        gap: 4rem;
        padding-top: 6.4rem;
        padding-bottom: 6.4rem;

        @include respond-to(tablet) {
            grid-template-columns: 1fr;
            gap: 3.2rem;
            padding-top: 3.2rem;
            padding-bottom: 3.2rem;
        }
    }

    .leftSide {
        position: sticky;
        top: calc($header-h + 3.2rem);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 60rem;

        @include respond-to(tablet) {
            position: relative;
            top: auto;
            height: auto;
        }
    }

    .title {
        @include text(h3);

        text-transform: uppercase;
        color: $base-300;

        &:first-line {
            color: $base-900;
        }

        @include respond-to(mobile) {
            @include text(h4);
        }
    }

    .bottom {
        @include respond-to(tablet) {
            display: none;
        }
    }

    .disclaimer {
        @include text(r14);

        margin-bottom: 2rem;
        color: $base-700;
    }

    .btn {
        width: 100%;
    }

    .consultForm {
        display: none;

        @include respond-to(tablet) {
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            margin: 0 -1.6rem;
            padding: 1.6rem;
            border-radius: 1.2rem;
            background: $primary-500;
        }
    }

    .formTitle {
        @include text(s16);

        color: $white;
    }

    .formDescription {
        @include text(m14);

        margin: .8rem 0 3.2rem;
        color: $primary-150;
    }

    .formBtn {
        //
    }

    .formBg {
        position: absolute;
        right: 0;
        bottom: 0;
    }
</style>
