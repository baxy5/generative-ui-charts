"use client";
import React, { useState } from "react";
import {
  fetchComponentData,
  transformAndRenderComponent,
} from "../utils/transformComponent";

export default function Home() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [prompt, setPrompt] = useState<string>("");

  const handleComponentRender = async () => {
    setError(null);

    try {
      setIsLoading(true);

      const data = await fetchComponentData(
        "http://localhost:8000/component/generate",
        prompt
      );

      const componentJsx = data.component;
      const componentName = data.name;

      const result = transformAndRenderComponent(
        componentJsx,
        componentName,
        "artifact-component-container"
      );

      if (!result.success && result.error) {
        setError(result.error);

        const container = document.getElementById(
          "artifact-component-container"
        );
        if (container) {
          container.innerHTML = `<div style="color: red; padding: 20px;">${result.error}</div>`;
        }
      }
    } catch (err: unknown) {
      let errMsg = "Failed to fetch JSX from API.";
      if (err instanceof Error) {
        errMsg = `Failed to fetch JSX from API: ${err.message}`;
      } else if (typeof err === "string") {
        errMsg = `Failed to fetch JSX from API: ${err}`;
      }
      console.error(errMsg, err);
      setError(errMsg);

      const container = document.getElementById("artifact-component-container");
      if (container) {
        container.innerHTML = `<div style="color: red; padding: 20px;">Unable to generate chart. Please try again.</div>`;
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleTransformAndRender = async () => {
    setError(null);

    try {
      setIsLoading(true);

      const data = await fetchComponentData(
        "http://localhost:8000/rechart/generate",
        prompt
      );

      const componentJsx = data.component;
      const componentName = data.name;
      const rechartComponents = data.rechartComponents || undefined;

      // Transform and render the component
      const result = transformAndRenderComponent(
        componentJsx,
        componentName,
        "artifact-container",
        rechartComponents
      );

      // Handle any errors
      if (!result.success && result.error) {
        setError(result.error);

        const container = document.getElementById("artifact-container");
        if (container) {
          container.innerHTML = `<div style="color: red; padding: 20px;">${result.error}</div>`;
        }
      }
    } catch (err: unknown) {
      let errMsg = "Failed to fetch JSX from API.";
      if (err instanceof Error) {
        errMsg = `Failed to fetch JSX from API: ${err.message}`;
      } else if (typeof err === "string") {
        errMsg = `Failed to fetch JSX from API: ${err}`;
      }
      console.error(errMsg, err);
      setError(errMsg);

      const container = document.getElementById("artifact-container");
      if (container) {
        container.innerHTML = `<div style="color: red; padding: 20px;">Unable to generate chart. Please try again.</div>`;
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {/* Artifact containers */}
      <div className="flex flex-wrap gap-4 p-6">
        <div
          id="artifact-component-container"
          className={`w-full min-h-[23rem] h-full bg-gray-800 rounded-lg border border-gray-700 p-4
            ${isLoading ? "animate-pulse bg-gray-100" : ""}`}
        ></div>
        <div
          id="artifact-container"
          className={`w-full min-h-[23rem] h-full bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center
            ${isLoading ? "animate-pulse bg-gray-100" : ""}`}
        ></div>
      </div>

      {/* Chat */}
      <div className="p-6">
        <button
          onClick={handleComponentRender}
          className="mb-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
        >
          Generate Component
        </button>
        <div className="mb-4">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full p-3 bg-gray-800 text-white rounded-lg border border-gray-700 mb-2 outline-none"
            rows={2}
            placeholder="Enter your chart prompt here..."
          />
          <button
            onClick={handleTransformAndRender}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
          >
            Generate Chart
          </button>
        </div>
        {error && (
          <div className="mb-4 p-3 bg-red-700 text-white rounded-md">
            {error}
          </div>
        )}
      </div>

      {/* Chart prompt suggestions */}
      <div className="px-6 pb-6">
        <h3 className="text-white mb-2 font-medium">Try these prompts:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          <button
            onClick={() =>
              setPrompt(
                "Create a line chart showing cholesterol levels (total, HDL, LDL) across all test dates with different colored lines for each type."
              )
            }
            className="p-2 bg-gray-800 text-sm text-gray-300 rounded hover:bg-gray-700 text-left cursor-pointer"
          >
            Line chart: Track cholesterol levels over time
          </button>
          <button
            onClick={() =>
              setPrompt(
                "Create a bar chart comparing the most recent liver enzyme values (GOT, GPT, GGT, ALP) to their reference ranges."
              )
            }
            className="p-2 bg-gray-800 text-sm text-gray-300 rounded hover:bg-gray-700 text-left cursor-pointer"
          >
            Bar chart: Liver enzyme comparison
          </button>
        </div>
      </div>
    </div>
  );
}
