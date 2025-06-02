"use client";
import React, { useState } from "react";
import { Grid3X3, Plus } from "lucide-react";
import {
  fetchComponentData,
  transformAndRenderComponent,
} from "../utils/transformComponent";

export default function Home() {
  const [error, setError] = useState<string | null>(null);

  const handleTransformAndRender = async () => {
    setError(null);

    try {
      // Fetch component data from API
      const { componentJsx, componentName, rechartComponents } =
        await fetchComponentData();

      // Transform and render the component
      const result = transformAndRenderComponent(
        componentJsx,
        componentName,
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
        container.innerHTML = `<div style="color: red; padding: 20px;">${errMsg}</div>`;
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      <div className="p-6">
        <button
          onClick={handleTransformAndRender}
          className="mb-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
        >
          Transform JSX & Render Component
        </button>
        {error && (
          <div className="mb-4 p-3 bg-red-700 text-white rounded-md">
            {error}
          </div>
        )}
      </div>

      {/* Chart placeholder container */}
      <div className="flex-1 p-6">
        <div
          id="artifact-container"
          className="w-full h-96 bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center"
        >
          <div className="text-gray-400 text-center">
            <Grid3X3 className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p className="text-sm">Chart will be displayed here</p>
          </div>
        </div>
      </div>

      {/* Chat interface */}
      <div className="p-6">
        <div className="max-w-4xl mx-auto">
          <div className="bg-gray-800 rounded-2xl border border-gray-700 p-4">
            <div className="flex items-center gap-3">
              <button className="p-2 hover:bg-gray-700 rounded-lg transition-colors">
                <Plus className="w-5 h-5 text-gray-400" />
              </button>

              <div className="flex-1 flex items-center gap-3">
                <input
                  type="text"
                  placeholder="Appic"
                  className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-lg"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
