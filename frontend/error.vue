<script setup lang="ts">
// #region Dara
const error = useError();
// #endregion

// #region Computed
const titleHtml = computed<string>(() => {
    const errorsTitleMap = {
        404: 'Страница не найдена',
        500: 'Возникла ошибка<br/>на стороне сервера',
        502: 'Cайт cкоро заработает',
        505: 'Возникла ошибка<br/>на стороне сервера',
    };

    return errorsTitleMap[error.value?.statusCode] || 'Возникла ошибка';
});

const descriptionHtml = computed<string>(() => {
    const errorsDescriptionMap = {
        404: 'Похоже, эта страница еще на стадии строительства или мы не успели ее завершить. Вы можете перейти на главную.',
        500: 'Попробуйте перезагрузить страницу.',
        502: 'На сайте ведутся технические работы. Закончим в ближайшее время.',
        505: 'Попробуйте перезагрузить страницу.',
    };

    return errorsDescriptionMap[error.value?.statusCode] || 'Попробуйте перезагрузить страницу.';
});
// #endregion

// #region Methods
function reload() {
    location.reload();
}

// #region
</script>

<template>
    <div
        :class="['page', $style.ErrorPage]"
    >
        <div :class="['container', $style.container]">
            <VIcon
                :class="$style.logo"
                size="custom"
                name="ida-logo"
            />

            <div :class="$style.text">
                <h4
                    :class="$style.title"
                    v-html="titleHtml"
                >
                </h4>
                <p :class="$style.description">
                    <span v-html="descriptionHtml">
                    </span>
                </p>
            </div>

            <div
                v-if="error && error.statusCode === 404"
                class="actions"
            >
                <VButton
                    tag="a"
                    to="/"
                    round
                    :class="$style.btn"
                >
                    На главную
                </VButton>
            </div>
            <div
                v-else
                class="actions"
            >
                <VButton
                    round
                    :class="$style.btn"
                    @click="reload"
                >
                    Перезагрузить страницу
                </VButton>
            </div>
        </div>
        <p
            v-if="error && error.statusCode"
            :class="$style.statusText"
        >
            {{ error.statusCode }}
        </p>
    </div>
</template>

<style lang="scss" module>
    .ErrorPage {
        position: relative;
        height: 100dvh;
    }

    .ErrorPage,
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .logo {
        height: 14rem;
    }

    .text {
        width: 100%;
        max-width: 64rem;
        margin: 4.8rem 0;
    }

    .title,
    .description {
        text-align: center;
    }

    .title {
        @include text(h2);

        margin-bottom: 3.2rem;

        @include respond-to(mobile) {
            font-size: 2.4rem;
        }
    }

    .description {
        @include text(p1);

        @include respond-to(mobile) {
            @include text(p2);
        }
    }

    .tel {
        font-weight: bold;
    }

    .btn {
        margin-right: .8rem;

        &:last-child {
            margin-right: 0;
        }
    }

    .statusText {
        @include text(title);

        position: absolute;
        top: 9.2rem;
        right: 6.4rem;
        color: $base-200;
        user-select: none;

        @include respond-to(tablet) {
            @include text(h1);

            top: 2rem;
            right: 2rem;
        }
    }
</style>
