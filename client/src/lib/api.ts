import type {
  User,
  Project,
  Document,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  DashboardStats,
  RFPAnalysis,
  GenerateBidRequest,
} from "@shared/types";

const API_BASE = "/api";

// Get auth token from localStorage
function getAuthToken(): string | null {
  return localStorage.getItem("accessToken");
}

// API request helper
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Request failed" }));
    throw new Error(error.error || `HTTP ${response.status}`);
  }

  return response.json();
}

// Auth API
export const authApi = {
  register: (data: RegisterRequest) =>
    apiRequest<AuthResponse>("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  login: (data: LoginRequest) =>
    apiRequest<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  refresh: (refreshToken: string) =>
    apiRequest<{ accessToken: string }>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify({ refreshToken }),
    }),

  me: () => apiRequest<User>("/auth/me"),

  logout: (refreshToken: string) =>
    apiRequest<{ message: string }>("/auth/logout", {
      method: "POST",
      body: JSON.stringify({ refreshToken }),
    }),
};

// Projects API
export const projectsApi = {
  create: (data: { name: string; clientName: string }) =>
    apiRequest<Project>("/projects", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  getAll: () => apiRequest<Project[]>("/projects"),

  getById: (id: string) => apiRequest<Project>(`/projects/${id}`),

  update: (id: string, data: Partial<Project>) =>
    apiRequest<Project>(`/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  delete: (id: string) =>
    apiRequest<{ message: string }>(`/projects/${id}`, {
      method: "DELETE",
    }),

  getDocuments: (id: string) => apiRequest<Document[]>(`/projects/${id}/documents`),

  getStats: () => apiRequest<DashboardStats>("/projects/dashboard/stats"),
};

// Documents API
export const documentsApi = {
  upload: async (projectId: string, file: File) => {
    const token = getAuthToken();
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE}/documents/upload/${projectId}`, {
      method: "POST",
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: "Upload failed" }));
      throw new Error(error.error);
    }

    return response.json() as Promise<Document>;
  },

  getById: (id: number) => apiRequest<Document>(`/documents/${id}`),

  delete: (id: number) =>
    apiRequest<{ message: string }>(`/documents/${id}`, {
      method: "DELETE",
    }),
};

// Bids API
export const bidsApi = {
  generate: (data: GenerateBidRequest) =>
    apiRequest<{ bids: Array<{ model: string; content?: string; error?: string; id?: number }> }>(
      "/bids/generate",
      {
        method: "POST",
        body: JSON.stringify(data),
      }
    ),

  getHistory: (projectId: string) =>
    apiRequest<Array<{
      id: number;
      projectId: string;
      content: string;
      model: string;
      version: number;
      createdAt: Date;
    }>>(`/bids/history/${projectId}`),

  analyze: (projectId: string) =>
    apiRequest<RFPAnalysis>(`/bids/analyze/${projectId}`, {
      method: "POST",
    }),

  getAnalysis: (projectId: string) =>
    apiRequest<RFPAnalysis>(`/bids/analysis/${projectId}`),
};
