const config = {
    development: {
        backendUrl: "http://127.0.0.1:8000/api",
    },
    production: {
        backendUrl: "",
    },
};

export const API_BASE = config.development.backendUrl;