"use client";
import React, { useState } from "react";
import {
  fetchComponentData,
  transformAndRenderComponent,
} from "../utils/transformComponent";
import Artifact from "@/components/Artifact";
import { toBase64 } from "@/utils/common";
import ChatContainer from "@/components/ChatContainer";

export default function Home() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [prompt, setPrompt] = useState<string>("");
  const [dataset, setDataset] = useState<File | null>(null);
  const [initialStructure, setInitialStructure] = useState<boolean>(true);

  const handleSubmit = async () => {
    if (!prompt.trim() || !dataset) {
      setError("Both prompt and provided dataset must be filled.");
      return;
    }

    let b64Dataset = null;
    let datasetName = null;

    if (dataset) {
      b64Dataset = await toBase64(dataset);
      datasetName = dataset.name;
    }

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
      setError(null);
      setIsLoading(true);
      setInitialStructure(false);
      const data = await fetchComponentData(
        "http://localhost:8000/ui_component/generate",
        currentPrompt,
        b64Dataset as unknown as string,
        datasetName as string
      );

      const componentId = data.id;
      const componentJsx = data.component;
      const componentName = data.name;
      const rechartComponents = data.rechartComponents || undefined;

      const artifactContaienr = document.getElementById("artifact");
      if (artifactContaienr) {
        const componentDiv = document.createElement("div");
        componentDiv.id = componentId;
        componentDiv.className = "w-full";
        artifactContaienr.appendChild(componentDiv);
        console.log(artifactContaienr);
      }

      const result = transformAndRenderComponent(
        componentId,
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
    <div
      className={`min-h-screen bg-gray-900 p-6
    ${
      initialStructure ? "flex justify-center items-center" : "grid grid-rows-6"
    }`}
    >
      {!initialStructure && <Artifact />}
      <ChatContainer
        prompt={prompt}
        setPrompt={setPrompt}
        dataset={dataset}
        setDataset={setDataset}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
        message={error}
        setMessage={setError}
      />
    </div>
  );
}
