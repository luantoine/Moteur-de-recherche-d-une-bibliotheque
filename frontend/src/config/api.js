import { API_BASE } from "./config";

export const SIMPLE_SEARCH_API = (query) => `${API_BASE}/search/?q=${encodeURIComponent(query)}`;
export const ADVANCED_SEARCH_API = (query) => `${API_BASE}/advanced_search/?regex=${encodeURIComponent(query)}`;
export const BOOK_INFO_API = (bookID) => `${API_BASE}/book/${encodeURIComponent(bookID)}`;