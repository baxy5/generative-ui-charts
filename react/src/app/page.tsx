"use client";
import React, { useState } from "react";
import {
  fetchComponentData,
  transformAndRenderComponent,
} from "../utils/transformComponent";
import Chat from "@/components/Chat";
import SystemMessage from "@/components/SystemMessage";
import Artifact from "@/components/Artifact";

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

  const handleSubmit = () => {};

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col p-6">
      <Artifact />
      <div className="p-6">
        <SystemMessage message={error} />
        <Chat
          prompt={prompt}
          setPrompt={setPrompt}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
