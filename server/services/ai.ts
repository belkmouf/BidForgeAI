import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";
import { GoogleGenerativeAI } from "@google/genai";
import type { AIModel } from "@shared/types";

// Initialize AI clients
const openai = process.env.OPENAI_API_KEY ? new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
}) : null;

const anthropic = process.env.ANTHROPIC_API_KEY ? new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
}) : null;

const gemini = process.env.GOOGLE_API_KEY ? new GoogleGenerativeAI(process.env.GOOGLE_API_KEY) : null;

export interface GenerateBidOptions {
  projectContext: string;
  rfqContent: string;
  instructions?: string;
}

// Generate embeddings for RAG
export async function generateEmbedding(text: string): Promise<number[]> {
  if (!openai) {
    throw new Error("OpenAI API key not configured");
  }

  const response = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: text,
  });

  return response.data[0].embedding;
}

// Generate bid using OpenAI
export async function generateBidWithOpenAI(options: GenerateBidOptions): Promise<string> {
  if (!openai) {
    throw new Error("OpenAI API key not configured");
  }

  const systemPrompt = `You are an expert construction bid proposal writer. Generate a professional, detailed HTML bid response based on the provided RFQ and project context. Include:
- Executive Summary
- Project Understanding
- Proposed Approach
- Timeline
- Pricing Structure
- Team Qualifications
- Risk Mitigation

Use professional formatting and be persuasive while maintaining accuracy.`;

  const userPrompt = `RFQ Content:
${options.rfqContent}

Project Context:
${options.projectContext}

${options.instructions ? `Additional Instructions:\n${options.instructions}` : ''}

Generate a comprehensive bid proposal in HTML format.`;

  const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: systemPrompt },
      { role: "user", content: userPrompt },
    ],
    temperature: 0.7,
    max_tokens: 4000,
  });

  return completion.choices[0].message.content || "";
}

// Generate bid using Anthropic
export async function generateBidWithAnthropic(options: GenerateBidOptions): Promise<string> {
  if (!anthropic) {
    throw new Error("Anthropic API key not configured");
  }

  const systemPrompt = `You are an expert construction bid proposal writer. Generate a professional, detailed HTML bid response based on the provided RFQ and project context. Include:
- Executive Summary
- Project Understanding
- Proposed Approach
- Timeline
- Pricing Structure
- Team Qualifications
- Risk Mitigation

Use professional formatting and be persuasive while maintaining accuracy.`;

  const userPrompt = `RFQ Content:
${options.rfqContent}

Project Context:
${options.projectContext}

${options.instructions ? `Additional Instructions:\n${options.instructions}` : ''}

Generate a comprehensive bid proposal in HTML format.`;

  const message = await anthropic.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 4000,
    messages: [
      {
        role: "user",
        content: systemPrompt + "\n\n" + userPrompt,
      },
    ],
  });

  const content = message.content[0];
  return content.type === "text" ? content.text : "";
}

// Generate bid using Gemini
export async function generateBidWithGemini(options: GenerateBidOptions): Promise<string> {
  if (!gemini) {
    throw new Error("Google API key not configured");
  }

  const model = gemini.getGenerativeModel({ model: "gemini-2.0-flash-exp" });

  const prompt = `You are an expert construction bid proposal writer. Generate a professional, detailed HTML bid response.

RFQ Content:
${options.rfqContent}

Project Context:
${options.projectContext}

${options.instructions ? `Additional Instructions:\n${options.instructions}` : ''}

Include:
- Executive Summary
- Project Understanding
- Proposed Approach
- Timeline
- Pricing Structure
- Team Qualifications
- Risk Mitigation

Generate a comprehensive bid proposal in HTML format.`;

  const result = await model.generateContent(prompt);
  const response = await result.response;
  return response.text();
}

// Main bid generation function
export async function generateBid(model: AIModel, options: GenerateBidOptions): Promise<string> {
  switch (model) {
    case "openai":
      return generateBidWithOpenAI(options);
    case "anthropic":
      return generateBidWithAnthropic(options);
    case "gemini":
      return generateBidWithGemini(options);
    default:
      throw new Error(`Unsupported AI model: ${model}`);
  }
}

// Analyze RFP
export async function analyzeRFP(rfqContent: string): Promise<{
  qualityScore: number;
  clarityScore: number;
  doabilityScore: number;
  vendorRiskScore: number;
  overallRisk: string;
  findings: {
    redFlags: string[];
    opportunities: string[];
    missingDocuments: string[];
  };
  recommendations: Array<{
    title: string;
    description: string;
    priority: string;
    estimatedTime: string;
  }>;
}> {
  if (!openai) {
    throw new Error("OpenAI API key not configured");
  }

  const prompt = `Analyze this RFQ document and provide:
1. Quality Score (0-100): Completeness and professional quality
2. Clarity Score (0-100): Clear requirements and expectations
3. Doability Score (0-100): Feasibility of completing within constraints
4. Vendor Risk Score (0-100): Client reliability and payment risk
5. Overall Risk Level: low, medium, high, or critical
6. Red flags to watch out for
7. Opportunities to highlight
8. Missing documents that should be requested
9. Actionable recommendations

RFQ Content:
${rfqContent}

Respond in JSON format with the structure: { qualityScore, clarityScore, doabilityScore, vendorRiskScore, overallRisk, findings: { redFlags, opportunities, missingDocuments }, recommendations: [{ title, description, priority, estimatedTime }] }`;

  const completion = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: prompt }],
    response_format: { type: "json_object" },
    temperature: 0.3,
  });

  const result = JSON.parse(completion.choices[0].message.content || "{}");
  return result;
}

// Chunk text for embeddings
export function chunkText(text: string, chunkSize: number = 1000, overlap: number = 200): string[] {
  const chunks: string[] = [];
  let start = 0;

  while (start < text.length) {
    const end = start + chunkSize;
    chunks.push(text.slice(start, end));
    start = end - overlap;
  }

  return chunks;
}
