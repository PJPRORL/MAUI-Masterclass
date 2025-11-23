window.monacoInterop = {
    editors: {},
    initialize: function (elementId, initialCode, language) {
        require(['vs/editor/editor.main'], function () {
            var editor = monaco.editor.create(document.getElementById(elementId), {
                value: initialCode,
                language: language,
                theme: 'vs-dark',
                automaticLayout: true,
                minimap: { enabled: false }
            });
            window.monacoInterop.editors[elementId] = editor;
        });
    },
    getValue: function (elementId) {
        if (window.monacoInterop.editors[elementId]) {
            return window.monacoInterop.editors[elementId].getValue();
        }
        return "";
    }
};
