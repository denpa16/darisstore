<template>
    <div :class="$style.TheSpinner">
        <div :class="$style.ellipsis"><div></div><div></div><div></div><div></div></div>
    </div>
</template>

<script>
export default {
    name: 'TheSpinner',
};
</script>

<style
    lang="scss"
    module
>
    .TheSpinner {
        position: relative;
    }

    .ellipsis {
        position: absolute;
        top: 50%;
        left: 50%;
        display: inline-block;
        width: 8rem;
        height: 8rem;
        transform: translate(-50%, -50%);
    }

    .ellipsis div {
        position: absolute;
        top: 3.33rem;
        width: 1.33rem;
        height: 1.33rem;
        border-radius: 50%;
        background: $white;
        animation-timing-function: cubic-bezier(0, 1, 1, 0);
    }

    .ellipsis div:nth-child(1) {
        left: 8px;
        animation: ellipsis1 .6s infinite;
    }

    .ellipsis div:nth-child(2) {
        left: 8px;
        animation: ellipsis2 .6s infinite;
    }

    .ellipsis div:nth-child(3) {
        left: 32px;
        animation: ellipsis2 .6s infinite;
    }

    .ellipsis div:nth-child(4) {
        left: 56px;
        animation: ellipsis3 .6s infinite;
    }

    @keyframes ellipsis1 {
        0% {
            transform: scale(0);
        }

        100% {
            transform: scale(1);
        }
    }

    @keyframes ellipsis3 {
        0% {
            transform: scale(1);
        }

        100% {
            transform: scale(0);
        }
    }

    @keyframes ellipsis2 {
        0% {
            transform: translate(0, 0);
        }

        100% {
            transform: translate(24px, 0);
        }
    }
</style>
