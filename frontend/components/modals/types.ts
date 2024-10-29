export interface HelloProps {
    title?: string,
    description?: string,
}

export interface ContactFormProps {
    title?: string,
}

export interface BaseModalProps {
    tag?: string,
    withCloseBtn?: boolean,
    isfullscreen?: boolean,
    smallContent?: boolean,
    /**
     * Центрирует модальное окна на десктопе
     */
    center?: boolean,
    color?: string,
}

export interface ContactFormFields {
    name: string,
    phone: string,
    email: string,
    project: string,
    subject: string,
    message: string,
    personal: boolean,
    file: string | null,
}

export interface FormSuccessProps {
    title?: string,
    description?: string,
    error?: boolean,
}
