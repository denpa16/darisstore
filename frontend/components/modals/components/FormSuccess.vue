<script setup lang="ts">

import type { FormSuccessProps } from '@/components/modals/types.ts';
import LogoIda from '@/components/common/LogoIda.vue';

const {
    title,
    description,
    error,
} = defineProps<FormSuccessProps>();
</script>

<template>
    <div :class="[$style.FormSuccess, {[$style._error]: error}]">
        <LogoIda
            :class="$style.logo"
            size="custom"
            name="logo-primary"
        />

        <div
            v-if="title"
            :class="$style.title"
            v-html="!error ? title : 'Техническая ошибка'"
        >
        </div>

        <div
            :class="$style.description"
            v-html="!error ? description : 'К сожалению, ваше обращение не может быть отправлено по техническим причинам.<br/>Попробуйте отправить обращение еще раз или напишите нам в чат.'"
        >
        </div>

        <slot />
    </div>
</template>

<style module lang="scss">
    .FormSuccess {
        display: flex;
        align-items: center;
        flex-direction: column;
        min-height: 53.4rem;

        @include respond-to(tablet) {
            min-height: calc(100dvh - 8.2rem);
        }

        @include respond-to(mobile) {
            min-height: calc(100dvh - 4.2rem);
        }

        &._error {
            .date {
                color: $primary-600;
            }
        }
    }

    .logo {
        height: 14rem;
        margin-top: 10%;

        @include respond-to(tablet) {
            height: 10rem;
        }

        @include respond-to(mobile) {
            margin-top: 6.4rem;
        }
    }

    .title {
        @include text(h3);

        margin-top: 4.8rem;
        text-align: center;

        @include respond-to(tablet) {
            @include text(h4);

            max-width: 33.4rem;
            margin-top: 4rem;
        }
    }

    .description {
        @include text(p2);

        margin-top: 2rem;
        text-align: center;

        @include respond-to(tablet) {
            @include text(p3);

            max-width: 33.4rem;
            margin-top: 1.6rem;
        }
    }
</style>
