import * as Babel from "@babel/standalone";
import React from "react";
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
  ReferenceArea,
  Area,
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  AreaChart,
  ComposedChart,
  Scatter,
  ScatterChart,
  PieChart,
  Pie,
  Cell,
  Sector,
} from "recharts";
import ReactDOM from "react-dom/client";

interface TransformationResult {
  success: boolean;
  error?: string;
}

// A map of all recharts components that might be used
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
  Area: Area,
  ReferenceArea: ReferenceArea,
  Radar: Radar,
  RadarChart: RadarChart,
  PolarGrid: PolarGrid,
  PolarAngleAxis: PolarAngleAxis,
  PolarRadiusAxis: PolarRadiusAxis,
  AreaChart: AreaChart,
  ComposedChart: ComposedChart,
  Scatter: Scatter,
  ScatterChart: ScatterChart,
  PieChart: PieChart,
  Pie: Pie,
  Cell: Cell,
  Sector: Sector,
};

// TODO: Something still wrong with the rootsMap
/* You are calling ReactDOMClient.createRoot() on a container that has already been passed to createRoot() 
before. Instead, call root.render() on the existing root instead if you want to update it. */
const rootsMap: Record<string, ReactDOM.Root> = {};

/**
 * Transforms and renders a component from JSX string
 * @param componentJsx JSX string of the component
 * @param componentName Name of the component
 * @param rechartComponents Array of Recharts component names used
 * @param containerId ID of container element to render the component
 * @returns Object with success status and error message if any
 */
export function transformAndRenderComponent(
  componentJsx: string,
  componentName: string,
  rechartComponents?: string[]
): TransformationResult {
  try {
    const containerId = componentName;
    console.log("containerId", containerId);
    console.log("componentName", componentName);
    console.log("rechartComponents", rechartComponents);
    console.log("componentJsx", componentJsx);

    // Remove React and Recharts imports
    componentJsx = componentJsx.replace(
      /import React from ['"]react['"];?\s*/g,
      ""
    );

    componentJsx = componentJsx.replace(
      /import\s+\{\s*[^}]*\}\s+from\s+['"]recharts['"];?\s*/g,
      ""
    );

    // Transform JSX to JS using Babel
    const transformResult = Babel.transform(componentJsx, {
      presets: ["react"],
    });

    const transformedCode = transformResult.code;

    if (!transformedCode) {
      throw new Error("Babel transformation resulted in empty code.");
    }

    // Remove export statement and replace with return
    const codeWithoutExport = transformedCode.replace(
      new RegExp(`export default ${componentName};?`),
      `return ${componentName};`
    );

    // Get component arguments
    const componentArgs = ["React", ...(rechartComponents || [])].map(
      (name) => componentsMap[name as keyof typeof componentsMap]
    );

    // Create component factory function
    const componentFactory = new Function(
      "React",
      ...(rechartComponents || []),
      codeWithoutExport
    );

    const DynamicReactComponent = componentFactory(...componentArgs);

    if (typeof DynamicReactComponent !== "function") {
      throw new Error(
        "Transformation did not result in a callable component function."
      );
    }

    // Find container and render component
    const container = document.getElementById(containerId);
    if (!container) {
      throw new Error(`Container element with id '${containerId}' not found.`);
    }

    // Reuse existing root or create a new one
    let root: ReactDOM.Root;
    if (rootsMap[containerId]) {
      root = rootsMap[containerId];
    } else {
      root = ReactDOM.createRoot(container);
      rootsMap[containerId] = root;
    }

    // Render the component
    root.render(React.createElement(DynamicReactComponent));

    return { success: true };
  } catch (e: unknown) {
    let errorMessage = "An unknown error occurred.";
    if (e instanceof Error) {
      errorMessage = e.message;
    } else if (typeof e === "string") {
      errorMessage = e;
    }
    console.error("Error during JSX transformation or rendering:", e);
    return {
      success: false,
      error: `Transformation/Rendering Error: ${errorMessage}`,
    };
  }
}

export async function fetchComponentData(apiUrl: string, prompt: string) {
  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();

  return data;
}
