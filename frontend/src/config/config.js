const config = {
    development: {
        backendUrl: "http://127.0.0.1:8000/api",
    },
    production: {
        backendUrl: "",
    },
};

export const LIMIT_BOOK_TOSHOW = 12;
export const NUMBER_OF_BOOK = 1664;

export const API_BASE = config.development.backendUrl;