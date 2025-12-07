import { Router, Response } from "express";
import { storage } from "../storage";
import {
  generateAccessToken,
  generateRefreshToken,
  hashPassword,
  verifyPassword,
  verifyRefreshToken,
  authenticateToken,
  AuthRequest,
} from "../middleware/auth";
import { LoginRequestSchema, RegisterRequestSchema } from "@shared/types";
import { fromZodError } from "zod-validation-error";

const router = Router();

// Register
router.post("/register", async (req, res: Response) => {
  try {
    const validated = RegisterRequestSchema.parse(req.body);

    // Check if user already exists
    const existingUser = await storage.getUserByEmail(validated.email);
    if (existingUser) {
      return res.status(400).json({ error: "Email already registered" });
    }

    // Hash password
    const passwordHash = await hashPassword(validated.password);

    // Create user
    const user = await storage.createUser(validated.email, passwordHash, validated.name);

    // Generate tokens
    const accessToken = generateAccessToken(user.id, user.email, user.role);
    const refreshToken = generateRefreshToken(user.id);

    // Store refresh token
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);
    await storage.createSession(user.id, refreshToken, expiresAt);

    // Remove password hash from response
    const { ...userWithoutPassword } = user;

    res.status(201).json({
      user: userWithoutPassword,
      accessToken,
      refreshToken,
    });
  } catch (error: any) {
    if (error.name === "ZodError") {
      return res.status(400).json({ error: fromZodError(error).message });
    }
    console.error("Registration error:", error);
    res.status(500).json({ error: "Registration failed" });
  }
});

// Login
router.post("/login", async (req, res: Response) => {
  try {
    const validated = LoginRequestSchema.parse(req.body);

    // Find user
    const user = await storage.getUserByEmail(validated.email);
    if (!user) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    // Verify password
    const isValid = await verifyPassword(validated.password, user.passwordHash);
    if (!isValid) {
      return res.status(401).json({ error: "Invalid credentials" });
    }

    // Generate tokens
    const accessToken = generateAccessToken(user.id, user.email, user.role);
    const refreshToken = generateRefreshToken(user.id);

    // Store refresh token
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);
    await storage.createSession(user.id, refreshToken, expiresAt);

    // Remove password hash from response
    const { passwordHash, ...userWithoutPassword } = user;

    res.json({
      user: userWithoutPassword,
      accessToken,
      refreshToken,
    });
  } catch (error: any) {
    if (error.name === "ZodError") {
      return res.status(400).json({ error: fromZodError(error).message });
    }
    console.error("Login error:", error);
    res.status(500).json({ error: "Login failed" });
  }
});

// Refresh token
router.post("/refresh", async (req, res: Response) => {
  const { refreshToken } = req.body;

  if (!refreshToken) {
    return res.status(401).json({ error: "Refresh token required" });
  }

  const userId = await verifyRefreshToken(refreshToken);
  if (!userId) {
    return res.status(403).json({ error: "Invalid refresh token" });
  }

  const user = await storage.getUserById(userId);
  if (!user) {
    return res.status(404).json({ error: "User not found" });
  }

  // Generate new access token
  const accessToken = generateAccessToken(user.id, user.email, user.role);

  res.json({ accessToken });
});

// Get current user
router.get("/me", authenticateToken, async (req: AuthRequest, res: Response) => {
  try {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const user = await storage.getUserById(req.user.id);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    const { passwordHash, ...userWithoutPassword } = user;
    res.json(userWithoutPassword);
  } catch (error) {
    console.error("Get user error:", error);
    res.status(500).json({ error: "Failed to fetch user" });
  }
});

// Logout
router.post("/logout", authenticateToken, async (req: AuthRequest, res: Response) => {
  const { refreshToken } = req.body;

  if (refreshToken) {
    await storage.deleteSession(refreshToken);
  }

  res.json({ message: "Logged out successfully" });
});

export default router;
