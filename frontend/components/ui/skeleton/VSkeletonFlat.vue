<script setup lang="ts">
</script>

<template>
    <div :class="[$style.VSkeleton]">
        <div :class="$style.main">
            <div :class="$style.first">
                <div :class="[$style.square, $style._animating]" style="width: 15.6rem; height: 1.6rem;"></div>
                <div :class="[$style._animating]" style="width: 6.2rem; height: 2.4rem; border-radius: .4rem;"></div>
            </div>

            <div :class="$style.second">
                <div>
                    <div :class="[$style.square, $style._animating]" style="width: 18.9rem; height: 1.9rem;"></div>
                    <div :class="[$style.square, $style._animating]" style="width: 20.9rem; height: 2.4rem; margin-top: .2rem;"></div>
                </div>

                <div :class="[$style.circle, $style._animating]">
                    <VIcon
                        name="mock-heart"
                        :class="$style.heart"
                    />
                </div>
            </div>

            <div :class="[$style.third, $style.square, $style._animating]"></div>

            <div :class="$style.fourth">
                <div :class="[$style.square, $style._animating]" style="width: 100%; height: 1.8rem;"></div>
                <div :class="[$style.square, $style._animating]" style="width: 15.9rem; height: 1.9rem;"></div>
                <div :class="[$style.square, $style._animating]" style="width: 15.9rem; height: 1.8rem;"></div>
            </div>

            <div :class="$style.fifth">
                <div :class="[$style.circle, $style._animating]"></div>
                <div :class="[$style.circle, $style._animating]"></div>
                <div :class="[$style.circle, $style._animating]"></div>
                <div :class="[$style.circle, $style._animating]"></div>
                <div :class="[$style.circle, $style._animating]"></div>
            </div>
        </div>

        <div :class="[$style.footer, $style._animating]"></div>
    </div>
</template>

<style lang="scss" module>
    .VSkeleton {
        position: relative;
        overflow: hidden;
        width: 100%;
        border-radius: 1.2rem;
        background-color: $base-0;
    }

    ._animating {
        position: relative;
        overflow: hidden;
        background-color: $base-100;

        &:after {
            content: "";
            position: absolute;
            top: -25%;
            left: 0;
            z-index: 1;
            display: block;
            width: 100px;
            height: 200%;
            background: linear-gradient(110deg, rgb(255 255 255 / 70%), rgb(247 247 247 / 70%));
            transform: skewX(-10deg);
            animation: translate-left 1.5s infinite;

            @keyframes translate-left {
                0% {
                    left: -110%;
                    opacity: 0;
                }

                30% {
                    opacity: 1;
                }

                70% {
                    opacity: 1;
                }

                100% {
                    left: 110%;
                    opacity: 0;
                }
            }
        }
    }

    .main {
        padding: 2rem 2rem 1.6rem;
    }

    .first {
        display: flex;
        justify-content: space-between;
    }

    .second {
        display: flex;
        justify-content: space-between;
        margin-top: .8rem;
    }

    .third {
        width: 100%;
        height: 24.9rem;
        margin-top: 1.6rem;
    }

    .fourth {
        display: flex;
        flex-direction: column;
        gap: .8rem;
        margin-top: 3rem;
    }

    .fifth {
        display: flex;
        gap: .8rem;
        margin-top: 1.6rem;
        padding-top: 1.6rem;
        border-top: 1px solid $base-100;
    }

    .heart {
        position: absolute;
        top: 50%;
        left: 50%;
        color: $base-200;
        transform: translate(-50%, -50%);
    }

    .square {
        max-width: 100%;
        border-radius: .8rem;
    }

    .circle {
        width: 4rem;
        height: 4rem;
        border-radius: 50%;
    }

    .footer {
        width: 100%;
        height: 4.8rem;
        margin-top: auto;
        background-color: $base-200;
    }
</style>
