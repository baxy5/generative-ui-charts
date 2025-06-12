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
    if (!prompt.trim()) return;

    // Add user message to artifact container
    const artifactContainer = document.getElementById("artifact");
    if (artifactContainer) {
      const userMessageDiv = document.createElement("div");
      userMessageDiv.className = "flex justify-end w-full";
      userMessageDiv.id = "user-chat-message";
      userMessageDiv.innerHTML = `
        <div class="shrink-0 bg-secondary w-full max-w-[500px] border-2 border-[#13856c] px-4 py-2 rounded-t-lg rounded-bl-lg">
          <p class="font-bold">${prompt}</p>
        </div>
      `;
      artifactContainer.appendChild(userMessageDiv);
    }

    const currentPrompt = prompt;
    setPrompt("");

    try {
      setIsLoading(true);
      const data = await fetchComponentData(
        "http://localhost:8000/ui_component/generate",
        currentPrompt
      );

      const componentJsx = data.component;
      const componentName = data.name;
      const rechartComponents = data.rechartComponents || undefined;

      const artifactContaienr = document.getElementById("artifact");
      if (artifactContaienr) {
        const componentDiv = document.createElement("div");
        componentDiv.id = componentName;
        artifactContaienr.appendChild(componentDiv);
        console.log(artifactContaienr);
      }

      const result = transformAndRenderComponent(
        componentJsx,
        componentName,
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
