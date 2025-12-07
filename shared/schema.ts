import { pgTable, text, serial, integer, timestamp, uuid, jsonb, boolean, real, vector } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

// Users table
export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  name: text("name").notNull(),
  role: text("role").notNull().default("user"), // admin, manager, user, viewer
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Sessions table for refresh tokens
export const sessions = pgTable("sessions", {
  id: serial("id").primaryKey(),
  userId: integer("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  refreshToken: text("refresh_token").notNull(),
  expiresAt: timestamp("expires_at").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Projects table
export const projects = pgTable("projects", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: text("name").notNull(),
  clientName: text("client_name").notNull(),
  status: text("status").notNull().default("active"), // active, submitted, closed-won, closed-lost
  metadata: jsonb("metadata"),
  userId: integer("user_id").notNull().references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Documents table
export const documents = pgTable("documents", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  fileName: text("file_name").notNull(),
  fileType: text("file_type").notNull(),
  content: text("content"),
  processed: boolean("processed").default(false).notNull(),
  uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
});

// Document chunks for vector search
export const documentChunks = pgTable("document_chunks", {
  id: serial("id").primaryKey(),
  documentId: integer("document_id").notNull().references(() => documents.id, { onDelete: "cascade" }),
  content: text("content").notNull(),
  embedding: vector("embedding", { dimensions: 1536 }),
  chunkIndex: integer("chunk_index").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// RFP Analyses table
export const rfpAnalyses = pgTable("rfp_analyses", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  qualityScore: integer("quality_score").notNull(),
  clarityScore: integer("clarity_score").notNull(),
  doabilityScore: integer("doability_score").notNull(),
  vendorRiskScore: integer("vendor_risk_score").notNull(),
  overallRisk: text("overall_risk").notNull(), // low, medium, high, critical
  findings: jsonb("findings").notNull(),
  recommendations: jsonb("recommendations").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Vendor database
export const vendorDatabase = pgTable("vendor_database", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  paymentHistory: text("payment_history").notNull(), // excellent, good, fair, poor
  rating: real("rating").notNull(),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// Win probability predictions
export const winProbabilityPredictions = pgTable("win_probability_predictions", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  probability: real("probability").notNull(),
  confidence: real("confidence").notNull(),
  features: jsonb("features").notNull(),
  riskFactors: jsonb("risk_factors").notNull(),
  strengthFactors: jsonb("strength_factors").notNull(),
  recommendations: jsonb("recommendations").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Bid outcomes for model feedback
export const bidOutcomes = pgTable("bid_outcomes", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  outcome: text("outcome").notNull(), // won, lost, no-bid
  actualValue: real("actual_value"),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Conflict detection
export const documentConflicts = pgTable("document_conflicts", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  sourceDocumentId: integer("source_document_id").notNull().references(() => documents.id, { onDelete: "cascade" }),
  targetDocumentId: integer("target_document_id").notNull().references(() => documents.id, { onDelete: "cascade" }),
  conflictType: text("conflict_type").notNull(), // semantic, numeric
  severity: text("severity").notNull(), // low, medium, high, critical
  description: text("description").notNull(),
  sourceText: text("source_text").notNull(),
  targetText: text("target_text").notNull(),
  status: text("status").notNull().default("unresolved"), // unresolved, reviewed, resolved
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Generated bids
export const generatedBids = pgTable("generated_bids", {
  id: serial("id").primaryKey(),
  projectId: uuid("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  content: text("content").notNull(),
  model: text("model").notNull(), // openai, anthropic, gemini, deepseek
  version: integer("version").notNull().default(1),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  projects: many(projects),
  sessions: many(sessions),
}));

export const projectsRelations = relations(projects, ({ one, many }) => ({
  user: one(users, {
    fields: [projects.userId],
    references: [users.id],
  }),
  documents: many(documents),
  rfpAnalyses: many(rfpAnalyses),
  winProbabilityPredictions: many(winProbabilityPredictions),
  bidOutcomes: many(bidOutcomes),
  conflicts: many(documentConflicts),
  generatedBids: many(generatedBids),
}));

export const documentsRelations = relations(documents, ({ one, many }) => ({
  project: one(projects, {
    fields: [documents.projectId],
    references: [projects.id],
  }),
  chunks: many(documentChunks),
}));

export const documentChunksRelations = relations(documentChunks, ({ one }) => ({
  document: one(documents, {
    fields: [documentChunks.documentId],
    references: [documents.id],
  }),
}));
