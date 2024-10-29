import type { headScriptList, headScriptItem } from '~/types/common';

export function useThirdPartyScripts() {
    const handleSetHeadSrc = (scriptItem: headScriptItem) => {
        const script = document.createElement('script');
        script.type = 'text/javascript';

        if (scriptItem.async) {
            script.async = true;
        }

        script.src = (scriptItem.src as string);
        document.head.appendChild(script);
    };

    const handleSetHeadScript = (scriptItem: headScriptItem, idx: number) => {
        const script = document.createElement('script');
        if (scriptItem.async) {
            script.async = true;
        }

        script.text = (scriptItem.innerHTML as string);
        script.id = `script_${idx}`;
        document.head.appendChild(script);
        const found = document.querySelector(`script[id="script_${idx}"]`);

        if (found) {
            found.removeAttribute('id');
            found.parentNode?.insertBefore(script, found);
        }
    };

    const handleAddScripts = (array: headScriptList) => {
        if (array?.length) {
            array.forEach((scriptItem: headScriptItem, id: number) => {
                if (scriptItem.src) {
                    handleSetHeadSrc(scriptItem);
                } else if (scriptItem.innerHTML) {
                    handleSetHeadScript(scriptItem, id);
                }
            });
        }
    };

    return {
        handleAddScripts,
    };
}
