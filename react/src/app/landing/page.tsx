"use client";

import {
  fetchComponentData,
  transformAndRenderComponent,
} from "@/utils/transformComponent";
import React, { useState } from "react";

const Landing = () => {
  const [prompt, setPrompt] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit() {
    try {
      setIsLoading(true);

      const response = await fetchComponentData(
        "http://localhost:8000/appic/generate",
        prompt
      );

      const componentJsx = response.component;
      const componentName = response.name;

      transformAndRenderComponent(componentJsx, componentName, "artifact");
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col">
      {isLoading && (
        <div className="w-full p-6 space-y-6">
          <div className="h-[400px] bg-gray-700 rounded-lg animate-pulse"></div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="h-40 bg-gray-700 rounded-lg animate-pulse"></div>
            <div className="h-40 bg-gray-700 rounded-lg animate-pulse"></div>
            <div className="h-40 bg-gray-700 rounded-lg animate-pulse"></div>
          </div>

          <div className="p-6 bg-gray-700 rounded-lg animate-pulse">
            <div className="h-6 bg-gray-600 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-600 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-600 rounded w-full mb-2"></div>
            <div className="h-4 bg-gray-600 rounded w-5/6"></div>
          </div>
        </div>
      )}
      <div id="artifact" className="w-full h-full"></div>

      <div className="fixed bottom-0 left-0 right-0 p-4">
        <div className="max-w-md mx-auto bg-gray-800 rounded-lg shadow-md p-4">
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Type your message..."
              className="flex-grow p-2 rounded-lg bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-700"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <button
              onClick={handleSubmit}
              className="ml-2 px-4 py-2 bg-blue-700 text-white cursor-pointer rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-700"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;
