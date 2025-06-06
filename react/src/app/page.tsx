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

  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      const data = await fetchComponentData(
        "http://localhost:8000/rechart/generate",
        prompt
      );

      const componentJsx = data.component;
      const componentName = data.name;
      const rechartComponents = data.rechartComponents || undefined;

      const result = transformAndRenderComponent(
        componentJsx,
        componentName,
        "artifact",
        rechartComponents
      );

      if (!result.success && result.error) {
        setError(result.error);
      }
    } catch (err: unknown) {
      let errMsg = "";
      if (err instanceof Error) {
        errMsg = `Failed to fetch JSX from API: ${err.message}`;
      }
      console.error(errMsg, err);
    } finally {
      setIsLoading(false);
    }
  };

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
