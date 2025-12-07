import { drizzle } from "drizzle-orm/neon-serverless";
import { neonConfig, Pool } from "@neondatabase/serverless";
import ws from "ws";
import { eq, desc, and, sql, cosineDistance } from "drizzle-orm";
import * as schema from "@shared/schema";
import type { User, Project, Document, RFPAnalysis, WinProbabilityPrediction, DashboardStats } from "@shared/types";

// Configure Neon for WebSocket support
neonConfig.webSocketConstructor = ws;

if (!process.env.DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable is not set");
}

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
export const db = drizzle(pool, { schema });

// Storage interface for testability
export interface IStorage {
  // User operations
  createUser(email: string, passwordHash: string, name: string): Promise<User>;
  getUserByEmail(email: string): Promise<User | null>;
  getUserById(id: number): Promise<User | null>;
  updateUser(id: number, updates: Partial<User>): Promise<User>;

  // Session operations
  createSession(userId: number, refreshToken: string, expiresAt: Date): Promise<void>;
  getSessionByToken(refreshToken: string): Promise<{ userId: number; expiresAt: Date } | null>;
  deleteSession(refreshToken: string): Promise<void>;
  deleteUserSessions(userId: number): Promise<void>;

  // Project operations
  createProject(name: string, clientName: string, userId: number): Promise<Project>;
  getProject(id: string): Promise<Project | null>;
  getProjectsByUser(userId: number): Promise<Project[]>;
  updateProject(id: string, updates: Partial<Project>): Promise<Project>;
  deleteProject(id: string): Promise<void>;

  // Document operations
  createDocument(projectId: string, fileName: string, fileType: string, content: string): Promise<Document>;
  getDocument(id: number): Promise<Document | null>;
  getProjectDocuments(projectId: string): Promise<Document[]>;
  updateDocument(id: number, updates: Partial<Document>): Promise<Document>;
  deleteDocument(id: number): Promise<void>;

  // Document chunk operations
  createChunk(documentId: number, content: string, embedding: number[], chunkIndex: number): Promise<void>;
  searchSimilarChunks(embedding: number[], projectId: string, limit: number): Promise<Array<{ content: string; similarity: number }>>;

  // RFP Analysis operations
  createRFPAnalysis(analysis: Omit<RFPAnalysis, "id" | "createdAt">): Promise<RFPAnalysis>;
  getLatestRFPAnalysis(projectId: string): Promise<RFPAnalysis | null>;

  // Win Probability operations
  createWinProbabilityPrediction(prediction: Omit<WinProbabilityPrediction, "id" | "createdAt">): Promise<WinProbabilityPrediction>;
  getLatestWinProbability(projectId: string): Promise<WinProbabilityPrediction | null>;

  // Dashboard statistics
  getDashboardStats(userId: number): Promise<DashboardStats>;
}

// Database implementation
export class DatabaseStorage implements IStorage {
  // User operations
  async createUser(email: string, passwordHash: string, name: string): Promise<User> {
    const [user] = await db.insert(schema.users)
      .values({ email, passwordHash, name })
      .returning();
    return user as User;
  }

  async getUserByEmail(email: string): Promise<User | null> {
    const [user] = await db.select()
      .from(schema.users)
      .where(eq(schema.users.email, email))
      .limit(1);
    return (user as User) || null;
  }

  async getUserById(id: number): Promise<User | null> {
    const [user] = await db.select()
      .from(schema.users)
      .where(eq(schema.users.id, id))
      .limit(1);
    return (user as User) || null;
  }

  async updateUser(id: number, updates: Partial<User>): Promise<User> {
    const [user] = await db.update(schema.users)
      .set({ ...updates, updatedAt: new Date() })
      .where(eq(schema.users.id, id))
      .returning();
    return user as User;
  }

  // Session operations
  async createSession(userId: number, refreshToken: string, expiresAt: Date): Promise<void> {
    await db.insert(schema.sessions)
      .values({ userId, refreshToken, expiresAt });
  }

  async getSessionByToken(refreshToken: string): Promise<{ userId: number; expiresAt: Date } | null> {
    const [session] = await db.select()
      .from(schema.sessions)
      .where(eq(schema.sessions.refreshToken, refreshToken))
      .limit(1);
    return session ? { userId: session.userId, expiresAt: session.expiresAt } : null;
  }

  async deleteSession(refreshToken: string): Promise<void> {
    await db.delete(schema.sessions)
      .where(eq(schema.sessions.refreshToken, refreshToken));
  }

  async deleteUserSessions(userId: number): Promise<void> {
    await db.delete(schema.sessions)
      .where(eq(schema.sessions.userId, userId));
  }

  // Project operations
  async createProject(name: string, clientName: string, userId: number): Promise<Project> {
    const [project] = await db.insert(schema.projects)
      .values({ name, clientName, userId })
      .returning();
    return project as Project;
  }

  async getProject(id: string): Promise<Project | null> {
    const [project] = await db.select()
      .from(schema.projects)
      .where(eq(schema.projects.id, id))
      .limit(1);
    return (project as Project) || null;
  }

  async getProjectsByUser(userId: number): Promise<Project[]> {
    const projects = await db.select()
      .from(schema.projects)
      .where(eq(schema.projects.userId, userId))
      .orderBy(desc(schema.projects.createdAt));
    return projects as Project[];
  }

  async updateProject(id: string, updates: Partial<Project>): Promise<Project> {
    const [project] = await db.update(schema.projects)
      .set({ ...updates, updatedAt: new Date() })
      .where(eq(schema.projects.id, id))
      .returning();
    return project as Project;
  }

  async deleteProject(id: string): Promise<void> {
    await db.delete(schema.projects)
      .where(eq(schema.projects.id, id));
  }

  // Document operations
  async createDocument(projectId: string, fileName: string, fileType: string, content: string): Promise<Document> {
    const [document] = await db.insert(schema.documents)
      .values({ projectId, fileName, fileType, content, processed: false })
      .returning();
    return document as Document;
  }

  async getDocument(id: number): Promise<Document | null> {
    const [document] = await db.select()
      .from(schema.documents)
      .where(eq(schema.documents.id, id))
      .limit(1);
    return (document as Document) || null;
  }

  async getProjectDocuments(projectId: string): Promise<Document[]> {
    const documents = await db.select()
      .from(schema.documents)
      .where(eq(schema.documents.projectId, projectId))
      .orderBy(desc(schema.documents.uploadedAt));
    return documents as Document[];
  }

  async updateDocument(id: number, updates: Partial<Document>): Promise<Document> {
    const [document] = await db.update(schema.documents)
      .set(updates)
      .where(eq(schema.documents.id, id))
      .returning();
    return document as Document;
  }

  async deleteDocument(id: number): Promise<void> {
    await db.delete(schema.documents)
      .where(eq(schema.documents.id, id));
  }

  // Document chunk operations
  async createChunk(documentId: number, content: string, embedding: number[], chunkIndex: number): Promise<void> {
    await db.insert(schema.documentChunks)
      .values({
        documentId,
        content,
        embedding: sql`${JSON.stringify(embedding)}::vector`,
        chunkIndex
      });
  }

  async searchSimilarChunks(embedding: number[], projectId: string, limit: number = 5): Promise<Array<{ content: string; similarity: number }>> {
    const embeddingStr = `[${embedding.join(',')}]`;

    const results = await db.select({
      content: schema.documentChunks.content,
      similarity: sql<number>`1 - (${schema.documentChunks.embedding} <=> ${embeddingStr}::vector)`,
    })
      .from(schema.documentChunks)
      .innerJoin(schema.documents, eq(schema.documentChunks.documentId, schema.documents.id))
      .where(eq(schema.documents.projectId, projectId))
      .orderBy(sql`${schema.documentChunks.embedding} <=> ${embeddingStr}::vector`)
      .limit(limit);

    return results;
  }

  // RFP Analysis operations
  async createRFPAnalysis(analysis: Omit<RFPAnalysis, "id" | "createdAt">): Promise<RFPAnalysis> {
    const [result] = await db.insert(schema.rfpAnalyses)
      .values(analysis)
      .returning();
    return result as RFPAnalysis;
  }

  async getLatestRFPAnalysis(projectId: string): Promise<RFPAnalysis | null> {
    const [analysis] = await db.select()
      .from(schema.rfpAnalyses)
      .where(eq(schema.rfpAnalyses.projectId, projectId))
      .orderBy(desc(schema.rfpAnalyses.createdAt))
      .limit(1);
    return (analysis as RFPAnalysis) || null;
  }

  // Win Probability operations
  async createWinProbabilityPrediction(prediction: Omit<WinProbabilityPrediction, "id" | "createdAt">): Promise<WinProbabilityPrediction> {
    const [result] = await db.insert(schema.winProbabilityPredictions)
      .values(prediction)
      .returning();
    return result as WinProbabilityPrediction;
  }

  async getLatestWinProbability(projectId: string): Promise<WinProbabilityPrediction | null> {
    const [prediction] = await db.select()
      .from(schema.winProbabilityPredictions)
      .where(eq(schema.winProbabilityPredictions.projectId, projectId))
      .orderBy(desc(schema.winProbabilityPredictions.createdAt))
      .limit(1);
    return (prediction as WinProbabilityPrediction) || null;
  }

  // Dashboard statistics
  async getDashboardStats(userId: number): Promise<DashboardStats> {
    const projects = await this.getProjectsByUser(userId);

    const activeProjects = projects.filter(p => p.status === "active").length;
    const submittedProjects = projects.filter(p => p.status === "submitted").length;
    const closedWonProjects = projects.filter(p => p.status === "closed-won").length;
    const closedLostProjects = projects.filter(p => p.status === "closed-lost").length;

    const totalClosed = closedWonProjects + closedLostProjects;
    const winRate = totalClosed > 0 ? closedWonProjects / totalClosed : 0;

    return {
      activeProjects,
      submittedProjects,
      closedWonProjects,
      closedLostProjects,
      winRate,
      totalProjects: projects.length,
    };
  }
}

export const storage = new DatabaseStorage();
