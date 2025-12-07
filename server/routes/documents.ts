import { Router, Response } from "express";
import multer from "multer";
import { storage } from "../storage";
import { authenticateToken, AuthRequest } from "../middleware/auth";
import { generateEmbedding, chunkText } from "../services/ai";

const router = Router();

// Configure multer for file uploads
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB limit
});

// All routes require authentication
router.use(authenticateToken);

// Upload document
router.post("/upload/:projectId", upload.single("file"), async (req: AuthRequest, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const projectId = req.params.projectId;

    // Verify project ownership
    const project = await storage.getProject(projectId);
    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    // Extract text content from file (simplified - you'd implement proper parsing)
    const content = req.file.buffer.toString("utf-8");

    // Create document
    const document = await storage.createDocument(
      projectId,
      req.file.originalname,
      req.file.mimetype,
      content
    );

    // Process document asynchronously (chunk and embed)
    processDocument(document.id, content).catch(console.error);

    res.status(201).json(document);
  } catch (error) {
    console.error("Upload error:", error);
    res.status(500).json({ error: "Failed to upload document" });
  }
});

// Process document: chunk and create embeddings
async function processDocument(documentId: number, content: string) {
  try {
    const chunks = chunkText(content);

    for (let i = 0; i < chunks.length; i++) {
      const embedding = await generateEmbedding(chunks[i]);
      await storage.createChunk(documentId, chunks[i], embedding, i);
    }

    // Mark document as processed
    await storage.updateDocument(documentId, { processed: true });
  } catch (error) {
    console.error("Document processing error:", error);
  }
}

// Get document
router.get("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const document = await storage.getDocument(parseInt(req.params.id));

    if (!document) {
      return res.status(404).json({ error: "Document not found" });
    }

    // Verify project ownership
    const project = await storage.getProject(document.projectId);
    if (!project || project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    res.json(document);
  } catch (error) {
    console.error("Get document error:", error);
    res.status(500).json({ error: "Failed to fetch document" });
  }
});

// Delete document
router.delete("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const document = await storage.getDocument(parseInt(req.params.id));

    if (!document) {
      return res.status(404).json({ error: "Document not found" });
    }

    // Verify project ownership
    const project = await storage.getProject(document.projectId);
    if (!project || project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    await storage.deleteDocument(parseInt(req.params.id));
    res.json({ message: "Document deleted successfully" });
  } catch (error) {
    console.error("Delete document error:", error);
    res.status(500).json({ error: "Failed to delete document" });
  }
});

export default router;
