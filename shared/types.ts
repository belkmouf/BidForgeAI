import { z } from "zod";

// User types
export const UserSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  name: z.string(),
  role: z.enum(["admin", "manager", "user", "viewer"]),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type User = z.infer<typeof UserSchema>;

// Project types
export const ProjectStatusSchema = z.enum(["active", "submitted", "closed-won", "closed-lost"]);

export const ProjectSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  clientName: z.string(),
  status: ProjectStatusSchema,
  metadata: z.record(z.any()).nullable(),
  userId: z.number(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type Project = z.infer<typeof ProjectSchema>;
export type ProjectStatus = z.infer<typeof ProjectStatusSchema>;

// Document types
export const DocumentSchema = z.object({
  id: z.number(),
  projectId: z.string().uuid(),
  fileName: z.string(),
  fileType: z.string(),
  content: z.string().nullable(),
  processed: z.boolean(),
  uploadedAt: z.date(),
});

export type Document = z.infer<typeof DocumentSchema>;

// RFP Analysis types
export const RiskLevelSchema = z.enum(["low", "medium", "high", "critical"]);

export const RFPAnalysisSchema = z.object({
  id: z.number(),
  projectId: z.string().uuid(),
  qualityScore: z.number().min(0).max(100),
  clarityScore: z.number().min(0).max(100),
  doabilityScore: z.number().min(0).max(100),
  vendorRiskScore: z.number().min(0).max(100),
  overallRisk: RiskLevelSchema,
  findings: z.object({
    redFlags: z.array(z.string()),
    opportunities: z.array(z.string()),
    missingDocuments: z.array(z.string()),
  }),
  recommendations: z.array(z.object({
    title: z.string(),
    description: z.string(),
    priority: z.enum(["low", "medium", "high", "critical"]),
    estimatedTime: z.string(),
  })),
  createdAt: z.date(),
});

export type RFPAnalysis = z.infer<typeof RFPAnalysisSchema>;
export type RiskLevel = z.infer<typeof RiskLevelSchema>;

// Win Probability types
export const WinProbabilityPredictionSchema = z.object({
  id: z.number(),
  projectId: z.string().uuid(),
  probability: z.number().min(0).max(1),
  confidence: z.number().min(0).max(1),
  features: z.record(z.number()),
  riskFactors: z.array(z.string()),
  strengthFactors: z.array(z.string()),
  recommendations: z.array(z.string()),
  createdAt: z.date(),
});

export type WinProbabilityPrediction = z.infer<typeof WinProbabilityPredictionSchema>;

// AI Model types
export const AIModelSchema = z.enum(["openai", "anthropic", "gemini", "deepseek"]);
export type AIModel = z.infer<typeof AIModelSchema>;

// API request/response types
export const LoginRequestSchema = z.object({
  email: z.string().email(),
  password: z.string(),
});

export const RegisterRequestSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, "Password must contain uppercase, lowercase, and number"),
  name: z.string().min(1),
});

export const AuthResponseSchema = z.object({
  user: UserSchema,
  accessToken: z.string(),
  refreshToken: z.string(),
});

export type LoginRequest = z.infer<typeof LoginRequestSchema>;
export type RegisterRequest = z.infer<typeof RegisterRequestSchema>;
export type AuthResponse = z.infer<typeof AuthResponseSchema>;

// Bid generation request
export const GenerateBidRequestSchema = z.object({
  projectId: z.string().uuid(),
  models: z.array(AIModelSchema),
  instructions: z.string().optional(),
});

export type GenerateBidRequest = z.infer<typeof GenerateBidRequestSchema>;

// Chat message types
export const ChatMessageSchema = z.object({
  role: z.enum(["user", "assistant", "system"]),
  content: z.string(),
  timestamp: z.date(),
});

export type ChatMessage = z.infer<typeof ChatMessageSchema>;

// Dashboard statistics
export const DashboardStatsSchema = z.object({
  activeProjects: z.number(),
  submittedProjects: z.number(),
  closedWonProjects: z.number(),
  closedLostProjects: z.number(),
  winRate: z.number(),
  totalProjects: z.number(),
});

export type DashboardStats = z.infer<typeof DashboardStatsSchema>;
