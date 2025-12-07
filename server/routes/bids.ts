import { Router, Response } from "express";
import { storage, db } from "../storage";
import { authenticateToken, AuthRequest } from "../middleware/auth";
import { generateBid, generateEmbedding, analyzeRFP } from "../services/ai";
import { GenerateBidRequestSchema } from "@shared/types";
import { fromZodError } from "zod-validation-error";
import { generatedBids } from "@shared/schema";
import { eq, desc } from "drizzle-orm";

const router = Router();

// All routes require authentication
router.use(authenticateToken);

// Generate bid
router.post("/generate", async (req: AuthRequest, res: Response) => {
  try {
    const validated = GenerateBidRequestSchema.parse(req.body);

    // Verify project ownership
    const project = await storage.getProject(validated.projectId);
    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    // Get project documents
    const documents = await storage.getProjectDocuments(validated.projectId);
    if (documents.length === 0) {
      return res.status(400).json({ error: "No documents uploaded for this project" });
    }

    // Combine document content
    const rfqContent = documents.map(doc => doc.content || "").join("\n\n");

    // Get relevant context using RAG
    const queryEmbedding = await generateEmbedding(rfqContent.slice(0, 500)); // Use first part as query
    const similarChunks = await storage.searchSimilarChunks(queryEmbedding, validated.projectId, 5);
    const projectContext = similarChunks.map(chunk => chunk.content).join("\n\n");

    // Generate bids with requested models
    const results = await Promise.all(
      validated.models.map(async (model) => {
        try {
          const content = await generateBid(model, {
            rfqContent,
            projectContext,
            instructions: validated.instructions,
          });

          // Save generated bid
          const [bid] = await db.insert(generatedBids)
            .values({
              projectId: validated.projectId,
              content,
              model,
              version: 1,
            })
            .returning();

          return {
            model,
            content,
            id: bid.id,
          };
        } catch (error: any) {
          return {
            model,
            error: error.message,
          };
        }
      })
    );

    res.json({ bids: results });
  } catch (error: any) {
    if (error.name === "ZodError") {
      return res.status(400).json({ error: fromZodError(error).message });
    }
    console.error("Generate bid error:", error);
    res.status(500).json({ error: "Failed to generate bid" });
  }
});

// Get bid history
router.get("/history/:projectId", async (req: AuthRequest, res: Response) => {
  try {
    // Verify project ownership
    const project = await storage.getProject(req.params.projectId);
    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    const bids = await db.select()
      .from(generatedBids)
      .where(eq(generatedBids.projectId, req.params.projectId))
      .orderBy(desc(generatedBids.createdAt));

    res.json(bids);
  } catch (error) {
    console.error("Get bid history error:", error);
    res.status(500).json({ error: "Failed to fetch bid history" });
  }
});

// Analyze RFP
router.post("/analyze/:projectId", async (req: AuthRequest, res: Response) => {
  try {
    // Verify project ownership
    const project = await storage.getProject(req.params.projectId);
    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    // Get project documents
    const documents = await storage.getProjectDocuments(req.params.projectId);
    if (documents.length === 0) {
      return res.status(400).json({ error: "No documents uploaded for this project" });
    }

    // Combine document content
    const rfqContent = documents.map(doc => doc.content || "").join("\n\n");

    // Analyze RFP
    const analysis = await analyzeRFP(rfqContent);

    // Save analysis
    const saved = await storage.createRFPAnalysis({
      projectId: req.params.projectId,
      ...analysis,
    });

    res.json(saved);
  } catch (error) {
    console.error("Analyze RFP error:", error);
    res.status(500).json({ error: "Failed to analyze RFP" });
  }
});

// Get latest analysis
router.get("/analysis/:projectId", async (req: AuthRequest, res: Response) => {
  try {
    // Verify project ownership
    const project = await storage.getProject(req.params.projectId);
    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    const analysis = await storage.getLatestRFPAnalysis(req.params.projectId);

    if (!analysis) {
      return res.status(404).json({ error: "No analysis found for this project" });
    }

    res.json(analysis);
  } catch (error) {
    console.error("Get analysis error:", error);
    res.status(500).json({ error: "Failed to fetch analysis" });
  }
});

export default router;
