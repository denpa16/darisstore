<script setup
        lang="ts"
>
/**
 * Позволяет пользователю добавлять файлы для отправки
 *
 * @version 1.0.0
 * @displayName VFile
 */

// #region Imports
import useInputFile from '@idaproject/core/composables/ui/useInputFile';
import type { FileProps } from './types';
import { SizeEnum, ThemeEnum } from '@/types/ui/type.ts'; // #endregion
// #endregion

// #region Props
/**
 * This function adds one to its input.
 * @param {number} input any number
 * @returns {number} that number, plus one.
 */
const {
    size = SizeEnum.medium,
    theme = ThemeEnum.light,
    label = 'Файлы',
    placeholder = 'Файл в формате PDF, PNG, JPEG до 5 Мб',
    mobilePlaceholder = 'Выберите файл',
    maxFilesCount = 1,
    maxFileSize = 5242880,
    maxSizeErrorText = 'Размер прикреплённого файла не должен превышать',
    fileTypes = ['image/png', 'image/jpeg', 'image/bmp', 'application/pdf'],
    fileTypeError = 'Принимаются только форматы изображений (png, jpeg, bmp, pdf)',
    serverError = '',
    disabled = false,
    name = '',
    required = false,
    loading = false,
} = defineProps<FileProps>();
// #endregion

// #region Emits
const emit = defineEmits<{
    change: [value: File[]],
}>();
// #endregion

// #region Data
const $style = useCssModule();
const uid = useId();

const {
    fileExt,
    fileName,
    currentFiles,
    acceptedTypes,
    error,
    handleFileChange,
    handleLoadClick,
    fakeClick,
} =
    useInputFile(emit, placeholder, mobilePlaceholder, placeholder, toRef(() => serverError), fileTypes, maxFilesCount, maxFileSize, maxSizeErrorText, fileTypeError);
// #endregion

// #region Computed
const classList = computed(() => [
    {
        [$style[`_${theme}`]]: theme,
        [$style[`_${size}`]]: size,
        [$style._active]: currentFiles.value.length,
        [$style._disabled]: disabled,
        [$style._error]: error.value || serverError,
    },
]);

const labelString = computed((): string => required ? label + '<span>*</span>' : label);

const filaNameFull = computed((): string => fileName.value + ' ' + fileExt.value);

const btnText = computed((): string => {
    if (maxFilesCount === 1) {
        return !currentFiles.value?.length ? 'выберите файл' : 'Удалить';
    }

    return 'выберите файлы';
});

const btnMobileText = computed((): string => {
    if (maxFilesCount === 1) {
        return !currentFiles.value?.length ? 'Выбрать' : 'Удалить';
    }

    return 'Выбрать';
});

const errorText = computed((): string => serverError || error);

const loadStatus = computed((): string => loading ? 'Файл загружается' : 'Файл загружен');
// #endregion

// #region Computed
function handleClick(): void {
    if (maxFilesCount === 1) {
        handleLoadClick();
        return;
    }
    fakeClick();
}

function handleDeleteOne(ind: number) {
    currentFiles.value.splice(ind, 1);
}
// #endregion
</script>

<template>
    <div
        :class="[$style.VFile, classList]"
        :data-test-id="name"
    >
        <div
            v-if="label"
            :class="$style.label"
        >
            <div
                :class="$style.text"
                v-html="labelString"
            >
            </div>
        </div>

        <div
            :class="$style.wrapper"
            @drop.prevent="handleFileChange($event, true)"
            @dragover.prevent="() => {}"
        >
            <label
                :for="`file_${uid}`"
                :class="$style.container"
            >
                <input
                    :id="`file_${uid}`"
                    ref="fileRef"
                    type="file"
                    :class="$style.input"
                    :accept="acceptedTypes"
                    :multiple="maxFilesCount > 1"
                    @change="handleFileChange($event, false)"
                >
                <span :class="$style.left">
                    <VIcon
                        :class="$style.fileIcon"
                        size="custom"
                        name="file-stroke"
                    />

                    <Transition
                        mode="out-in"
                        name="dropdown"
                    >
                        <span v-if="currentFiles.length && maxFilesCount === 1" :class="$style.header">
                            <span
                                :key="loadStatus"
                                :class="$style.loadStatus"
                                v-html="loadStatus"
                            />
                            <span
                                :class="$style.fileName"
                                v-html="filaNameFull"
                            />
                        </span>
                        <span
                            v-else-if="errorText"
                            :key="errorText"
                            :class="$style.header"
                        >
                            <span
                                :class="$style.title"
                                v-html="errorText"
                            />
                        </span>
                        <span
                            v-else
                            :key="placeholder || mobilePlaceholder"
                            :class="$style.header"
                        >
                            <span
                                :class="$style.title"
                                v-html="placeholder"
                            />
                            <span
                                :class="[$style.title, $style._mobile]"
                                v-html="mobilePlaceholder"
                            />
                        </span>
                    </Transition>
                </span>

                <VButton
                    :class="$style.loadBtn"
                    color="tertiary"
                    :disabled="disabled"
                    @click="handleClick"
                >
                    {{ btnText }}
                </VButton>
                <VButton
                    :class="[$style.loadBtn, $style._mobile]"
                    color="tertiary"
                    :disabled="disabled"
                    full-width
                    @click="handleClick"
                >
                    {{ btnMobileText }}
                </VButton>
            </label>
        </div>

        <transition name="fade-fast">
            <ul v-if="currentFiles.length && maxFilesCount > 1" :class="$style.files">
                <li
                    v-for="(item, ind) in currentFiles"
                    :key="`item_${ind}`"
                    :class="$style.file"
                >
                    <div :class="$style.fileTitle">{{item.name}}</div>
                    <button :class="$style.fileBtn" @click="handleDeleteOne(ind)">
                        <VIcon name="close"/>
                    </button>
                </li>
            </ul>
        </transition>

        <transition name="fade-fast">
            <InputHint
                v-if="msg"
                :absolute="isSearch || absoluteHint"
                :theme="theme"
                :disabled="disabled"
            >
                {{ msg }}
            </InputHint>
        </transition>
    </div>
</template>

<style lang="scss"
       module
>
    /* Colors */
    $error-color: $primary-900;
    $success-color: $additional-success-900;
    $grey-color: $base-500;

    // base
    $base-black: $base-900;
    $base-white: $base-0;

    .VFile {
        width: 100%;
        transition: opacity $default-transition;

        /* Sizes */
        &._medium {
            .container {
                padding: 1.6rem 2.4rem;
            }

            .fileIcon {
                width: 3.2rem;
                height: 3.2rem;
                color: $base-100;
            }

            .label {
                @include text(l3);

                margin-bottom: 1.2rem;
            }

            .loadStatus,
            .title {
                @include text(t3);

                white-space: nowrap;
            }

            .fileName {
                @include text(l1u);
            }

            .files {
                margin-top: 1.2rem;
            }

            .file {
                padding: .4rem .4rem .4rem 1.6rem;
            }

            .fileTitle {
                @include text(l1u);
            }

            .fileBtn {
                width: 4rem;
                height: 4rem;
            }
        }

        /* Colors */
        &._light {
            .container {
                border: 1px dashed $base-200;
                background-color: $base-white;

                @include hover {
                    &:hover:not(._active) {
                        &:not(._disabled) {
                            border-color: $base-400;
                        }
                    }
                }
            }

            .loadStatus {
                color: $grey-color;
            }

            .label {
                color: $base-black;

                span {
                    color: $error-color;
                }
            }

            .fileName {
                color: $base-black;
            }
        }

        /* Mods */
        &._disabled {
            border-color: $base-200;
            cursor: not-allowed;

            .wrapper {
                pointer-events: none;
            }

            .title {
                color: $base-400;
            }
        }

        /* Когда файл выбран */
        &._active {
            //
        }

        /* Ошибки */
        &._error {
            .header {
                color: $error-color;
            }

            .title {
                @include respond-to(mobile) {
                    position: relative;
                    visibility: visible;
                    pointer-events: all;
                }
            }
        }

        .loadBtn {
            &._mobile {
                display: none;
            }

            @include respond-to(mobile) {
                display: none;

                &._mobile {
                    display: block;
                }
            }
        }
    }

    .wrapper {
        position: relative;
        width: 100%;
    }

    .container {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: border-color $default-transition;
        cursor: pointer;
        user-select: none;

        @include respond-to(mobile) {
            flex-direction: column;
            gap: 1.2rem;
        }
    }

    .left {
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 1.6rem;
        width: 100%;

        @include respond-to(mobile) {
            flex-direction: column;
            gap: 1.2rem;
        }
    }

    .header {
        display: flex;
        flex-direction: column;
        width: 100%;

        @include respond-to(mobile) {
            flex-direction: row;
            justify-content: center;
            gap: .8rem;
        }
    }

    .fileIcon {
        flex-shrink: 0;
    }

    .loadStatus {
        margin-bottom: .4rem;
    }

    .title {
        @include respond-to(mobile) {
            position: absolute;
            visibility: hidden;
            pointer-events: none;
        }

        &._mobile {
            position: absolute;
            visibility: hidden;
            pointer-events: none;

            @include respond-to(mobile) {
                position: relative;
                visibility: visible;
                pointer-events: all;
            }
        }
    }

    .files {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: .8rem;

        @include respond-to(mobile) {
            grid-template-columns: 1fr;
        }
    }

    .file {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: .8rem;
        background: $base-50;
    }

    .fileBtn {
        cursor: pointer;
    }

    .input {
        display: none;
    }
</style>
