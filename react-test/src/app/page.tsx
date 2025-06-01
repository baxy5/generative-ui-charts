"use client";
import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import * as Babel from "@babel/standalone";
import { Grid3X3, Plus } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  LineChart,
  Line,
  Legend,
} from "recharts";

export default function Home() {
  const [error, setError] = useState<string | null>(null);

  const handleTransformAndRender = async () => {
    setError(null);
    let componentJsx = "";
    let componentName = "";
    let rechartComponents = [];

    try {
      const response = await fetch("http://localhost:8000/generative-ui");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("data", data);

      componentJsx = data.message.component;
      componentName = data.message.name;
      rechartComponents = data.message.rechartComponents;
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
        container.innerHTML = `<div style=\"color: red; padding: 20px;\">${errMsg}</div>`;
      }

      return;
    }

    /* if (typeof Babel === "undefined" || typeof Babel.transform !== "function") {
      const errMsg =
        "Babel (from @babel/standalone) is not loaded or not available. Ensure it's installed and imported correctly.";
      console.error(errMsg);
      setError(errMsg);
      const container = document.getElementById("artifact-container");
      if (container) {
        container.innerHTML = `<div style=\"color: red; padding: 20px;\">${errMsg}</div>`;
      }
      return;
    } */

    try {
      // TODO: Remove the imports from the component in the ai response
      componentJsx = componentJsx.replace(
        /import React from ['"]react['"];?\s*/g,
        ""
      );
      componentJsx = componentJsx.replace(
        /import\s+\{\s*[^}]*\}\s+from\s+['"]recharts['"];?\s*/g,
        ""
      );

      const transformResult = Babel.transform(componentJsx, {
        presets: ["react"],
      });

      const transformedCode = transformResult.code;
      console.log("Transformed Code:", transformedCode);

      if (!transformedCode) {
        throw new Error("Babel transformation resulted in empty code.");
      }

      const codeWithoutExport = transformedCode.replace(
        new RegExp(`export default ${componentName};?`),
        `return ${componentName};`
      );

      const componentsMap = {
        React: React,
        LineChart: LineChart,
        Line: Line,
        XAxis: XAxis,
        YAxis: YAxis,
        CartesianGrid: CartesianGrid,
        Tooltip: Tooltip,
        Legend: Legend,
        ResponsiveContainer: ResponsiveContainer,
        BarChart: BarChart,
        Bar: Bar,
      };

      const componentArgs = ["React", ...rechartComponents].map(
        (name) => componentsMap[name as keyof typeof componentsMap]
      );

      const componentFactory = new Function(
        "React",
        ...rechartComponents,
        codeWithoutExport
      );
      console.log("componentFactory", componentFactory);

      const DynamicReactComponent = componentFactory(...componentArgs);
      console.log("DynamicReactComponent type:", typeof DynamicReactComponent);
      console.log("DynamicReactComponent value:", DynamicReactComponent);

      if (typeof DynamicReactComponent !== "function") {
        throw new Error(
          "Transformation did not result in a callable component function."
        );
      }

      const container = document.getElementById("artifact-container");
      if (container) {
        const root = ReactDOM.createRoot(container);
        root.render(React.createElement(DynamicReactComponent));
      } else {
        const errMsg =
          "Artifact container (id='artifact-container') not found in the DOM.";
        console.error(errMsg);
        setError(errMsg);
      }
    } catch (e: unknown) {
      let errorMessage = "An unknown error occurred.";
      if (e instanceof Error) {
        errorMessage = e.message;
      } else if (typeof e === "string") {
        errorMessage = e;
      }
      console.error("Error during JSX transformation or rendering:", e);
      setError(`Transformation/Rendering Error: ${errorMessage}`);
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
