<script setup
        lang="ts"
>
// Types
import type { MediaSLideProps } from '~/components/sliders/types';


const {
    video = '',
    active = false,
    slideIndex,
    shadowsPosition,
    image = '',
    title = '',
    sizes = '',
    loadFirstImg,
} = defineProps<MediaSLideProps>();

const img = useImage();
const videoRef = ref<HTMLVideoElement | null>(null);

const previewImg = computed(() => {
    const options = {
        width: 400,
        quality: 20,
        blur: 30,
    };

    return img(image || '', options);
});

watch(() => active, async val => {
    await nextTick();
    if (!videoRef.value) {
        return;
    }

    val ? handlePlayVideo() : handlePauseVideo();
});

function handlePlayVideo() {
    videoRef.value?.play();
}

function handlePauseVideo() {
    const player = videoRef.value;
    player?.pause();

    // setTimeout(() => {
    //     if (player) {
    //         player.currentTime = 0;
    //     }
    // }, 300);
}

const emit = defineEmits<{
    (e: 'video-ended'): void
}>();

function onVideoEnded() {
    handlePauseVideo();
    emit('video-ended');
}
</script>

<template>
    <div
        :class="[$style.MediaSlide, {
            [$style._shadows]: shadowsPosition,
            [$style[`_shadows-${shadowsPosition}`]]: shadowsPosition,
        }]"
    >
        <video
            v-if="video"
            ref="videoRef"
            :class="[$style.image]"
            :src="video"
            :autoplay="true"
            :playsinline="true"
            :poster="previewImg"
            :muted="true"
            webkit-playsinline
            preload="none"
            @ended="onVideoEnded"
        />

        <VImage
            v-else-if="image"
            :class="[$style.image]"
            :sizes="sizes"
            :image="image"
            :alt="title"
            :no-lazy="loadFirstImg && slideIndex === 0"
        />
    </div>
</template>

<style lang="scss"
       module
>
    .MediaSlide {
        position: relative;
        display: block;
        width: 100%;
        height: 100%;
        transform: translateZ(0);

        &._shadows {
            &:after {
                content: "";
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                pointer-events: none;
            }
        }

        &._shadows-both {
            &:after {
                background: linear-gradient(180deg, rgb(21 22 24 / 0%) 74%, rgb(21 22 24 / 52%) 100%),
                    linear-gradient(180deg, rgb(21 22 24 / 64%) 0%, rgb(45 47 51 / 0%) 24%);
            }
        }

        &._shadows-bottom {
            &:after {
                background: linear-gradient(180deg, rgb(21 22 24 / 0%) 74%, rgb(21 22 24 / 52%) 100%);
            }
        }
    }

    div.image,
    video.image {
        display: block;
        width: 100%;
        height: 100%;
    }

    video.image {
        object-fit: cover;
    }
</style>
