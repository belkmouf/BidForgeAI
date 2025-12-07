import { Router, Response } from "express";
import { storage } from "../storage";
import { authenticateToken, AuthRequest } from "../middleware/auth";
import { z } from "zod";
import { fromZodError } from "zod-validation-error";

const router = Router();

// All routes require authentication
router.use(authenticateToken);

// Create project
const CreateProjectSchema = z.object({
  name: z.string().min(1),
  clientName: z.string().min(1),
});

router.post("/", async (req: AuthRequest, res: Response) => {
  try {
    const validated = CreateProjectSchema.parse(req.body);

    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const project = await storage.createProject(
      validated.name,
      validated.clientName,
      req.user.id
    );

    res.status(201).json(project);
  } catch (error: any) {
    if (error.name === "ZodError") {
      return res.status(400).json({ error: fromZodError(error).message });
    }
    console.error("Create project error:", error);
    res.status(500).json({ error: "Failed to create project" });
  }
});

// Get all projects for user
router.get("/", async (req: AuthRequest, res: Response) => {
  try {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const projects = await storage.getProjectsByUser(req.user.id);
    res.json(projects);
  } catch (error) {
    console.error("Get projects error:", error);
    res.status(500).json({ error: "Failed to fetch projects" });
  }
});

// Get single project
router.get("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const project = await storage.getProject(req.params.id);

    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    // Check ownership
    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    res.json(project);
  } catch (error) {
    console.error("Get project error:", error);
    res.status(500).json({ error: "Failed to fetch project" });
  }
});

// Update project
const UpdateProjectSchema = z.object({
  name: z.string().min(1).optional(),
  clientName: z.string().min(1).optional(),
  status: z.enum(["active", "submitted", "closed-won", "closed-lost"]).optional(),
  metadata: z.record(z.any()).optional(),
});

router.patch("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const validated = UpdateProjectSchema.parse(req.body);

    const project = await storage.getProject(req.params.id);

    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    // Check ownership
    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    const updated = await storage.updateProject(req.params.id, validated);
    res.json(updated);
  } catch (error: any) {
    if (error.name === "ZodError") {
      return res.status(400).json({ error: fromZodError(error).message });
    }
    console.error("Update project error:", error);
    res.status(500).json({ error: "Failed to update project" });
  }
});

// Delete project
router.delete("/:id", async (req: AuthRequest, res: Response) => {
  try {
    const project = await storage.getProject(req.params.id);

    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    // Check ownership
    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    await storage.deleteProject(req.params.id);
    res.json({ message: "Project deleted successfully" });
  } catch (error) {
    console.error("Delete project error:", error);
    res.status(500).json({ error: "Failed to delete project" });
  }
});

// Get project documents
router.get("/:id/documents", async (req: AuthRequest, res: Response) => {
  try {
    const project = await storage.getProject(req.params.id);

    if (!project) {
      return res.status(404).json({ error: "Project not found" });
    }

    // Check ownership
    if (project.userId !== req.user?.id) {
      return res.status(403).json({ error: "Access denied" });
    }

    const documents = await storage.getProjectDocuments(req.params.id);
    res.json(documents);
  } catch (error) {
    console.error("Get documents error:", error);
    res.status(500).json({ error: "Failed to fetch documents" });
  }
});

// Get dashboard stats
router.get("/dashboard/stats", async (req: AuthRequest, res: Response) => {
  try {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const stats = await storage.getDashboardStats(req.user.id);
    res.json(stats);
  } catch (error) {
    console.error("Get stats error:", error);
    res.status(500).json({ error: "Failed to fetch stats" });
  }
});

export default router;
